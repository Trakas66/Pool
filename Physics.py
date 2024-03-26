import phylib
import os
import sqlite3
from math import sqrt, floor
import CreateTable

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS
BALL_DIAMETER = 2*BALL_RADIUS

HOLE_RADIUS   = 2*BALL_DIAMETER
TABLE_LENGTH  = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH   = TABLE_LENGTH/2.0

SIM_RATE      = phylib.PHYLIB_SIM_RATE
VEL_EPSILON   = phylib.PHYLIB_VEL_EPSILON

DRAG          = phylib.PHYLIB_DRAG
MAX_TIME      = phylib.PHYLIB_MAX_TIME

MAX_OBJECTS   = phylib.PHYLIB_MAX_OBJECTS

FRAME_RATE    = 0.01

SHOT_POWER    = 5.0

# add more here

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" id="surface"/>"""

FOOTER = """</svg>\n"""

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ]

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall

    # add an svg method here
    def svg(self):
        if self.obj.still_ball.number == 0:
            return """ <circle cx="%d" cy="%d" r="%d" fill="%s" id="cue-ball" />\n""" \
            % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, \
            BALL_COLOURS[self.obj.still_ball.number])
        else:
            return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" \
            % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, \
            BALL_COLOURS[self.obj.still_ball.number])


################################################################################

class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc ):
        """
        Constructor function. Requires position (x,y), velocity (x,y) and
        acceleration (x,y) as arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = RollingBall


    # add an svg method here
    def svg(self):
        if self.obj.rolling_ball.number == 0:
            return """ <circle cx="%d" cy="%d" r="%d" fill="%s" id="cue-ball"/>\n""" \
            % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, \
            BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])
        else:
            return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" \
            % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, \
            BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])


################################################################################

class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos ):
        """
        Constructor function. Requires position (x,y) as argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       None, 
                                       pos, None, None, 
                                       0.0, 0.0 )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = Hole


    # add an svg method here
    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" \
            % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)


################################################################################

class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__( self, y ):
        """
        Constructor function. Requires y position as argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       None, 
                                       None, None, None, 
                                       0.0, y )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = HCushion


    # add an svg method here
    def svg(self):
        y = self.obj.hcushion.y
        if y < TABLE_WIDTH:
            y -= 25
        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" \
            % y


################################################################################

class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__( self, x ):
        """
        Constructor function. Requires x position as argument.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       None, 
                                       None, None, None, 
                                       x, 0.0 )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = VCushion


    # add an svg method here
    def svg(self):
        x = self.obj.vcushion.x
        if x < TABLE_WIDTH:
            x -= 25
        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" \
            % x


################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self )
        self.current = -1

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other )
        return self

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ] # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1    # reset the index counter
        raise StopIteration  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion
        return result

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = ""    # create empty string
        result += "time = %6.1f;\n" % self.time    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj)  # append object description
        return result  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self )
        if result:
            result.__class__ = Table
            result.current = -1
        return result

    # add svg method here
    def svg(self):
        string = HEADER
        for object in self:
            if object:
                string += object.svg()
        string += FOOTER
        return string
    
    def cueBall(self, xVel, yVel):
        for obj in self:
            if isinstance(obj, StillBall):
                if obj.obj.still_ball.number == 0:
                    xPos = obj.obj.still_ball.pos.x
                    yPos = obj.obj.still_ball.pos.y
                    obj.type = phylib.PHYLIB_ROLLING_BALL
                    obj.obj.rolling_ball.number = 0
                    obj.obj.rolling_ball.pos.x = xPos
                    obj.obj.rolling_ball.pos.y = yPos
                    obj.obj.rolling_ball.vel.x = xVel
                    obj.obj.rolling_ball.vel.y = yVel
                    speed = sqrt(xVel**2 + yVel**2)
                    xAcc = xVel/speed * DRAG
                    yAcc = yVel/speed * DRAG
                    obj.obj.rolling_ball.acc.x = xAcc
                    obj.obj.rolling_ball.acc.y = yAcc
                    return

    def roll( self, t ):
        new = Table()
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) )
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t )
                # add ball to table
                new += new_ball
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                        Coordinate( ball.obj.still_ball.pos.x,
                                                    ball.obj.still_ball.pos.y ) )
                # add ball to table
                new += new_ball
        # return table
        return new


class Database:

    def __init__(self, reset=False):
        if reset:
            if os.path.exists("phylib.db"):
                os.remove("phylib.db")

        self.conn = sqlite3.connect("phylib.db")
    

    def createDB(self):
        cur = self.conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS Ball(
                    BALLID INTEGER NOT NULL,
                    BALLNO INTEGER NOT NULL,
                    XPOS FLOAT NOT NULL,
                    YPOS FLOAT NOT NULL,
                    XVEL FLOAT,
                    YVEL FLOAT,
                    PRIMARY KEY (BALLID)
                    );''')
        
        cur.execute('''CREATE TABLE IF NOT EXISTS TTable(
                    TABLEID INTEGER NOT NULL,
                    TIME FLOAT NOT NULL,
                    PRIMARY KEY (TABLEID)
                    );''')
        
        cur.execute('''CREATE TABLE IF NOT EXISTS BallTable(
                    BALLID INTEGER NOT NULL,
                    TABLEID INTEGER NOT NULL,
                    FOREIGN KEY (BALLID) REFERENCES Ball,
                    FOREIGN KEY (TABLEID) REFERENCES TTable
                    );''')
        
        cur.execute('''CREATE TABLE IF NOT EXISTS Shot(
                    SHOTID INTEGER NOT NULL,
                    PLAYERID INTEGER NOT NULL,
                    GAMEID INTEGER NOT NULL,
                    PRIMARY KEY (SHOTID),
                    FOREIGN KEY (PLAYERID) REFERENCES Player,
                    FOREIGN KEY (GAMEID) REFERENCES Game
                    );''')
        
        cur.execute('''CREATE TABLE IF NOT EXISTS TableShot(
                    TABLEID INTEGER NOT NULL,
                    SHOTID INTEGER NOT NULL,
                    FOREIGN KEY (TABLEID) REFERENCES TTable,
                    FOREIGN KEY (SHOTID) REFERENCES Shot
                    );''')
        
        cur.execute('''CREATE TABLE IF NOT EXISTS Game(
                    GAMEID INTEGER NOT NULL,
                    GAMENAME VARCHAR(64) NOT NULL,
                    TABLEID INTEGER NOT NULL,
                    PRIMARY KEY (GAMEID),
                    FOREIGN KEY (TABLEID) REFERENCES TTable
                    );''')
        
        cur.execute('''CREATE TABLE IF NOT EXISTS Player(
                    PLAYERID INTEGER NOT NULL,
                    GAMEID INTEGER NOT NULL,
                    PLAYERNAME VARCHAR(64) NOT NULL,
                    PRIMARY KEY (PLAYERID),
                    FOREIGN KEY (GAMEID) REFERENCES Game
                    );''')
        
        cur.close()
        self.conn.commit()

    def readTable(self, tableID):
        cur = self.conn.cursor()

        table = Table()

        maxID = cur.execute('''SELECT MAX(TABLEID) FROM TTable''').fetchone()[0]
        if tableID >= maxID:
            return None

        balls = cur.execute(f'''SELECT * FROM 
                                (Ball INNER JOIN BallTable ON
                                Ball.BALLID = BallTable.BALLID)
                                WHERE TABLEID = {tableID+1}''')

        for ball in balls.fetchall():

            if ball[4] == 0.0 and ball[5] == 0.0:
                table += StillBall(ball[1], Coordinate(ball[2], ball[3]))
            
            else:
                speed = sqrt(ball[4]**2 + ball[5]**2)
                acc = Coordinate(float(ball[4]/speed * DRAG), float(ball[5]/speed * DRAG))
                table += RollingBall(ball[1], Coordinate(ball[2], ball[3]), 
                                     Coordinate(ball[4], ball[5]), acc)
        
        time = cur.execute(f'''SELECT TIME FROM TTable
                            WHERE TABLEID = {tableID+1}''')
        table.time = float(time.fetchall()[0][0])

        cur.close()
        self.conn.commit()

        return table
    
    def writeTable(self, table):
        cur = self.conn.cursor()

        cur.execute(f'''INSERT INTO TTable(TIME)
                    VALUES({table.time})''')
        
        tableID = cur.execute('''SELECT last_insert_rowid() FROM TTable''').fetchall()[0][0]

        for obj in table:
            if isinstance(obj, StillBall):
                ball = obj.obj.still_ball
                cur.execute(f'''INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                                VALUES ({ball.number}, {ball.pos.x}, {ball.pos.y}, 0.0, 0.0)''')
                id = cur.execute('''SELECT last_insert_rowid() FROM Ball''').fetchall()[0][0]
                cur.execute(f'''INSERT INTO BallTable (BALLID, TABLEID)
                            VALUES ({id}, {tableID})''')
                
            elif isinstance(obj, RollingBall):
                ball = obj.obj.rolling_ball
                cur.execute(f'''INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                                VALUES ({ball.number}, {ball.pos.x}, {ball.pos.y}, 
                                {ball.vel.x}, {ball.vel.y})''')
                id = cur.execute('''SELECT last_insert_rowid() FROM Ball''').fetchall()[0][0]
                cur.execute(f'''INSERT INTO BallTable (BALLID, TABLEID)
                            VALUES ({id}, {tableID})''')

        cur.close()
        self.conn.commit()

        return tableID - 1

    def getGame(self, gameID):
        cur = self.conn.cursor()

        data = cur.execute(f'''SELECT PLAYERNAME, GAMENAME FROM
                    (Game INNER JOIN Player ON
                    Game.GAMEID = Player.GAMEID)
                    WHERE Game.GAMEID = {gameID}''').fetchall()
        
        gameName = data[0][1]
        player1Name = data[0][0]
        player2Name = data[1][0]

        data = cur.execute(f'''SELECT TABLEID FROM Game
                           WHERE GAMEID = {gameID}''').fetchone()
        
        tableID = int(data[0]) - 1

        cur.close()
        self.conn.commit()

        return (gameName, player1Name, player2Name, tableID)

    def setGame(self, gameName, player1Name, player2Name, tableID):

        cur = self.conn.cursor()

        tableID += 1

        cur.execute(f'''INSERT INTO Game(GAMENAME, TABLEID)
                    VALUES ("{gameName}", {tableID})''')
        
        gameID = cur.execute('''SELECT last_insert_rowid() FROM Game''').fetchone()[0]
        
        cur.execute(f'''INSERT INTO Player(GAMEID, PLAYERNAME)
                    VALUES({gameID}, "{player1Name}")''')
        cur.execute(f'''INSERT INTO Player(GAMEID, PLAYERNAME)
                    VALUES({gameID}, "{player2Name}")''')
        
        cur.close()
        self.conn.commit()

        return gameID - 1

    def newShot(self, playerName, gameID):
        gameID += 1
        cur = self.conn.cursor()

        playerID = cur.execute(f'''SELECT PLAYERID FROM Player
                               WHERE GAMEID = {gameID}''').fetchone()[0]
        
        cur.execute(f'''INSERT INTO Shot (PLAYERID, GAMEID)
                    VALUES ({playerID}, {gameID})''')
        shotID = cur.execute('''SELECT last_insert_rowid() FROM Shot''').fetchone()[0]

        cur.close()
        self.conn.commit()

        return shotID

    def recordShot(self, tableID, shotID):
        cur = self.conn.cursor()

        cur.execute(f'''INSERT INTO TableShot (TABLEID, SHOTID)
                    VALUES ({tableID}, {shotID})''')
        
        cur.close()
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()

class Game:
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):

        self.db = Database()

        self.db.createDB()

        self.lastShot = []

        if gameID != None:
            if gameName or player1Name or player2Name:
                raise TypeError("gameID was passed in with other parameters")
            
            self.gameID = gameID
            gameName, player1Name, player2Name, tableID = self.db.getGame(self.gameID + 1)
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
            self.tableID = tableID
            with open("table.svg", "w") as file:
                file.write(self.db.readTable(self.tableID).svg())
        
        elif gameName and player1Name and player2Name:

            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name

            self.tableID = self.setupTable()

            self.gameID = self.db.setGame(self.gameName, self.player1Name, self.player2Name, self.tableID)
        
            with open("table.svg", "w") as file:
                file.write(self.db.readTable(self.tableID).svg())

        else:
            raise TypeError("Not enough arguments")
    
    def setupTable(self):
        table = CreateTable.CreateTable()

        tableID = self.db.writeTable(table)

        return tableID

    def shoot(self, gameName, playerName, table, xVel, yVel):

        initTable = table
        table.cueBall(xVel, yVel)

        while table:
            oldTable = table
            table = table.segment()
            if table:
                totalTime = table.time - oldTable.time
                frames = floor(totalTime / FRAME_RATE)
                for i in range(frames):
                    myTime = i * FRAME_RATE
                    newTable = oldTable.roll(myTime)
                    newTable.time = oldTable.time + myTime
                    yield newTable
        
        table = initTable

        yield 0

        """ shotID = self.db.newShot(playerName, self.gameID)

        table.cueBall(xVel, yVel)

        while table:
            oldTable = table
            table = table.segment()
            if table:
                totalTime = table.time - oldTable.time
                frames = floor(totalTime / FRAME_RATE)
                for i in range(frames):
                    myTime = i * FRAME_RATE
                    newTable = oldTable.roll(myTime)
                    newTable.time = oldTable.time + myTime
                    tableID = self.db.writeTable(newTable)
                    self.db.recordShot(tableID, shotID)
        
        self.tableID = tableID
        
        yield shotID """

    #def svg(self, )

    def __del__(self):
        self.db.close()
