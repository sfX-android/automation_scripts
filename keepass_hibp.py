#!/usr/bin/env python3
##################################################################################################################################################
# Copyright(c) 2025 by steadfasterX <steadfasterX #AT# binbash |dot| rocks>
#
# LICENSE: GPLv2
##################################################################################################################################################
# Requirements:
# - python pykeepass
# - hibp DB downloaded by https://github.com/oschonrock/hibp
# 
# Change:
# - hibpscmd: full path to the hibp search command
# - hibpdb: full path to your downloaded sha1 database
##################################################################################################################################################

import os
import hashlib
import subprocess
import argparse
import getpass
import threading
import itertools
import time
from pykeepass import PyKeePass
from concurrent.futures import ThreadPoolExecutor, as_completed

# change according to your setup
hibpscmd = '/opt/data/hibp/build/gcc/release/hibp-search'
hibpdb = '/opt/data/hibp/hibp_all.sha1.bin'

def generate_sha1_hash(password):
    return hashlib.sha1(password.encode('utf-8')).hexdigest()

def search_hibp(hash):
    result = subprocess.run([hibpscmd, hibpdb, hash], capture_output=True, text=True)
    return result.stdout

def process_entry(entry, verbose):
    if entry.password:
        sha1_hash = generate_sha1_hash(entry.password)
        hibp_result = search_hibp(sha1_hash)
        if "not found" in hibp_result:
            if verbose:
                return f"Password for entry '{entry.title}' not found in HIBP"
            return None
        elif "found" in hibp_result:
            try:
                count = hibp_result.split(':')[2].strip()
                url = entry.url if entry.url else "No URL"
                return f"Match found for entry '{entry.uuid}' - '{entry.title}' with URL '{url}'. Count: {count}"
            except IndexError:
                if verbose:
                    return f"Password for entry '{entry.title}' found but an error occurred parsing the result."
                return None
    return None

def spinner():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if not spinner_running:
            break
        print(f'\rOpening KeePassXC database (this can take a looong time)... {c}', end='', flush=True)
        time.sleep(0.1)
    print('\rOpening KeePassXC database... Done!', flush=True)

def main(db_path, verbose):
    kdb_password = getpass.getpass(prompt="Enter KeePassXC database password (press Enter to skip): ")
    keyfile_path = input("Enter KeePassXC keyfile path (press Enter to skip): ")

    if not kdb_password and not keyfile_path:
        print("Error: Either a password or a keyfile must be provided.")
        return

    global spinner_running
    spinner_running = True
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()

    try:
        if kdb_password and keyfile_path:
            kp = PyKeePass(db_path, password=kdb_password, keyfile=keyfile_path)
        elif kdb_password:
            kp = PyKeePass(db_path, password=kdb_password)
        elif keyfile_path:
            kp = PyKeePass(db_path, keyfile=keyfile_path)
    except Exception as e:
        spinner_running = False
        spinner_thread.join()
        print(f"\nError opening KeePassXC database: {e}")
        return

    spinner_running = False
    spinner_thread.join()

    entries = kp.entries
    total_entries = len(entries)
    print(f"Checking {total_entries} entries...")

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_entry, entry, verbose): entry for entry in entries}
        for index, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            if result:
                print(result)
            if verbose:
                print(f"Progress: {index}/{total_entries} entries checked.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check KeePassXC database passwords against the HIBP database.')
    parser.add_argument('db_path', help='Path to the KeePassXC database file')
    parser.add_argument('--verbose', action='store_true', help='Print details of all checks, including not found entries')
    args = parser.parse_args()

    main(args.db_path, args.verbose)
