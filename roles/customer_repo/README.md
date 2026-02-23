customer_repo
=============

Register nodes with the LINBIT customer portal and configure LINBIT package repositories.

This role uses the `linbit.common.linbit_register_node` module to authenticate against the LINBIT customer portal API, register nodes, and write OS-appropriate package repository configuration.

Use [my.linbit.com](https://my.linbit.com/) to manage credentials, nodes, and clusters.
See [packages.linbit.com](https://packages.linbit.com/) to register nodes manually via python script ([`linbit-manage-node.py`](https://packages.linbit.com/public/linbit-manage-node.py)).

Registration data is cached in `/var/lib/drbd-support/registration.json` for idempotency. Re-registering can be forced by setting `customer_repo_force_register: true`.

Requirements
------------

LINBIT customer portal credentials must be provided as Ansible variables (e.g. via `group_vars`, `host_vars`, or `--extra-vars`):

| Variable | Required | Description |
|---|---|---|
| `linbit_username` | yes | LINBIT portal username |
| `linbit_password` | yes | LINBIT portal password |
| `linbit_contract_id` | no | Contract ID. Auto-discovered from the newest (highest ID) active contract on the account |
| `linbit_cluster_id` | no | Cluster ID. Auto-discovered from existing registration, most recent cluster, or a new cluster is created |

If `linbit_username` or `linbit_password` is undefined or empty, the role prompts for it interactively at runtime.
Prompts run once regardless of how many hosts are in the play.
The password prompt is suppressed from Ansible output (`no_log: true`).

Role Variables
--------------

| Variable | Default | Description |
|---|---|---|
| `customer_repo_force_register` | `false` | Force re-registration even if the node is already registered |
| `customer_repo_el_minor` | `false` | Pin Enterprise Linux repo URLs to the specific minor version (e.g. `9.3`) rather than the major stream |
| `customer_repo_includes` | `[]` | List of glob patterns; only repos matching at least one pattern are enabled. Empty list enables all repos |
| `customer_repo_excludes` | `[]` | List of glob patterns; repos matching any pattern are disabled. Applied after included patterns |
| `customer_repo_staging` | `false` | Enable staging package URLs for repos matching `customer_repo_staging_repos` |
| `customer_repo_staging_repos` | `['drbd-9*']` | List of glob patterns; repos matching any pattern use the staging URL when `customer_repo_staging` is `true` |

Dependencies
------------

None.

Example Playbook
----------------

Enable all available LINBIT repositories:

```yaml
- name: Register LINBIT nodes
  hosts: all
  become: true
  tasks:
    - name: Register and configure LINBIT repos
      ansible.builtin.import_role:
        name: linbit.common.customer_repo
```

Exclude LINBIT Pacemaker repositories:

```yaml
- name: Register LINBIT nodes
  hosts: all
  become: true
  tasks:
    - name: Register and configure LINBIT repos
      vars:
        customer_repo_excludes:
          - 'pacemaker-*'
      ansible.builtin.import_role:
        name: linbit.common.customer_repo
```

Store credentials with Ansible Vault:

```sh
ansible-vault create group_vars/all/vault.yaml
```

```yaml
# group_vars/all/vault.yaml (encrypted)
linbit_username: myuser@example.com
linbit_password: secretpassword
```

```sh
ansible-playbook playbook.yaml --ask-vault-pass
```

License
-------

MIT

Author Information
------------------

[LINBIT](https://linbit.com)
