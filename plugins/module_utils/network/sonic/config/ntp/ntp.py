#
# -*- coding: utf-8 -*-
# Copyright 2022 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The sonic_ntp class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base import (
    ConfigBase,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    to_list,
)
from ansible_collections.dellemc.enterprise_sonic.plugins.module_utils.network.sonic.facts.facts import Facts
from ansible_collections.dellemc.enterprise_sonic.plugins.module_utils.network.sonic.sonic import (
    to_request,
    edit_config
)
from ansible_collections.dellemc.enterprise_sonic.plugins.module_utils.network.sonic.utils.utils import (
    get_diff,
    update_states,
    normalize_interface_name,
    normalize_interface_name_list
)
from ansible.module_utils.connection import ConnectionError

PATCH = 'PATCH'
DELETE = 'DELETE'

TEST_KEYS_ADD = [
    {
        "vrf": "", "enable_ntp_auth": "",
        "source_interfaces": "", "trusted_keys": "",
        "servers": {"address": "", "key_id": "", "maxpoll": "", "minpoll": ""},
        "ntp_keys": {"key_id": "", "key_type": "", "key_value": "", "encrypted": ""}
    }
]

TEST_KEYS_DEL = [
    {
        "vrf": "", "enable_ntp_auth": "", "source_interfaces": "", "trusted_keys": "",
        "servers": {"address": ""}, "ntp_keys": {"key_id": ""}
    }
]


class Ntp(ConfigBase):
    """
    The sonic_ntp class
    """

    gather_subset = [
        '!all',
        '!min',
    ]

    gather_network_resources = [
        'ntp',
    ]

    def __init__(self, module):
        super(Ntp, self).__init__(module)

    def get_ntp_facts(self):
        """ Get the 'facts' (the current configuration)

        :rtype: A dictionary
        :returns: The current configuration as a dictionary
        """
        facts, _warnings = Facts(self._module).get_facts(self.gather_subset, self.gather_network_resources)
        ntp_facts = facts['ansible_network_resources'].get('ntp')

        if not ntp_facts:
            return []
        return ntp_facts

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        result = {'changed': False}
        warnings = list()
        commands = list()
        requests = list()

        existing_ntp_facts = self.get_ntp_facts()

        commands, requests = self.set_config(existing_ntp_facts)

        if commands and len(requests) > 0:
            if not self._module.check_mode:
                try:
                    edit_config(self._module, to_request(self._module, requests))
                except ConnectionError as exc:
                    self._module.fail_json(msg=str(exc), code=exc.code)
            result['changed'] = True
        result['commands'] = commands

        changed_ntp_facts = self.get_ntp_facts()

        result['before'] = existing_ntp_facts
        if result['changed']:
            result['after'] = changed_ntp_facts

        result['warnings'] = warnings
        return result

    def set_config(self, existing_ntp_facts):
        """ Collect the configuration from the args passed to the module,
            collect the current configuration (as a dict from facts)

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        want = self._module.params['config']
        if want is None:
            want = []

        have = existing_ntp_facts

        resp = self.set_state(want, have)

        return to_list(resp)

    def set_state(self, want, have):
        """ Select the appropriate function based on the state provided

        :param want: the desired configuration as a dictionary
        :param have: the current configuration as a dictionary
        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        state = self._module.params['state']

        self.preprocess_want(want, state)

        if state == 'deleted':
            commands, requests = self._state_deleted(want, have)
        elif state == 'merged':
            commands, requests = self._state_merged(want, have)

        return commands, requests

    def _state_merged(self, want, have):
        """ The command generator when state is merged

        :param want: the additive configuration as a dictionary
        :param have: the current configuration as a dictionary
        :returns: the commands necessary to merge the provided into
                  the current configuration
        """
        diff = get_diff(want, have, TEST_KEYS_ADD)

        commands = diff
        requests = []
        if commands:
            requests = self.get_merge_requests(commands, have)

        if len(requests) > 0:
            commands = update_states(commands, "merged")
        else:
            commands = []

        return commands, requests

    def _state_deleted(self, want, have):
        """ The command generator when state is deleted

        :param want: the objects from which the configuration should be removed
        :param have: the current configuration as a dictionary
        :returns: the commands necessary to remove the current configuration
                  of the provided objects
        """
        diff = get_diff(want, have, TEST_KEYS_DEL)

        want_none = {'enable_ntp_auth': None, 'ntp_keys': None,
                     'servers': None, 'source_interfaces': [],
                     'trusted_keys': None, 'vrf': None}
        want_any = get_diff(want, want_none, TEST_KEYS_DEL)
        # if want_any is none, then delete all NTP configurations

        if not want_any:
            commands = have
        else:
            if not diff:
                commands = want_any
            else:
                commands = get_diff(want_any, diff, TEST_KEYS_DEL)

        commands = self.preprocess_delete_commands(commands, have)

        requests = []
        if commands:
            requests = self.get_delete_requests(commands)

        if len(requests) > 0:
            commands = update_states(commands, "deleted")
        else:
            commands = []

        return commands, requests

    def preprocess_want(self, want, state):

        if 'source_interfaces' in want:
            want['source_interfaces'] = normalize_interface_name_list(want['source_interfaces'], self._module)

        if state == 'deleted':
            enable_auth_want = want.get('enable_ntp_auth', None)
            if enable_auth_want is not None:
                want['enable_ntp_auth'] = True

            if 'servers' in want and want['servers'] is not None:
                for server in want['servers']:
                    server.pop('key_id', None)
                    server.pop('minpoll', None)
                    server.pop('maxpoll', None)
            if 'ntp_keys' in want and want['ntp_keys'] is not None:
                for ntp_key in want['ntp_keys']:
                    ntp_key.pop('encrypted', None)
                    ntp_key.pop('key_type', None)
                    ntp_key.pop('key_value', None)

        elif state == 'merged':
            if 'servers' in want and want['servers'] is not None:
                for server in want['servers']:
                    if 'key_id' in server and not server['key_id']:
                        server.pop('key_id')
                    if 'minpoll' in server and not server['minpoll']:
                        server.pop('minpoll')
                    if 'maxpoll' in server and not server['maxpoll']:
                        server.pop('maxpoll')

    def get_merge_requests(self, configs, have):

        requests = []

        enable_auth_config = configs.get('enable_ntp_auth', None)
        if enable_auth_config is not None:
            enable_auth_request = self.get_create_enable_ntp_auth_requests(enable_auth_config, have)
            if enable_auth_request:
                requests.extend(enable_auth_request)

        src_intf_config = configs.get('source_interfaces', None)
        if src_intf_config:
            src_intf_request = self.get_create_source_interface_requests(src_intf_config, have)
            if src_intf_request:
                requests.extend(src_intf_request)

        keys_config = configs.get('ntp_keys', None)
        if keys_config:
            keys_request = self.get_create_keys_requests(keys_config, have)
            if keys_request:
                requests.extend(keys_request)

        servers_config = configs.get('servers', None)
        if servers_config:
            servers_request = self.get_create_servers_requests(servers_config, have)
            if servers_request:
                requests.extend(servers_request)

        trusted_key_config = configs.get('trusted_keys', None)
        if trusted_key_config:
            trusted_key_request = self.get_create_trusted_key_requests(trusted_key_config, have)
            if trusted_key_request:
                requests.extend(trusted_key_request)

        vrf_config = configs.get('vrf', None)
        if vrf_config:
            vrf_request = self.get_create_vrf_requests(vrf_config, have)
            if vrf_request:
                requests.extend(vrf_request)

        return requests

    def preprocess_delete_commands(self, commands, have):

        new_commands = {}

        enable_auth_command = commands.get('enable_ntp_auth', None)
        enable_auth_have = have.get('enable_ntp_auth', None)
        if enable_auth_command is not None and enable_auth_have is not None and \
           (enable_auth_command or enable_auth_have):
            new_commands['enable_ntp_auth'] = True

        keys_command = commands.get('ntp_keys', None)
        if keys_command:
            new_commands['ntp_keys'] = commands['ntp_keys']

        servers_command = commands.get('servers', None)
        if servers_command:
            new_commands['servers'] = commands['servers']

        src_intf_command = commands.get('source_interfaces', None)
        if src_intf_command:
            new_commands['source_interfaces'] = commands['source_interfaces']

        trusted_key_command = commands.get('trusted_keys', None)
        if trusted_key_command:
            new_commands['trusted_keys'] = commands['trusted_keys']

        vrf_command = commands.get('vrf', None)
        if vrf_command:
            new_commands['vrf'] = commands['vrf']

        return new_commands

    def get_delete_requests(self, configs):

        requests = []

        src_intf_config = configs.get('source_interfaces', None)
        if src_intf_config:
            src_intf_request = self.get_delete_source_interface_requests(src_intf_config)
            if src_intf_request:
                requests.extend(src_intf_request)

        servers_config = configs.get('servers', None)
        if servers_config:
            servers_request = self.get_delete_servers_requests(servers_config)
            if servers_request:
                requests.extend(servers_request)

        trusted_key_config = configs.get('trusted_keys', None)
        if trusted_key_config:
            trusted_key_request = self.get_delete_trusted_key_requests(trusted_key_config)
            if trusted_key_request:
                requests.extend(trusted_key_request)

        keys_config = configs.get('ntp_keys', None)
        if keys_config:
            keys_request = self.get_delete_keys_requests(keys_config)
            if keys_request:
                requests.extend(keys_request)

        enable_auth_config = configs.get('enable_ntp_auth', None)
        if enable_auth_config is not None:
            enable_auth_request = self.get_delete_enable_ntp_auth_requests(enable_auth_config)
            if enable_auth_request:
                requests.extend(enable_auth_request)

        vrf_config = configs.get('vrf', None)
        if vrf_config:
            vrf_request = self.get_delete_vrf_requests(vrf_config)
            if vrf_request:
                requests.extend(vrf_request)

        return requests

    def get_create_source_interface_requests(self, configs, have):

        requests = []

        # Create URL and payload
        method = PATCH
        url = 'data/openconfig-system:system/ntp/config/source-interface'
        payload = {"openconfig-system:source-interface": configs}
        request = {"path": url, "method": method, "data": payload}
        requests.append(request)

        return requests

    def get_create_servers_requests(self, configs, have):

        requests = []

        # Create URL and payload
        method = PATCH
        url = 'data/openconfig-system:system/ntp/servers'
        server_configs = []
        for config in configs:
            if 'key_id' in config:
                config['key-id'] = config['key_id']
                config.pop('key_id')
            server_addr = config['address']
            server_config = {"address": server_addr, "config": config}
            server_configs.append(server_config)

        payload = {"openconfig-system:servers": {"server": server_configs}}
        request = {"path": url, "method": method, "data": payload}
        requests.append(request)

        return requests

    def get_create_vrf_requests(self, configs, have):

        requests = []

        # Create URL and payload
        method = PATCH
        url = 'data/openconfig-system:system/ntp/config/network-instance'
        payload = {"openconfig-system:network-instance": configs}
        request = {"path": url, "method": method, "data": payload}
        requests.append(request)

        return requests

    def get_create_enable_ntp_auth_requests(self, configs, have):

        requests = []

        # Create URL and payload
        method = PATCH
        url = 'data/openconfig-system:system/ntp/config/enable-ntp-auth'
        payload = {"openconfig-system:enable-ntp-auth": configs}
        request = {"path": url, "method": method, "data": payload}
        requests.append(request)

        return requests

    def get_create_trusted_key_requests(self, configs, have):

        requests = []

        # Create URL and payload
        method = PATCH
        url = 'data/openconfig-system:system/ntp/config/trusted-key'
        payload = {"openconfig-system:trusted-key": configs}
        request = {"path": url, "method": method, "data": payload}
        requests.append(request)

        return requests

    def get_create_keys_requests(self, configs, have):

        requests = []

        # Create URL and payload
        method = PATCH
        url = 'data/openconfig-system:system/ntp/ntp-keys'
        key_configs = []
        for config in configs:
            key_id = config['key_id']
            if 'key_id' in config:
                config['key-id'] = config['key_id']
                config.pop('key_id')
            if 'key_type' in config:
                config['key-type'] = config['key_type']
                config.pop('key_type')
            if 'key_value' in config:
                config['key-value'] = config['key_value']
                config.pop('key_value')

            key_config = {"key-id": key_id, "config": config}
            key_configs.append(key_config)

        payload = {"openconfig-system:ntp-keys": {"ntp-key": key_configs}}
        request = {"path": url, "method": method, "data": payload}
        requests.append(request)

        return requests

    def get_delete_source_interface_requests(self, configs):

        requests = []

        # Create URL and payload
        method = DELETE
        for config in configs:
            url = 'data/openconfig-system:system/ntp/config/source-interface={0}'.format(config)
            request = {"path": url, "method": method}
            requests.append(request)

        return requests

    def get_delete_servers_requests(self, configs):

        requests = []

        # Create URL and payload
        method = DELETE
        for config in configs:
            server_addr = config['address']
            url = 'data/openconfig-system:system/ntp/servers/server={0}'.format(server_addr)
            request = {"path": url, "method": method}
            requests.append(request)

        return requests

    def get_delete_vrf_requests(self, configs):

        requests = []

        # Create URL and payload
        method = DELETE
        url = 'data/openconfig-system:system/ntp/config/network-instance'
        request = {"path": url, "method": method}
        requests.append(request)

        return requests

    def get_delete_enable_ntp_auth_requests(self, configs):

        requests = []

        # Create URL and payload
        method = DELETE
        url = 'data/openconfig-system:system/ntp/config/enable-ntp-auth'
        request = {"path": url, "method": method}
        requests.append(request)

        return requests

    def get_delete_trusted_key_requests(self, configs):

        requests = []

        # Create URL and payload
        method = DELETE
        for config in configs:
            url = 'data/openconfig-system:system/ntp/config/trusted-key={0}'.format(config)
            request = {"path": url, "method": method}
            requests.append(request)

        return requests

    def get_delete_keys_requests(self, configs):

        requests = []

        # Create URL and payload
        method = DELETE
        key_configs = []
        for config in configs:
            key_id = config['key_id']
            url = 'data/openconfig-system:system/ntp/ntp-keys/ntp-key={0}'.format(key_id)
            request = {"path": url, "method": method}
            requests.append(request)

        return requests