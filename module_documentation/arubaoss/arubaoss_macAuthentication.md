# Mac Authentication
Module: ****arubaoss_macAuthentication****  
Description: "This implements rest apis which can be used to configure Mac Authentication"

##### ARGUMENTS
    command:
        description: The command to be configured
        required: False
        choices: configMacAuth, configMacAuthOnPort
    port_id:
        description: The port id to be configured on the switch
        required: False
    unauthorized_vlan_id:
        description: Unauthorized VLAN ID. If we are giving unauthorized_vlan_id as 0,
                     it will remove the unauthorized_vlan_id configured
        required: False
    is_mac_authentication_enabled:
        description: Enables/disables MAC authentication on the Port
        required: False
    reauthenticate
        description: Provides option on whether to reauthenticate
        required: False
    mac_address_limit:
        description: The MAC Authentication address limit to be configured
        required: False


##### EXAMPLES
```YAML
    - name: Updates Mac Authentication globally
      arubaoss_macAuthentication:
        command: "configMacAuth"
        unauthorized_vlan_id: 10
```