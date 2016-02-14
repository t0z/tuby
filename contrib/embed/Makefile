CFLAGS=-Wall $(shell pkg-config --cflags --libs python2)
CC=gcc
SRC=$(shell ls *.c)
OBJ=$(SRC:.c=.o)

PROGNAME=emby

.PHONY: all pre_build

all: build

clean: 
	rm -f $(PROGNAME)
	rm -f *.o

build: pre_build $(PROGNAME) $(SRC) $(OBJ)

pre_build:
	mkdir -p build/

*.o: *.c *.h
	echo "+++ object: " $<
	$(CC) -o build/$<.o $(CFLAGS) -S 

$(PROGNAME): $(OBJ)
	$(CC) $(OBJ) -o $(PROGNAME) $(CFLAGS)

