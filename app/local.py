import os

from p2p import node

if __name__ == "__main__":
    node.start()
    SHARED_FOLDER = f"{os.getcwd()}"
    node.setfiledir(SHARED_FOLDER)

    # node.loadstate()
    node.connect_to("3.225.100.86")
    node.send_peers()
    file_hash = node.addfile("/home/henrique/Downloads/GramLivresContexto.pdf")
    assert file_hash == "67f1b7052a3dbf44152afbb0293eae15"
    node.send_message(data='{"message": "Hello World!"}')
    node.send_message(data='{"message": "Hello World!"}')
    node.send_message(data='{"message": "Hello World!"}')
    node.send_message(data='{"message": "Hello World!"}')
    node.send_message(data='{"message": "Hello World!"}')
    node.savestate()

    node.stop()
