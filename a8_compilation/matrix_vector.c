#include<stdio.h>
#include<stdlib.h>
#include "ausgabe.h"

#define LINEBUF 256

double* new_vector(int n)
{
	double* v;
	printf("n*(double) = %ld\n", n*sizeof(double));
	v = (double *) malloc(n * sizeof(double));

	return v;
}

double** new_matrix(int n, int m)
{
	/* erstelle zeiger auf zeiger */
	double **mat;						
	int j;
	printf("n*(double*) = %ld\n", n*sizeof(double*));

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

double* read_vector(FILE *inputfile, int n)
{
	int i;

	double *b; 
	b = new_vector(n);
	if (b == NULL) return NULL;

	/* Lese elemente für b ein */
	for (i = 0; i < n; i++ ) 
	{
		fscanf(inputfile,"%lf", &(b[i]) );
		printf("%f   ",b[i]);
	}
	printf("\n");

	return b;
}

double** read_matrix(FILE *inputfile, int *n)
{
	int i,j;

	double **a = NULL;

	char buf[LINEBUF];

	*n = 0;
	while ( fgets(buf, LINEBUF, inputfile) != NULL)
	{
		(*n)++;
	}
	(*n)--;
	printf("Anzahl Zeilen: %i\n", *n);

	rewind(inputfile);

	a = new_matrix(*n,*n);
	if (a == NULL) return NULL;

	/* Lese elemente für A ein */
	for (i = 0; i < *n; i++ ) 
	{
		//printf("i = %d\n", i);
		for (j = 0; j < *n; j++) 
		{
			//printf("j = %d\n", j);
			//printf("%f\n", a[i][j]);
			fscanf(inputfile,"%lf", &(a[i][j]));
			//printf("%f   ", a[i][j]);
		}
		//printf("\n");
	}

	print_matrix(a, *n);
	return a;
}


