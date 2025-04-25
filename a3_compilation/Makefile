CC = gcc
CFLAGS = -Wall -c -I../lib

all: main.o

main.o: main.c
	$(CC) $(CFLAGS) main.c -o main.o

clean:
	rm -f *.o *.out
