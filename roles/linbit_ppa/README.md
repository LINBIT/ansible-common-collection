linbit_ppa
==========

Add the LINBIT Launchpad PPA for Ubuntu nodes.

Requirements
------------

Ubuntu.

Role Variables
--------------

See `defaults/main.yml`.

Dependencies
------------

None.

Example Playbook
----------------

```yaml
- name: Add LINBIT PPA
  hosts: ubuntu_nodes
  become: true
  tasks:
    - ansible.builtin.include_role:
        name: linbit.common.linbit_ppa
```

License
-------

MIT

Author Information
------------------

[LINBIT](https://linbit.com)
