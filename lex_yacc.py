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
	FUN_APP = auto()
	ARGS = auto()
	VAR_AND_ASSIGN = auto()
	SEMI_STATEMENT  = auto()
	NON_SEMI_STATEMENT = auto()
	ASSIGN = auto()
	LOOP_INIT = auto()
	PRINT_FORMATS = auto()
	PTRS = auto()
	ARRAY_DECS = auto()
	ARR_VAR = auto()
	PTR_VAR = auto()
	EXPR = auto()
	RETURN = auto()
	FOR = auto()
	WHILE = auto()

class ptr_type():
	def __init__(self, type, depth):
		self.type = type
		self.depth = depth

	def __repr__(self):
		return ("*" * self.depth + self.type)

class arr_type():
	def __init__(self, type, dims):
		self.type = type
		self.dims = dims

class fun_app():
	def __init__(self, fname, arguments):
		self.fname = fname
		self.arguments = arguments

class loop():
	def __init__(self, init_expr, term_expr, update_expr, body):
		self.init_expr = init_expr
		self.term_expr = term_expr
		self.update_expr = update_expr
		self.body = body

class AST():
	def __init__(self, start_lineno, end_lineno, content, AST_type, left = None, right = None):
		self.start_lineno = start_lineno
		self.end_lineno = end_lineno
		self.content = content
		self.left = left
		self.right = right
		self.type = AST_type

	def copy_AST(start_lineno, end_lineno, old_AST):
		return AST(start_lineno, end_lineno, old_AST.content, old_AST.type, old_AST.left, old_AST.right)
	def get(self):
		return self.content

	def __repr__(self):
		if(self.left == None):
				return (("line #%d :" % self.start_lineno) + " " + str(self.type) + " " + str(self.get()))
		elif(self.left != None and self.right == None):
				return (("line #%d :" % self.start_lineno) + " " + str(self.type) + " " + str(self.left.get()) + " " + str(self.get()))
		else:
			return (("line #%d :" % self.start_lineno) + " " + str(self.type) + " " + str(self.left.get()) + " " + str(self.get()) + " " + str(self.right.get()))			

	def get_str_expr(self):
		if(self.left == None):
			if(type(self.get()) == AST):
				return self.get().get_str_expr()
			else:
				if(self.type == AST_TYPE.ARR_VAR):
					ret_str = self.get()[1]
					for dim in self.get()[0]:
						ret_str += '[' + dim.get_str_expr() + ']'
					return ret_str
				elif(self.type == AST_TYPE.PTR_VAR):
					ret_str = '*' * self.get()[0]
					ret_str += self.get()[1]
					return ret_str
				elif(self.type == AST_TYPE.FUN_APP):
					fun = self.get()
					ret_str = fun.fname
					ret_str += '('
					for i in range(len(fun.arguments)):
						arg = fun.arguments[i]
						if(type(arg) == AST):
							ret_str += arg.get_str_expr()
						else:
							ret_str += arg
						if(i != len(fun.arguments) - 1):
							ret_str += ', '

					ret_str += ')'
					return ret_str
				else:			
					return str(self.get())
		elif(self.left != None and self.right == None):
			if(self.get() == '()'):
				return '(' + self.left.get_str_expr() + ')'
			elif(self.get() == '-'):
				return '-' + self.left.get_str_expr()
			elif(self.get() == '++_left'):
				return '++' + self.left.get_str_expr()
			elif(self.get() == '++_right'):
				return self.left.get_str_expr() + '++'
			else:
				return self.left.get_str_expr() + " " + str(self.get())
		else:
			return self.left.get_str_expr() + " " + str(self.get()) + " " + self.right.get_str_expr()
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
	'DOUBLEPLUS',
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
t_DOUBLEPLUS	= r'\+\+'
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

def t_FLOAT_VAL(t):
	r'\d+\.\d+'
	t.value = float(t.value)
	return t

def t_INT_VAL(t):
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
	
	if __debug__ == False:
		print(p[0])

def p_function(p):
	'''function : type id variable_declaration block'''
	if __debug__ == False:
		print('FUNCTION')
	
	p[0] = AST(p[1].start_lineno, p[4].end_lineno, c_function(p[2].get(), p[1].get(), p[3].get(), p[4]), AST_TYPE.FUNCTION)

	if __debug__ == False:
		print(p[0])

def p_type(p):
	'''type : INT
			| FLOAT'''
	if __debug__ == False:
		print('TYPE')
	
	p[0] = AST(p.lineno(1), p.lineno(1), p[1], AST_TYPE.TYPE)
	
	if __debug__ == False:
		print(p[0])

def p_id(p):
	'''id : ID'''
	if __debug__ == False:
		print('ID')
	
	p[0] = AST(p.lineno(1), p.lineno(1), p[1], AST_TYPE.ID)
	
	if __debug__ == False:
		print(p[0])

def p_varaible_declaration(p):
	'''variable_declaration : LPAREN declarations RPAREN'''
	if __debug__ == False:
		print('VAR_DEC')
	
	p[0] = AST.copy_AST(p.lineno(1), p.lineno(3), p[2])

	if __debug__ == False:
		print(p[0])

def p_declarations(p):
	'''declarations : type id_ptr_or_array COMMA declarations
					| type id_ptr_or_array
					| VOID'''
	if __debug__ == False:
		print('DECS')
	
	if(len(p) == 5):
		if(p[2].type == AST_TYPE.ARR_VAR):
			p[0] = AST(p[1].start_lineno, p[4].end_lineno, [(arr_type(p[1].get(), p[2].get()[0]), p[2].get()[1])] + p[4].get(), AST_TYPE.FUN_VAR_DEC)
		elif(p[2].type == AST_TYPE.PTR_VAR):
			p[0] = AST(p[1].start_lineno, p[4].end_lineno, [(ptr_type(p[1].get(), p[2].get()[0]), p[2].get()[1])] + p[4].get(), AST_TYPE.FUN_VAR_DEC)
		else:
			p[0] = AST(p[1].start_lineno, p[4].end_lineno, [(p[1].get(), p[2].get())] + p[4].get(), AST_TYPE.FUN_VAR_DEC)
	elif(len(p) == 3):
		if(p[2].type == AST_TYPE.ARR_VAR):
			p[0] = AST(p[1].start_lineno, p[2].end_lineno, [(arr_type(p[1].get(), p[2].get()[0]), p[2].get()[1])], AST_TYPE.FUN_VAR_DEC)
		elif(p[2].type == AST_TYPE.PTR_VAR):
			p[0] = AST(p[1].start_lineno, p[2].end_lineno, [(ptr_type(p[1].get(), p[2].get()[0]), p[2].get()[1])], AST_TYPE.FUN_VAR_DEC)
		else:
			p[0] = AST(p[1].start_lineno, p[2].end_lineno, [(p[1].get(), p[2].get())], AST_TYPE.FUN_VAR_DEC)
	else:
		p[0] = AST(p.lineno(1), p.lineno(1), [], AST_TYPE.FUN_VAR_DEC)
	
	if __debug__ == False:
		print(p[0])

def p_id_ptr_or_array(p):
	'''id_ptr_or_array : id
					   | id array_decs
					   | ptrs id'''
	if(len(p) == 2):
		p[0] = p[1]
	else:
		if(p[1].type == AST_TYPE.ID):
			p[0] = AST(p[1].start_lineno, p[2].end_lineno, (p[2].get(), p[1].get()), AST_TYPE.ARR_VAR)
		else:
			p[0] = AST(p[1].start_lineno, p[2].end_lineno, (p[1].get(), p[2].get()), AST_TYPE.PTR_VAR)
	
	if __debug__ == False:
		print(p[0])

def p_array_decs(p):
	'''array_decs : SQ_LBRACKET expression SQ_RBRACKET array_decs
				  | SQ_LBRACKET expression SQ_RBRACKET'''
	if(len(p) == 5):
		p[0] = AST(p.lineno(1), p[4].end_lineno, [p[2]] + p[4].get(), AST_TYPE.ARRAY_DECS)
	else:
		p[0] = AST(p.lineno(1), p.lineno(3), [p[2]], AST_TYPE.ARRAY_DECS)
	
	if __debug__ == False:
		print(p[0])

def p_ptrs(p):
	'''ptrs : MULTIPLY ptrs
		    | MULTIPLY'''
	if(len(p) == 3):
		p[0] = AST(p.lineno(1), p[2].end_lineno, p[2].get() + 1, AST_TYPE.PTRS)
	else:
		p[0] = AST(p.lineno(1), p.lineno(1), 1, AST_TYPE.PTRS)

	if __debug__ == False:
		print(p[0])

def p_block(p):
	'''block : LBRACE statements RBRACE'''
	if __debug__ == False:
		print('BLOCK')

	p[0] = AST(p.lineno(1), p.lineno(3), 'block', AST_TYPE.BLOCK, p[2])

	if __debug__ == False:
		print(p[0])

def p_statements(p):
	'''statements : semi_statement
				  | non_semi_statement
			      | semi_statement SEMI statements
			      | non_semi_statement statements
			      | empty'''
	if __debug__ == False:
		print('STATEMENTS')

	if(len(p) == 2):
		if(type(p[1]) == AST):		
			p[0] = AST(p[1].start_lineno, p[1].end_lineno, 'statements', AST_TYPE.STATEMENTS, p[1])
		else:
			p[0] = None
	elif(len(p) == 3):
		if(p[2] != None):
			p[0] = AST(p[1].start_lineno, p[2].end_lineno, 'statements', AST_TYPE.STATEMENTS, p[1], p[2])
		else:
			p[0] = AST(p[1].start_lineno, p[1].end_lineno, 'statements', AST_TYPE.STATEMENTS, p[1])	
	elif(len(p) == 4):
		if(p[3] != None):
			p[0] = AST(p[1].start_lineno, p[3].end_lineno, 'statements', AST_TYPE.STATEMENTS, p[1], p[3])
		else:
			p[0] = AST(p[1].start_lineno, p[1].end_lineno, 'statements', AST_TYPE.STATEMENTS, p[1])			

	if __debug__ == False:
		print(p[0])

def p_semi_statement(p):
	'''semi_statement : var_declaration
					  | var_assignment
					  | function_app
					  | expression
					  | return_expr'''
	if __debug__ == False:
		print('SEMI_STATEMENT')

	p[0] = AST(p[1].start_lineno, p[1].end_lineno, 'SEMI_STATEMENT', AST_TYPE.SEMI_STATEMENT, p[1])

	if __debug__ == False:
		print(p[0])

def p_non_semi_statement(p):
	'''non_semi_statement : conditional
						  | for
						  | while'''
	if __debug__ == False:
		print('NON_SEMI_STATEMENT')

	p[0] = AST(p[1].start_lineno, p[1].end_lineno, 'NON_SEMI_STATEMENT', AST_TYPE.NON_SEMI_STATEMENT, p[1])


	if __debug__ == False:
		print(p[0])

def p_conditional(p):
	'''conditional : if elif_else'''
	if __debug__ == False:
		print('CONDITIONAL')
	if(p[2] != None):
		p[0] = AST(p[1].start_lineno, p[2].end_lineno, 'conditional', AST_TYPE.COND, p[1], p[2])
	elif(p[2] == None):
		p[0] = AST(p[1].start_lineno, p[1].end_lineno, 'conditional', AST_TYPE.COND, p[1])		

	if __debug__ == False:
		print(p[0])

def p_if(p):
	'''if : IF LPAREN expression RPAREN block'''
	if __debug__ == False:
		print('IF')
	p[0] = AST(p.lineno(1), p[5].end_lineno, p[3], AST_TYPE.IF, p[5])

	if __debug__ == False:
		print(p[0])

def p_elif_else(p):
	'''elif_else : ELSE IF LPAREN expression RPAREN block elif_else
				 | ELSE block
				 | empty'''
	if __debug__ == False:
		print('ELIF_ELSE')
	
	if(len(p) == 2):
		p[0] = None
	elif(len(p) == 3):
		p[0] = AST(p.lineno(1), p[2].end_lineno, True, AST_TYPE.ELIF_ELSE)		
	else:
		if(p[7] != None):
			p[0] = AST(p.lineno(1), p[7].end_lineno, p[4], AST_TYPE.ELIF_ELSE, p[6], p[7])
		else:
			p[0] = AST(p.lineno(1), p[6].end_lineno, p[4], AST_TYPE.ELIF_ELSE, p[6])

	if __debug__ == False:
		print(p[0])

def p_for(p):
	'''for : FOR LPAREN loop_init_or_empty SEMI semi_statement_or_empty SEMI semi_statement_or_empty RPAREN block'''
	if __debug__ == False:
		print('FOR')

	p[0] = AST(p.lineno(1), p[9].end_lineno, loop(p[3], p[5], p[7], p[9]), AST_TYPE.FOR)

	if __debug__ == False:
		print(p[0])

def p_loop_init_or_empty(p):
	'''loop_init_or_empty : loop_init
						  | expression
						  | empty'''
	if __debug__ == False:
		print('INIT_OR_EMPTY')

	p[0] = p[1]

	if __debug__ == False:
		print(p[0])

def p_semi_statement_or_empty(p):
	'''semi_statement_or_empty : semi_statement
							   | expression
						       | empty'''
	if __debug__ == False:
		print('EXPR_OR_EMPTY')

	p[0] = p[1]

	if __debug__ == False:
		print(p[0])

def p_loop_init(p):
	'''loop_init : type var_assignment
				 | semi_statement'''
	if __debug__ == False:
		print('LOOP_INIT')

	if(len(p) == 3):
		p[0] = AST(p[1].start_lineno, p[2].end_lineno, (p[1], p[2]), AST_TYPE.LOOP_INIT)
	else:
		p[0] = AST(p[1].start_lineno, p[1].end_lineno, p[1], AST_TYPE.LOOP_INIT)

	if __debug__ == False:
		print(p[0])

def p_while(p):
	'''while : WHILE LPAREN expression RPAREN block'''
	if __debug__ == False:
		print('WHILE')
	
	p[0] = AST(p.lineno(1), p[5].end_lineno, loop(None, p[3], None, p[5]), AST_TYPE.WHILE)

	if __debug__ == False:
		print(p[0])

def p_var_declaration(p):
	'''var_declaration : type var_and_assign'''
	if __debug__ == False:
		print('VAR_DEC')

	# vars_and_assigns : array of ((type, id), assign) | (type, id)
	vars_and_assigns = []
	content = p[2].get()
	for i in range(len(content)):
		if(content[i].type == AST_TYPE.ASSIGN):
			# var dec with assign
			var_AST = content[i].get()[0]
			expr = content[i].get()[1]
			if(var_AST.type == AST_TYPE.ARR_VAR):
				cur_type_id = (arr_type(p[1].get(), var_AST.get()[0]), var_AST.get()[1])
				vars_and_assigns.append((cur_type_id, expr))
			elif(var_AST.type == AST_TYPE.PTR_VAR):
				cur_type_id = (ptr_type(p[1].get(), var_AST.get()[0]), var_AST.get()[1])
				vars_and_assigns.append((cur_type_id, expr))
			elif(var_AST.type == AST_TYPE.ID):
				cur_type_id = (p[1].get(), var_AST.get())
				vars_and_assigns.append((cur_type_id, expr))
		else:
			# var dec without assign
			var_AST = content[i]
			if(content[i].type == AST_TYPE.ARR_VAR):
				cur_type_id = (arr_type(p[1].get(), var_AST.get()[0]), var_AST.get()[1])
				vars_and_assigns.append(cur_type_id)
			elif(content[i].type == AST_TYPE.PTR_VAR):
				cur_type_id = (ptr_type(p[1].get(), var_AST.get()[0]), var_AST.get()[1])
				vars_and_assigns.append(cur_type_id)
			elif(content[i].type == AST_TYPE.ID):
				cur_type_id = (p[1].get(), var_AST.get())
				vars_and_assigns.append(cur_type_id)

	p[0] = AST(p[1].start_lineno, p[2].end_lineno, vars_and_assigns, AST_TYPE.VAR_DEC)

	if __debug__ == False:
		print(p[0])

def p_var_assignment(p):
	'''var_assignment : id_ptr_or_array EQ expression
					  | id_ptr_or_array EQ function_app'''
	if __debug__ == False:
		print('VAR_ASSIGN')

	p[0] = AST(p[1].start_lineno, p[3].end_lineno, (p[1], p[3]), AST_TYPE.ASSIGN)

	if __debug__ == False:
		print(p[0])

def p_var_and_assign(p):
	'''var_and_assign : var_assignment COMMA var_and_assign
					  | var_assignment
					  | id_ptr_or_array COMMA var_and_assign
					  | id_ptr_or_array'''
	if __debug__ == False:
		print('VAR_AND_ASSIGN')
	
	if(len(p) == 4):
		p[0] = AST(p[1].start_lineno, p[3].end_lineno, [p[1]] + p[3].get(), AST_TYPE.VAR_AND_ASSIGN)
	else:
		p[0] = AST(p[1].start_lineno, p[1].end_lineno, [p[1]], AST_TYPE.VAR_AND_ASSIGN)

	if __debug__ == False:
		print(p[0])

def p_return_expr(p):
	'''return_expr : RETURN expression
				   | RETURN'''
	if(len(p) == 3):
		p[0] = AST(p.lineno(1), p[2].end_lineno, 'return', AST_TYPE.RETURN, p[2])
	else:
		p[0] = AST(p.lineno(1), p.lineno(1), 'return', AST_TYPE.RETURN)

def p_function_app(p):
	'''function_app : PRINTF LPAREN STRING print_formats RPAREN
					| ID LPAREN arguments RPAREN'''
	if __debug__ == False:
		print('FUNCTION_APP')

	if(len(p) == 5):
		if(p[3] != None):
			p[0] = AST(p.lineno(1), p.lineno(4), fun_app(p[1], p[3].get()), AST_TYPE.FUN_APP)
		else:
			p[0] = AST(p.lineno(1), p.lineno(4), fun_app(p[1], []), AST_TYPE.FUN_APP)
	else:
		if(p[4] != None):
			p[0] = AST(p.lineno(1), p.lineno(5), fun_app('printf', [p[3]] + p[4].get()), AST_TYPE.FUN_APP)
		else:
			p[0] = AST(p.lineno(1), p.lineno(5), fun_app('printf', [p[3]]), AST_TYPE.FUN_APP)

	if __debug__ == False:
		print(p[0])

def p_print_formats(p):
	'''print_formats : COMMA expression print_formats
					 | empty'''
	if __debug__ == False:
		print('PRINTF_FORMATS')
	
	if(len(p) == 4):
		if(p[3] != None):
			p[0] = AST(p.lineno(1), p[3].end_lineno, [p[2]] + p[3].get(), AST_TYPE.PRINT_FORMATS)
		else:
			p[0] = AST(p.lineno(1), p[2].end_lineno, [p[2]], AST_TYPE.PRINT_FORMATS)			
	else:
		p[0] = None

	if __debug__ == False:
		print(p[0])

def p_arguments(p):
	'''arguments : expression COMMA arguments
				 | expression
				 | empty'''
	if __debug__ == False:
		print('ARGUMENTS')
	
	if(len(p) == 4):
		p[0] = AST(p[1].start_lineno, p[3].start_lineno, [p[1]] + p[3].get(), AST_TYPE.ARGS)
	else:
		if(p[1] != None):
			p[0] = AST(p[1].start_lineno, p[1].end_lineno, [p[1]], AST_TYPE.ARGS)
		else:
			p[0] = None

	if __debug__ == False:
		print(p[0])

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
		  		  | id_ptr_or_array DOUBLEPLUS
		  		  | DOUBLEPLUS id_ptr_or_array
		  		  | id_ptr_or_array
		  		  | function_app
		  		  | var_assignment
			  	  | INT_VAL
			  	  | FLOAT_VAL'''
	if __debug__ == False:
		print('EXPRESSION')

	if(len(p) == 4):
		if(p[1] == '('):
			p[0] = AST(p.lineno(1), p.lineno(3), '()', AST_TYPE.EXPR, p[2])
		else:
			p[0] = AST(p[1].start_lineno, p[3].end_lineno, p[2], AST_TYPE.EXPR, p[1], p[3])
	elif(len(p) == 3):
		if(type(p[2]) == AST):
			if(p[2].type == AST_TYPE.EXPR):
				p[0] = AST(p.lineno(1), p[2].end_lineno, p[1], AST_TYPE.EXPR, p[2])
			else:
				p[0] = AST(p.lineno(1), p[2].end_lineno, '++_left', AST_TYPE.EXPR, p[2])				
		else:
			p[0] = AST(p[1].start_lineno, p.lineno(2), '++_right', AST_TYPE.EXPR, p[1])			
	else:
		if(type(p[1]) == AST):
			p[0] = AST(p[1].start_lineno, p[1].start_lineno, p[1], AST_TYPE.EXPR)
		else:
			p[0] = AST(p.lineno(1), p.lineno(1), p[1], AST_TYPE.EXPR)

	if __debug__ == False:
		print(p[0])

def p_error(p):
	print("Syntax error in input!")

def parse(text):
	parser = yacc.yacc()
	return parser.parse(text)

def main():
	if(__name__ == '__main__'):
		with open('input.c', 'r') as file:
			data = file.read()
		# lexer.input(data)
		# while True:
		# 	tok = lexer.token()
		# 	if not tok:
		# 		break
		# 	print(tok)
		parser = yacc.yacc()
		parser.parse(data)

main()