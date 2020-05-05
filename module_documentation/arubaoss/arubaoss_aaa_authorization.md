# AAA Authorization

Module: ****arubaoss_aaa_authorization****  
Description: implements rest api for AAA Authorization configuration

##### ARGUMENTS
    command:
        description: To configure a specific feature on AAA authorization
        choices=["authorization_group","authorization_method"]
        required: False
        default="authorization_method"
    authorization_method:
        description: To authorization method needed
        choices: AZM_NONE, AZM_TACACS
        required: False
    group_name:
        description: Group name for the autorization group
        type: 'str'
    seq_num:
        description: The sequence number. <1-2147483647>
        type: 'int'
    match_cmd:
        description: Specify the command to match.
        type: 'str'
    cmd_permission:
        description: Permit or deny the match command
        choices=["AZP_PERMIT","AZP_DENY"]
        required: False
        default="AZP_PERMIT"
    is_log_enabled:
        description: Generate an event log any time a match happens.
        choices: [True, False]
        required=False
        default=False
    config:
        description: To config or unconfig the required command
        choices: create, delete


##### EXAMPLES
```YAML
     - name: Updates the given console authorization configuration to the system
       arubaoss_aaa_authorization:
         authorization_method: "AZM_TACACS"

      - name: Create Authorization group
        arubaoss_aaa_authorization:
          command: authorization_group
          group_name: "cool"
          seq_num: 500
          match_cmd: "show running-config"
          cmd_permission: "AZP_PERMIT"
          is_log_enabled: "true"

      - name: Create Authorization group
        arubaoss_aaa_authorization:
          command: authorization_group
          group_name: "cool"
          seq_num: 600
          match_cmd: "show version"
          cmd_permission: "AZP_DENY"
          is_log_enabled: "false"

      - name: Delete Authorization group
        arubaoss_aaa_authorization:
          command: authorization_group
          group_name: "cool"
          seq_num: 500
          config: "delete"
```