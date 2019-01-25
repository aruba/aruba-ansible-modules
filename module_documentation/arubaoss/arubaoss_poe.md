# POE
Module: ****arubaoss_poe****  
Description:  "This implements rest apis which can be used to configure PoE"

##### ARGUMENTS
    command:
        description: The module to be called.
        choices: reset_poe_port, config_poe_port and config_poe_slot
        required: False
    port_id:
        description: The Port id
        required: False
    is_poe_enabled:
        description: The port PoE status
        required: False
    poe_priority:
        description: The port PoE priority
        choices: PPP_CRITICAL, PPP_HIGH, PPP_LOW
        required: False
    poe_allocation_method:
        description: The PoE allocation method
        choices: PPAM_USAGE, PPAM_CLASS, PPAM_VALUE
        required: False
    allocated_power_in_watts:
        description: Allocated power value. Default value for this is
                     platform dependent
        required: False
    port_configured_type:
        description:  Port configured type
        required: False
    pre_standard_detect_enabled:
        description: pre_std_detect enable or disable
        required: False
    slot_name:
        description: The slot name
        required: False
    power_threshold_percentage:
        description: The power threshold percentage
        required: False

##### EXAMPLES
```YAML
     - name: Updates poe port
       arubaoss_poe:
         command: config_poe_port
         port_id: 2
         is_poe_enabled: True
         poe_priority: "PPP_HIGH"
         poe_allocation_method: "PPAM_VALUE"
         allocated_power_in_watts: 15
         port_configured_type: ""
         pre_standard_detect_enabled: False
```