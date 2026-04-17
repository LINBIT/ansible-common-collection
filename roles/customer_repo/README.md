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
| `customer_repo_default_excludes` | `['drbd-8*', 'drbd-9.0*']` | Default repo exclusion patterns shipped by the collection. Override to `[]` to disable |
| `customer_repo_user_excludes` | `[]` | User-defined repo exclusion patterns, merged with `customer_repo_default_excludes` |
| `customer_repo_staging` | `false` | Additionally write a second repo file (`linbit-staging.repo` on RPM distros, `linbit-staging.list` on Debian/Ubuntu) containing staging versions of repos matching `customer_repo_staging_repos`. The production repo file is left unchanged. Staging repos are additive and partial — they typically ship only a small subset of packages under active testing, not a full 1:1 mirror of prod — so the production repo must stay enabled for everything else to resolve. Staging sections are suffixed with `-staging` and use `repo_gpgcheck=0` since staging repo metadata is not signed consistently. |
| `customer_repo_staging_repos` | `['drbd-9']` | List of glob patterns (anchored, no implicit substring match). Repos matching any pattern are written to the staging file when `customer_repo_staging` is `true`. This list is authoritative for the staging file: `customer_repo_default_excludes` and `customer_repo_user_excludes` do NOT apply to staging, so a repo that is a stub in production (e.g. `pacemaker-3`) can still be pulled from staging if added here |

Dependencies
------------

None.

Example Playbook
----------------

Enable all available LINBIT repositories:

```yaml
- name: Register LINBIT nodes
  hosts: all
  any_errors_fatal: true
  become: true
  vars:
    linbit_username: 'myuser@example.com'
    linbit_password: 'secretpassword'
  tasks:
    - name: Register and configure LINBIT repos
      ansible.builtin.import_role:
        name: linbit.common.customer_repo
```

Store credentials with Ansible Vault:

```sh
ansible-vault create group_vars/all/vault.yaml
```

```yaml
# group_vars/all/vault.yaml (encrypted)
linbit_username: 'myuser@example.com'
linbit_password: 'secretpassword'
```

```sh
ansible-playbook playbook.yaml --ask-vault-pass
```

Exclude additional repositories (merged with default excludes):

```yaml
- name: Register LINBIT nodes
  hosts: all
  any_errors_fatal: true
  become: true
  tasks:
    - name: Register and configure LINBIT repos
      ansible.builtin.import_role:
        name: linbit.common.customer_repo
      vars:
        customer_repo_user_excludes:
          - 'pacemaker-*'
```

License
-------

MIT

Author Information
------------------

[LINBIT](https://linbit.com)
