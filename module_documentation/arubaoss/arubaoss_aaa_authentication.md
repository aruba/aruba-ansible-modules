# AAA Authentication

Module: ****arubaoss_aaa_authentication****
Description:

##### ARGUMENTS
    command:
        description: Function name calls according to configuration required
        choices: config_authentication, config_authentication_console, config_authentication_ssh
        required: False
    is_privilege_mode_enabled:
        description: To enable/disable privilaged mode
        required: False
    primary_method:
        description: The primary authentication method
        choices: PAM_LOCAL, PAM_TACACS
        required: False
    secondary_method
        description: The secondary authentication method
        choices: SAM_NONE, SAM_LOCAL
        required: False

##### EXAMPLES
```YAML
     - name: Updates the given console authentication configuration to the system
       arubaoss_aaa_authentication:
         primary_method: "PAM_TACACS"
         secondary_method: "SAM_LOCAL"
         command: config_authentication_console
```