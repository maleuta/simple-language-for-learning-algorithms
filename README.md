# Prosty język dla nauki algorytmów

1. Dane studentów:
  - Yuliya Matsulevich, matsyuliya@student.agh.edu.pl
  - Marta Ronchyk, martaronchyk@student.agh.edu.pl

2. Założenia programu:
  - Ogólne cele: Stworzenie przejrzystego środowiska do uruchamiania algorytmów bez zbędnego "szumu" składniowego. Język wspiera podstawowe struktury danych i sterowania.

  - Rodzaj translatora: Interpreter

  - Planowany wynik: Program, który po wczytaniu pliku wykonuje obliczenia, obsługuje interakcję z użytkownikiem (wejście/wyjście) i zarządza stanem zmiennych w czasie rzeczywistym.

  - Język implementacji: Python 3.11

  - Sposób realizacji skanera/parsera: Wykorzystanie generatora PLY (Python Lex-Yacc). Skaner bazuje na wyrażeniach regularnych, a parser implementuje gramatykę bezkontekstową typu LALR.

3. Opis tokenów:

| Kod Tokena        | Reguła / Wartość        | Opis                                                         |
|-------------------|------------------------|--------------------------------------------------------------|
| BEGIN             | BEGIN                  | Otwarcie bloku programu                                      |
| END               | END                    | Zamknięcie bloku programu                                    |
| IF                | IF                     | Słowa kluczowe instrukcji warunkowej                         |
| THEN              | THEN                   | Wprowadzenie bloku instrukcji po spełnieniu warunku          |
| ELSE              | ELSE                   | Opcjonalny blok instrukcji                                   |
| WHILE             | WHILE                  | Początek pętli                                               |
| DO                | DO                     | Wprowadzenie ciała pętli                                     |
| WRITE             | WRITE                  | Instrukcja wyjścia                                           |
| READ              | READ                   | Instrukcja wejścia                                           |
| IDENTIFIER        | [a-zA-Z_][a-zA-Z0-9_]* | Nazwy zmiennych (zaczynające się od litery lub podkreślnika) |
| INTEGER           | [0-9]+                 | Liczby całkowite                                             |
| FLOAT             | [0-9]+\.[0-9]+         | Liczby zmiennoprzecinkowe                                    |
| ASSIGN            | :=                     | Operator przypisania wartości                                |
| RELOP             | =, !=, <, >, <=, >=    | Operatory porównania logicznego (relacyjne)                  |
| ADD_OP            | +, -,                  | Operatory o niskim priorytecie                               |
| MULT_OP           | *, /                   | Operatory o wysokim priorytecie                              |
| LPAREN            | (                      | Nawias otwierający                                           |
| RPAREN            | )                      | Nawias zamykający                                            |
| SEMICOLON         | ;                      | Separator instrukcji                                         |
| DOT               | .                      | Znak kończący strukturę programu                             |



4. Gramatyka:
"Program_sym" = "Blok" Kropka.

"Blok" = "Begin_sym" "Instrukcja" {"Srednik" "Instrukcja"} "End_sym".

"Instrukcja" =
      "Instr_podstaw"
    | "Instr_if"
    | "Instr_while"
    | "Instr_io"
    | "Blok".

"Instr_podstaw" = Ident "Przypisz" "Wyrazenie".

"Instr_if" =
    "If_sym" "Warunek" "Then_sym" "Instrukcja"
    [ "Else_sym" "Instrukcja" ].

"Instr_while" =
    "While_sym" "Warunek" "Do_sym" "Instrukcja".

"Instr_io" =
      "Write_sym" "Wyrazenie"
    | "Read_sym" Ident.

"Warunek" = "Wyrazenie" "Relop" "Wyrazenie".

"Wyrazenie" =
    "Skladnik" { "Add_op" "Skladnik" }.

"Skladnik" =
    "Czynnik" { "Mult_op" "Czynnik" }.

"Czynnik" =
      Ident
    | Integer
    | Float
    | Lewy_nawias "Wyrazenie" Prawy_nawias.
