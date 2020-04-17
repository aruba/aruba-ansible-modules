#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Sacha Boudjema <sachaboudjema@gmail.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r'''
    options:
        host:
            description:
                - Hostname or IP Address of the controller.
                - If not set the environment variable C(ANSIBLE_ARUBAOS_HOST) will be used.
            required: true
            type: str
        username:
            description:
                - Username used to login to the controller.
                - If not set the environment variable C(ANSIBLE_ARUBAOS_USERNAME) will be used.
            required: true
            type: str
        password:
            description:
                - Password used to login to the controller.
                - If not set the environment variable C(ANSIBLE_ARUBAOS_PASSWORD) will be used.
            required: true
            type: str
            no_log: true
        validate_certs:
            description:
                - Set to True to validate server SSL certificate upon HTTPS connection. Default option is false.
            required: false
            type: str
            default: None
        client_cert:
            description:
                - Set the file path for client certificate validation from server side. Default option is None.
            required: false
            type: str
            default: None
        client_key:
            description:
                - If the client_cert did not have the key, use this parameter. Default option is None.
            required: false
            type: str
            default: None
    seealso:
        - name: ArubaOS 8.x API Guide
          description: Complete description of ArubaOS API methods with examples.
          link: https://asp.arubanetworks.com/downloads;fileTypes=DOCUMENT;products=Aruba%20Mobility%20Controllers%20%28AOS%29;fileContents=API%20Guide
        - name: ArubaOS API Explorer
          description: Complete reference of ArubaOS API data model.
          link: https://<your_controller>:4343/api/
    notes:
        - Supports check-mode.
        - ArubaOS version 8.0.0.0 or later required.
    '''
