# SPDX-License-Identifier: MIT
"""Filter plugins for kernel detection."""


class FilterModule:
    """Kernel detection filters."""

    def filters(self):
        return {
            'is_pve': self.is_pve,
            'is_uek': self.is_uek,
        }

    @staticmethod
    def is_pve(facts):
        """Return True when running on a Proxmox VE kernel."""
        return 'pve' in facts.get('kernel', '')

    @staticmethod
    def is_uek(facts):
        """Return True when running on an Oracle Linux UEK kernel."""
        return 'uek' in facts.get('kernel', '')
