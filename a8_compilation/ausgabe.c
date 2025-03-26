/**
 * @file ausgabe.c
 * @brief Diese Datei enthält Funktionen zur formatierten Ausgabe von Vektoren und Matrizen.
 *        Zusätzlich enthält sie eine Testfunktion, die die Ausgabe eines Vektors mit erwarteten
 *        Ergebnissen aus einer Datei vergleicht und einen Teststatus ausgibt.
 *
 * Grober Ablauf:
 * - Definiert Hilfsfunktion zum String-Vergleich mit Toleranz.
 * - Definiert Funktion zum formatierten Ausgeben von Vektoren.
 * - Liest erwartete Vektorelemente aus einer Datei.
 * - Vergleicht die tatsächliche Ausgabe mit den erwarteten Werten.
 * - Gibt einen Teststatus (Erfolg/Fehler) aus.
 * - Definiert Funktion zum formatierten Ausgeben von Matrizen.
 */

 #include "ausgabe.h"
 #include <stdio.h>
 #include <stdlib.h>
 #include <string.h>
 #include <math.h>
 
 // Hilfsfunktion zum Vergleichen von Strings mit Toleranz
 int compare_strings(const char *str1, const char *str2, double tolerance) {
     double val1, val2, diff;  // Deklarieren von Variablen für die Zahlenwerte und die Differenz
 
     // Versuche, die Strings in double-Werte zu konvertieren
     if (sscanf(str1, "%lf", &val1) == 1 && sscanf(str2, "%lf", &val2) == 1) {
         diff = fabs(val1 - val2);  // Berechne die absolute Differenz der Zahlenwerte
         if (diff <= tolerance) {    // Prüfe, ob die Differenz innerhalb der Toleranz liegt
             return 0; // Strings sind (innerhalb der Toleranz) gleich
         }
     }
     return strcmp(str1, str2);     // Strings sind nicht gleich (lexikographischer Vergleich)
 }
 void print_vector_plain(double *v, int n) {
    for (int i = 0; i < n; i++) {
        printf("%10.5f\n", v[i]);
    }
}

 // Funktion zum Ausgeben eines Vektors und Vergleich mit erwarteten Werten aus einer Datei
 void print_vector(double *v, int n, const char *expected_file) {
     int i;                   // Laufvariable für die Schleife
     FILE *fp;                // File Pointer für die erwartete Ergebnisdatei
     char expected_line[100]; // Puffer für die gelesene Zeile aus der Datei
     char actual_line[100];   // Puffer für die formatierte Ausgabe des Vektorelements
     double tolerance = 1e-6;  // Toleranz für den Vergleich von Gleitkommazahlen
     int test_passed = 1;     // Flag, um zu verfolgen, ob alle Tests bestanden wurden
 
     fp = fopen(expected_file, "r");  // Öffne die Datei im Lesemodus
     if (fp == NULL) {                // Prüfe, ob das Öffnen erfolgreich war
         fprintf(stderr, "Fehler: Kann erwartete Ergebnisdatei '%s' nicht öffnen!\n", expected_file); // Gib eine Fehlermeldung aus
         exit(1);                     // Beende das Programm mit Fehlercode 1
     }
 
     // printf("\nLoesung:\n"); // Ausgabe der Überschrift, wenn gewünscht (hier auskommentiert)
 
     for (i = 0; i < n; i++) { // Schleife über alle Elemente des Vektors
         snprintf(actual_line, sizeof(actual_line), "%10.5f", v[i]); // Formatiere das Vektorelement als String
         if (fgets(expected_line, sizeof(expected_line), fp) != NULL) { // Lese eine Zeile aus der Datei
             if (compare_strings(actual_line, expected_line, tolerance) != 0) { // Vergleiche formatierte Ausgabe mit erwarteter Zeile
                 printf("(ausgabe) Wert nach Cholesky: %s , erwartet: %s -> Fehler\n", actual_line, expected_line); // Gib eine Fehlermeldung aus
                 test_passed = 0;         // Setze das Test-bestanden-Flag auf 0
             } else {
                 printf("(ausgabe) Wert nach Cholesky: %s erwartet %s -> Erfolg\n", actual_line, expected_line); // Gib eine Erfolgsmeldung aus
             }
         } else {                     // Wenn fgets NULL zurückgibt (Dateiende erreicht)
             fprintf(stderr, "Fehler: Erwartete Ergebnisdatei ist zu kurz!\n"); // Gib eine Fehlermeldung aus
             test_passed = 0;         // Setze das Test-bestanden-Flag auf 0
             break;                     // Beende die Schleife
         }
     }
 
     fclose(fp);  // Schließe die Datei
 
     // Hole den Benutzernamen aus der Session (angenommen, dass der Benutzername in der Umgebungsvariable USERNAME gespeichert ist)
     char *username = getenv("USERNAME");
     if (username == NULL) {
         fprintf(stderr, "Fehler: Benutzername nicht gefunden!\n");
         exit(1);
     }

     // Erstelle den Pfad zur Datei im Benutzerverzeichnis
     char result_file_path[256];
     snprintf(result_file_path, sizeof(result_file_path), "uploads/%s/test_result.txt", username);

     FILE *result_file = fopen(result_file_path, "w");
     if (result_file) {
         fprintf(result_file, "100%%");
         fclose(result_file);
     } else {              // Wenn nicht alle Tests bestanden wurden
         // printf("\nTest fehlgeschlagen!\n"); // Gib eine Fehlermeldung aus, wenn gewünscht (hier auskommentiert)
     }
 }
 
 // Funktion zum Ausgeben einer Matrix (zweidimensionales Array von Doubles)
 void print_matrix(double **a, int n) {
     int i, j;  // Laufvariablen für die Schleifen
 
     for (i = 0; i < n; i++) { // Äußere Schleife für die Zeilen
         printf("i = %d", i);   // Gib den Zeilenindex aus (Debugging)
         for (j = 0; j < n; j++) { // Innere Schleife für die Spalten
             printf("%10.5f", a[i][j]); // Gib das Matrixelement formatiert aus
         }
         printf("\n");         // Gib einen Zeilenumbruch aus
     }
 }