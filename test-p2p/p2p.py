from my_node import MyNode

if __name__ == "__main__":
    node = MyNode()
    node.ip = "179.108.22.7"
    node.start()

    node.loadstate()
    # node.connect_to("44.211.213.91")
    node.send_peers()
    node.send_message(data='{"message": "Hello World!"}')
    node.send_message(data='{"message": "Hello World!"}')
    node.send_message(data='{"message": "Hello World!"}')
    node.send_message(data='{"message": "Hello World!"}')
    node.send_message(data='{"message": "Hello World!"}')
    node.savestate()

    node.stop()
