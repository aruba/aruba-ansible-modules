# AAA Accounting
Module: ****arubaoss_aaa_accounting****  
Description: "This implements rest apis which can be used to configure AAA Accounting"

##### ARGUMENTS
    cmd_accounting_method
        description: Method for commands Accounting Configuration
        type: str
        default: AME_NONE
        choices: AME_NONE, AME_TACACS, AME_RADIUS        
        required: False
    cmd_accounting_mode
        description: Mode for commands Accounting Configuration
        type: str
        default: AME_NONE
        choices: AMO_NONE, AMO_STOP_ONLY
        required: False
    ntwk_accounting_method
        description: Method for network Accounting Configuration
        type: str
        default: AME_NONE
        choices: AME_NONE, AME_TACACS, AME_RADIUS
        required: False
    ntwk_accounting_mode
        description: Mode for network Accounting Configuration
        type: str
        default: AME_NONE
        choices: AMO_NONE, AMO_STOP_ONLY, AMO_START_STOP
        required: False
    update_interval
        description: Update interval for accounting
        type: int
        default: 0
        required: False
    cmd_server_group
        description: Server Group name
        type: str
        default: None
        required: False
##### EXAMPLES
```YAML
     - name: Updates the given accounting configuration to the system
       arubaoss_aaa_accounting:
         cmd_accounting_method: "AME_TACACS"
         cmd_accounting_mode: "AMO_STOP_ONLY"
         ntwk_accounting_method: "AME_NONE"
         ntwk_accounting_mode: "AMO_NONE"
         update_interval: 10
```
