# TACACS Profile
Module: ****arubaoss_tacacs_profile****  
Description: "This implements rest apis which can be used to configure TACACS Server"

##### ARGUMENTS
    command:
        description: Function name calls according to configuration required
        choices: config_tacacs_profile, config_tacacs_server
        required: True
    config:
        description: To config or unconfig the required command
        choices: create, delete
        required: False
    dead_time
        description: Dead time for unavailable TACACS+ servers
        required: False
    time_out
        description: TACACS server response timeout
        required: False
    global_auth_key
        description: Authentication key
        required: False
    server_ip
        description: TACACS Server IP Address
        required: False
    auth_key
        description: Authentication key
        required: False
    is_oobm
        description: Use oobm interface to connect the server
        required: False

##### EXAMPLES
```YAML
     - name: Updates the given tacacs profile configuration to the system
       arubaoss_tacacs_profile:
         command: config_tacacs_profile
         dead_time: 10
         time_out: 3
         global_auth_key: ""
```