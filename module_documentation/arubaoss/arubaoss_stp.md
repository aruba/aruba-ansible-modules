# STP
Module: ****arubaoss_stp****  
Description: "This implements rest apis which can be used to configure STP"

##### ARGUMENTS
    command:
        description: Function name calls according to configuration required
        choices: config_spanning_tree, config_spanning_tree_port
        required: True
    config:
        description: To config or unconfig the required command
        choices: create, delete
        required: False
    mode:
        description:
        required: False
    priority:
        description:
        required: False
    port_id:
        description: ID of the port
        required: False
    is_enable_admin_edge_port:
        description: Enable/Disable admin-edge-port
        required: False
    is_enable_bpdu_protection:
        description: Enable/Disable bpdu-protection.
        required: False
    is_enable_bpdu_filter:
        description: Enable/Disable bpdu-filter.
        required: False
    is_enable_root_guard:
        description: Enable/Disable root-guard.
        required: False

##### EXAMPLES
```YAML
     - name: update spanning tree port
       arubaoss_stp:
         port_id: 2
         mode:  "STM_MSTP"
         priority: 2
         is_enable_bpdu_protection: True
         is_enable_bpdu_filter: True
         is_enable_root_guard: True
         command: config_spanning_tree_port

```