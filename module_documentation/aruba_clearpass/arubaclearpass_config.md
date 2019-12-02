# ARUBA CLEARPASS CONFIG
Module: ****arubaclearpass_config****  
Description: "This module implements REST API based configuration for Aruba ClearPass."

##### ARGUMENTS
    host:
        description: Hostname or IP Address of the Clearpass server.
        required: true
    api_name:
        description: API endpoint for which the request is made
        required: true
    method:
        description: HTTP Method to be used for the API call
        required: true
        choices: GET, DELETE, POST, PATCH, PUT
    access_token:
        description: Access token used to authenticate API calls
        required: false
    client_id:
        description: API client ID used to retrieve access tokens
        required: false
    client_secret:
        description: API Client secret used to retrieve access tokens
        required: false
    data:
        description: Dictionnary respresenting data to be sent with the request
        required: false
    validate_certs:
        description: Validate server certs when this is set to True
        required: false
    client_cert:
        description: (Optional) Provide the path to client cert file for validation in server side.
        required: false 
    client_key:
        description: If the provided client cert does not have the key in it, use this parameter
        required: false
    
##### EXAMPLES
```YAML
    # Using client credentials
    - name: Add new switch to network devices
        arubaos_cppm_config:
        host: 192.168.1.1
        client_id: admin
        client_secret: aruba123
        api_name: network-device
        method: POST
        data: { "name": "new_switch", "ip_address": "1.1.1.1", "radius_secret": "aruba123", "vendor_name": "Aruba" }
        validate_certs: True

    # Using an access token
    - name: Add new switch to network devices
        arubaos_cppm_config:
        host: 192.168.1.1
        access_token: 2c2a25d4dee25dab99e3d011d52a8247b11a40df
        api_name: network-device
        method: POST
        data: { "name": "new_switch", "ip_address": "1.1.1.1", "radius_secret": "aruba123", "vendor_name": "Aruba" }
        validate_certs: True
```
