# AAA Authentication

Module: ****arubaoss_aaa_authentication****
Description:

##### ARGUMENTS
```YAML
  command:
    description: Function name calls according to configuration required.
      config_authentication - To enable/disable privilaged mode, Specify that
        switch respects the authentication server's privilege level.
      config_authentication_console - Configure authentication mechanism used to control
        access to the switch console.
      config_authentication_ssh - Configure authentication mechanism used to control SSH
        access to the switch.
      config_authentication_local_user - Create or remove a local user account.
    default: config_authentication
    choices: ['config_authentication', 'config_authentication_console',
      'config_authentication_ssh', 'config_authentication_local_user']
    required: False
  primary_method:
    description: The primary authentication method, used with config_authentication_console
      and config_authentication_ssh command.
    choices: ['PAM_LOCAL', 'PAM_TACACS']
    default: PAM_LOCAL
    required: False
  secondary_method:
    description: The secondary authentication method, used with config_authentication_console
      and config_authentication_ssh command.
    choices: ['SAM_NONE', 'SAM_LOCAL']
    default: SAM_NONE
    required: False
  local_user_name:
    description: Create or remove a local user account. Used with config_authentication_local_user
      command.
    type: 'str'
    required: False
  group_name:
    description: Specify the group for a username. Used with config_authentication_local_user
      command.
    type: 'str'
  password_type:
    description: Specify the password type. Used with config_authentication_local_user
      command.
    choices=["PET_SHA1","PET_PLAIN_TEXT", "PET_SHA256"]
    required: False
    default="PET_SHA1"
  user_password:
    description: Specify the password.  Used with config_authentication_local_user
      command.
    type: 'str'
  min_pwd_len:
    description: Configures the minimum password length for a user. Used with
      config_authentication_local_user command.
    type='int' <1-64>
    default=8
  aging_period:
    description: Configures the password aging time for a user. Used with
      config_authentication_local_user command.
    type: int
    default: 0
```    

##### EXAMPLES
```YAML
- name: aaa authentication login privilege-mode
  arubaoss_aaa_authentication:
    command: config_authentication

- name: aaa authentication console login tacacs
  arubaoss_aaa_authentication:
    command: config_authentication_console
    primary_method: PAM_TACACS
    secondary_method: SAM_LOCAL

- name: aaa authentication ssh login tacacs
  arubaoss_aaa_authentication:
    command: config_authentication_ssh
    primary_method: PAM_TACACS
    secondary_method: SAM_LOCAL

- name: Create Authentication local user plaintext password
  arubaoss_aaa_authentication:
    command: config_authentication_local_user
    group_name: "Level-15"
    local_user_name: "ARUBA"
    password_type: "PET_PLAIN_TEXT"
    user_password: "ArubaR0Cks!"

- name: Create Authentication local user sha256
  arubaoss_aaa_authentication:
    command: config_authentication_local_user
    group_name: "super"
    local_user_name: "ARUBA"
    password_type: "PET_SHA256"
    user_password: "1c6976e5b5410115bde308bd4dee15dfb167a9c873fc4bb8a81f6f2ab478a918"

  - name: Create Authentication local user2
    arubaoss_aaa_authentication:
      command: config_authentication_local_user
      group_name: "super"
      local_user_name: "user2"
      password_type: "PET_SHA1"
      user_password: "d033e22ae348aeb5660fc2140aec35850c4da997"

  - name: update Authentication local user min_pwd_len, aging_period
    arubaoss_aaa_authentication:
      command: config_authentication_local_user
      local_user_name: "user1"
      min_pwd_len: 10
      aging_period: 20

  - name: Delete Authentication local user
    arubaoss_aaa_authentication:
      command: config_authentication_local_user
      local_user_name: "user1"
      config: "delete"
```