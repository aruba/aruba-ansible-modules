# Routing
Module: ****arubaoss_routing****  
Description: "This implements routing rest api to enable/disable routing on device"


##### ARGUMENTS
    state:
        description:
            - To enable/disable routing globally.
        required: true
        choices: create, delete


##### EXAMPLES
```YAML
     - name: enable routing
       arubaoss_routing:
         state: create
     - name: disable routing
       arubaoss_routing:
         state: delete

```