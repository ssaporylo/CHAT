__author__ = 'user'
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import sys
import time

class ChatProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        pass
    def dataReceived(self, data):
        self.lineReceived(data.strip())

    def connectionLost(self, reason):
        pass
    def lineReceived(self, line):

        if "REGISTER@" in line:
            if self._checkUser(line):
                self.sendLine("Connected..")
        elif "UPDATE_SESSION@" in line:
            self.handle_REGISTER(line)
        elif "DELETE@" in line:
            self.handle_DELETE(line)
        elif "MESSAGE@" in line:
            self.transport.write('OK')
            self.broadcastMessage(line.split('@')[-1])
        else:
            self.handle_CHAT(line)

    def _checkUser(self, line):
        user = line.split('@')[1]
        if user in self.factory.users.keys():
            self.sendLine('User exists')
            return False
        return True


    def handle_REGISTER(self, line):
        user = line.split("@")[1]
        message = "{} joined to chat".format(user)
        self.factory.users[user]= self
        self.broadcastMessage(message)
        self.factory.users[user]= self

    def handle_DELETE(self,line):
        #print line
        user = line.split("@")[1]
        message = "{} left chat".format(user)

        self.factory.users[user].sendLine('<//KILL_READER//>')
        del self.factory.users[user]
        self.broadcastMessage(message)


    def handle_CHAT(self, message):
        self.broadcastMessage(message)

    def broadcastMessage(self, message):


        for protocol in self.factory.users.values():
            protocol.sendLine(message)
            self._users(protocol)

    def _users(self,protocol):
        users="@- {}".format('\n-'.join(self.factory.users.keys()))
        protocol.sendLine(users)

class ChatFactory(Factory):
    def __init__(self):
        self.users = {}
    def buildProtocol(self, addr):
        return ChatProtocol(self)

if __name__ == "__main__":
    reactor.listenTCP(int(sys.argv[1]), ChatFactory())
    reactor.run()
