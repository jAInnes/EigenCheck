#include<stdio.h>
void print_vector(double *v, int n);
void print_matrix(double **a, int n, int m);
double** read_matrix(FILE *inputfile, int *n, int *m);
double* read_vector(FILE *inputfile, int n);
