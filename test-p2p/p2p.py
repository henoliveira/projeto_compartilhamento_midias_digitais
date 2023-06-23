from pythonp2p import Node


class MyNode(Node):
    def on_message(message, sender, private):
        # Gets called everytime there is a new message
        print(message)


node = MyNode()
node.start()

# node.connect_to("44.211.213.91")
# node.savestate()
# node.loadstate()
# node.send_message({"msg": "Oi do Xonha"}, "44.211.213.91")
