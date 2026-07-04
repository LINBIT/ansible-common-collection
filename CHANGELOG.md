# Linbit\.Common Release Notes

**Topics**

- <a href="#v0-9-9">v0\.9\.9</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v0-9-8">v0\.9\.8</a>
    - <a href="#minor-changes-1">Minor Changes</a>
- <a href="#v0-9-7">v0\.9\.7</a>
    - <a href="#minor-changes-2">Minor Changes</a>
    - <a href="#bugfixes-1">Bugfixes</a>
    - <a href="#new-modules">New Modules</a>
This changelog describes changes after version 0\.9\.6\.

<a id="v0-9-9"></a>
## v0\.9\.9

<a id="release-summary"></a>
### Release Summary

Adds the <code>dkms\_kernel\_headers</code> filter plugin and the <code>zfs\_install</code> role\, alongside README and packaging metadata cleanup\.

<a id="minor-changes"></a>
### Minor Changes

* New <code>dkms\_kernel\_headers</code> filter plugin \- returns the kernel\-header packages DKMS needs to build out\-of\-tree modules for the running kernel\, selecting the correct packages per kernel flavor/edition \(generic\, aws\, cloud\-amd64\, Proxmox VE\, \.\.\.\) instead of assuming the stock or generic flavor\.
* New <code>zfs\_install</code> role \- installs OpenZFS packages and loads the <code>zfs</code> kernel module across Debian\, Ubuntu\, Red Hat family \(stock and UEK kernels\)\, and SUSE family distributions\. Extracted from <code>linbit\.linstor\.satellite\_install</code> so any collection can reuse it\.
* README \- add Authors section crediting the collection creator and pre\-collection Ansible contributors\.
* README \- add Installation section with ansible\-galaxy collection install commands and a requirements\.yml example\.
* README \- link role names in the Roles table to their per\-role README files for easier navigation\.
* README \- overhaul title and intro\: rename title to \"LINBIT Common Collection\" and rewrite the description with cross\-links to the other LINBIT Ansible collections\.
* README \- replace Dependencies section with a Requirements section listing ansible\-core prerequisites\; collection\-level dependencies are declared in galaxy\.yml\.
* README \- rewrite License section as Licensing\, with per\-file MIT/GPL\-3\.0\-or\-later coverage where applicable\.
* customer\_repo \- tidy the README\: drop trailing periods from table cells\, move the staging\-repository detail into a dedicated prose section\, and collapse the verbose variable descriptions to one line each\.
* galaxy\.yml \- point documentation URL at the GitHub repo so Galaxy renders the Documentation link to the same public\-facing source as the Repository link\.
* galaxy\.yml \- point repository and issues URLs at the public GitHub mirror so Galaxy renders contributor and issue links to the public\-facing source\.
* galaxy\.yml \- raise the <code>community\.general</code> dependency floor to <code>\>\=11\.0\.0</code> to keep it uniform across the LINBIT collections\.

<a id="bugfixes"></a>
### Bugfixes

* customer\_repo\, public\_repo \- gather minimal OS facts when they are not already present\, so the roles work when invoked with tag filters that skip the implicit fact\-gathering task or under <code>gather\_facts\: false</code>\. Without this\, fact\-dependent expressions such as the LINBIT distribution string failed with \"object of type \'dict\' has no attribute \'os\_family\'\"\.

<a id="v0-9-8"></a>
## v0\.9\.8

<a id="minor-changes-1"></a>
### Minor Changes

* customer\_repo \- convert APT repository configuration to deb822 format via <code>ansible\.builtin\.deb822\_repository</code>\, replacing the legacy <code>sources\.list</code> template\.
* plugins/filter \- SPDX headers on <code>is\_pve</code> and <code>is\_uek</code> flipped from MIT to GPL\-3\.0\-or\-later for Ansible community package inclusion compliance\. <code>galaxy\.yml</code> now declares both MIT and GPL\-3\.0\-or\-later\. Modules and <code>module\_utils</code> remain MIT\.

<a id="v0-9-7"></a>
## v0\.9\.7

<a id="minor-changes-2"></a>
### Minor Changes

* customer\_repo \- drop <code>pacemaker\-3</code> from <code>default\_excludes</code> so the Pacemaker 3 repo is enabled by default\.
* customer\_repo \- optional DRBD Proxy license fetch via the new <code>linbit\_proxy\_license</code> module\, gated on <code>linbit\_cluster\_id</code> being defined and non\-empty\.

<a id="bugfixes-1"></a>
### Bugfixes

* public\_repo \- warn instead of failing the play on plain Debian nodes \(non\-Proxmox VE\)\, so unrelated repo configuration can proceed\.

<a id="new-modules"></a>
### New Modules

* linbit\.common\.linbit\_proxy\_license \- Fetch and write the DRBD Proxy license for a registered node\.
