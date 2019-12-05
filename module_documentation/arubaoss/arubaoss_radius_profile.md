# Radius Profile
Module: ****arubaoss_radius_profile****  
Description: "This implements rest apis which can be used to configure RADIUS Server"

##### ARGUMENTS
    command:
      description: "Function name calls according to configuration required -
        choice config_radius_profile allows you to configure the switch's global radius server settings
        choice config_radius_server allows you to configure a radius server IP host
        choice config_radius_servergroup allows you to configure a radius-server group with existing radius server hosts"
      choices: ['config_radius_profile','config_radius_serverGroup','config_radius_server']
      required: True
      type: str
    config:
      description: To config or remove the required command
      choices: ['create','delete']
      required: False
      type: str
    retry_interval:
      description: The RADIUS server retry interval
      default: 7
      required: False
      type: int
    retransmit_attempts:
      description: The RADIUS server retransmit attempts
      default: 5
      type: int
      required: False
    dead_time:
      description: "The RADIUS server dead_time. dead_time cannot set when
        is_tracking_enabled is true. Input dead_time: null to
        reset the value. dead_time is indicated as null instead of '0' in CLI"
      default: 10
      type: int
      required: False
    dyn_autz_port:
      description: Configure the UDP port for dynamic authorization messages.
      default: 3799
      type: int
      required: False
    key:
      description: "Used with config_radius_profile command, Configure the default authentication key for all RADIUS.
        Input key as empty string to reset the value"
      type: str
      required: False
    tracking_uname:
      description: The RADIUS service tracking username
      default: radius-tracking-user
      type: str
      required: False
    is_tracking_enabled:
      description: "The RADIUS server for if tracking is enabled . The flag is_tracking_enabled,
        cannot set to true when dead_time is configured"
      required: False
    cppm_details:
      description: "Username and password combination of CPPM which is used to
        login to CPPM to download user roles, dictionary should be in the form: {'username':'superman','password': 'arubAn3tw0rks'}"
      type: dict
      required: False
    server_ip:
      description: "Used with config_radius_server or config_radius_serverGroup -
        Radius server hosts IP address. Minimum is 1 servers, and maximum is 3"
      type: str
      required: False
    shared_secret:
      description: "Used with config_radius_server command - The Radius server secret key"
      type: str
      required: False
    version:
      description: Version of the IP Address used
      default: IAV_IP_V4
      choices: IAV_IP_V4. (V6 is not supported via REST)
      required: False
    server_group_name:
      description: the AAA Server Group name
      required: False
    time_window_type:
        description: Time window type
        choices: TW_POSITIVE_TIME_WINDOW, TW_PLUS_OR_MINUS_TIME_WINDOW
        required: False


##### EXAMPLES
```YAML
    - name: Configure Radius server 10.0.0.1 with shared secret RADIUS!
      arubaoss_radius_profile:
        command: config_radius_server
        server_ip: 10.0.0.1
        shared_secret: "RADIUS!"

    - name: Configure Global Radius Profile key
      arubaoss_radius_profile:
        command: config_radius_profile
        key: "RADIUS!"

    - name: Configure Radius Profile CPPM details for User Roles
      arubaoss_radius_profile:
        command: config_radius_profile
        cppm_details: {'username':'superman','password': 'upupandaway'}

    - name: Configure Radius Server -
      arubaoss_radius_profile:
        command: config_radius_server
        server_ip: 10.0.0.1
        shared_secret: "RADIUS!"
        is_dyn_authorization_enabled: True
        time_window: 0

    - name: Configure Radius Server Group
      arubaoss_radius_profile:
        command: config_radius_serverGroup
        server_ip: 10.0.0.1
        server_group_name: SUPER

    - name: Configure Radius server 10.1.1.1 with shared secret ARUBA!
      arubaoss_radius_profile:
        command: config_radius_server
        server_ip: 10.1.1.1
        shared_secret: "ARUBA!"

    - name: Configure Radius server group
      arubaoss_radius_profile:
        command: config_radius_serverGroup
        server_group_name: AVENGERS
        server_ip: 10.1.1.1
```