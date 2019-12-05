'''
    run():
    Execute given optimized tree.
    Get an input string from the user and execute this command.
'''
from lex_yacc import AST_TYPE, AST, arr_type
import data_structures

data_structure = data_structures.Global_Data_Structure()
search_stack = []

def run(optimized_tree):
    '''
        @TODO: implement run()
    '''

    start_line = -1
    for func in optimized_tree.content:
        #put functions in function table
        if func.type == AST_TYPE.FUNCTION:
            if not func.content.params:  #parameter empty
                if not data_structure.function_table.insert(func.content.name, func, func.content.return_type, []):
                    print('Error: redefinition of', func.content.name)
            else:
                if not data_structure.function_table.insert(func.content.name, func, func.content.return_type, list(func.content.params[0:-1][0])):
                    print('Error: redefinition of', func.content.name)

        if func.content.name == "main":
            start_line = func.start_lineno
            search_stack.append((func, False, False, False))
    if start_line == -1:
        print("There is no main function")

    data_structure.set_current_line(start_line)

    while(True):
        print(">>> ", end="")
        user_input = input()
        input_list = user_input.split(" ")
        if (input_list[0] == "next"):
            num_line = 0
            if (len(input_list) > 1):
                num_line = int(input_list[1])
            __next(num_line)

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
            break

# @private
def __next(num_line : int):
    current_linenum = data_structure.get_current_line()
    if (num_line == 0):
        data_structure.set_current_line(__execute(current_linenum))
    else:
        for i in range(num_line):
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
    tree = search_stack[-1][0]
    present_lineno = data_structure.get_current_line()
    
    while (True):
        if (tree.start_lineno != present_lineno):
            present_lineno = tree.start_lineno
            break

        print(tree.start_lineno, tree.end_lineno, tree.type)
        print(tree.content, tree.left, tree.right)

        if not search_stack[-1][3]:
            if tree.type != AST_TYPE.LOOP_INIT:
                __visit()
            if tree.type == AST_TYPE.FUNCTION:
                data_structure.memory.new_scope_out()
                search_stack.append((tree.content.body, False, False, False))
            elif tree.type == AST_TYPE.VAR_DEC:
                for variable_type, name in tree.content:
                    if type(variable_type) == arr_type:
                        dims = calculate_expr(variable_type.dims[0])
                        print('dims', dims)
                        data_structure.memory.add_array(name, dims, present_lineno)
                    else:
                        data_structure.memory.add_variable(name, None, present_lineno)
            elif tree.type == AST_TYPE.ASSIGN:
                name = tree.content[0].content
                value = calculate_expr(tree.content[1])
                if type(name) == tuple:
                    index = calculate_expr(name[0][0])
                    name = name[1]
                    print('test', index, name, value)
                    data_structure.memory.assign_array(name, index, value)
                else:
                    data_structure.memory.add_variable(name, value, present_lineno)
            elif tree.type == AST_TYPE.FOR:
                data_structure.memory.new_scope_in()
                loop_info = (tree.content.term_expr, tree.content.update_expr, tree.content.body, False)
                data_structure.loop_table.add_loop_info(loop_info)
                search_stack.append((tree.content.init_expr, False, False, False))
            elif tree.type == AST_TYPE.LOOP_INIT:
                if data_structure.loop_table.loop_first():
                    search_stack.append((tree.content, False, False, False))
                    data_structure.loop_table.loop_start()
                else:
                    if calculate_expr(data_structure.loop_table.loop_term()):
                        search_stack.append((data_structure.loop_table.loop_body(), False, False, False))

        else:
            if not search_stack[-1][1]:
                search_stack[-1] = (tree, True, False, True)
                if tree.left != None:
                    search_stack.append((tree.left, False, False, False))
            elif not search_stack[-1][2]:
                search_stack[-1] = (tree, True, True, True)
                if tree.right != None:
                    search_stack.append((tree.right, False, False, False))
            else:
                search_stack.pop()
        
        tree = search_stack[-1][0]
        
    data_structure.set_current_line(present_lineno)
    return

def calculate_expr(ast):
    if ast.type == AST_TYPE.EXPR:
        if ast.content in ['+', '-', '*', '/', '<', '>']:
            left = calculate_expr(ast.left)
            right = calculate_expr(ast.right)
            if ast.content == '+':
                return left + right
            elif ast.content == '-':
                return left - right
            elif ast.content == '*':
                return left * right
            elif ast.content == '/':
                return left // right
            elif ast.content == '<':
                return left < right
            elif ast.content == '>':
                return left > right 
        elif type(ast.content) == AST:
            return calculate_expr(ast.content)
        else:
            return ast.content
    elif ast.type == AST_TYPE.ID:
        return data_structure.memory.get_variable(ast.content)
    elif ast.type == AST_TYPE.ARR_VAR:
        index = calculate_expr(ast.content[0][0])
        name = ast.content[1]
        return data_structure.memory.get_array(name, index)
    elif ast.type == AST_TYPE.FUN_APP:
        print('fuck!!')

def __visit():
    tree = search_stack[-1][0]
    search_stack[-1] = (tree, False, False, True)

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
        print(data_structure.memory.get_variable(var))
    except:
        print("cannot find variable")
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
        print(history_list)
        for i in range(len(history_list)):
            value = history_list[i][0]
            linenum = str(history_list[i][1])
            if value is None:
                print(var + " = N/A at line " + linenum)
            else:
                print(var + " = " + str(value) + " at line " + linenum)
    except:
        print('cannot find variable')
    return
        