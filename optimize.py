import lex_yacc



for(i = 0; i < 10; i = i + 1){
	print(i);
}

for(i = 0; i < 10; i += 2){
	print(i);
	print(i + 1);
}

def recurse_over_variable(mode, ast, char_to_find = None, expr_to_replace = None):
	# mode : 0 -> check if char_to_find exist as a free occurrence
	# mode : 1 -> check if char_to_find exist as a bound occurrence 
	# mode : 2 -> replace free occurence of char_to_find to expr_to_replace
    if ast.type == AST_TYPE.EXPR:
        if ast.content in ['+', '-', '*', '/', '<', '>']:
            if ast.content == '-' and ast.right is None: # e = -e
            	if(mode == 0 || mode == 1):
	                return recurse_over_variable(mode, ast.left, char_to_find)
	            else:
					return lex_yacc.copy_AST_change(ast, None, recurse_over_variable(mode, ast.left, char_to_find, expr_to_replace))
            else: # e = e + e | e - e | e * e | e = e / e | e < e | e = e > e
            	if(mode == 0 || mode == 1):
            		return check_variable(mode, ast.left, char_to_find) | recurse_over_variable(mode, ast.right, char_to_find)
            	else:
            		return lex_yacc.copy_AST_change(ast, None, recurse_over_variable(check, ast.left, char_to_find, expr_to_replace), recurse_over_variable(check, ast.right, char_to_find, expr_to_replace))
        elif ast.content == '()': # e = (e)
        	if(mode == 0 || mode == 1):
                return recurse_over_variable(mode, ast.left, char_to_find)
            else:
				return lex_yacc.copy_AST_change(ast, None, recurse_over_variable(mode, ast.left, char_to_find, expr_to_replace))
        elif type(ast.content) == str and ast.content.startswith('++'): # e = e++ | e = ++e
            	if(mode == 0 || mode == 1):
	                return recurse_over_variable(check, ast.left, char_to_find)
	            else:
					lex_yacc.copy_AST_change(ast, None, check_free_variable(check, ast.left, char_to_find, expr_to_replace))
        elif type(ast.content) == AST: # e = id_ptr_or_array | function_app | var_assignment
            return calculate_expr(ast.content)
        else: # e = INT_VAL | FLOAT_VAL
            return ast.content
    elif ast.type == AST_TYPE.ID: # id_ptr_or_array = id
        return data_structure.memory.get_variable(ast.content)
    elif ast.type == AST_TYPE.ARR_VAR: #id_ptr_or_array = id array_decs
        index = calculate_expr(ast.content[0][0])
        name = ast.content[1]
        return data_structure.memory.get_array(name, index)
    elif ast.type == AST_TYPE.SEMI_STATEMENT:
        return calculate_expr(ast.left)
    elif ast.type == AST_TYPE.FUN_APP:
        if data_structure.return_table.value_returned:
            data_structure.return_table.value_returned = False
            return data_structure.return_table.return_value.pop()
        else:
            __unvisit()
            func = data_structure.function_table.get_ast(ast.content.fname)
            params = data_structure.function_table.get_params(ast.content.fname)
            data_structure.return_table.is_function_call = True
            search_stack.append((func, False, False, False))
            data_structure.set_current_line(func.start_lineno)

            variable = []
            variable_ptr = []
            arg_ind = 0
            for variable_type, name in params:
                arg = ast.content.arguments[arg_ind]
                if str(variable_type)[0] == '*':
                    variable_ptr.append(data_structure.memory.get_array_ptr(arg.content.content))
                else:
                    variable.append(calculate_expr(arg))
                arg_ind = arg_ind + 1
            data_structure.memory.new_scope_out()
            variable_ind = 0
            variable_ptr_ind = 0
            for variable_type, name in params:
                if str(variable_type)[0] == '*':
                    data_structure.memory.add_array_ptr(name, variable_ptr[variable_ptr_ind])
                    variable_ptr_ind = variable_ptr_ind + 1
                else:
                    lineno = data_structure.get_current_line()
                    data_structure.memory.add_variable(name, None, lineno)
                    data_structure.memory.add_variable(name, variable[variable_ind], lineno)
                    variable_ind = variable_ind + 1


def loop_optimizable(tree):
	loop = tree.get()
	if(loop.init_expr == None):
		return False
	if(loop.init_expr.type == lex_yacc.AST_TYPE.LOOP_INIT):
		if(type(loop.init_expr.get()) == tuple):
			if(loop.init_expr.get()[0].get() == 'float'):
				return False 
			var_assign = loop.init_expr.get()[1]
			if(var_assign.get()[0].type != lex_yacc.AST_TYPE.ID):
				return False
			if(var_assign.get()[1].type == lex_yacc.AST_TYPE.FUN_APP):
				return False
			if(check_free_variable(var_assign.get()[1])):
				return False
			loop_variable = var_assign.get()[0]
		else:
			var_assign = loop.init_expr.get().get()
			if(var_assign.type != lex_yacc.AST_TYPE.ASSIGN):
				return False
			if(var_assign.get()[1].type == lex_yacc.AST_TYPE.FUN_APP):
				return False
			if(check_free_variable(var_assign.get()[1])):
				return False
			loop_variable = var_assign.get()[0]

	if(loop.term_expr == None):
		return False
	if(loop.term_expr.type != lex_yacc.AST_TYPE.EXPR):
		return False
	if(not(loop.term_expr.get() == '<' || loop.term_expr.get() == '>')):
		return False
	comparison_op = loop.term_expr.get()
	if(not(find_and_get_var(loop.term_expr.left) == loop_variable)):
		return False
	if(check_free_variable(loop.term_expr.right)):
		return False

	if(loop.update_expr == None):
		return False

	# update_expr should be of the form like a = a + 1, a++
	if(loop.update_expr.type != lex_yacc.AST_TYPE.SEMI_STATEMENT):
		return False
	if(loop.update_expr.left.type == lex_yacc.AST_TYPE.ASSIGN):
		var_assign = loop.update_expr.left
		if(var_assign.get()[0].type != lex_yacc.AST_TYPE.ID):
			return False
		if(var_assign.get()[0].get() != loop_variable):
			return False
		if(var_assign.get()[1].type == lex_yacc.AST_TYPE.FUN_APP):
			return False
		if(comparison_op == '<'):
			if(var_assign.get()[1].get() != '+'):
				return False
		elif(comparison_op == '>'):
			if(var_assign.get()[1].get() != '-'):
				return False
		if(var_assign.get()[1].left.get() != loop_variable):
			return False
		if(check_free_variable(var_assign.get()[1].right)):
			return False

	elif(loop.update_expr.left.type == lex_yacc.AST_TYPE.EXPR):
		expr = loop.update_expr.left
		if(expr.get() == '++_left' || expr_get() == '++_right'):
			if(expr.left.type != lex_yacc.AST_TYPE.ID):
				return False
			if(expr.left.get() != loop_variable):
				return False
		else:
			return False

def	loop_unrolling(tree):

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

		if(loop_optimizable(tree)):
			loop_unrolling(tree)

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
