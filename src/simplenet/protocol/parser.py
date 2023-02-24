import re
from typing import List, Tuple, Union
import warnings


from payload import Payload
from messages import Messages
from replies import Replies


MESSAGE_MAPPING = tuple(
    (re.compile(_type.replace("{}", "(.*)")), _type)
    for _type in Messages
)

REPLY_MAPPING = tuple(
    (re.compile(_type.replace("{}", "(.*)")), _type)
    for _type in Replies
)

Mapping = Tuple[Tuple[re.Pattern, Payload]]
ParsedPayload = Union[Tuple[Union[str, List[str]], Payload], None]


def parse(raw: str, payload_mapping: Mapping) -> ParsedPayload:
    for mapping, _type in payload_mapping:
        if data := mapping.match(raw):
            return (_type.parse_raw_data(data.string), _type)

    warnings.warn(f'Payload "{raw}" ignored, unknown format.')
    return None


def parse_message(raw: str) -> ParsedPayload:
    return parse(raw, MESSAGE_MAPPING)


def parse_reply(raw: str) -> ParsedPayload:
    return parse(raw, REPLY_MAPPING)
