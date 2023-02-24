"""
This file describes an abstract class for the construction of
simplenet protocol payloads (messages or replies).
Those are written in a style similar to XML, albeit much simpler.

Author: Eduardo Farinati Leite
Date: 21/02/2023
"""

from abc import ABC, abstractmethod
from enum import StrEnum
from typing import List, Self, Union
import re


class Payload(ABC):
    """Abstract class defining methods required to build payloads."""

    @abstractmethod
    def __init__(self, data: Union[str, List[str]]):
        pass

    @staticmethod
    @abstractmethod
    def types() -> StrEnum:
        raise NotImplementedError()

    @property
    def data(self) -> Union[str, List[str]]:
        return self.data

    @classmethod
    def from_bytes(cls, payload: bytes) -> Self:
        return cls()

    @abstractmethod
    def to_bytes(self) -> bytes:
        pass
