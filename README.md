# Ansible Collection - linbit.common

Handles LINBIT portal node registration and public LINBIT package repository setup.
This collection has no dependencies on other LINBIT collections.

## Roles

| Role | Description |
|---|---|
| `customer_repo` | Register nodes with the LINBIT subscription portal (`my.linbit.com`) |
| `public_repo` | Configure the LINBIT public APT repository for Ubuntu (PPA) and Proxmox VE |

## Modules

| Module | Description |
|---|---|
| `linbit_register_node` | Register a node with the LINBIT customer portal API. Used internally by `customer_repo`; can also be invoked directly for advanced workflows. |
| `linbit_proxy_license` | Fetch the DRBD Proxy license file for a registered node. Reads identity from `/var/lib/drbd-support/registration.json` and POSTs to `my.linbit.com/v1/license-from-nodehash`. |

## Filter Plugins

| Filter | Description |
|---|---|
| `is_pve` | Returns true when running on a Proxmox VE kernel (`'pve'` in `ansible_kernel`). Used to gate Proxmox-specific tasks. |
| `is_uek` | Returns true when running on an Oracle Linux UEK kernel (`'uek'` in `ansible_kernel`). Used to choose between RHCK and UEK kernel-devel packages. |

## Dependencies

None.

## Licensing

This collection is primarily licensed and distributed as a whole under the MIT License. See [LICENSE](LICENSE) for the full text.

The following files are licensed under the [GNU General Public License v3.0 or later](https://www.gnu.org/licenses/gpl-3.0.txt), as required by the Ansible community package inclusion rules:

- [`plugins/filter/is_pve.py`](plugins/filter/is_pve.py)
- [`plugins/filter/is_uek.py`](plugins/filter/is_uek.py)
