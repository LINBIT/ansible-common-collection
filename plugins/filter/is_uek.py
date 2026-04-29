# SPDX-License-Identifier: MIT
"""Filter plugin: detect Oracle Linux UEK kernel."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
  name: is_uek
  short_description: Detect an Oracle Linux UEK kernel
  version_added: "0.9.0"
  description:
    - Returns C(true) when the kernel string contains C(uek), C(false) otherwise.
    - Used to choose between RHCK and UEK kernel-devel packages on Oracle Linux.
  options:
    _input:
      description: Ansible facts dictionary, typically C(ansible_facts).
      type: dict
      required: true
  author:
    - Ryan Ronnander (@rronnander)
'''

EXAMPLES = '''
- name: Install kernel-uek-devel for the running UEK kernel
  ansible.builtin.dnf:
    name: "kernel-uek-devel-{{ ansible_kernel }}"
  when: ansible_facts | linbit.common.is_uek
'''

RETURN = '''
  _value:
    description: True if the kernel string contains C(uek), otherwise false.
    type: bool
'''


def is_uek(facts):
    return 'uek' in facts.get('kernel', '')


class FilterModule:
    def filters(self):
        return {'is_uek': is_uek}
