# Compiler
CC = gcc
CFLAGS = -Wall -c

# Dateien
OBJS = matrix_vector.o
LIB = libmatrix.a

# Ziel: Bibliothek erzeugen
all: $(LIB)

# Bibliothek aus Objektdateien
$(LIB): $(OBJS)
	ar rcs $(LIB) $(OBJS)

# Objektdateien aus Quellen
matrix_vector.o: matrix_vector.c matrix_vector.h
	$(CC) $(CFLAGS) matrix_vector.c -o matrix_vector.o

# Clean
clean:
	rm -f *.o *.a
