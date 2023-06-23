import os

from my_node import MyNode

if __name__ == "__main__":
    node = MyNode()

    node.start()
    SHARED_FOLDER = f"{os.getcwd()}"
    node.setfiledir(SHARED_FOLDER)

    node.loadstate()
    node.connect_to("44.211.213.91")
    node.send_peers()
    file_hash = node.addfile("/home/henrique/Downloads/GramLivresContexto.pdf")
    assert file_hash == "67f1b7052a3dbf44152afbb0293eae15"
    assert (
        node.id
        == "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC3H/6oXN6P/Je4bX8udNnvs2GOe/aNk1hEtgLSwyxrJVSsd6YMm4G12mJLt+5O+l7v4u50vCPq28SSYCVRCUSDBKDNJHOdoA4eDQJDB6uQHkbH2WBbKwf5GrhfPiBsscxJ+mRkw0lUFngfaGT6L1IZMml255UzxcXXB3UE5WHdgQIDAQAB"
    )
    node.send_message(data='{"message": "Hello World!"}')
    node.send_message(data='{"message": "Hello World!"}')
    node.send_message(data='{"message": "Hello World!"}')
    node.send_message(data='{"message": "Hello World!"}')
    node.send_message(data='{"message": "Hello World!"}')
    node.savestate()

    node.stop()
