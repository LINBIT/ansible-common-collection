# SPDX-License-Identifier: MIT
"""Filter plugin for Proxmox VE detection."""


class FilterModule:
    """Proxmox VE detection filters."""

    def filters(self):
        return {'is_pve': self.is_pve}

    @staticmethod
    def is_pve(facts):
        """Return True when running on a Proxmox VE kernel."""
        return 'pve' in facts.get('kernel', '')
