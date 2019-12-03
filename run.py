'''
    run():
    Execute given optimized tree.
    Get an input string from the user and execute this command.
'''
import data_structures

def run(optimized_tree, data_structure):
    '''
        @TODO: implement run()
    '''
    while(True):
        print(">>> ", end="")
        user_input = input()
        input_list = user_input.split(" ")
        if (input_list[0] == "next"):
            num_line = 0
            if (len(input_list) > 1):
                num_line = int(input_list[1])
            __next(num_line, data_structure)

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
def __next(num_line : int, data_structure):
    current_linenum = data_structure.get_current_line()
    if (num_line == 0):
        data_structure.set_current_line(__execute(current_linenum))
    else:
        for i in range(num_line):
            current_linenum = data_structure.get_current_line()
            data_structure.set_current_line(__execute(current_linenum))
    return

''' 
    __execute(linenum):
    Execute given line and returns next line number
'''
# @private
def __execute(linenum : int):
    pass

# @private
def __print(var : str, data_structure):
    scope_stack = data_structure.scope_stack
    symbol_table = scope_stack.find_table_from_variable(var)
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
    symbol_table = scope_stack.find_table_from_variable(var)
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
        