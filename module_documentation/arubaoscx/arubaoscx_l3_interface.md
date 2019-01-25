# L3 Interface
Module: ****arubaoscx_l3_interface****  
Description: "This module implements Layer3 interface configuration for ArubaOS_CX switch"

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
    ipv4:
        description: The IPv4 address and subnet mask in the address/mask format.
                     The first entry in the list is the primary IPv4, the remainings are secondary IPv4.
        type: list
        required: False
    ipv6:
        description: The IPv6 address and subnet mask in the address/mask format.
                     It takes multiple IPv6 with comma separated in the list.
        type: list
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
    aclv4_out:
        description: Attaching egress IPv4 ACL to interface.
        type: string
        required: False
    vrf:
        description: Attaching interface to VRF, commonly known as Virtual Routing and Forwarding.
                     The interface will be attached to default vrf if not specified.
        type: string
        required: False
    ip_helper_address:
        description: Configure a remote DHCP server/relay IP address on the device interface. Here the
                     helper address is same as the DHCP server address or another intermediate DHCP relay.
        type: list
        required: False
    state:
        description: Create/Update or Delete interface
        default: 'present'
        choices: ['present', 'absent']
        required: False

##### EXAMPLES
```YAML
     - name: Adding new interface
       arubaoscx_l3_interface:
         interface: "{{ item.interface }}"
         description: "{{ item.description }}"
       with_items:
         - { interface: 1/1/3, description: 'This is interface 1/1/3' }
         - { interface: 1/1/4, description: 'This is interface 1/1/4' }
     - name: Attaching IP addresses to interface
       arubaoscx_l3_interface:
         interface: "{{ item.interface }}"
         ipv4: "{{ item.ipv4 }}"
         ipv6: "{{ item.ipv6 }}"
       with_items:
         - { interface: 1/1/3, ipv4: ['1.2.3.4/24', '1.3.4.5/24'], ipv6: ['2000:db8::1234/32', '2001:db8::1234/32'] }
         - { interface: 1/1/4, ipv4: ['1.4.5.6/24', '1.5.6.7/24'], ipv6: ['2002:db8::1234/32', '2003:db8::1234/32'] }
     - name: Attaching QoS to interface
       arubaoscx_l3_interface:
         interface: "{{ item.interface }}"
         qos_rate: "{{ item.qos_rate }}"
         qos_schedule_profile: "{{ item.qos_schedule_profile }}"
       with_items:
         - { interface: 1/1/3, qos_rate: {'unknown-unicast': 100pps, 'broadcast': 200pps, 'multicast': 200pps}, qos_schedule_profile: dwrr }
         - { interface: 1/1/4, qos_rate: {'unknown-unicast': 100pps, 'broadcast': 200pps, 'multicast': 200pps}, qos_schedule_profile: dwrr }
     - name: Attaching ACL to interface
       arubaoscx_l3_interface:
         interface: "{{ item.interface }}"
         aclv4_in: "{{ item.aclv4_in }}"
         aclv6_in: "{{ item.aclv6_in }}"
         aclmac_in: "{{ item.aclmac_in }}"
         aclv4_out: "{{ item.aclv4_out }}"
       with_items:
         - { interface: 1/1/3, aclv4_in: ipv4test1, aclv6_in: ipv6test1, aclmac_in: mactest1, aclv4_out: ipv4egress1 }
         - { interface: 1/1/4, aclv4_in: ipv4test2, aclv6_in: ipv6test2, aclmac_in: mactest2, aclv4_out: ipv4egress2 }
     - name: Attaching user configured VRF to interface
       arubaoscx_l3_interface:
         interface: "{{ item.interface }}"
         vrf: "{{ item.vrf }}"
       with_items:
         - { interface: 1/1/3, vrf: myvrf }
         - { interface: 1/1/4, vrf: myvrf }
     - name: Attaching IP helper address to interface
       arubaoscx_l3_interface:
         interface: "{{ item.interface }}"
         ip_helper_address: "{{ item.ip_helper_address }}"
       with_items:
         - { interface: 1/1/3, ip_helper_address: ['5.6.7.8', '10.10.10.10'] }
         - { interface: 1/1/4, ip_helper_address: 1.2.3.4 }
     - name: Adding new interface with IP, QoS, ACL, VRF attached
       arubaoscx_l3_interface:
         interface: "{{ item.interface }}"
         description: "{{ item.description }}"
         ipv4: "{{ item.ipv4 }}"
         ipv6: "{{ item.ipv6 }}"
         qos_rate: "{{ item.qos_rate }}"
         qos_schedule_profile: "{{ item.qos_schedule_profile }}"
         aclv4_in: "{{ item.aclv4_in }}"
         aclv6_in: "{{ item.aclv6_in }}"
         aclmac_in: "{{ item.aclmac_in }}"
         aclv4_out: "{{ item.aclv4_out }}"
         vrf: "{{ item.vrf }}"
         ip_helper_address: "{{ item.ip_helper_address }}"
       with_items:
         - { interface: 1/1/3, description: 'This is interface 1/1/3',
             ipv4: ['1.2.3.4/24'], ipv6: ['2001:db8::1234/32'],
             qos_rate: {'unknown-unicast': 100pps, 'broadcast': 200pps, 'multicast': 200pps},
             qos_schedule_profile: dwrr, aclv4_in: ipv4test1, aclv6_in_type: ipv6test1,
             aclmac_in_type: mactest1, aclv4_out: ipv4egress1, vrf: myvrf, ip_helper_address: 10.10.10.10 }
         - { interface: 1/1/4, description: 'This is interface 1/1/4',
             ipv4: ['1.3.4.5/24'], ipv6: ['2001:db7::1234/32'],
             qos_rate: {'unknown-unicast': 100pps, 'broadcast': 200pps, 'multicast': 200pps},
             qos_schedule_profile: dwrr, aclv4_in: ipv4test2, aclv6_in_type: ipv6test2,
             aclmac_in_type: mactest2, aclv4_out: ipv4egress2, vrf: myvrf, ip_helper_address: 10.10.10.10 }
     - name: Deleting interface
       arubaoscx_l3_interface:
         interface: "{{ item.interface }}"
         state: "{{ item.state }}"
       with_items:
           - { interface: 1/1/3, state: absent }
           - { interface: 1/1/4, state: absent }

```