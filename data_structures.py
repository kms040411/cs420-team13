from exceptions import *

class Global_Data_Structure():
    def __init__(self):
        self.function_table = Function_table()
        self.global_symbol_table = Global_Symbol_table()
        self.scope_stack = Scope_stack()
        self.current_line = 0
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
        if self.map[name] is not None:
            return False
        else:
            self.map[name] = Function_table_entry(ast, return_type, argument_types)
            return True
    
    # @private
    def __get(self, name):
        return self.map[name].get()
    
    def get_ast(self, name):
        return self.__get(name)[0]
    
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

class Symbol_table():
    def __init__(self):
        self.map = dict()
        return
    
    def insert(self, name, sym_type):
        if self.map[name] is not None:
            return False
        else:
            self.map[name] = Symbol_table_entry(sym_type)
    
    def get_value(self, name):
        return self.map[name].get_value()

    def set_value(self, name, linenum, value):
        return self.map[name].set_value(linenum, value)
    
    def get_history(self, name):
        return self.map[name].get_history()
    
    def get_type(self, name):
        return self.map[name].get_type

class Symbol_table_entry():
    def __init__(self, sym_type):
        self.sym_type = sym_type
        self.history = History()
        return
    
    def get_value(self):
        return self.history.get_recent()
    
    def set_value(self, linenum, value):
        '''
            @TODO: Need to check type of 'value'
        '''
        return self.history.insert(linenum, value)
    
    def get_type(self):
        return self.sym_type
    
    def get_history(self):
        return self.history.get_all()

class Global_Symbol_table(Symbol_table):
    def __init__(self):
        super().__init__()
        return

class History():
    def __init__(self):
        self.list = list()
        return
    
    def insert(self, linenum, value):
        length = len(self.list)
        if self.list[length - 1][0] == linenum:
            return False
        else:
            self.list.append((linenum, value))
            return True
    
    def get_recent(self):
        length = len(self.list)
        return self.list[length - 1][1]
    
    def get_all(self):
        return self.list
    
class Scope_stack():
    def __init__(self):
        self.stack = list()
        return
    
    def push(self, scope_type, linenum):
        # linenum : if scope_type is "For", linenum means the line number where for loop starts
        #           if scope_type is "Function", linenum means the line number where the function returns
        self.stack.append(scope_type, linenum)
        return
    
    def pop(self):
        return self.stack.pop()
    
    # @private
    def __top(self):
        length = len(self.stack)
        if (length == 0):
            return None
        return self.stack[length - 1]
    
    def get_symbol_table(self):
        top = self.__top()
        if top is None:
            return None
        return top.get_symbol_table()
    
    def get_start_point(self):
        if self.__top().scope_type != "For":
            raise ScopeTypeError
        else:
            return self.__top().linenum

class Scope_stack_entry():
    def __init__(self, scope_type, linenum):
        self.scope_type = scope_type
        self.linenum = linenum
        self.symbol_table = Symbol_table()
        return
    
    def get_symbol_table():
        return self.symbol_table