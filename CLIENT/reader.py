import thread
from twisted.internet import reactor, protocol
from datetime import *
import interface
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

        if data.strip() in '<//KILL_READER//>':
            self.transport.loseConnection()
        else:
            data = data.split('@')
            interface.tex.user_field.delete("1.0", END)
            d = datetime.now()
            message  = '{0}:{1}:{2} {3}\n'.format(d.hour if len(str(d.hour))>1 else '0'+str(d.hour),
                                            d.minute if len(str(d.minute))>1 else '0'+str(d.minute),
                                            d.second if len(str(d.second))>1 else '0'+str(d.second),
                                            data[0].strip())
            f = open('archive.txt', 'a')
            f.write('{0} {1}'.format(d.date(),message))
            f.close()
            users = data[1].strip() + '\n'

            interface.tex.user_field.insert(INSERT,users)
            interface.tex.text.insert(INSERT,message)
            insert_row = int(float(interface.tex.text.index("end")))-2
            try:
                start = "{0}.{1}".format(str(insert_row),message.index('<'))
                end = "{0}.{1}".format(str(insert_row),message.index('>')+1)
                interface.tex.text.tag_add('text', start, end)
            except ValueError, e:
                start = "{0}.0".format(str(insert_row))
                end = "{0}.{1}".format(str(insert_row),len(message))
                interface.tex.text.tag_add('status', start, end)

            interface.tex.text.yview(END)
            interface.tex.user_field.yview(END)

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
