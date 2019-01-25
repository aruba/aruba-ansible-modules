# VLAN
Module: ****arubaoss_vlan****  
Description: "This implements rest apis which can be used to configure vlan"

##### ARGUMENTS
    command:
        description: Name of sub module, according to the configuration required.
        choices: config_vlan, config_vlan_port,
                config_vlan_ipaddress, config_vlan_dhcpHelperAddress
        required: True
    config:
        description: To config or unconfig the required command
        choices: create, delete
        required: False
    vlan_id:
        description: vlan id to be configured
        required: true
    name:
        description: Name of the VLAN. While creating a Vlan If name is given
        as empty string, default value (VLANx, where x is the vlan_id) will be
        configured. Empty string will not be accepted while modifying a Vlan
        required: false
    status:
        description: the status of the VLAN
        choices: VS_PORT_BASED, VS_PROTOCOL_BASED, VS_DYNAMIC
        required: false
    vlantype:
        description: The type of VLAN, default being VT_STATIC
        choices: VT_STATIC, VT_STATIC_SVLAN, VT_GVRP
        required: false
    is_jumbo_enabled:
        description:  Whether Jumbo is enabled
        required: false
    is_voice_enabled:
        description:  Whether Voice is enabled
        required: false
    is_dsnoop_enabled:
        description:  Whether DSNOOP is enabled
        required: false
    is_dhcp_server_enabled:
        description:  Whether DHCP server is enabled
        required: false
    is_management_vlan:
        description:  Whether vlan is a management vlan or not
        required: false
    ip_address_mode:
        description: IP Address Mode to be configured on vlan
        choices: IAAM_DISABLED, IAAM_STATIC, IAAM_DHCP
        required: False
    vlan_ip_address:
        description: IP Address to be configured on vlan
        required: False
    vlan_ip_mask:
        description: IP Mask for the IP Address configured
        required: False
    version:
        description: Version of IP Address
        choices: IAV_IP_V4. (V6 is not supported via REST)
        required: False
    helper_addresses:
        description: DHCP helper address for the corresponding VLAN id
        required: False
    port_id:
        description: Port ID to be configured on the vlan
        required: False
    port_mode:
        description: Port modes to be configured
        choices: POM_UNTAGGED, POM_TAGGED_STATIC, POM_FORBIDDEN
        required: False
    qos_policy:
        description: Qos policy to be added to vlan
        required: False
    acl_id:
        description: Acl policy to be added to vlan
        required: false
    acl_type:
        description: Type of acl policy
        default: AT_STANDARD_IPV4
        choices: AT_STANDARD_IPV4, AT_EXTENDED_IPV4, AT_CONNECTION_RATE_FILTER
        required: false
    acl_direction:
        description: Direction is which acl to be applied
        choices: AD_INBOUND, AD_OUTPUND, AD_CRF
        required: false

##### EXAMPLES
```YAML
     - name: configure vlan
       arubaoss_vlan:
         vlan_id: 300
         name: "vlan300"
         status: "VS_PORT_BASED"
         vlantype: "VT_STATIC"
         is_jumbo_enabled: false
         is_voice_enabled: false
         is_dsnoop_enabled: false
         is_dhcp_server_enabled: false
         is_management_vlan: false
         config: "create"
         command: config_vlan

```