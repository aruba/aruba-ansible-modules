# ARUBAOS FACTS

Module: **arubaos_facts**\
Description: Populates ansible_facts with C(sys_info) details about the system to which the query is being sent

### ARGUMANTS
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

### RETURN

    ansible_facts:
        description: Facts to be merged to the current play context.
        type: dict
        contains:
            arubaos:
                description: Details about the system to which the query is being sent.
                type: dict

### EXAMPLES
```YAML
environment:
  ANSIBLE_ARUBAOS_HOST: 192.168.1.1
  ANSIBLE_ARUBAOS_USERNAME: admin
  ANSIBLE_ARUBAOS_PASSWORD: aruba123

tasks:

  - name: Gather controller system facts
    arubaos_facts:
```

