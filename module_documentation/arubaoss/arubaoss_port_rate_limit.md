# Port Rate Limit
Module: ****arubaoss_port_rate_limit****  
Description: "This implements rest apis which can be used to configure Port Rate Limit"

##### ARGUMENTS
    command:
        description: Function name calls according to configuration required
        choices: update_rate_limit_attributes, clear_rate_limit_trap,
                  update_rate_limit_onPort, update_rate_limit_attributes_onPort
        required: False 
    port_id 
        description: Port_id of the port
        required: True 
    icmp_traffic_type 
        description: ICMP traffic type. Default is "PITT_IP_V4"
        choices: PITT_IP_ALL, PITT_IP_V4, PITT_IP_V6
        required: False
    icmp_rate_limit 
        description: ICMP Rate Limit value.
        required: False
    queues_direction 
        description: Queue traffic direction. port_id and queues_direction 
                     are required to uniquely identify the 
                     queue_rate_percentage to be set
        choices: PTD_OUT
        required: False
    queue_rate_percentage 
        description: Rate limit for each egress queue in percentage. Apply 
                     the default value on all queues to reset the configuration
        required: False
    traffic_type
        description: The traffic type. port_id, traffic_type and direction are 
                     required to uniquely identify the rate_limit value to be set
        choices: PTT_BCAST, PTT_MCAST, PTT_ALL, PTT_UKWN_UNCST
        required: False
    direction:
        description: Traffic flow direction. port_id, traffic_type and direction 
                     are required to uniquely identify the rate_limit value to be set. 
                     PTD_OUT is applicable, only when traffic_type is PTT_ALL on 
                     specific platforms
        choices: PTD_IN, PTD_OUT
        required: False
    rate_limit
        description: Rate limit value. rate_limit_in_kbps and rate_limit_in_percent 
                     will be null if rate_limit is not configured
        required: False


##### EXAMPLES
```YAML
     - name: Updates attributes of port ICMP rate limit per port id
       arubaoss_port_rate_limit:
         command: update_rate_limit_attributes
         port_id: 1
         icmp_traffic_type: "PITT_IP_ALL"
         rate_limit_in_kbps: "10"
         rate_limit_in_percent: "0"

```