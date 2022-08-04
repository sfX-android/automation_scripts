# Ansible Automation (+Semaphore)

## about

These [Ansible](http://www.ansible.com) roles and playbooks are used together with [Semaphore](https://ansible-semaphore.com/) to provide a reliable CI/CD build system for my development around Android, TWRP, and more.


## background

Since several years I went with [Jenkins](https://www.jenkins.io) as my CI/CD tool of choice. <br/>Due to ongoing and re-curring issues and ofc the ressource hungry Jenkins process I've looked around for alternatives. There are some but they all come with either a lot of overhead or running e.g. in cloud only.

I am using [Ansible](http://www.ansible.com) since years already and thought why not using it as a CI/CD tool for my tasks? Mainly I have used Jenkins to execute shell commands anyways (besides the scheduling part and some smaller things around) so that makes Ansible a perfect replacement, imho.

There is one major drawback with Ansible: it comes without an UI. Yes there is AWX (OSS part of Ansible Tower) but it is RHEL/CentOS only and well I don't like being tight to a specific distribution. Yes there are (e.g Ansible) workarounds to get AWX running on e.g. Debian but really that does not work well at all - at least in my tests. Even though it would work 100% perfectly fine it is still a LOT of overhead coming with AWX - like with Jenkins.

After testing all other CI/CD tools I found it becomes clear I might have to live with Ansible and without an UI. Then I stumbled over the only reliable Open Source project at this time (yes I tried rundeck etc, too) which looks nice and is quite current: Semaphore. It has some disadvantages and not everything was working right out of the box (several documentation is still missing) but.. now it works perfectly fine - for me :)

There is one major drawback with semaphore though: one cannot enable read-only users for the UI: https://github.com/ansible-semaphore/semaphore/issues/891 so I cannot provide the UI to public. I hope that will be fixed one day but until then it will not be accessible from public internet.

If I ever find the time I will document the Semaphore part here as well but in the meantime if you want to re-produce this setup just ping me and I am happy to provide what's needed.
