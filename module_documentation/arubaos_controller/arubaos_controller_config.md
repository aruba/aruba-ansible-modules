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
```
