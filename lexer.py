import ply.lex as lex

# Słowa kluczowe (zarezerwowane)
reserved = {
    'BEGIN': 'BEGIN', 'END': 'END', 'DEF': 'DEF', 'ARRAY': 'ARRAY',
    'IF': 'IF', 'THEN': 'THEN', 'ELSE': 'ELSE', 'WHILE': 'WHILE',
    'DO': 'DO', 'FOR': 'FOR', 'TO': 'TO', 'RETURN': 'RETURN',
    'AND': 'AND', 'OR': 'OR', 'NOT': 'NOT', 'TRUE': 'TRUE',
    'FALSE': 'FALSE', 'WRITE': 'WRITE', 'READ': 'READ', 'MOD': 'MULT_OP'
}

# Lista tokenów (łączymy nasze tokeny ze słowami kluczowymi)
tokens = [
    'STR', 'IDENTIFIER', 'FLOAT', 'INTEGER',
    'ASSIGN', 'RELOP', 'ADD_OP', 'MULT_OP',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
    'COMMA', 'SEMICOLON', 'DOT'
] + list(set(reserved.values()))

# Proste reguły wyrażeń regularnych dla tokenów
t_ASSIGN    = r':='
t_RELOP     = r'==|!=|<=|>=|<|>'
t_ADD_OP    = r'\+|-'
t_MULT_OP   = r'\*|/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_COMMA     = r','
t_SEMICOLON = r';'
t_DOT       = r'\.'

# Ignorowane znaki (spacje, taby)
t_ignore = ' \t\r'

# Komentarze (ignorowane)
def t_COMMENT(t):
    r'(//.*)|(\#.*)'
    pass

# Napisy
def t_STR(t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1] # Usuwamy cudzysłowy
    return t

# Liczby zmiennoprzecinkowe
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Liczby całkowite
def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Identyfikatory i słowa kluczowe
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Sprawdzamy czy identyfikator nie jest słowem kluczowym (np. IF, WHILE)
    t.type = reserved.get(t.value.upper(), 'IDENTIFIER')
    return t

# Obsługa nowych linii
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Obsługa błędów skanera
def t_error(t):
    print(f"Błąd skanera: Nieznany znak '{t.value[0]}' w linii {t.lexer.lineno}")
    t.lexer.skip(1)

# Budowa leksera
lexer = lex.lex()
