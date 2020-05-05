# DNS
Module: ****arubaoss_dns****  
Description: "This implements rest apis which can be used to configure DNS"

##### ARGUMENTS
    dns_config_mode:
        description: DNS Configuration Mode, default is DCM_DHCP
        choices: DCM_DHCP, DCM_MANUAL, DCM_DISABLED
        required: False
    dns_domain_names:
        description: The first  manually configured DNS server domain name,
          all DNS configurations need to be made in a single module call,
          to remove configuration pass in empty string ""
        type: str
        required: False
    dns_domain_names_2:
        description: The second  manually configured DNS server domain name,
          all DNS configurations need to be made in a single module call,
          to remove configuration pass in empty string ""
        type: str
        required: False
    dns_domain_names_3:
        description: The third  manually configured DNS server domain name,
          all DNS configurations need to be made in a single module call,
          to remove configuration pass in empty string ""
        type: str
        required: False
    dns_domain_names_4:
        description: The fourth  manually configured DNS server domain name,
          all DNS configurations need to be made in a single module call,
          to remove configuration pass in empty string ""
        type: str
        required: False
    dns_domain_names_5:
        description: The fifth  manually configured DNS server domain name,
          all DNS configurations need to be made in a single module call,
          to remove configuration pass in empty string ""
        type: str
        required: False
    server_1:
        description: The first manually configured DNS Server IP address with priority 1,
          all DNS configurations need to be made in a single module call,
          to remove configuration pass in empty string ""
        type: str
        required: False
    version_1:
        description: The ip version of first manually configured DNS Server.
        choices: IAV_IP_V4. (V6 is not supported via REST)
        type: str
        required: False
    server_2:
        description: The second manually configured DNS Server IP address with priority 2,
          all DNS configurations need to be made in a single module call
        type: str
        required: False
    version_2:
        description: The ip version of second manually configured DNS Server.
        choices: IAV_IP_V4. (V6 is not supported via REST)
        type: str
        required: False
    server_3:
        description: The third manually configured DNS Server IP address with priority 3,
          all DNS configurations need to be made in a single module call,
          to remove configuration pass in empty string ""
        type: str
        required: False
    version_3:
        description: The ip version of third manually configured DNS Server.
        choices: IAV_IP_V4. (V6 is not supported via REST)
        type: str
        required: False
    server_4:
        description: The fourth manually configured DNS Server IP address with priority 4,
          all DNS configurations need to be made in a single module call,
          to remove configuration pass in empty string ""
        type: str
        required: False
    version_4:
        description: The ip version of fourth manually configured DNS Server.
        choices: IAV_IP_V4. (V6 is not supported via REST)
        type: str
        required: False
        
        
##### EXAMPLES
```YAML
    - name: Configure Maximum DNS Domains and DNS Server
      arubaoss_dns:
        dns_domain_names: "mydomain.com"
        dns_domain_names_2: "myotherdomain.com"
        dns_domain_names_3: myotherotherdomain.com
        dns_domain_names_4: yourdomain.com
        dns_domain_names_5: otherdomain.com
        server_1: "10.2.3.4"
        server_2: "10.2.3.5"
        server_3: "10.2.3.6"
        server_4: "10.2.3.7"

    - name: Configure Remove all DNS Domains and DNS Server 3 and 4
      arubaoss_dns:
        server_1: "10.2.3.4"
        server_2: "10.2.3.5"
        server_3: ""
        server_4: ""

    - name: Configure DNS to be DHCP
      arubaoss_dns:
        dns_config_mode: "DCM_DHCP"

    - name: Disable DNS
      arubaoss_dns:
        dns_config_mode: "DCM_DISABLED"

    - name: Configure DNS Server with priority 4
      arubaoss_dns:
        dns_config_mode: "DCM_MANUAL"
        server_4: "10.2.3.4"

    - name: Configure DNS Server with priority 4 and priority 1
      arubaoss_dns:
        dns_config_mode: "DCM_MANUAL"
        server_1: "10.2.3.1"
        server_4: "10.2.3.4"
```