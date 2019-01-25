# Syslog
Module: ****arubaoss_syslog****  
Description: "This implements rest api's which configure syslog on device"

##### ARGUMENTS
    server_address:
        description:
            - syslog server IP address
        required: true
    version:
        description:
            - Server IP address version
        default: IAV_IP_V4
        choices: IAV_IP_V4, IAV_IP_V6
        required: false
    description:
        description:
            - Server description
        required: false
    protocol:
        description:
            - Type of protocol to configure
        default: TP_UDP
        choices: TP_TCP, TP_UDP, TP_TLS
        required: false
    server_port:
        description:
            - Server port id to be configured
        required: false
    state:
        description:
            - Create of delete configuration
        default: create
        choices: create,delete
        required: false

##### EXAMPLES
```YAML
      - name: configure syslog server
        arubaoss_syslog:
          server_address: 1.1.1.1
          protocol: TP_TCP
      - name: delete syslog server
        arubaoss_syslog:
          server_address: 1.1.1.1
          state: delete
```