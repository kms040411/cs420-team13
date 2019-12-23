'''
    run():
    Execute given optimized tree.
    Get an input string from the user and execute this command.
'''
from lex_yacc import AST_TYPE, AST, arr_type
import data_structures
from exceptions import FunctionReturned
import sys

data_structure = data_structures.Global_Data_Structure()
function_stack = [[]] # each entry: search_stack
search_stack = function_stack[-1]

def run_procedure(): #run procedure, returns its return value
    # search_stack.append((func, False, False, False))
    func = search_stack[-1][0]
    try:
        if func.content.name != "main":
            __next() # execute remaining lines first
        while(True):
            print(">>> ", end="")
            user_input = input()
            input_list = user_input.split()
            if (input_list[0] == "next"):
                __next.executed_lines = 0
                __next.num_lines = 1
                if (len(input_list) > 1):
                    __next.num_lines = int(input_list[1])
                __next()

            elif (input_list[0] == "print"):
                if (len(input_list) <= 1):
                    continue
                else:
                    var = input_list[1]
                    __print(var)

            elif (input_list[0] == "trace"):
                if (len(input_list) <= 1):
                    continue
                else:
                    var = input_list[1]
                    __trace(var)
            
            elif (input_list[0] == "quit"):
                sys.exit(0)
    
    except FunctionReturned:
        assert data_structure.return_table.value_returned
        data_structure.return_table.value_returned = False
        return data_structure.return_table.return_value.pop()

def run(optimized_tree):
    '''
        @TODO: implement run()
    '''
    global search_stack
    start_line = -1
    main_func = None
    for func in optimized_tree.content:
        # put functions in function table
        if func.type == AST_TYPE.FUNCTION:
            if not func.content.params:  # parameter empty
                if not data_structure.function_table.insert(func.content.name, func, func.content.return_type, []): #func.content.body
                    print('Error: redefinition of', func.content.name)
            else:
                if not data_structure.function_table.insert(func.content.name, func, func.content.return_type, func.content.params):
                    print('Error: redefinition of', func.content.name)

        if func.content.name == "main":
            start_line = func.start_lineno
            data_structure.set_current_line(start_line)
            search_stack.append((func, False, False, False))
            main_func = func
            # data_structure.memory.new_scope_out()
    if start_line == -1:
        print("There is no main function")
        sys.exit(0)

    # data_structure.set_current_line(start_line)
    run_procedure()

    # while(True):
    #     print(">>> ", end="")
    #     user_input = input()
    #     input_list = user_input.split(" ")
    #     if (input_list[0] == "next"):
    #         __next.executed_lines = 0
    #         __next.num_lines = 1
    #         if (len(input_list) > 1):
    #             __next.num_lines = int(input_list[1])
    #         __next()

    #     elif (input_list[0] == "print"):
    #         if (len(input_list) <= 1):
    #             continue
    #         else:
    #             var = input_list[1]
    #             __print(var)

    #     elif (input_list[0] == "trace"):
    #         if (len(input_list) <= 1):
    #             continue
    #         else:
    #             var = input_list[1]
    #             __trace(var)
        
    #     elif (input_list[0] == "quit"):
    #         break

# @private
def __next():
    current_linenum = data_structure.get_current_line()
    while __next.executed_lines < __next.num_lines:
        __next.executed_lines += 1
        __execute()
        #current_linenum = data_structure.get_current_line()
        #data_structure.set_current_line(__execute(current_linenum))
    return

''' 
    __execute(linenum):
    Execute given line and returns next line number
'''
# @private
def __execute():
    global search_stack
    tree = search_stack[-1][0]
    present_lineno = data_structure.get_current_line()

    print('present line number : ' + str(present_lineno))
    
    while (True):
        if tree is None:
            break
        if (tree.start_lineno != present_lineno and not (tree.start_lineno <= present_lineno and present_lineno <= tree.end_lineno)):
            present_lineno = tree.start_lineno
            break

        #print(tree.start_lineno, tree.end_lineno, tree.type)
        #print(tree.content, tree.left, tree.right)
        #print(tree)

        if not search_stack[-1][3]:

            if tree.type != AST_TYPE.LOOP_INIT:
                __visit()
            
            if tree.type == AST_TYPE.FUNCTION:
                search_stack.append((tree.content.body, False, False, False))
            elif tree.type == AST_TYPE.VAR_DEC:
                for variable_type, name in tree.content:
                    if type(variable_type) == arr_type:
                        dims = calculate_expr(variable_type.dims[0])
                        data_structure.memory.add_variable_type(name, variable_type.type)
                        data_structure.memory.add_array(name, dims, present_lineno)
                    else:
                        data_structure.memory.add_variable_type(name, variable_type)
                        data_structure.memory.add_variable(name, None, present_lineno)
            elif tree.type == AST_TYPE.ASSIGN:
                name = tree.content[0].content
                value = calculate_expr(tree.content[1])
                #print(name, value)
                if type(name) == tuple:
                    index = 0 if type(name[0]) == int else calculate_expr(name[0][0]) #pointer
                    name = name[1]
                    data_structure.memory.assign_array(name, index, value)
                else:
                    data_structure.memory.add_variable(name, value, present_lineno)
            elif tree.type == AST_TYPE.FOR:
                data_structure.memory.scope_in()
                loop_info = (tree.content.term_expr, tree.content.update_expr, tree.content.body, False, False)
                data_structure.loop_table.add_loop_info(loop_info)
                search_stack.append((tree.content.init_expr, False, False, False))
            elif tree.type == AST_TYPE.LOOP_INIT:
                if data_structure.loop_table.loop_first():
                    search_stack.append((tree.content, False, False, False))
                    data_structure.loop_table.loop_start()
                else:
                    if data_structure.loop_table.loop_second():
                        calculate_expr(data_structure.loop_table.loop_update())
                    if calculate_expr(data_structure.loop_table.loop_term()):
                        search_stack.append((data_structure.loop_table.loop_body(), False, False, False))
                    else:
                        __visit()
                    data_structure.loop_table.loop_start_update()
            elif tree.type == AST_TYPE.IF:
                data_structure.memory.scope_in()
                if not calculate_expr(tree.content):
                    __stop_search()
                else:
                    __stop_elif_else()
            elif tree.type == AST_TYPE.ELIF_ELSE:
                data_structure.memory.scope_in()
                #elif case
                if not (tree.content == True):
                    #condition False
                    if not calculate_expr(tree.content):
                        __next_elif()
                    #condition True
                    else:
                        __stop_behind_elif_else()
                #else case: just go left without any action

            elif tree.type == AST_TYPE.EXPR:
                calculate_expr(tree)
                __stop_search()

            elif tree.type == AST_TYPE.RETURN:
                __stop_search()
                return_value = None if tree.left is None else calculate_expr(tree.left)
                data_structure.return_table.value_returned = True
                data_structure.return_table.return_value.append(return_value)
                #print('value returned: %d' % return_value)
                data_structure.memory.function_return()
                if len(function_stack) > 1:
                    function_stack.pop() #destroy frame
                    search_stack = function_stack[-1]
                    raise FunctionReturned

            elif tree.type == AST_TYPE.FUN_APP:
                if tree.content.fname == 'printf':
                    format_string = tree.content.arguments[0][1:-1]
                    format_string = format_string.replace('\\n', '\n')
                    args = tuple(map(calculate_expr, tree.content.arguments[1:]))
                    print(format_string % args, end = '')
                else:
                    calculate_expr(tree)

            # if data_structure.return_table.is_function_call:
            #     __unvisit()
            #     data_structure.return_table.is_function_call = False
            #     #print(data_structure.memory.present)
            #     return

        else:
            if not search_stack[-1][1]:
                search_stack[-1] = (tree, True, search_stack[-1][2], True)
                if tree.left != None:
                    search_stack.append((tree.left, False, False, False))
            elif not search_stack[-1][2]:
                search_stack[-1] = (tree, True, True, True)
                if tree.right != None:
                    search_stack.append((tree.right, False, False, False))
            else:
                if tree.type == AST_TYPE.FOR:
                    #data_structure.memory.delete_scope()
                    data_structure.memory.scope_out()
                    data_structure.loop_table.table.pop()
                elif tree.type == AST_TYPE.IF:
                    #data_structure.memory.delete_scope()
                    data_structure.memory.scope_out()
                elif tree.type == AST_TYPE.FUNCTION:
                    if tree.content.name == "main":
                        print('End of program')
                        return
                    else:
                        __stop_search()
                        if not data_structure.return_table.value_returned: # end of function body with no return statement
                            return_value = None
                            data_structure.return_table.value_returned = True
                            data_structure.return_table.return_value.append(return_value)
                            data_structure.memory.function_return()
                            function_stack.pop() #destroy frame
                            search_stack = function_stack[-1]
                            tree = search_stack[-1][0]
                            # continue
                            raise FunctionReturned
                
                search_stack.pop()
        
        tree = search_stack[-1][0]
        
    data_structure.set_current_line(present_lineno)
    return

def calculate_expr(ast):
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
    global search_stack
    if ast.type == AST_TYPE.EXPR:
        if ast.content in ['+', '-', '*', '/', '<', '>']:
            left = calculate_expr(ast.left)
            if ast.content == '-' and ast.right is None: # e = -e
                return -left
            right = calculate_expr(ast.right)
            #print(ast.left)
            #print(ast.right)
            if ast.content == '+': # e = e + e
                return left + right
            elif ast.content == '-': # e = e - e
                return left - right
            elif ast.content == '*': # e = e * e
                return left * right
            elif ast.content == '/': # e = e / e
                if type(left) == float or type(right) == float:
                    return left / right
                else:
                    return left // right
            elif ast.content == '<': # e = e < e
                return left < right 
            elif ast.content == '>': # e = e > e
                return left > right 
        elif ast.content == '()':
            return calculate_expr(ast.left)
        elif type(ast.content) == str and ast.content.startswith('++'):
            name = ast.left.content
            old_val = calculate_expr(ast.left)
            new_val = old_val + 1
            data_structure.memory.add_variable(name, new_val, data_structure.get_current_line())
            return new_val if ast.content == '++_left' else old_val
        elif ast.content == '()': # e = (e)
            return calculate_expr(ast.left)
        elif type(ast.content) == AST: # e = id_ptr_or_array | function_app | var_assignment
            return calculate_expr(ast.content)
        elif ast.content == '&':
            return ast.left.content.content
        else: # e = INT_VAL | FLOAT_VAL
            return ast.content
    elif ast.type == AST_TYPE.ID: # id_ptr_or_array = id
        return data_structure.memory.get_variable(ast.content)
    elif ast.type == AST_TYPE.PTR_VAR:
        address = data_structure.memory.get_variable(ast.content[1])
        return data_structure.memory.get_variable(address)
    elif ast.type == AST_TYPE.ARR_VAR: #id_ptr_or_array = id array_decs
        index = calculate_expr(ast.content[0][0])
        name = ast.content[1]
        return data_structure.memory.get_array(name, index)
    elif ast.type == AST_TYPE.SEMI_STATEMENT:
        return calculate_expr(ast.left)
    elif ast.type == AST_TYPE.FUN_APP:
        # __unvisit()
        func = data_structure.function_table.get_ast(ast.content.fname)
        params = data_structure.function_table.get_params(ast.content.fname)
        # data_structure.return_table.is_function_call = True
        search_stack = []
        search_stack.append((func, False, False, False))
        function_stack.append(search_stack) # setup new frame
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
        data_structure.memory.function_call()
        variable_ind = 0
        variable_ptr_ind = 0
        for variable_type, name in params:
            if str(variable_type)[0] == '*':
                data_structure.memory.add_array_ptr(name, variable_ptr[variable_ptr_ind])
                variable_ptr_ind = variable_ptr_ind + 1
            else:
                lineno = data_structure.get_current_line()
                data_structure.memory.add_variable_type(name, variable_type)
                data_structure.memory.add_variable(name, None, lineno)
                data_structure.memory.add_variable(name, variable[variable_ind], lineno)
                variable_ind = variable_ind + 1
        # __next.executed_lines += 1
        return run_procedure()

def __visit():
    search_stack = function_stack[-1]
    tree = search_stack[-1][0]
    search_stack[-1] = (tree, False, False, True)    

def __unvisit():
    search_stack = function_stack[-1]
    tree = search_stack[-1][0]
    search_stack[-1] = (tree, False, False, False)

def __unvisit_caller():
    print(function_stack)
    tree = function_stack[-2][-1][0]
    function_stack[-2][-1] = (tree, False, False, False)
    print(function_stack)
    sys.exit(0)

def __stop_search():
    search_stack = function_stack[-1]
    tree = search_stack[-1][0]
    search_stack[-1] = (tree, True, True, True)
    
def __stop_elif_else():
    search_stack = function_stack[-1]
    tree = search_stack[-2][0]
    #can eliminate dead code
    search_stack[-2] = (tree, True, True, True)

def __stop_behind_elif_else():
    search_stack = function_stack[-1]
    tree = search_stack[-1][0]
    #for dead code elimination
    # tree.right = None
    search_stack[-1] = (tree, False, True, True)

def __next_elif():
    search_stack = function_stack[-1]
    tree = search_stack[-1][0]
    #can eliminate dead code
    search_stack[-1] = (tree, True, False, True)

# @private
def __print(var : str):
    #scope_stack = data_structure.scope_stack
    #symbol_table = scope_stack.get_symbol_table()
    #if symbol_table is None:
    #    print("Cannot find value")
    #    return
    #value = symbol_table.get_value(var)
    #if value is None:
    #    print("Cannot find value")
    #    return
    #print(value)

    try:
        value = data_structure.memory.get_variable(var)
        if value == None:
            print('N/A')
        else:
            print(value)
    except:
        print("Invisible variable")
    return

# @private
def __trace(var : str):
    #scope_stack = data_structure.scope_stack
    #symbol_table = scope_stack.get_symbol_table()
    #if symbol_table is None:
    #    print("Cannot find value")
    #    return
    try:
        history_list = data_structure.memory.get_history(var)#symbol_table.get_history(var)
        #print(history_list)
        for i in range(len(history_list)):
            value = history_list[i][0]
            linenum = str(history_list[i][1])
            if value is None:
                print(var + " = N/A at line " + linenum)
            else:
                print(var + " = " + str(value) + " at line " + linenum)
    except:
        print('Invisible variable')
    return
        
