# zfs_install

Install OpenZFS packages and load the `zfs` kernel module, persisting it across reboots.

The role selects the installation method per distribution:

- **Debian**: enables the contrib and backports repositories, installs kernel headers through the `dkms_kernel_headers` filter, and builds `zfs-dkms`.
- **Ubuntu**: installs `zfsutils-linux` from the main archive. Ubuntu kernels already include the ZFS modules, but the userspace tools do not ship by default.
- **Red Hat family (stock kernel)**: installs prebuilt `kmod-zfs` packages from the OpenZFS kmod repository.
- **Oracle Linux (UEK kernel)**: builds `zfs-dkms` with a GCC toolset matching the kernel build compiler.
- **SUSE family**: installs ZFS from the openSUSE filesystems repository and allows unsupported kernel modules.

> **Note:** Proxmox VE ships ZFS out of the box. The role detects an existing installation and skips package work.

> **Warning:** On SUSE UEFI systems with Secure Boot, installing `zfs-ueficert` triggers a reboot to enroll the ZFS signing key in MOK.

> **Note:** The SUSE path requires a release that the [OBS filesystems project](https://download.opensuse.org/repositories/filesystems/) still publishes.

## Requirements

- ansible-core >= 2.15 (for the `deb822_repository` module on the Debian path).
- The `community.general` collection (`modprobe`, `zypper`, `zypper_repository` modules).

## Role variables

None.

## Dependencies

None.

## Example playbook

```yaml
- name: Install ZFS
  hosts: storage_nodes
  any_errors_fatal: true
  become: true
  tasks:
    - name: Install ZFS
      ansible.builtin.import_role:
        name: linbit.common.zfs_install
```

## License

MIT

## Author information

[LINBIT](https://linbit.com)
