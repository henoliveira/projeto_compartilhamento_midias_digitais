from pythonp2p import Node


class MyNode(Node):
    def on_message(self, message, sender, private):
        # Gets called everytime there is a new message
        print(message)

    @property
    def connected_nodes(self):
        return [node.host for node in self.nodes_connected]

    def ConnectToNodes(self):
        for i in self.peers:
            if not self.connect_to(i, self.port) and i not in self.connected_nodes:
                del self.peers[self.peers.index(i)]  # delete wrong / own ip from peers
