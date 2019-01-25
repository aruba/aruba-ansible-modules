# SNMP Trap
Module: ****arubaoss_snmp_trap****  
Description: "This implements rest api's which enable/disable snmp traps for different features on device"

##### ARGUMENTS
    arp_protect:
        description:
            - Traps for dynamic arp protection
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    aut_server_fail:
        description:
            - Traps reporting authentication server unreachable
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    dhcp_server:
        description:
            - Trpas for dhcp server
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    dhcp_snooping:
        description:
            - Traps for dhcp snooping
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    dhcpv6_snooping_out_of_resource:
        description:
            - Enable traps for dhcpv6 snooping out of resource
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    dhcpv6_snooping_errant_replies:
        description:
            - Traps for DHCPv6 snooping errant replies
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    dyn_ip_lockdown:
        description:
            - Traps for Dynamic Ip Lockdown
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    dyn_ipv6_ld_out_of_resources:
        description:
            - Enable traps for Dynamic IPv6 Lockdown out of resources
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    dyn_ipv6_ld_violations:
        description:
            - Enable traps for Dynamic IPv6 Lockdown violations.
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    login_failure_mgr:
        description:
            - Traps for management interface login failure
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    mac_count_notify:
        description:
            - Traps for MAC addresses learned on the specified ports exceeds the threshold
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    nd_snooping_out_of_resources:
        description:
            - The trap for nd snooping out of resources
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    password_change_mgr:
        description:
            - Traps for management interface password change
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    port_security:
        description:
            - Traps for port access authentication failure
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    startup_config_change:
        description:
            - Traps for changed to the startup config
        required: false
        default: STM_DISABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    macsec_failure:
        description:
            - Enable the MACsec Connectivity Association (CA) failure trap
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    mac_move_notify_mode:
        description:
            - Traps for move mac address table changes
        required: false
        default: STM_DISABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    mac_notify_mode:
        description:
            - Traps for mac notify
        required: false
        default: STM_DISABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    running_conf_change_trap:
        description:
            - Traps mode for running config change
        required: false
        default: STM_DISABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    snmp_authentication:
        description:
            - Select RFC1157 (standard) or HP-ICF-SNMP (extended) traps
        required: false
        default: SATM_EXTENDED
        choices: SATM_EXTENDED, SATM_STANDARD, SATM_NONE
    mac_notify_trap_interval:
        description:
            - Trap interval for mac_move_notify_mode and mac_notify_mode
        required: false
        default: 30
        choices: 0-120
    running_config_trap_interval:
        description:
            - Traps interval for running_conf_change_trap
        required: false
        default: 0
        choices: 0-120

##### EXAMPLES
```YAML
      - name: configure snmp trap
        arubaoss_snmp_traps:
          mac_move_notify_mode: "{{item}}"
        with_items:
          - STM_ENABLE
          - STM_DISABLE
```