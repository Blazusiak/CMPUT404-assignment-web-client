#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return self.socket

    def get_code(self, data):
        #print("We are in get_code", data)
        split_data = data.split("\r\n")
        #print(split_data)
        split_again = split_data[0].split(" ")
        #print("again", split_again)
        return split_again[1]

    def get_headers(self,data):
        #headers = data.split("\r\n\r\n")[0]
        #print("These are the headers", headers)
        return None

    def get_body(self, data):
        split_data = data.split("\r\n\r\n")
        return split_data[1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""
        
        print("what is this?", url, args)

        # Parse url for host and port
        parsed_url = urllib.parse.urlparse(url)
        host, port = parsed_url.netloc.split(':')
        path = urllib.parse.urlparse(url).path
        #print("this is the path", path)

        # Connect to the server
        sock = self.connect(host, int(port))
        print(sock) # Make sure port 80 for google
        header = "GET "+path+" HTTP/1.1\nHost: "+host+"\n\n"
        print(header)
        self.sendall(header)
        response = self.recvall(sock)

        print("WHAT WE HAVE?\n", response, "\nThe end of what we have")
        self.get_headers(response)
        # Update status code
        code = int(self.get_code(response))

        # Update body
        body = self.get_body(response)

        # Close the socket
        self.close()

        #print("YES THIS IS RESPONSE", response)
        print("\n\n\n", code, body, "THIS IS THE REPONSE")
        return HTTPResponse(int(code), body)

    def POST(self, url, args=None):
        code = 500
        body = ""

        print("what is this?", url)

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
