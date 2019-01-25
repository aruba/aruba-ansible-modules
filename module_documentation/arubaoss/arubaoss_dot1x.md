# DOT1x
Module: ****arubaoss_dot1x****  
Description: "This implements rest apis which can be used to configure DOT1x"

##### ARGUMENTS
    command:
        description: Module to be configured.
        choices: dot1x_config, authenticator_port_config, authentication_method_config, dot1x_port_security,
                 authenticator_port_clearstats, authenticator_port_initialize, authenticator_port_reauthenticate
        required: False
    is_dot1x_enabled:
        description: Global 802.1x admin status
        required: False
    cached_reauth_delay:
        description: Global 802.1x cached reauth delay
        required: False
    allow_gvrp_vlans:
        description:  allow GVRP vlans
        required: False
    use_lldp_data:
        description: Use LLDP data
        required: False
    port_id:
        description: Port ID
        required: False
    is_authenticator_enabled:
        description: 802.1X Authenticator Port admin status
        required: False
    control:
        description: 802.1X Authenticator Port operational control
        required: False
        choices: DAPC_UNAUTHORIZED, DAPC_AUTO, DAPC_AUTHORIZED
    unauthorized_vlan_id:
        description: 802.1X unauthorized VLAN ID. Displays 0 if not configured. Use 0 to reset unauthorized_vlan_id.
        required: False
    client_limit:
        description: Client limit
        required: False
    quiet_period: Quiet Period
        description:
        required: False
    tx_period:
        description: Tx Period
        required: False
    supplicant_timeout:
        description: Supplicant timeout, default= 30
        required: False
    server_timeout:
        description: Server timeout, default= 300
        required: False
    max_requests:
        description: Max requests, default =2
        required: False
    reauth_period:
        description: Reauth Period
        required: False
    authorized_vlan_id:
        description: 802.1X authorized VLAN ID. Displays 0 if not configured.
                     Use 0 to reset authorized_vlan_id
        required: False
    logoff_period:
        description: Logoff Period, default = 300
        required: False
    unauth_period:
        description: Unauth period, default = 0
        required: False
    cached_reauth_period:
        description: Cached reauth period, default = 0
        required: False
    enforce_cache_reauth:
        description: Authenticator enforce canched reauthentication
        required: False
    server_timeout:
        description:
        required: False
    supplicant_timeout:
        description:
        required: False
    primary_authentication_method:
        description: The primary authentication method
        choices: DPAM_LOCAL, DPAM_EAP_RADIUS, DPAM_CHAP_RADIUS
        required: False
    secondary_authentication_method:
        description: The secondary authentication method
        choices: DSAM_NONE, DSAM_AUTHORIZED, DSAM_CACHED_REAUTH
        required: False
    server_group:
        description: The server group
        required: False
    controlled_direction:
        description: Traffic Controlled direction
        choices: DCD_IN, DCD_OUT
        required: False
    allow_mbv:
        description: Configuration of MAC based Vlans
        required: False
    allow_mixed_users:
        description: Allowed users
        required: False
    is_port_speed_vsa_enabled:
        description: Is port speed VSA enabled
        required: False


##### EXAMPLES
```YAML
     - name: Updates the given console dot1x configuration to the system
       arubaoss_aaa_dot1x:
         server_group: "AZM_TACACS"
```