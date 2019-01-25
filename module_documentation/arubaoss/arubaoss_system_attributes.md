# System Attributes
Module: ****arubaoss_system_attributes****  
Description: "This implements rest apis which can be used to configure System Attributes"

##### ARGUMENTS
    hostname:
        description: The system name
        required: False
    location:
        description: Location where the system is installed
        required: False
    contact:
        description: Contact information for the system.
        required: False
    domain_name:
        description: Regulatory domain where the system is operating on
        required: False
    version:
        description: Version of ip address
        required: False
    device_operation_mode:
        description: Mode in which the device is operating on
        required: False
    uplink_vlan_id:
        description: Vlan via which central is connected. This is applicable
                     only when device_operation_mode is DOM_CLOUD or DOM_CLOUD_WITH_SUPPORT.
                     This won't be available for non Central uses case
        required: False
    uplink_ip:
        description: Ip address of Vlan via which central is connected. This is
                     applicable only when device_operation_mode is DOM_CLOUD or
                     DOM_CLOUD_WITH_SUPPORT. This won't be available for non Central uses case
        required: False
    default_gateway_ip:
        description: The global IPV4 default gateway. Input octets as 0.0.0.0 to reset.
        required: False


##### EXAMPLES
```YAML
     - name: Updates the given console authorization configuration to the system
       arubaoss_system_attributes:
         hostname: "Test_santorini"
         location: "Bangalore"
         contact: "08099035734"
         domain_name: "hpe.com"
         version: "IAV_IP_V4"
         device_operation_mode: "DOM_AUTONOMOUS"
         uplink_vlan_id: "10"
         uplink_ip: "10.100.20.30"
         default_gateway_ip: "10.100.119.1"

```