# ARUBAOS SHOW COMMAND

Module: arubaos_showcommand
Description: Executes a C(show) command on the controller and returns structured data when supported

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
    command:
        descriptition:
            - Any show command supported by the controller.
            - The command is executed on the target controller node (i.e. mynode).
            - Invalid commands return empty data.
        required: true
        type: str

### RETURNS

    response:
        description: Data set returned by the GET request.
        returned: on success
        type: dict

### EXAMPLES

```YAML
environment:
  ANSIBLE_ARUBAOS_HOST: 192.168.1.1
  ANSIBLE_ARUBAOS_USERNAME: admin
  ANSIBLE_ARUBAOS_PASSWORD: aruba123

tasks:

  - name: Get list of managed devices
    arubaos_showcommand:
      command: show switches
```