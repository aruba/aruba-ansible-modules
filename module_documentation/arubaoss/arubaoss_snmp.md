# SNMP
Module: ****arubaoss_snmp****  
Description: "This implements rest api's which configure snmp on device"

##### ARGUMENTS
    commmunity_nme:
        description:
            - snmp community name. Required when configuring community
        required: false
    access_type:
        description:
            - Type of access required. Operator or Manager.
        required: false
    restricted:
        description:
            - Extent of access restricted or unrestricted
        required: false
    host_ip:
        description:
            - Snmp host ip address
        required: false
    version:
        description:
            - Host IP address version
        required: false
    informs:
        description:
            - Enable/disables informs to host
        required: false
    inform_timeout:
        description:
            - Timeout for informs
        required: false
    inform_retires:
        description:
            - Retries required for informs
        required: false
    trap_level:
        description:
            - Trap level for host
        required: false
    use_oobm:
        description:
            - Enable/disable oobm port usage
        required: false
    location:
        description:
            - Server location
        required: false
    contact:
        description:
            - Server contact
        required: false

##### EXAMPLES
```YAML
      - name: configure snmp community
        arubaoss_snmp:
          community_name: test
          access_type: "{{item}}"
        with_items:
          - UT_MANAGER
          - UT_MANAGER
          - UT_OPERATOR
          - UT_OPERATOR
      - name: configure snmp community
        arubaoss_snmp:
          community_name: test
          access_type: "{{item.role}}"
          restricted: "{{item.res}}"
        with_items:
          - {"role":"UT_MANAGER","res":False}
          - {"role":"UT_MANAGER","res":True}
          - {"role":"UT_MANAGER","res":True}
          - {"role":"UT_OPERATOR","res":False}
          - {"role":"UT_OPERATOR","res":True}
          - {"role":"UT_OPERATOR","res":True}
      - name: configure snmp host
        arubaoss_snmp:
          community_name: test
          host_ip: "{{item}}"
        with_items:
          - 10.1.1.1
          - 10.1.1.1
      - name: configure snmp host inform
        arubaoss_snmp:
          community_name: test
          host_ip: 10.1.1.1
          informs: "{{item}}"
        with_items:
          - True
          - True
          - False
      - name: configure snmp host inform retry timeout
        arubaoss_snmp:
          community_name: test
          host_ip: 10.1.1.1
          informs: True
          inform_retries: "{{item.retry}}"
          inform_timeout: "{{item.timeout}}"
        with_items:
          - {"retry":10,"timeout":20}
          - {"retry":100,"timeout":200}
      - name: delete snmp host inform retry timeout
        arubaoss_snmp:
          community_name: test
          informs: False
      - name: configure snmp host trap-level
        arubaoss_snmp:
          community_name: test
          host_ip: 10.1.1.1
          trap_level: "{{item}}"
        with_items:
          - STL_ALL
          - STL_CRITICAL
          - STL_NOT_INFO
          - STL_DEBUG
          - STL_NONE
      - name: configure snmp host inform retry timeout traplevel
        arubaoss_snmp:
          community_name: test
          host_ip: 10.1.1.1
          informs: True
          inform_retries: "{{item.retry}}"
          inform_timeout: "{{item.timeout}}"
          trap_level: "{{item.trap}}"
        with_items:
          - {"retry":10,"timeout":20,"trap":"STL_CRITICAL"}
          - {"retry":100,"timeout":200,"trap":"STL_DEBUG"}
      - name: configure snmp host oobm
        arubaoss_snmp:
          community_name: test
          host_ip: 10.1.1.1
          use_oobm: "{{item}}"
        with_items:
          - True
          - False
      - name: delete snmp host
        arubaoss_snmp:
          community_name: test
          host_ip: 10.1.1.1
          state : delete
      - name: delete snmp community
        arubaoss_snmp:
          community_name: test
          state: delete
      - name: delete snmp community
        arubaoss_snmp:
          community_name: test
          state: delete
      - name: snmp contact and location
        arubaoss_snmp:
          location: lab
          contact: test_lab
      - name: delete snmp location
        arubaoss_snmp:
          location: lab
          state: delete
      - name: delete snmp contact
        arubaoss_snmp:
          contact: test_lab
          state: delete

```
