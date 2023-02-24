from asyncio.trsock import _RetAddress
import socketserver
from typing import Self, List


class ServerTCPHandler(socketserver.StreamRequestHandler):
    """Request handler for the simplenet server.

    It should handle tcp connections from most if not all
    other nodes in the network, replying to commands and
    notifying them of subscribed events.
    """

    def handle(self: Self):
        print(f"Node {self.client_address} is up")

        # Receive a message from the client
        while data := self.rfile.readline():
            # Answer with a reply
            self.wfile.write(data)

        # Connection closed
        print(f"Node {self.client_address} is shutting down")


class SimpleNetTCPServer(socketserver.ThreadingTCPServer):
    """TCP server for the simplenet protocol.

    It should accept tcp connections from nodes listed in the
    network configuration, handling requests when needed.
    """

    def __init__(
        self: Self,
        node_addresses: List[str],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.node_addresses = node_addresses

    def verify_request(
        self: Self,
        request: socketserver._RequestType,
        client_address: _RetAddress,
    ) -> bool:
        """Test if the client's ip address is inside the node's
        ip address list defined in the network configuration."""
        ip, _ = client_address
        return ip in self.node_addresses and super().verify_request(
            request, client_address
        )


if __name__ == "__main__":
    HOST, PORT = "", 8080
    with SimpleNetTCPServer(
        [HOST],
        (HOST, PORT),
        ServerTCPHandler,
    ) as server:
        server.serve_forever()
