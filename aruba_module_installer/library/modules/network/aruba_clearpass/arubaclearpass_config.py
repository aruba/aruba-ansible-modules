#!/usr/bin/python
DOCUMENTATION = """
---
module: aruba_clearpass_config
version_added: 0.1
short_description: Configure Aruba Clearpass using APIs.
options:
    host:
        decription:
            - Hostname or IP Address of the Aruba ClearPass
        required: true
    client_id:
        decription:
            - client id obtained from the Aruba ClearPass API client
        required: true
    client_secret:
        decription:
            - client secret obtained from the Aruba ClearPass API client
        required: true
    api_name:
        decription:
            - Name of the API to call
        required: true
    method:
        decription:
            - HTTP Method to be used for the API call
        required: true
        choises:
            - GET
            - POST
    data:
        decription:
            - JSON encoded data for the API call
        required: false
"""
EXAMPLES = """
#Usage Examples
    - name: Create node /md/branch1 in configuration hierarchy
      arubaclearpass_config:
        host: 192.168.1.1
        client_id: admin
        client_secret: aruba123
        api_name: network-device
        method: POST
        data: { "name": "new_switch", "ip_address": "1.1.1.1", "radius_secret": "aruba123", "vendor_name": "Aruba" }
"""

from ansible.module_utils.basic import *
from ansible.module_utils.urls import open_url
import json

def login_cppm(module, host, client_id, client_secret):
    resp = ""
    access_token = ""
    url = "https://" + str(host) + ":443/api/oauth"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    data = {"grant_type": "client_credentials","client_id": client_id,"client_secret": client_secret}
    module.api_call['url'] = url # Store the url to module, so we can print the details in case of error
    module.api_call['login_data'] = data
    try:
        resp = open_url(url=url, data=json.dumps(data), headers=headers, method="POST", validate_certs=False)
        if resp.code == 200:
            result = json.loads(resp.read())
            access_token = result["access_token"]
        else:
            module.fail_json(changed=False, msg="Login Failed!", reason="",
                api_call=module.api_call, response="HTTP status_code: " + str(resp.code) + " content: " +
                resp.read())
    except Exception as e:
        if resp == "": # Exception during http request, we have no response
             module.fail_json(changed=False, msg="API Call failed! Exception during login", reason=str(e),
                api_call=module.api_call)
        else:
            module.fail_json(changed=False, msg="API Call failed! Exception during login", reason=str(e),
                api_call=module.api_call, response="http status: " + str(resp.code) + " content: " + resp.read())
    return access_token

def cppm_api_call(module, host, access_token, api_name, method='GET', data={}):
    url = "https://" + str(host) + ":443/api/" + str(api_name)
    module.api_call['url'] = url # Store the url to module, so we can print the details in case of error
    try:
        if method == "GET":
            headers = {'Accept': 'application/json', 'Authorization': "Bearer " + access_token}
            resp = open_url(url=url, headers=headers, method="GET", validate_certs=False)
        else: # POST
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
                          'Authorization': "Bearer " + access_token}
            resp = open_url(url=url, data=json.dumps(data), headers=headers, method="POST", validate_certs=False)
        return resp
    except Exception as e:
        if "422" in str(e):
            module.exit_json(changed=False, msg=str(e) + "...Entry might exists on ClearPass")
        else:
            module.fail_json(changed=False, msg="API Call failed! Exception during api call", reason=str(e),
                api_call=module.api_call)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True, type='str'),
            client_id=dict(required=True, type='str'),
            client_secret=dict(required=True, type='str'),
            api_name=dict(required=True, type='str'),
            method=dict(required=True, type='str', choises=['GET', 'POST']),
            data=dict(required=False, type='dict')
        ))
    host = module.params.get('host')
    client_id = module.params.get('client_id')
    client_secret = module.params.get('client_secret')
    api_name = module.params.get('api_name')
    method = module.params.get('method')
    data = module.params.get('data')
    module.cookie_file = "aruba_cookie.pkl"
    module.api_call = {'host':host,'client_id':client_id,'client_secret':client_secret,'api_name':api_name,'method':method,'data':data, 'url':''}

    access_token = login_cppm(module, host, client_id, client_secret)
    resp = cppm_api_call(module, host, access_token, api_name, method=method, data=data)
    if resp.code == 200 or resp.code == 201:  # Success
        module.exit_json(changed=True, msg=resp.msg, status_code=int(resp.code), response=resp.read())

    else:  # Call failed
        err = json.loads(resp.read())
        module.fail_json(changed=False, msg="API Call failed!",
                         status_code=resp.code, reason=resp.msg + ", " + err.detail, api_call=module.api_call)


if __name__ == '__main__':
    main()
