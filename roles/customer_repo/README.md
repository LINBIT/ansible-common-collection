customer_repo
=============

Register nodes with the LINBIT customer portal and configure LINBIT package repositories.

This role is the Ansible-driven equivalent of running `linbit-manage-node.py` manually.
The script (fetched from `https://my.linbit.com/linbit-manage-node.py`) is the standard
LINBIT tool for node registration — it authenticates against the customer portal using
contract credentials and writes OS-appropriate package repository configuration.
See [packages.linbit.com](https://packages.linbit.com/) for details.

Requirements
------------

LINBIT customer portal credentials, typically stored in `lbcreds.yaml` and symlinked
into each stack's `group_vars/all/`:

| Variable | Description |
|---|---|
| `lb_user` | LINBIT portal username |
| `lb_pass` | LINBIT portal password |
| `lb_con_id` | Contract ID |
| `lb_clu_id` | Cluster ID |

Role Variables
--------------

| Variable | Default | Description |
|---|---|---|
| `customer_repo_force_register` | `false` | Re-run registration even if the script has not changed |
| `customer_repo_use_rhel_minor_version` | `false` | Pin RHEL repos to the specific minor version (e.g. `8.6`) rather than the major stream |
| `lb_repos` | (undefined) | Optional space-separated list of repos to enable selectively; omit to enable all available repos |
| `staging` | (undefined) | Set to `true` to rewrite repo URLs to point at staging packages |

Dependencies
------------

None.

Example Playbook
----------------

```yaml
- name: Register LINBIT nodes
  hosts: all
  become: true
  tasks:
    - ansible.builtin.import_role:
        name: linbit.common.customer_repo
      vars:
        lb_user: "{{ lb_user }}"
        lb_pass: "{{ lb_pass }}"
        lb_con_id: "{{ lb_con_id }}"
        lb_clu_id: "{{ lb_clu_id }}"
```

License
-------

MIT

Author Information
------------------

[LINBIT](https://linbit.com)
