from pythonp2p import Node


class MyNode(Node):
    def on_message(self, message, sender, private):
        # Gets called everytime there is a new message
        print(message)


if __name__ == "__main__":
    node = Node()
    node.start()

    # res = node.connect_to("44.211.213.91")
    # node.send_message(data={"message": "Hello World!"})
    # node.savestate()
    # node.loadstate()
