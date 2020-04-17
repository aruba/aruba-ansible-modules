# ARUBAOS CONFIG

Module: **arubaos_config**\
Description: Queries full or partial configuration of a particular configuration node

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
            - The hierarchy (complete config-node or config-path) from which the information should be retrieved.
            - On a managed device this will be restricted to /mm/mynode.
            - On a stand-alone controller, this will be restricted to /mm and /mm/mynode.
        required: false
        type: str
        default: None
    type:
        description:
            - State of configuration blocks to be retrieved.
            - If the user deletes any configuration which is pending, it is not returned in this API call.
            - Only added or modified configurations are retrieved. To get deleted configuration, use the 'show configuration pending' command.
        required: false
        type: str
        default: None
        choices:
            - pending
            - committed
            - local
            - committed,local

### RETURN

    response:
        description: Effective configuration of the specified node.
        returned: always
        type: dict

### EXAMPLES
```YAML
environment:
  ANSIBLE_ARUBAOS_HOST: 192.168.1.1
  ANSIBLE_ARUBAOS_USERNAME: admin
  ANSIBLE_ARUBAOS_PASSWORD: aruba123

tasks:

  - name: Get local configuration of branch1
    arubaos_config:
      config_path: /md/branch1
      type: local
```
