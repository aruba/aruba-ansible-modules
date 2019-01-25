# AAA Authorization

Module: ****arubaoss_aaa_authorization****  
Description: implements rest api for AAA Authorization configuration

##### ARGUMENTS
    authorization_method:
        description: To authorization method needed
        choices: AZM_NONE, AZM_TACACS
        required: False


##### EXAMPLES
```YAML
     - name: Updates the given console authorization configuration to the system
       arubaoss_aaa_authorization:
         authorization_method: "AZM_TACACS"
```