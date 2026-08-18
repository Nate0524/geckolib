"""Gecko CURCH/CHCUR/CHACH/CHCHA handlers.

CHACH/CHCHA (RF channel write) reverse-engineered from in.touch2 v2.11.0's decompiled .NET IL
this session -- InTouchCommand.ChangeRFChannel() builds a 1-byte payload (the new channel
number) with an extended 5000ms retry delay (vs. the usual 800-1500ms -- channel changes
apparently take the spa longer to apply/ack than most commands).
"""

from __future__ import annotations

import logging
import struct
from typing import Any

from geckolib.config import GeckoConfig

from .packet import GeckoPacketProtocolHandler

CURCH_VERB = b"CURCH"
CHCUR_VERB = b"CHCUR"
CHACH_VERB = b"CHACH"
CHCHA_VERB = b"CHCHA"
GETCHANNEL_FORMAT = ">BB"
SET_CHANNEL_RETRY_DELAY_MS = 5000  # confirmed from ChangeRFChannel() IL; longer than default

_LOGGER = logging.getLogger(__name__)


class GeckoGetChannelProtocolHandler(GeckoPacketProtocolHandler):
    """Handle CURCH/CHCUR verbs."""

    @staticmethod
    def request(seq: int, **kwargs: Any) -> GeckoGetChannelProtocolHandler:
        """Generate request."""
        return GeckoGetChannelProtocolHandler(
            content=b"".join([CURCH_VERB, struct.pack(">B", seq)]),
            timeout=GeckoConfig.PROTOCOL_TIMEOUT_IN_SECONDS,
            on_retry_failed=GeckoPacketProtocolHandler.default_retry_failed_handler,
            **kwargs,
        )

    @staticmethod
    def response(
        channel: int, signal_strength: int, **kwargs: Any
    ) -> GeckoGetChannelProtocolHandler:
        """Generate response."""
        return GeckoGetChannelProtocolHandler(
            content=b"".join(
                [
                    CHCUR_VERB,
                    struct.pack(
                        GETCHANNEL_FORMAT,
                        channel,
                        signal_strength,
                    ),
                ]
            ),
            **kwargs,
        )

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the class."""
        super().__init__(**kwargs)
        self.channel = self.signal_strength = None

    def can_handle(self, received_bytes: bytes, _sender: tuple) -> bool:
        """Can we handle this verb."""
        return received_bytes.startswith((CURCH_VERB, CHCUR_VERB))

    def handle(self, received_bytes: bytes, _sender: tuple) -> None:
        """Handle the verb."""
        remainder = received_bytes[5:]
        if received_bytes.startswith(CURCH_VERB):
            self._sequence = struct.unpack(">B", remainder)[0]
            return  # Stay in the handler list
        # Otherwise must be CHCUR
        (
            self.channel,
            self.signal_strength,
        ) = struct.unpack(GETCHANNEL_FORMAT, remainder)
        self._should_remove_handler = True


class GeckoChangeChannelProtocolHandler(GeckoPacketProtocolHandler):
    """Handle CHACH/CHCHA verbs -- write a new RF channel."""

    @staticmethod
    def set(seq: int, channel: int, **kwargs: Any) -> GeckoChangeChannelProtocolHandler:
        """Generate a change-channel command."""
        return GeckoChangeChannelProtocolHandler(
            content=b"".join(
                [CHACH_VERB, struct.pack(">B", seq), struct.pack(">B", channel)]
            ),
            timeout=GeckoConfig.PROTOCOL_TIMEOUT_IN_SECONDS,
            retry_delay=SET_CHANNEL_RETRY_DELAY_MS / 1000,
            on_retry_failed=GeckoPacketProtocolHandler.default_retry_failed_handler,
            **kwargs,
        )

    @staticmethod
    def set_response(**kwargs: Any) -> GeckoChangeChannelProtocolHandler:
        """Generate the ack."""
        return GeckoChangeChannelProtocolHandler(content=CHCHA_VERB, **kwargs)

    def can_handle(self, received_bytes: bytes, _sender: tuple) -> bool:
        """Can we handle this verb."""
        return received_bytes.startswith((CHACH_VERB, CHCHA_VERB))

    def handle(self, received_bytes: bytes, _sender: tuple) -> None:
        """Handle the verb."""
        if received_bytes.startswith(CHACH_VERB):
            remainder = received_bytes[5:]
            self._sequence = struct.unpack(">B", remainder[0:1])[0]
            return  # Stay in the handler list
        # Otherwise CHCHA ack
        self._should_remove_handler = True
