# Prosty język dla nauki algorytmów

## 1. Dane studentów:
  - Yuliya Matsulevich, matsyuliya@student.agh.edu.pl
  - Marta Ronchyk, martaronchyk@student.agh.edu.pl

## 2. Założenia programu:
  - Ogólne cele: Stworzenie przejrzystego środowiska do uruchamiania algorytmów bez zbędnego "szumu" składniowego. Język wspiera podstawowe struktury danych i sterowania.

  - Rodzaj translatora: Interpreter

  - Planowany wynik: Program, który po wczytaniu pliku wykonuje obliczenia, obsługuje interakcję z użytkownikiem (wejście/wyjście) i zarządza stanem zmiennych w czasie rzeczywistym.

  - Język implementacji: Python 3.11

  - Sposób realizacji skanera/parsera: Wykorzystanie generatora PLY (Python Lex-Yacc). Skaner bazuje na wyrażeniach regularnych, a parser implementuje gramatykę bezkontekstową typu LALR.

## 3. Opis tokenów:

| Kod Tokena | Reguła | Opis |
|---|---|---|
| `BEGIN` | `BEGIN` | Otwarcie bloku programu lub funkcji |
| `END` | `END` | Zamknięcie bloku programu lub funkcji |
| `DEF` | `DEF` | Słowo kluczowe definicji funkcji/procedury |
| `ARRAY` | `ARRAY` | Słowo kluczowe deklaracji tablicy |
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
| `IDENTIFIER` | `[a-zA-Z_][a-zA-Z0-9_]*` | Nazwy zmiennych i funkcji (zaczynające się od litery lub podkreślnika) |
| `INTEGER` | `[0-9]+` | Liczby całkowite |
| `FLOAT` | `[0-9]+\.[0-9]+` | Liczby zmiennoprzecinkowe |
| `ASSIGN` | `:=` | Operator przypisania wartości |
| `RELOP` | `==`, `!=`, `<`, `>`, `<=`, `>=` | Operatory porównania logicznego (relacyjne) |
| `ADD_OP` | `+`, `-` | Operatory arytmetyczne o niskim priorytecie |
| `MULT_OP` | `*`, `/`, `MOD` | Operatory arytmetyczne o wysokim priorytecie (w tym reszta z dzielenia) |
| `LPAREN` | `(` | Nawias okrągły otwierający (grupowanie wyrażeń, argumenty funkcji) |
| `RPAREN` | `)` | Nawias okrągły zamykający |
| `LBRACKET` | `[` | Nawias kwadratowy otwierający (indeksowanie i deklaracja tablic) |
| `RBRACKET` | `]` | Nawias kwadratowy zamykający (indeksowanie i deklaracja tablic) |
| `COMMA` | `,` | Separator argumentów w wywołaniach i definicjach funkcji |
| `SEMICOLON`| `;` | Separator instrukcji |
| `DOT` | `.` | Znak kończący strukturę programu |
| `COMMENT` | `//.*` lub `#.*` | Komentarze jednolinijkowe (ignorowane przez parser) |



## 4. Gramatyka:
```
/* Struktura ogólna programu */
program : declaration_list main_block DOT

declaration_list : declaration_list function_decl
                 | empty

function_decl : DEF IDENTIFIER LPAREN param_list RPAREN block

param_list : param_list_nonempty
           | empty

param_list_nonempty : param_list_nonempty COMMA IDENTIFIER
                    | IDENTIFIER

main_block : block

block : BEGIN statement_list END

statement_list : statement_list statement SEMICOLON
               | statement SEMICOLON

statement : assignment_stmt
          | array_decl
          | if_stmt
          | while_stmt
          | for_stmt
          | read_stmt
          | write_stmt
          | return_stmt
          | function_call_stmt
          | block
          | empty

empty : /* Pusta reguła */

/* Instrukcje */
array_decl : ARRAY IDENTIFIER LBRACKET expression RBRACKET

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

function_call_stmt : IDENTIFIER LPAREN arg_list RPAREN

/* Wywołanie funkcji i listy argumentów */
arg_list : arg_list_nonempty
         | empty

arg_list_nonempty : arg_list_nonempty COMMA expression
                  | expression

/* Wyrażenia z uwzględnieniem priorytetów */
expression : logical_expression

logical_expression : logical_expression OR logical_and_expr
                   | logical_and_expr

logical_and_expr : logical_and_expr AND rel_expr
                 | rel_expr

rel_expr : math_expr RELOP math_expr
         | math_expr

math_expr : math_expr ADD_OP term
          | term

term : term MULT_OP factor
     | factor

factor : IDENTIFIER
       | IDENTIFIER LBRACKET expression RBRACKET
       | IDENTIFIER LPAREN arg_list RPAREN
       | INTEGER
       | FLOAT
       | STR
       | TRUE
       | FALSE
       | LPAREN expression RPAREN
       | NOT factor
       | ADD_OP factor
```
## 5. Informacje o stosowanych generatorach i pakietach:
   
Projekt korzysta wyłącznie z wbudowanych bibliotek języka Python oraz z jednego pakietu zewnętrznego:
- PLY (Python Lex-Yacc) - Narzędzie to implementuje narzędzia lex oraz yacc znane z języka C. Pakiet nie tworzy zewnętrznych plików ze skompilowanym parserem, a przetwarza gramatykę w locie przy pomocy refleksji języka Python (docstrings).
- Moduł ply.lex odpowiada za tokenizację strumienia wejściowego na podstawie zdefiniowanych wyrażeń regularnych.
- Moduł ply.yacc buduje drzewo parsowania LALR w oparciu o gramatykę zdefiniowaną w postaci funkcji i łańcuchów znakowych, wyłapując wczesne błędy syntaktyczne.

## 6. Wymagania i instalacja
Projekt korzysta wyłącznie z wbudowanych bibliotek języka Python oraz z jednego pakietu zewnętrznego (PLY).

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/maleuta/simple-language-for-learning-algorithms.git
   cd simple-language-for-learning-algorithms
   ```

2. Zainstaluj wymagane zależności przy użyciu pliku requirements.txt:
```pip install -r requirements.txt ```

3. Struktura plików:

- ```lexer.py``` – plik skanera (leksera).

- ```parser.py``` – plik parsera syntaktycznego oraz logika interpretera.

- ```main.py``` – plik główny aplikacji.

- ```skrypt.txt``` – plik z kodem w naszym języku.

4. Uruchomienie interpretera:
Otwórz terminal w katalogu z projektem i wykonaj polecenie:
```python main.py skrypt.txt```

5. W konsoli pojawią się ewentualne komunikaty wykonania (efekty instrukcji WRITE) lub prośby o wprowadzenie danych (READ).
