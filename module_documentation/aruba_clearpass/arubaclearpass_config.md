# ARUBA CLEARPASS CONFIG
Module: ****arubaclearpass_config****  
Description: "This module implements REST API based configuration(GET/POST) for Aruba ClearPass."

##### ARGUMENTS
    host:
        description: Aruba ClearPass IP address or domain name 
        type: string
        required: true
    client_id:
        description: client_id obtained from ClearPass Account (Need to create API client and obtain this info)
        type: string
        required: true
    client_secret:
        description: client_secret obtained from ClearPass Account (Need to create API client and obtain this info)
        type: string
        required: true
    api_name:
        description: API endpoint for which the request is made
        type: string
        required: true
    method:
        description: HTTP method type either (GET/POST)
        type: string
        required: true       
    data:
        description: Payload data for the mentioned API endpoint
        type: dict
        required: true 
        
##### EXAMPLES
```YAML
    - name: Add a Device
      arubaclearpass_config:
        host: "{{ clearpass_ip }}"
        client_id: "{{ clearpass_client_id }}"
        client_secret: "{{ clearpass_client_secret }}"
        method: "{{ clearpass_method }}"
        api_name: network-device
        data: { "name": "new_switch", "ip_address": "1.1.1.1", "radius_secret": "aruba123", "vendor_name": "Aruba" }
```
