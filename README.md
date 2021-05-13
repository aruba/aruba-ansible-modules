:warning: :warning: :warning: :warning: :warning: 

**_This repository is deprecated._**

**_For all Aruba created Ansible content visit [ArubaNetworks on Galaxy](https://galaxy.ansible.com/arubanetworks)._**

**_For official AOS-Switch Ansible [Collection](https://galaxy.ansible.com/arubanetworks/aos_switch)._**  

**_For official Central Ansible [Role](https://galaxy.ansible.com/arubanetworks/aruba_central_role)._**  

**_For official WLAN Ansible [Role](https://galaxy.ansible.com/arubanetworks/aos_wlan_role)._**  

**_For official AOS-CX automation with Ansible guides and workflows visit Aruba's [Developer Hub](https://developer.arubanetworks.com/aruba-aoscx)._**  

:warning: :warning: :warning: :warning: :warning: 

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
* For AOS-Switch firmware version **16.08** and above is supported, for AOS-Switch setup instructions see [below](#how-to-run-a-playbook-on-aos-switch)


## How to run this code
Clone this repository onto your Linux machine:  
```bash
$ git clone https://github.com/aruba/aruba-ansible-modules.git
```
Enter the cloned directory and execute the python installer:  
```bash
$ cd aruba-ansible-modules
$ python aruba_module_installer/aruba_module_installer.py
```
If you receive a permission error, use 'sudo':
```bash
$ sudo python aruba_module_installer/aruba_module_installer.py
```

In order to run these scripts, please complete the steps below:
1. Install Python version 2.7 or 3.5+ on the system.

2. Install Ansible 2.5 or later (refer https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html).
 
## How to install updates or new modules
Enter the cloned directory and pull any updates from the repository:  
```bash
$ cd aruba-ansible-modules
$ git pull
```
Run the python installer with the `--reinstall` option, remember to use `sudo` if you receive a permission error:
```bash
$ sudo python aruba_module_installer/aruba_module_installer.py --reinstall
```

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

## SSH/CLI Modules
* To use the SSH/CLI modules `arubaoss_config` and `arubaoss_command`, SSH access must
 be enabled on your AOS-Switch device. It is enabled by default.
    * If necessary, re-enable SSH access on the device with the following command:
    ```
    switch(config)# ip ssh
    ```
* The control machine's `known_hosts` file must contain the target device's public key.
    * Alternatively, host key checking by the control machine may be disabled, although this is not recommended.
    * To disable host key checking modify the ansible.cfg file (default /etc/ansible/ansible.cfg) to include:
      `host_key_checking = false`

## Inventory Variables
The variables that should be defined in your inventory for your AOS-Switch host are:

* `ansible_host`: IP address of switch in `A.B.C.D` format. For IPv6 hosts use a string and enclose in square brackets E.G. `'[2001::1]'`.
* `ansible_user`: Username for switch in `plaintext` format
* `ansible_password`: Password for switch in `plaintext` format
* `ansible_network_os`: Must always be set to `arubaoss`
* `ansible_connection`: Set to `local` to use REST API modules, and to `network_cli` to use SSH/CLI modules
  * See [below](#using-both-rest-api-and-sshcli-modules-on-a-host) for info on using both REST API modules and SSH/CLI modules on a host


## Using Both REST API and SSH/CLI Modules on a Host

To use both REST API and SSH/CLI modules on the same host, 
you must create separate plays such 
that each play uses either only REST API modules or only SSH/CLI modules.
A play cannot mix and match REST API and SSH/CLI module calls.
In each play, `ansible_connection` must possess the appropriate value 
according to the modules used. 
If the play uses REST API modules, the value should be `local`. 
If the play uses SSH/CLI modules, the value should be `network_cli`.
 
A recommended approach to successfully using both types of modules for a host
is as follows:
1. Set the host variables such that Ansible will connect to the host using REST API.
2. In the playbook, in each play wherein the SSH/CLI
modules are used, set the `ansible_connection` to `network_cli`. 

The inventory should look something like this:

```yaml
all:
  hosts:
    switch1:
      ansible_host: 10.0.0.1
      ansible_user: admin
      ansible_password: password
      ansible_network_os: arubaoss
      ansible_connection: local  # REST API connection method
```

and the playbook like this (note how the second play, which uses the SSH/CLI module `arubaoss_command`,
sets the `ansible_connection` value accordingly):

```yaml
- hosts: all
  tasks:
    - name: Create VLAN 200
      arubaoss_vlan:
        vlan_id: 300
        name: "vlan300"
        config: "create"
        command: config_vlan

- hosts: all
  vars:
    ansible_connection: network_cli
  tasks:
    - name: Execute show run on the switch
      arubaoss_command:
        commands: ['show run']
```

```yaml
all:
  hosts:
    switch1:
      ansible_host: 10.0.0.1
      ansible_user: admin
      ansible_password: password
      ansible_network_os: arubaoss
      ansible_connection: local  # REST API connection method
```

# How to Run a Playbook on ArubaOS Controller
Follow the above steps to install the Aruba's Ansible modules. 

## Prerequisites
1. Install python request module "pip install requests".
2. Ensure that the IP address of the Aruba controllers are reachable from your Ansible machine.
3. Update variables.yml file with required variables like username, IP address and password.
4. Refer to the module_documentation folder for description of module arguments and example playbooks.


Contribution
-------
If you're interested in contributing please read and follow our [contribution documentation](https://github.com/aruba/aruba-ansible-modules/blob/master/CONTRIBUTING.md).


License
-------

Apache 2.0
