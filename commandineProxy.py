import SocketServer
import SimpleHTTPServer
import urllib2
import select, socket, SocketServer 

# Note to self: In firefox explicitly change proxy AND SSL proxy

PORT = 1024
class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
     def do_GET(self):
	 print self.path
         self.copyfile(urllib2.urlopen(self.path), self.wfile) 

     def _connect_to(self, netloc, soc):
        i = netloc.find(':')
        if i >= 0:
            host_port = netloc[:i], int(netloc[i+1:])
        else:
            host_port = netloc, 80
	#print host_port
	try: soc.connect(host_port)
        except socket.error, arg:
            try: msg = arg[1]
            except: msg = arg 
            self.send_error(404, msg)
            return 0
        return 1

     def do_CONNECT(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if self._connect_to(self.path, soc):
                self.wfile.write(self.protocol_version +
                                 " 200 Connection established\r\n")
                self.wfile.write("Proxy-agent: %s\r\n" % self.version_string())
                self.wfile.write("\r\n")
                self._read_write(soc, 300)
        finally:
            soc.close()
            self.connection.close()

     def _read_write(self, soc, max_idling=20, local=False):
        iw = [self.connection, soc]
        print self.path
	local_data = ""
        ow = []
        count = 0
        while 1:
            count += 1
            (ins, _, exs) = select.select(iw, ow, iw, 1)
            if exs: break
            if ins:
                for i in ins:
                    if i is soc: out = self.connection
                    else: out = soc
                    data = i.recv(8192)
                    if data:
                        if local: local_data += data
                        else: out.send(data)
                        count = 0
            if count == max_idling: break
        if local: return local_data
        return None


httpd = SocketServer.ForkingTCPServer(('', PORT), Proxy)
print "serving at port", PORT
httpd.serve_forever()
