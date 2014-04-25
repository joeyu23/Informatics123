from network import Handler, poll
import sys
from threading import Thread
from time import sleep


myname = raw_input('What is your name? ')

class Client(Handler):
    
    def on_close(self):
        pass
    
    def on_msg(self, msg):
        if 'name' in msg:
            print msg['name'] + ': ' + msg['txt']
        elif 'join' in msg:
            print msg['join'] + ' has joined the room. Users in the room: ' + msg['users']
        elif 'leave' in msg:
            print msg['leave'] + ' has left the room. Users in the room: ' + msg['users']
        
host, port = 'localhost', 8888
client = Client(host, port)
client.do_send({'join': myname})

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds
                            
thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies 
thread.start()

while 1:
    mytxt = sys.stdin.readline().rstrip()
    client.do_send({'speak': myname, 'txt': mytxt})