#!/usr/bin/python
# SPDX-License-Identifier: MIT

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: linbit_register_node
short_description: Register a node with the LINBIT customer portal
version_added: "0.9.7"
description:
  - Registers a node with the LINBIT customer portal API.
  - Gathers permanent Ethernet MAC addresses from sysfs for node identification.
  - Checks if the node is already registered for idempotency.
  - Saves registration data to C(/var/lib/drbd-support/registration.json).
options:
  username:
    description: LINBIT portal username.
    type: str
    required: true
  password:
    description: LINBIT portal password.
    type: str
    required: true
  contract_id:
    description:
      - LINBIT contract ID.
      - If omitted, the module queries the API and uses the newest (highest ID) active contract.
    type: str
    required: false
  cluster_id:
    description:
      - LINBIT cluster ID.
      - If omitted, the module checks whether the node is already registered (reuses that cluster),
        falls back to the most recent cluster on the contract, or creates a new cluster.
    type: str
    required: false
  force:
    description: Force re-registration even if the node is already registered.
    type: bool
    default: false
  api_url:
    description: LINBIT API base URL.
    type: str
    default: https://api.linbit.com
  distribution:
    description:
      - LINBIT distribution string identifying the OS family for repo selection
        (for example C(ubuntu-noble), C(debian-trixie), C(rhel9), C(sles15)).
      - Resolved by the calling role from Ansible facts.
    type: str
    required: true
notes:
  - Fully idempotent. Saves registration data to C(/var/lib/drbd-support/registration.json)
    and skips the API call on subsequent runs when MAC addresses match.
  - Supports C(check_mode). In check mode, the module authenticates and resolves
    contract and cluster IDs but does not register the node.
  - MAC addresses are gathered from C(/sys/class/net/) and filtered to permanent
    Ethernet interfaces only (excluding virtual, bond, and loopback interfaces).
  - When C(contract_id) is omitted, the module selects the newest active contract
    on the account (highest numeric ID).
  - When C(cluster_id) is omitted, the module checks for an existing registration,
    falls back to the most recent cluster on the contract, or creates a new cluster.
  - Consider storing C(username) and C(password) in an Ansible Vault encrypted file
    rather than in plain-text variables.
    See L(Ansible Vault,https://docs.ansible.com/ansible/latest/vault_guide/index.html).
seealso:
  - name: LINBIT Customer Portal
    link: https://my.linbit.com/
    description: Manage contracts, clusters, and node registrations.
author:
  - Ryan Ronnander (@rronnander)
'''

EXAMPLES = r'''
- name: Register node (auto-discover contract and cluster)
  linbit.common.linbit_register_node:
    username: "{{ linbit_username }}"
    password: "{{ linbit_password }}"
  register: registration

- name: Register node with explicit IDs
  linbit.common.linbit_register_node:
    username: "{{ linbit_username }}"
    password: "{{ linbit_password }}"
    contract_id: "{{ linbit_contract_id }}"
    cluster_id: "{{ linbit_cluster_id }}"

- name: Force re-registration
  linbit.common.linbit_register_node:
    username: "{{ linbit_username }}"
    password: "{{ linbit_password }}"
    force: true
'''

RETURN = r'''
already_registered:
  description: Whether the node was already registered before this run.
  type: bool
  returned: always
nodehash:
  description: Node hash assigned by the LINBIT portal.
  type: str
  returned: success
cluster_id:
  description: Cluster ID used for registration.
  type: str
  returned: success
contract_id:
  description: Contract ID used for registration.
  type: str
  returned: success
hostname:
  description: Hostname used for registration.
  type: str
  returned: success
mac_addresses:
  description: MAC addresses detected on the node.
  type: list
  elements: str
  returned: success
repos:
  description: Repository configuration returned by the API.
  type: dict
  returned: success
repo_config:
  description: Raw repository configuration string returned by the API.
  type: str
  returned: success
'''

import json
import os
import socket

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import open_url

try:
    from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
except ImportError:
    from urllib.error import HTTPError, URLError

REGISTRATION_DIR = '/var/lib/drbd-support'
REGISTRATION_FILE = os.path.join(REGISTRATION_DIR, 'registration.json')
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

        # addr_assign_type: 0 = permanent, 3 = set by dev_set_mac_address
        try:
            with open(os.path.join(iface_path, 'addr_assign_type')) as f:
                if int(f.read().strip()) not in (0, 3):
                    continue
        except (IOError, OSError, ValueError):
            continue

        # Read the MAC address
        try:
            with open(os.path.join(iface_path, 'address')) as f:
                mac = f.read().strip()
                if mac and mac != '00:00:00:00:00:00':
                    macs.append(mac)
        except (IOError, OSError):
            continue

    return macs


def load_registration():
    """Load saved registration data from disk."""
    try:
        with open(REGISTRATION_FILE) as f:
            return json.load(f)
    except (IOError, OSError, ValueError):
        return None


def save_registration(data):
    """Save registration data to disk."""
    if not os.path.isdir(REGISTRATION_DIR):
        os.makedirs(REGISTRATION_DIR, 0o755)

    with open(REGISTRATION_FILE, 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)
    os.chmod(REGISTRATION_FILE, 0o600)


def api_request(module, url, method='POST', data=None, token=None):
    """Make an API request and return the parsed JSON response."""
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = 'Bearer ' + token

    body = json.dumps(data).encode('utf-8') if data is not None else None

    try:
        response = open_url(
            url, method=method, data=body, headers=headers,
            validate_certs=True, timeout=30,
        )
        return json.loads(response.read())
    except HTTPError as e:
        body_text = ''
        try:
            body_text = e.read().decode('utf-8', errors='replace')
        except Exception:
            pass
        module.fail_json(
            msg="API request failed: %s %s returned %d: %s" % (
                method, url, e.code, body_text),
        )
    except URLError as e:
        module.fail_json(
            msg="API request failed: %s %s: %s" % (method, url, str(e.reason)),
        )
    except Exception as e:
        module.fail_json(
            msg="API request failed: %s %s: %s" % (method, url, str(e)),
        )


def api_login(module, api_url, username, password):
    """Authenticate with the LINBIT API and return a JWT token."""
    url = api_url + '/v1/login'
    headers = {'Content-Type': 'application/json'}
    body = json.dumps({'user': username, 'pass': password}).encode('utf-8')

    try:
        response = open_url(
            url, method='POST', data=body, headers=headers,
            validate_certs=True, timeout=30,
        )
        result = json.loads(response.read())
    except HTTPError as e:
        if e.code == 401:
            module.fail_json(
                msg="Login failed: invalid username or password. "
                    "Verify your credentials at https://my.linbit.com/")
        module.fail_json(
            msg="Login failed: API returned %d. "
                "Verify your credentials at https://my.linbit.com/" % e.code)
    except URLError as e:
        module.fail_json(
            msg="Login failed: could not reach %s: %s" % (url, str(e.reason)))
    except Exception as e:
        module.fail_json(msg="Login failed: %s" % str(e))

    data = result.get('data', result)
    token = data.get('access_token') or data.get('token')
    if not token:
        module.fail_json(
            msg="Login failed: unexpected API response. "
                "Verify your credentials at https://my.linbit.com/")
    return token


def api_get_contracts(module, api_url, token):
    """List contracts on the account. Returns a list of contract dicts."""
    result = api_request(
        module, api_url + '/v1/my/contracts', method='GET', token=token)
    data = result.get('data', result)
    return data.get('list', [])


def api_get_clusters(module, api_url, token, contract_id):
    """List clusters on a contract. Returns a list of cluster dicts."""
    url = '%s/v1/my/contracts/%s/clusters' % (api_url, contract_id)
    result = api_request(module, url, method='GET', token=token)
    data = result.get('data', result)
    return data.get('list', [])


def api_create_cluster(module, api_url, token, contract_id):
    """Create a new cluster on a contract. Returns the cluster dict."""
    url = '%s/v1/my/contracts/%s/clusters' % (api_url, contract_id)
    result = api_request(module, url, data={}, token=token)
    data = result.get('data', result)
    return data


def api_is_node_registered(module, api_url, token, contract_id,
                           hostname, mac_addresses):
    """Check if a node is already registered. Returns dict or None."""
    url = '%s/v1/my/contracts/%s/is-node-registered' % (
        api_url, contract_id)
    result = api_request(module, url, data={
        'hostname': hostname,
        'mac_addresses': mac_addresses,
    }, token=token)
    data = result.get('data', result)
    if 'cluster_id' in data:
        return data
    return None


def api_register_node(module, api_url, token, contract_id, cluster_id,
                      hostname, distribution, mac_addresses):
    """Register the node with the LINBIT API."""
    url = '%s/v1/my/contracts/%s/clusters/%s/register-node' % (
        api_url, contract_id, cluster_id)
    result = api_request(module, url, data={
        'hostname': hostname,
        'distribution': distribution,
        'mac_addresses': mac_addresses,
        'register_version': 1,
        'hidden_repos': False,
    }, token=token)
    return result.get('data', result)


def resolve_contract(module, api_url, token, contract_id):
    """Resolve contract_id: use explicit value, or auto-discover from API."""
    if contract_id:
        return contract_id

    contracts = api_get_contracts(module, api_url, token)
    if len(contracts) == 0:
        module.fail_json(msg="No active contracts found for this account")

    # Newest contract has the highest ID
    best = max(contracts, key=lambda c: int(c['id']))
    return str(best['id'])


def resolve_cluster(module, api_url, token, contract_id, cluster_id,
                    hostname, mac_addresses):
    """Resolve cluster_id: use explicit value, or auto-discover from API."""
    if cluster_id:
        return cluster_id

    # Check if the node is already registered on this contract
    reg = api_is_node_registered(
        module, api_url, token, contract_id, hostname, mac_addresses)
    if reg:
        return str(reg['cluster_id'])

    # Use the most recent cluster, or create a new one
    clusters = api_get_clusters(module, api_url, token, contract_id)
    if clusters:
        return str(clusters[-1]['id'])

    new_cluster = api_create_cluster(module, api_url, token, contract_id)
    return str(new_cluster['id'])


def main():
    module = AnsibleModule(
        argument_spec=dict(
            username=dict(type='str', required=True),
            password=dict(type='str', required=True, no_log=True),
            contract_id=dict(type='str', required=False, default=None),
            cluster_id=dict(type='str', required=False, default=None),
            distribution=dict(type='str', required=True),
            force=dict(type='bool', default=False),
            api_url=dict(type='str', default='https://api.linbit.com'),
        ),
        supports_check_mode=True,
    )

    params = module.params
    force = params['force']
    api_url = params['api_url'].rstrip('/')

    # Step 1: Gather MAC addresses
    mac_addresses = get_mac_addresses()
    if not mac_addresses:
        module.fail_json(msg="No permanent Ethernet MAC addresses found")

    hostname = socket.gethostname()

    # Step 2: Check saved registration for idempotency
    if not force:
        saved = load_registration()
        if saved and sorted(saved.get('mac_addresses', [])) == sorted(mac_addresses):
            module.exit_json(
                changed=False,
                already_registered=True,
                nodehash=saved.get('nodehash', ''),
                cluster_id=saved.get('cluster_id', ''),
                contract_id=saved.get('contract_id', ''),
                hostname=saved.get('hostname', hostname),
                mac_addresses=mac_addresses,
                repos=saved.get('repos', {}),
                repo_config=saved.get('repo_config', ''),
                msg="Node already registered (cached)",
            )

    # Step 3: Login to API
    token = api_login(module, api_url, params['username'], params['password'])

    # Step 4: Resolve contract and cluster IDs
    contract_id = resolve_contract(
        module, api_url, token, params['contract_id'])
    cluster_id = resolve_cluster(
        module, api_url, token, contract_id, params['cluster_id'],
        hostname, mac_addresses)

    # Step 5: Check mode stops here
    if module.check_mode:
        module.exit_json(
            changed=True,
            already_registered=False,
            nodehash='',
            cluster_id=cluster_id,
            contract_id=contract_id,
            hostname=hostname,
            mac_addresses=mac_addresses,
            repos={},
            msg="Node would be registered (check mode)",
        )

    # Step 6: Register the node (API handles re-registration gracefully)
    result = api_register_node(
        module, api_url, token,
        contract_id, cluster_id,
        hostname, params['distribution'], mac_addresses,
    )

    repos = result.get('repos', {})
    repo_config = result.get('repo_config', '')
    nodehash = result.get('nodehash', '')
    result_cluster_id = str(result.get('cluster_id', cluster_id))

    # Step 7: Save registration data
    registration_data = {
        'nodehash': nodehash,
        'cluster_id': result_cluster_id,
        'contract_id': contract_id,
        'hostname': hostname,
        'mac_addresses': mac_addresses,
        'repos': repos,
        'repo_config': repo_config,
    }

    try:
        save_registration(registration_data)
    except (IOError, OSError) as e:
        module.warn("Failed to save registration data: %s" % str(e))

    module.exit_json(
        changed=True,
        already_registered=False,
        nodehash=nodehash,
        cluster_id=result_cluster_id,
        contract_id=contract_id,
        hostname=hostname,
        mac_addresses=mac_addresses,
        repos=repos,
        repo_config=repo_config,
        msg="Node registered successfully",
    )


if __name__ == '__main__':
    main()
