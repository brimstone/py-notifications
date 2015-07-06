from Tkinter import *
# https://mafayyaz.wordpress.com/2013/02/08/writing-simple-http-server-in-python-with-rest-and-json/
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading


class Notification(Frame):

    def __init__(self, master, text, icon):
        self.text = StringVar()
        f = Frame(master)
        # add a picture
        self.i = Label(f, image=icon)
        self.i.pack(side=LEFT)
        # add some text
        self.text.set(text)
        self.l = Label(f, textvar=self.text, justify=LEFT)
        self.l.pack(side=LEFT, fill=X)
        # pack it all in
        f.pack(fill=X)


class Notifications(object):
    notifications = {}
    def add(self, text, icon, tags):
    def remove(self, id):
    def list(self, tags):
    
class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write("omg hi")


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
jira = PhotoImage(file="jira.png")
jira1 = Notification(
    master, text="OPS-123\nThingy or whatnot\nTomrrow!", icon=jira)
jira2 = Notification(master, text="OPS-234\nOther thingy\nTuesday!", icon=jira)


mainloop()
server.stop()