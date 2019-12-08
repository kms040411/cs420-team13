import lex_yacc

'''
    optimize(out_file, tree):
    Optimize the given tree and return optimized tree.
'''
def optimize(out_file, tree, tabs = 0, tab = True, end = True, semi = True):
	if(tree.type == lex_yacc.AST_TYPE.PROGRAM):
		for func in tree.content:
			optimize(out_file, func)
	elif(tree.type == lex_yacc.AST_TYPE.FUNCTION):
		func = tree.content
		out_file.write(func.return_type + ' ' + func.name +  '(')
		if(len(func.params) == 0):
			out_file.write('void')
		else:
			for i in range(len(func.params)):
				param = func.params[i]
				param_type = param[0]
				param_name = param[1]
				if(type(param_type) == lex_yacc.arr_type):
					out_file.write(param_type.type + ' ' + param_name)
					for dim in param_type.dims:
						out_file.write('[' + str(dim.get()) + ']')
				elif(type(param_type) == lex_yacc.ptr_type):
					out_file.write(param_type.type + ' ')
					for j in range(param_type.depth):
						out_file.write('*')
					out_file.write(param_name)
				else:
					out_file.write(param_type + ' ' + param_name)
				if(i != len(func.params) - 1):
					out_file.write(', ')
		out_file.write(')')
		optimize(out_file, func.body, tabs)
	elif(tree.type == lex_yacc.AST_TYPE.BLOCK):
		out_file.write('{\n')
		optimize(out_file, tree.left, tabs + 1)
		out_file.write('\t' * tabs + '}\n')
	elif(tree.type == lex_yacc.AST_TYPE.STATEMENTS):
		optimize(out_file, tree.left, tabs)
		if(tree.right != None):
			optimize(out_file, tree.right, tabs)
	elif(tree.type == lex_yacc.AST_TYPE.SEMI_STATEMENT):
		if(tab):
			out_file.write('\t' * tabs)
		optimize(out_file, tree.left, tabs)
		if(end and semi):
			out_file.write(';\n')
		elif(semi):
			out_file.write(';')
		elif(end):
			out_file.write('\n')
	elif(tree.type == lex_yacc.AST_TYPE.NON_SEMI_STATEMENT):
		if(tab):
			out_file.write('\t' * tabs)
		optimize(out_file, tree.left, tabs)
	elif(tree.type == lex_yacc.AST_TYPE.VAR_DEC):
		for i in range(len(tree.content)):
			cur_var = tree.content[i]
			if(type(cur_var[1]) == lex_yacc.AST):
				# assignment
				if(type(cur_var[0][0]) == lex_yacc.arr_type):
					if(i == 0):
						out_file.write(cur_var[0][0].type + ' ')
					out_file.write(cur_var[0][1])
					for j in range(len(cur_var[0][0].dims)):
						out_file.write('[' + cur_var[0][0].dims[j].get_str_expr() + ']')
					out_file.write(' = ')
					out_file.write(cur_var[1].get_str_expr())
				elif(type(cur_var[0][0]) == lex_yacc.ptr_type):
					if(i == 0):
						out_file.write(cur_var[0][0].type + ' ')
					out_file.write('*' * cur_var[0][0].depth)
					out_file.write(cur_var[0][1] + ' = ')
					out_file.write(cur_var[1].get_str_expr())
				else:
					if(i == 0):
						out_file.write(cur_var[0] + ' ')
					out_file.write(cur_var[0][1] + ' = ')
					out_file.write(cur_var[1].get_str_expr())
			else:
				# declaration
				if(type(cur_var[0]) == lex_yacc.arr_type):
					if(i == 0):
						out_file.write(cur_var[0].type + ' ')
					out_file.write(cur_var[1])
					for j in range(len(cur_var[0].dims)):
						out_file.write('[' + cur_var[0].dims[j].get_str_expr() + ']')
				elif(type(cur_var[0]) == lex_yacc.ptr_type):
					if(i == 0):
						out_file.write(cur_var[0].type + ' ')
					out_file.write('*' * cur_var[0].depth)
					out_file.write(cur_var[1])
				else:
					if(i == 0):
						out_file.write(cur_var[0] + ' ')
					out_file.write(cur_var[1])
			if(i != len(tree.content) - 1):
				out_file.write(', ')

	elif(tree.type == lex_yacc.AST_TYPE.ASSIGN):
		left_tree = tree.get()[0]
		if(left_tree.type == lex_yacc.AST_TYPE.ID):
			out_file.write(left_tree.get())
		elif(left_tree.type == lex_yacc.AST_TYPE.ARR_VAR):
			out_file.write(left_tree.get()[1])
			for dim in left_tree.get()[0]:
				out_file.write('[' + dim.get_str_expr() + ']')
		elif(left_tree.type == lex_yacc.AST_TYPE.PTR_VAR):
			out_file.write('*' * left_tree.get()[0])
			out_file.write(left_tree.get()[1])
		out_file.write(' = ')
		out_file.write(tree.get()[1].get_str_expr())
	elif(tree.type == lex_yacc.AST_TYPE.FUN_APP):
		out_file.write(tree.get_str_expr())		
	elif(tree.type == lex_yacc.AST_TYPE.EXPR):
		out_file.write(tree.get_str_expr())
	elif(tree.type == lex_yacc.AST_TYPE.RETURN):
		out_file.write('return ')
		optimize(out_file, tree.left)
	elif(tree.type == lex_yacc.AST_TYPE.COND):
		optimize(out_file, tree.left, tabs)
		if(tree.right != None):
			optimize(out_file, tree.right, tabs)
	elif(tree.type == lex_yacc.AST_TYPE.IF):
		out_file.write('if(')
		optimize(out_file, tree.get())
		out_file.write(')')
		optimize(out_file, tree.left, tabs)
	elif(tree.type == lex_yacc.AST_TYPE.ELIF_ELSE):
		if(tree.get() == True):
			if(tab):
				out_file.write('\t' * tabs)
			out_file.write('else')
			optimize(out_file, tree.left, tabs)
		else:
			if(tab):
				out_file.write('\t' * tabs)
			out_file.write('else if(')
			optimize(out_file, tree.get())
			out_file.write(')')
			optimize(out_file, tree.left, tabs)
			optimize(out_file, tree.right, tabs)
	elif(tree.type == lex_yacc.AST_TYPE.WHILE):
		out_file.write('while(')
		optimize(out_file, tree.get().term_expr)
		out_file.write(')')
		optimize(out_file, tree.get().body, tabs)
	elif(tree.type == lex_yacc.AST_TYPE.FOR):
	# class loop():
	# 	def __init__(self, init_expr, term_expr, update_expr, body):
	# 		self.init_expr = init_expr
	# 		self.term_expr = term_expr
	# 		self.update_expr = update_expr
	# 		self.body = body
		loop = tree.get()
		out_file.write('for(')
		if(loop.init_expr != None):
			optimize(out_file, loop.init_expr)
		else:
			out_file.write('; ')

		if(loop.term_expr != None):
			optimize(out_file, loop.term_expr, tabs, False, False)
			out_file.write(' ')
		else:
			out_file.write('; ')

		if(loop.update_expr != None):
			optimize(out_file, loop.update_expr, tabs, False, False, False)
		out_file.write(')')

		optimize(out_file, loop.body, tabs)
	elif(tree.type == lex_yacc.AST_TYPE.LOOP_INIT):
		if(type(tree.get()) == lex_yacc.AST):
			optimize(out_file, tree.get(), tabs, False, False)
			out_file.write(' ')
		else:
			optimize(out_file, tree.get()[0], tabs, False, False)
			out_file.write(' ')
			optimize(out_file, tree.get()[1], tabs, False, False)
			out_file.write('; ')
	elif(tree.type == lex_yacc.AST_TYPE.TYPE):
		if(tab):
			out_file.write('\t' * tabs + '\n')
		out_file.write(tree.get())
	else:
		pass
	return tree

def optimize_init(tree):
	f = open('optimized.c', 'w')
	optimize(f, tree)
	f.close()
