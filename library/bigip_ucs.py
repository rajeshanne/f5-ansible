#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: bigip_ucs
short_description: Manage upload, installation and removal of UCS files
description:
   - Manage upload, installation and removal of UCS files.
version_added: "2.4"
options:
  include_chassis_level_config:
    description:
      - During restore of the UCS file, include chassis level configuration
        that is shared among boot volume sets. For example, cluster default
        configuration.
    type: bool
  ucs:
    description:
      - The path to the UCS file to install. The parameter must be
        provided if the C(state) is either C(installed) or C(activated).
        When C(state) is C(absent), the full path for this parameter will be
        ignored and only the filename will be used to select a UCS for removal.
        Therefore you could specify C(/mickey/mouse/test.ucs) and this module
        would only look for C(test.ucs).
  force:
    description:
      - If C(yes) will upload the file every time and replace the file on the
        device. If C(no), the file will only be uploaded if it does not already
        exist. Generally should be C(yes) only in cases where you have reason
        to believe that the image was corrupted during upload.
    type: bool
    default: no
  no_license:
    description:
      - Performs a full restore of the UCS file and all the files it contains,
        with the exception of the license file. The option must be used to
        restore a UCS on RMA devices (Returned Materials Authorization).
    type: bool
  no_platform_check:
    description:
      - Bypasses the platform check and allows a UCS that was created using a
        different platform to be installed. By default (without this option),
        a UCS created from a different platform is not allowed to be installed.
    type: bool
  passphrase:
    description:
      - Specifies the passphrase that is necessary to load the specified UCS file.
    type: bool
  reset_trust:
    description:
      - When specified, the device and trust domain certs and keys are not
        loaded from the UCS. Instead, a new set is regenerated.
    type: bool
  state:
    description:
      - When C(installed), ensures that the UCS is uploaded and installed,
        on the system. When C(present), ensures that the UCS is uploaded.
        When C(absent), the UCS will be removed from the system. When
        C(installed), the uploading of the UCS is idempotent, however the
        installation of that configuration is not idempotent.
    default: present
    choices:
      - absent
      - installed
      - present
notes:
   - Only the most basic checks are performed by this module. Other checks and
     considerations need to be taken into account. See the following URL.
     https://support.f5.com/kb/en-us/solutions/public/11000/300/sol11318.html
   - This module does not handle devices with the FIPS 140 HSM
   - This module does not handle BIG-IPs systems on the 6400, 6800, 8400, or
     8800 hardware platform.
   - This module does not verify that the new or replaced SSH keys from the
     UCS file are synchronized between the BIG-IP system and the SCCP
   - This module does not support the 'rma' option
   - This module does not support restoring a UCS archive on a BIG-IP 1500,
     3400, 4100, 6400, 6800, or 8400 hardware platform other than the system
     from which the backup was created
   - The UCS restore operation restores the full configuration only if the
     hostname of the target system matches the hostname on which the UCS
     archive was created. If the hostname does not match, only the shared
     configuration is restored. You can ensure hostnames match by using
     the C(bigip_hostname) Ansible module in a task before using this module.
   - This module does not support re-licensing a BIG-IP restored from a UCS
   - This module does not support restoring encrypted archives on replacement
     RMA units.
extends_documentation_fragment: f5
author:
  - Tim Rupp (@caphrim007)
'''

EXAMPLES = r'''
- name: Upload UCS
  bigip_ucs:
    server: lb.mydomain.com
    user: admin
    password: secret
    ucs: /root/bigip.localhost.localdomain.ucs
    state: present
  delegate_to: localhost

- name: Install (upload, install) UCS.
  bigip_ucs:
    server: lb.mydomain.com
    user: admin
    password: secret
    ucs: /root/bigip.localhost.localdomain.ucs
    state: installed
  delegate_to: localhost

- name: Install (upload, install) UCS without installing the license portion
  bigip_ucs:
    server: lb.mydomain.com
    user: admin
    password: secret
    ucs: /root/bigip.localhost.localdomain.ucs
    state: installed
    no_license: yes
  delegate_to: localhost

- name: Install (upload, install) UCS except the license, and bypassing the platform check
  bigip_ucs:
    server: lb.mydomain.com
    user: admin
    password: secret
    ucs: /root/bigip.localhost.localdomain.ucs
    state: installed
    no_license: yes
    no_platform_check: yes
  delegate_to: localhost

- name: Install (upload, install) UCS using a passphrase necessary to load the UCS
  bigip_ucs:
    server: lb.mydomain.com
    user: admin
    password: secret
    ucs: /root/bigip.localhost.localdomain.ucs
    state: installed
    passphrase: MyPassphrase1234
  delegate_to: localhost

- name: Remove uploaded UCS file
  bigip_ucs:
    server: lb.mydomain.com
    user: admin
    password: secret
    ucs: bigip.localhost.localdomain.ucs
    state: absent
  delegate_to: localhost
'''

RETURN = r'''
# only common fields returned
'''

import os
import re
import time

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import iteritems
from distutils.version import LooseVersion

HAS_DEVEL_IMPORTS = False

try:
    # Sideband repository used for dev
    from library.module_utils.network.f5.bigip import HAS_F5SDK
    from library.module_utils.network.f5.bigip import F5Client
    from library.module_utils.network.f5.common import F5ModuleError
    from library.module_utils.network.f5.common import AnsibleF5Parameters
    from library.module_utils.network.f5.common import cleanup_tokens
    from library.module_utils.network.f5.common import fqdn_name
    from library.module_utils.network.f5.common import f5_argument_spec
    try:
        from library.module_utils.network.f5.common import iControlUnexpectedHTTPError
    except ImportError:
        HAS_F5SDK = False
    HAS_DEVEL_IMPORTS = True
except ImportError:
    # Upstream Ansible
    from ansible.module_utils.network.f5.bigip import HAS_F5SDK
    from ansible.module_utils.network.f5.bigip import F5Client
    from ansible.module_utils.network.f5.common import F5ModuleError
    from ansible.module_utils.network.f5.common import AnsibleF5Parameters
    from ansible.module_utils.network.f5.common import cleanup_tokens
    from ansible.module_utils.network.f5.common import fqdn_name
    from ansible.module_utils.network.f5.common import f5_argument_spec
    try:
        from ansible.module_utils.network.f5.common import iControlUnexpectedHTTPError
    except ImportError:
        HAS_F5SDK = False

try:
    from collections import OrderedDict
except ImportError:
    try:
        from ordereddict import OrderedDict
    except ImportError:
        pass


class Parameters(AnsibleF5Parameters):
    api_map = {}
    updatables = []
    returnables = []
    api_attributes = []

    def _check_required_if(self, parameter):
        if self._values[parameter] is not True:
            return self._values[parameter]
        if self.state != 'installed':
            raise F5ModuleError(
                '"{0}" parameters requires "installed" state'.format(parameter)
            )

    @property
    def basename(self):
        return os.path.basename(self.ucs)

    @property
    def options(self):
        return {
            'include-chassis-level-config': self.include_chassis_level_config,
            'no-license': self.no_license,
            'no-platform-check': self.no_platform_check,
            'passphrase': self.passphrase,
            'reset-trust': self.reset_trust
        }

    @property
    def reset_trust(self):
        self._check_required_if('reset_trust')
        return self._values['reset_trust']

    @property
    def passphrase(self):
        self._check_required_if('passphrase')
        return self._values['passphrase']

    @property
    def no_platform_check(self):
        self._check_required_if('no_platform_check')
        return self._values['no_platform_check']

    @property
    def no_license(self):
        self._check_required_if('no_license')
        return self._values['no_license']

    @property
    def include_chassis_level_config(self):
        self._check_required_if('include_chassis_level_config')
        return self._values['include_chassis_level_config']

    @property
    def install_command(self):
        cmd = 'tmsh load sys ucs /var/local/ucs/{0}'.format(self.basename)
        # Append any options that might be specified
        options = OrderedDict(sorted(self.options.items(), key=lambda t: t[0]))
        for k, v in iteritems(options):
            if v is False or v is None:
                continue
            elif k == 'passphrase':
                cmd += ' %s %s' % (k, v)
            else:
                cmd += ' %s' % (k)
        return cmd

    def to_return(self):
        result = {}
        for returnable in self.returnables:
            result[returnable] = getattr(self, returnable)
        result = self._filter_params(result)
        return result

    def api_params(self):
        result = {}
        for api_attribute in self.api_attributes:
            if self.api_map is not None and api_attribute in self.api_map:
                result[api_attribute] = getattr(self, self.api_map[api_attribute])
            else:
                result[api_attribute] = getattr(self, api_attribute)
        result = self._filter_params(result)
        return result


class ModuleManager(object):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.get('client', None)
        self.kwargs = kwargs

    def exec_module(self):
        if self.is_version_v1():
            manager = V1Manager(**self.kwargs)
        else:
            manager = V2Manager(**self.kwargs)

        return manager.exec_module()

    def is_version_v1(self):
        """Checks to see if the TMOS version is less than 12.1.0

        Versions prior to 12.1.0 have a bug which prevents the REST
        API from properly listing any UCS files when you query the
        /mgmt/tm/sys/ucs endpoint. Therefore you need to do everything
        through tmsh over REST.

        :return: Bool
        """
        version = self.client.api.tmos_version
        if LooseVersion(version) < LooseVersion('12.1.0'):
            return True
        else:
            return False


class BaseManager(object):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.client = kwargs.get('client', None)
        self.want = Parameters(params=self.module.params)
        self.changes = Parameters()

    def exec_module(self):
        changed = False
        result = dict()
        state = self.want.state

        try:
            if state in ['present', 'installed']:
                changed = self.present()
            elif state == "absent":
                changed = self.absent()
        except iControlUnexpectedHTTPError as e:
            raise F5ModuleError(str(e))

        changes = self.changes.to_return()
        result.update(**changes)
        result.update(dict(changed=changed))
        return result

    def present(self):
        if self.exists():
            return self.update()
        else:
            return self.create()

    def update(self):
        if self.module.check_mode:
            if self.want.force:
                return True
            return False
        elif self.want.force:
            self.remove()
            return self.create()
        elif self.want.state == 'installed':
            return self.install_on_device()
        else:
            return False

    def create(self):
        if self.module.check_mode:
            return True
        self.create_on_device()
        if not self.exists():
            raise F5ModuleError("Failed to upload the UCS file")
        if self.want.state == 'installed':
            self.install_on_device()
        return True

    def absent(self):
        if self.exists():
            return self.remove()
        return False

    def should_update(self):
        result = self._update_changed_options()
        if result:
            return True
        return False

    def remove(self):
        if self.module.check_mode:
            return True
        self.remove_from_device()
        if self.exists():
            raise F5ModuleError("Failed to delete the UCS file")
        return True

    def wait_for_rest_api_restart(self):
        time.sleep(5)
        for x in range(0, 60):
            try:
                self.client.reconnect()
                break
            except Exception:
                time.sleep(3)

    def wait_for_configuration_reload(self):
        noops = 0
        while noops < 4:
            time.sleep(3)
            try:
                output = self.client.api.tm.util.bash.exec_cmd(
                    'run',
                    utilCmdArgs='-c "tmsh show sys mcp-state"'
                )
            except Exception as ex:
                # This can be caused by restjavad restarting.
                continue

            if not hasattr(output, 'commandResult'):
                continue

            # Need to re-connect here because the REST framework will be restarting
            # and thus be clearing its authorization cache
            result = output.commandResult
            if self._is_config_reloading_failed_on_device(result):
                raise F5ModuleError(
                    "Failed to reload the configuration. This may be due "
                    "to a cross-version incompatibility. {0}".format(result)
                )
            if self._is_config_reloading_success_on_device(result):
                if self._is_config_reloading_running_on_device(result):
                    noops += 1
                    continue
            noops = 0

    def _is_config_reloading_success_on_device(self, output):
        succeed = r'Last Configuration Load Status\s+full-config-load-succeed'
        matches = re.search(succeed, output)
        if matches:
            return True
        return False

    def _is_config_reloading_running_on_device(self, output):
        running = r'Running Phase\s+running'
        matches = re.search(running, output)
        if matches:
            return True
        return False

    def _is_config_reloading_failed_on_device(self, output):
        failed = r'Last Configuration Load Status\s+base-config-load-failed'
        matches = re.search(failed, output)
        if matches:
            return True
        return False


class V1Manager(BaseManager):
    """Manager class for V1 product

    V1 products include versions of BIG-IP < 12.1.0, but >= 12.0.0.

    These versions had a number of API deficiencies. These include, but
    are not limited to,

      * UCS collection endpoint listed no items
      * No API to upload UCS files

    """
    def create_on_device(self):
        remote_path = "/var/local/ucs"
        tpath_name = '/var/config/rest/downloads'

        upload = self.client.api.shared.file_transfer.uploads

        try:
            upload.upload_file(self.want.ucs)
        except IOError as ex:
            raise F5ModuleError(str(ex))

        self.client.api.tm.util.unix_mv.exec_cmd(
            'run',
            utilCmdArgs='{0}/{2} {1}/{2}'.format(
                tpath_name, remote_path, self.want.basename
            )
        )
        return True

    def read_current_from_device(self):
        result = []
        output = self.client.api.tm.util.bash.exec_cmd(
            'run',
            utilCmdArgs='-c "tmsh list sys ucs"'
        )
        if hasattr(output, 'commandResult'):
            lines = output.commandResult.split("\n")
            result = [x.strip() for x in lines]
            result = list(set(result))
        return result

    def exists(self):
        collection = self.read_current_from_device()
        if self.want.basename in collection:
            return True
        return False

    def remove_from_device(self):
        output = self.client.api.tm.util.bash.exec_cmd(
            'run',
            utilCmdArgs='-c "tmsh delete sys ucs {0}"'.format(self.want.basename)
        )
        if hasattr(output, 'commandResult'):
            if '{0} is deleted'.format(self.want.basename) in output.commandResult:
                return True
        return False

    def install_on_device(self):
        try:
            self.client.api.tm.util.bash.exec_cmd(
                'run',
                utilCmdArgs='-c "{0}"'.format(self.want.install_command)
            )
        except Exception as ex:
            # Reloading a UCS configuration will cause restjavad to restart,
            # aborting the connection.
            if 'Connection aborted' in str(ex):
                pass
            elif 'TimeoutException' in str(ex):
                # Timeouts appear to be able to happen in 12.1.2
                pass
            else:
                raise F5ModuleError(str(ex))
        self.wait_for_rest_api_restart()
        self.wait_for_configuration_reload()
        return True


class V2Manager(V1Manager):
    """Manager class for V2 product

    V2 products include versions of BIG-IP >= 12.1.0 but < 13.0.0.

    These versions fixed the collection bug in V1, but had yet to add the
    ability to upload files using a dedicated UCS upload API.

    """

    def read_current_from_device(self):
        result = []
        resource = self.client.api.tm.sys.ucs.load()
        items = resource.attrs.get('items', [])
        for item in items:
            result.append(os.path.basename(item['apiRawValues']['filename']))
        return result

    def exists(self):
        collection = self.read_current_from_device()
        if self.want.basename in collection:
            return True
        return False


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict(
            force=dict(
                type='bool',
                default='no'
            ),
            include_chassis_level_config=dict(
                type='bool'
            ),
            no_license=dict(
                type='bool'
            ),
            no_platform_check=dict(
                type='bool'
            ),
            passphrase=dict(no_log=True),
            reset_trust=dict(type='bool'),
            state=dict(
                default='present',
                choices=['absent', 'installed', 'present']
            ),
            ucs=dict(required=True)
        )
        self.argument_spec = {}
        self.argument_spec.update(f5_argument_spec)
        self.argument_spec.update(argument_spec)


def main():
    spec = ArgumentSpec()

    module = AnsibleModule(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode
    )
    if not HAS_F5SDK:
        module.fail_json(msg="The python f5-sdk module is required")

    try:
        client = F5Client(**module.params)
        mm = ModuleManager(module=module, client=client)
        results = mm.exec_module()
        cleanup_tokens(client)
        module.exit_json(**results)
    except F5ModuleError as ex:
        cleanup_tokens(client)
        module.fail_json(msg=str(ex))


if __name__ == '__main__':
    main()
