"""
This file describes the formatting of replies in the simplenet protocol.
Those are written in a style similar to XML, albeit much simpler.

Author: Eduardo Farinati Leite
Date: 21/02/2023
"""

from enum import StrEnum
from typing import List, Self, Union

from payload import Payload


class Acks(StrEnum):
    """Enum defining possible statuses for the ACK reply to a
    status command. If the node is off, there's no reply.
    """

    UP = "Up"
    """The node is online."""

    START_UP = "StartUp"
    """The node is starting."""

    SHUTDOWN = "ShutDown"
    """The node is shutting down."""


class Replies(Payload):
    """Enum defining reply types to build and parse payloads."""

    SUBSCRIBED = "<Subscribed> {} </Subscribed>"
    """Reply to a subscribe message with a list of events
    the node subscribed to."""

    INFO = "{}"
    """Reply to an info request with the node's network info."""

    ACK = "<Ack> {} </Ack>"
    """Reply to an status request indicating the node status.
    Must be one of "Up", "StartUp" or "ShutDown".
    """

    def build(self: Self, data: Union[str, List[str]]) -> str:
        """Build a reply string according to the reply type
        formatting and valid data."""

        match self:
            case Replies.SUBSCRIBED:
                return self.format(" ".join(data))

            case Replies.ACK:
                if data not in Acks:
                    raise ValueError(
                        "Ack replies must be one of "
                        f"{[ack.value for ack in Acks]}"
                    )
                return self.format(data)

            case _:
                return self.format(data)
