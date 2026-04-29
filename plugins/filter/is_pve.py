# SPDX-License-Identifier: MIT
"""Filter plugin: detect Proxmox VE kernel."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
  name: is_pve
  short_description: Detect a Proxmox VE kernel
  version_added: "0.9.0"
  description:
    - Returns C(true) when the kernel string contains C(pve), C(false) otherwise.
    - Used to gate Proxmox VE-specific package and repo logic in roles.
  options:
    _input:
      description: Ansible facts dictionary, typically C(ansible_facts).
      type: dict
      required: true
  author:
    - Ryan Ronnander (@rronnander)
'''

EXAMPLES = '''
- name: Install Proxmox VE specific kernel headers
  ansible.builtin.apt:
    name: "pve-headers-{{ ansible_kernel }}"
  when: ansible_facts | linbit.common.is_pve
'''

RETURN = '''
  _value:
    description: True if the kernel string contains C(pve), otherwise false.
    type: bool
'''


def is_pve(facts):
    return 'pve' in facts.get('kernel', '')


class FilterModule:
    def filters(self):
        return {'is_pve': is_pve}
