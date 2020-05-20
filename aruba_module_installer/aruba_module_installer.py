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

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from subprocess import check_output
from shutil import copytree, copyfile, rmtree
from os.path import dirname, realpath, exists, isdir
from os import remove
from sys import exit
from re import search
import errno


COLORRED = "\033[0;31m{0}\033[00m"

SW_PATHS = {'module': 'modules/network/arubaoss',
            'module_utils': 'module_utils/network/arubaoss',
            'plugins_action': 'plugins/action/arubaoss.py',
            'plugins_cliconf': 'plugins/cliconf/arubaoss.py',
            'plugins_terminal': 'plugins/terminal/arubaoss.py',
            'plugins_doc_fragments': 'plugins/doc_fragments/arubaoss_rest.py'
            }
CONTROLLER_PATHS = {'module': 'modules/network/arubaos_controller'}
CONTROLLER_SSH_PATHS = {'module': 'modules/network/aruba',
                       'plugins_cliconf': 'plugins/cliconf/aruba.py',
                       'plugins_terminal': 'plugins/terminal/aruba.py',
                       'plugins_action': 'plugins/action/aruba.py'
                      }
AIRWAVE_PATHS = {'module': 'modules/network/aruba_airwave'}
CLEARPASS_PATHS = {'module': 'modules/network/aruba_clearpass'}
ACTIVATE_PATHS = {'module': 'modules/network/aruba_activate'}
INSTANT_PATHS = {'module': 'modules/network/aruba_instant'}


CMD = 'ansible --version'

SRC_PATH = dirname(realpath(__file__))+'/library/'

ANS_PATH = ''

def define_arguments():
    """
    Define arguments that this script will use.
    :return: Populated argument parser
    """

    description = ('This tool installs all files/directories required by '
                   'Ansible for AOS-Switch, Airwave, Clearpass, Activate,'
                   ' Instant, and ArubaOS Controller integration.\n\n'
                   'Requirements:'
                   '\n\t- Linux OS only'
                   '\n\t- Ansible release version 2.5 or later installed'
                   '\n\t- Python 2.7 or 3.5+ installed'
                   )

    epilog = ('Directories added:'
              '\n\t- <ansible_module_path>/modules/network/arubaoss'
              '\n\t- <ansible_module_path>/module_utils/network/arubaoss'
              '\n\t- <ansible_module_path>/modules/network/arubaos_controller'
              '\n\t- <ansible_module_path>/modules/network/aruba_airwave'
              '\n\t- <ansible_module_path>/modules/network/aruba_clearpass'
              '\n\t- <ansible_module_path>/modules/network/aruba_activate'
              '\n\t- <ansible_module_path>/modules/network/aruba_instant'
              '\n\n'
              'Files added/modified:'
              '\n\t- <ansible_module_path>/plugins/action/arubaoss.py'
              '\n\t- <ansible_module_path>/config/base.yml'
              '\n\t- <ansible_module_path>/plugins/terminal/aruba.py'
              '\n\t- <ansible_module_path>/plugins/cliconf/aruba.py'
              '\n\t- <ansible_module_path>/plugins/action/aruba.py'
              '\n\t- <ansible_module_path>/modules/network/aruba/aruba_command.py'
              '\n\t- <ansible_module_path>/modules/network/aruba/aruba_config.py'
             )

    parser = ArgumentParser(description=description,
                            formatter_class=RawDescriptionHelpFormatter,
                            epilog=epilog)
    parser.add_argument('-r', '--remove', required=False,
                        help=('remove all files & directories installed '
                              'by this script.'),
                        action='store_true')
    parser.add_argument('--reinstall', required=False,
                        help=('remove all files & directories installed '
                              'by this script. Then re-install.'),
                        action='store_true')

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--switch', required=False,
                       help=('only install files/directories required for '
                             'AOS-Switch.'
                             ),
                       action='store_true')
    group.add_argument('--controller', required=False,
                       help=('only install files/directories required for '
                             'ArubaOS-Controller.'
                             ),
                       action='store_true')
    group.add_argument('--activate', required=False,
                       help=('only install files/directories required for '
                             'Aruba-Activate.'
                             ),
                       action='store_true')
    group.add_argument('--airwave', required=False,
                       help=('only install files/directories required for '
                             'Aruba-AirWave.'
                             ),
                       action='store_true')
    group.add_argument('--clearpass', required=False,
                       help=('only install files/directories required for '
                             'Aruba-ClearPass.'
                             ),
                       action='store_true')
    group.add_argument('--instant', required=False,
                       help=('only install files/directories required for '
                             'Aruba-Instant.'
                             ),
                       action='store_true')
    return parser.parse_args()


def find_module_path():
    """
    A helper function to validate Ansible version and parse for python
    module path.
    :return: str re_path: The string value of the module path or None if
                         failure
    """
    global CMD, COLORRED

    output = check_output(CMD, shell=True).strip()

    re_path = search(r"ansible python module location = (?P<path>\S+)",
                     output.decode('utf-8'))

    re_version = search(r"ansible\s(?P<version>\d\S+\d)", output.decode('utf-8'))

    if re_path and re_version:

        re_version = re_version.groupdict()['version']
        re_path = re_path.groupdict()['path']

        # Validate Ansible version is supported
        if '2.5' <= re_version <= '2.9.9':
            return re_path+'/'
        else:
            exit(COLORRED.format('There was an issue with your '
                                 'ansible version: {}\n'
                                 'The Aruba Modules support Ansible release '
                                 'versions 2.5 or later.').format(re_version))
    else:
        exit(COLORRED.format('There was an issue finding your '
                             'ansible version.\n'
                             'Please run \'ansible --version\' from bash'
                             ', resolve any errors, and verify version'
                             ' is release version 2.5 or later.'))


def install_sw_modules():
    """
    Installs all files/directories required by Ansible for AOS-Switch
    integration. Modifies base.yml to include 'arubaoss' modules in
    'NETWORK_GROUP_MODULES'.

    Directories added:
        <ansible_module_path>/modules/network/arubaoss
        <ansible_module_path>/module_utils/network/arubaoss

    Files added/modified:
        <ansible_module_path>/plugins/action/arubaoss.py
        <ansible_module_path>/config/base.yml

    :return: None
    """

    global SW_PATHS, SRC_PATH, COLORRED, ANS_PATH

    base_yml = ANS_PATH+'config/base.yml'

    # Copy each directory and file to ansible module location
    for source, path in SW_PATHS.items():
        # If directories or files exist already, do nothing
        if exists(ANS_PATH+path):
            print(COLORRED.format('{} already exists'
                                  ' at {}...\n'.format(path, ANS_PATH+path)))
        else:
            print('Copying {} to {}...\n'.format(path, ANS_PATH+path))
            if isdir(SRC_PATH+path):
                copytree(SRC_PATH+path, ANS_PATH+path)
            else:
                copyfile(SRC_PATH+path, ANS_PATH+path)

    # Modifies base.yml to include arubaoss modules
    # If base.yml doesn't exist, invalid ansible version is installed
    if exists(base_yml):
        with open(base_yml, 'r') as f:
            base_contents = f.read()

        re_modules = (r"NETWORK_GROUP_MODULES:\s*"
                      r"name:.*\s*"
                      r"default:\s(?P<modules>\[.*\])")

        re_result = search(re_modules, base_contents)

        if re_result:
            if len(re_result.groups('modules')) == 1:
                old_string = re_result.groups('modules')[0]
                if 'arubaoss' not in old_string:
                    new_string = old_string.replace(']', ', arubaoss]')
                    new_base_contents = base_contents.replace(old_string,
                                                              new_string)
                    with open(base_yml, 'w') as f:
                        f.write(new_base_contents)
                    print(
                        '{} modification successful...\n'.format(base_yml))
                else:
                    print(COLORRED.format('{}: arubaoss already '
                                          'exists...\n'.format(base_yml)))
            else:
                exit(COLORRED.format('Multiple instances of '
                                     'NETWORK_GROUP_MODULES found...\n'
                                     'Modification of {} failed...'
                                     .format(base_yml)))

    else:
        exit(COLORRED.format('No base.yml found...Please ensure you have '
                             'Ansible 2.5 or later...\n'
                             'Modification of {} failed...'.format(base_yml)))


def install_wlan_modules(install_package=None):
    """
    Installs files/directories required by Ansible for Aruba Wlan integration.
    Provide the argument to install a specific package during script execution.

    Directories added/modified to the path:
        <ansible_module_path>/modules/network/aruba_airwave
        <ansible_module_path>/modules/network/aruba_clearpass
        <ansible_module_path>/modules/network/aruba_activate
        <ansible_module_path>/modules/network/arubaos_controller
        <ansible_module_path>/modules/network/aruba_instant

    Files added/modified:
        <ansible_module_path>/modules/network/aruba/aruba_command.py
        <ansible_module_path>/modules/network/aruba/aruba_config.py
        <ansible_module_path>/plugins/terminal/aruba.py
        <ansible_module_path>/plugins/cliconf/aruba.py
        <ansible_module_path>/plugins/action/aruba.py

    :return: None
    """

    global ANS_PATH

    path_list = [CONTROLLER_PATHS, AIRWAVE_PATHS, CLEARPASS_PATHS,
                 ACTIVATE_PATHS, INSTANT_PATHS, CONTROLLER_SSH_PATHS]

    #If an argument is specified, install only that package.
    #Otherwise installs all the packages
    if install_package and install_package != '':
        path_list = [install_package]

    # Copy each directory and file to ansible module location
    for aPath in path_list:
        for source, path in aPath.items():
            # If directories or files exist already, do nothing
            if exists(ANS_PATH+path):
                print(COLORRED.format('{} already exists'
                                      ' at {}...\n'.format(path, ANS_PATH+path)))
            else:
                print('Copying {} to {}...\n'.format(path, ANS_PATH+path))
                if isdir(SRC_PATH+path):
                    copytree(SRC_PATH+path, ANS_PATH+path)
                else:
                    copyfile(SRC_PATH+path, ANS_PATH+path)


def remove_modules():
    """
    Removes all files/directories installed by this script for
    module integration in Ansible. Modifies base.yml to remove 'arubaoss'
    'NETWORK_GROUP_MODULES'.

    Directories removed:
        <ansible_module_path>/modules/network/arubaoss
        <ansible_module_path>/module_utils/network/arubaoss
        <ansible_module_path>/modules/network/aruba_airwave
        <ansible_module_path>/modules/network/aruba_clearpass
        <ansible_module_path>/modules/network/aruba_activate
        <ansible_module_path>/modules/network/arubaos_controller
        <ansible_module_path>/modules/network/aruba_instant

    Files removed/modified:
        <ansible_module_path>/plugins/action/arubaoss.py
        <ansible_module_path>/config/base.yml
        <ansible_module_path>/modules/network/aruba/aruba_command.py
        <ansible_module_path>/modules/network/aruba/aruba_config.py
        <ansible_module_path>/plugins/terminal/aruba.py
        <ansible_module_path>/plugins/cliconf/aruba.py
        <ansible_module_path>/plugins/action/aruba.py

    :return: None
    """

    global SW_PATHS, SRC_PATH, COLORRED, ANS_PATH
    path_list = [CONTROLLER_PATHS, AIRWAVE_PATHS, CLEARPASS_PATHS,
                 ACTIVATE_PATHS, INSTANT_PATHS, CONTROLLER_SSH_PATHS] + [SW_PATHS]

    base_yml = ANS_PATH+'config/base.yml'

    for type in path_list:
        # Copy each directory and file to ansible module location
        for source, path in type.items():
            # If directories or files exist already, do nothing
            if exists(ANS_PATH+path):
                if isdir(ANS_PATH+path):
                    rmtree(ANS_PATH + path)
                else:
                    remove(ANS_PATH + path)
                print('{} removed...'.format(ANS_PATH + path))

            else:
                print(COLORRED.format('{} does not exist at '
                                      '{}...\n'.format(path, ANS_PATH + path)))

    # Modifies base.yml to include arubaoss modules
    # If base.yml doesn't exist, invalid ansible version is installed
    if exists(base_yml):
        with open(base_yml, 'r') as f:
            base_contents = f.read()

        re_modules = (r"NETWORK_GROUP_MODULES:\s*"
                      r"name:.*\s*"
                      r"default:\s(?P<modules>\[.*\])")

        re_result = search(re_modules, base_contents)

        if re_result:
            if len(re_result.groups('modules')) == 1:
                old_string = re_result.groups('modules')[0]
                if ', arubaoss]' in old_string:
                    new_string = old_string.replace(', arubaoss]', ']')
                    new_base_contents = base_contents.replace(old_string,
                                                              new_string)
                    with open(base_yml, 'w') as f:
                        f.write(new_base_contents)
                    print('{} modification successful...\n'.format(base_yml))
                else:
                    print(COLORRED.format('{}: arubaoss does not '
                                          'exist...\n'.format(base_yml)))
            else:
                exit(COLORRED.format('Multiple instances of '
                                     'NETWORK_GROUP_MODULES found...\n'
                                     'Modification of {} failed...'
                                     .format(base_yml)))
    else:
        exit(COLORRED.format('No base.yml found...Please ensure you have '
                             'Ansible 2.5 or later...\n'
                             'Modification of {} failed...'.format(base_yml)))


if __name__ == "__main__":

    args = define_arguments()

    try:

        ANS_PATH = find_module_path()

        if args.remove:
            remove_modules()
        elif args.reinstall:
            remove_modules()
            install_sw_modules()
            install_wlan_modules()
        elif args.switch:
            install_sw_modules()
        elif args.controller:
            install_wlan_modules(install_package=CONTROLLER_PATHS)
            install_wlan_modules(install_package=CONTROLLER_SSH_PATHS)
        elif args.airwave:
            install_wlan_modules(install_package=AIRWAVE_PATHS)
        elif args.clearpass:
            install_wlan_modules(install_package=CLEARPASS_PATHS)
        elif args.activate:
            install_wlan_modules(install_package=ACTIVATE_PATHS)
        elif args.instant:
            install_wlan_modules(install_package=INSTANT_PATHS)
        else:
            install_sw_modules()
            install_wlan_modules()

    except (OSError, IOError) as e:
        if (e[0] == errno.EACCES):
            print(e)
            if args.remove:
                exit(COLORRED.format("You need root permissions to execute "
                                     "this script against "
                                     "these files/directories.\n\n"
                                     "re-run the installer using\n"
                                     "sudo python"
                                     "aruba_module_installer.py -r"))
            else:
                exit(COLORRED.format("You need root permissions to execute "
                                     "this script against "
                                     "these files/directories.\n\n"
                                     "re-run the installer using\n"
                                     "sudo python "
                                     "aruba_module_installer.py"))
        else:
            raise e
