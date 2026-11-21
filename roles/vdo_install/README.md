# vdo_install

Install the VDO userspace tools and load the VDO kernel module, persisting it across reboots.

LVM builds VDO volumes itself (refer to [lvmvdo(7)](https://man7.org/linux/man-pages/man7/lvmvdo.7.html)), and it needs two things from the node:

- the `vdo` package, which provides `vdoformat` for creating a VDO volume and `vdostats` for its usage
- the VDO kernel module: the in-tree `dm-vdo` module on Linux 6.9 and newer, or `kvdo` from the `kmod-kvdo` package on older Enterprise Linux kernels

The role selects the packages and the module per distribution and kernel:

| Distribution | Packages | Kernel module |
|---|---|---|
| Enterprise Linux 9, Red Hat compatible kernel | `vdo`, `kmod-kvdo` | `kvdo` |
| Enterprise Linux 10, Red Hat compatible kernel | `vdo` | `dm-vdo`, in `kernel-modules-core` |
| Oracle Linux 10 with Unbreakable Enterprise Kernel (UEK) 8 | `vdo`, `kernel-uek-modules-core` for the running kernel | `dm-vdo` |
| Debian 13 and newer, Proxmox VE 9 and newer | `vdo` | `dm-vdo` |
| Ubuntu 25.04 and newer | `vdo` from universe | `dm-vdo` |

On UEK, the role installs `kernel-uek-modules-core` at the version of the running kernel.
An unversioned install would resolve to the newest kernel in the repository, install it, and make it the boot default.

The role refuses these platforms:

- Ubuntu 24.04 and older, and Debian 12 and older: the distribution ships no `vdo` package.
- Red Hat family releases older than 9.
- Oracle Linux 9, with either kernel: on UEK, its `vdo` package requires `kmod-kvdo`, which installs the Red Hat compatible kernel next to UEK, and a later update of that kernel makes it the boot default.
- openSUSE Leap 16.0 and SUSE Linux Enterprise Server (SLES) 16.0: the kernel ships `dm-vdo` in `kernel-default-extra`, but the distribution ships no `vdo` package.
- A kernel older than 6.9 other than the Red Hat compatible kernel of Enterprise Linux 9: it has no `dm-vdo` module.

On an unsupported platform, the role fails before it changes anything and lists the supported platforms.

> [!NOTE]
> A thin pool on VDO, such as the one the `linbit.linstor.storage_pool` role builds for `vdo: true`, also needs LVM 2.03.24 or newer, which this role does not install.

## Requirements

- The `community.general` collection (`modprobe` module).

## Role variables

None.

## Dependencies

None.

## Example playbook

```yaml
- name: Install VDO
  hosts: storage_nodes
  any_errors_fatal: true
  become: true
  tasks:
    - name: Install VDO
      ansible.builtin.import_role:
        name: linbit.common.vdo_install
```

## License

MIT

## Author information

[LINBIT](https://linbit.com)
