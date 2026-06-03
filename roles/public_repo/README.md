# public_repo

Configure the LINBIT public package repository for Ubuntu and Proxmox VE.

On **Ubuntu** nodes, adds the [LINBIT drbd9-stack Launchpad PPA](https://launchpad.net/~linbit/+archive/ubuntu/linbit-drbd9-stack).
On **Proxmox VE** nodes, installs `linbit-keyring` and adds the LINBIT public APT repo.

> **Note:** Plain Debian (without Proxmox VE) is not supported.

## Requirements

ansible-core >= 2.15 (for `deb822_repository` module).

## Role variables

See `defaults/main.yml`.

| Variable | Default | Description |
|---|---|---|
| `public_repo_ppa_url` | `https://ppa.launchpadcontent.net/linbit/linbit-drbd9-stack/ubuntu` | PPA repository URL for Ubuntu |
| `public_repo_ppa_api_url` | `https://api.launchpad.net/devel/~linbit/+archive/ubuntu/linbit-drbd9-stack` | Launchpad API URL for PPA signing key lookup |
| `public_repo_keyring_package_url` | `https://packages.linbit.com/public/linbit-keyring.deb` | LINBIT keyring package URL |
| `public_repo_proxmox_repo` | `http://packages.linbit.com/public/` | LINBIT public APT repo URL |
| `public_repo_gpg_path` | `/etc/apt/trusted.gpg.d/linbit-keyring.gpg` | GPG key path |

## Dependencies

None.

## Example playbook

```yaml
- name: Configure LINBIT public repo
  hosts: all
  any_errors_fatal: true
  become: true
  tasks:
    - name: Configure LINBIT public repo
      ansible.builtin.import_role:
        name: linbit.common.public_repo
```

## License

MIT

## Author information

[LINBIT](https://linbit.com)
