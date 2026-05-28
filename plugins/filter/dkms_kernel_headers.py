# SPDX-License-Identifier: GPL-3.0-or-later
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)
# Non-module plugins run in the Ansible controller process and must be
# GPL-3.0-or-later per the Ansible community package inclusion rules.
# The rest of the linbit.* collections remain MIT-licensed.
"""Filter plugin: kernel header packages for DKMS module builds."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re

DOCUMENTATION = '''
  name: dkms_kernel_headers
  short_description: Kernel header packages required to successfully build DKMS modules
  version_added: "0.9.9"
  description:
    - Returns the kernel-header packages DKMS needs to build out-of-tree modules
      (DRBD, ZFS, SCST) for the running kernel.
    - On the Debian family, returns the flavor/edition metapackage (for example
      C(linux-headers-aws) on Ubuntu or C(linux-headers-cloud-amd64) on Debian) so
      future kernels of the same flavor stay covered on C(apt) upgrade, plus the
      exact C(linux-headers-<release>) for the running kernel.
    - On the RedHat family, returns the exact devel package for the running kernel,
      versioned to the release - C(kernel-devel), or C(kernel-uek-devel) (Oracle
      UEK) or C(kernel-rt-devel) (Real Time). The aarch64 64K-page kernel uses
      the unversioned C(kernel-64k-devel), since its C(+64k) uname suffix is not
      part of the package version.
    - On Proxmox VE, returns C(proxmox-default-headers).
    - Assumes Debian-family flavors have an unversioned C(linux-headers-<flavor>)
      metapackage, which holds for server and cloud kernels; flavors whose metapackage
      name includes a release suffix (for example Ubuntu C(oem) -> C(linux-headers-oem-24.04))
      are not supported. Returns an empty list on families with no common DKMS header
      convention (for example SUSE, which ships prebuilt KMPs).
  options:
    _input:
      description: Ansible facts dictionary, typically C(ansible_facts).
      type: dict
      required: true
  author:
    - Ryan Ronnander (@rronnander)
'''

EXAMPLES = '''
- name: Install kernel headers for DKMS
  ansible.builtin.package:
    name: "{{ ansible_facts | linbit.common.dkms_kernel_headers }}"
    state: present
'''

RETURN = '''
  _value:
    description: List of kernel-header package names for the running kernel.
    type: list
    elements: str
'''


def dkms_kernel_headers(facts):
    kernel = facts.get('kernel', '')
    distribution = facts.get('distribution', '').lower()
    os_family = facts.get('os_family', '').lower()

    if 'pve' in kernel:
        return ['proxmox-default-headers']

    # RedHat family: exact-versioned devel matching the running kernel. 64k is
    # the exception - its uname adds a +64k suffix that isn't in the package
    # version, so the unversioned package name is used.
    if os_family == 'redhat':
        if 'uek' in kernel:
            return ['kernel-uek-devel-' + kernel]
        if 'rt' in kernel:
            return ['kernel-rt-devel-' + kernel]
        if '64k' in kernel:
            return ['kernel-64k-devel']
        return ['kernel-devel-' + kernel]

    exact = 'linux-headers-' + kernel

    # Ubuntu metapackage drops the arch (linux-headers-aws); Debian keeps it
    # (linux-headers-cloud-amd64). Hence the two different version-prefix strips.
    if distribution == 'ubuntu':
        flavor = re.sub(r'^[0-9.]+-[0-9]+-', '', kernel)
        return ['linux-headers-' + flavor, exact]

    if os_family == 'debian':
        suffix = re.sub(r'^[0-9][0-9.]*(\+deb[0-9]+)?(-[0-9]+)?-', '', kernel)
        return ['linux-headers-' + suffix, exact]

    return []


class FilterModule:
    def filters(self):
        return {'dkms_kernel_headers': dkms_kernel_headers}
