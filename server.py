import sys  # used to get argv
import cgi  # used to parse Mutlipart FormData 
            # this should be replace with multipart in the future
import os

import Physics
from math import sqrt

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl

# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path )

        # check if the web-pages matches the list
        if parsed.path in ['', '/']:

            fp = open('index.html')
            content = fp.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))
            fp.close()
        
        elif parsed.path in ['/game.css']:
            fp = open( '.'+self.path )
            content = fp.read()

            # generate the headers
            self.send_response( 200 ) # OK
            self.send_header( "Content-type", "text/css" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) )
            fp.close()
        
        elif parsed.path in ['/game.js']:
            fp = open('.'+self.path)
            content = fp.read()

            self.send_response(200)
            self.send_header("Content-type", "text/javascript")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))
            fp.close()
        
        elif parsed.path in ['/table.svg']:
            fp = open('.'+self.path)
            content = fp.read()

            self.send_response(200)
            self.send_header("Content-type", "image/svg+xml")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))
            fp.close()

        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )
        
    def do_POST(self):

        parsed = urlparse(self.path)

        if parsed.path in ['/game.html']:
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")
            form = dict(parse_qsl(post_data))

            if form["new"] == "True":
                game = Physics.Game(None, form["gamename"], form["player1name"], form["player2name"])
            else:
                game = Physics.Game(int(form["gameid"]))

            fp = open("game.html", "r")
            content = fp.read()

            content = content.replace('data-id="0"', f'data-id="{game.gameID}"')

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))
        
        elif parsed.path in ['/shoot']:
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")
            form = dict(parse_qsl(post_data))

            game = Physics.Game(int(form["gameid"]))

            xVel = (float(form["ballX"]) - float(form["x"])) * Physics.SHOT_POWER
            yVel = (float(form["ballY"]) - float(form["y"])) * Physics.SHOT_POWER

            lastShots = game.shoot(game.gameName, game.player1Name, game.db.readTable(game.tableID), xVel, yVel)

            for i in range(len(lastShots)):
                svgString = lastShots[i].svg()
                lastShots[i] = svgString

            content = ":,:".join(lastShots)

            self.send_response(200)
            self.send_header("Content-type", "text")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"))


if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler )
    print( "Server listing in port:  ", int(sys.argv[1]) )
    print(f"Server started on http://localhost:{sys.argv[1]}/")
    httpd.serve_forever()
