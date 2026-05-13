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

| Kod Tokena | Reguła | Opis |
|---|---|---|
| `BEGIN` | `BEGIN` | Otwarcie bloku programu |
| `END` | `END` | Zamknięcie bloku programu |
| `IF` | `IF` | Słowo kluczowe instrukcji warunkowej |
| `THEN` | `THEN` | Wprowadzenie bloku instrukcji po spełnieniu warunku |
| `ELSE` | `ELSE` | Opcjonalny blok instrukcji warunkowej |
| `WHILE` | `WHILE` | Początek pętli dopóki |
| `DO` | `DO` | Wprowadzenie ciała pętli |
| `FOR` | `FOR` | Słowo kluczowe rozpoczynające pętlę iteracyjną |
| `TO` | `TO` | Słowo kluczowe określające górną granicę w pętli FOR |
| `RETURN` | `RETURN` | Instrukcja zwracająca wartość lub zamykająca blok/program |
| `AND` | `AND` | Operator logiczny koniunkcji (prawda, gdy oba są prawdziwe) |
| `OR` | `OR` | Operator logiczny alternatywy (prawda, gdy minimum jeden jest prawdziwy) |
| `NOT` | `NOT` | Operator logiczny negacji (odwraca wartość logiczną) |
| `TRUE` | `TRUE` | Stała logiczna prawdy |
| `FALSE` | `FALSE` | Stała logiczna fałszu |
| `STR` | `\"[^\"]*\"` | Ciąg znaków ujęty w podwójne cudzysłowy (np. "Witaj") |
| `WRITE` | `WRITE` | Instrukcja wyjścia (wypisywanie na ekran) |
| `READ` | `READ` | Instrukcja wejścia (czytanie od użytkownika) |
| `IDENTIFIER` | `[a-zA-Z_][a-zA-Z0-9_]*` | Nazwy zmiennych (zaczynające się od litery lub podkreślnika) |
| `INTEGER` | `[0-9]+` | Liczby całkowite |
| `FLOAT` | `[0-9]+\.[0-9]+` | Liczby zmiennoprzecinkowe |
| `ASSIGN` | `:=` | Operator przypisania wartości |
| `RELOP` | `=`, `!=`, `<`, `>`, `<=`, `>=` | Operatory porównania logicznego (relacyjne) |
| `ADD_OP` | `+`, `-` | Operatory arytmetyczne o niskim priorytecie |
| `MULT_OP` | `*`, `/`, `MOD` | Operatory arytmetyczne o wysokim priorytecie (w tym reszta z dzielenia) |
| `LPAREN` | `(` | Nawias okrągły otwierający (grupowanie wyrażeń) |
| `RPAREN` | `)` | Nawias okrągły zamykający |
| `LBRACKET` | `[` | Nawias kwadratowy otwierający (indeksowanie tablic) |
| `RBRACKET` | `]` | Nawias kwadratowy zamykający (indeksowanie tablic) |
| `SEMICOLON`| `;` | Separator instrukcji |
| `DOT` | `.` | Znak kończący strukturę programu |
| `COMMENT` | `//.*` lub `#.*` | Komentarze jednolinijkowe (ignorowane przez parser) |



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
                | IDENTIFIER LBRACKET expression RBRACKET ASSIGN expression

if_stmt : IF expression THEN statement
        | IF expression THEN statement ELSE statement

while_stmt : WHILE expression DO statement

for_stmt : FOR IDENTIFIER ASSIGN expression TO expression DO statement

read_stmt : READ LPAREN IDENTIFIER RPAREN
          | READ LPAREN IDENTIFIER LBRACKET expression RBRACKET RPAREN

write_stmt : WRITE LPAREN expression RPAREN

return_stmt : RETURN expression

/* Punkt wejścia dla wszystkich wyrażeń */
expression : logical_expression

/* Priorytet 1: Alternatywa logiczna (OR) */
logical_expression : logical_expression OR logical_and_expr
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

/* Priorytet 6: Mnożenie, dzielenie i modulo (*, /, MOD) */
factor : IDENTIFIER
       | INTEGER
       | FLOAT
       | STR
       | TRUE
       | FALSE
       | LPAREN expression RPAREN
       | NOT factor
       | ADD_OP factor  /* Umożliwia zapisywanie liczb ujemnych, np. -5 */
