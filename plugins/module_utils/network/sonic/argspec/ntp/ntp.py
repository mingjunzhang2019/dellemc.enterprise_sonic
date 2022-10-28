#
# -*- coding: utf-8 -*-
# Copyright 2022 Dell Inc. or its subsidiaries. All Rights Reserved
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
The arg spec for the sonic_ntp module
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class NtpArgs(object):  # pylint: disable=R0903
    """The arg spec for the sonic_ntp module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        'config': {
            'options': {
                'enable_ntp_auth': {'type': 'bool'},
                'ntp_keys': {
                    'elements': 'dict',
                    'options': {
                        'encrypted': {'type': 'bool'},
                        'key_id': {'required': True,
                                   'type': 'int',
                                   'no_log': True},
                        'key_type': {'type': 'str',
                                     'choices': ['NTP_AUTH_SHA1',
                                                 'NTP_AUTH_MD5',
                                                 'NTP_AUTH_SHA2_256']},
                        'key_value': {'type': 'str', 'no_log': True}
                    },
                    'type': 'list',
                    'no_log': True
                },
                'servers': {
                    'elements': 'dict',
                    'options': {
                        'address': {'required': True,
                                    'type': 'str'},
                        'key_id': {'type': 'int', 'no_log': True},
                        'maxpoll': {'type': 'int'},
                        'minpoll': {'type': 'int'},
                        'prefer': {'type': 'bool'}
                    },
                    'required_together': [['minpoll', 'maxpoll']],
                    'type': 'list'
                },
                'source_interfaces': {
                    'elements': 'str',
                    'type': 'list'
                },
                'trusted_keys': {
                    'elements': 'int',
                    'type': 'list',
                    'no_log': True
                },
                'vrf': {'type': 'str'}
            },
            'type': 'dict'
        },
        'state': {
            'choices': ['merged', 'deleted'],
            'default': 'merged',
            'type': 'str'
        }
    }  # pylint: disable=C0301
