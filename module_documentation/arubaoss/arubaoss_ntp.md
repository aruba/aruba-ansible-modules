# NTP
Module: ****arubaoss_ntp****  
Description: "This implements rest apis which can be used to configure NTP"

##### ARGUMENTS
    command:
        description: To configure a specific feature of NTP -
          choice config_timesync allows you to configure the switch's timesync
          choice enable_includeCredentials allows you to enable include credentials on the switch, either Encrypt Credentials or Include Credentials must be enabled to use key-id authentication with this module
          choice config_ntp allows you to enable/disable and configure switch's global NTP settings
          choice config_ntp_ipv4addr allows you to configure an NTP server with IPv4 address or hostname
          choice config_ntp_keyId allows you to configure an authentication key to use
        choices: ['config_timesync', 'enable_includeCredentials', 'config_ntp', 'config_ntp_ipv4addr', 'config_ntp_keyId']
        required: True
    config:
        description: To config or unconfig the required command
        choices: create, delete
    ntp_ip4addr:
        description: The IPv4 address of the server used with config_ntp_ipv4addr command
        required: False
    minpoll_value:
        description: Configures the minimum time interval in seconds used with config_ntp_ipv4addr command
        required: False
    maxpoll_value:
        description: Configures the maximum time interval in seconds used with config_ntp_ipv4addr command
        required: False
    mode:
        description: Enable burst or iburst mode used with config_ntp_ipv4addr command
        choices: ['burst', 'iburst']
        required: False
    keyId:
        description: Sets the authentication key to use for this server used with config_ntp_ipv4addr and config_ntp_keyId command
        required: False
    timesyncType:
        description: Updates the timesync type  used with config_timesync command
        choices: ['burst', 'iburst']
        required: False
    include_credentials_in_response:
        description: Enables include credentials when value is set to ICS_ENABLED  used with enable_includeCredentials command
        choices: [ICS_ENABLED, ICS_DISABLED, ICS_RADIUS_TACAS_ONLY]
        required: False
    operate:
        description: Operate in broadcast or unicast mode  used with config_ntp command
        choices: [broadcast, unicast]
        required: False
    association_value:
        description: Maximum number of NTP associations used with config_ntp command
        required: False
    trap_value:
        description: Enable or disable traps used with config_ntp command, list of dictionary vaules of enable and trap, see example below.
        type: list of dictionaries
        enable:
            description: enable or disable traps
            choices: True, False
            required: False
        trap:
            description: Select trap variable
            choices: "ntp-Mode-Change",
                     "ntp-Stratum-Change",
                     "ntp-Peer-Change",
                     "ntp-New-Association",
                     "ntp-Remove-Association",
                     "ntp-Config-Change",
                     "ntp-LeapSec-announced",
                     "Ntp-alive-Heartbeat",
                     "all"
        required: true
    keyValue:
        description: The string to be added to authentication KeyId used with config_ntp_keyId command
        required: False
    use_oobm:
        description: Use the OOBM interface to connect to the server used with config_ntp_ipv4addr command. Note not all devices have OOBM ports
        choices: True, False
        required: False


##### EXAMPLES
```YAML
      - name: configure timesync to be ntp
        arubaoss_ntp:
          command: "config_timesync"
          timesyncType: ntp

      - name: Enable NTP
        arubaoss_ntp:
          command: "config_ntp"
          config: create

      - name: Enable NTP in Unicast
        arubaoss_ntp:
          command: "config_ntp"
          config: create
          operate: "unicast"

      - name: Enable include Credentials
        arubaoss_ntp:
          command: "enable_includeCredentials"
          include_credentials_in_response: "ICS_ENABLED"

      - name: Configure ntp authentication keyID 2
        arubaoss_ntp:
          command: "config_ntp_keyId"
          authenticationMode: sha1
          keyId: 2
          keyValue: ARUBA
          trusted: True

      - name: Configure ntp server with keyID
        arubaoss_ntp:
          command: "config_ntp_ipv4addr"
          ntp_ip4addr: "10.20.40.33"
          keyId: 2
          mode: "iburst"

      - name: Configure ntp server 10.20.60.33 with iburst and using OOBM
        arubaoss_ntp:
          command: "config_ntp_ipv4addr"
          ntp_ip4addr: "10.20.60.33"
          mode: "iburst"
          use_oobm: True

      - name: configure ntp server time1.google.com
        arubaoss_ntp:
          command: "config_ntp_ipv4addr"
          ntp_ip4addr: "time1.google.com"
          mode: "iburst"

      - name: delete ntp server time1.google.com
        arubaoss_ntp:
          command: "config_ntp_ipv4addr"
          ntp_ip4addr: "time1.google.com"
          mode: "iburst"
          config: delete

      - name: Add NTP traps
        arubaoss_ntp:
          command: "config_ntp"
          config: create
          trap_value:
            - trap: "ntp-Stratum-Change"
            - trap: "ntp-Mode-Change"
            - trap: "ntp-Peer-Change"

      - name: Remove NTP traps
        arubaoss_ntp:
          command: "config_ntp"
          config: create
          trap_value:
            - enable: False
              trap: "ntp-Peer-Change"
            - enable: False
              trap: "ntp-Mode-Change"

      - name: Remove all NTP traps
        arubaoss_ntp:
          command: "config_ntp"
          trap_value: 
            - enable: False
              trap: "all"
```