# NTP
Module: ****arubaoss_ntp****  
Description: "This implements rest apis which can be used to configure NTP"

##### ARGUMENTS
    command:
        description: To config or unconfig the required command
        choices: config_timesync, enable_includeCredentials, config_ntp,
                 config_ntp_keyId, config_ntp_ipv4addr
        required: False
    ntp_ip4addr:
        description: The IPv4 address of the server
        required: False
    minpoll_value:
        description: Configures the minimum time interval in seconds
        required: False
    maxpoll_value:
        description: Configures the maximum time interval in seconds
        required: False
    burst:
        description: Enables burst mode
        required: False
    iburst:
        description: Enables initial burst mode
        required: False
    keyId:
        description: Sets the authentication key to use for this server
        required: False
    timesyncType:
        description: Updates the timesync type, takes values: ntp, sntp, timep
                     and timep-or-sntp
        required: False
    include_credentials_in_response:
        description: Enables include credentials when value is set to ICS_ENABLED
        choices: ICS_ENABLED, ICS_DISABLED, ICS_RADIUS_TACAS_ONLY
        required: False
    broadcast:
        description: Operate in broadcast mode
        required: False
    association_value:
        description: Maximum number of NTP associations
        required: False
    trap_value:
        description: Sets trap type
        required: False
    keyValue:
        description: The string to be added to authentication KeyId
        required: False


##### EXAMPLES
```YAML
     - name: Updates the  system with NTP Server configuration
       arubaoss_ntp:
         command: "config_ntp_ipv4addr"
         config: "create"
         ntp_ip4addr: "10.20.40.33"
         keyId: 2
         burst: True
         iburst: True
```