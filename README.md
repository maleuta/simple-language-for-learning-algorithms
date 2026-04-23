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

| Kod Tokena        | Reguła / Wartość        | Opis                                                                      |
|-------------------|------------------------|----------------------------------------------------------------------------|
| BEGIN             | BEGIN                  | Otwarcie bloku programu                                                    |
| END               | END                    | Zamknięcie bloku programu                                                  |
| IF                | IF                     | Słowa kluczowe instrukcji warunkowej                                       |
| THEN              | THEN                   | Wprowadzenie bloku instrukcji po spełnieniu warunku                        |
| ELSE              | ELSE                   | Opcjonalny blok instrukcji                                                 |
| WHILE             | WHILE                  | Początek pętli                                                             |
| DO                | DO                     | Wprowadzenie ciała pętli                                                   |
| FOR               | FOR                    | Słowo kluczowe rozpoczynające pętlę iteracyjną                             |
| TO                | TO                     | Słowo kluczowe określające górną granicę zakresu w pętli FOR               |
| RETURN            | RETURN                 | Instrukcja zwracająca wartość lub wymuszająca zakończenie bloku/programu   |
| AND               | AND                    | Operator logiczny koniunkcji (prawda, gdy oba warunki są prawdziwe)        |
| OR                | OR                     | Operator logiczny alternatywy (prawda, gdy minimum jeden warunek jest prawdziwy)       |
| NOT               | NOT                    | Operator logiczny negacji (odwraca wartość logiczną)                       |
| STR               | \"[^\"]*\"             | Ciąg znaków ujęty w podwójne cudzysłowy (np. "Witaj świecie")              |
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
```
program : block DOT

block : BEGIN statement_list END

statement_list : statement_list statement SEMICOLON
               | statement SEMICOLON

statement : assignment_stmt
          | if_stmt
          | while_stmt
          | for_stmt
          | read_stmt
          | write_stmt
          | return_stmt
          | block
          | empty

empty : /* Pusta reguła pozwalająca na nadmiarowe średniki lub puste linie */

assignment_stmt : IDENTIFIER ASSIGN expression

if_stmt : IF expression THEN statement
        | IF expression THEN statement ELSE statement

while_stmt : WHILE expression DO statement

for_stmt : FOR IDENTIFIER ASSIGN expression TO expression DO statement

read_stmt : READ LPAREN IDENTIFIER RPAREN

write_stmt : WRITE LPAREN expression RPAREN

return_stmt : RETURN expression

/* Priorytet 1: Alternatywa logiczna (OR) */
expression : expression OR logical_and_expr
           | logical_and_expr

/* Priorytet 2: Koniunkcja logiczna (AND) */
logical_and_expr : logical_and_expr AND rel_expr
                 | rel_expr

/* Priorytet 3: Operatory relacyjne (=, !=, <, >, <=, >=) */
rel_expr : math_expr RELOP math_expr
         | math_expr

/* Priorytet 4: Dodawanie i odejmowanie (+, -) */
math_expr : math_expr ADD_OP term
          | term

/* Priorytet 5: Mnożenie i dzielenie (*, /) */
term : term MULT_OP factor
     | factor

/* Priorytet 6: Czynniki bazowe, nawiasy, negacja, liczby ujemne i teksty */
factor : IDENTIFIER
       | INTEGER
       | FLOAT
       | STR
       | LPAREN expression RPAREN
       | NOT factor
       | ADD_OP factor  /* Umożliwia zapisywanie liczb ujemnych, np. -5 */
