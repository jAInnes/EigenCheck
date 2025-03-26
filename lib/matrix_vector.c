#include<stdio.h>
#include<stdlib.h>
#include "matrix_vector.h"

void print_vector(double *v, int n)
{
   int i;

   for(i = 0; i < n; i++)
   {
      printf("%10.5f", v[i]);
      printf("\n");
   }
}

void print_matrix(double **a, int n, int m)
{
   int i, j;

   for(i = 0; i < n; i++)
   {
      for(j = 0; j < m; j++)
      {
         printf("%10.5f", a[i][j]);
      }
      printf("\n");
   }
}

double* read_vector(FILE *inputfile, int n)
{
   int i;

   double *b; 
   b = (double *) malloc(n * sizeof(double));
   if (b == NULL) return NULL;
   
   /* Lese elemente für b ein */
   for (i = 0; i < n; i++ ) 
   {
      fscanf(inputfile,"%lf", &(b[i]) );
   }
   print_vector(b, n);

   return b;
}

double** read_matrix(FILE *inputfile, int *n, int *m)
{
   int i,j;

   double **a = NULL;

   fscanf (inputfile,"%d", n);
   fscanf (inputfile,"%d", m);
   printf("%d\n",*n);
   printf("%d\n",*m);

   a = (double **) malloc(*n * sizeof(double* ));
   if(a == NULL) return NULL;

   /* Lese elemente für A ein */
   for (i = 0; i < *n; i++ ) 
   {
      a[i] = (double* ) malloc(*m * sizeof(double));
	  if(a[i] == NULL) return NULL;

      for (j = 0; j < *m; j++) 
      {
         fscanf(inputfile,"%lf", &(a[i][j]));
      }
   }

   print_matrix(a, *n, *m);
   return a;
}


