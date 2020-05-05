# File Transfer
Module: ****arubaoss_file_transfer****  
Description: "implements rest api's for file transfer from/to device"

##### LIMITATIONS
* Only HTTP/HTTPS urls are accepted for copying configurations, firmware, and logs  from/to the switch.
  * Recommended workaround is to use the SSH CLI module for copy commands that involve an SFTP or TFTP server. 

  
##### ARGUMENTS
    file_url:
        description:
            - Location of the file to which file needs to be transfered
              or from file needs to downloded to switch. This is http/https
              server, which needs to configured with default ports.
        required: True
    file_type:
        description:
            - Type of file that needs to be transfered. Defualt is
            firmware.
        default='FTT_FIRMWARE'
        choices='FTT_CONFIG','FTT_FIRMWARE','FTT_EVENT_LOGS',
                     'FTT_CRASH_FILES','FTT_SYSTEM_INFO','FTT_SHOW_TECH',
                     'FTT_DEBUG_LOGS'
        required: false
    action:
        description:
            - Type of action upload/download. Default is download.
        default='FTA_DOWNLOAD'
        choices='FTA_DOWNLOAD','FTA_UPLOAD'
        required: False
    show_tech_option:
        description:
            - Specifies type of show tech command to be executed.
        required: false
    boot_image:
        description:
            - Flash where image needs to be copied
        choices=['BI_PRIMARY_IMAGE','BI_SECONDARY_IMAGE']
    copy_iter:
        description:
            - Approx max iteration to wait for image copy to get completed.
            
            
##### EXAMPLES
```YAML
      - name: image download
        arubaoss_file_transfer:
          file_url: "http://192.168.1.2/WC_16_07_REL_XANADU_QA_062618.swi"
          file_type: "FTT_FIRMWARE"
          action: "FTA_DOWNLOAD"
```