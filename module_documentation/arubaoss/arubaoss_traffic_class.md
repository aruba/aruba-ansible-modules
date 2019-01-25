# Traffic Class
Module: ****arubaoss_traffic_class****  
Description: "This implements rest apis which can be used to configure Traffic Classes"

##### ARGUMENTS
    class_name:
        description:
            - Traffic class name
        required: true
    class_type:
        description:
            - Traffic class type
        default: QCT_IP_V4
        choices: QCT_IP_V4, QCT_IP_V6
        required: true
    dscp_value:
        description:
            - dscp value to be applied
        choices: 0-64
        required: false
    entry_type:
        description:
            - Type of action to take.
        choices: QTCET_MATCH, QTCET_IGNORE
        required: false
    protocol_type:
        description:
            - Protocol type for traffic filter.
        required: false
        choices: 'PT_GRE','PT_ESP','PT_AH','PT_OSPF','PT_PIM','PT_VRRP',
                 'PT_ICMP','PT_IGMP','PT_IP','PT_SCTP','PT_TCP','PT_UDP'
    icmp_type:
        description:
            - Applies to icmp type matching this field. Only PT_ICMP
              protocol_type support icmp_code
        required: false
    icmp_code:
        description:
            - Applies to icmp code matching this field. Only PT_ICMP
              protocol_type support icmp_code
        required: false
    igmp_type:
        description:
            - Applies to igmp type matching this field. Only PT_IGMP
              protocol_type support igmp_type
        required: false
    match_bit:
        description:
            - The set of tcp match bits . Only PT_TCP  protocol_type
              support match_bit
        required: false
    source_port:
        description:
            - Applies to source port matching this filter. Only PT_SCTP,
              PT_TCP and PT_UDP Protocol types support source_port
        required: false
    destination_port:
        description:
            - Applies to destination port matching this filter. Only
              PT_SCTP,PT_TCP and PT_UDP Protocol types support destination_port
        required: false
    source_ip_address:
        description:
            - Applies to source IP Address/Subnet matching this extended traffic filter
        required: false
    source_ip_mask:
        description:
            - Net mask source_ip_address
        required: false
    destination_ip_address:
        description:
            - Applies to destination IP Address/Subnet matching this extended traffic filter
        required: false
    device_type:
        description:
            - Applies to device type matching this extended traffic filter
        required: false
    application_type:
        description:
            - Applies to application matching this extended traffic filter
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
            - Sequence number for the traffic class configured
        required: false

##### EXAMPLES
```YAML
      - name: create traffic class
        arubaoss_traffic_class:
          class_name: my_class
      - name: add match criteria
        arubaoss_traffic_class:
          class_name: my_class
          icmp_code: 1
          icmp_type: 1
          source_ip_address: 0.0.0.0
          source_ip_mask: 255.255.255.255
          destination_ip_address: 0.0.0.0
          destination_ip_mask: 255.255.255.255
          protocol_type: "PT_ICMP"
          entry_type: QTCET_MATCH
      - name: add udp traffic ignore rule
        arubaoss_traffic_class:
          class_name: my_class
          source_ip_address: 0.0.0.0
          source_ip_mask: 255.255.255.255
          destination_ip_address: 0.0.0.0
          destination_ip_mask: 255.255.255.255
          protocol_type: "PT_UDP"
          entry_type: QTCET_IGNORE
          destination_port: {"port_not_equal": 0,"port_range_start": 443,"port_range_end": 443}
      - name: delete traffic class
        arubaoss_traffic_class:
          class_name: my_class
          state: delete

```