#!/usr/bin/python
DOCUMENTATION = """
---
module: aruba_activate_config
version_added: 0.1
short_description: Configure Aruba Activate using APIs.
options:
    host:
        description:
            - Hostname or IP Address of the Aruba Activate
        required: true
    credential_0:
        description:
            - Username used to login to the Aruba Activate
        required: true
    credential_1:
        description:
            - Password used to login to the Aruba Activate
        required: true
    method:
        description:
            - HTTP Method to be used for the API call
        required: true
        choises:
            - GET
            - POST
    api_name:
        description:
            - ARUBA Activate Rest API Object Name
        required: true
    api_action:
        description:
            - ARUBA Activate action. (update/query)
        required: true
    data:
        description:
            - JSON encoded data for the API call
        required: true
    validate_certs: 
        description:
            - Set to True. Validates the server cert.
        required: false
"""
EXAMPLES = """
#Usage Examples
    - name: Add Folder
      arubaactivate_config:
        credential_0: "{{ activate_username }}"
        credential_1: "{{ activate_password }}"
        method: "{{ api_method }}"
        api_name: "folder"
        api_action: "update"
        data: 'json={ "folders": [ { "parentId": "4d4b127e-a7ab-4d89-9e07-508c3b529975", "folderName": "New_Test_folder"}]}'
        validate_certs: True
"""

from ansible.module_utils.basic import *
from ansible.module_utils.urls import open_url
import ansible.module_utils.six.moves.http_cookiejar as cookiejar
#import json
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

def login_activate(module, credential_0, credential_1):
    set_cookie = ""
    resp = ""
    url = "https://activate.arubanetworks.com/LOGIN"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': 'Activate-cookie.text'}
    data = {"credential_0": credential_0 ,"credential_1": credential_1 }
    cookies = cookiejar.LWPCookieJar()
    validate_certs = module.params.get('validate_certs')
    try:
        resp = open_url(url=url, data=urlencode(data), headers=headers, method="POST", validate_certs=validate_certs, cookies=cookies)
        if resp.code == 200:
            cookie_list = []
            for ck in cookies:
                cookie_list.append(str(ck.name) + "="+ str(ck.value))
            set_cookie = "; ".join(cookie_list)
        else:
            module.fail_json(changed=False, msg="Login Failed!", reason=resp.read(),
                response="HTTP status_code: " + str(resp.code))
    except Exception as e:
        module.fail_json(changed=False, msg="API Call failed! Exception during login", reason=str(e))
    return set_cookie

def activate_api_call(module, set_cookie, api_name, api_action, method='GET', data={}):
    resp = ""
    validate_certs = module.params.get('validate_certs')
    url = "https://activate.arubanetworks.com/api/ext/" + str(api_name) + ".json?action=" + str(api_action)
    try:
        if method == "GET":
            headers = {'Accept': 'application/json', 'Cookie': str(set_cookie)}
            resp = open_url(url=url, headers=headers, method=method, validate_certs=validate_certs)
        else: # method is POST
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
                       'Cookie': str(set_cookie)}
            resp = open_url(url=url, headers=headers, method="POST", validate_certs=validate_certs, data=data)

    except Exception as e:
        module.fail_json(changed=False, msg="API Call failed! Exception during api call", reason=str(e))
    return resp

def main():
    module = AnsibleModule(
        argument_spec=dict(
            credential_0=dict(required=True, type='str'),
            credential_1=dict(required=True, type='str'),
            api_name=dict(required=True, type='str'),
            api_action=dict(required=True, type='str'),
            method=dict(required=True, type='str', choises=['GET', 'POST']),
            data=dict(required=True, type='str'),
            validate_certs=dict(required=False, type='bool', default=False)
        ))
    credential_0 = module.params.get('credential_0')
    credential_1 = module.params.get('credential_1')
    method = module.params.get('method')
    api_name = module.params.get('api_name')
    api_action = module.params.get('api_action')
    data = module.params.get('data')

    set_cookie = login_activate(module, credential_0, credential_1)
    resp = activate_api_call(module, set_cookie, api_name, api_action, method=method, data=data)

    if resp.code == 200:  # Success
        module.exit_json(changed=True, msg=str(resp.read()), status_code=int(resp.code))

    else:  # Call failed
        module.fail_json(changed=False, msg="API Call failed!",
                         status_code=resp.code, reason=resp.msg)

if __name__ == '__main__':
    main()
