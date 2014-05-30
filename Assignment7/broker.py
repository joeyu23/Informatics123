from network import Listener, Handler, poll


handlers = {}  # map client handler to user name
names = {} # map name to handler
subs = {} # map tag to handlers

def broadcast(msg):
    for h in handlers.keys():
        h.do_send(msg)


class MyHandler(Handler):
    
    def on_open(self):
        handlers[self] = None
        
    def on_close(self):
        name = handlers[self]
        del handlers[self]
        broadcast({'leave': name, 'users': handlers.values()})
        
    def on_msg(self, msg):
        
        if 'join' in msg:
            name = msg['join']
            handlers[self] = name
            names[name] = self
            broadcast({'join': name, 'users': handlers.values()})
        elif 'speak' in msg:
            name, txt = msg['speak'], msg['txt']
            wordlist = msg['txt'].split(" ")
            words_to_remove_list = []
            broadcastlist = []
            
            #Check if message is for everyone
            public = True
            for word in wordlist:
                
                ## Q1 - subscribe ##
                if word[0] == '+':
                    topic = word[1:]
                    if topic in subs:
                        subs[topic].append(name)
                    else: 
                        subs[topic] = []
                        subs[topic].append(name)
                    words_to_remove_list.append(word) #adds the word to a list of words to be removed

                ## Q2 - publish ##
                elif word[0] == "#":
                    public = False
                    topic = word[1:]
                    if topic in subs:
                        subscribers = subs[topic]

                        for subscriber in subscribers:
                            if subscriber not in broadcastlist:
                                broadcastlist.append(subscriber)

                ## Q3 - unsubscribe ##
                elif word[0] == "-":
                    topic = word[1:]
                    if topic in subs:
                        subscribers = subs[topic]

                        if name in subscribers:
                            subscribers.remove(name)

                    words_to_remove_list.append(word)

                ## Q4 - private messages ##
                elif word[0] == "@":
                    public = False
                    recipient = word[1:]
                    if recipient in names:
                        if recipient not in broadcastlist:
                            broadcastlist.append(recipient)
                            
            for word in words_to_remove_list:
                wordlist.remove(word)

            txt = " ".join(wordlist)

            if txt:
                # if the message for public, send to everyone
                if public:
                    broadcast({'speak': name, 'txt': txt})
                # otherwise, send it to the client
                else:
                    for client in broadcastlist:
                        names[client].do_send({'speak': name, 'txt': txt})

Listener(8888, MyHandler)
while 1:
    poll(0.05)
    poll(0.05)