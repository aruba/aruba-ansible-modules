# module: arubaoss_config

description: This module allows configuration of running-configs on AOS-Switch devices via SSH connection.

##### LIMITATIONS
* `arubaoss_config` is unable to match on custom prompts such as confirming a new password or banner message of the day  

##### ARGUMENTS
```yaml
  lines:
    description:
      - List of configuration commands to be executed. If "parents" is specified, these
        are the child lines contained under/within the parent entry. If "parents" is not 
        specified, these lines will be checked and/or placed under the global config level. 
        These commands must correspond with what would be found in the device's running-config.
    required: False
    type: list
  parents:
    description:
      - Parent lines that identify the configuration section or context under which the
        "lines" lines should be checked and/or placed. 
    required: False
    type: list
  src:
    description:
      - Path to the file containing the configuration to load into the device.  The path can 
        be either a full system path to the configuration file if the value starts with "/"
        or a path relative to the directory containing the playbook. This argument is mutually 
        exclusive with the "lines" and "parents" arguments. This src file must have same 
        indentation as a live switch config. The operation is purely additive, as it doesn't remove
        any lines that are present in the existing running-config, but not in the source config.
    required: False
    type: str
  before:
    description:
      - Commands to be executed prior to execution of the parent and child lines. This option
        can be used to guarantee idempotency.
    required: False
    type: list
  after:
    description:
      - Commands to be executed following the execution of the parent and child lines. This 
        option can be used to guarantee idempotency.
    required: False
    type: list
  match:
    description:
      - Specifies the method of matching. Matching is the comparison against the existing 
        running-config to determine whether changes need to be applied.
        If "match" is set to "line," commands are matched line by line.  
        If "match" is set to "strict," command lines are matched with respect to position.  
        If "match" is set to "exact," command lines must be an equal match.  
        If "match" is set to "none," the module will not attempt to compare the source 
        configuration with the running-config on the remote device.
    default: line
    choices: ['line', 'strict', 'exact', 'none']
    required: False
    type: str
  replace:
    description:
      - Specifies the approach the module will take when performing configuration on the 
        device. 
        If "replace" is set to "line," then only the differing and missing configuration lines 
        are pushed to the device. 
        If "replace" is set to "block," then the entire command block is pushed to the device 
        if there is any differing or missing line at all.
    default: line
    choices: ['line', 'block']
    required: False
    type: str
  backup:
    description:
      - Specifies whether a full backup of the existing running-config on the device will be 
        performed before any changes are potentially made. If the "backup_options" value is not 
        specified, the backup file is written to the "backup" folder in the playbook root 
        directory. If the directory does not exist, it is created.
    required: False
    type: bool
    default: False
  backup_options:
    description:
      - File path and name options for backing up the existing running-config. 
        To be used with "backup."
    suboptions:
      filename:
        description:
          - Name of file in which the running-config will be saved.
        required: False
        type: str
      dir_path:
        description:
          - Path to directory in which the backup file should reside.
        required: False
        type: str
    type: dict
  running_config:
    description:
      - Specifies an alternative running-config to be used as the base config for matching. The 
        module, by default, will connect to the device and retrieve the current running-config 
        to use as the basis for comparison against the source.  This argument is handy for times 
        when it is not desirable to have the task get the current running-config, and instead use
        another config for matching. 
    aliases: ['config']
    required: False
    type: str
  save_when:
    description:
      - Specifies when to copy the running-config to the startup-config. When changes are made to 
        the device running-configuration, the changes are not copied to non-volatile storage by default.  
        If "save_when" is set to "always," the running-config will unconditionally be copied to 
        startup-config.
        If "save_when" is set to "never," the running-config will never be copied to startup-config.
        If "save_when" is set to "modified," the running-config will be copied to startup-config 
        if the two differ.
        If "save_when" is set to "changed," the running-config will be copied to startup-config 
        if the task modified the running-config.
    default: never
    choices: ['always', 'never', 'modified', 'changed']
    required: False
    type: str
  diff_against:
    description:
      - When using the "ansible-playbook --diff" command line argument this module can generate 
        diffs against different sources. This argument specifies the particular config against 
        which a diff of the running-config will be performed. 
        If "diff_against" is set to "startup," the module will return the diff of the running-config 
        against the startup configuration.
        If "diff_against" is set to "intended," the module will return the diff of the running-config 
        against the configuration provided in the "intended_config" argument.
        If "diff_against" is set to "running," the module will return before and after diff of the 
        running-config with respect to any changes made to the device configuration.
    choices: ['startup', 'intended', 'running']
    required: False
    type: str
  diff_ignore_lines:
    description:
      - Specifies one or more lines that should be ignored during the diff. This is used to 
        ignore lines in the configuration that are automatically updated by the system. This 
        argument takes a list of regular expressions or exact commands.
    required: False
    type: list
  intended_config:
    description:
      - Path to file containing the intended configuration that the device should conform to, and 
        that is used to check the final running-config against. To be used with "diff_against," 
        which should be set to "intended."
    required: False
    type: str
```

##### EXAMPLES
```yaml
- name: First delete VLAN 44, then configure VLAN 45, and lastly create VLAN 46
  arubaoss_config:
    before: 
      - no vlan 44
    parents: 
      - vlan 45
    lines:
      - name testvlan
      - untagged 1-6
    after: 
      - vlan 46
- name: Back up running-config, then configure TACACS, and save running-config to startup-config if change was made
  arubaoss_config:
    backup: True
    lines: 
      - tacacs-server host 192.168.8.1 key "ArubaR0Cks!"
      - tacacs-server host 192.168.8.1 oobm
    backup_options:
      filename: backup.cfg
      dir_path: /users/Home/
    save_when: changed
- name: Compare running-config with saved config
  arubaoss_config:
    diff_against: intended
    intended_config: /users/Home/backup.cfg
- name: Configure VLAN 2345 and compare resulting running-config with previous running-config
  arubaoss_config:
    lines: 
      - vlan 2345
    diff_against: running
- name: Upload a config from local system file onto device
  arubaoss_config:
    src:  /users/Home/golden.cfg
- name: Update vlan 46, matching only if both "parents" and "lines" are present
  arubaoss_config:
    lines:
      - ip address 4.4.4.5/24
    parents: vlan 46
    match: strict
```