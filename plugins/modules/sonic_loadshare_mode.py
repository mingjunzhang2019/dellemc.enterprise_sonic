#!/usr/bin/python
# -*- coding: utf-8 -*-
# © Copyright 2024 Dell Inc. or its subsidiaries. All Rights Reserved
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
The module file for sonic_loadshare_mode
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
---
module: sonic_loadshare_mode
version_added: 3.0.0
author: "M. Zhang (@mingjunzhang2019)"
notes:
- Tested against Enterprise SONiC Distribution by Dell Technologies.
- Supports C(check_mode).
short_description: IP ECMP load share mode configuration handling for SONiC.
description:
  - This module provides configuration management for IP ECMP load share mode on
  - devices running SONiC.
options:
  config:
    description:
      - Specifies IP ECMP load share mode configuration.
    type: dict
    suboptions:
      hash_algorithm:
        description:
          - Load share hash algorithm.
        type: str
        choices:
          - CRC
          - XOR
          - CRC_32LO
          - CRC_32HI
          - CRC_CCITT
          - CRC_XOR
          - JENKINS_HASH_LO
          - JENKINS_HASH_HI
      hash_ingress_port:
        description:
          - Load share hash ingress port.
        type: bool
      hash_offset:
        description:
          - Load share hash offset.
        type: dict
        suboptions:
          offset:
            description:
              - IP ECMP hash offset value.
              - The range of values is from 0 to 15.
            type: int
          flow_based:
            description:
              - Enable flow-based IP ECMP hashing.
            type: bool
      hash_roce_qpn:
        description:
          - Load share ROCE Queue-Pair Number.
        type: bool
      hash_seed:
        description:
          - IP ECMP hash seed value.
          - The range of values is from 0 to 16777215.
        type: int
      ipv4:
        description:
          - IPv4 ECMP Load share hash parameters.
        type: dict
        suboptions:
          ipv4_dst_ip:
            description:
              - IPv4 destination IP address.
            type: bool
          ipv4_src_ip:
            description:
              - IPv4 source IP address.
            type: bool
          ipv4_ip_proto:
            description:
              - IPv4 protocol.
            type: bool
          ipv4_l4_dst_port:
            description:
              - IPv4 L4 destination port.
            type: bool
          ipv4_l4_src_port:
            description:
              - IPv4 L4 source port.
            type: bool
          ipv4_symmetric:
            description:
              - IPv4 symmetric hash mode.
            type: bool
      ipv6:
        description:
          - IPv6 ECMP Load share hash parameters.
        type: dict
        suboptions:
          ipv6_dst_ip:
            description:
              - IPv6 destination IP address.
            type: bool
          ipv6_src_ip:
            description:
              - IPv6 source IP address.
            type: bool
          ipv6_next_hdr:
            description:
              - IPv6 protocol.
            type: bool
          ipv6_l4_dst_port:
            description:
              - IPv6 L4 destination port.
            type: bool
          ipv6_l4_src_port:
            description:
              - IPv6 L4 source port.
            type: bool
          ipv6_symmetric:
            description:
              - IPv6 symmetric hash mode.
            type: bool
  state:
    description:
      - Specifies the operation to be performed on the load share mode configured on the device.
      - In case of merged, the input configuration will be merged with the existing load share mode on the device.
      - In case of deleted, the existing load share mode configuration will be removed from the device.
      - In case of overridden, all existing load share mode will be deleted and
      - the specified input configuration will be add.
      - In case of replaced, the existing load share mode on the device will be replaced
      - by the specified input configuration.
    type: str
    choices:
      - merged
      - deleted
      - replaced
      - overridden
    default: merged
"""
EXAMPLES = """
#
# Using deleted
#
# Before state:
# -------------
#
#sonic# show running-configuration | grep load-share
#ip load-share hash seed 8888
#ip load-share hash ipv4 ipv4-dst-ip
#ip load-share hash ipv4 ipv4-src-ip
#ip load-share hash ipv4 ipv4-ip-proto
#ip load-share hash ipv4 ipv4-l4-src-port
#ip load-share hash ipv4 ipv4-l4-dst-port
#ip load-share hash algorithm CRC
#ip load-share hash ingress-port
#
- name: Merge some configuration
  sonic_loadshare_mode:
    config:
      hash_algorithm: CRC
      hash_offset:
        offset: 12
        flow_based: True
      hash_roce_qpn: True
      hash_seed: 8888
      ipv4:
        ipv4_l4_dst_port: True
        ipv4_l4_src_port: True
    state: deleted
#
# After state:
# ------------
#
#sonic# show running-configuration | grep load-share
#ip load-share hash ipv4 ipv4-dst-ip
#ip load-share hash ipv4 ipv4-src-ip
#ip load-share hash ipv4 ipv4-ip-proto
#ip load-share hash ingress-port
#
# Using merged
#
# Before state:
# -------------
#
#sonic# show running-configuration | grep load-share
#ip load-share hash seed 8888
#ip load-share hash ipv4 ipv4-dst-ip
#ip load-share hash ipv4 ipv4-src-ip
#ip load-share hash algorithm CRC
#
- name: Merge some configuration
  sonic_loadshare_mode:
    config:
      hash_algorithm: CRC_32LO
      hash_ingress_port: True
      hash_offset:
        offset: 12
        flow_based: True
      hash_roce_qpn: True
      hash_seed: 9999
      ipv4:
        ipv4_src_ip: True
        ipv4_ip_proto: True
        ipv4_l4_dst_port: True
        ipv4_l4_src_port: True
    state: merged
#
# After state:
# ------------
#
#sonic# show running-configuration | grep load-share
#ip load-share hash seed 9999
#ip load-share hash ipv4 ipv4-dst-ip
#ip load-share hash ipv4 ipv4-src-ip
#ip load-share hash ipv4 ipv4-ip-proto
#ip load-share hash ipv4 ipv4-l4-src-port
#ip load-share hash ipv4 ipv4-l4-dst-port
#ip load-share hash algorithm CRC_32LO
#ip load-share hash ingress-port
#
# Using replaced
#
# Before state:
# -------------
#
#sonic# show running-configuration | grep load-share
#ip load-share hash offset flow-based
#ip load-share hash seed 8888
#ip load-share hash ipv4 ipv4-dst-ip
#ip load-share hash ipv4 ipv4-src-ip
#ip load-share hash algorithm CRC
#ip load-share hash ingress-port
#
- name: Merge some configuration
  sonic_loadshare_mode:
    config:
      hash_algorithm: CRC
      hash_ingress_port: True
      hash_offset:
        flow_based: True
      hash_seed: 8888
      ipv4:
        ipv4_src_ip: True
        ipv4_ip_proto: True
        ipv4_l4_dst_port: True
        ipv4_l4_src_port: True
    state: replaced
#
# After state:
# ------------
#
#sonic# show running-configuration | grep load-share
#ip load-share hash offset flow-based
#ip load-share hash seed 8888
#ip load-share hash ipv4 ipv4-src-ip
#ip load-share hash ipv4 ipv4-ip-proto
#ip load-share hash ipv4 ipv4-l4-src-port
#ip load-share hash ipv4 ipv4-l4-dst-port
#ip load-share hash algorithm CRC
#ip load-share hash ingress-port
#
# Using overridden
#
# Before state:
# -------------
#
#sonic# show running-configuration | grep load-share
#ip load-share hash seed 8888
#ip load-share hash ipv4 ipv4-dst-ip
#ip load-share hash ipv4 ipv4-src-ip
#ip load-share hash algorithm CRC
#
- name: Merge some configuration
  sonic_loadshare_mode:
    config:
      hash_algorithm: CRC_32LO
      hash_ingress_port: True
      hash_offset:
        flow_based: True
      hash_seed: 9999
      ipv4:
        ipv4_src_ip: True
        ipv4_ip_proto: True
        ipv4_l4_dst_port: True
        ipv4_l4_src_port: True
    state: overridden
#
# After state:
# ------------
#
#sonic# show running-configuration | grep load-share
#ip load-share hash offset flow-based
#ip load-share hash seed 9999
#ip load-share hash ipv4 ipv4-src-ip
#ip load-share hash ipv4 ipv4-ip-proto
#ip load-share hash ipv4 ipv4-l4-src-port
#ip load-share hash ipv4 ipv4-l4-dst-port
#ip load-share hash algorithm CRC_32LO
#ip load-share hash ingress-port
#
"""
RETURN = """
before:
  description: The configuration prior to the module invocation.
  returned: always
  type: list
  sample: >
    The configuration returned will always be in the same format
    as the parameters above.
after:
  description: The resulting configuration module invocation.
  returned: when changed
  type: list
  sample: >
    The configuration returned will always be in the same format
    as the parameters above.
after(generated):
  description: The generated configuration module invocation.
  returned: when C(check_mode)
  type: list
  sample: >
    The configuration returned will always be in the same format
    as the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample: ['command 1', 'command 2', 'command 3']
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.enterprise_sonic.plugins.module_utils.network.sonic.argspec.loadshare_mode.loadshare_mode import Loadshare_modeArgs
from ansible_collections.dellemc.enterprise_sonic.plugins.module_utils.network.sonic.config.loadshare_mode.loadshare_mode import Loadshare_mode


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(argument_spec=Loadshare_modeArgs.argument_spec,
                           supports_check_mode=True)

    result = Loadshare_mode(module).execute_module()
    module.exit_json(**result)


if __name__ == '__main__':
    main()