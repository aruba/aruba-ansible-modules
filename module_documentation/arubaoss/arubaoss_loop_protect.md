# Loop Protect
Module: ****arubaoss_loop_protect****  
Description: "This configures loop protect on device over vlan or port"

##### ARGUMENTS
    command:
        description:
            - Type of action to be taken.
        required: true
    port_disable_timer:
        description:
            - Set the number of seconds before disabled ports are
              automatically re-enabled
        required: false
    trasmit_interval:
        description:
            - Set the number of seconds between loop detect packet transmissions.
        required: false
    mode:
        description:
            - Configures vlan or port mode
        required: false
        default: LPM_PORT
        choices: LPM_PORT, LPM_VLAN
    interface:
        description:
            - Interface id on which loop protect to be configured
        required: false
    receiver_action:
        description:
            - Set the action to take when a loop is detected.
              is_loop_protection_enabled must be true to update the receiver_action.
        required: false
        default: LPRA_SEND_DISABLE
        choices: LPRA_SEND_DISABLE, LPRA_NO_DISABLE, LPRA_SEND_RECV_DISABLE
    vlan:
        description:
            - Vlan id on which loop protect is to be configured
        required: false


##### EXAMPLES
```YAML
    - name: update loop
       arubaoss_loop_protect:
         command: update
         trap: True
     - name: enable loop-prtoect on port
       arubaoss_loop_protect:
         command: update_port
         interface: 1
     - name: disable loop-prtoect on port
       arubaoss_loop_protect:
         command: update_port
         interface: 1
         loop_protected: False
     - name: change loop-protect mode to vlan
       arubaoss_loop_protect:
         command: update
         mode: LPM_VLAN
     - name: enable loop-prtoect on vlan
       arubaoss_loop_protect:
         command: update_vlan
         vlan: 10
```