registered_node
===============

Register nodes with the LINBIT subscription portal.

Requirements
------------

LINBIT portal credentials: `lb_user`, `lb_pass`, `lb_con_id`, `lb_clu_id`.

Role Variables
--------------

See `defaults/main.yml`.

Dependencies
------------

None.

Example Playbook
----------------

```yaml
- name: Register LINBIT nodes
  hosts: all
  become: true
  tasks:
    - ansible.builtin.import_role:
        name: linbit.common.registered_node
      vars:
        lb_user: "{{ lb_user }}"
        lb_pass: "{{ lb_pass }}"
        lb_con_id: "{{ lb_con_id }}"
        lb_clu_id: "{{ lb_clu_id }}"
```

License
-------

MIT

Author Information
------------------

[LINBIT](https://linbit.com)
