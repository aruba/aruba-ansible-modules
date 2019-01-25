# aruba-ansible-modules
All Ansible modules, module installer, and sample playbooks for ArubaOS-Switch and ArubaOS-CX.

## Structure

* ArubaOS-CX and ArubaOS-Switch Ansible modules and files are stored in aos_wired_module_installer/src.
* ArubaOS-CX Ansible playbook examples are stored in example_playbooks/arubaoss
* ArubaOS-Switch Ansible playbook examples are stored in example_playbooks/arubaoscx
* Documentation of ArubsOS-CX and ArubaOS-Switch modules are located in module_documentation/ 

# How to Install Modules
The aos_wired_module_installer.py tool installs all files/directories required by Ansible for Aruba-OS Switch and CX integration.

## Requirements

* Linux operating system
* Python 2.7
* Ansible version 2.5 or later

## Files/Directories Installed

* Directories added:
  * <ansible_module_path>/modules/network/arubaoss
  * <ansible_module_path>/modules/network/arubaoscx
  * <ansible_module_path>/module_utils/network/arubaoss
* Files added/modified:
  * <ansible_module_path>/plugins/action/arubaoss.py
  * <ansible_module_path>/plugins/connection/arubaoscx_rest.py
  * <ansible_module_path>/config/base.yml



## How to run this code
From command line:    
```bash
$ python aos_wired_module_installer.py
```
If you receive a permission error, use 'sudo':
```bash
$ sudo python aos_wired_module_installer.py
```

In order to run these scripts, please complete the steps below:
1. Install Python version 2.7 on the system.

2. Install Ansible 2.5 or later (refer https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html).
 
## Optional Arguments
```
optional arguments:
  -h, --help    show this help message and exit
  -r, --remove  remove all files & directories installed by this script.
  --cx          only install files/directories required for ArubaOS-CX.
  --switch      only install files/directories required for ArubaOS-Switch.
```

# How to Run a Playbook
Below you'll find step by step instructions on how to run an example playbook on your ArubaOS-Switch or CX device.
## Prerequisites
Follow the above steps to install the ArubaOS-CX and ArubaOS-Switch Ansible modules.

### ArubaOS-CX
1. Assign an IP address to the management interface of your CX device. Ensure that the IP address is reachable
from your Ansible control machine.
2. Enable REST on your CX device with the following commands:
    ```
    switch(config)# https-server rest access-mode read-write
    switch(config)# https-server vrf mgmt
    ```
3. Modify the IP address in the hosts file example_playbooks/arubaoscx/cx_hosts.yml to match the IP of your CX device.
4. Modify the ansible_user and ansible_password in the hosts file example_playbooks/arubaoscx/cx_hosts.yml to match the login information of your CX device.

    
### ArubaOS-Switch
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
To execute a playbook run the following command from the Linux machine, replace playbook_file with the desired playbook and either cx_hosts.yml or switch_hosts.yml:  
```bash
$ ansible-playbook [playbook_file] -i [cx_hosts.yml|switch_hosts.yml]
```
