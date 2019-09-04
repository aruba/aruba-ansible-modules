#!/usr/bin/python

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: arubaiap_config
version_added: 0.1
short_description: Configures and monitors IAP in either master, slave or standalone mode using APIs
options:
    host:
        description:
            - Hostname or IP Address of the Virtual Controller.
        required: false
    username:
        description:
            - Username used to login to the Virtual Controller/Master IAP
        required: false
    password:
        description:
            - Password used to login to the Virtual Controller/Master IAP
        required: false
    method:
        description:
            - HTTP Method to be used for the API call
        required: true
        choices:
            - GET
            - POST
    session:
        description:
            - The session variable is a dictionary returned by arubaos session ansible module
        required: false
    api_type:
        description:
            - type of API used for interacting with the iap
        required: true
        choices:
            - action
            - configuration
            - monitoring
    api_name:
        description:
            - IAP Rest API Object Name
        required: true
    config_path:
        description:
            - Path in configuration hierarchy to the node the API call is applied to
        required: false
    data:
        description:
            - dictionary data for the API call
        required: false
"""
EXAMPLES = """
#Usage Examples
    - name: Change the hostname of a particular IAP
      iap_config:
        host: 1.1.1.1
        username: admin
        password: aruba123
        method: POST
        api_type: action
        api_name: hostname
        data: { "iap_ip_addr": "2.2.2.2", "hostname_info": {"hostname": "iap-floor1-building1"}}

    - name: Change the hostname of a particular IAP
      arubaiap_config:
        session: {{ session_dict.msg }}
        method: POST
        api_type: action
        api_name: hostname
        data: { "iap_ip_addr": "2.2.2.2", "hostname_info": {"hostname": "iap-floor1-building1"}}

    - name: Configure a Management User
      arubaiap_config:
        host: 1.1.1.1
        username: admin
        password: admin123
        method: POST
        api_type: configuration
        api_name: mgmt-user
        data: {"action" : "create","username" : "admin-new", "cleartext_password" : "aruba123", "usertype" : "guest-mgmt"}}

    - name: Show a existing network
      arubaiap_config:
        host: 1.1.1.1
        username: admin
        password: admin123
        method: GET
        api_type: monitoring
        api_name: show network

"""
from ansible.module_utils.basic import *
import json
from ansible.module_utils.urls import open_url
import ansible.module_utils.six.moves.http_cookiejar as cookiejar

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

def login_api_mm(module):
    # Define variables from module arguments
    host = module.params.get('host')
    username = module.params.get('username')
    password = module.params.get('password')
    session_key = ""
    resp = ""
    # Variables required for open_url
    url = "https://" + str(host) + ":4343/rest/login"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    data = {'user': username, 'passwd': password}
    data = json.dumps(data)
    cookies = cookiejar.LWPCookieJar()
    validate_certs = False
    http_agent = 'ansible-httpget'
    follow_redirects = 'urllib2'
    method = "POST"

    module.api_call = {'host':host,'user':username,'passwd':password, 'url':''}
    module.api_call['url'] = url # Stores the url to module, so we can print the details in case of error

    try:
        resp = open_url(url, data=data, headers=headers, method=method, validate_certs=validate_certs, http_agent=http_agent, follow_redirects=follow_redirects, cookies=cookies)
        resp = resp.read()
        result = json.loads(resp)

        if result['Status'] == "Success":
            session_key = result['sid']
        else:
            module.fail_json(changed=False, msg="Login Failed! Recheck the credentials you provided", reason=str(result), api_call=module.api_call, response="content: " + str(resp) + " login status code: " + str(result['status']) + " login error: " + str(result['status_str']))

    except Exception as e:
        module.fail_json(changed=False, msg="API Call failed! Exception during login", reason=str(e), api_call=module.api_call)

    session_dict = {'host':host,
                   'session_token': session_key}
    return session_dict

def mm_api_call(module, session):
    host = module.params.get('host', session['host'])
    username = module.params.get('username')
    password = module.params.get('password')
    method = module.params.get('method')
    api_type = module.params.get('api_type')
    api_name = module.params.get('api_name')
    iap_ip_addr = module.params.get('iap_ip_addr')
    config_path = module.params.get('config_path')
    data = module.params.get('data')
    cookies = cookiejar.LWPCookieJar()
    resp = ""
    validate_certs = False
    http_agent = 'ansible-httpget'
    follow_redirects = 'urllib2'
    session_token = session['session_token']
    if not host:
        host = session['host']
    module.api_call = {'host':host,'username':username,'password':password,'api_name':api_name,'method':method,'config_path':config_path,'data':data, 'url':''}

    # Create the URL for the REST API call

    if api_type == 'action' or api_type == 'configuration':
        if method == 'POST':
            url = "https://" + str(host) + ":4343/rest/" + str(api_name) + "?sid=" + str(session_token)
            module.api_call['url'] = url # Store the url to module, so we can print the details in case of error
        else:#method is GET
            module.fail_json(changed=False, failed=True, msg="Action APIs and Configuartion APIs should have 'POST' as the method, since they are only used to add new data, modify or delete existing data")

    elif api_type == 'monitoring':
        if method == 'GET':
            api_name = api_name.replace(" ","%20")
            url = "https://" + str(host) + ":4343/rest/show-cmd?iap_ip_addr=" +str(iap_ip_addr) + "&cmd=" + str(api_name) + "&sid=" + str(session_token)
            module.api_call['url'] = url # Store the url to module, so we can print the details in case of error

        else:#method is POST
            module.fail_json(changed=False, failed=True, msg="Monitoring APIs or show commands should have 'GET' as the method.")


    try:
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Cookie': 'SESSION=' + str(session_token)}
        # Data has to be json formatted
        data = json.dumps(data) #converts python object to json string that is readable by Ansible
        resp =  open_url(url, data = data, headers=headers, method=method, validate_certs=validate_certs, http_agent=http_agent, follow_redirects=follow_redirects, cookies=cookies)
        result = json.loads(resp.read())

        if result['Status'] == 'Success':
            module.exit_json(changed=True, msg=str(result), status_code=int(resp.code))
        else:
            module.fail_json(changed=False, msg="API Call failed!", reason=result['status_str'], api_call=module.api_call)

    except Exception as e:
        module.fail_json(changed=False, msg="API Call failed! Exception during api call",
                         reason=str(e), api_call=module.api_call)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=False, type='str'),
            username=dict(required=False, type='str'),
            password=dict(required=False, type='str'),
            session=dict(required=False, type='dict'),
            api_type=dict(required=True, type='str', choices=['action','configuration', 'monitoring']),
            api_name=dict(required=True, type='str'),
            iap_ip_addr=dict(required=False, type='str'),
            method=dict(required=True, type='str', choices=['GET','POST']),
            data=dict(required=False, type='dict')
        ))

    session =  module.params.get('session', None)

    # If session_token is not provided as module argument, call login function to generate the session_token
    if not session or 'session_token' not in session.keys():
        # Check if username, password, host is present in module args
        host = module.params.get('host')
        username = module.params.get('username')
        password = module.params.get('password')

        if host and username and password:
            session = login_api_mm(module)
        else:
            module.fail_json(changed=False, msg="Check if host, username and password are provided. Else generate session dict using arubaos session ansible module")

    # Check if the sesstion token is present and call to POST/GET REST API commands
    if session and 'session_token' in session.keys():
        mm_api_call(module, session)
    else:
        module.fail_json(changed=False, msg="Unable to create the session token")


if __name__ == '__main__':
    main()
