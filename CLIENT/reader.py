import thread
from twisted.internet import reactor, protocol
from datetime import *

import interface
#from TWISTED.CHATprod.config import USER,IP_ADRESS,PORT
from Tkinter import *
import time
import pickle

with open('conf.pickle', 'rb') as handle:
  config = pickle.load(handle)



class EchoClient(protocol.Protocol):

    def connectionMade(self):
        thread.start_new_thread(interface.start,())
        time.sleep(1)
        self.transport.write("UPDATE_SESSION@{}".format(config["USER"]))

    def dataReceived(self, data):
        print data,'*****'
        if data.strip() in '<//KILL_READER//>':
            self.transport.loseConnection()
        else:
            data = data.split('@')
            interface.tex.user_field.delete("1.0", END)
            d = datetime.now()
            message  = '{0}:{1}:{2}'.format(d.hour,d.minute,d.second) +  '@@' + data[0].strip() + '\n'
            f = open('archive.txt', 'a')
            f.write('{0} {1}'.format(d.date(),message))
            f.close()
            users = data[1].strip() + '\n'
            interface.tex.user_field.insert(INSERT,users)
            interface.tex.text.insert(INSERT,message)

    def connectionLost(self, reason):
        print reason.value

class EchoFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):

        return EchoClient()
    def clientConnectionFailed(self, connector, reason):
        print "Connection failed."
        reactor.stop()
    def clientConnectionLost(self, connector, reason):
        print "Connection lost."
        reactor.stop()

reactor.connectTCP(config["IP_ADRESS"], config["PORT"], EchoFactory())
reactor.run()
