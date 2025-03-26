# Compiler & Optionen
CC=gcc
CCFLAGS=-O -Wall -fPIC  # ✅ -fPIC für Position Independent Code
AR=ar
ARFLAGS=rcs

# Globale Objekte (werden nur einmal kompiliert)
GLOBAL_OBJECTS=ausgabe.o matrix_vector.o
LIBRARY=global_lib.a

# Ziel: Kompiliere globale Dateien in eine statische Bibliothek
all: $(LIBRARY)

$(LIBRARY): $(GLOBAL_OBJECTS)
	$(AR) $(ARFLAGS) $@ $^

# Generiere .o-Dateien aus .c-Dateien
%.o: %.c
	$(CC) $(CCFLAGS) -c $< -o $@

clean:
	rm -f *.o
	rm -f $(LIBRARY)

# c -O -Wall -I. -c ausgabe.c -o ausgabe.o in cd compilation anwenden bei änderungen in Ausgabe.c