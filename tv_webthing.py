import sys
import logging
import tornado.ioloop
from webthing import (SingleThing, Property, Thing, Value, WebThingServer)
from tv import Tv



class TvThing(Thing):

    # regarding capabilities refer https://iot.mozilla.org/schemas
    # there is also another schema registry http://iotschema.org/docs/full.html not used by webthing

    def __init__(self, tv: Tv):
        Thing.__init__(
            self,
            'urn:dev:ops:tvSensor-1',
            'TV',
            ['MultiLevelSensor'],
            "tv sensor"
        )

        self.tv = tv
        self.tv.set_listener(self.on_value_changed)
        self.ioloop = tornado.ioloop.IOLoop.current()

        self.audio = Value(self.tv.audio, self.tv.set_audio)
        self.add_property(
            Property(self,
                     'audio',
                     self.audio,
                     metadata={
                         'title': 'audio',
                         'type': 'string',
                         'description': 'The selected audio output',
                         'readOnly': False,
                     }))



    def on_value_changed(self):
        self.ioloop.add_callback(self.__on_value_changed)

    def __on_value_changed(self):
        self.audio.notify_of_external_update(self.tv.audio)


def run_server(port: int, ip_address: str, dir: str):
    tv = Tv(ip_address, dir)
    server = WebThingServer(SingleThing(TvThing(tv)), port=port, disable_host_validation=True)
    try:
        logging.info('starting the server http://localhost:' + str(port) + " (ip address=" + ip_address + ")")
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        tv.stop()
        server.stop()
        logging.info('done')


if __name__ == '__main__':
    try:
        logging.basicConfig(format='%(asctime)s %(name)-20s: %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
        logging.getLogger('tornado.access').setLevel(logging.ERROR)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
        run_server(int(sys.argv[1]), sys.argv[2], sys.argv[3])
    except Exception as e:
        logging.error(str(e))
        raise e





# test curl
# curl -X PUT -d '{"audio": 'arc'}' http://127.0.0.1:8989/properties/audio


