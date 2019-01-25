# Config Bkup

Module: ****arubaoss_config_bkup****
Description: "Implements Ansible module for switch configuration backup and restore."

##### ARGUMENTS
    file_name:
        description:
            - configuration file name
        required: true
    config_type:
        description:
            - Type of configuration file. If this option is used, configuration
              file is saved to the system.
        choices: CT_RUNNING_CONFIG, CT_STARTUP_CONFIG
        required: false
    server_type:
        description:
            - server type from/to which configuration needs to be copied
        choices: ST_FLASH, ST_TFTP, ST_SFTP
        required: false
    forced_reboot:
        description:
            - Apply the configuration with reboot if the configuration
              has reboot required commands
        required: false
    recovery_mode:
        description:
            - To enable or disable recovery mode. Not applicable if
              is_forced_reboot_enabled is true
        required: false
    server_name:
        description:
            - Server name in which file is stored. Not applicable for ST_FLASH.
        required: false
    server_ip:
        description:
            - Server ip address in which file is stored. Not applicable for
              ST_FLASH
        required: false
    sftp_port:
        description:
            - TCP port number. Applicable for ST_SFTP.
        default: 22
        required: false
    wait_for_apply:
        description:
            - Wait if there is already an ongoing configuration change on device.
        defualt: True
        required: false
    state:
        description:
            - Adding or reading data
        default: create
        required: false
    user_name:
            description: SFTP server Username
            required: false
    server_passwd:
            description: SFTP server password
            required: false
##### EXAMPLES
```YAML
      - name: backup configuration files
        arubaoss_config_bkup:
          file_name: test1
          server_type: ST_TFTP
          server_ip: 192.168.1.2
      - name: backup configuration files
        arubaoss_config_bkup:
          file_name: test1
          config_type: CT_RUNNING_CONFIG
```