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

## Filter Plugins

| Filter | Description |
|---|---|
| `is_pve` | Returns true when running on a Proxmox VE kernel (`'pve'` in `ansible_kernel`). Used to gate Proxmox-specific tasks. |
| `is_uek` | Returns true when running on an Oracle Linux UEK kernel (`'uek'` in `ansible_kernel`). Used to choose between RHCK and UEK kernel-devel packages. |

## Dependencies

None.
