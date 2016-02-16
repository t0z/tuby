DEBUG=-DDEBUG
#CFLAGS=-Os -Wall -fdata-sections -ffunction-sections\
	$(shell pkg-config --cflags --libs python2,openssl,libcurl)
CFLAGS=-Wall -L/usr/lib $(shell pkg-config --static --cflags --libs python2,libcurl)
#LDFLAGS=-Wl,--gc-sections
LDFLAGS=
CC=gcc $(DEBUG)
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

