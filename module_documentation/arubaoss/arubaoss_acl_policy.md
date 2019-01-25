# ACL Policy
Module: arubaoss_acl_policy  
Description: "This implements rest apis which can be used to configure AAA Accounting"

## ARGUMENTS
    acl_name:
        description: Name for acl policy being configured.
        type: str
        required: True
    acl_type:
        description: Type of acl policy to be configured.
        type: str
        default: AT_STANDARD_IPV4
        choices: AT_STANDARD_IPV4, AT_EXTENDED_IPV4,
                 AT_CONNECTOIN_RATE_FILTER
        required: false
    acl_action:
        description: Type of action acl will take.
        required: false
        choices: AA_DENY, AA_PERMIT
    remark:
        description: Description for acl policy
        required: false
    acl_source_address:
        description: source ip address for acl policy type standard.
        required: false
    acl_source_mask:
        description: net mask for source acl_source_address
        required: false
    is_log:
        description: Enable/disable acl logging.
        required: false
    protocol_type:
        description: Protocol type for acl filter. Applicable for extended acl.
        required: false
        choices: 'PT_GRE','PT_ESP','PT_AH','PT_OSPF','PT_PIM','PT_VRRP',
                 'PT_ICMP','PTIGMP','PT_IP','PT_SCTP','PT_TCP','PT_UDP'
    icmp_type:
        description: Applies to icmp type matching this field. Only PT_ICMP
              protocol_type support icmp_code
        required: false
    icmp_code:
        description: Applies to icmp code matching this field. Only PT_ICMP
              protocol_type support icmp_code
        required: false
    igmp_type:
        description: Applies to igmp type matching this field. Only PT_IGMP
              protocol_type support igmp_type
        required: false
    is_connection_established:
        description: is_connection_established. Only PT_TCP  protocol_type
              support is_connection_established
        required: false
    match_bit:
        description: The set of tcp match bits . Only PT_TCP  protocol_type
              support match_bit
        required: false
    source_port:
        description: Applies to source port matching this filter. Only PT_SCTP,
              PT_TCP and PT_UDP Protocol types support source_port
        required: false
    destination_port:
        description:
            - Applies to destination port matching this filter. Only
              PT_SCTP,PT_TCP and PT_UDP Protocol types support destination_port
        required: false
    source_ip_address:
        description:
            - Applies to source IP Address/Subnet matching this extended acl filter
        required: false
    source_ip_mask:
        description:
            - Net mask source_ip_address
        required: false
    destination_ip_address:
        description:
            - Applies to destination IP Address/Subnet matching this extended acl filter
        required: false
    device_type:
        description:
            - Applies to device type matching this extended acl filter
        required: false
    application_type:
        description:
            - Applies to application matching this extended acl filter
        required: fasle
    precedence:
        description:
            - IP precedence flag
        required: false
        choices: 0, 1, 2, 3, 4, 5, 6, 7
    tos:
        description:
            - Tos value
        required: false
        choices: 0, 2, 4, 8
    sequece_no:
        description:
            - Sequence number for the acl policy configured
        required: false
    state:
        description:
            - Create or deletes acl policy.
        required: false
        default: create
        choices: create, delete
### EXAMPLES
```YAML
- name: Create Standard ACL 'global' w/ 20 permit 0.0.0.0 255.255.255.255
  arubaoss_acl_policy:
    acl_name: global
    sequence_no: 20
    acl_source_address: 0.0.0.0
    acl_source_mask: 255.255.255.255
    acl_action: AA_PERMIT

- name: Create Extended acl permit_all
  arubaoss_acl_policy:
    acl_name: permit_all
    source_ip_address: 0.0.0.0
    source_ip_mask: 255.255.255.255
    destination_ip_address: 0.0.0.0
    destination_ip_mask: 255.255.255.255
    acl_action: AA_PERMIT
    acl_type: AT_EXTENDED_IPV4

- name: Create Extended acl deny_all
  arubaoss_acl_policy:
    acl_name: deny_all
    source_ip_address: 0.0.0.0
    source_ip_mask: 255.255.255.255
    destination_ip_address: 0.0.0.0
    destination_ip_mask: 255.255.255.255
    protocol_type: PT_IP
    acl_action: AA_DENY
    acl_type: AT_EXTENDED_IPV4
```