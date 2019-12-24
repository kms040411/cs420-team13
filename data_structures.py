from exceptions import *

class Global_Data_Structure():
    def __init__(self):
        self.function_table = Function_table()
        self.memory = VariableTable()
        self.loop_table = LoopTable()
        self.return_table = ReturnTable()
        self.current_line = 0
        self.print_linenum = True
        return
    
    def set_current_line(self, linenum):
        self.current_line = linenum
        return
    
    def get_current_line(self):
        return self.current_line


class Function_table():
    def __init__(self):
        self.map = dict()
        return

    def insert(self, name, ast, return_type, argument_types):
        if name in self.map:
            return False
        else:
            self.map[name] = Function_table_entry(ast, return_type, argument_types)
            return True
    
    # @private
    def __get(self, name):
        return self.map[name].get()
    
    def get_ast(self, name):
        return self.__get(name)[0]

    def get_params(self, name):
        return self.__get(name)[2]
    
    def get_types(self, name):
        '''
            get_types(name):
            returns a tuple(Return Type, Argument Types)
        '''
        return self.__get(name)[1:]


class Function_table_entry():
    def __init__(self, ast, return_type, argument_types):
        self.ast = ast
        self.return_type = return_type
        self.argument_types = argument_types
        return
    
    def get(self):
        return (self.ast, self.return_type, self.argument_types)


class VariableTable():
    def __init__(self):
        self.tables = [[dict()]]
        self.type_tables = [[dict()]]

    def function_call(self): #previously new_scope_in
        self.tables.append([dict()])
        self.type_tables.append([dict()])

    def function_return(self): #previously new_scope_out
        self.tables.pop()
        self.type_tables.pop()
    
    def scope_in(self):
        self.tables[-1].append(dict())
        self.type_tables[-1].append(dict())
    
    def scope_out(self):
        self.tables[-1].pop()
        self.type_tables[-1].pop()

    def add_variable_type(self, name, variable_type):
        self.type_tables[-1][-1][name] = variable_type

    def get_variable_type(self, name):
        current_function_scope = self.type_tables[-1]
        for scope in reversed(current_function_scope):
            if name in scope:
                return scope[name]

        raise Exception('undefined variable: ' + name)

    def add_variable(self, name, value, lineno):
        if value == None:
            self.tables[-1][-1][name] = []
        else:
            variable_type = self.get_variable_type(name)
            if variable_type == 'int':
                value = int(value)
            elif variable_type == 'float':
                value = float(value)
        self.get_history(name).append((value, lineno))

    def add_array(self, name, dims, lineno):
        self.tables[-1][-1][name] = [None] * dims

    def add_array_ptr(self, name, ptr):
        self.tables[-1][-1][name] = ptr

    def assign_array(self, name, index, value):
        variable_type = self.get_variable_type(name)
        if variable_type == 'int':
            value = int(value)
        elif variable_type == 'float':
            value = float(value)
        self.get_history(name)[index] = value
        
    def get_variable(self, name):
        return self.get_history(name)[-1][0]

    def get_array(self, name, index):
        return self.get_history(name)[index]

    def get_array_ptr(self, name):
        return self.get_history(name)

    def get_history(self, name):
        current_function_scope = self.tables[-1]
        for scope in reversed(current_function_scope):
            if name in scope:
                return scope[name]

        raise Exception('undefined variable: ' + name)


class LoopTable():
    def __init__(self):
        self.table = []

    def add_loop_info(self, loop_info):
        self.table.append(loop_info)

    def loop_first(self):
        return not self.table[-1][3]

    def loop_start(self):
        term, update, body, _, second = self.table[-1]
        self.table[-1] = (term, update, body, True, second)

    def loop_second(self):
        return self.table[-1][4]

    def loop_start_update(self):
        term, update, body, first, _ = self.table[-1]
        self.table[-1] = (term, update, body, first, True)

    def loop_end(self):
        self.table.pop()

    def loop_term(self):
        return self.table[-1][0]
    
    def loop_update(self):
        return self.table[-1][1]

    def loop_body(self):
        return self.table[-1][2]


class ReturnTable():
    def __init__(self):
        self.table = []
        self.return_value = []
        self.is_function_call = False
        self.value_returned = False
