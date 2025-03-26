# a3_compilation/main.make

CC = gcc
CFLAGS = -Wall -c -I../lib      # ← include ../lib für Header-Dateien
LDFLAGS = -lm
LIB = ../lib/libmatrix.a

all: main.out

main.out: main.o qr.o
	$(CC) -o main.out main.o qr.o $(LIB) $(LDFLAGS)

main.o: main.c
	$(CC) $(CFLAGS) main.c -o main.o

qr.o: qr.c qr.h
	$(CC) $(CFLAGS) qr.c -o qr.o

clean:
	rm -f *.o *.out
