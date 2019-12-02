#!/usr/bin/python
DOCUMENTATION = """
---
module: arubaos_cppm_config
version_added: 0.1
short_description: Call Mobility Master API
options:
    host:
        description: Hostname or IP Address of the Clearpass server.
        required: true
    api_name:
        description: API endpoint for which the request is made
        required: true
    method:
        description: HTTP Method to be used for the API call
        required: true
        choices: GET, DELETE, POST, PATCH, PUT
    access_token:
        description: Access token used to authenticate API calls
        required: false
    client_id:
        description: API client ID used to retrieve access tokens
        required: false
    client_secret:
        description: API Client secret used to retrieve access tokens
        required: false
    data:
        description: Dictionnary respresenting data to be sent with the request
        required: false
    validate_certs:
        description: Validate server certs when this is set to True
        required: false
    client_cert:
        description: (Optional) Provide the path to client cert file for validation in server side.
        required: false 
    client_key:
        description: If the provided client cert does not have the key in it, use this parameter
        required: false
"""
EXAMPLES = """
# Using client credentials
- name: Add new switch to network devices
    arubaos_cppm_config:
    host: 192.168.1.1
    client_id: apiadmin
    client_secret: 4O7QKMrpPiKFoMtR5J/2DQwC6TzHfUloJDJXSYkYl1Uc
    api_name: network-device
    method: POST
    data: { "name": "new_switch", "ip_address": "1.1.1.1", "radius_secret": "aruba123", "vendor_name": "Aruba" }
    validate_certs: True

# Using an access token
- name: Add new switch to network devices
    arubaos_cppm_config:
    host: 192.168.1.1
    access_token: 2c2a25d4dee25dab99e3d011d52a8247b11a40df
    api_name: network-device
    method: POST
    data: { "name": "new_switch", "ip_address": "1.1.1.1", "radius_secret": "aruba123", "vendor_name": "Aruba" }
    validate_certs: True
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
    validate_certs=module.params.get('validate_certs')
    client_cert=module.params.get('client_cert')
    client_key=module.params.get('client_key')
    try:
        resp = open_url(url=url, data=json.dumps(data), headers=headers, method="POST", validate_certs=validate_certs,
                        client_cert=client_cert, client_key=client_key)
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
    headers = ""
    resp = ""
    variableID = ""
    hard_list = ["user_id", "name", "mac_address"]
    validate_certs=module.params.get('validate_certs')
    client_cert=module.params.get('client_cert')
    client_key=module.params.get('client_key')
    try:
        if method == "GET" or method == "DELETE":
            headers = {'Accept': 'application/json', 'Authorization': "Bearer " + access_token}
            resp = open_url(url=url, headers=headers, method=method, validate_certs=validate_certs, 
                            client_cert=client_cert, client_key=client_key)
        else: # POST, PATCH
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
                          'Authorization': "Bearer " + access_token}
            resp = open_url(url=url, data=json.dumps(data), headers=headers, method=method, validate_certs=validate_certs,
                            client_cert=client_cert, client_key=client_key)
        return resp
    except Exception as e:
        if "422" in str(e):
            if method == "POST":
                try:
                    for ele in data.keys():
                        if ele in hard_list:
                            variableID = ele
                            break
                    if variableID:
                        ##### Convert _ to -
                        varIDEdit = variableID.replace("_", "-")
                        url = "https://" + str(host) + ":443/api/" + str(api_name) + "/" + str(varIDEdit) + "/" + data[variableID]
                        resp = open_url(url=url, data=json.dumps(data), headers=headers, method="PATCH", validate_certs=validate_certs,
                                        client_cert=client_cert, client_key=client_key)
                        return resp
                    else:
                        module.exit_json(skipped=True, msg=str(e) + "...Entry might exists on ClearPass")
                except Exception as err:
                    module.exit_json(skipped=True, msg=str(err) + "...Entry might exists on ClearPass")
        else:
            module.fail_json(changed=False, msg="API Call failed! Exception during api call", reason=str(e),
                api_call=module.api_call)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True, type='str'),
            api_name=dict(required=True, type='str'),
            access_token=dict(required=False, default=None),
            client_id=dict(required=False, type='str', default=None),
            client_secret=dict(required=False, type='str', default=None),
            method=dict(required=True, type='str', choices=['GET', 'DELETE','POST', 'PATCH', 'PUT']),
            data=dict(required=False, type='dict', default={}),
            validate_certs=dict(required=False, type='bool', default=False),
            client_cert=dict(required=False, type='str', default=None), 
            client_key=dict(required=False, type='str', default=None)
        ))
    host = module.params.get('host')
    client_id = module.params.get('client_id')
    client_secret = module.params.get('client_secret')
    api_name = module.params.get('api_name')
    method = module.params.get('method')
    data = module.params.get('data')
    access_token = module.params.get('access_token')
    module.cookie_file = "aruba_cookie.pkl"
    module.api_call = {
        'host':host,
        'api_name':api_name,
        'method':method,
        'data':data, 'url':''
    }
    if not access_token:
        if not (client_id and client_secret):
            module.fail_json(
                changed=False, msg="Either an access token or client credentials must be provided!",
                access_token=access_token, client_id=client_id, client_secret=client_secret
            )
        access_token = login_cppm(module, host, client_id, client_secret)
        module.api_call['client_id'] = client_id
        module.api_call['client_secret'] = client_secret
    else:
        module.api_call['access_token'] = access_token
    
    resp = cppm_api_call(module, host, access_token, api_name, method=method, data=data)
    if resp.code == 200 or resp.code == 201:  # Success
        if method in ["POST", "PUT", "PATCH"]:
            module.exit_json(changed=True, msg=resp.msg, status_code=int(resp.code), json=json.load(resp))
        else:
            module.exit_json(changed=False, msg=resp.msg, status_code=int(resp.code), json=json.load(resp))
    else:  # Call failed
        err = json.loads(resp.read())
        module.fail_json(changed=False, msg="API Call failed!",
                         status_code=resp.code, reason=resp.msg + ", " + err.detail, api_call=module.api_call)


if __name__ == '__main__':
    main()
