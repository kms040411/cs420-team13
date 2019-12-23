import lex_yacc
import run

def statements_concat(st_1, st_2):
	if(st_1.right == None):
		return lex_yacc.AST.copy_AST_change(st_1, None, None, st_2)
	else:
		return lex_yacc.AST.copy_AST_change(st_1, None, None, statements_concat(st_1.right, st_2))

def recurse_over_variable(mode, ast, char_to_find = None, expr_to_replace = None):
	# mode : 0 -> check if char_to_find exist as a free occurrence
	# mode : 1 -> check if char_to_find exist as a bound occurrence 
	# mode : 2 -> replace free occurence of char_to_find to expr_to_replace
	if ast == None:
		if(mode == 0 or mode == 1):
			return False
		else:
			return ast
	elif ast.type == lex_yacc.AST_TYPE.EXPR:
		if ast.content in ['+', '-', '*', '/', '<', '>']:
			if ast.content == '-' and ast.right is None: # e = -e
				if(mode == 0 or mode == 1):
					return recurse_over_variable(mode, ast.left, char_to_find)
				else:
					return lex_yacc.AST.copy_AST_change(ast, None, recurse_over_variable(mode, ast.left, char_to_find, expr_to_replace))
			else: # e = e + e | e - e | e * e | e = e / e | e < e | e = e > e
				if(mode == 0 or mode == 1):
					return recurse_over_variable(mode, ast.left, char_to_find) | recurse_over_variable(mode, ast.right, char_to_find)
				else:
					return lex_yacc.AST.copy_AST_change(ast, None, recurse_over_variable(mode, ast.left, char_to_find, expr_to_replace), recurse_over_variable(mode, ast.right, char_to_find, expr_to_replace))
		elif ast.content == '()': # e = (e)
			if(mode == 0 or mode == 1):
				return recurse_over_variable(mode, ast.left, char_to_find)
			else:
				return lex_yacc.AST.copy_AST_change(ast, None, recurse_over_variable(mode, ast.left, char_to_find, expr_to_replace))
		elif type(ast.content) == str and ast.content.startswith('++'): # e = e++ | e = ++e
			if(mode == 0 or mode == 1):
				return recurse_over_variable(mode, ast.left, char_to_find)
			else:
				return lex_yacc.AST.copy_AST_change(ast, None, recurse_over_variable(mode, ast.left, char_to_find, expr_to_replace))
		elif type(ast.content) == lex_yacc.AST: # e = id_ptr_or_array | function_app | var_assignment
			if(mode == 0 or mode == 1):
				return recurse_over_variable(mode, ast.content, char_to_find)
			else:
				return lex_yacc.AST.copy_AST_change(ast, recurse_over_variable(mode, ast.content, char_to_find, expr_to_replace))
		else: # e = INT_VAL | FLOAT_VAL
			if(mode == 0 or mode == 1):
				return False
			else:
				return ast
	elif ast.type == lex_yacc.AST_TYPE.ID: # id_ptr_or_array = id
		if(mode == 0):
			if(char_to_find == None):
				return True
			else:
				if(ast.get() == char_to_find):
					return True
				else:
					return False
		elif(mode == 1):
			return False
		else:
			if(ast.get() == char_to_find):
				return expr_to_replace
			else:
				return ast
	elif ast.type == lex_yacc.AST_TYPE.ARR_VAR: #id_ptr_or_array = id array_decs
		if(mode == 0):
			if(char_to_find == None):
				return True
			else:
				ret = (ast.get()[1] == char_to_find)
				for elem in ast.get()[0]:
					ret = ret | recurse_over_variable(mode, elem, char_to_find)
				return ret
		elif(mode == 1):
			if(char_to_find == None):
				return True
			else:
				return ast.get()[1] == char_to_find
		else:

			new_array_decs = []
			for elem in ast.get()[0]:
				new_array_decs.append(recurse_over_variable(mode, elem, char_to_find, expr_to_replace))
			return lex_yacc.AST.copy_AST_change(ast, (new_array_decs, ast.get()[1]))
	elif ast.type == lex_yacc.AST_TYPE.PTR_VAR:
		if(mode == 0 or mode == 1):
			if(char_to_find == None):
				return True
			else:
				return char_to_find == ast.get()[1]
		else:
			return ast
	elif ast.type == lex_yacc.AST_TYPE.SEMI_STATEMENT:
		if(mode == 0 or mode == 1):
			return recurse_over_variable(mode, ast.left, char_to_find)
		else:
			return lex_yacc.AST.copy_AST_change(ast, None, recurse_over_variable(mode, ast.left, char_to_find, expr_to_replace))
	elif ast.type == lex_yacc.AST_TYPE.VAR_DEC:
		ret = False
		vars_and_assigns = ast.get()
		new_vars_and_assigns = []
		for elem in vars_and_assigns:
			if(type(elem) == tuple):
				if(mode == 0):
					ret = ret | recurse_over_variable(mode, elem[1], char_to_find)
				elif(mode == 1):
					ret = ret | (elem[0][1] == char_to_find)
				else:
					new_vars_and_assigns.append((elem[0], recurse_over_variable(mode, elem[1], char_to_find, expr_to_replace)))
			else:
				if(mode == 0):
					ret = ret | recurse_over_variable(mode, elem, char_to_find)
				elif(mode == 1):
					ret = ret | (elem[0][1] == char_to_find)
				else:
					new_vars_and_assigns.append(elem)
		if(mode == 0 or mode == 1):
			return ret
		else:
			return lex_yacc.AST.copy_AST_change(ast, new_vars_and_assigns)
	elif ast.type == lex_yacc.AST_TYPE.ASSIGN:
		elem = ast.get()
		if(type(elem[0].get()) == tuple):
			if(mode == 0):
				if(type(elem[0].get()[0]) == int):
					return recurse_over_variable(mode, elem[0].get()[1], char_to_find) | recurse_over_variable(mode, elem[1], char_to_find)
				else:
					ret = False
					for i in range(len(elem[0].get()[0])):
						ret = ret | recurse_over_variable(mode, elem[0].get()[0][i], char_to_find)
					return ((ret | recurse_over_variable(mode, elem[0].get()[1], char_to_find)) | recurse_over_variable(mode, elem[1], char_to_find))
			elif(mode == 1):
				return (elem[0].get()[1] == char_to_find)
			else:
				if(type(elem[0].get()[0]) == int):
					return ast
				else:
					return lex_yacc.AST.copy_AST_change(ast, (recurse_over_variable(mode, elem[0], char_to_find, expr_to_replace), recurse_over_variable(mode, elem[1], char_to_find, expr_to_replace)))		
		else:
			if(mode == 0):
				return recurse_over_variable(mode, elem[0], char_to_find | recurse_over_variable(mode, elem[1], char_to_find))
			elif(mode == 1):
				return (elem[0].get() == char_to_find)
			else:
				return lex_yacc.AST.copy_AST_change(ast, (elem[0], recurse_over_variable(mode, elem[1], char_to_find, expr_to_replace)))
	elif ast.type == lex_yacc.AST_TYPE.FUN_APP:
		fun = ast.get()
		if(mode == 0):
			ret = False
			for arg in fun.arguments:
				if(arg.type == lex_yacc.AST):
					ret = ret | recurse_over_variable(mode, arg, char_to_find)
			return ret
		elif(mode == 1):
			if(fun.fname == char_to_find):
				return True
			else:
				return False
		else:
			new_args = []
			for arg in fun.arguments:
				if(type(arg) == lex_yacc.AST):
					new_args.append(recurse_over_variable(mode, arg, char_to_find, expr_to_replace))
				else:
					new_args.append(arg)
			return lex_yacc.AST.copy_AST_change(ast, lex_yacc.fun_app(fun.fname, new_args))
	elif ast.type == lex_yacc.AST_TYPE.RETURN:
		if(mode == 0 or mode == 1):
			if(ast.left == None):
				return False
			else:
				return recurse_over_variable(mode, ast.left, char_to_find)
		else:
			if(ast.left == None):
				return ast
			else:
				return lex_yacc.AST.copy_AST_change(ast, None, recurse_over_variable(mode, ast.left, char_to_find, expr_to_replace))
	elif ast.type == lex_yacc.AST_TYPE.NON_SEMI_STATEMENT:
		if(mode == 0 or mode == 1):
			return recurse_over_variable(mode, ast.left, char_to_find)
		else:
			return lex_yacc.AST.copy_AST_change(ast, None, recurse_over_variable(mode, ast.left, char_to_find, expr_to_replace))
	elif ast.type == lex_yacc.AST_TYPE.COND:
		if(mode == 0 or mode == 1):
			if(ast.right == None):
				return recurse_over_variable(mode, ast.left, char_to_find)
			else:
				return recurse_over_variable(mode, ast.left, char_to_find) or recurse_over_variable(mode, ast.left, char_to_find)
		else:
			if(ast.right == None):
				return lex_yacc.AST.copy_AST_change(ast, None, recurse_over_variable(mode, ast.left, char_to_find, expr_to_replace))
			else:
				return lex_yacc.AST.copy_AST_change(ast, None, recurse_over_variable(mode, ast.left, char_to_find, expr_to_replace),
															recurse_over_variable(mode, ast.right, char_to_find, expr_to_replace))
	elif ast.type == lex_yacc.AST_TYPE.IF:
		if(mode == 0 or mode == 1):
			return recurse_over_variable(mode, ast.content, char_to_find) or recurse_over_variable(mode, ast.left, char_to_find)
		else:
			return lex_yacc.AST.copy_AST_change(ast, recurse_over_variable(mode, ast.content, char_to_find, expr_to_replace),
												recurse_over_variable(mode, ast.left, char_to_find, expr_to_replace))			
	elif ast.type == lex_yacc.AST_TYPE.ELIF_ELSE:
		if(mode == 0 or mode == 1):
			if(ast.content == True):
				return recurse_over_variable(mode, ast.left, char_to_find)
			elif(ast.right == None):
				return recurse_over_variable(mode, ast.content, char_to_find) | recurse_over_variable(mode, ast.left, char_to_find)
			else:
				return recurse_over_variable(mode, ast.content, char_to_find) | recurse_over_variable(mode, ast.left, char_to_find) | recurse_over_variable(mode, ast.right, char_to_find)
		else:
			if(ast.content == True):
				return lex_yacc.AST.copy_AST_change(ast, None, recurse_over_variable(mode, ast.left, char_to_find, expr_to_replace))		
			elif(ast.right == None):
				return lex_yacc.AST.copy_AST_change(ast, recurse_over_variable(mode, ast.content, char_to_find, expr_to_replace),
												recurse_over_variable(mode, ast.left, char_to_find, expr_to_replace))
			else:
				return lex_yacc.AST.copy_AST_change(ast, recurse_over_variable(mode, ast.content, char_to_find, expr_to_replace),
													recurse_over_variable(mode, ast.left, char_to_find, expr_to_replace),
													recurse_over_variable(mode, ast.right, char_to_find, expr_to_replace))		
	elif ast.type == lex_yacc.AST_TYPE.FOR:
		if(mode == 0 or mode == 1):
			return (((recurse_over_variable(mode, ast.content.init_expr, char_to_find) |
					recurse_over_variable(mode, ast.content.term_expr, char_to_find)) |
					recurse_over_variable(mode, ast.content.update_expr, char_to_find)) |
					recurse_over_variable(mode, ast.content.body, char_to_find))
		else:
			return lex_yacc.AST.copy_AST_change(ast, lex_yacc.loop(recurse_over_variable(mode, ast.content.init_expr, char_to_find, expr_to_replace),
																recurse_over_variable(mode, ast.content.term_expr, char_to_find, expr_to_replace),
																recurse_over_variable(mode, ast.content.update_expr, char_to_find, expr_to_replace),
																recurse_over_variable(mode, ast.content.body, char_to_find, expr_to_replace)))		
	elif ast.type == lex_yacc.AST_TYPE.LOOP_INIT:
		if(mode == 0 or mode == 1):
			if(type(ast.content) == tuple):
				return recurse_over_variable(mode, ast.contnet[1])
			else:
				return recurse_over_variable(mode, ast.content)
		else:
			if(type(ast.content) == tuple):
				return lex_yacc.AST.copy_AST_change(ast, (ast.content[0], recurse_over_variable(mode, ast.content[1], char_to_find, expr_to_replace)))
			else:
				return lex_yacc.AST.copy_AST_change(ast, (ast.content[0], recurse_over_variable(mode, ast.content, char_to_find, expr_to_replace)))
	elif ast.type == lex_yacc.AST_TYPE.BLOCK:
		if(mode == 0 or mode == 1):
			return recurse_over_variable(mode, ast.left)
		else:
			return lex_yacc.AST.copy_AST_change(ast, None, recurse_over_variable(mode, ast.left, char_to_find, expr_to_replace))
	elif ast.type == lex_yacc.AST_TYPE.STATEMENTS:
		if(mode == 0 or mode == 1):
			if(ast.right == None):
				return recurse_over_variable(mode, ast.left)
			else:
				return recurse_over_variable(mode, ast.left) | recurse_over_variable(mode, ast.right)
		else:
			if(ast.right == None):
				return lex_yacc.AST.copy_AST_change(ast, None, recurse_over_variable(mode, ast.left, char_to_find, expr_to_replace))			
			else:
				return lex_yacc.AST.copy_AST_change(ast, None, recurse_over_variable(mode, ast.left, char_to_find, expr_to_replace)
														, recurse_over_variable(mode, ast.right, char_to_find, expr_to_replace))			

	else:
		raise Exception('Optimize does not cover all the case')

def loop_optimizable(tree):
	loop = tree.get()
	if(loop.init_expr == None):
		return False
	if(loop.init_expr.type == lex_yacc.AST_TYPE.LOOP_INIT):
		if(type(loop.init_expr.get()) == tuple):
			if(loop.init_expr.get()[0].get() == 'float'):
				if __debug__ == False:
					print(0)
				return False 
			var_assign = loop.init_expr.get()[1]
			if(var_assign.get()[0].type != lex_yacc.AST_TYPE.ID):
				if __debug__ == False:
					print(1)
				return False
			if(var_assign.get()[1].type == lex_yacc.AST_TYPE.FUN_APP):
				if __debug__ == False:
					print(2)
				return False
			if(recurse_over_variable(0, var_assign.get()[1])):
				if __debug__ == False:
					print(3)
				return False
			loop_variable = var_assign.get()[0].get()
		else:
			var_assign = loop.init_expr.get().left
			if(var_assign.type != lex_yacc.AST_TYPE.ASSIGN):
				if __debug__ == False:
					print(4)
				return False
			if(var_assign.get()[1].type == lex_yacc.AST_TYPE.FUN_APP):
				if __debug__ == False:
					print(5)
				return False
			if(recurse_over_variable(0, var_assign.get()[1])):
				if __debug__ == False:
					print(6)
				return False
			loop_variable = var_assign.get()[0].get()

	if(loop.term_expr == None):
		if __debug__ == False:
			print(7)
		return False
	loop_expr = loop.term_expr.left
	if(loop_expr.type != lex_yacc.AST_TYPE.EXPR):
		if __debug__ == False:
			print(8)
		return False
	if(not(loop_expr.get() == '<' or loop_expr.get() == '>')):
		if __debug__ == False:
			print(9)
		return False
	comparison_op = loop_expr.get()
	if(not(loop_expr.left.get().type == lex_yacc.AST_TYPE.ID and loop_expr.left.get().get() == loop_variable)):
		if __debug__ == False:
			print(10)
		return False
	if(recurse_over_variable(0, loop_expr.right)):
		if __debug__ == False:
			print(10)
		return False

	if(loop.update_expr == None):
		if __debug__ == False:
			print(11)	
		return False

	# update_expr should be of the form like a = a + 1, a++
	if(loop.update_expr.type != lex_yacc.AST_TYPE.SEMI_STATEMENT):
		if __debug__ == False:
			print(12)
		return False
	if(loop.update_expr.left.type == lex_yacc.AST_TYPE.ASSIGN):
		var_assign = loop.update_expr.left
		if(var_assign.get()[0].type != lex_yacc.AST_TYPE.ID):
			if __debug__ == False:
				print(13)
			return False
		if(var_assign.get()[0].get() != loop_variable):
			if __debug__ == False:
				print(14)
			return False
		if(var_assign.get()[1].type == lex_yacc.AST_TYPE.FUN_APP):
			if __debug__ == False:
				print(15)
			return False
		if(comparison_op == '<'):
			if(var_assign.get()[1].get() != '+'):
				if __debug__ == False:
					print(16)
				return False
		elif(comparison_op == '>'):
			if(var_assign.get()[1].get() != '-'):
				if __debug__ == False:
					print(17)
				return False
		if(var_assign.get()[1].left.get().get() != loop_variable):
			if __debug__ == False:
				print(18)
			return False
		if(recurse_over_variable(0, var_assign.get()[1].right, loop_variable)):
			if __debug__ == False:
				print(19)
			return False

	elif(loop.update_expr.left.type == lex_yacc.AST_TYPE.EXPR):
		if(comparison_op == '>'):
			if __debug__ == False:
				print(20)
			return False
		expr = loop.update_expr.left
		if(expr.get() == '++_left' or expr.get() == '++_right'):
			if(expr.left.type != lex_yacc.AST_TYPE.ID):
				if __debug__ == False:
					print(21)
				return False
			if(expr.left.get() != loop_variable):
				if __debug__ == False:
					print(22)
				return False
		else:
			if __debug__ == False:
				print(23)
			return False
	return True

def	loop_unrolling(out_file, tree, tabs, tab, end, semi):
	loop = tree.get()
	if(type(loop.init_expr.get()) == tuple):
		var_assign = loop.init_expr.get()[1]
		loop_variable = var_assign.get()[0].get()
		init_val = run.calculate_expr(var_assign.get()[1])
	else:
		var_assign = loop.init_expr.get().left
		loop_variable = var_assign.get()[0].get()
		init_val = run.calculate_expr(var_assign.get()[1])
	loop_expr = loop.term_expr.left

	comparison_op = loop_expr.get()
	term_val = run.calculate_expr(loop_expr.right)
	if(loop.update_expr.left.type == lex_yacc.AST_TYPE.ASSIGN):
		var_assign = loop.update_expr.left
		update_val = run.calculate_expr(var_assign.get()[1].right)
		if(comparison_op == '>'):
			update_val = -update_val

	elif(loop.update_expr.left.type == lex_yacc.AST_TYPE.EXPR):
		update_val = 1
	if(term_val >= init_val and comparison_op == '<'):
			new_loop_init = loop.init_expr
			new_loop_term = lex_yacc.AST(0, 0, 'SEMI_STATEMENT', lex_yacc.AST_TYPE.SEMI_STATEMENT, 
													lex_yacc.AST(0, 0, '<', lex_yacc.AST_TYPE.EXPR,
													lex_yacc.AST(0, 0, loop_variable, lex_yacc.AST_TYPE.ID),
													lex_yacc.AST(0, 0, term_val - ((term_val - init_val)% (3 * update_val)), lex_yacc.AST_TYPE.EXPR)))
			new_loop_update = lex_yacc.AST(0, 0, (lex_yacc.AST(0, 0, loop_variable, lex_yacc.AST_TYPE.ID),
												lex_yacc.AST(0, 0, '+', lex_yacc.AST_TYPE.EXPR, lex_yacc.AST(0, 0, loop_variable, lex_yacc.AST_TYPE.ID), lex_yacc.AST(0, 0, 3 * update_val, lex_yacc.AST_TYPE.EXPR))),
											lex_yacc.AST_TYPE.ASSIGN)

			new_body_block_1 = loop.body.left
			new_body_block_2 = recurse_over_variable(2, loop.body.left, loop_variable, lex_yacc.AST(0, 0, '()', lex_yacc.AST_TYPE.EXPR, 
																		lex_yacc.AST(0, 0, '+', lex_yacc.AST_TYPE.EXPR,
																		lex_yacc.AST(0, 0, loop_variable, lex_yacc.AST_TYPE.ID),
																		lex_yacc.AST(0, 0, update_val, lex_yacc.AST_TYPE.EXPR))))
			new_body_block_3 = recurse_over_variable(2, loop.body.left, loop_variable, lex_yacc.AST(0, 0, '()', lex_yacc.AST_TYPE.EXPR, 
																		lex_yacc.AST(0, 0, '+', lex_yacc.AST_TYPE.EXPR,
																		lex_yacc.AST(0, 0, loop_variable, lex_yacc.AST_TYPE.ID),
																		lex_yacc.AST(0, 0, 2 * update_val, lex_yacc.AST_TYPE.EXPR))))
			new_body = statements_concat(new_body_block_1, new_body_block_2)
			new_body = statements_concat(new_body, new_body_block_3)
			new_body_block = lex_yacc.AST(0, 0, 'block', lex_yacc.AST_TYPE.BLOCK, new_body)
			new_loop = lex_yacc.loop(new_loop_init, new_loop_term, new_loop_update, new_body_block)
			new_ast = lex_yacc.AST(0, 0, new_loop, lex_yacc.AST_TYPE.FOR)
			optimize(out_file, new_ast, tabs, tab, end, semi, False)

			loop_num = (term_val - init_val) // (3 * update_val)
			loop_start = init_val + (3 * update_val) * loop_num
			loop_left = (term_val - loop_start) // update_val
			for i in range(loop_left):
				body_left = recurse_over_variable(2, loop.body.left, loop_variable, lex_yacc.AST(0, 0, loop_start + i * update_val, lex_yacc.AST_TYPE.EXPR))
				optimize(out_file, body_left, tabs, tab, end, semi, False)		
	elif(term_val <= init_val and comparison_op == '>'):
			new_loop_init = loop.init_expr
			new_loop_term = lex_yacc.AST(0, 0, 'SEMI_STATEMENT', lex_yacc.AST_TYPE.SEMI_STATEMENT, 
													lex_yacc.AST(0, 0, '>', lex_yacc.AST_TYPE.EXPR,
													lex_yacc.AST(0, 0, loop_variable, lex_yacc.AST_TYPE.ID),
													lex_yacc.AST(0, 0, term_val + ((init_val - term_val) % (3 * -update_val)), lex_yacc.AST_TYPE.EXPR)))
			new_loop_update = lex_yacc.AST(0, 0, (lex_yacc.AST(0, 0, loop_variable, lex_yacc.AST_TYPE.ID),
												lex_yacc.AST(0, 0, '-', lex_yacc.AST_TYPE.EXPR, lex_yacc.AST(0, 0, loop_variable, lex_yacc.AST_TYPE.ID), lex_yacc.AST(0, 0, 3 * (-update_val), lex_yacc.AST_TYPE.EXPR))),
											lex_yacc.AST_TYPE.ASSIGN)
			new_body_block_1 = loop.body.left
			new_body_block_2 = recurse_over_variable(2, loop.body.left, loop_variable, lex_yacc.AST(0, 0, '()', lex_yacc.AST_TYPE.EXPR, 
																		lex_yacc.AST(0, 0, '-', lex_yacc.AST_TYPE.EXPR,
																		lex_yacc.AST(0, 0, loop_variable, lex_yacc.AST_TYPE.ID),
																		lex_yacc.AST(0, 0, -update_val, lex_yacc.AST_TYPE.EXPR))))
			new_body_block_3 = recurse_over_variable(2, loop.body.left, loop_variable, lex_yacc.AST(0, 0, '()', lex_yacc.AST_TYPE.EXPR, 
																		lex_yacc.AST(0, 0, '-', lex_yacc.AST_TYPE.EXPR,
																		lex_yacc.AST(0, 0, loop_variable, lex_yacc.AST_TYPE.ID),
																		lex_yacc.AST(0, 0, 2 * (-update_val), lex_yacc.AST_TYPE.EXPR))))
			new_body = statements_concat(new_body_block_1, new_body_block_2)
			new_body = statements_concat(new_body, new_body_block_3)
			new_body_block = lex_yacc.AST(0, 0, 'block', lex_yacc.AST_TYPE.BLOCK, new_body)
			new_loop = lex_yacc.loop(new_loop_init, new_loop_term, new_loop_update, new_body_block)
			new_ast = lex_yacc.AST(0, 0, new_loop, lex_yacc.AST_TYPE.FOR)
			optimize(out_file, new_ast, tabs, tab, end, semi, False)

			loop_num = (init_val - term_val) // (3 * -update_val)
			loop_start = init_val + (3 * update_val) * loop_num
			loop_left = (loop_start - term_val) // (-update_val)
			for i in range(loop_left):
				body_left = recurse_over_variable(2, loop.body.left, loop_variable, lex_yacc.AST(0, 0, loop_start + i * update_val, lex_yacc.AST_TYPE.EXPR))
				optimize(out_file, body_left, tabs, tab, end, semi, False)
	else:
		optimize(out_file, tree, tabs, tab, end, semi, False)

'''
    optimize(out_file, tree):
    Optimize the given tree and return optimized tree.
'''
def optimize(out_file, tree, tabs = 0, tab = True, end = True, semi = True, loop_unroll= True):
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
		if(loop_unroll == True and loop_optimizable(tree)):
			loop_unrolling(out_file, tree, tabs, tab, end, semi)
		else:
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
