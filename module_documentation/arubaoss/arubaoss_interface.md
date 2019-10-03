# Interface
Module: ****arubaoss_interface****  
Description: "Implements Ansible module for port configuration and management."

##### ARGUMENTS
    interface:
        description:
            - interface id to be configured
        required: true
    description:
        description:
            - interface name/description, to remove the description of an interface
            pass in an empty string ''
    admin_stat:
        description:
            - interface admin status
        required: false
    qos_policy:
        description:
            - Name of QOS policy profile that needs to applied to port
        required: false
    qos_direction:
        description:
            - Direction of QOS policy profile that needs to applied to port
        default='QPPD_INBOUND'
        choices='QPPD_INBOUND','QPPD_OUTBOUND'    
        required: false
    acl_id:
        description:
            - Name ACL profile that needs to applied to port
        required: false
    acl_type:
        description:
            - ACL Type that needs to applied to port
        default='AT_STANDARD_IPV4'
        choices='AT_STANDARD_IPV4','AT_EXTENDED_IPV4'
        required: false
    acl_direction:
        description:
            - Direction in which ACL will be applied.
        choices='AD_INBOUND', 'AD_OUTBOUND'
        required: false

##### EXAMPLES
```YAML
     - name: configure port description
       arubaoss_interface:
         interface: 1
         description: "test_interface"

      - name: configure qos on port
        arubaoss_interface:
          interface: 5
          qos_policy: "my_qos"

      - name: delete qos from port
        arubaoss_interface:
          interface: 5
          qos_policy: "my_qos"
          enable: False

      - name: config acl on ports
        arubaoss_interface:
          interface: 2
          acl_id: test
          acl_type: standard
          acl_direction: in

      - name: delete acl ports stats
        arubaoss_interface:
          state: delete
          interface: 2
          acl_id: test
          acl_type: standard
          acl_direction: in
```