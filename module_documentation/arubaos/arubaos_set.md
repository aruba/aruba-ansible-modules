#  ARUBAOS SET

Module: **arubaos_set**
Description: Add, modify or delete the configuration
Notes:
- Supports --diff
- Check-mode is not supported on nodes with pending configuration.

### ARGUMENTS
    host:
        description:
            - Hostname or IP Address of the controller.
            - If not set the environment variable C(ANSIBLE_ARUBAOS_HOST) will be used.
        required: true
        type: str
        fallback: ANSIBLE_ARUBAOS_HOST
    username:
        description:
            - Username used to login to the controller.
            - If not set the environment variable C(ANSIBLE_ARUBAOS_USERNAME) will be used.
        required: true
        type: str
        fallback: ANSIBLE_ARUBAOS_USERNAME
    password:
        description:
            - Password used to login to the controller.
            - If not set the environment variable C(ANSIBLE_ARUBAOS_PASSWORD) will be used.
        required: true
        type: str
        no_log: true
        fallback: ANSIBLE_ARUBAOS_PASSWORD
    validate_certs:
        description:
            - Set to True to validate server SSL certificate upon HTTPS connection. Default option is false.
        required: false
        type: str
        default: None
    client_cert:
        description:
            - Set the file path for client certificate validation from server side. Default option is None.
        required: false
        type: str
        default: None
    client_key:
        description:
            - If the client_cert did not have the key, use this parameter. Default option is None.
        required: false
        type: str
        default: None
    config_path:
        description:
            - Complete config-node or config-path to which the operation should be applied.
            - On a managed device this will be restricted to /mm/mynode.
            - On a stand-alone controller, this will be restricted to /mm and /mm/mynode.
        required: false
        type: str
        default: None
    data:
        decription:
            - One or more objects which needs to be set. Each object type is a keyn of the top level dict.
            - The SET request is best effort and in case of first failure, others in the same block are not even tried.
            - Each object can contain either a single instance (dict) or a list of instances (list of dicts).
            - Every object and sub-object can optionally contain an C(_action) field which describes the action napplied to the configuration.
            - If C(_action) field is not set it implies that the user wants to add/modify the configuration.
            - Toggle objects are set using the C(_present) field, which takes a bool value.
            - Mutually exclusive with C(multipart_data).
        required: false
        type: dict
        default: {}
    multipart_data:
        description:
            - List of configuration data sets to be treated as independent requests.
            - Each item follows the same formating rules as for the C(data) option.
            - In contrary to C(data) option, even if one item (i.e. request) in the list contains errors, the other items will still continue to be processed.
            - Mutually exclusive with C(data).
        required: false
        type: list
        elements: dict
        default: []
    commit:
        description:
            - If set to true, configuration changes will be commited (write memory) on the specified C(config_path).
            - Task will be skipped if any changes are pending prior to the operation.
            - Changes will not be commited if any configuration blocks in the set operation contain errors.
            - Changes will still be staged if commit is skipped due to block errors.
            - Mutually exclusive with C(commit_force) option.
        required: false
        type: bool
        default: false
    commit_force:
        description:
            - If set to true, any changes to the configuration will be commited (write memory) to the specified C(config_path).
            - Task will be skipped if any changes are pending prior to the operation.
            - Commmit will happen even if some configuration blocks in the set operation contain errors.
            - Mutually exclusive with C(commit) option.
        required: false
        type: bool
        default: false

### RETURN

    response:
        description: Returned payload with additional "_result" fields for each object "_global_result".
        returned: always
        type: dict
    pending:
        description: Pending configuraiton of the target node
        returned: on check mode error
        type: dict

### EXAMPLES

```YAML
environment:
  ANSIBLE_ARUBAOS_HOST: 192.168.1.1
  ANSIBLE_ARUBAOS_USERNAME: admin
  ANSIBLE_ARUBAOS_PASSWORD: aruba123

tasks:

  - name: Create single instance of single object
    arubaos_set:
      config_path: /md/branch1/building1
      data:
        aaa_prof:
          profile-name: aaa_prof-guest
          mba_server_group:
            srv-group: srv_group-guest

  - name: Create multiple instances of single object
    arubaos_set:
      config_path: /md/branch1/building1
      data:
        aaa_prof:
          - profile-name: aaa_prof-guest
              mba_server_group:
                srv-group: srv_group-guest
          - profile-name: aaa_prof-employee
              dot1x_server_group:
                srv-group: srv_group-guest

  - name: Set & commit (do not of errors)
    arubaos_set:
      config_path: /md/branch1/building1
      data:
        aaa_prof:
          - profile-name: aaa_prof-guest
          - profile-name: aaa_prof-employee
      commit: true

  - name: Create inctances of multiple object types
    arubaos_set:
      config_path: /md/branch1/building1
      data:
        server_group_prof:
          - sg_name: srv_group-guest
          - sg_name: srv_group-employee
        aaa_prof:
          - profile-name: aaa_prof-guest
            mba_server_group:
              srv-group: srv_group-guest
          - profile-name: aaa_prof-employee
            dot1x_server_group:
              srv-group: srv_group-employee

  - name: Multi-part set & commit (commit even if a block fails)
    arubaos_set:
      config_path: /md/branch1/building1
      multipart_data:
        - server_group_prof:
            - sg_name: srv_group-guest
          aaa_prof:
            - profile-name: aaa_prof-guest
              mba_server_group:
                srv-group: srv_group-guest
        - server_group_prof:
            - sg_name: srv_group-employee
          aaa_prof:
            - profile-name: aaa_prof-employee
              dot1x_server_group:
                srv-group: srv_group-employee
      commit_force: true
```

