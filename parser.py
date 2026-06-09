import ply.yacc as yacc
from lexer import tokens

# Symbol table
variables = {}

# =========================
# GRAMATYKA
# =========================

def p_program(p):
    '''program : declaration_list main_block DOT'''
    p[0] = ('PROGRAM', p[1], p[2])


def p_declaration_list(p):
    '''declaration_list : declaration_list function_decl
                        | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]] if p[1] else [p[2]]
    else:
        p[0] = []


def p_function_decl(p):
    '''function_decl : DEF IDENTIFIER LPAREN param_list RPAREN block'''
    p[0] = ('FUNC_DECL', p[2], p[4], p[6])


def p_param_list(p):
    '''param_list : param_list_nonempty
                  | empty'''
    p[0] = p[1] if p[1] else []


def p_param_list_nonempty(p):
    '''param_list_nonempty : param_list_nonempty COMMA IDENTIFIER
                           | IDENTIFIER'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_main_block(p):
    '''main_block : block'''
    p[0] = p[1]


def p_block(p):
    '''block : BEGIN statement_list END'''
    p[0] = ('BLOCK', p[2])


def p_statement_list(p):
    '''statement_list : statement_list statement SEMICOLON
                      | statement SEMICOLON'''
    if len(p) == 4:
        p[0] = p[1] + [p[2]] if p[1] else [p[2]]
    else:
        p[0] = [p[1]]


def p_statement(p):
    '''statement : assignment_stmt
                 | array_decl
                 | if_stmt
                 | while_stmt
                 | for_stmt
                 | read_stmt
                 | write_stmt
                 | return_stmt
                 | function_call_stmt
                 | block
                 | empty'''
    p[0] = p[1]


def p_empty(p):
    'empty :'
    p[0] = None


# =========================
# statements
# =========================

def p_array_decl(p):
    '''array_decl : ARRAY IDENTIFIER LBRACKET expression RBRACKET'''
    p[0] = ('ARRAY_DECL', p[2], p[4])


def p_assignment_stmt(p):
    '''assignment_stmt : IDENTIFIER ASSIGN expression
                       | IDENTIFIER LBRACKET expression RBRACKET ASSIGN expression'''
    if len(p) == 4:
        p[0] = ('ASSIGN', p[1], p[3])
    else:
        p[0] = ('ARRAY_ASSIGN', p[1], p[3], p[6])


def p_if_stmt(p):
    '''if_stmt : IF expression THEN statement
               | IF expression THEN statement ELSE statement'''
    if len(p) == 5:
        p[0] = ('IF', p[2], p[4], None)
    else:
        p[0] = ('IF', p[2], p[4], p[6])


def p_while_stmt(p):
    '''while_stmt : WHILE expression DO statement'''
    p[0] = ('WHILE', p[2], p[4])


def p_for_stmt(p):
    '''for_stmt : FOR IDENTIFIER ASSIGN expression TO expression DO statement'''
    p[0] = ('FOR', p[2], p[4], p[6], p[8])


def p_read_stmt(p):
    '''read_stmt : READ LPAREN IDENTIFIER RPAREN
                 | READ LPAREN IDENTIFIER LBRACKET expression RBRACKET RPAREN'''
    if len(p) == 5:
        p[0] = ('READ', p[3])
    else:
        p[0] = ('READ_ARRAY', p[3], p[5])


def p_write_stmt(p):
    '''write_stmt : WRITE LPAREN expression RPAREN'''
    p[0] = ('WRITE', p[3])


def p_return_stmt(p):
    '''return_stmt : RETURN expression'''
    p[0] = ('RETURN', p[2])


def p_function_call_stmt(p):
    '''function_call_stmt : IDENTIFIER LPAREN arg_list RPAREN'''
    p[0] = ('CALL', p[1], p[3])


# =========================
# ARGUMENTY
# =========================

def p_arg_list(p):
    '''arg_list : arg_list_nonempty
                | empty'''
    p[0] = p[1] if p[1] else []


def p_arg_list_nonempty(p):
    '''arg_list_nonempty : arg_list_nonempty COMMA expression
                         | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


# =========================
# EXPRESSIONS
# =========================

def p_expression(p):
    '''expression : logical_expression'''
    p[0] = p[1]


def p_logical_expression(p):
    '''logical_expression : logical_expression OR logical_and_expr
                          | logical_and_expr'''
    if len(p) == 4:
        p[0] = ('BINOP', p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_logical_and_expr(p):
    '''logical_and_expr : logical_and_expr AND rel_expr
                        | rel_expr'''
    if len(p) == 4:
        p[0] = ('BINOP', p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_rel_expr(p):
    '''rel_expr : math_expr RELOP math_expr
                | math_expr'''
    if len(p) == 4:
        p[0] = ('BINOP', p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_math_expr(p):
    '''math_expr : math_expr ADD_OP term
                 | term'''
    if len(p) == 4:
        p[0] = ('BINOP', p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_term(p):
    '''term : term MULT_OP factor
            | factor'''
    if len(p) == 4:
        p[0] = ('BINOP', p[2], p[1], p[3])
    else:
        p[0] = p[1]


# =========================
# FACTORS
# =========================

def p_factor(p):
    '''factor : IDENTIFIER
              | IDENTIFIER LBRACKET expression RBRACKET
              | IDENTIFIER LPAREN arg_list RPAREN
              | INTEGER
              | FLOAT
              | STR
              | TRUE
              | FALSE
              | LPAREN expression RPAREN
              | NOT factor
              | ADD_OP factor'''

    # INTEGER
    if len(p) == 2 and p.slice[1].type == 'INTEGER':
        p[0] = p[1]

    # FLOAT
    elif len(p) == 2 and p.slice[1].type == 'FLOAT':
        p[0] = p[1]

    # STRING
    elif len(p) == 2 and p.slice[1].type == 'STR':
        p[0] = p[1]

    # TRUE
    elif len(p) == 2 and p.slice[1].type == 'TRUE':
        p[0] = True

    # FALSE
    elif len(p) == 2 and p.slice[1].type == 'FALSE':
        p[0] = False

    # VARIABLE
    elif len(p) == 2 and p.slice[1].type == 'IDENTIFIER':
        p[0] = ('VAR', p[1])

    # ( expression )
    elif len(p) == 4 and p[1] == '(':
        p[0] = p[2]

    # array[index]
    elif len(p) == 5 and p[2] == '[':
        p[0] = ('ARRAY_GET', p[1], p[3])

    # function(...)
    elif len(p) == 5 and p[2] == '(':
        p[0] = ('CALL', p[1], p[3])

    # NOT expr
    elif len(p) == 3 and p[1] == 'NOT':
        p[0] = ('NOT', p[2])

    # unary + / -
    elif len(p) == 3 and p[1] in ('+', '-'):
        p[0] = ('UNARY', p[1], p[2])


# =========================
# OBSLUGA BŁĘDÓW
# =========================

def p_error(p):
    if p:
        print(f"Błąd składni w okolicach tokena '{p.value}' (linia {p.lineno})")
    else:
        print("Błąd składni: Nieoczekiwany koniec pliku")


# Build parser
parser = yacc.yacc()


# =========================
# OBSŁUGA BŁĘDÓW SEMANTYCZNYCH
# =========================
class SemanticError(Exception):
    pass

# =========================
# EXPRESSION EVALUATION
# =========================
def evaluate_expression(expr):
    if isinstance(expr, (int, float, str, bool)):
        return expr
    if expr is None:
        return None

    op = expr[0]

    if op == 'VAR':
        if expr[1] not in variables:
            raise SemanticError(f"Użycie niezainicjowanej zmiennej '{expr[1]}'.")
        return variables[expr[1]]

    elif op == 'BINOP':
        operator = expr[1]
        l_val = evaluate_expression(expr[2])
        r_val = evaluate_expression(expr[3])

        # Sprawdzanie dzielenia przez zero
        if operator in ('/', 'MOD') and r_val == 0:
            raise SemanticError("Dzielenie przez zero jest niedozwolone!")

        # Sprawdzanie zgodności typów dla operacji matematycznych
        if operator in ('+', '-', '*', '/', '>', '<', '>=', '<='):
            if type(l_val) != type(r_val) and not (isinstance(l_val, (int, float)) and isinstance(r_val, (int, float))):
                raise SemanticError(f"Niezgodność typów! Nie można wykonać '{operator}' między {type(l_val).__name__} a {type(r_val).__name__}.")

        if operator == '+': return l_val + r_val
        elif operator == '-': return l_val - r_val
        elif operator == '*': return l_val * r_val
        elif operator == '/': return l_val / r_val
        elif operator == '>': return l_val > r_val
        elif operator == '<': return l_val < r_val
        elif operator == '==': return l_val == r_val
        elif operator == '!=': return l_val != r_val
        elif operator == '>=': return l_val >= r_val
        elif operator == '<=': return l_val <= r_val
        elif operator == 'AND': return l_val and r_val
        elif operator == 'OR': return l_val or r_val

    elif op == 'NOT':
        return not evaluate_expression(expr[1])

    elif op == 'UNARY':
        operator = expr[1]
        value = evaluate_expression(expr[2])
        if operator == '-': return -value
        return value

    elif op == 'ARRAY_GET':
        if expr[1] not in variables:
            raise SemanticError(f"Tablica '{expr[1]}' nie istnieje.")
        idx = evaluate_expression(expr[2])
        if idx < 0 or idx >= len(variables[expr[1]]):
            raise SemanticError(f"Indeks {idx} wykracza poza rozmiar tablicy '{expr[1]}'.")
        return variables[expr[1]][idx]
    
    return 0

# =========================
# EXECUTOR
# =========================
def execute_ast(node):
    if node is None:
        return
    op = node[0]

    if op == 'PROGRAM':
        execute_ast(node[2])

    elif op == 'BLOCK':
        for stmt in node[1]:
            if stmt:
                execute_ast(stmt)

    elif op == 'WRITE':
        value = evaluate_expression(node[1])
        print(value)

    elif op == 'READ':
        val = input(f"{node[1]} = ")
        try:
            variables[node[1]] = int(val)
        except ValueError:
            try:
                variables[node[1]] = float(val)
            except ValueError:
                variables[node[1]] = val

    elif op == 'ASSIGN':
        value = evaluate_expression(node[2])
        variables[node[1]] = value

    elif op == 'IF':
        condition = evaluate_expression(node[1])
        if condition:
            execute_ast(node[2])
        elif node[3]:
            execute_ast(node[3])

    elif op == 'WHILE':
        while evaluate_expression(node[1]):
            execute_ast(node[2])

    elif op == 'FOR':
        var_name = node[1]
        start_val = evaluate_expression(node[2])
        end_val = evaluate_expression(node[3])
        variables[var_name] = start_val
        while variables[var_name] <= end_val:
            execute_ast(node[4])
            variables[var_name] += 1

    elif op == 'ARRAY_DECL':
        rozmiar = evaluate_expression(node[2])
        if rozmiar <= 0:
             raise SemanticError("Rozmiar tablicy musi być większy od 0.")
        variables[node[1]] = [0] * rozmiar

    elif op == 'ARRAY_ASSIGN':
        if node[1] not in variables:
             raise SemanticError(f"Tablica '{node[1]}' nie istnieje.")
        wartosc = evaluate_expression(node[3])
        indeks = evaluate_expression(node[2])
        if indeks < 0 or indeks >= len(variables[node[1]]):
            raise SemanticError(f"Indeks {indeks} wykracza poza rozmiar tablicy '{node[1]}'.")
        variables[node[1]][indeks] = wartosc

# =========================
# MAIN INTERPRETER ENTRY
# =========================
def run_interpreter(code):
    # Wyczyszczenie zmiennych przy każdym uruchomieniu (ważne dla trybu interaktywnego)
    variables.clear() 
    ast = parser.parse(code)
    if ast:
        try:
            execute_ast(ast)
        except SemanticError as e:
            print(f"\n[BŁĄD SEMANTYCZNY]: {e}")
        except Exception as e:
            print(f"\n[BŁĄD KRYTYCZNY INTERPRETERA]: {e}")