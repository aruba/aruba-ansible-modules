# TACACS Profile
Module: ****arubaoss_tacacs_profile****  
Description: "This implements rest apis which can be used to configure TACACS Server"

##### ARGUMENTS
```YAML
  command:
    description: Function name calls according to configuration required.
      choice config_tacacs_server - Configure a TACACS+ server.
      choice config_tacacs_profile - Configure global TACACS+ profile.
    choices: config_tacacs_profile, config_tacacs_server
    required: True
  config:
    description: To configure or unconfigure the required command.
    choices: create, delete
    default: create
    required: False
  dead_time:
    description: Dead time for unavailable TACACS+ servers. Used with the
      config_tacacs_profile command.
    type: int
    default: 0
    required: False
  time_out:
    description: TACACS server response timeout. Used with the
      config_tacacs_profile command.
    type: int
    default: 5
    required: False
  global_auth_key:
    description: Configure the default authentication key for all TACACS+ servers.
      Used with the config_tacacs_profile command. To delete, pass in empty string ''.
    required: False
    type: str
  ip_address:
    description: TACACS Server IP Address. Used with the config_tacacs_server
      command.
    required: False
    type: str
  auth_key:
    description: Configure the server authentication key. Used with the
      config_tacacs_server command.
    required: False
    type: str
  is_oobm:
    description: Use oobm interface to connect the server.  Used with the
      config_tacacs_server
    default: False
    type: bool
    required: False
  ordering_sequence:
    description: Enables reordering upon deletion of existing server.
      Used with the config_tacacs_profile command.
    required: False
    type: bool
    default: False
```
##### EXAMPLES
```YAML
- name: Creates tacacs-server host 10.1.1.1 with key Aruba!
  arubaoss_tacacs_profile:
    command: config_tacacs_server
    ip_address: 10.1.1.1
    auth_key: "Aruba!"
    is_oobm: true

- name: Deletes tacacs-server host 10.1.1.1 with key Aruba!
  arubaoss_tacacs_profile:
    command: config_tacacs_server
    ip_address: 10.1.1.1
    auth_key: "Aruba!"
    config: delete

- name: Creates global TACACS+ authentication key
  arubaoss_tacacs_profile:
    command: config_tacacs_profile
    global_auth_key: "Aruba!"

- name: Configure global TACACS+ settings
  arubaoss_tacacs_profile:
    command: config_tacacs_profile
    global_auth_key: "Aruba!"
    dead_time: 60
    time_out: 10

- name: Deletes Global TACACS+ settings
  arubaoss_tacacs_profile:
    command: config_tacacs_profile
    global_auth_key: ""
```
