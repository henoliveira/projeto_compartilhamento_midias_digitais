from pythonp2p import Node as _Node
from schemas import Nodes, db_session


class Node(_Node):
    def on_message(self, message, sender, private):
        # Gets called everytime there is a new message
        print(message)
        print(self.peers)

    @property
    def connected_nodes(self):
        return [node.host for node in self.nodes_connected]

    # def ConnectToNodes(self):
    #     for i in self.peers:
    #         if not self.connect_to(i, self.port) and i not in self.connected_nodes:
    #             del self.peers[self.peers.index(i)]  # delete wrong / own ip from peers

    # def loadstate(self):
    #     database_peers = [node.ip for node in Nodes.select()]
    #     for i in database_peers:
    #         self.connect_to(i)

    # @db_session
    # def savestate(self):
    #     database_peers: list[str] = [node.ip for node in Nodes.select()]
    #     active_peers = self.peers

    #     for peer in self.peers:
    #         if peer not in database_peers:
    #             Nodes(ip=peer)


node = Node(host="0.0.0.0")
