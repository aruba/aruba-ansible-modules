# IP Route
Module: ****arubaoss_ip_route****  
Description: "This implements static routing rest api and global routing configuration"

##### ARGUMENTS
    ip_route_mode:
        description:
            - Mode for route type
        choices: 'IRM_GATEWAY','IRM_REJECT','IRM_VLAN','IRM_BLACK_HOLE','IRM_TUNNEL_ARUBA_VPN'
        required: true
    destination_vlan:
        description:
            - vlan id for IRM_VLAN mode.
        required: false
    metric:
        description:
            - ip route metric
        default= 1
        required: false
    distance:
        description:
            - ip route distance
        defualt: 1
        required: false
    name:
        description:
            - name for ip route being configured
        required: false
    tag:
        description:
            - Tag that can be used to filter redistribution of this route via route-maps
        required: false
    logging:
        description:
            - if the packets received on the route need to be logged
        required: false
    ip_version:
        description:
            - Ip address type to be configured
        defualt: IAV_IPV_V4
        required: false
    gateway:
        description:
            - IP address of the gateway to forward traffic when route mode is IRM_GATEWAY
        required: false
    mask:
        description:
            - Subnet for the ip route.
        required: false
    destination:
        description:
            - IP address for the ip routed
        required: false
    bfd_ip_address:
        description:
            - Enable BFD for static routes. Only for Lava and Bolt platforms.
        required: false
    vlan_name:
        description:
            - vlan id/name to which route is being applied
        required: false


##### EXAMPLES
```YAML
    - name: add route vlan
       arubaoss_ip_route:
         ip_route_mode: IRM_VLAN
         ip_version: IAV_IP_V4
         destination: 1.1.1.0
         mask: 255.255.255.0
         destination_vlan: 20
         name: "test"
     - name: add route vlan
       arubaoss_ip_route:
         ip_route_mode: IRM_VLAN
         ip_version: IAV_IP_V4
         destination: 1.1.1.0
         mask: 255.255.255.0
         destination_vlan: 20
         name: "test"
     - name: add route blackhole
       arubaoss_ip_route:
         ip_route_mode: IRM_BLACK_HOLE
         ip_version: IAV_IP_V4
         destination: 2.2.2.0
         mask: 255.255.255.0
     - name: delete route vlan
       arubaoss_ip_route:
         ip_route_mode: IRM_VLAN
         destination_vlan: 20
         destination: 1.1.1.0
         mask: 255.255.255.0
         state: delete
     - name: delete route blackhole
       arubaoss_ip_route:
         ip_route_mode: IRM_BLACK_HOLE
         destination: 2.2.2.0
         mask: 255.255.255.0
         state: delete
     - name: delete route blackhole
       arubaoss_ip_route:
         ip_route_mode: IRM_BLACK_HOLE
         destination: 2.2.2.0
         mask: 255.255.255.0
         state: delete

```