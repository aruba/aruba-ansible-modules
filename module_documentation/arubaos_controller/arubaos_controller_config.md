# ARUBA CONTROLLER CONFIG 
Module: ****arubaos_controller_config****  
Description: "This module implements REST API based configuration(GET/POST) for ArubaOS8 based controllers in Master/Standalone role. Refer to the API swagger doc https://<controller-ip>/api."

##### ARGUMENTS
    host:
        description: Aruba Controller IP address or domain name 
        type: string
        required: true
    username:
        description: Username of Aruba Controller
        type: string
        required: true
    password:
        description: Password of Aruba Controller
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
    config_path:
        description: Path to the configuration node of the device which has to configured
        type: string
        required: false        
    data:
        description: Payload data for the mentioned API endpoint
        type: dict
        required: false        
    validate_certs:
        description: set to True, to enable server certificate validation. By default certificate validation is disabled.
        type: bool
        required: false
    client_cert:
        description: set the file path, to supply client cert to server for validation. By default client certificate validation is disabled.
        type: string
        required: false
    client_key:
        description: set the key for the client_cert, if key is not part of the client certificate
        type: string
        required: false

##### EXAMPLES
```YAML
    - name: Add a vlan id
      arubaos_controller_config:
        host: "{{ mm_ip }}"
        username: "{{ mm_username }}"
        password: "{{ mm_password }}"
        method: "{{ method_type }}"
        config_path: "{{ configuration_path }}"
        api_name: vlan_id
        data: { "id": 47 }
        
    - name: Execute a show version command
      arubaos_controller_config:
        host: "{{ mm_ip }}"
        username: "{{ mm_username }}"
        password: "{{ mm_password }}"
        method: "GET"
        config_path: "{{ configuration_path }}"
        api_name: showcommand
        data: { "command": "show version" }
        validate_certs: True
```

