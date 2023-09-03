import zmq

port = "5555"
class ZmqMsgs:
    def __init__(self) -> None:
        self.context = zmq.Context()
        self.socket=None
        
    def connect(self):
        self.socket.connect("tcp://127.0.0.1:5555")
        print("connected to zmq")
    def send(self,msg:str)->None:
        #self.socket.send_string("tsfeeder",zmq.SNDMORE)
        self.socket.send_string(msg)        
    def receive(self) -> str:
        return self.socket.recv_string()
    def send_and_wait(self,msg:str)->str:
        self.send(msg)
        resp = self.receive()
        print("response="+resp)
        return resp
    def disconnect(self)->None:
        self.socket.close()



class ZmqSender(ZmqMsgs):
    def __init__(self) -> None:
        super().__init__()
        self.socket = self.context.socket(zmq.REQ)

class ZmqReceiver(ZmqMsgs):
    def __init__(self) -> None:
        super().__init__()
        self.socket=self.context.socket(zmq.REP)
        self.socket.bind("tcp://127.0.0.1:5555")
        print("listening on 5555")
        #self.socket.setsockopt_string(zmq.SUBSCRIBE, "tsfeeder")


