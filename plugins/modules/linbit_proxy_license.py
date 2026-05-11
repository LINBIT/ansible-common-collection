#!/usr/bin/python
# SPDX-License-Identifier: MIT

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: linbit_proxy_license
short_description: Fetch and write the DRBD Proxy license for a registered node
version_added: "0.10.0"
description:
  - Fetches the DRBD Proxy license file from the LINBIT customer portal
    for a node already registered via M(linbit.common.linbit_register_node).
  - Reads node identity (nodehash, cluster_id, contract_id, hostname) from
    C(/var/lib/drbd-support/registration.json) written by registration.
  - Writes the decoded license to the configured destination path.
  - Idempotent - skips the API call when the destination license file
    already exists, unless C(force) is true.
options:
  dest:
    description: Destination path for the DRBD Proxy license file.
    type: path
    default: /etc/drbd-proxy.license
  api_url:
    description: LINBIT API base URL.
    type: str
    default: https://api.linbit.com
  force:
    description: Re-fetch the license even when C(dest) already exists.
    type: bool
    default: false
seealso:
  - module: linbit.common.linbit_register_node
author:
  - Ryan Ronnander (@rronnander)
'''

EXAMPLES = r'''
- name: Fetch the DRBD Proxy license after registration
  linbit.common.linbit_proxy_license:

- name: Fetch to a custom path
  linbit.common.linbit_proxy_license:
    dest: /etc/drbd/proxy.license
'''

RETURN = r'''
license_path:
  description: Path the license file was written to.
  type: str
  returned: success
'''

import base64
import json
import os

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import open_url

try:
    from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
except ImportError:
    from urllib.error import HTTPError, URLError


REGISTRATION_FILE = '/var/lib/drbd-support/registration.json'
EXCLUDE_PREFIXES = ('vir', 'vnet', 'bond')


def get_mac_addresses():
    """Gather permanent Ethernet MAC addresses from sysfs."""
    macs = []
    net_dir = '/sys/class/net'

    if not os.path.isdir(net_dir):
        return macs

    for iface in sorted(os.listdir(net_dir)):
        if iface.startswith(EXCLUDE_PREFIXES):
            continue

        iface_path = os.path.join(net_dir, iface)

        # type == 1 means Ethernet
        try:
            with open(os.path.join(iface_path, 'type')) as f:
                if f.read().strip() != '1':
                    continue
        except (IOError, OSError):
            continue

        # addr_assign_type - 0 = permanent, 3 = set by dev_set_mac_address
        try:
            with open(os.path.join(iface_path, 'addr_assign_type')) as f:
                if int(f.read().strip()) not in (0, 3):
                    continue
        except (IOError, OSError, ValueError):
            continue

        try:
            with open(os.path.join(iface_path, 'address')) as f:
                mac = f.read().strip()
                if mac and mac != '00:00:00:00:00:00':
                    macs.append(mac)
        except (IOError, OSError):
            continue

    return macs


def main():
    module = AnsibleModule(
        argument_spec=dict(
            dest=dict(type='path', default='/etc/drbd-proxy.license'),
            api_url=dict(type='str', default='https://api.linbit.com'),
            force=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )

    dest = module.params['dest']
    api_url = module.params['api_url'].rstrip('/')
    force = module.params['force']

    if not force and os.path.exists(dest):
        module.exit_json(
            changed=False,
            license_path=dest,
            msg='License file already exists at %s' % dest,
        )

    try:
        with open(REGISTRATION_FILE) as f:
            reg = json.load(f)
    except (IOError, OSError):
        module.fail_json(
            msg='Registration data not found at %s - run linbit_register_node first' % REGISTRATION_FILE)
    except ValueError as e:
        module.fail_json(msg='Failed to parse %s: %s' % (REGISTRATION_FILE, str(e)))

    nodehash = reg.get('nodehash')
    if not nodehash:
        module.fail_json(msg='nodehash missing from %s' % REGISTRATION_FILE)

    macs = get_mac_addresses()
    if not macs:
        module.fail_json(msg='No permanent Ethernet MAC addresses found')

    payload = {
        'nodehash': nodehash,
        'mac_addresses': macs,
    }
    if reg.get('hostname'):
        payload['hostname'] = reg['hostname']
    if reg.get('contract_id'):
        payload['contract_id'] = int(reg['contract_id'])
    if reg.get('cluster_id'):
        payload['cluster_id'] = int(reg['cluster_id'])

    if module.check_mode:
        module.exit_json(
            changed=True,
            license_path=dest,
            msg='Would fetch license to %s' % dest,
        )

    url = api_url + '/v1/license-from-nodehash'
    headers = {
        'Content-Type': 'application/json',
        'User-agent': 'linbit_proxy_license-ansible-module',
    }

    try:
        response = open_url(
            url, method='POST',
            data=json.dumps(payload).encode('utf-8'),
            headers=headers, validate_certs=True, timeout=30,
        )
        result = json.loads(response.read())
    except HTTPError as e:
        body_text = ''
        try:
            body_text = e.read().decode('utf-8', errors='replace')
        except Exception:
            pass
        module.fail_json(
            msg='Proxy license API request failed: POST %s returned %d: %s' % (
                url, e.code, body_text))
    except URLError as e:
        module.fail_json(
            msg='Proxy license API request failed: POST %s: %s' % (url, str(e.reason)))
    except Exception as e:
        module.fail_json(
            msg='Proxy license API request failed: POST %s: %s' % (url, str(e)))

    if 'error' in result:
        module.fail_json(
            msg='Proxy license API returned error: %s' % json.dumps(result['error']))

    data = result.get('data', {})
    license_b64 = data.get('license_file_content')
    if not license_b64:
        module.fail_json(
            msg='Proxy license API response missing license_file_content: %s' % json.dumps(result))

    try:
        license_bytes = base64.b64decode(license_b64)
    except Exception as e:
        module.fail_json(msg='Failed to base64-decode license content: %s' % str(e))

    try:
        parent = os.path.dirname(dest)
        if parent and not os.path.isdir(parent):
            os.makedirs(parent, 0o755)

        with open(dest, 'wb') as f:
            f.write(license_bytes)
        os.chmod(dest, 0o600)
    except (IOError, OSError) as e:
        module.fail_json(msg='Failed to write license to %s: %s' % (dest, str(e)))

    module.exit_json(
        changed=True,
        license_path=dest,
        msg='License written to %s' % dest,
    )


if __name__ == '__main__':
    main()
