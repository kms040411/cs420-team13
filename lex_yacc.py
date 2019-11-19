import ply.lex as lex
import ply.yacc as yacc
import sys
from enum import Enum, auto

class AST_TYPE(Enum):
	TYPE = auto()
	PROGRAM = auto()
	FUNCTION = auto()
	DECLARATION = auto()
	BLOCK = auto()
	ID = auto()
	FUN_VAR_DEC = auto()
	STATEMENTS = auto()
	VAR_DEC = auto()
	COND = auto()
	IF = auto()
	ELIF_ELSE = auto()
	ELIF = auto()
	ELSE = auto()
	FUN_APP = auto()
	ARGS = auto()
	VAR_AND_ASSIGN = auto()
	LOOP_INIT = auto()
	PRINT_FORMATS = auto()
	PTRS = auto()
	ARRAY_DECS = auto()

class ptr_type():
	def __init__(self, type, depth):
		self.type = type
		self.depth = depth

class arr_type():
	def __init__(self, type, dims):
		self.type = type
		self.dims = dims

class fun_app():
	def __init__(self, fname, arguments):
		self.fname = fname
		self.arguments = arguments

class loop():
	def __init__(self, type, init_expr, term_expr, update_expr, body):
		self.type = type
		self.init_expr = init_expr
		self.term_expr = term_expr
		self.update_expr = update_expr
		self.body = body

class AST():
	def __init__(self, start_lineno, end_lineno, token, AST_type, left = None, right = None):
		self.start_lineno = start_lineno
		self.end_lineno = end_lineno
		self.token = token
		self.left = left
		self.right = right
		self.type = AST_type

	def copy_AST(start_lineno, end_lineno, old_AST):
		return AST(start_lineno, end_lineno, old_AST.token, old_AST.left, old_AST.right, old_AST.type)

	def get(self):
		return self.token

class c_function():
	def __init__(self, function_name, return_type, params, body):
		self.name = function_name
		self.return_type = return_type
		self.params = params
		self.body = body

tokens = [
	'INT_VAL',
	'FLOAT_VAL',
	'ID',
	'PLUS',
	'MINUS',
	'MULTIPLY',
	'DIVIDE',
	'LPAREN',
	'RPAREN',
	'LBRACE',
	'RBRACE',
	'SQ_RBRACKET',
	'SQ_LBRACKET',
	'SEMI',
	'EQ',
	'COMMA',
	'PTR_AMP',
	'LESS',
	'GREATER',
	'STRING',

]

reserved = {
	'if' : 'IF',
	'else' : 'ELSE',
	'while' : 'WHILE',
	'for' : 'FOR',
	'int' : 'INT',
	'float' : 'FLOAT',
	'return' : 'RETURN',
	'void' : 'VOID',
	'printf' : 'PRINTF',
}

tokens = tokens + list(reserved.values())
 
# Regular expression rules for simple tokens
t_PLUS			= r'\+'
t_MINUS			= r'\-'
t_MULTIPLY		= r'\*'
t_DIVIDE		= r'\/'
t_LPAREN		= r'\('
t_RPAREN		= r'\)'
t_LBRACE 		= r'\{'
t_RBRACE 		= r'\}'
t_SQ_LBRACKET 	= r'\['
t_SQ_RBRACKET 	= r'\]'
t_SEMI 			= r'\;'
t_EQ 			= r'\='
t_COMMA			= r'\,'
t_PTR_AMP		= r'\&'
t_LESS			= r'\<'
t_GREATER		= r'\>'
t_STRING 		= r'\"(\\.|[^"\\])*\"'
# A regular expression rule with some action code

def t_FLOAT(t):
	r'\d+\.\d+'
	t.value = float(t.value)
	return t

def t_INT(t):
	r'\d+'
	t.value = int(t.value)    
	return t

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'ID')    # Check for reserved words
	return t

# Define a rule so we can track line numbers
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def p_program(p):
	'''program : function program
			   | function'''
	if __debug__ == False:
		print('PROGRAM')
	if(len(p) == 2):
		p[0] = AST(p.lineno(1), p.lineno(1), [p[1]], AST_TYPE.PROGRAM)
	else:
		p[0] = AST(p.lineno(1), p[2].end_lineno, [p[1]] + p[2].get(), AST_TYPE.PROGRAM) 

def p_function(p):
	'''function : type id variable_declaration block'''
	if __debug__ == False:
		print('FUNCTION')
	p[0] = AST(p[1].start_lineno, p[4].end_lineno, c_function(p[2].get(), p[1].get(), p[3].get(), p[4]), AST_TYPE.FUNCTION)

def p_type(p):
	'''type : INT
			| FLOAT'''
	if __debug__ == False:
		print('TYPE')
	p[0] = AST(p.lineno(1), p.lineno(1), p[1], AST_TYPE.TYPE)

def p_id(p):
	'''id : ID'''
	if __debug__ == False:
		print('ID')
	p[0] = AST(p.lineno(1), p.lineno(1), p[1], AST_TYPE.ID)

def p_varaible_declaration(p):
	'''variable_declaration : LPAREN declarations RPAREN'''
	if __debug__ == False:
		print('VAR_DEC')
	p[0] = AST.copy_AST(p.lineno(1), p.lineno(3), p[2])

def p_declarations(p):
	'''declarations : type id COMMA declarations
					| type id array_decs COMMA declarations
					| type ptrs id COMMA declarations
					| type id
					| type id array_decs
				    | type ptrs id
				    | VOID'''
	# len of RHS - 5 6 6 3 4 4 2
	if __debug__ == False:
		print('DECS')
	if(len(p) == 5):
		p[0] = AST(p[1].start_lineno, p[4].end_lineno, [(p[1].get(), p[2].get())] + p[4].get(), AST_TYPE.FUN_VAR_DEC)  
	elif(len(p) == 6):
		if(p[2].type == AST_TYPE.PTRS):
			p[0] = AST(p[1].start_lineno, p[5].end_lineno, [(ptr_type(p[1].get(), p[2].get()), p[3].get())] + p[5].get(), AST_TYPE.FUN_VAR_DEC)
		else:
			p[0] = AST(p[1].start_lineno, p[5].end_lineno, [(arr_type(p[1].get(), p[3].get()), p[2].get())] + p[5].get(), AST_TYPE_FUN_VAR_DEC)
	elif(len(p) == 3):
		p[0] = AST(p[1].start_lineno, p[2].end_lineno, [(p[1].get(), p[2].get())], AST_TYPE.FUN_VAR_DEC)
	elif(len(p) == 4):
		if(p[2].type == AST_TYPE.PTRS):
			p[0] = AST(p[1].start_lineno, p[3].end_lineno, [(ptr_type(p[1].get(), p[2].get()), p[3].get())], AST_TYPE.FUN_VAR_DEC)
		else:
			p[0] = AST(p[1].start_lineno, p[3].end_lineno, [(arr_type(p[1].get(), p[3].get()), p[2].get())], AST_TYPE_FUN_VAR_DEC)
	else:
		p[0] = AST(p.lineno(1), p.lineno(1), [], AST_TYPE.FUN_VAR_DEC)

def p_array_decs(p):
	'''array_decs : LPAREN INT_VAL RPAREN array_decs
				  | LPAREN INT_VAL RPAREN'''
	if(len(p) == 5):
		p[0] = AST(p.lineno(1), p.endlineno(4), [p[2]] + p[4].get(), AST_TYPE_ARRAY_DECS)
	else:
		p[0] = AST(p.lineno(1), p.lineno(3), [p[2]], AST_TYPE_ARRAY_DECS)
def p_ptrs(p):
	'''ptrs : MULTIPLY ptrs
		    | MULTIPLY'''
	if(len(p) == 3):
		p[0] = AST(p.lineno(1), p[2].end_lineno, p[2].get() + 1, AST_TYPE.PTRS)
	else:
		p[0] = AST(p.lineno(1), p.lineno(1), 1, AST_TYPE.PTRS)

def p_block(p):
	'''block : LBRACE statements RBRACE'''
	if __debug__ == False:
		print('BLOCK')
	p[0] = AST(p.lineno(1), p.lineno(3), 'block', TYPE.BLOCK, p[2])

def p_statements(p):
	'''statements : semi_statement
				  | non_semi_statement
			      | semi_statement SEMI statements
			      | non_semi_statement statements'''
	if __debug__ == False:
		print('STATEMENTS')
	if(len(p) == 2):
		p[0] = AST(p[1].start_lineno, p[1].end_lineno, 'statements', AST_TYPE.STATEMENTS, p[1])
	elif(len(p) == 3):
		p[0] = AST(p[1].start_lineno, p[3].end_lineno, 'statements', AST_TYPE.STATEMENTS, p[1], p[2])
	else:
		p[0] = AST(p[1].start_lineno, p[2].end_lineno, 'statements', AST_TYPE.STATEMENTS, p[1], p[3])

def p_semi_statement(p):
	'''semi_statement : var_declaration
					  | var_assignment
					  | function_app'''
	if __debug__ == False:
		print('SEMI_STATEMENT')
	p[0] = p[1]

def p_non_semi_statement(p):
	'''non_semi_statement : conditional
						  | for
						  | while'''
	if __debug__ == False:
		print('NON_SEMI_STATEMENT')
	p[0] = p[1]

def p_conditional(p):
	'''conditional : if elif_else'''
	if __debug__ == False:
		print('CONDITIONAL')
	if(p[2] != None):
		p[0] = AST(p[1].start_lineno, p[2].end_lineno, 'conditional', AST_TYPE.COND, p[1], p[2])
	elif(p[2] == None):
		p[0] = AST(p[1].start_lineno, p[1].end_lineno, 'conditional', AST_TYPE.COND, p[1])		

def p_if(p):
	'''if : IF LPAREN expression RPAREN block'''
	if __debug__ == False:
		print('IF')
	p[0] = AST(p.lineno(1), p[5].end_lineno, p[3], AST_TYPE.IF, p[5])

def p_elif_else(p):
	'''elif_else : elif else'''
	if __debug__ == False:
		print('ELIF_ELSE')
	if(p[1] == None and p[2] == None):
		p[0] = None
	elif(p[1] == None and p[2] != None):
		p[0] = AST(p[2].start_lineno, p[2].end_lineno, 'elif_else', AST_TYPE.ELIF_ELSE, p[2])		
	elif(p[1] != None and p[2] == None):
		p[0] = AST(p[1].start_lineno, p[1].end_lineno, 'elif_else', AST_TYPE.ELIF_ELSE, p[1])
	elif(p[1] != None and p[2] != None):
		p[0] = AST(p[1].start_lineno, p[2].end_lineno, 'elif_else', AST_TYPE.ELIF_ELSE, p[1], p[2])


def p_elif(p):
	'''elif : ELSE IF LPAREN expression RPAREN block elif
			| empty'''
	if __debug__ == False:
		print('ELIF')
	if(len(p) == 2):
		p[0] = None
	else:
		if(p[7] != None):
			p[0] = AST(p.lineno(1), p[7].end_lineno, p[4], AST_TYPE.ELIF, p[6], p[7])
		else:
			p[0] = AST(p.lineno(1), p[6].end_lineno, p[4], AST_TYPE.ELIF, p[6])			

def p_else(p):
	'''else : ELSE block
			| empty'''
	if __debug__ == False:
		print('ELSE')
	if(len(p) == 2):
		p[0] = None
	else:
		p[0] = AST(p.lineno(1), p[2].end_lineno, 'else', AST_TYPE.ELSE, p[2])


def p_for(p):
	'''for : FOR LPAREN loop_init_or_empty SEMI semi_statement_or_empty SEMI semi_statement_or_empty RPAREN block'''
	if __debug__ == False:
		print('FOR')
	p[0] = AST(p.lineno(1), p[9].end_lineno, loop(p[3], p[5], p[7], p[9]), AST_TYPE_FOR)

def p_loop_init_or_empty(p):
	'''loop_init_or_empty : loop_init
						  | empty'''
	if __debug__ == False:
		print('INIT_OR_EMPTY')
	p[0] = p[1]

def p_semi_statement_or_empty(p):
	'''semi_statement_or_empty : semi_statement
						       | empty'''
	if __debug__ == False:
		print('EXPR_OR_EMPTY')
	p[0] = p[1]

def p_loop_init(p):
	'''loop_init : type var_assignment
				 | semi_statement'''
	if __debug__ == False:
		print('LOOP_INIT')
	if(len(p) == 3):
		p[0] = AST(p[1].start_lineno, p[2].end_lineno, (p[1].get(), p[2].get()), AST_TYPE.LOOP_INIT)
	else:
		p[0] = AST(p[1].start_lineno, p[1].end_lineno, p[1], AST_TYPE.LOOP_INIT)

def p_while(p):
	'''while : WHILE LPAREN expression RPAREN block'''
	if __debug__ == False:
		print('WHILE')
	p[0] = AST(p.lineno(1), p[5].end_lineno, loop(None, p[3], None, p[5]), AST_TYPE.WHILE)

def p_var_declaration(p):
	'''var_declaration : type var_and_assign'''
	if __debug__ == False:
		print('VAR_DEC')
	p[0] = AST(map(lambda x : (p[1].get(), x), p[2].get()), AST_TYPE.VAR_DEC)

def p_var_assignment(p):
	'''var_assignment : ID EQ expression
					  | ID EQ function_app'''
	if __debug__ == False:
		print('VAR_ASSIGN')
	p[0] = AST((p[1], p[3]), AST_TYPE.ASSIGN)
	print(p[1], p[3] + 'abcdef')

def p_var_and_assign(p):
	'''var_and_assign : var_assignment COMMA var_and_assign
					  | var_assignment
					  | ID COMMA var_and_assign
					  | ID'''
	if __debug__ == False:
		print('VAR_AND_ASSIGN')
	if(len(p) == 4):
		p[0] = AST([p[1]] + p[3].get(), AST_TYPE.VAR_AND_ASSIGN)
	elif(type(p[1]) is lex.LexToken):
		p[0] = AST([p[1]], AST_TYPE.VAR_AND_ASSIGN)
	else:
		p[0] = AST([p[1].get()], AST_TYPE.VAR_AND_ASSIGN)

def p_function_app(p):
	'''function_app : PRINTF LPAREN STRING print_formats RPAREN
					| ID LPAREN arguments RPAREN'''
	if __debug__ == False:
		print('FUNCTION_APP')
	if(len(p) == 5):
		p[0] = AST(fun_app(p[1], p[3].get()), AST_TYPE.FUNC_APP)
	else:
		p[0] = AST(fun_app('PRINTF', [p[3]] + p[4].get()), AST_TYPE_FUNC_APP)

def p_print_formats(p):
	'''print_formats : COMMA expression print_formats
					 | empty'''
	if __debug__ == False:
		print('PRINTF_FORMATS')
	if(len(p) == 3):
		p[0] = AST([p[2]] + p[3].get(), AST_TYPE.PRINT_FORMATS)
	else:
		p[0] = AST([], AST_TYPE.PRINT_FORMATS)

def p_arguments(p):
	'''arguments : expression arguments
				 | empty'''
	if __debug__ == False:
		print('ARGUMENTS')
	if(len(p) == 3):
		p[0] = AST([p[1]] + p[2].get(), AST_TYPE.ARGS)
	else:
		p[0] = None

def p_empty(p):
	'''empty :'''
	p[0] = None

precedence = (
	('left', 'LESS', 'GREATER'),
	('left', 'PLUS', 'MINUS'),
	('left', 'MULTIPLY', 'DIVIDE'),
)

def p_expression(p):
	'''expression : expression PLUS expression
				  | expression MINUS expression
			 	  | expression MULTIPLY expression
			  	  | expression DIVIDE expression
			  	  | expression LESS expression
			  	  | expression GREATER expression
		  		  | LPAREN expression RPAREN
		  		  | MINUS expression
			  	  | ID
			  	  | INT_VAL
			  	  | FLOAT_VAL'''
	if(len(p) == 4):
		if(type(p[2]) is lex.LexToken):
			p[0] = AST(p[2], AST_TYPE.EXPR, p[1], p[3])
		else:
			p[0] = p[2]
	elif(len(p) == 3):
		p[0] = AST(p[1], AST_TYPE.EXPR, p[2])
	else:
		p[0] = AST(p[1], AST_TYPE.EXPR)

def p_error(p):
	print("Syntax error in input!")


def main():
	if(__name__ == '__main__'):
		with open('input.c', 'r') as file:
			data = file.read()
		lexer.input(data)
		while True:
			tok = lexer.token()
			if not tok:
				break
			print(tok)
		parser = yacc.yacc()
		parser.parse(data)

main()