linbit_public_repo
==================

Configure the LINBIT public package repository for Ubuntu and Proxmox VE.

On **Ubuntu** nodes, adds the [LINBIT drbd9-stack Launchpad PPA](https://launchpad.net/~linbit/+archive/ubuntu/linbit-drbd9-stack).
On **Proxmox VE** nodes, installs `linbit-keyring` and adds the LINBIT public APT repo.

> **Note:** Plain Debian (without Proxmox VE) is not supported.

Requirements
------------

None.

Role Variables
--------------

See `defaults/main.yml`.

| Variable | Default | Description |
|---|---|---|
| `lb_ppa` | `ppa:linbit/linbit-drbd9-stack` | Launchpad PPA for Ubuntu |
| `lb_keyring_package_url` | `https://packages.linbit.com/public/linbit-keyring.deb` | LINBIT keyring package URL |
| `lb_proxmox_repo` | `http://packages.linbit.com/public/` | LINBIT public APT repo URL |
| `lb_gpg_path` | `/etc/apt/trusted.gpg.d/linbit-keyring.gpg` | GPG key path |

Dependencies
------------

None.

Example Playbook
----------------

```yaml
- name: Configure LINBIT public repo
  hosts: all
  become: true
  tasks:
    - ansible.builtin.import_role:
        name: linbit.common.linbit_public_repo
```

License
-------

MIT

Author Information
------------------

[LINBIT](https://linbit.com)
