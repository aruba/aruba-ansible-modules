# module: arubaoss_command

description: This module allows execution of CLI commands on AOS-Switch devices via SSH connection.

##### LIMITATIONS
* `arubaoss_command` will not handle commands that repeat forever such as `repeat` - Ansible will freeze  
* `arubaoss_command` is unable to match on custom prompts such as confirming a new password or banner message of the day  

##### ARGUMENTS
```yaml
  commands:
    description: List of commands to be executed in sequence on the switch. Every command
      will attempt to be executed regardless of the success or failure of the previous 
      command in the list. To execute commands in the 'configure' context, you must include 
      the 'configure terminal' command or one of its variations before the configuration commands. 
      'Show' commands are valid and their output will be printed to the screen, returned by the 
      module, and optionally saved to a file. The default module timeout is 30 seconds. To change the 
      command timeout, set the variable 'ansible_command_timeout' to the desired time in seconds.
    required: True
    type: list
  wait_for:
    description: A list of conditions to wait to be satisfied before continuing execution.
      Each condition must include a test of the 'result' variable, which contains the output 
      results of each already-executed command in the 'commands' list. 'result' is a list
      such that result[0] contains the output from commands[0], results[1] contains the output 
      from commands[1], and so on.  
    required: False
    type: list
    
  match:
    description: Specifies whether all conditions in 'wait_for' must be satisfied or if just 
      any one condition can be satisfied. To be used with 'wait_for'.
    default: 'all'
    choice: ['any', 'all']
    required: False
    type: str
        
  retries:
    description: Maximum number of retries to check for the expected prompt.
    default: 10
    required: False
    type: int
  interval:
    description: Interval between retries, in seconds.
    default: 1
    required: False
    type: int
  output_file:
    description: Full path of the local system file to which commands' results will be output.
    The directory must exist, but if the file doesn't exist, it will be created.
    required: False
    type: str
```

##### EXAMPLES
```yaml
- name: Execute show commands and configure commands, and output results to file
  arubaoss_command:
    commands: ['show run',
      'show interface 24',
      'config',
      'vlan 2',
        'ip address 10.10.10.10/24',
      'end']
    output_file: /users/Home/configure.cfg
- name: Show running-config and show version, and pass only if all (both) results match
  arubaoss_command:
    commands:
      - 'show run'
      - 'show version'
    wait_for:
      - result[0] contains "vlan 2"
      - result[1] contains "WC.16.09.0010G"
    match: all
    retries: 5
    interval: 5
- name: Execute show running-config and show version commands and output results to file
  arubaoss_command:
    commands: ['show run', 'show version']
    output_file: /users/Home/config_list.cfg
- name: Run ping command with increased command timeout
  vars:
    - ansible_command_timeout: 60
  arubaoss_command:    
    commands:
      - ping 10.100.0.12 repetitions 100
    output_file: /users/Home/ping.cfg
```