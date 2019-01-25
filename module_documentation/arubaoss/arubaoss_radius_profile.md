# Radius Profile
Module: ****arubaoss_radius_profile****  
Description: "This implements rest apis which can be used to configure RADIUS Server"

##### ARGUMENTS
    command:
        description: Function name calls according to configuration required
        choices: config_radius_profile,config_radius_serverGroup,config_radius_server
        required: True
    config:
        description: To config or unconfig the required command
        choices: create, delete
        required: False
    retry_interval
        description: The RADIUS server retry interval
        required: False
    retransmit_attempts
        description: The RADIUS server retransmit attempts
        required: False
    dead_time
        description: The RADIUS server dead_time. dead_time cannot set when
                     is_tracking_enabled is true. Input dead_time as null to
                     reset the value. dead_time is indicated as null instead of '0' in CLI
        required: False
    dyn_autz_port
        description: The RADIUS dyn_autz_port
        required: False
    key
        description: The RADIUS server key. Input key as empty string to reset the value
        required: False
    tracking_uname
        description: The RADIUS tracking_uname, default is radius-tracking-user
        required: False
    is_tracking_enabled
        description: The RADIUS server for if tracking is enabled . The flag is_tracking_enabled,
                     cannot set to true when dead_time is configured
        required: False
    cppm_details
        description: Username and password combination of CPPM which is used to
                     login to CPPM to download user roles
        required: False
    server_ip
        description: IP Address of the Radius Server
        required: False
    shared_secret
        description: The Radius server shared secret
        required: False
    version
        description: Version of the IP Address used
        choices: IAV_IP_V4. (V6 is not supported via REST)
        required: False
    server_group_name
        description: Server Group name
        required: False
   time_window_type
        description: Time window type
        choices: TW_POSITIVE_TIME_WINDOW, TW_PLUS_OR_MINUS_TIME_WINDOW
        required: False
    server_ip
        description: Radius server hosts. Minimum is 1 servers, and maximum is 3
        required: False

##### EXAMPLES
```YAML
     - name: Updates the radius profile details on system
       arubaoss_radius_profile:
         command: config_radius_profile
         retry_interval: 7
         retransmit_attempts: 5
         dead_time: 12
         dyn_autz_port: 3799
         key: ""
         tracking_uname: "radius-tracking-user"
         is_tracking_enabled: false
         cppm_details: null

```