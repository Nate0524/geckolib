"""Gecko SNAME/NAMES handlers -- rename the in.touch2 WiFi module.

Reverse-engineered from in.touch2 v2.11.0's decompiled .NET IL this session --
InTouchCommand.ChangeInTouchNameCommand() sends the new name as raw bytes (GetBytesArray()
on the name string, no length prefix or fixed width visible in the IL -- just the name's own
byte length). Cosmetic-only setting, no functional risk, but included per "every setting"
scope. Untested against a real spa -- if your firmware enforces a max name length it will
presumably just reject/truncate rather than crash, but that hasn't been verified.
"""

from __future__ import annotations

import logging
import struct
from typing import Any

from geckolib.config import GeckoConfig

from .packet import GeckoPacketProtocolHandler

SNAME_VERB = b"SNAME"
NAMES_VERB = b"NAMES"

_LOGGER = logging.getLogger(__name__)


class GeckoChangeInTouchNameProtocolHandler(GeckoPacketProtocolHandler):
    """Handle SNAME/NAMES verbs -- rename the in.touch2 WiFi module."""

    @staticmethod
    def set(seq: int, name: str, **kwargs: Any) -> GeckoChangeInTouchNameProtocolHandler:
        """Generate a rename command."""
        return GeckoChangeInTouchNameProtocolHandler(
            content=b"".join(
                [SNAME_VERB, struct.pack(">B", seq), name.encode("ascii")]
            ),
            timeout=GeckoConfig.PROTOCOL_TIMEOUT_IN_SECONDS,
            on_retry_failed=GeckoPacketProtocolHandler.default_retry_failed_handler,
            **kwargs,
        )

    @staticmethod
    def set_response(**kwargs: Any) -> GeckoChangeInTouchNameProtocolHandler:
        """Generate the ack."""
        return GeckoChangeInTouchNameProtocolHandler(content=NAMES_VERB, **kwargs)

    def can_handle(self, received_bytes: bytes, _sender: tuple) -> bool:
        """Can we handle this verb."""
        return received_bytes.startswith((SNAME_VERB, NAMES_VERB))

    def handle(self, received_bytes: bytes, _sender: tuple) -> None:
        """Handle the verb."""
        if received_bytes.startswith(SNAME_VERB):
            remainder = received_bytes[5:]
            self._sequence = struct.unpack(">B", remainder[0:1])[0]
            return  # Stay in the handler list
        # Otherwise NAMES ack
        self._should_remove_handler = True
