#!/usr/bin/python
#
# Copyright (c) 2019-2020 Hewlett Packard Enterprise Development LP
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


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: arubaos_controller_config
version_added: 0.1
short_description: Configure ArubaOS products like Mobility Master and Mobility Controllers using AOS APIs
options:
    host:
        description:
            - Hostname or IP Address of the Mobility Master.
        required: false
    username:
        description:
            - Username used to login to the Mobility Master
        required: false
    password:
        description:
            - Password used to login to the Mobility Master
        required: false
    session_token:
        description:
            - Session Token string can be used instead of login using credentials
        required: False
    method:
        description:
            - HTTP Method to be used for the API call
        required: true
        choices:
            - GET
            - POST
    api_name:
        description:
            - ARUBA MM Rest API Object Name
        required: true
    config_path:
        description:
            - Path in configuration hierarchy to the node the API call is applied to
        required: false
    data:
        description:
            - dictionary data for the API call
        required: false
    verify_cert:
        description:
            - (Optional) Path to ca_cert. Defaults to "true" for installed certs. Set to "false" to prevent SSL cert check.
        choices:
            - /path/to/cert
            - false
            - true
        required: False
    client_cert:
        description:
            - (Optional) set the file path for client certificate validation from server side. Default option is None.
        required: false
    client_key:
        description:
            - (Optional) if the client_cert did not have the key, use this parameter. Default option is None.
        required: false
"""
EXAMPLES = """
#Usage Examples
    - name: Create a ssid profile with opmode by providing host and credentials.
      arubaos_controller_config:
        host: 192.168.1.1
        username: admin
        password: aruba123
        method: POST
        api_name: ssid_prof
        config_path: /md/branch1/building1
        data: { "profile-name": "test_ssid_profile", "essid" :{"essid":"test_employee_ssid"}, "opmode": {"name": "wpa-aes"}}


    - name: Configure a server group profile and add an existing radius server to it
      arubaos_controller_config:
        host: 192.168.1.1
        username: admin
        password: admin123
        method: POST
        api_name: server_group_prof
        config_path: /md/branch1/building1
        data: {"sg_name":"test", "auth_server": {"name": "test_rad_server"}}

"""
from ansible.module_utils.basic import *
import json
from ansible.module_utils.urls import open_url
import ansible.module_utils.six.moves.http_cookiejar as cookiejar
import requests

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

def login_api_mm(module):
    # Define variables from module arguments
    username = module.params.get('username')
    password = module.params.get('password')
    host = module.params.get('host')
    session_key = ""
    resp = ""
    # Variables required for open_url
    url = "https://" + str(host) + ":4343/v1/api/login"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    data = urlencode({'username': username, 'password': password})
    global cookies
    client_cert = module.params.get('client_cert')
    client_key = module.params.get('client_key')
    verify_cert = module.params.get('verify_cert')
    if verify_cert.lower() == "false":
        verify_cert = False
    elif verify_cert.lower() == "true":
        verify_cert = True
    http_agent = 'ansible-httpget'
    follow_redirects = 'urllib2'
    method = "POST"
    # Store the url to module, so we can print the details in case of error
    module.api_call = {'host':host,'username':username,'password':password, 'url':''}
    module.api_call['url'] = url

    try:
        resp = requests.post(url, data=data, headers=headers, verify=verify_cert,
			                cert=(client_cert, client_key))
        cookies = resp.cookies
        resp = resp.text
        result = json.loads(resp)['_global_result']
        if result['status'] == "0":
            session_key = result['UIDARUBA']
        else:
            module.fail_json(changed=False,
                             msg="Login Failed! Recheck the credentials you provided",
                             reason=str(result['status_str']),
                             api_call=module.api_call,
                             response="content: " + str(resp) + " login status code: " + str(result['status']) + " login error: " + str(result['status_str']))
    except Exception as e:
        module.fail_json(changed=False, msg="API Call failed! Exception during login", reason=str(e), api_call=module.api_call)

    session_dict = {'host':host,
                   'session_token': session_key}
    return session_dict

def logout(module, session_token):
    host = module.params.get('host')
    url = "https://" + str(host) + ":4343/v1/api/logout"
    headers = {'Accept': 'application/json', 'Cookie': 'SESSION=' + str(session_token)}
    client_cert = module.params.get('client_cert')
    client_key = module.params.get('client_key')
    verify_cert = module.params.get('verify_cert')
    if verify_cert.lower() == "false":
        verify_cert = False
    elif verify_cert.lower() == "true":
        verify_cert = True
    return requests.get(url, headers=headers, verify=verify_cert,
                    cookies=cookies,
                    cert=(client_cert, client_key))

def mm_api_call(module, session):
    host = module.params.get('host', session['host'])
    username = module.params.get('username')
    password = module.params.get('password')
    method = module.params.get('method')
    api_name = module.params.get('api_name')
    config_path = module.params.get('config_path')
    data = module.params.get('data')
    resp = ""
    client_cert = module.params.get('client_cert')
    client_key = module.params.get('client_key')
    verify_cert = module.params.get('verify_cert')
    if verify_cert.lower() == "false":
        verify_cert = False
    elif verify_cert.lower() == "true":
        verify_cert = True
    session_token = session['session_token']
    if not host:
        host = session['host']
    module.api_call = {'host':host,'username':username,'password':password,'api_name':api_name,'method':method,'config_path':config_path,'data':data, 'url':''}

    # Create the URL for the REST API call
    if config_path != None and config_path != "" and config_path != "null":
        url = "https://" + str(host) + ":4343/v1/configuration/object/" + str(api_name) + "?config_path=" + str(config_path) + "&UIDARUBA=" + str(session_token)
    else:
        url = "https://" + str(host) + ":4343/v1/configuration/object/" + str(api_name) + "?UIDARUBA=" + str(session_token)


    # Store the url to module, so we can print the details in case of error
    module.api_call['url'] = url

    try:
        # Data has to be json formatted
        if method == "GET":
            headers = {'Accept': 'application/json', 'Cookie': 'SESSION=' + str(session_token)}
            if api_name == "showcommand":
                params = {"command": data["command"], "UIDARUBA": str(session_token)}
                url = "https://" + str(host) + ":4343/v1/configuration/" + str(api_name) + "?" + urlencode(params)
            resp = requests.get(url, headers=headers, verify=verify_cert,
                            cookies=cookies, cert=(client_cert, client_key))

        else: # method is POST
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
                       'Cookie': 'SESSION=' + str(session_token)}

            data = json.dumps(data) #converts python object to json string that is readable by Ansible

            resp =  requests.post(url, data=data, headers=headers, verify=verify_cert,
                             cookies=cookies, cert=(client_cert, client_key))

        if resp.text == "" and resp.status_code == 200:
            logout(module, session_token)
            module.exit_json(changed=False, msg="Success", status_code=resp.status_code)
        elif resp.text == "" :
            raise Exception("API call failed with status code %d" % int(resp.status_code))
        result = json.loads(resp.text)

        if method == "POST":
            # Result will contain "Error" key if the request was made with wrong api name and data
            if "Error" in result.keys():
                logout(module, session_token)
                module.fail_json(changed=False, msg="API Call failed! Check api name and data", reason=result['Error'], api_call=module.api_call)

            result = result['_global_result']
            if result['status'] == 0:
                logout(module, session_token)
                module.exit_json(changed=True, msg=str(result['status_str']), status_code=int(resp.status_code))
            # Skip if result status is either 2 and 1. Example trying to delete something that do not exist will return such status
            elif result['status'] == 2 or result['status'] == 1:
                logout(module, session_token)
                module.exit_json(skipped=True, msg=str(result['status_str']), status_code=int(resp.status_code))
            else:
                logout(module, session_token)
                module.fail_json(changed=False, msg="API Call failed!", reason=result['status_str'], api_call=module.api_call)
        # if method is GET
        else:
            if resp.status_code == 200:
                logout(module, session_token)
                module.exit_json(changed=False, msg=result['_data'], status_code=resp.status_code, response=result)
            else:
                logout(module, session_token)
                raise Exception("API call failed with status code %d" % int(resp.status_code))

    except Exception as e:
        logout(module, session_token)
        module.fail_json(changed=False, msg=resp.status_code,
                         reason=str(e), api_call=module.api_call)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=False, type='str'),
            username=dict(required=False, type='str'),
            password=dict(required=False, type='str', no_log=True),
            api_name=dict(required=True, type='str'),
            method=dict(required=True, type='str', choices=['GET', 'POST']),
            config_path=dict(required=False, type='str'),
            data=dict(required=False, type='dict'),
            client_cert=dict(required=False, type="str", default=None),
            client_key=dict(required=False, type="str", default=None),
            verify_cert=dict(required=False, type="str", default=True),
            session_token=dict(required=False, type="str", default=None, no_log=True)
        ))
    session = None
    session_token =  module.params.get('session_token')
    # If session_token is not provided as module argument, call to generate the session_token
    if not session_token:
        ### Check if username, password, host is present in module args
        host = module.params.get('host')
        username = module.params.get('username')
        password = module.params.get('password')
        if host and username and password:
            session = login_api_mm(module)
        else:
            module.fail_json(changed=False, msg="Check if host, username and password are provided. Else generate session dict using arubaos session ansible module")
    elif session_token:
        session = {'host': module.params.get('host'),
                   'session_token': session_token}
    # Check if the sesstion token is present and call to POST/GET REST API commands
    #if session_token is not '' and session_token:
    if session and 'session_token' in session.keys():
        mm_api_call(module, session)
    else:
        module.fail_json(changed=False, msg="Unable to create the session token")


if __name__ == '__main__':
    cookies = ""
    main()
