# LINBIT Common Collection

The `linbit.common` Ansible collection providing shared utilities for the [LINBIT®](https://linbit.com) Ansible collections:

- [`linbit.drbd`](https://github.com/LINBIT/ansible-drbd-collection)
- [`linbit.drbd_reactor`](https://github.com/LINBIT/ansible-drbd_reactor-collection)
- [`linbit.linstor`](https://github.com/LINBIT/ansible-linstor-collection)

Includes LINBIT customer portal registration, public package repository setup for Ubuntu LTS and Proxmox VE, [DRBD®](https://linbit.com/drbd/) Proxy license retrieval, and kernel-detection filter plugins.

## Requirements

- ansible-core 2.16 or newer

## Installation

Install the collection with the Ansible Galaxy command-line tool:

```bash
# Install from GitHub until published in Ansible Galaxy
ansible-galaxy collection install git+https://github.com/LINBIT/ansible-common-collection.git
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`:

```yaml
collections:
  - name: linbit.common
    source: https://github.com/LINBIT/ansible-common-collection.git
    type: git
```

To upgrade to the latest available version:

```bash
# Upgrade from GitHub until published in Ansible Galaxy
ansible-galaxy collection install --upgrade git+https://github.com/LINBIT/ansible-common-collection.git
```

See [using Ansible collections](https://docs.ansible.com/ansible/latest/collections_guide/) for more details.

## Roles

| Role | Description |
|---|---|
| [`customer_repo`](roles/customer_repo/README.md) | Register nodes with the LINBIT subscription portal (`my.linbit.com`) |
| [`public_repo`](roles/public_repo/README.md) | Configure the LINBIT public APT repository for Ubuntu (PPA) and Proxmox VE |
| [`zfs_install`](roles/zfs_install/README.md) | Install OpenZFS packages and load the `zfs` kernel module across distributions |

## Modules

| Module | Description |
|---|---|
| `linbit_register_node` | Register a node with the LINBIT customer portal API. Used internally by `customer_repo`; can also be invoked directly for advanced workflows. |
| `linbit_proxy_license` | Fetch the DRBD Proxy license file for a registered node. Reads identity from `/var/lib/drbd-support/registration.json` and POSTs to `my.linbit.com/v1/license-from-nodehash`. |

## Filter plugins

| Filter | Description |
|---|---|
| `is_pve` | Returns true when running on a Proxmox VE kernel (`'pve'` in `ansible_kernel`). Used to gate Proxmox-specific tasks. |
| `is_uek` | Returns true when running on an Oracle Linux UEK kernel (`'uek'` in `ansible_kernel`). Used to choose between RHCK and UEK kernel-devel packages. |

## Licensing

This collection is primarily licensed and distributed as a whole under the MIT License. See [LICENSE](LICENSE) for the full text.

The following files are licensed under the [GNU General Public License v3.0 or later](https://www.gnu.org/licenses/gpl-3.0.txt), as required by the Ansible community package inclusion rules:

- [`plugins/filter/is_pve.py`](plugins/filter/is_pve.py)
- [`plugins/filter/is_uek.py`](plugins/filter/is_uek.py)

## Authors

Created in 2026 by [Ryan Ronnander](https://github.com/ryan-ronnander) on behalf of [LINBIT](https://linbit.com).

Inspired by pre-collection Ansible contributions from [Matt Kereczman](https://github.com/kermat), [Ryan Ronnander](https://github.com/ryan-ronnander), [Michael Troutman](https://github.com/emteelb), and [Devin Vance](https://github.com/dvance).
