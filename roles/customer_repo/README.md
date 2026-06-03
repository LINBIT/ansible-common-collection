# customer_repo

Register nodes with the LINBIT customer portal and configure LINBIT package repositories.

This role uses the `linbit.common.linbit_register_node` module to authenticate against the LINBIT customer portal API, register nodes, and write OS-appropriate package repository configuration.

Use [my.linbit.com](https://my.linbit.com/) to manage credentials, nodes, and clusters.
See [packages.linbit.com](https://packages.linbit.com/) to register nodes manually using [`linbit-manage-node.py`](https://packages.linbit.com/public/linbit-manage-node.py).

Registration data is cached in `/var/lib/drbd-support/registration.json` for idempotency.
Re-registering can be forced by setting `customer_repo_force_register: true`.

## Requirements

LINBIT customer portal credentials must be provided as Ansible variables (for example in `group_vars`, `host_vars`, or `--extra-vars`):

| Variable | Required | Description |
|---|---|---|
| `linbit_username` | yes | LINBIT portal username |
| `linbit_password` | yes | LINBIT portal password |
| `linbit_contract_id` | no | Contract ID, auto-discovered from the newest (highest ID) active contract on the account |
| `linbit_cluster_id` | no | Cluster ID, auto-discovered from existing registration or the most recent cluster, or a new cluster is created |

If `linbit_username` or `linbit_password` is undefined or empty, the role prompts for it interactively at runtime.
Prompts run once regardless of how many hosts are in the play.
The password prompt is suppressed from Ansible output (`no_log: true`).

## Role variables

| Variable | Default | Description |
|---|---|---|
| `customer_repo_force_register` | `false` | Force re-registration even if the node is already registered |
| `customer_repo_el_minor` | `false` | Pin Enterprise Linux repo URLs to the specific minor version (for example `9.3`) rather than the major stream |
| `customer_repo_includes` | `[]` | List of glob patterns; only repos matching at least one pattern are enabled, empty list enables all repos |
| `customer_repo_default_excludes` | `['drbd-8*', 'drbd-9.0*', 'drbd-proxy-3*']` | Default repo exclusion patterns shipped by the collection; override to `[]` to disable |
| `customer_repo_user_excludes` | `[]` | User-defined repo exclusion patterns, merged with `customer_repo_default_excludes` |
| `customer_repo_staging` | `false` | Also write a supplemental staging repo file alongside the production repository file (see [Staging repositories](#staging-repositories)) |
| `customer_repo_staging_repos` | `['drbd-9']` | Anchored glob patterns selecting which repos go in the staging file |
| `customer_repo_install_proxy_license` | `false` | Fetch the DRBD Proxy license using the `linbit.common.linbit_proxy_license` module; requires `linbit_cluster_id`, otherwise skipped silently (interactive runs prompt y/N when unset) |
| `customer_repo_proxy_license_path` | `/etc/drbd-proxy.license` | Destination path for the fetched DRBD Proxy license file |

### Staging repositories

LINBIT staging repositories are supplemental, not a mirror of production.
They ship only the small subset of packages under active testing, so the production repository must stay enabled for everything else to resolve.
Setting `customer_repo_staging: true` writes a second repo file (`linbit-staging.repo` on RPM distributions, `linbit-staging.sources` on Debian and Ubuntu) alongside the production repository file, containing staging versions of the repos matching `customer_repo_staging_repos`.
That pattern list is authoritative for the staging file: `customer_repo_default_excludes` and `customer_repo_user_excludes` do not apply to it, so a repo excluded in production can still be pulled from staging by adding it here.
Staging metadata is not signed consistently, so RPM staging sections are suffixed with `-staging` and set `repo_gpgcheck=0`, and APT staging sets `Trusted: yes`.

## Dependencies

None.

## Example playbook

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

## License

MIT

## Author information

[LINBIT](https://linbit.com)
