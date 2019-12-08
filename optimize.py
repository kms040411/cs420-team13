import lex_yacc

'''
    optimize(tree):
    Optimize the given tree and return optimized tree.
'''
def optimize(tree, tabs = 0, tab = True, end = True, semi = True):
	if(tree.type == lex_yacc.AST_TYPE.PROGRAM):
		for func in tree.content:
			optimize(func)
	elif(tree.type == lex_yacc.AST_TYPE.FUNCTION):
		func = tree.content
		print(func.return_type + ' ' + func.name +  '(', end = '')
		for i in range(len(func.params)):
			param = func.params[i]
			param_type = param[0]
			param_name = param[1]
			if(type(param_type) == lex_yacc.arr_type):
				print(param_type.type + ' ' + param_name, end = '')
				for dim in param_type.dims:
					print('[' + str(dim.get()) + ']', end = '')
			elif(type(param_type) == lex_yacc.ptr_type):
				print(param_type.type + ' ', end = '')
				for j in range(param_type.depth):
					print('*', end = '')
				print(param_name, end = '')
			else:
				print(param_type + ' ' + param_name, end = '')
			if(i != len(func.params) - 1):
				print(',', end = '')
		print(')')
		optimize(func.body, tabs)
	elif(tree.type == lex_yacc.AST_TYPE.BLOCK):
		print('{')
		optimize(tree.left, tabs + 1)
		print('\t' * tabs + '}')
	elif(tree.type == lex_yacc.AST_TYPE.STATEMENTS):
		optimize(tree.left, tabs)
		if(tree.right != None):
			optimize(tree.right, tabs)
	elif(tree.type == lex_yacc.AST_TYPE.SEMI_STATEMENT):
		if(tab):
			print('\t' * tabs, end = '')
		optimize(tree.left, tabs)
		if(end and semi):
			print(';')
		elif(semi):
			print(';', end = '')
		elif(end):
			print()
	elif(tree.type == lex_yacc.AST_TYPE.NON_SEMI_STATEMENT):
		if(tab):
			print('\t' * tabs, end = '')
		optimize(tree.left, tabs)
	elif(tree.type == lex_yacc.AST_TYPE.VAR_DEC):
		for i in range(len(tree.content)):
			cur_var = tree.content[i]
			if(type(cur_var[1]) == lex_yacc.AST):
				# assignment
				if(type(cur_var[0][0]) == lex_yacc.arr_type):
					if(i == 0):
						print(cur_var[0][0].type, end = ' ')
					print(cur_var[0][1], end = '')
					for j in range(len(cur_var[0][0].dims)):
						print('[' + cur_var[0][0].dims[j].get_str_expr() + ']', end = '')
					print(' = ', end = '')
					print(cur_var[1].get_str_expr(), end = '')
				elif(type(cur_var[0][0]) == lex_yacc.ptr_type):
					if(i == 0):
						print(cur_var[0][0].type, end = ' ')
					print('*' * cur_var[0][0].depth, end = '')
					print(cur_var[0][1] + ' = ', end = '')
					print(cur_var[1].get_str_expr(), end = '')
				else:
					if(i == 0):
						print(cur_var[0], end = ' ')
					print(cur_var[0][1] + ' = ', end = '')
					print(cur_var[1].get_str_expr(), end = '')
			else:
				# declaration
				if(type(cur_var[0]) == lex_yacc.arr_type):
					if(i == 0):
						print(cur_var[0].type, end = ' ')
					print(cur_var[1], end = '')
					for j in range(len(cur_var[0].dims)):
						print('[' + cur_var[0].dims[j].get_str_expr() + ']', end = '')
				elif(type(cur_var[0]) == lex_yacc.ptr_type):
					if(i == 0):
						print(cur_var[0].type, end = ' ')
					print('*' * cur_var[0].depth, end = '')
					print(cur_var[1], end = '')
				else:
					if(i == 0):
						print(cur_var[0], end = ' ')
					print(cur_var[1], end = '')
			if(i != len(tree.content) - 1):
				print(', ', end = '')

	elif(tree.type == lex_yacc.AST_TYPE.ASSIGN):
		left_tree = tree.get()[0]
		if(left_tree.type == lex_yacc.AST_TYPE.ID):
			print(left_tree.get(), end = '')
		elif(left_tree.type == lex_yacc.AST_TYPE.ARR_VAR):
			print(left_tree.get()[1], end = '')
			for dim in left_tree.get()[0]:
				print('[' + dim.get_str_expr() + ']', end = '')
		elif(left_tree.type == lex_yacc.AST_TYPE.PTR_VAR):
			print('*' * left_tree.get()[0], end = '')
			print(left_tree.get()[1], end = '')
		print(' = ', end = '')
		print(tree.get()[1].get_str_expr(), end = '')
	elif(tree.type == lex_yacc.AST_TYPE.FUN_APP):
		pass
	elif(tree.type == lex_yacc.AST_TYPE.EXPR):
		print(tree.get_str_expr(), end = '')
	elif(tree.type == lex_yacc.AST_TYPE.RETURN):
		pass
	elif(tree.type == lex_yacc.AST_TYPE.FOR):
	# class loop():
	# 	def __init__(self, init_expr, term_expr, update_expr, body):
	# 		self.init_expr = init_expr
	# 		self.term_expr = term_expr
	# 		self.update_expr = update_expr
	# 		self.body = body
		loop = tree.get()
		print('for(', end = '')
		if(loop.init_expr != None):
			optimize(loop.init_expr)
		else:
			print('; ', end = '')

		if(loop.term_expr != None):
			optimize(loop.term_expr, tabs, False, False)
			print(' ', end = '')
		else:
			print('; ', end = '')

		if(loop.update_expr != None):
			optimize(loop.update_expr, tabs, False, False, False)
		print(')', end = '')

		optimize(loop.body, tabs)

	elif(tree.type == lex_yacc.AST_TYPE.LOOP_INIT):
		if(type(tree.get()) == lex_yacc.AST):
			optimize(tree.get(), tabs, False, False)
			print(' ', end = '')
		else:
			optimize(tree.get()[0], tabs, False, False)
			print(' ', end = '')
			optimize(tree.get()[1], tabs, False, False)
			print('; ', end = '')
	elif(tree.type == lex_yacc.AST_TYPE.TYPE):
		if(tab):
			print('\t' * tabs)
		print(tree.get(), end = '')
	else:
		pass



	return tree
