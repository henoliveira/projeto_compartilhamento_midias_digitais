from p2p import node

if __name__ == "__main__":
    node.ip = "44.211.213.91"
    node.start()

    node.loadstate()
    node.connect_to("179.108.22.7")
    node.savestate()
