# ARUBA AIRWAVE CONFIG
Module: ****arubaairwave_config****  
Description: "This module implements REST API based configuration(GET/POST) for Aruba Airwave"

##### ARGUMENTS
    host:
        description: Aruba Airwave IP address or domain name 
        type: string
        required: true
    credential_0:
        description: Username of Aruba Airwave
        type: string
        required: true
    credential_1:
        description: Password of Aruba Airwave
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
        required: false      
    params:
        description: Optional parameters for the API call. Query operations might have additional params to be supplied with the request. 
        type: dict
        required: false 
    validate_certs:
        description: Validate the server cert when this option is set to True.
        type: bool
        required: false
    client_cert:
        description: Optionally provide path to client cert file to validate it in server
        type: string
        required: false
    client_key:        
        description: If client cert if provided without the key in it, use this parameter
        type: string
        required: false

##### EXAMPLES
```YAML
   - name: AP search query
      arubaairwave_config:
        host: 192.168.1.1
        credential_0: admin
        credential_1: admin123
        method: GET
        api_name: ap_search.xml
        params: { "query" : "cf:32"}
        validate_certs: True
```
