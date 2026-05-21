# Linbit\.Common Release Notes

**Topics**

- <a href="#v0-9-8">v0\.9\.8</a>
    - <a href="#minor-changes">Minor Changes</a>
- <a href="#v0-9-7">v0\.9\.7</a>
    - <a href="#minor-changes-1">Minor Changes</a>
    - <a href="#bugfixes">Bugfixes</a>
    - <a href="#new-modules">New Modules</a>

This changelog describes changes after version 0\.9\.6\.

<a id="v0-9-8"></a>
## v0\.9\.8

<a id="minor-changes"></a>
### Minor Changes

* customer\_repo \- convert APT repository configuration to deb822 format via <code>ansible\.builtin\.deb822\_repository</code>\, replacing the legacy <code>sources\.list</code> template\.
* plugins/filter \- SPDX headers on <code>is\_pve</code> and <code>is\_uek</code> flipped from MIT to GPL\-3\.0\-or\-later for Ansible community package inclusion compliance\. <code>galaxy\.yml</code> now declares both MIT and GPL\-3\.0\-or\-later\. Modules and <code>module\_utils</code> remain MIT\.

<a id="v0-9-7"></a>
## v0\.9\.7

<a id="minor-changes-1"></a>
### Minor Changes

* customer\_repo \- drop <code>pacemaker\-3</code> from <code>default\_excludes</code> so the Pacemaker 3 repo is enabled by default\.
* customer\_repo \- optional DRBD Proxy license fetch via the new <code>linbit\_proxy\_license</code> module\, gated on <code>linbit\_cluster\_id</code> being defined and non\-empty\.

<a id="bugfixes"></a>
### Bugfixes

* public\_repo \- warn instead of failing the play on plain Debian nodes \(non\-Proxmox VE\)\, so unrelated repo configuration can proceed\.

<a id="new-modules"></a>
### New Modules

* linbit\.common\.linbit\_proxy\_license \- Fetch and write the DRBD Proxy license for a registered node\.
