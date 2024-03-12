CC=clang
CFLAGS=-c -Wall -pedantic -std=c99
FLAGS=-Wall -pedantic -std=c99
LIBS=-lm -L. -lphylib
PLIBS=-L. -L/usr/include/python3.11 -lpython3.11 -lphylib
FILES=phylib_wrap.c phylib.py

all: _phylib.so

libphylib.so: phylib.o
	$(CC) phylib.o -shared -o libphylib.so

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) phylib.c -fPIC -o phylib.o

_phylib.so: phylib_wrap.o
	$(CC) $(FLAGS) -shared phylib_wrap.o $(PLIBS) -o _phylib.so

phylib_wrap.o: $(FILES)
	$(CC) $(CFLAGS) phylib_wrap.c -I/usr/include/python3.11 -fPIC -o phylib_wrap.o

$(FILES): phylib.i libphylib.so
	swig -python phylib.i

clean:
	rm -rf *.o *.so main *.svg __pycache__ phylib.py phylib_wrap.c