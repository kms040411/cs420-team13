import re

'''
    optimize(text):
    Optimize the given text and return optimized text.
'''
def optimize(text):
    '''
        @TODO: Implement optimize()
    '''
    result = dead_code_elimination(text)
    print(result)
    result = loop_unrolling(result)
    return result

def dead_code_elimination(text):
    code_list = text.split("\n")
    line_table = mark(code_list)
    return sweep(line_table, code_list)

class Line_Table():
    def __init__(self):
        self.map = dict()
    
    def insert_line(self, linenum, text):
        self.map[linenum] = Line_Table_Entry(text)
    
    def return_line(self, linenum):
        return self.map[linenum]
    
class Line_Table_Entry():
    def __init__(self, text):
        self.text = text
        self.marked = False
    
    def mark(self):
        self.marked = True
    
    def is_marked(self):
        return self.marked

def mark(code_list):
    line_table = Line_Table()
    linenum = 0
    for i in code_list:
        linenum = linenum + 1
        line_table.insert_line(linenum, i)
    
    read_and_mark(line_table, 1, linenum, True)
    return line_table

def read_and_mark(line_table, start_linenum, end_linenum, func):
    print("read from " + str(start_linenum) + " to " + str(end_linenum))
    if func is True:
        current_linenum = start_linenum
        # Mark current line
        line_table.return_line(current_linenum).mark()
        
        (start, end) = find_start_end(line_table, current_linenum)
        # Read inside the Function
        read_and_mark(line_table, start, end, False)
        # Read after the Function
        if end + 1 < end_linenum:
            read_and_mark(line_table, end + 1, end_linenum, True)
        return
    else:
        current_line = start_linenum
        while(current_line < end_linenum):
            current_text = line_table.return_line(current_line).text
            # Mark current line
            line_table.return_line(current_line).mark()

            print(split_all(current_text))
            # Check line if there is "for"
            if "for" in split_all(current_text):
                print("for found")
                (start, end) = find_start_end(line_table, current_line)
                # Read inside For Loop
                read_and_mark(line_table, start, end, False)
                # Read after For Loop
                read_and_mark(line_table, end, end_linenum, False)
                return
            
            # Check line if there is "else if"
            elif "else if" in current_text and "if" in split_all(current_text) and "else" in split_all(current_text):
                print("else if found")
                (start, end) = find_start_end(line_table, current_line)
                # Read inside else if block
                read_and_mark(line_table, start, end, False)
                # Read after else if block
                read_and_mark(line_table, end, end_linenum, False)
                return

            # Check line if there is "if"
            elif "if" in split_all(current_text):
                print("if found")
                (start, end) = find_start_end(line_table, current_line)
                # Read inside if block
                read_and_mark(line_table, start, end, False)
                # Read after if block
                read_and_mark(line_table, end, end_linenum, False)
                return

            # check line if there is "else"
            elif "else" in split_all(current_text):
                print("else found")
                (start, end) = find_start_end(line_table, current_line)
                # Read inside else block
                read_and_mark(line_table, start, end, False)
                # Read after else block
                read_and_mark(line_table, end, end_linenum, False)
                return

            # Check line if there is "return"
            elif "return" in split_all(current_text):
                print("return found")
                return  # Don't Proceed After Return

            else:
                current_line = current_line + 1 # Proceed

# returns linenum of "{" and linenum of "}"
def find_start_end(line_table, start_linenum):
    current_line = start_linenum
    start = 0
    end = 0
    bracket = 0
    while(True):
        current_text = line_table.return_line(current_line).text
        if bracket == 0:
            line_table.return_line(current_line).mark()         # Mark Before "{" Line and "{" Line
        if "{" in current_text:
            if bracket == 0:
                start = current_line
            bracket = bracket + 1
        if "}" in current_text:
            if bracket == 1:
                end = current_line
                line_table.return_line(current_line).mark()     # Mark "}" Line
                return (start + 1, end)
            else:
                bracket = bracket - 1
        current_line = current_line + 1

def sweep(line_table, code_list):
    linenum = 0
    result = ""
    for i in code_list:
        linenum = linenum + 1
        if line_table.return_line(linenum).is_marked():
            result = result + i + "\n"
    return result

def split_all(text):
    text_list = list()
    text_list.append(text)
    result = list()
    for i in text_list:
        result = result + i.split(" ")
    result2 = list()
    for i in result:
        result2 = result2 + i.split("(")
    result3 = list()
    for i in result2:
        result3 = result3 + i.split(")")
    result4 = list()
    for i in result3:
        result4 = result4 + i.split(";")
    result5 = list()
    for i in result4:
        result5 = result5 + i.split("{")
    result6 = list()
    for i in result5:
        result6 = result6 + i.split("}")
    result7 = list()
    for i in result6:
        result7 = result7 + i.split("\t")
    return result7

def loop_unrolling(text):
    pass