import json
from bismuthclient.rpcconnections import Connection
from diff_simple import difficulty
import psutil


class Socket:
    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.connection = Connection(("127.0.0.1", 5658))
        except:
            raise

    def get_txid(self, txid):
        self.connect()
        responded = False
        while not responded:
            try:
                self.connection._send("api_gettransaction")
                self.connection._send(txid)

                reply = self.connection._receive()
                if not reply == "*":
                    responded = True
                    return reply
            except Exception as e:
                print(f"Error: {e}")
                self.connect()

    def get_address(self, address):
        responded = False
        while not responded:
            try:
                self.connection._send("api_getaddressrange")
                self.connection._send(address)
                self.connection._send(0)
                self.connection._send(100)

                reply = self.connection._receive()
                if not reply == "*":
                    responded = True
                    return reply
            except Exception as e:
                print(f"Error: {e}")
                self.connect()

    def get_status(self):
        responded = False
        while not responded:
            try:
                self.connection._send("statusjson")
                reply = self.connection._receive()
                if not reply == "*":
                    responded = True
                    return reply
            except Exception as e:
                print(f"Error: {e}")
                self.connect()

    def get_blockfromhash(self, hash):
        responded = False
        while not responded:
            try:
                self.connection._send("api_getblockfromhash")
                self.connection._send(hash)
                reply = self.connection._receive()
                if not reply == "*":
                    responded = True
                    return reply
            except Exception as e:
                print(f"Error: {e}")
                self.connect()

    def get_blockfromheight(self, height):
        responded = False
        while not responded:
            try:
                self.connection._send("api_getblockfromheight")
                self.connection._send(height)
                reply = self.connection._receive()
                if not reply == "*":
                    responded = True
                    return reply

            except Exception as e:
                print(f"Error: {e}")
                self.connect()

    def get_getblockrange(self, block, limit):
        responded = False
        while not responded:
            try:
                self.connection._send("api_getblockrange")
                self.connection._send(block)
                self.connection._send(limit)

                reply = self.connection._receive()

                if not reply == "*":
                    responded = True
                    return reply

            except Exception as e:
                print(f"Error: {e}")
                self.connect()


class Status:
    def refresh(self, socket):
        self.status = socket.get_status()

        # non-chartable instants
        self.protocolversion = self.status['protocolversion']
        self.address = self.status['address']
        self.testnet = self.status['testnet']
        self.timeoffset = self.status['timeoffset']
        self.connections_list = self.status['connections_list']
        self.uptime = self.status['uptime']
        self.server_timestamp = self.status['server_timestamp']

        # chartable instants
        self.connections = self.status['connections']
        self.threads = self.status['threads']
        self.consensus = self.status['consensus']
        self.consensus_percent = self.status['consensus_percent']

        # non-instants
        self.difficulty = self.status['difficulty']
        self.blocks = self.status['blocks']
        return self.status


class History:
    """saves status calls and the last block range call"""

    def __init__(self):
        self.blocks = []
        self.stata = []
        self.diffs = []

    def truncate(self):
        if len(self.stata) >= 50:
            self.stata = self.stata[-50:]

        if len(self.diffs) >= 50:
            self.diffs = self.diffs[50:]


class DiffCalculator:
    @staticmethod
    def calculate(diff_blocks, diff_blocks_minus_1440, block: str, block_minus_1: str, block_minus_1440: str):
        try:
            print("Calculating difficulty")
            print("diff_blocks", diff_blocks)

            last_block_timestamp = diff_blocks[block]["mining_tx"]["timestamp"]
            block_minus_1_timestamp = diff_blocks[block_minus_1]["mining_tx"]["timestamp"]
            block_minus_1_difficulty = diff_blocks[block_minus_1]["mining_tx"]["difficulty"]
            block_minus_1441_timestamp = diff_blocks_minus_1440[block_minus_1440]["mining_tx"]["difficulty"]

            diff = difficulty(float(last_block_timestamp),
                              float(block_minus_1_timestamp),
                              float(block_minus_1_difficulty),
                              float(block_minus_1441_timestamp))

            return {block: diff}

        except Exception as e:
            print(f"issue with {e}")
            raise


class Updater:
    def __init__(self):
        self.status = Status()
        self.history = History()
        self.last_block = 0

    def update(self):
        try:
            self.socket = Socket()

            new_data = self.status.refresh(self.socket)


            local_data = {}
            local_data["memory"] = dict(psutil.virtual_memory()._asdict())["percent"]
            local_data["cpu_usage"] = psutil.cpu_percent(3)
            new_data["local_data"] = local_data

            self.history.stata.append([new_data])
            self.last_block = new_data["blocks"]

            self.history.blocks = json.loads(self.socket.get_getblockrange(self.status.blocks - 50, 50))
            print(self.history.blocks)  # last block

            self.history.truncate()

            for number in range(-50, 0):
                # difficulty

                diff_blocks = json.loads(self.socket.get_getblockrange(self.status.blocks + number, 2))  # number is negative
                diff_blocks_minus_1440 = json.loads(self.socket.get_getblockrange(self.status.blocks - 1440 + number, 1))  # number is negative

                self.history.diffs.append(DiffCalculator.calculate(diff_blocks, diff_blocks_minus_1440,
                                                                   str(self.status.blocks + number + 1),
                                                                   str(self.status.blocks + number),
                                                                   str(self.status.blocks - 1440 + number)))
                # /difficulty

            print(self.history.blocks)
            print(self.history.diffs)

        except Exception as e:
            print(f"An error occured during update, skipping ({e})")


if __name__ == "__main__":
    updater = Updater()
