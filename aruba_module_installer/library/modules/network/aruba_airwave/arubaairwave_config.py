#!/usr/bin/python
DOCUMENTATION = """
---
module: aruba_airwave_config
version_added: 0.1
short_description: Configure Aruba Airwave using APIs.
options:
    host:
        description:
            - Hostname or IP Address of the Aruba Airwave
        required: true
    credential_0:
        description:
            - Username used to login to the Aruba Airwave
        required: true
    credential_1:
        description:
            - Password used to login to the Aruba Airwave
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
            - API endpoint for which the request is made
        required: True
    data:
        description:
            - JSON encoded data for the API call
        required: false
    params:
        description:
            - parameters for required for some query operations in dictionary
              format.
        required: false
    validate_certs:
        description:
            - Validate server certs when this is set to True
        required: false
    client_cert:
        description: (Optional)Provide the path to client cert file for validation in server side.
        required: false
    client_key:
        description: If the provided client cert does not have the key in it, use this parameter
        required: false
"""
EXAMPLES = """
#Usage Examples
    - name: Upload csv file
      arubaairwave_config:
          host: 192.168.1.1
          credential_0: admin
          credential_1: admin123
          method: POST
          api_name: api/ap_whitelist_upload
          data: "csv={{ csv_file_content }}&append_whitelist=0"

    - name: AP search query
      arubaairwave_config:
        host: 192.168.1.1
        credential_0: admin
        credential_1: admin123
        method: GET
        api_name: ap_search.xml
        params: { "query" : "cf:32"}

"""
from ansible.module_utils.basic import *
from ansible.module_utils.urls import open_url
import ansible.module_utils.six.moves.http_cookiejar as cookiejar

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def login_amp(module, host, credential_0, credential_1):
    return_list = []
    resp = ""
    url = "https://" + str(host) + "/LOGIN"
    headers = { 'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    data = 'credential_0=' + credential_0 + '&credential_1=' + credential_1 + '&destination=/&login=Log In'
    cookies = cookiejar.LWPCookieJar()
    validate_certs = module.params.get('validate_certs')
    client_cert= module.params.get('client_cert')
    client_key= module.params.get('client_key')
    try:

        resp = open_url(url, headers=headers, method="POST", validate_certs=validate_certs, data=data, cookies=cookies, client_cert=client_cert, client_key=client_key)
        if resp.code == 200:
            ## Extract Biscotti from headers
            if "X-BISCOTTI" in resp.headers:
                x_biscotti = resp.headers.get("X-BISCOTTI")
                return_list.append(x_biscotti)
            ## Extract session key from cookie
            for set_cookie in cookies:
                set_cookie = set_cookie.value
                return_list.append(set_cookie)

        else:
            module.fail_json(changed=False, msg="Login Failed!", reason=resp.text,
                response="HTTP status_code: " + str(resp.status_code))
    except Exception as e:
        module.fail_json(changed=False, msg="API Call failed! Exception during login", reason=str(e))
    return return_list

def amp_api_call(module, x_biscotti, set_cookie, host, api_name, method='GET', data={}, params=None):
    url = "https://" + str(host) + "/" + str(api_name)
    cookies = cookiejar.LWPCookieJar()
    validate_certs = module.params.get('validate_certs')
    client_cert= module.params.get('client_cert')
    client_key= module.params.get('client_key')
    http_agent = 'ansible-httpget'
    follow_redirects = 'urllib'
    try:
        if method == "GET":
            if params:
                params = urlencode(params)
                url= url + "?" + params
            headers = { 'Cookie' : 'MercuryAuthHandlerCookie_AMPAuth=' + set_cookie }
            resp = open_url(url, headers=headers, validate_certs=validate_certs)

        else: # POST
            headers = {'Cookie' : 'MercuryAuthHandlerCookie_AMPAuth=' + set_cookie, 'X-BISCOTTI' : x_biscotti }
            resp = open_url(url, headers=headers, method=method, validate_certs=validate_certs, data=data, client_cert=client_cert, client_key=client_key)

    except Exception as e:
        module.fail_json(changed=False, msg="API Call failed! Exception during api call", reason=str(e))
    return resp

def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True, type='str'),
            credential_0=dict(required=True, type='str'),
            credential_1=dict(required=True, type='str'),
            api_name=dict(required=True, type='str'),
            method=dict(required=True, type='str', choises=['GET', 'POST']),
            data=dict(required=False, type='str'),
            params=dict(required=False, type='dict'),
            validate_certs=dict(required=False, type='bool', default= False),
            client_cert=dict(required=False, type='str', default= None),
            client_key=dict(required=False, type='str', default= None)
        ))
    host = module.params.get('host')
    credential_0 = module.params.get('credential_0')
    credential_1 = module.params.get('credential_1')
    method = module.params.get('method')
    api_name = module.params.get('api_name')
    data = module.params.get('data')
    params = module.params.get('params')

    access_token = login_amp(module, host, credential_0, credential_1)
    x_biscotti = access_token[0]
    set_cookie = access_token[1]
    resp = amp_api_call(module, x_biscotti, set_cookie, host, api_name, method=method, data=data, params=params)

    if resp.code == 200:  # Success
        module.exit_json(changed=True, msg=str(resp.read()), status_code=int(resp.code))

    else:  # Call failed
        module.fail_json(changed=False, msg="API Call failed!",
                         status_code=resp.code, reason=resp.reason)


if __name__ == '__main__':
    main()


# python testpython.py '{"ANSIBLE_MODULE_ARGS":{"host":"10.127.16.30","username":"admin","password":"Aruba@123","api_name":"/api/ap_whitelist_upload","method":"POST","data": {"append_whitelist":0, "csv":"Modify authorized device,Name,LAN MAC Address,Serial Number,Group Name,Folder Name,cppm_1,cppm_key_1,int_controller_vlan,cppm_role,vlan_user_1,controller_role,tunneled_ports,untagged_vlan_1_ports,ap_vlan,untagged_ap_vlan_ports,tagged_ap_vlan_ports\n1,Switch-1,94:f1:28:8b:14:10,CN83HKZ0XF, Group-1, Folder-1, 10.127.16.20, Aruba@123,10.127.17.11, Tunnel, 16,authenticated,0,"6-10",17, 1-3, 8"}}}'
