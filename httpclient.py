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

    # Connect Socket
    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return self.socket

    # Returns status code
    def get_code(self, data):
        code = int(data.split(" ")[1])
        return code

    # Returns body
    def get_body(self, data):
        body = data.split("\r\n\r\n")[1]
        return body

    # Parse url for host, port and path
    def get_parsed_url(self, url):
        parsed_url = urllib.parse.urlparse(url)
        scheme = parsed_url.scheme
        host = parsed_url.hostname
        port = parsed_url.port
        path = parsed_url.path

        # Default Port if one is not given
        if port == None:
            if scheme == "https":
                port = 443
            else:
                port = 80
        
        # Default Path if one is not given
        if path == "":
            path = "/"

        return host, int(port), path
    
    # Encode and send all data to server
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))

    # Close the existing connection to server    
    def close(self):
        self.socket.close()

    # Read everything from the socket
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

    # GET Request from Client
    def GET(self, url, args=None):

        # Fetch host, port and path information
        host, port, path = self.get_parsed_url(url)

        # Connect to the server
        sock = self.connect(host, port)
        request = "GET "+path+" HTTP/1.1\r\nHost: "+host+"\r\nConnection: close\r\n\r\n"
        print("REQUEST= ", request)
        self.sendall(request)
        response = self.recvall(sock)

        # Fetch status code
        code = self.get_code(response)

        # Fetch body
        body = self.get_body(response)

        # Close the socket
        self.close()

        return HTTPResponse(code, body)

    # POST Request from Client
    def POST(self, url, args=None):
        code = 500
        body = ""
        # Fetch host, port and path information
        host, port, path = self.get_parsed_url(url)

        # Connect to the server
        sock = self.connect(host, port)

        # Check if there are args
        if args == None:
            request = "POST "+path+" HTTP/1.1\r\nHost: "+host+"\r\nContent-Length: "+ str(0)+"\r\nContent-Type: application/x-www-form-urlencoded\r\nConnection: close\r\n\r\n"

        else:
            request = a

            
        self.sendall(request)
        response = self.recvall(sock)

        # Fetch status code
        code = self.get_code(response)

        # Fetch body
        body = self.get_body(response)

        # Close the socket
        self.close()

        return HTTPResponse(code, body)

    # Command is used separately from test server files
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
