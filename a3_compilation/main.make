CC = gcc
CFLAGS = -Wall -c -I../lib

SRC = a3_compilation/main.c
OBJ = a3_compilation/main.o

all: $(OBJ)

$(OBJ): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(OBJ)

clean:
	rm -f a3_compilation/*.o a3_compilation/*.out
