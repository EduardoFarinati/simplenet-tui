"""
This file describes classes relating to definition a node running within
the simplenet network protocol.

Author: Eduardo Farinati Leite
Date: 20/02/2023
"""

from dataclasses import dataclass
import socket
from typing import List, Tuple


@dataclass(slots=True)
class NodeConfig:
    """Class to describe a simplenet node's configuration."""

    info: str
    address: Tuple[str, int]
    input_events: List[str]
    output_events: List[str]


@dataclass(slots=True)
class Network:
    """Class to describe a simplenet network."""

    name: str
    addresses: List[Tuple[str, int]]
    broadcast_address: str


@dataclass(slots=True)
class Node:
    """Class to handle data and functions of a simplenet node."""

    name: str
    config: NodeConfig
    network: Network
    servers: List[socket.socket]
    clients: List[socket.socket]

    def connect_to_servers(self):
        server_addresses = [
            address
            for address in self.network.addresses
            if address != self.config.address
        ]

        for address in server_addresses:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.connect(address)
            self.servers.append(tcp_socket)
