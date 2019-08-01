import json
import socks
from bisbasic.connections import send, receive
from bisbasic.essentials import format_raw_tx
from diff_simple import difficulty
import time

class Socket():
    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.s = socks.socksocket()
            self.s.connect(("127.0.0.1", 5658))
        except:
            raise

    def get_txid(self, txid):
        self.connect()
        responded = False
        while not responded:
            try:
                send(self.s, "api_gettransaction")
                send(self.s, txid)

                reply = receive(self.s)
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
                send(self.s, "api_getaddressrange")
                send(self.s, address)
                send(self.s, 0)
                send(self.s, 100)

                reply = receive(self.s)
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
                send(self.s, "statusjson")
                reply = receive(self.s, timeout=1)
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
                send(self.s, "api_getblockfromhash")
                send(self.s, hash)
                reply = receive(self.s, timeout=1)
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
                send(self.s, "api_getblockfromheight")
                send(self.s, height)
                reply = receive(self.s, timeout=1)
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
                send(self.s, "api_getblockrange")
                send(self.s, block)
                send(self.s, limit)

                reply = receive(self.s, timeout=1)

                if not reply == "*":
                    responded = True
                    return reply

            except Exception as e:
                print(f"Error: {e}")
                self.connect()


class Status():
    def refresh(self, socket):

        self.status = socket.get_status()

        #non-chartable instants
        self.protocolversion = self.status['protocolversion']
        self.address = self.status['address']
        self.testnet = self.status['testnet']
        self.timeoffset = self.status['timeoffset']
        self.connections_list = self.status['connections_list']
        self.uptime = self.status['uptime']
        self.server_timestamp = self.status['server_timestamp']

        #chartable instants
        self.connections = self.status['connections']
        self.threads = self.status['threads']
        self.consensus = self.status['consensus']
        self.consensus_percent = self.status['consensus_percent']

        #non-instants
        self.difficulty = self.status['difficulty']
        self.blocks = self.status['blocks']

        #self.diffstatus = socket.get_diff()

        #instants from diffget
        #self.diff_dropped = self.diffstatus['diff_dropped']
        #self.time_to_generate = self.diffstatus['time_to_generate']
        #self.block_time = self.diffstatus['block_time']
        #self.diff_adjustment = self.diffstatus['diff_adjustment']
        #self.hashrate = self.diffstatus['hashrate']

        return self.status

class History():
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

class DiffCalculator():
    @staticmethod
    def calculate(diff_blocks, diff_blocks_minus_1440, block : str, block_minus_1 : str, block_minus_1440 : str):
        try:
            print("Calculating difficulty")
            print("diff_blocks", diff_blocks)

            last_block_timestamp = diff_blocks[block]["mining_tx"]["timestamp"]
            block_minus_1_timestamp = diff_blocks[block_minus_1]["mining_tx"]["timestamp"]
            block_minus_1_difficulty = diff_blocks[block_minus_1]["mining_tx"]["difficulty"]
            block_minus_1441_timestamp = diff_blocks_minus_1440[block_minus_1440]["mining_tx"]["difficulty"]

            diff = difficulty(float(last_block_timestamp),float(block_minus_1_timestamp), float(block_minus_1_difficulty),float(block_minus_1441_timestamp))
            return {block : diff}

        except Exception as e:
            print(f"issue with {e}")
            raise

class Updater():
    def __init__(self):
        self.status = Status()
        self.history = History()
        self.last_block = 0

    def update(self):
        self.socket = Socket()

        new_data = self.status.refresh(self.socket)

        self.history.stata.append([new_data])
        self.last_block = new_data["blocks"]

        self.history.blocks = json.loads(self.socket.get_getblockrange(self.status.blocks -50, 50))
        print (self.history.blocks) #last block

        self.history.truncate()


        for number in range (-50,0):
            #difficulty

            diff_blocks = json.loads(self.socket.get_getblockrange(self.status.blocks + number, 2)) # number is negative
            diff_blocks_minus_1440 = json.loads(self.socket.get_getblockrange(self.status.blocks - 1440 + number, 1)) # number is negative

            self.history.diffs.append(DiffCalculator.calculate(diff_blocks, diff_blocks_minus_1440, str(self.status.blocks + number + 1), str(self.status.blocks + number), str(self.status.blocks - 1440 + number)))
            #/difficulty

        print(self.history.blocks)
        print(self.history.diffs)

if __name__ == "__main__":
    updater = Updater()