#!/usr/bin/python

# CGI SimpleFileUpload WebServer Ver. 0.1.5
# Author: Srinivas Gowda
# Email: srinivas@solancer.com


import string,cgi,time, re
import json
import math
import time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import os # os. path

CWD = os.path.abspath('.') + '/uploads'
print CWD

# PORT = 8080
UPLOAD_PAGE = 'upload'

def convertSize(size):
   size_name = ("B","KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   if (s > 0):
       return '%s %s' % (s,size_name[i])
   else:
       return '0B'

def json_view(relpath):
    abspath = os.path.abspath(relpath) + '/uploads'
    flist = os.listdir( abspath )
    modlist = []
    slist = []
    for i in flist:
        modlist.append(time.ctime(os.path.getmtime(abspath+sep+i)))
        slist.append(convertSize(os.path.getsize(abspath+sep+i)))
    print modlist
    return json.dumps([{'name':k,'mod': v,'size':n} for k, v, n in zip(flist,modlist,slist)])



# -----------------------------------------------------------------------

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            
            if self.path == '/' :     
                f = open(curdir + sep + 'indexer.html')
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                return     

            if self.path.endswith('/json'):
                page2 = json_view( '.' )
                self.send_response(200)
                self.send_header('Content-type',    'application/json')
                self.end_headers()
                self.wfile.write(page2)
                return

            if self.path == '/upload' :     
                f = open(curdir + sep + 'upload.html')
                self.send_response(200)
                self.send_header('Content-type',    'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                return

            if self.path.endswith(".html"):
                ## print curdir + sep + self.path
                f = open(curdir + sep + self.path)

                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            if self.path == ("/static/python-powered.png"):
                ## print curdir + sep + self.path
                f = open(curdir + sep + self.path)

                self.send_response(200)
                self.send_header('Content-type',    'image/png')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return


            if self.path.endswith(".css"):
                ## print curdir + sep + self.path
                f = open(curdir + sep + self.path)

                self.send_response(200)
                self.send_header('Content-type',    'text/css')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            
            if self.path.endswith(".js"):
                ## print curdir + sep + self.path
                f = open(curdir + sep + self.path)

                self.send_response(200)
                self.send_header('Content-type',    'text/javascript')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            if self.path.endswith(".eot"):
                ## print curdir + sep + self.path
                f = open(curdir + sep + self.path)

                self.send_response(200)
                self.send_header('Content-type',    'application/vnd.ms-fontobject')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            if self.path.endswith(".ttf"):
                ## print curdir + sep + self.path
                f = open(curdir + sep + self.path)

                self.send_response(200)
                self.send_header('Content-type',    'application/x-font-ttf')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            if self.path.endswith(".svg"):
                ## print curdir + sep + self.path
                f = open(curdir + sep + self.path)

                self.send_response(200)
                self.send_header('Content-type',    'image/svg+xml')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            if self.path.endswith(".woff"):
                ## print curdir + sep + self.path
                f = open(curdir + sep + self.path)

                self.send_response(200)
                self.send_header('Content-type',    'application/font-woff')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            else : # default: just send the file     
                
                filepath = self.path[1:] # remove leading '/'     
            
                f = open( os.path.join(CWD, filepath), 'rb' ) 

                self.send_response(200)
                self.send_header('Content-type',	'application/octet-stream')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            return # be sure not to fall into "except:" clause ?       
                
        except IOError as e :  
            # debug     
            print e
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_POST(self):
        # global rootnode ## something remained in the orig. code     
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))     

            if ctype == 'multipart/form-data' :     

                fs = cgi.FieldStorage( fp = self.rfile, 
                                       headers = self.headers, # headers_, 
                                       environ={ 'REQUEST_METHOD':'POST' }    
                                     )

            else: raise Exception("Unexpected POST request")
                
                
            fs_up = fs['upfile']
            filename = os.path.split(fs_up.filename)[1]
            f_filename = str(filename).replace(" ", "_")
            fullname = os.path.join(CWD, f_filename)

            # check for copies :     
            if os.path.exists( fullname ):     
                fullname_test = fullname + '.copy'
                i = 0
                while os.path.exists( fullname_test ):
                    fullname_test = "%s.copy(%d)" % (fullname, i)
                    i += 1
                fullname = fullname_test
                
            if not os.path.exists(fullname):
                with open(fullname, 'wb') as o:
                    # self.copyfile(fs['upfile'].file, o)
                    o.write( fs_up.file.read() )     


            self.send_response(200)
            self.end_headers()
            
            self.wfile.write("<HTML><HEAD></HEAD><BODY>Upload Successful!<BR><BR>");
            self.wfile.write( "File uploaded under name: " + os.path.split(fullname)[1] );
            self.wfile.write(  '<BR><A HREF="/">Main page</A>')
            self.wfile.write(  '<BR><A HREF=%s>back</A>' % ( UPLOAD_PAGE, )  )
            self.wfile.write("</BODY></HTML>");
            
            
        except Exception as e:
            # pass
            print e
            self.send_error(404,'POST to "%s" failed: %s' % (self.path, str(e)) )

def main():

    try:
        server = HTTPServer(('', 8080), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

