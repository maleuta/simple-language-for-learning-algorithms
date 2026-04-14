# Prosty język dla nauki algorytmów

1. Dane studentów:
  - Yuliya Matsulevich, matsyuliya@student.agh.edu.pl
  - Marta Ronchyk, martaronchyk@student.agh.edu.pl

2. Założenia programu:
  - Ogólne cele: Stworzenie przejrzystego środowiska do uruchamiania algorytmów bez zbędnego "szumu" składniowego. Język wspiera podstawowe struktury danych i sterowania.

  - Rodzaj translatora: Interpreter

  - Planowany wynik: Program, który po wczytaniu pliku wykonuje obliczenia, obsługuje interakcję z użytkownikiem (wejście/wyjście) i zarządza stanem zmiennych w czasie rzeczywistym.

  - Język implementacji: Python 3.13

  - Sposób realizacji skanera/parsera: Wykorzystanie generatora PLY (Python Lex-Yacc). Skaner bazuje na wyrażeniach regularnych, a parser implementuje gramatykę bezkontekstową typu LALR.

3. Opis tokenów:

| Kod Tokena        | Reguła / Wartość        | Opis                                                         |
|-------------------|------------------------|--------------------------------------------------------------|
| BEGIN / END       | BEGIN, END             | Granice bloku głównego programu                              |
| IF / THEN / ELSE  | IF, THEN, ELSE         | Słowa kluczowe instrukcji warunkowej                         |
| WHILE / DO        | WHILE, DO              | Słowa kluczowe pętli warunkowej                              |
| WRITE / READ      | WRITE, READ            | Funkcje wejścia (klawiatura) i wyjścia (konsola)             |
| IDENTIFIER        | [a-zA-Z_][a-zA-Z0-9_]* | Nazwy zmiennych (zaczynające się od litery lub podkreślnika) |
| INTEGER           | [0-9]+                 | Liczby całkowite                                             |
| FLOAT             | [0-9]+\.[0-9]+         | Liczby zmiennoprzecinkowe                                    |
| ASSIGN            | :=                     | Operator przypisania wartości                                |
| RELOP             | =, !=, <, >, <=, >=    | Operatory porównania logicznego (relacyjne)                  |
| MATH_OP           | +, -, *, /             | Podstawowe operatory arytmetyczne                            |
| SEMICOLON         | ;                      | Separator instrukcji                                         |
| DOT               | .                      | Znak kończący strukturę programu                             |

4. Gramatyka formatu:
<program> ::= BEGIN <statements> END "."

<statements> ::= <statement>
               | <statement> ";" <statements>

<statement> ::= <assignment>
              | <if_statement>
              | <while_statement>
              | <write_statement>
              | <read_statement>

<assignment> ::= IDENTIFIER ":=" <expression>

<if_statement> ::= IF <condition> THEN <statement>
                 | IF <condition> THEN <statement> ELSE <statement>

<while_statement> ::= WHILE <condition> DO <statement>

<write_statement> ::= WRITE "(" <expression> ")"

<read_statement> ::= READ "(" IDENTIFIER ")"

<condition> ::= <expression> <relop> <expression>

<relop> ::= "=" | "!=" | "<" | ">" | "<=" | ">="

<expression> ::= <term>
               | <expression> "+" <term>
               | <expression> "-" <term>

<term> ::= <factor>
         | <term> "*" <factor>
         | <term> "/" <factor>

<factor> ::= IDENTIFIER
           | INTEGER
           | FLOAT
           | "(" <expression> ")"
