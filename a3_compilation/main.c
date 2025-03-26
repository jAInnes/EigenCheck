#include<stdio.h>
#include<math.h>
#include<stdlib.h>
#include"matrix_vector.h"
#include"qr.h"

double* new_vector(int n)
{
   double* v;
   v = (double *) malloc(n * sizeof(double));

   return v;
}

double** new_matrix(int n, int m)
{
   /* erstelle zeiger auf zeiger */
   double **mat;						
   int j;

   /* Stelle n-Speicherplaetze vom Typ double* zur Verfügung */
   mat = (double **) malloc(n*sizeof(double* ));
   if(mat == NULL) return NULL;
   
   for (j=0; j<n; j++)									
   {	                                
      /* weise den restlichen Zeigern jeweils eine Zeile zu */
       mat[j] = (double* ) malloc(m*sizeof(double));
       if(mat[j] == NULL) return NULL;
   }
	
   /* gebe Zeiger zurueck, der auf n*m-Speicherplaetze verweist */
   return mat;					

}

void free_matrix(double **mat, int n)
{
   int i;
   for(i = 0; i < n; i++)
      free(mat[i]);
   free(mat);
}

int main(int argc, char* argv[])
{
   int n,m;

   double **a;
   double *b, *x;
   FILE *datei = 0;

   if(argc == 1)
   {
	   printf("Keine Datei uebergeben!\n");
	   return -1;
   }

   datei = fopen(argv[1], "r");
   
   a = read_matrix(datei, &m, &n);
   printf("%p   \n", a);
   if(a == NULL) return 1;
   //print_matrix(a, m, n);

   b = read_vector(datei, m);
   if(b == NULL) return 2;
   //print_vector(b, m);

   x = new_vector(n);
   if(x == NULL) return 3;

   qr(a, b, x, m, n);
   printf("\nNach QR-Zerlegung:\n");
   print_matrix(a, m, n);
   printf("\nVektor b:\n");
   print_vector(b, m);
   printf("\nLoesung:\n");
   rueckwarts_einsetzen(a, b, x, n, m);
   if (argc == 3) {
      FILE *outfile = fopen(argv[2], "w");
      if (outfile != NULL) {
          for (int i = 0; i < n; i++) {
              fprintf(outfile, "%10.5f\n", x[i]);
          }
          fclose(outfile);
          print_vector(x, n);
          printf("Lösung wurde in %s geschrieben\n", argv[2]);
      } else {
          fprintf(stderr, "Konnte Datei %s nicht öffnen\n", argv[2]);
      }
  } else {
      print_vector(x, n);
  }
  
   printf("\n");
   
   free_matrix(a, m);
   free(b);
   free(x);

   return 0;
}

