# VLAN Interface
Module: ****arubaoscx_vlan_interface****  
Description: "This module implements VLAN interface configuration for ArubaOS_CX switch"

##### ARGUMENTS
    interface:
        description: Interface name, should be in form of 'vlan' + vlanid, eg. vlan2.
        type: string
        required: true
    admin_state:
        description: Admin status information about interface.
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
    vrf:
        description: Attaching interface to VRF, commonly known as Virtual Routing and Forwarding.
                     The interface will be attached to default VRF if not specified.
        type: string
        required: False
    ip_helper_address:
        description: Configure a remote DHCP server/relay IP address on the device interface. Here the
                     helper address is same as the DHCP server address or another intermediate DHCP relay.
        type: list
        required: False
    active_gateway_ip:
        description: For VSX and active-active routing, virtual gateway IPv4 address.
        type: string
        required: False
    active_gateway_mac_v4:
        description: VSX virtual gateway MAC address for the corresponding virtual gateway IPv4 address.
        type: string
        required: False
    state:
        description: Create/Update or Delete interface
        default: 'present'
        choices: ['present', 'absent']
        required: False

##### EXAMPLES
```YAML
     - name: Adding VLAN interface
       arubaoscx_vlan_interface:
         interface: "{{ item.interface }}"
         description: "{{ item.description }}"
       with_items:
         - { interface: vlan2, description: 'This is interface vlan2' }
         - { interface: vlan3, description: 'This is interface vlan3' }
     - name: Attaching IP addresses to interface
       arubaoscx_vlan_interface:
         interface: "{{ item.interface }}"
         ipv4: "{{ item.ipv4 }}"
         ipv6: "{{ item.ipv6 }}"
       with_items:
         - { interface: vlan2, ipv4: ['1.2.3.4/24', '1.3.4.5/24'], ipv6: ['2000:db8::1234/32', '2001:db8::1234/32'] }
         - { interface: vlan3, ipv4: ['1.4.5.6/24', '1.5.6.7/24'], ipv6: ['2002:db8::1234/32', '2003:db8::1234/32'] }
     - name: Attaching IP helper addresses to interface
       arubaoscx_vlan_interface:
         interface: "{{ item.interface }}"
         ip_helper_address: "{{ item.ip_helper_address }}"
       with_items:
         - { interface: vlan2, ip_helper_address: ['10.6.7.10'] }
         - { interface: vlan3, ip_helper_address: ['10.6.7.10', '10.10.10.10'] }
     - name: Attaching active gateway to interface
       arubaoscx_vlan_interface:
         interface: "{{ item.interface }}"
         active_gateway_ip: "{{ item.active_gateway_ip }}"
         active_gateway_mac_v4: "{{ item.active_gateway_mac_v4 }}"
       with_items:
         - { interface: vlan2, active_gateway_ip: '172.1.3.254', active_gateway_mac_v4: '98:F2:68:FF:B3:00' }
         - { interface: vlan3, active_gateway_ip: '172.1.3.254', active_gateway_mac_v4: '98:F2:68:FF:B3:00' }
     - name: Adding VLAN interface with IP addresses, VRF, IP helper address and active gateway
       arubaoscx_vlan_interface:
         interface: "{{ item.interface }}"
         description: "{{ item.description }}"
         ipv4: "{{ item.ipv4 }}"
         ipv6: "{{ item.ipv6 }}"
         vrf: "{{ item.vrf }}"
         ip_helper_address: "{{ item.ip_helper_address }}"
         active_gateway_ip: "{{ item.active_gateway_ip }}"
         active_gateway_mac_v4: "{{ item.active_gateway_mac_v4 }}"
       with_items:
         - { interface: vlan2, description: 'This is interface vlan2', ipv4: ['1.2.3.4/24'], ipv6: ['2001:db8::1234/32'], vrf: myvrf, ip_helper_address: ['10.6.7.10'], active_gateway_ip: '172.1.3.254', active_gateway_mac_v4: '98:F2:68:FF:B3:00' }
         - { interface: vlan3, description: 'This is interface vlan3', ipv4: ['1.2.4.5/24'], ipv6: ['2001:db7::1234/32'], vrf: myvrf, ip_helper_address: ['10.6.7.10'], active_gateway_ip: '172.1.3.254', active_gateway_mac_v4: '98:F2:68:FF:B3:00' }
     - name: Deleting interface
       arubaoscx_vlan_interface:
         interface: "{{ item.interface }}"
         state: "{{ item.state }}"
       with_items:
           - { interface: vlan2, state: absent }
           - { interface: vlan3, state: absent }

```