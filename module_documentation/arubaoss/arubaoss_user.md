# User
Module: ****arubaoss_user****  
Description: "This implement rest api's which can be use to manage and configure user on the device. Can configure only operator role via REST"

##### ARGUMENTS
    user_name:
        description:
            - user_name that needs to be configured.
        required: true
    user_type:
        description:
            - Type of user being configured.
        required: true
        default: UT_OPERATOR
    user_password:
        description:
            - user password in plain text or sha1
        required: true
    password_type:
        description:
            - type of password being conifgured
        required: true
        choices: PET_PLAIN_TEXT, PET_SHA1
    state:
        description:
            - Enable or disable
        choices: create, delete
        default: create
        required: false

##### EXAMPLES
```YAML
      - name: configure user
        arubaoss_user:
          user_name:  test_user
          user_password: test_user
          user_type: UT_OPERATOR
          password_type: PET_PLAIN_TEXT
      - name: delete user
        arubaoss_user:
          user_name:  test_user
          user_password: test_user
          user_type: UT_OPERATOR
          password_type: PET_PLAIN_TEXT
          state: delete
      - name: configure user sha1
        arubaoss_user:
          user_name: test_user
          user_password: F0347CE3A03A3BA71F596438A2B80DD21C9AF71B
          user_type: UT_OPERATOR
          password_type: PET_SHA1

```