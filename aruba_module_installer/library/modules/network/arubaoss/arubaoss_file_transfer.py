#!/usr/bin/python
#
# Copyright (c) 2019 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: arubaoss_file_transfer

short_description: implements rest api's for file transfer from/to device

version_added: "2.6"

description:
    - "This implements rest api's for file transfer from/to device. The
       file get copied to from a http/https server. Server needs to be
       pre-configured to make use of this module. This module will not
       do firmware-ugrade but can copy image to flash. User can then
       use arubaoss_reboot to bringup device with that flash, thus
       provides firmware-upgrade"

extends_documentation_fragment:
    - arubaoss_rest

options:
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
        required: false
    action:
        description:
            - Type of action upload/download. Default is download.
        required: False
    show_tech_option:
        description:
            - Specifies type of show tech command to be executed.
        required: false
    boot_image:
        description:
            - Flash where image needs to be copied
    copy_iter:
        description:
            - Approx max iteration to wait for image copy to get completed.


author:
    - Ashish Pant (@hpe)
'''

EXAMPLES = '''
      - name: image download
        arubaoss_file_transfer:
          file_url: "http://192.168.1.2/WC_16_07_REL_XANADU_QA_062618.swi"
          file_type: "FTT_FIRMWARE"
          action: "FTA_DOWNLOAD"

'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec, arubaoss_required_if
from ansible.module_utils.network.arubaoss.arubaoss import get_config
import sys, json
from time import sleep, time

def wait_to_copy(module):
    params=module.params
    file_url = params['file_url'].split('/')
    file_name = file_url[len(file_url)-1]
    final_result= ""
    wait = 1
    while wait <= params['copy_iter']:
        check_presence = get_config(module, "/file-transfer/status")
        if not check_presence:
            final_result = 'FILE TRANSFER CHECK FAILED'
        else:
            newdata = json.loads(check_presence)
            final_result = newdata['status']
            if newdata['status'] == 'FTS_IN_PROGRESS':
                sleep(10)
                wait += 1
                continue
            else:
                break



    return final_result



def transfer(module):

    params = module.params
    url = '/file-transfer'
    data = {
            'file_type': params['file_type'],
            'action': params['action'],
            'url': params['file_url'],
            }
    if params['show_tech_option']:
        data['show_tech_option'] = params['show_tech_option']

    if params['boot_image']:
        data['boot_image'] = params['boot_image']
    result = run_commands(module, url, data, 'POST')
    message = result.get('body') or None
    if message and 'Another download is in progress' in message:
        result = {'changed': False}
        result['failed'] = True
        result['message'] = 'Another download is in progress'

    else:
        total_time = 0
        start = time()
        result  = wait_to_copy(module)
        end = time()
        total_time = int(end-start)

        if result == 'FTS_COMPLETED':
            result = {'changed':True,'msg': 'image transfer  successful.','total_time':total_time}

        else:
            message='image transfer failed with code: ' + result
            result = {'failed': True,'msg': message,'total_time': total_time}


    return result


def run_module():
    module_args = dict(
        file_type=dict(type='str', required=False, default='FTT_FIRMWARE',
            choices=['FTT_CONFIG','FTT_FIRMWARE','FTT_EVENT_LOGS',
                     'FTT_CRASH_FILES','FTT_SYSTEM_INFO','FTT_SHOW_TECH',
                     'FTT_DEBUG_LOGS']),
        file_url=dict(type='str', required=True),
        action=dict(type='str', required=False, default='FTA_DOWNLOAD',
            choices=['FTA_DOWNLOAD','FTA_UPLOAD']),
        show_tech_option=dict(type='str', required=False,
            choices=['STO_BASIC','STO_ALL','STO_BUFFERS','STO_INSTRUMENTATION',
                'STO_MSTP','STO_OOBM','STO_RAPID_PVST','STO_ROUTE','STO_SMART_LINK',
                'STO_STATISTICS','STO_TRANSCEIVERS','STO_TUNNEL_INTERCEPT',
                'STO_TUNNEL_TAP','STO_TUNNEL_VXLAN','STO_COMPONENTS']),
        boot_image=dict(type='str', required=False, default='BI_PRIMARY_IMAGE',
            choices=['BI_PRIMARY_IMAGE','BI_SECONDARY_IMAGE']),
        copy_iter=dict(type='int', required=False, default=20),
    )

    module_args.update(arubaoss_argument_spec)

    result = dict(changed=False,warnings='Not Supported')

    module = AnsibleModule(
        required_if=arubaoss_required_if,
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)
    try:
        result = transfer(module)
    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)


def main():
    run_module()

if __name__ == '__main__':
    main()
