# ARUBA ACTIVATE CONFIG
Module: ****arubaactivate_config****  
Description: "This module implements REST API based configuration(GET/POST) for Aruba Activate"

##### ARGUMENTS
    credential_0:
        description: Username of Aruba Activate
        type: string
        required: true
    credential_1:
        description: Password of Aruba Activate
        type: string
        required: true
    method:
        description: HTTP method type either (GET/POST) 
        type: string
        required: true
    api_name:
        description: API endpoint for which the request is made
        type: string
        required: true   
    api_action:
        description: Aruba Activate action (update/query)
        type: string
        required: true        
    data:
        description: Payload data for the mentioned API endpoint
        type: dict
        required: true
    validate_certs:
        description: Validate the server cert if this option is set to True
        type: bool
        required: false
        
##### EXAMPLES
```YAML
    - name: Add Folder
      arubaactivate_config:
        credential_0: "{{ activate_username }}"
        credential_1: "{{ activate_password }}"
        method: "{{ api_method }}"
        api_name: "folder"
        api_action: "update"
        data: 'json={ "folders": [ { "parentId": "4d4b127e-a7ab-4d89-9e07-508c3b529975", "folderName": "New_Test_folder"}]}'
        validate_certs: True
```
