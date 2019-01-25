# VLAN
Module: ****arubaoscx_vlan****  
Description: "This module implements VLAN configuration for ArubaOS_CX switch"

##### ARGUMENTS
    vlan_id:
        description: The ID of this VLAN. Non-internal VLANs must have an 'id'
                     betwen 1 and 4094 to be effectively instantiated.
        required: true
    name:
        description: VLAN name
        required: false
    description:
        description: VLAN description
        required: false
    interfaces:
        description: Interfaces attached to VLAN
        required: False
    state:
        description: Create/Update or Delete VLAN
        default: present
        choices: ['present', 'absent']
        required: False

##### EXAMPLES
```YAML
     - name: Adding new VLAN
       arubaoscx_vlan:
         vlan_id: "{{ item.vlan_id }}"
         name: "{{ item.name }}"
         description: "{{ item.description }}"
       with_items:
           - { vlan_id: 2, name: VLAN2, description: 'This is VLAN2' }
           - { vlan_id: 3, name: VLAN3, description: 'This is VLAN3' }
     - name: Attaching interfaces to VLAN
       arubaoscx_vlan:
         vlan_id: "{{ item.vlan_id }}"
         interfaces: "{{ item.interfaces }}"
       with_items:
           - { vlan_id: 2, interfaces: ['1/1/3', '1/1/4'] }
           - { vlan_id: 3, interfaces: ['1/1/5', '1/1/6'] }
     - name: Adding new VLAN with name, description and interfaces
       arubaoscx_vlan:
         vlan_id: "{{ item.vlan_id }}"
         name: "{{ item.name }}"
         description: "{{ item.description }}"
         interfaces: "{{ item.interfaces }}"
       with_items:
           - { vlan_id: 2, name: VLAN2, description: 'This is VLAN2',
               interfaces: ['1/1/3', '1/1/4'] }
           - { vlan_id: 3, name: VLAN3, description: 'This is VLAN3',
               interfaces: ['1/1/5', '1/1/6'] }
     - name: Deleting VLAN
       arubaoscx_vlan:
         vlan_id: "{{ item.vlan_id }}"
         state: "{{ item.state }}"
       with_items:
           - { vlan_id: 2, state: absent }
           - { vlan_id: 3, state: absent }

```