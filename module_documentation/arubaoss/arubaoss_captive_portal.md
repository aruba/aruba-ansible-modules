# Captive Portal

Module: ****arubaoss_captive_portal****
Description: "Implements Ansible module for captive portal configuration."

##### ARGUMENTS
    profile_name:
        description:
            - captive portal profile name
        required: false
    server_url:
        description:
            - url for captive portal server
        required: false
    enable_captive_portal:
        description:
            - enable/disable captive portal on device
        required: false
    url_hash_key:
        description:
            - Hash key to verify integrity of the captive url
        required: false
    state:
        description:
            - Update or read captive protal data
        required: false
 
##### EXAMPLES
```YAML
      - name: enable/disable captive portal
        arubaoss_captive_portal:
          enable_captive_portal: "{{item}}"
        with_items:
          - False
          - True
      - name: add custom captive portal
        arubaoss_captive_portal:
          profile_name: "{{item}}"
          server_url: "http://arubanetworks.com"
        with_items:
          - test1
          - test2
      - name: add/remove url_has
        arubaoss_captive_portal:
          url_hash_key: "{{item}}"
        with_items:
          - ""
          - test1
```