# DNS
Module: ****arubaoss_dns****  
Description: "This implements rest apis which can be used to configure DNS"

##### ARGUMENTS
    dns_config_mode:
        description: DNS Configuration Mode, default is DCM_DHCP
        choices: DCM_DHCP, DCM_MANUAL, DCM_DISABLED
        required: False
    dns_domain_names:
        description: The first  manually configured DNS server domain name
        required: False
    dns_domain_names_2:
        description: The second  manually configured DNS server domain name
        required: False
    dns_domain_names_3:
        description: The third  manually configured DNS server domain name
        required: False
    dns_domain_names_4:
        description: The fourth  manually configured DNS server domain name
        required: False
    dns_domain_names_5:
        description: The fifth  manually configured DNS server domain name
        required: False
    server_1:
        description: The first manually configured DNS Server.
        required: False
    version_1:
        description: The ip version of first manually configured DNS Server.
        choices: IAV_IP_V4. (V6 is not supported via REST)
        required: False
    server_2:
        description: The second manually configured DNS Server.
        required: False
    version_2:
        description: The ip version of second manually configured DNS Server.
        choices: IAV_IP_V4. (V6 is not supported via REST)
        required: False
    server_3:
        description: The third manually configured DNS Server.
        required: False
    version_3:
        description: The ip version of third manually configured DNS Server.
        choices: IAV_IP_V4. (V6 is not supported via REST)
        required: False
    server_4:
        description: The fourth manually configured DNS Server.
        required: False
    version_4:
        description: The ip version of fourth manually configured DNS Server.
        choices: IAV_IP_V4. (V6 is not supported via REST)
        required: False
        
        
##### EXAMPLES
```YAML
 - name: Updates the given console DNS Server configuration to the system
   arubaoss_dns:
     dns_config_mode: "DCM_MANUAL"
     dns_domain_names: ["mydomain.com",
                         "myotherdomain.com"]
     version_1: "IAV_IP_V4"
     server_1: "10.2.3.4"
     version_2: "IAV_IP_V4"
     server_2: "10.2.3.5"
     version_3: "IAV_IP_V4"
     server_3: "10.2.3.6"
     version_4: "IAV_IP_V4"
     server_4: "10.2.3.7"
```