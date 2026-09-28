# SPDX-License-Identifier: GPL-3.0-or-later
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)
# Non-module plugins run in the Ansible controller process and must be
# GPL-3.0-or-later per the Ansible community package inclusion rules.
# The rest of the linbit.* collections remain MIT-licensed.
"""Filter plugin: select the addresses that fall inside a network."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
  name: in_network
  short_description: Select the IP addresses that fall inside a network
  version_added: "0.9.11"
  description:
    - Returns the entries of the input list that are IP addresses inside the network of
      C(network), for IPv4 and IPv6.
    - C(network) is an address in CIDR notation, such as a service IP C(192.168.222.100/24)
      or C(2001:db8:222::100/64). Host bits are ignored.
    - Entries that are not IP addresses, or belong to the other address family, are left out.
  options:
    _input:
      description: IP addresses to check, for example C(ansible_facts.all_ipv6_addresses).
      type: list
      elements: str
      required: true
    network:
      description: An address in CIDR notation whose network the addresses are checked against.
      type: str
      required: true
  author:
    - Ryan Ronnander (@rronnander)
'''

EXAMPLES = '''
- name: Assert this host has an address in an IPv4 service IP's subnet
  ansible.builtin.assert:
    that: >-
      ansible_facts.all_ipv4_addresses
      | linbit.common.in_network('192.168.222.100/24') | length > 0

- name: Assert this host has an address in an IPv6 service IP's subnet
  ansible.builtin.assert:
    that: >-
      ansible_facts.all_ipv6_addresses
      | linbit.common.in_network('2001:db8:222::100/64') | length > 0
'''

RETURN = '''
  _value:
    description: The input addresses that are inside the network.
    type: list
    elements: str
'''

import ipaddress


def in_network(addresses, network):
    net = ipaddress.ip_interface(network).network
    matches = []
    for addr in addresses:
        try:
            if ipaddress.ip_address(addr) in net:
                matches.append(addr)
        except ValueError:
            pass
    return matches


class FilterModule:
    def filters(self):
        return {'in_network': in_network}
