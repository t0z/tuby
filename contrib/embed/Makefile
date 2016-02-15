CFLAGS=-Os -Wall -fdata-sections -ffunction-sections $(shell pkg-config --cflags --libs python2)
LDFLAGS=-Wl,--gc-sections
CC=gcc
SRC=$(shell ls *.c)
OBJ=$(SRC:.c=.o)
PROGNAME=emby

.PHONY: all clean

all: build

clean:
	rm -f $(PROGNAME)
	rm -f *.o
	rm -rf build/

build: $(PROGNAME)
	echo "$(PROGNAME) built"

*.o: *.c *.h
	$(CC) -o $<.o $(CFLAGS) -S 

$(PROGNAME): $(OBJ)
	$(CC) $(OBJ) -o $(PROGNAME) $(CFLAGS) $(LDFLAGS)

