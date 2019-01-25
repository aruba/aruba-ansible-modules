# L2 Interface
Module: ****arubaoscx_l2_interface****  
Description: "This module implements Layer2 Interface configuration for ArubaOS_CX switch"

##### ARGUMENTS
    interface:
        description: Interface name, should be alphanumeric and no more than about 8 bytes long.
        type: string
        required: true
    admin_state:
        description: Status information about interface.
        default: 'up'
        choices: ['up', 'down']
        required: False
    description:
        description: Description of interface.
        type: string
        required: False
    vlan_mode:
        description: VLAN mode of access or trunk.
        default: 'access'
        choices: ['access', 'trunk']
    vlan_id:
        description: VLAN attached to the interface.
        type: list
        required: False
    vlan_trunk_native_id:
        description: Native ID of trunk VLAN.
        type: string
        required: False
    vlan_trunk_native_tag:
        description: Switching trunk VLAN between "native_untagged" and "native_tagged".
        default: False
        bool: ['true', 'false']
        required: False
    qos_rate:
        description: The rate limit value configured for broadcast/multicast/unknown unicast traffic.
        type: dictionary
        required: False
    qos_schedule_profile:
        description: Attaching existing QoS schedule profile to interface.
        type: string
        required: False
    aclv4_in:
        description: Attaching ingress IPv4 ACL to interface.
        type: string
        required: False
    aclv6_in:
        description: Attaching ingress IPv6 ACL to interface.
        type: string
        required: False
    aclmac_in:
        description: Attaching ingress MAC ACL to interface.
        type: string
        required: False
    state:
        description: Create/Update or Delete interface.
        default: 'present'
        choices: ['present', 'absent']
        required: False

##### EXAMPLES
```YAML
     - name: Adding new interface
       arubaoscx_l2_interface:
         interface: "{{ item.interface }}"
         description: "{{ item.description }}"
       with_items:
         - { interface: 1/1/3, description: 'This is interface 1/1/3' }
         - { interface: 1/1/4, description: 'This is interface 1/1/4' }
     - name: Attaching VLAN to interface
       arubaoscx_l2_interface:
         interface: "{{ item.interface }}"
         vlan_mode: " {{ item.vlan_mode }}"
         vlan_id: "{{ item.vlan_id }}"
       with_items:
         - { interface: 1/1/3, vlan_mode: access, vlan_id: [1] }
         - { interface: 1/1/4, vlan_mode: trunk, vlan_id: [2,3,4] }
     - name: Attaching QoS to interface
       arubaoscx_l2_interface:
         interface: "{{ item.interface }}"
         vlan_mode: "{{ item.vlan_mode }}"
         qos_rate: "{{ item.qos_rate }}"
         qos_schedule_profile: "{{ item.qos_schedule_profile }}"
       with_items:
         - { interface: 1/1/3, vlan_mode: access, qos_rate: {'unknown-unicast': 100pps,
           'broadcast': 200pps, 'multicast': 200pps}, qos_schedule_profile: dwrr }
         - { interface: 1/1/4, vlan_mode: access, qos_rate: {'unknown-unicast': 100pps,
           'broadcast': 200pps, 'multicast': 200pps}, qos_schedule_profile: dwrr }
     - name: Attaching ACL to interface
       arubaoscx_l2_interface:
         interface: "{{ item.interface }}"
         vlan_mode: "{{ item.vlan_mode }}"
         aclv4_in: "{{ item.aclv4_in }}"
         aclv6_in: "{{ item.aclv6_in }}"
         aclmac_in: "{{ item.aclmac_in }}"
       with_items:
         - { interface: 1/1/3, vlan_mode: access, aclv4_in: ipv4test1, aclv6_in: ipv6test1, aclmac_in: mactest1 }
         - { interface: 1/1/4, vlan_mode: access, aclv4_in: ipv4test2, aclv6_in: ipv6test2, aclmac_in: mactest2 }
     - name: Adding new interface with VLAN, QoS, ACL attached
       arubaoscx_l2_interface:
         interface: "{{ item.interface }}"
         description: "{{ item.description }}"
         vlan_mode: "{{ item.vlan_mode }}"
         vlan_id: "{{ item.vlan_id }}"
         qos_rate: "{{ item.qos_rate }}"
         qos_schedule_profile: "{{ item.qos_schedule_profile }}"
         aclv4_in: "{{ item.aclv4_in }}"
         aclv6_in: "{{ item.aclv6_in }}"
         aclmac_in: "{{ item.aclmac_in }}"
       with_items:
         - { interface: 1/1/3, description: 'interface description', vlan_mode: access,
             vlan_id: [1], qos_rate: {'unknown-unicast': 100pps, 'broadcast': 200pps, 'multicast': 200pps},
             qos_schedule_profile: dwrr, aclv4_in: ipv4test1, aclv6_in_type: ipv6test1, aclmac_in_type: mactest1 }
         - { interface: 1/1/4, description: 'interface description', vlan_mode: trunk,
             vlan_id: [2,3,4], qos_rate: {'unknown-unicast': 100pps, 'broadcast': 200pps, 'multicast': 200pps},
             qos_schedule_profile: dwrr, aclv4_in: ipv4test2, aclv6_in_type: ipv6test2, aclmac_in_type: mactest2 }
     - name: Deleting interface
       arubaoscx_l2_interface:
         interface: "{{ item.interface }}"
         state: "{{ item.state }}"
       with_items:
           - { interface: 1/1/3, state: absent }
           - { interface: 1/1/4, state: absent }

```