# module: arubaoss_dsnoop

description: This module allows configuration of DHCP Snooping on AOS-Switch devices via REST API connection.

##### ARGUMENTS
```yaml
    command:
        description: To configure a specific feature on DHCP snooping
        choices: ["authorized_server","option_82", "dsnoop"]
        required: False
        default: "dsnoop"
    dsnoop:
        description: To enable or disable DHCP snooping.
        choices: [True, False]
        required: False
        default: False
    is_dsnoop_option82_enabled:
        description: To enable/disable adding option 82 relay information to DHCP client
                     packets that are forwarded on trusted ports
        choices: [True, False]
        required: False
        default: True
    remote_id:
        description: To select the address used as the Remote ID for option 82
        choices: ["DRI_MAC","DRI_SUBNET_IP", "DRI_MGMT_IP"]
        required: False
        default: "DRI_MAC"
    untrusted_policy:
        description: To set the policy for DHCP packets containing option 82 that are 
                     received on untrusted ports
        choices: ["DUP_DROP","DUP_KEEP", "DUP_REPLACE"]
        required: False
        default: "DUP_DROP"
    server_ip:
        description: Add an authorized DHCP server address.
        required: False
        default: ""
    config:
        description: To configure or unconfigure the required command
        choices: ["create", "delete"]
        default: "create"   
```

##### EXAMPLES
```yaml
- name: enable dsnoop
  arubaoss_dsnoop:
    dsnoop: true

- name: disable dsnoop
  arubaoss_dsnoop:
    dsnoop: false

- name: enable dsnoop option82 with untrusted-policy keep remote-id subnet-ip
  arubaoss_dsnoop:
    command: option_82
    is_dsnoop_option82_enabled: true
    remote_id: "DRI_SUBNET_IP"
    untrusted_policy: "DUP_KEEP"

- name: disable dsnoop option82
  arubaoss_dsnoop:
    command: option_82
    is_dsnoop_option82_enabled: false

- name: add dsnoop authorized_server
  arubaoss_dsnoop:
    command: authorized_server
    server_ip: "30.0.0.1"

- name: remove dsnoop authorized_server
  arubaoss_dsnoop:
    command: authorized_server
    server_ip: "30.0.0.1"
    config: "delete"
```