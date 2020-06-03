# -*- coding: utf-8 -*-
#
# Copyright: (c) 2020, Andrew Riachi <ariachi@ku.edu>
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

class ModuleDocFragment(object):

    # Documenting arubaoss_top_spec from 
    # library/module_utils/network/arubaoss/arubaoss.py
    
    DOCUMENTATION = r'''
options:
    use_ssl:
        description:
            - Set to C(True) to use https.
            - Requires I(api_version) to be set.
        default: False
        type: bool
    validate_certs:
        description:
            - Whether or not to validate SSL certificates.
        default: False
        type: bool
    api_version:
        description:
            - The api version to use (e.g. C(v6.0)).
            - Required when I(use_ssl=True).
        default: 'None'
        type: str
'''