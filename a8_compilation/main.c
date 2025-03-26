#include <stdio.h>
#include <stdlib.h>
#include "matrix_vector.h"
#include "cholesky.h"
#include "ausgabe.h"

int main (int argc, char* argv[])
{
   int n;
   double **a;
   double *b, *x;
   FILE *datei = 0;

   printf("(main) main wird aufgerufen\n");

   if(argc < 2)
   {
	   printf("(main) Datei muss übergeben werden!\n");
	   return 255;
   }
   
   datei = fopen(argv[1], "r");
    if (!datei) {
        perror("(main) Fehler beim Öffnen der Datei");
        return 1;
    }

   printf("(main) Datei geoeffnet: %s\n", argv[1]);
   
   a = read_matrix(datei, &n);
   printf("(main) Adresse von a: %p\n", (void*)a);  // Ausgabe der Adresse von a

   if(a == NULL) {
       fprintf(stderr, "(main) Fehler beim Lesen der Matrix\n");
       fclose(datei);
       return 1;
   }
   
   // Temporäre Ausgabe der Matrix
   printf("(main) Überprüfe die Werte der Matrix:\n");
   for (int i = 0; i < n; i++) {
       for (int j = 0; j < n; j++) {
           printf("(main) a[%d][%d] = %10.5f ", i, j, a[i][j]);
       }
       printf("\n");
   }
   printf("(main) Ende Ausgabe Matrix\n");

   b = read_vector(datei, n);
   if(b == NULL) {
       fprintf(stderr, "(main) Fehler beim Lesen des Vektors\n");
       free_matrix(a, n);
       fclose(datei);
       return 2;
   }

   x = new_vector(n);
   if(x == NULL) {
       fprintf(stderr, "(main) Fehler beim Erstellen des Lösungsvektors\n");
       free_matrix(a, n);
       free(b);
       fclose(datei);
       return 3;
   }

   printf("(main) Daten erfolgreich gelesen\n");

   cholesky(a, b, x, n);
   printf("(main) \nLoesung:\n");

   
   if (argc == 3) {
       FILE *outfile = fopen(argv[2], "w");
       if (outfile != NULL) {
           for (int i = 0; i < n; i++) {
               fprintf(outfile, "%10.5f\n", x[i]);
           }
           fclose(outfile);
           print_vector_plain(x, n);
           printf("(main) Lösung wurde in %s geschrieben\n", argv[2]);
       } else {
           fprintf(stderr, "(main) Konnte Datei %s nicht öffnen\n", argv[2]);
       }
   } else {
       print_vector_plain(x, n);
   }
   

   printf("\n");
   
   free_matrix(a, n);
   free(b);
   free(x);
   fclose(datei);

   printf("(main) main erfolgreich beendet\n");
   return 0;
}