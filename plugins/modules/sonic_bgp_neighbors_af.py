#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the resource
#   module builder playbook.
#
# Do not edit this file manually.
#
# Changes to this file will be over written
#   by the resource module builder.
#
# Changes should be made in the model used to
#   generate this file or in the resource module
#   builder template.
#
#############################################

"""
The module file for sonic_bgp_neighbors_af
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
---
module: sonic_bgp_neighbors_af
version_added: 1.0.0
notes:
- Tested against Enterprise SONiC Distribution by Dell Technologies
author: "Niraimadaiselvam M (@niraimadaiselvamm)"
short_description: Configures BGP neighbors address-family configuration on devices running Enterprise SONiC.
description:
  - This module provides configuration management of BGP neighbors address-family parameters on devices running Enterprise SONiC.
  - bgp_as, vrf_name and neighbors need be created in advance on the device.
options:
  config:
    description:
      - Specifies the BGP neighbors address-family related configuration.
    type: list
    elements: dict
    suboptions:
      bgp_as:
        description:
          - Specifies the BGP autonomous system (AS) number which is already configured on the device.
        type: str
        required: true
      vrf_name:
        description:
          - Specifies the VRF name which is already configured on the device.
        type: str
        default: 'default'
      neighbors:
        description:
          - Specifies BGP neighbor related configurations in address-family configuration mode.
        type: list
        elements: dict
        suboptions:
          neighbor:
            description:
              - Neighbor router address which is already configured on the device.
            type: str
            required: True
          address_family:
            description:
              - Specifies BGP address-family related configurations.
              - afi and safi are required together.
            type: list
            elements: dict
            suboptions:
              afi:
                description:
                  - Type of address-family to configure.
                type: str
                choices:
                  - ipv4
                  - ipv6
                  - l2vpn
                required: True
              safi:
                description:
                  - Specifies the type of cast for the address-family.
                type: str
                choices:
                  - unicast
                  - evpn
                default: unicast
              activate:
                description:
                  - Enables the address-family for this neighbor.
                type: bool
              allowas_in:
                description:
                  - Specifies the allowas in values.
                type: dict
                suboptions:
                  value:
                    description:
                      - Specifies the value of the allowas in.
                    type: int
                  origin:
                    description:
                      - Specifies the origin value.
                    type: bool
              route_map:
                description:
                  - Specifies the route-map.
                type: list
                elements: dict
                suboptions:
                  name:
                    description:
                      - Specifies the name of the route-map.
                    type: str
                  direction:
                    description:
                      - Specifies the direction of the route-map.
                    type: str
              route_reflector_client:
                description:
                  - Specifies a neighbor as a route-reflector client.
                type: bool
              route_server_client:
                description:
                  - Specifies a neighbor as a route-server client.
                type: bool
  state:
    description:
      - Specifies the operation to be performed on the BGP process that is configured on the device.
      - In case of merged, the input configuration is merged with the existing BGP configuration on the device.
      - In case of deleted, the existing BGP configuration is removed from the device.
    default: merged
    type: str
    choices: ['merged', 'deleted']
"""
EXAMPLES = """
# Using deleted
#
# Before state:
# -------------
#
#!
#router bgp 4
# !
# neighbor interface Eth1/3
#  !
#  address-family ipv4 unicast
#   activate
#   allowas-in 4
#   route-map aa in
#   route-map aa out
#   route-reflector-client
#   route-server-client
#   send-community both
#!
#
- name: Deletes neighbors address-family with specific values.
  dellemc.enterprise_sonic.sonic_bgp_neighbors_af:
     config:
       - bgp_as: 4
         neighbors:
           - neighbor: Eth1/3
             address_family:
               - afi: ipv4
                 safi: unicast
                 allowas_in:
                   value: 4
                 route_map:
                   - name: aa
                     direction: in
                   - name: aa
                     direction: out
                 route_reflector_client: true
                 route_server_client: true
     state: deleted

# After state:
# ------------
#!
#router bgp 4
# !
# neighbor interface Eth1/3
#  !
#  address-family ipv4 unicast
#   send-community both
#!


# Using deleted
#
# Before state:
# -------------
#
#!
#router bgp 4
# !
# neighbor interface Eth1/3
#  !
#  address-family ipv4 unicast
#   activate
#   allowas-in 4
#   route-map aa in
#   route-map aa out
#   route-reflector-client
#   route-server-client
#   send-community both
#!
# neighbor interface Eth1/5
#  !
#  address-family ipv4 unicast
#   activate
#   allowas-in origin
#   send-community both
#!
#
- name: Deletes neighbors address-family with specific values.
  dellemc.enterprise_sonic.sonic_bgp_neighbors_af:
     config:
     state: deleted

# After state:
# ------------
#!
#router bgp 4
#!


# Using deleted
#
# Before state:
# -------------
#
#!
#router bgp 4
# !
# neighbor interface Eth1/3
#!
#
- name: Merges neighbors address-family with specific values.
  dellemc.enterprise_sonic.sonic_bgp_neighbors_af:
     config:
       - bgp_as: 4
         neighbors:
           - neighbor: Eth1/3
             address_family:
               - afi: ipv4
                 safi: unicast
                 allowas_in:
                   value: 4
                 route_map:
                   - name: aa
                     direction: in
                   - name: aa
                     direction: out
                 route_reflector_client: true
                 route_server_client: true
     state: merged

# After state:
# ------------
#!
#router bgp 4
# !
# neighbor interface Eth1/3
#  !
#  address-family ipv4 unicast
#   activate
#   allowas-in 4
#   route-map aa in
#   route-map aa out
#   route-reflector-client
#   route-server-client
#   send-community both
#!


"""
RETURN = """
before:
  description: The configuration prior to the model invocation.
  returned: always
  type: list
  sample: >
    The configuration returned is always in the same format
    of the parameters above.
after:
  description: The resulting configuration model invocation.
  returned: when changed
  type: list
  sample: >
    The configuration returned is always in the same format
    of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample: ['command 1', 'command 2', 'command 3']
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.enterprise_sonic.plugins.module_utils.network.sonic.argspec.bgp_neighbors_af.bgp_neighbors_af import Bgp_neighbors_afArgs
from ansible_collections.dellemc.enterprise_sonic.plugins.module_utils.network.sonic.config.bgp_neighbors_af.bgp_neighbors_af import Bgp_neighbors_af


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(argument_spec=Bgp_neighbors_afArgs.argument_spec,
                           supports_check_mode=True)

    result = Bgp_neighbors_af(module).execute_module()
    module.exit_json(**result)


if __name__ == '__main__':
    main()
