# IP Auth
Module: ****arubaoss_ip_auth****  
Description: "This implements rest api's which configure ip autorization on device"

##### ARGUMENTS
    auth_ip:
        description:
            - Ip address for autherization.
        required: false
    access_role:
        description:
            - Type of access to be allowed.
        required: false
        choices: AR_MANAGER, AR_OPERATOR
    mask:
        description:
            - Net mask for auth_ip.
        required: false
    access_method:
        description:
            - Type of access method allowed.
        required: false
    auth_id:
        description:
            - Sequence number for auth rule
        required: false
    state:
        description:
            - Enable/disable/read ip auth data
        required: false
        default: create
        choices: create, delete


##### EXAMPLES
```YAML
      - name: create ip auth all
        arubaoss_ip_auth:
          auth_ip: 10.0.12.91
          mask: 255.255.248.0
          access_role: AR_MANAGER
          access_method: AM_ALL
        register: auth_1
      - name: delete ip auth all
        arubaoss_ip_auth:
          auth_ip: 10.0.12.92
          auth_id: "{{auth_1.id}}"
          state: delete
```