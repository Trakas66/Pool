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
        if parsed.path in [ '/shoot.html' ]:

            # retreive the HTML file
            fp = open( '.'+self.path )
            content = fp.read()

            # generate the headers
            self.send_response( 200 ) # OK
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) )
            fp.close()

        # check if the web-pages matches the list
        elif parsed.path[:7] in [ '/table-' ] and parsed.path[-4:] in ['.svg']:

            # retreive the HTML file & insert form data into the HTML file
            try:
                fp = open( parsed.path[1:] )
                content = fp.read()

                # generate the headers
                self.send_response( 200 ); # OK
                self.send_header( "Content-type", "image/svg+xml" )
                self.send_header( "Content-length", len( content ) )
                self.end_headers()

                # send it to the browser
                self.wfile.write( bytes( content, "utf-8" ) )
                fp.close()

            except:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes( "404: %s not found" % self.path, "utf-8"))

        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )


    def do_POST(self):
        # hanle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path )

        if parsed.path in [ '/display.html' ]:

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form = dict(parse_qsl(post_data))

            #delete current svg files
            for root, dirs, files in os.walk(os.getcwd()):
                for file in files:
                    if file.endswith('.svg'):
                        os.remove(file)

            #create table
            table = Physics.Table()

            #add still ball
            sbPos = Physics.Coordinate(float(form['sb_x']), float(form['sb_y']))
            sb = Physics.StillBall(int(form['sb_number']), sbPos)
            table += sb

            #add rolling ball
            rbPos = Physics.Coordinate(float(form['rb_x']), float(form['rb_y']))
            rbVel = Physics.Coordinate(float(form['rb_dx']), float(form['rb_dy']))
            speed = sqrt(rbVel.x**2 + rbVel.y**2)
            if speed < Physics.VEL_EPSILON:
                rbVel.x = 0.0
                rbVel.y = 0.0
            rbAcc = Physics.Coordinate(float(rbVel.x/speed * Physics.DRAG), \
                float(rbVel.y/speed * Physics.DRAG))
            rb = Physics.RollingBall(rbPos, rbVel, rbAcc)
            table += rb

            #construct svg files
            numSvg = 0
            while table:
                with open("table-%d.svg" % numSvg, "w") as file:
                    file.write(table.svg())
                table = table.segment()
                numSvg += 1

            #generate html file
            with open("display.html", "w") as file:
                file.write("""<html>
                                <head>
                                    <title> Results </title>
                                </head>
                                <body>""")
                file.write("<h3>Still Ball: Number: %d, x: %lf, y: %lf</h3>\n<br>\n" \
                    % (sb.obj.still_ball.number, sb.obj.still_ball.pos.x, sb.obj.still_ball.pos.y))
                file.write("<h3>Rolling Ball: x: %lf, y: %lf, dx: %lf, dy: %lf</h3>\n<br>\n" \
                    % (rb.obj.rolling_ball.pos.x, rb.obj.rolling_ball.pos.y, \
                    rb.obj.rolling_ball.vel.x, rb.obj.rolling_ball.vel.y))
                for i in range(numSvg):
                    file.write('<img src="table-%d.svg"/>\n<br>\n' % i)
                file.write('<a href="shoot.html">Back</a>\n')
                file.write("</body>\n</html>")

            fp = open("display.html", "r")
            content = fp.read()

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            # send it to the browser
            self.wfile.write( bytes( content, "utf-8" ) )
            fp.close()

        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )


if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler )
    print( "Server listing in port:  ", int(sys.argv[1]) )
    print(f"Server started on http://localhost:{sys.argv[1]}/shoot.html")
    httpd.serve_forever()
