# ArubaOS Switching Modules + Ansible FAQ

* How do I debug a failing playbook?

    * Whenever an execution fails, the next step should be to re-execute the playbook
    using the `-v` option for verbosity. Increasing verbosity causes increasing
    levels of detail in the error messages which helps in determining the root
    cause of the Ansible playbook execution failure. You can increase the level of verbosity by adding more
    “v"’s and you can use up to 4 “v"’s: `-vvvv`
        ```
        ansible-control-machine$ansible-playbook system_attributes.yml -i switch_hosts.yml -vvvv
        ```
    * Ansible provides multiple options for debugging. Check out Ansible's
    documentation on [debugging playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks_debugger.html) and
    using the the [debug module](https://docs.ansible.com/ansible/latest/modules/debug_module.html) to print debugging statements
    during execution.


## Environment FAQ

* How do I setup my environment to use the Aruba Switching Modules?

    * Check out our video that describes [how to install Ansible and the Aruba Switching Modules](https://youtu.be/VFKJQZS-YXs?t=171)
    and read our [README.md](https://github.com/aruba/aruba-ansible-modules/blob/master/README.md).  

* I'm receiving an error `ERROR! no action detected in task. This often indicates a misspelled module name, or incorrect module path.`:
    ```
    ansible-control-machine$ansible-playbook system_attributes.yml -i switch_hosts.yml
    ERROR! no action detected in task. This often indicates a misspelled module name, or incorrect module path.
    
    The error appears to have been in '/ws/aruba-switch-ansible-modules/example_playbooks/arubaoss/system_attributes.yml': line 4, column 8, but may
    be elsewhere in the file depending on the exact syntax problem.
    
    The offending line appears to be:
    
      tasks:
         - name: Update Switch System Attributes
           ^ here
    ```
 
    * This error can be due to Ansible not being able to locate your Aruba Switching Modules.
Follow the below steps to resolve this issue:
        * **Resolution:**  Reinstall the Aruba Switching Modules. To uninstall the modules,
        navigate to the directory of the **aos_wired_module_installer** and execute the following command:
            * To uninstall: `sudo python aos_wired_module_installer.py -r`
            * To install: `sudo python aos_wired_module_installer.py`

### ___________________________________________________________________________

* I'm receiving the following error `Request failed: <urlopen error [Errno -2] Name or service not known>", "status": -1, "url": "http://None:80/rest/version`:

    ```
    ansible-control-machine$ansible-playbook system_attributes.yml -i switch_hosts.yml
    
    PLAY [switch1] ******************************************************************************************************************************************************************************************
    
    TASK [Gathering Facts] **********************************************************************************************************************************************************************************
    ok: [switch1]
    
    TASK [Update Switch System Attributes] ******************************************************************************************************************************************************************
    fatal: [switch1]: FAILED! => {"changed": false, "msg": "Request failed: <urlopen error [Errno -2] Name or service not known>", "status": -1, "url": "http://None:80/rest/version"}
            to retry, use: --limit @/ws/aruba-switch-ansible-modules/example_playbooks/arubaoss/system_attributes.retry
    
    PLAY RECAP **********************************************************************************************************************************************************************************************
    switch1                    : ok=1    changed=0    unreachable=0    failed=1
    ```

    * This error can be due to your Ansible version not being 2.5 or later: 
        * **Resolution:**  Run `ansible --version` and validate you have Ansible version 2.5 or later (2.7 preferred)
        * **Resolution:**  Reinstall the Aruba Switching Modules. To uninstall the modules,
        navigate to the directory of the **aos_wired_module_installer** and execute the following command:
            * To uninstall: `sudo python aos_wired_module_installer.py -r`
            * To install: `sudo python aos_wired_module_installer.py`

## Inventory FAQ

* I'm receiving error `Request failed: <urlopen error [Errno -2] Name or service not known>` OR `SSH Error: data could not be sent to remote host`:

    ```
    ansible-control-machine$ansible-playbook system_attributes.yml -i switch_hosts.yml
    
    PLAY [switch1] ******************************************************************************************************************************************************************************************
    
    TASK [Gathering Facts] **********************************************************************************************************************************************************************************
    ok: [switch1]
    
    TASK [Update Switch System Attributes] ******************************************************************************************************************************************************************
    fatal: [switch1]: FAILED! => {"changed": false, "msg": "Request failed: <urlopen error [Errno -2] Name or service not known>", "status": -1, "url": "http://[u'10.6.6.18']:80/rest/version"}
            to retry, use: --limit @/ws/aruba-switch-ansible-modules/example_playbooks/arubaoss/system_attributes.retry
    
    PLAY RECAP **********************************************************************************************************************************************************************************************
    switch1                    : ok=1    changed=0    unreachable=0    failed=1    
    ```
    
    ```
    ansible-control-machine$ansible-playbook system_attributes.yml -i switch_hosts.yml
    
    PLAY [switch1] ******************************************************************************************************************************************************************************************
    
    TASK [Gathering Facts] **********************************************************************************************************************************************************************************
     [WARNING]: sftp transfer mechanism failed on [10.6.6.18]. Use ANSIBLE_DEBUG=1 to see detailed information
    
     [WARNING]: scp transfer mechanism failed on [10.6.6.18]. Use ANSIBLE_DEBUG=1 to see detailed information
    
    fatal: [switch1]: UNREACHABLE! => {"changed": false, "msg": "SSH Error: data could not be sent to remote host \"10.6.6.18\". Make sure this host can be reached over ssh", "unreachable": true}
            to retry, use: --limit @/ws/aruba-switch-ansible-modules/example_playbooks/arubaoss/system_attributes.retry
    
    PLAY RECAP **********************************************************************************************************************************************************************************************
    switch1                    : ok=0    changed=0    unreachable=1    failed=0
    ```

    * These errors are most likely due to your Inventory file being incorrectly formatted 
    or missing the static variables `ansible_connection` and `ansible_network_os`.
    However you're formatting your inventory, ensure the variables for your host are
    similar to what's below:
        * **Resolution:** :
        ```yaml
        all:
          hosts:
            switch1:
              ansible_host: 10.6.6.18
              ansible_user: admin
              ansible_password: admin
              ansible_connection: local  # Do not change
              ansible_network_os: arubaoss  # Do not change
        ```

## Playbook FAQ

* I'm receiving a `Error 400 response "Bad Request Please login to access the resource.`:

    ```
    ansible-control-machine$ansible-playbook system_attributes.yml -i switch_hosts.yml
    
    PLAY [switch1] ******************************************************************************************************************************************************************************************
    
    TASK [Gathering Facts] **********************************************************************************************************************************************************************************
    ok: [switch1]
    
    TASK [Update Switch System Attributes] ******************************************************************************************************************************************************************
    fatal: [switch1]: FAILED! => {"body": "<HTML><TITLE>400 Bad Request</TITLE><H1>Bad Request</H1>Please login to access the resource.<P></HTML>", "changed": false, "connection": "close", "content-length": "102", "content-type": "text/html", "msg": "HTTP Error 400: Bad Request", "server": "eHTTP v2.0", "status": 400, "url": "http://10.6.6.18:80/rest/version"}
            to retry, use: --limit @/ws/aruba-switch-ansible-modules/example_playbooks/arubaoss/system_attributes.retry
    
    PLAY RECAP **********************************************************************************************************************************************************************************************
    switch1                    : ok=1    changed=0    unreachable=0    failed=1
    ```

* The above error could be due to one of the following:
    * The login information in your inventory file is not correct
        * **Resolution:** Provide the switch's login information in your inventory file by
        setting the variables `ansible_user` and `ansible_password`. See above for an example.
        If you prefer not to store your variables in plaintext, look into [Ansible's Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html)
         feature or [passing the variables from the command line](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#passing-variables-on-the-command-line).
     
    * Your ArubaOS-Switch has the **operator password** set on the device after
    firmware version 16.08. This is because during the execution of each module, the ArubaOS-Switch modules execute a 
    REST GET request to the switch to retrieve all the supported REST API versions of the switch. We're currently looking into
    fixing this behavior, but we do have a workaround:
        * **Workaround:** provide the variable `api_version` to each module call like so:
        ```yaml
        - name: Configure Interface 11 Description
          arubaoss_interface:
            interface: 11
            description: UPLINK_INTERFACE
            api_version: v6.0
        ```

* I want to have the modules use SSL or HTTPS only, how do I do that? :
    * The modules accept a parameter `use_ssl`, and when set to `True`, that task will use HTTPS and port 443 
    when executing the REST API calls. To have the modules use SSL or HTTPS, set `use_ssl` to `True` for each 
    module call. At this time the modules use HTTP to gather the supported REST API versions of the device,
    so you'll also have to pass in the `api_version` to each module as well:
    ```yaml
     - name: Update Switch System Attributes
       arubaoss_system_attributes:
         hostname: "Edge-AOSS-1"
         location: "Santa Clara"
         contact: "9253237651"
         domain_name: "hpe.com"
         api_version: v5.0
         use_ssl: True
       
     - name: Configure Public snmp Community
       arubaoss_snmp:
         community_name: public
         access_type: UT_OPERATOR
         restricted: False
         api_version: v5.0
         use_ssl: True
     ```  