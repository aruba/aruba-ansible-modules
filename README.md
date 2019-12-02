# aruba-ansible-modules
All Ansible modules, module installer, and example playbooks for AOS-Switch and WLAN products.
 For AOS-CX modules please see our AOS-CX Ansible Role in [Ansible's Galaxy](https://galaxy.ansible.com/arubanetworks/aoscx_role).

## Structure

* AOS-Switch and WLAN Ansible modules and files are stored in [aruba_module_installer/library](https://github.com/aruba/aruba-ansible-modules/tree/master/aruba_module_installer/library).
* Documentation of Switching and WLAN Ansible modules are located in [module_documentation/](https://github.com/aruba/aruba-ansible-modules/tree/master/module_documentation) 
* Frequently Asked Questions are located in [FAQ.md](https://github.com/aruba/aruba-ansible-modules/blob/master/FAQ.md)
* AOS-Switch and WLAN Ansible playbook examples are stored in [example_playbooks/](https://github.com/aruba/aruba-ansible-modules/tree/master/example_playbooks)

# How to Install Modules
The aruba_module_installer.py tool installs all files/directories required by Ansible for AOS-Switch and WLAN integration.

## Requirements

* Linux operating system
* Python 2.7 or 3.5+
* Ansible version 2.5 or later
* For AOS-Switch firmware version **16.08** and above is supported


## How to run this code
From command line:    
```bash
$ python aruba_module_installer.py
```
If you receive a permission error, use 'sudo':
```bash
$ sudo python aruba_module_installer.py
```

In order to run these scripts, please complete the steps below:
1. Install Python version 2.7 or 3.5+ on the system.

2. Install Ansible 2.5 or later (refer https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html).
 
## Optional Arguments
```
optional arguments:
  -h, --help    show this help message and exit
  -r, --remove  remove all files & directories installed by this script.
  --reinstall   remove all files & directories installed by this script. Then
                re-install.
  --switch      only install files/directories required for AOS-Switch.
```

# How to Run a Playbook on AOS-Switch

## Prerequisites
Follow the above steps to install the AOS-Switch Ansible modules.
   
1. Assign an IP address to the management interface of your Switch device. Ensure that the IP address is reachable
from your Ansible control machine.
2. Enable REST on your Switch device with the following commands:
    ```
    switch(config)# web-management ssl
    switch(config)# rest-interface
    ```
3. Modify the IP address in the hosts file example_playbooks/arubaoss/switch_hosts.yml to match the IP of your Switch device.
4. Modify the ansible_user and ansible_password in the hosts file example_playbooks/arubaoss/switch_hosts.yml to match the login information of your Switch device.


### Executing a Playbook
To execute a playbook run the following command from the Linux machine, replace playbook_file with the desired playbook:  
```bash
$ ansible-playbook [playbook_file] -i switch_hosts.yml
```
