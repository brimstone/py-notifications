from Tkinter import *
# https://mafayyaz.wordpress.com/2013/02/08/writing-simple-http-server-in-python-with-rest-and-json/
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import json
import webbrowser


class Notification(Frame):

    def __init__(self, master, text, icon, url, tags):
        self.url = url
        self.tags = tags
        self.text = StringVar()
        self.f = Frame(master)
        self.f.bind("<Button-1>", self.click)
        # add a picture
        self.image = PhotoImage(file="icons/%s.png" % icon)
        self.i = Label(self.f, image=self.image)
        self.i.pack(side=LEFT)
        self.i.bind("<Button-1>", self.click)
        # add some text
        self.text.set(text)
        self.l = Label(self.f, textvar=self.text, justify=LEFT)
        self.l.pack(side=LEFT, fill=X)
        self.l.bind("<Button-1>", self.click)
        # pack it all in
        self.f.pack(fill=X)

    def __del__(self):
        self.f.pack_forget()

    def click(self, event):
        if self.url:
            webbrowser.open(self.url)


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write("omg hi")

    def do_POST(self):
        if None != re.search('/', self.path):
            length = int(self.headers.getheader('content-length'))
            data = json.loads(self.rfile.read(length))
            notifications.append(Notification(
                                 master, text=data["text"], icon=data["icon"], tags=data["tags"], url=data["url"]))
            self.send_response(200)
            self.end_headers()
            self.wfile.write("ok")

    def do_DELETE(self):
        if None != re.search('/', self.path):
            length = int(self.headers.getheader('content-length'))
            data = json.loads(self.rfile.read(length))
            if data["tags"]:
                for t in data["tags"]:
                    for i in reversed(range(0, len(notifications))):
                        try:
                            if notifications[i].tags.index(t) >= 0:
                                del notifications[i]
                        except:
                            next
            self.send_response(200)
            self.end_headers()
            self.wfile.write("ok")


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True

    def shutdown(self):
        self.socket.close()
        HTTPServer.shutdown(self)


class SimpleHttpServer():

    def __init__(self, ip, port):
        self.server = ThreadedHTTPServer((ip, port), HTTPRequestHandler)

    def start(self):
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def waitForThread(self):
        self.server_thread.join()

    def addRecord(self, recordID, jsonEncodedRecord):
        LocalData.records[recordID] = jsonEncodedRecord

    def stop(self):
        self.server.shutdown()
        self.waitForThread()

server = SimpleHttpServer("0.0.0.0", 8080)
server.start()
# server.waitForThread()

master = Tk()
notifications = []

mainloop()
server.stop()
