import tornado.ioloop
import time

import tornado.ioloop
import tornado.web
import threading
import dator

def txid_from_sig(sig):
    return sig[:56]

class seekHandler(tornado.web.RequestHandler):
    def initialize(self, updater):
        self.updater = updater
        # self.updater.update()

    def get(self, data):
        # call fetcher
        # self.updater.update()

        query = seekHandler.get_argument(self, "query")
        print(f"Query: {query}, {type(query)}, {len(query)}")

        socket = dator.Socket()

        try:
            if query.strip() == "":
                self.write("Nothing entered")
                return

            if query.isnumeric():

                result = socket.get_blockfromheight(query)
                self.render("address.html",
                            data=result)
            elif query.lower() != query:
                print("txid")
                result = socket.get_txid(query)
                if result:
                    self.render("txid.html",
                                data=result)
            else:
                result = socket.get_blockfromhash(query)
                if result:
                    print(result)
                    self.render("address.html",
                                data=result)

                result = socket.get_address(query)
                if result:
                    print(result)
                    self.render("address.html",
                                data=result)

        except Exception as e:
            self.write(f"Request not recognized ({e})")

        # render
        """
        socket = dator.Socket()
        result = socket.get_blockfromheight(height)

        self.render("address.html",
                    data = result)
        """


class heightHandler(tornado.web.RequestHandler):
    def initialize(self, updater):
        self.updater = updater
        # self.updater.update()

    def get(self, height):
        # call fetcher
        # self.updater.update()

        # render

        socket = dator.Socket()
        result = socket.get_blockfromheight(height)

        self.render("address.html",
                    data=result)


class txidHandler(tornado.web.RequestHandler):
    def initialize(self, updater):
        self.updater = updater
        # self.updater.update()

    def get(self, txid):
        # call fetcher
        # self.updater.update()

        # render

        socket = dator.Socket()
        result = socket.get_txid(txid)

        self.render("txid.html",
                    data=result)


class hashHandler(tornado.web.RequestHandler):
    def initialize(self, updater):
        self.updater = updater
        # self.updater.update()

    def get(self, hash):
        # call fetcher
        # self.updater.update()

        # render

        socket = dator.Socket()
        result = socket.get_blockfromhash(hash)

        self.render("address.html",
                    data=result)


class addressHandler(tornado.web.RequestHandler):
    def initialize(self, updater):
        self.updater = updater
        # self.updater.update()

    def get(self, address):
        # call fetcher
        # self.updater.update()

        # render

        socket = dator.Socket()
        result = socket.get_address(address)

        self.render("address.html",
                    data=result)


class blockdisplayHandler(tornado.web.RequestHandler):
    def initialize(self, updater):
        self.updater = updater
        # self.updater.update()

    def get(self):
        # call fetcher
        # self.updater.update()

        # render

        s = reversed(sorted(self.updater.history.blocks.items()))

        self.render("explorer.html",
                    data=s, txid_from_sig=txid_from_sig)


class difficultyHandler(tornado.web.RequestHandler):
    def initialize(self, updater):
        self.updater = updater
        # self.updater.update()

    def get(self):
        # call fetcher
        # self.updater.update()

        # render

        y_axis = []
        x_axis = []

        for block, data in self.updater.history.blocks.items():
            print(block)
            print(data)

            x_axis.append(int(block))
            y_axis.append(float(data['mining_tx']['difficulty']))

        self.render("chart.html",
                    y_axis=y_axis,
                    x_axis=x_axis,
                    y_label="Difficulty",
                    x_label="Block")


class block_timestampsHandler(tornado.web.RequestHandler):
    def initialize(self, updater):
        self.updater = updater
        # self.updater.update()

    def get(self):
        # call fetcher
        # self.updater.update()

        # render

        y_axis = []
        x_axis = []

        for block, data in self.updater.history.blocks.items():
            x_axis.append(int(block))
            y_axis.append(float(data['mining_tx']['timestamp']))

        self.render("chart.html",
                    y_axis=y_axis,
                    x_axis=x_axis,
                    y_label="Timestamp",
                    x_label="Block")


class tx_timestampsHandler(tornado.web.RequestHandler):
    def initialize(self, updater):
        self.updater = updater
        # self.updater.update()

    def get(self):
        # call fetcher
        # self.updater.update()

        # render

        y_axis = []
        x_axis = []

        for block, data in self.updater.history.blocks.items():
            print(block)
            print(data)

            x_axis.append(int(block))
            for transaction in data['transactions']:
                y_axis.append(float(transaction['timestamp']))

        self.render("chart.html",
                    y_axis=y_axis,
                    x_axis=x_axis,
                    y_label="Timestamp",
                    x_label="Block")


class connectionsHandler(tornado.web.RequestHandler):
    def initialize(self, updater):
        self.updater = updater
        # self.updater.update()

    def get(self):
        # call fetcher
        # self.updater.update()

        # render

        y_axis = []
        x_axis = []

        for x in range(len(self.updater.history.stata)):
            x_axis.append(int(x))

        for items in self.updater.history.stata:
            for subitem in items:
                y_axis.append(subitem['connections'])

        self.render("chart.html",
                    y_axis=y_axis,
                    x_axis=x_axis,
                    y_label="Connections",
                    x_label="Interval")


class consensusHandler(tornado.web.RequestHandler):
    def initialize(self, updater):
        self.updater = updater
        # self.updater.update()

    def get(self):
        # call fetcher
        # self.updater.update()

        # render

        y_axis = []
        x_axis = []

        for x in range(len(self.updater.history.stata)):
            x_axis.append(int(x))

        for items in self.updater.history.stata:
            for subitem in items:
                y_axis.append(subitem['consensus'])

        self.render("chart.html",
                    y_axis=y_axis,
                    x_axis=x_axis,
                    y_label="Consensus",
                    x_label="Interval")


class consensus_percentHandler(tornado.web.RequestHandler):
    def initialize(self, updater):
        self.updater = updater
        # self.updater.update()

    def get(self):
        # call fetcher
        # self.updater.update()

        # render

        y_axis = []
        x_axis = []

        for x in range(len(self.updater.history.stata)):
            x_axis.append(int(x))

        for items in self.updater.history.stata:
            for subitem in items:
                y_axis.append(subitem['consensus_percent'])

        self.render("chart.html",
                    y_axis=y_axis,
                    x_axis=x_axis,
                    y_label="Consensus Percentage",
                    x_label="Interval")


class threadsHandler(tornado.web.RequestHandler):
    def initialize(self, updater):
        self.updater = updater
        # self.updater.update()

    def get(self):
        # call fetcher
        # self.updater.update()

        # render

        y_axis = []
        x_axis = []

        for x in range(len(self.updater.history.stata)):
            x_axis.append(int(x))

        for items in self.updater.history.stata:
            for subitem in items:
                y_axis.append(subitem['threads'])

        self.render("chart.html",
                    y_axis=y_axis,
                    x_axis=x_axis,
                    y_label="Threads",
                    x_label="Interval")


class diff_droppedHandler(tornado.web.RequestHandler):
    def initialize(self, updater):
        self.updater = updater
        # self.updater.update()

    def get(self):
        # call fetcher
        # self.updater.update()

        # render

        y_axis = []
        x_axis = []

        for item in self.updater.history.diffs:
            for block, difficulty in item.items():
                x_axis.append(int(block))

        for item in self.updater.history.diffs:
            for block, difficulty in item.items():
                y_axis.append(difficulty['diff_dropped'])

        self.render("chart.html",
                    y_axis=y_axis,
                    x_axis=x_axis,
                    y_label="Difficulty After Readjustment",
                    x_label="Block")


class time_to_generateHandler(tornado.web.RequestHandler):
    def initialize(self, updater):
        self.updater = updater
        # self.updater.update()

    def get(self):
        # call fetcher
        # self.updater.update()

        # render

        y_axis = []
        x_axis = []

        for item in self.updater.history.diffs:
            for block, difficulty in item.items():
                x_axis.append(int(block))

        for item in self.updater.history.diffs:
            for block, difficulty in item.items():
                y_axis.append(difficulty['time_to_generate'])

        self.render("chart.html",
                    y_axis=y_axis,
                    x_axis=x_axis,
                    y_label="Seconds",
                    x_label="Block")


class diff_adjustmentHandler(tornado.web.RequestHandler):
    def initialize(self, updater):
        self.updater = updater
        # self.updater.update()

    def get(self):
        # call fetcher
        # self.updater.update()

        # render

        y_axis = []
        x_axis = []

        for item in self.updater.history.diffs:
            for block, difficulty in item.items():
                x_axis.append(int(block))

        for item in self.updater.history.diffs:
            for block, difficulty in item.items():
                y_axis.append(difficulty['diff_adjustment'])

        self.render("chart.html",
                    y_axis=y_axis,
                    x_axis=x_axis,
                    y_label="Difficulty Readjustment",
                    x_label="Block")


class hashrateHandler(tornado.web.RequestHandler):
    def initialize(self, updater):
        self.updater = updater
        # self.updater.update()

    def get(self):
        # call fetcher
        # self.updater.update()

        y_axis = []
        x_axis = []

        for item in self.updater.history.diffs:
            for block, difficulty in item.items():
                x_axis.append(int(block))

        for item in self.updater.history.diffs:
            for block, difficulty in item.items():
                y_axis.append(difficulty['hashrate'])

        self.render("chart.html",
                    y_axis=y_axis,
                    x_axis=x_axis,
                    y_label="Hashrate",
                    x_label="Block")


class statsHandler(tornado.web.RequestHandler):
    def initialize(self, updater):
        self.updater = updater
        # self.updater.update()

    def get(self):
        # call fetcher
        # self.updater.update()

        self.render("stats.html",
                    stata=self.updater.history.stata
                    )


def make_app():
    return tornado.web.Application([
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
        (r"/explorer", blockdisplayHandler, {'updater': updater}),
        (r"/explorer/address/(.*)", addressHandler, {'updater': updater}),
        (r"/explorer/hash/(.*)", hashHandler, {'updater': updater}),
        (r"/explorer/height/(.*)", heightHandler, {'updater': updater}),
        (r"/explorer/txid/(.*)", txidHandler, {'updater': updater}),
        (r"/difficulty", difficultyHandler, {'updater': updater}),
        (r"/block_timestamps", block_timestampsHandler, {'updater': updater}),
        (r"/tx_timestamps", tx_timestampsHandler, {'updater': updater}),
        (r"/connections", connectionsHandler, {'updater': updater}),
        (r"/consensus", consensusHandler, {'updater': updater}),
        (r"/consensus_percent", consensus_percentHandler, {'updater': updater}),
        (r"/threads", threadsHandler, {'updater': updater}),
        (r"/diff_dropped", diff_droppedHandler, {'updater': updater}),
        (r"/time_to_generate", time_to_generateHandler, {'updater': updater}),
        (r"/diff_adjustment", diff_adjustmentHandler, {'updater': updater}),
        (r"/hashrate", hashrateHandler, {'updater': updater}),
        (r"/", statsHandler, {'updater': updater}),
        (r"/explorer/seek(.*)", seekHandler, {'updater': updater}),

    ])


class ThreadedClient(threading.Thread):
    def __init__(self, updater):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            updater.update()
            time.sleep(360)


if __name__ == "__main__":
    updater = dator.Updater()

    background = ThreadedClient(updater)
    background.start()

    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
