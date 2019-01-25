# Reboot
Module: ****arubaoss_reboot****  
Description: "This reboots the device and waits until it comes up. User has an option to disable the wait and just send the reboot to device"

##### ARGUMENTS
    boot_image:
        description:
            - Boots device using this image
        default: BI_PRIMARY_IMAGE
        choices: BI_PRIMARY_IMAGE, BI_SECONDARY_IMAGE
        required: true
    is_wait:
        description:
            - Wait for boot or skip the reboot
        default: true
        choice: true, false
        required: false

##### EXAMPLES
```YAML
      - name: reboot device
        arubaoss_reboot:
          boot_image: BI_SECONDARY_IMAGE
          is_wait: False
```