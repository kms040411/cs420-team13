'''
    run():
    Execute given optimized tree.
    Get an input string from the user and execute this command.
'''
from lex_yacc import AST_TYPE
import data_structures

data_structure = data_structures.Global_Data_Structure()
search_stack = []

def run(optimized_tree):
    '''
        @TODO: implement run()
    '''

    start_line = -1
    for func in optimized_tree.content:
        if func.type == AST_TYPE.FUNCTION:
            if not func.content.params:  #parameter empty
                if not data_structure.function_table.insert(func.content.name, func, func.content.return_type, []):
                    print('redefinition of', func.content.name)
            else:
                if not data_structure.function_table.insert(func.content.name, func, func.content.return_type, list(func.content.params[0:-1][0])):
                    print('redefinition of', func.content.name)

        if func.content.name == "main":
            start_line = func.start_lineno
            search_stack.append((func, False, False))
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
                __print(var, data_structure)

        elif (input_list[0] == "trace"):
            if (len(input_list) <= 1):
                continue
            else:
                var = input_list[1]
                __trace(var, data_structure)
        
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

        if tree.type == AST_TYPE.FUNCTION:
            data_structure.memory.new_scope_in()
            search_stack.append((tree.content.body, False, False))
        else:
            if not search_stack[-1][1]:
                search_stack[-1] = (tree, True, False)
                if tree.left != None:
                    search_stack.append((tree.left, False, False))
            elif not search_stack[-1][2]:
                search_stack[-1] = (tree, True, True)
                if tree.right != None:
                    search_stack.append((tree.right, False, False))
            else:
                search_stack.pop()
        
        tree = search_stack[-1][0]
        
    data_structure.set_current_line(present_lineno)
    return

# @private
def __print(var : str, data_structure):
    scope_stack = data_structure.scope_stack
    symbol_table = scope_stack.get_symbol_table()
    if symbol_table is None:
        print("Cannot find value")
        return
    value = symbol_table.get_value(var)
    if value is None:
        print("Cannot find value")
        return
    print(value)
    return

# @private
def __trace(var : str, data_structure):
    scope_stack = data_structure.scope_stack
    symbol_table = scope_stack.get_symbol_table()
    if symbol_table is None:
        print("Cannot find value")
        return
    history_list = symbol_table.get_history(var)
    for i in range(len(history_list)):
        linenum = history_list[i][0]
        value = history_list[i][1]
        if value is None:
            print(var + " = N/A at line " + linenum )
        else:
            print(var + " = " + value + " at line " + linenum )
    return
        
