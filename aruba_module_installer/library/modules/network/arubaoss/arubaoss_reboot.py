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
module: arubaoss_reboot

short_description: reboots the device

version_added: "2.6"

description:
    - "This reboots the device and waits until it comes up.
       User has an option to disable the wait and just send
       the reboot to device"

options:
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

author:
    - Ashish Pant (@hpe)
'''

EXAMPLES = '''
      - name: reboot device
        arubaoss_reboot:
          boot_image: BI_SECONDARY_IMAGE
          is_wait: False

'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands,get_config
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec
from time import sleep, time


def wait_for_boot(module):

    url = '/system/status'
    wait = 1

    msg_queue = []
    while wait <= 60:
        result = get_config(module, url, check_login=False)
        if result:
            return result

        sleep(5)
        wait += 1

    return False


def reboot(module):

    params = module.params
    url = '/system/reboot'

    status_url = '/system/status'
    result = get_config(module, status_url)
    if not result:
        return {'msg':'Could not get devcie status. Not rebooted!','changed':False,
                'failed':True}

    data = {
            'boot_image': params['boot_image'],
            }

    result = run_commands(module, url, data, 'reboot')
    total_time = 0

    if result['message'] == 'Device is rebooting' and params['is_wait']:
        start = time()
        result  = wait_for_boot(module)

        end = time()
        total_time = int(end-start)

        if result:
            result = {'changed':True,'msg': 'Device reboot successful.','total_time':total_time}
        else:
            result = {'failed': True,'msg': 'Device reboot failed.','total_time': total_time}



    return result


def run_module():
    module_args = dict(
        boot_image=dict(type='str', required=False, default='BI_PRIMARY_IMAGE',
            choices=['BI_PRIMARY_IMAGE','BI_SECONDARY_IMAGE']),
        is_wait=dict(type='bool', required=False, default=True)
    )

    module_args.update(arubaoss_argument_spec)

    result = dict(changed=False,warnings='Not Supported')

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    try:
        result = reboot(module)
    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)


def main():
    run_module()

if __name__ == '__main__':
    main()
