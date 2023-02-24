"""
This file describes the formatting of messages in the simplenet protocol.
Those are written in a style similar to XML, albeit much simpler.

Author: Eduardo Farinati Leite
Date: 21/02/2023
"""

from enum import StrEnum
from typing import List, Self, Union

from payload import Payload


class Commands(StrEnum):
    """Enum defining possible commands for the Cmd message."""

    INFO = "Info"
    """Request the network info recorded in the node."""

    STATUS = "Status"
    """Request the node's status."""

    RESET_REQUEST = "ResetRequest"
    """Request a reset to the node."""


class MessageTypes(StrEnum):
    """Enum defining message types of payloads."""

    SUBSCRIBE = "<Subscribe> {} </Subscribe>"
    """Subscribe to notifications regarding a list of events."""

    COMMAND = "<Cmd> {} </Cmd>"
    """Commands representing a request to the node.
    Must be one of "Info", "Status" or "ResetRequest".
    """

    NOTIFY = "<Notify> {} </Notify>"
    """Notify a subscribed node of an event occurrence."""

    COMMENT = "% {}"
    """Send a comment to a node. Should be ignored in most cases."""

    def build(self: Self, data: Union[str, List[str]]) -> str:
        """Build a message string according to the message
        type formatting."""

        match self:
            case Messages.SUBSCRIBE:
                return self.format(" ".join(data))

            case Messages.COMMAND:
                if data not in Commands:
                    raise ValueError(
                        "Command messages must be one of "
                        f"{[command.value for command in Commands]}"
                    )
                return self.format(data)

            case _:
                return self.format(data)
