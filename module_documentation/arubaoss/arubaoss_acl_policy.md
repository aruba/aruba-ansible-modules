# ACL Policy
Module: arubaoss_acl_policy  
Description: "This implements rest apis which can be used to configure AAA Accounting"

## ARGUMENTS
      acl_name:
        description:
            - Name for acl policy being configured.
        required: true
        type: str
      acl_type:
        description:
            - Type of acl policy to be configured.
        required: false
        default: AT_STANDARD_IPV4
        choices: ['AT_STANDARD_IPV4', 'AT_EXTENDED_IPV4',
                 'AT_CONNECTOIN_RATE_FILTER']
      acl_action:
        description:
            - Type of action acl rule will take, required when defining ACL rule.
        required: false
        choices: ['AA_DENY', 'AA_PERMIT']
        type: str
      remark:
        description: Description for acl policy
        required: false
        type: str
      acl_source_address:
        description: source ip address for acl policy type standard i.e 192.168.0.1, used with
          acl_type=AT_STANDARD_IPV4
        required: false
        type: str
      acl_source_mask:
        description: net mask for source acl_source_address in octet form i.e 255.255.255.0, used with
          acl_type=AT_STANDARD_IPV4
        required: false
        type: str
      is_log:
        description: Enable/disable acl logging.
        required: false
        type: bool
      protocol_type:
        description: Protocol type for acl filter. Applicable for extended acl.
        required: false
        choices: ['PT_GRE','PT_ESP','PT_AH','PT_OSPF','PT_PIM','PT_VRRP',
                 'PT_ICMP','PTIGMP','PT_IP','PT_SCTP','PT_TCP','PT_UDP']
      icmp_type:
        description: Applies to icmp type matching this field. Only PT_ICMP
              protocol_type support icmp_code
        default: -1
        required: false
        type: int
      icmp_code:
        description: Applies to icmp code matching this field. Only PT_ICMP
              protocol_type support icmp_code
        required: false
        default: -1
        required: false
        type: int
      igmp_type:
        description: Applies to igmp type matching this field. Only PT_IGMP
          protocol_type support igmp_type
        required: false
        choices: ['IT_HOST_QUERY',
                  'IT_HOST_REPORT','IT_DVMRP','IT_PIM','IT_TRACE','IT_V2_HOST_REPORT',
                  'IT_V2_HOST_LEAVE','IT_MTRACE_REPLY','IT_MTRACE_REQUEST','IT_V3_HOST_REPORT',
                  'IT_MROUTER_ADVERTISEMENT','IT_MROUTER_SOLICITATION','IT_MROUTER_TERMINATION']
      is_connection_established:
        description:  Match TCP packets of an established connection on ACL rule.
          Only PT_TCP protocol_type support is_connection_established
        required: false
        type: bool
      match_bit:
        description: The set of TCP match bits. Only PT_TCP protocol_type support match_bit.
          - MB_ACK : Match TCP packets with the ACK bit set.
          - MB_FIN : Match TCP packets with the FIN bit set
          - MB_RST : Match TCP packets with the RST bit set
          - MB_SYN : Match TCP packets with the SYN bit set
        required: false
        choices: ['MB_ACK','MB_FIN', 'MB_RST','MB_SYN']
      source_port:
        description: "Dictionary of ports to match on. Applies to source port matching this filter. Only PT_SCTP,
              PT_TCP and PT_UDP Protocol types support source_port. Maximum value for port_range_end is 65525.
              Dictionary containing the keys 'port_not_equal','port_range_start', 'port_range_end'. See below for examples.
              Used with acl_type=AT_EXTENDED_IPV4"
        required: false
        type: dict
      destination_port:
        description: "Dictionary of integer ports to match on. Applies to destination port matching this filter. Only PT_SCTP,
              PT_TCP and PT_UDP Protocol types destination source_port. Maximum value for port_range_end is 65525.
              Dictionary containing the keys 'port_not_equal','port_range_start', 'port_range_end' See below for examples.
              Used with acl_type=AT_EXTENDED_IPV4"
        required: false
        type: dict
      source_ip_address:
        description: Applies to source IP Address matching this extended acl filter, i.e 192.168.0.1.
          Used with acl_type=AT_EXTENDED_IPV4
        required: false
      source_ip_mask:
        description: Net mask source_ip_address in octet form i.e 255.255.255.0.
          Used with acl_type=AT_EXTENDED_IPV4
        required: false
      destination_ip_address:
        description: Applies to destination IP Address/Subnet matching this extended acl filter, i.e 192.168.0.1.
          Used with acl_type=AT_EXTENDED_IPV4
        required: false
      precedence:
        description: Match a specific IP precedence flag.
        required: false
        choices: [0, 1, 2, 3, 4, 5, 6, 7]
        type: int
      tos:
        description: Match a specific IP type of service flag - Tos value
        required: false
        choices: [0, 2, 4, 8]
        type: int
      sequence_no:
          description: Sequence number for the ACL rule to be configured
          required: false
          type: int
      state:
        description: Create or deletes acl policy.
        required: false
        default: create
        choices: ['create', 'delete']
### EXAMPLES
```YAML
- name: Create Standard ACL 'global' w/ 20 permit 0.0.0.0 255.255.255.255
  arubaoss_acl_policy:
    acl_name: global
    sequence_no: 20
    acl_source_address: 0.0.0.0
    acl_source_mask: 255.255.255.255
    acl_action: AA_PERMIT

- name: Create ip access-list extended permit_all with rule permit ip any any
  arubaoss_acl_policy:
    acl_name: permit_all
    source_ip_address: 0.0.0.0
    source_ip_mask: 255.255.255.255
    destination_ip_address: 0.0.0.0
    destination_ip_mask: 255.255.255.255
    acl_action: AA_PERMIT
    protocol_type: PT_IP
    acl_type: AT_EXTENDED_IPV4

- name: Create ip access-list extended permit_port_80 with rule permit tcp any eq 80
  arubaoss_acl_policy:
    acl_name: permit_port_80
    source_ip_address: 0.0.0.0
    source_ip_mask: 255.255.255.255
    protocol_type: PT_TCP
    source_port:
      port_not_equal: 0       # Set to 0
      port_range_start: 80    # Set to equal port
      port_range_end: 80      # Set to equal port
    destination_ip_address: 0.0.0.0
    destination_ip_mask: 255.255.255.255
    destination_port: {"port_not_equal": 0,"port_range_start": 80,"port_range_end": 80}
    acl_action: AA_PERMIT
    acl_type: AT_EXTENDED_IPV4

- name: Create ip access-list extended deny_all_ports_not_80 with rule deny tcp any neq 80
  arubaoss_acl_policy:
    acl_name: deny_all_ports_not_80
    source_ip_address: 0.0.0.0
    source_ip_mask: 255.255.255.255
    protocol_type: PT_TCP
    source_port:
      port_not_equal: 80       # Set to neq port
      port_range_start: 0
      port_range_end: 0
    destination_ip_address: 0.0.0.0
    destination_ip_mask: 255.255.255.255
    destination_port: {"port_not_equal": 80,"port_range_start": 0,"port_range_end": 0}
    acl_action: AA_PERMIT
    acl_type: AT_EXTENDED_IPV4

- name: Create ip access-list extended deny_all_ports_less_than_80 with rule deny tcp any lt 80
  arubaoss_acl_policy:
    acl_name: deny_all_ports_less_than_80
    source_ip_address: 0.0.0.0
    source_ip_mask: 255.255.255.255
    protocol_type: PT_TCP
    source_port:
      port_not_equal: 0       # Set to 0
      port_range_start: 1     # Start is 1
      port_range_end: 79      # End is port - 1
    destination_ip_address: 0.0.0.0
    destination_ip_mask: 255.255.255.255
    destination_port:
      port_not_equal: 0       # Set to 0
      port_range_start: 1     # Start is 1
      port_range_end: 79      # End is port - 1
    acl_action: AA_PERMIT
    acl_type: AT_EXTENDED_IPV4

- name: Create ip access-list extended deny_all_ports_gt_than_80 with rule deny tcp any gt 80
  arubaoss_acl_policy:
    acl_name: deny_all_ports_gt_than_80
    source_ip_address: 0.0.0.0
    source_ip_mask: 255.255.255.255
    protocol_type: PT_TCP
    source_port:
      port_not_equal: 0       # Set to 0
      port_range_start: 81    # Start is 1 + port
      port_range_end: 65535   # Highest port value is 65535
    destination_ip_address: 0.0.0.0
    destination_ip_mask: 255.255.255.255
    destination_port:
      port_not_equal: 0       # Set to 0
      port_range_start: 81    # Start is 1 + port
      port_range_end: 65535   # Highest port value is 65535
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