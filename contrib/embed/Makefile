CFLAGS=-Os -Wall -fdata-sections -ffunction-sections $(shell pkg-config --cflags --libs python2,openssl)
CFLAGS=-Os -Wall $(shell pkg-config --cflags --libs python2,openssl)
LDFLAGS=-Wl,--gc-sections
LDFLAGS=
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
	@echo ">> `ls -lah $(PROGNAME)`"

*.o: *.c *.h
	$(CC) -o $<.o $(CFLAGS) -S 

$(PROGNAME): $(OBJ)
	$(CC) $(OBJ) -o $(PROGNAME) $(CFLAGS) $(LDFLAGS)

