'''
    dead_code_elmination(text):
    Optimize the given text and return optimized text.
'''
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
        # Unused member
        self.next = list()
    
    def mark(self):
        self.marked = True
    
    def is_marked(self):
        return self.marked

    # Unused function
    def insert_next(self, next_linenum):
        self.next.append(next_linenum)

def mark(code_list):
    line_table = Line_Table()
    linenum = 0
    for i in code_list:
        linenum = linenum + 1
        line_table.insert_line(linenum, i)
    
    read_and_mark(line_table, 1, linenum, True)
    return line_table

'''
    read_and_mark(line_table, start_linenum, end_linenum, func : bool, prev_status : bool):
    read lines from start_linenum to end_linenum. Mark all reachable lines.
'''
def read_and_mark(line_table, start_linenum, end_linenum, func, prev_status = True):
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
        return True
    else:
        current_line = start_linenum
        while(current_line < end_linenum):
            current_text = line_table.return_line(current_line).text
            # Mark current line
            line_table.return_line(current_line).mark()

            # Check line if there is "for"
            if "for" in split_all(current_text):
                (start, end) = find_start_end(line_table, current_line)
                # Read inside For Loop
                read_and_mark(line_table, start, end, False)
                # Read after For Loop
                read_and_mark(line_table, end, end_linenum, False)
                return True
            
            # Check line if there is "else if"
            elif "else if" in current_text and "if" in split_all(current_text) and "else" in split_all(current_text):
                (start, end) = find_start_end(line_table, current_line)
                # Read inside else if block
                prev_result = read_and_mark(line_table, start, end, False)
                # Read after else if block
                # prev_result is False if there is a "return" in else if block
                read_and_mark(line_table, end, end_linenum, False, prev_result or prev_status)
                return True

            # Check line if there is "if"
            elif "if" in split_all(current_text):
                (start, end) = find_start_end(line_table, current_line)
                # Read inside if block
                prev_result = read_and_mark(line_table, start, end, False)
                # Read after if block
                # prev_result is False if there is a "return" in if block
                read_and_mark(line_table, end, end_linenum, False, prev_result)
                return True

            # check line if there is "else"
            elif "else" in split_all(current_text):
                (start, end) = find_start_end(line_table, current_line)
                # Read inside else block
                read_and_mark(line_table, start, end_linenum, False)
                # Read after else block
                if prev_status is True:
                    read_and_mark(line_table, end, end_linenum, False)
                return True

            # Check line if there is "return"
            elif "return" in split_all(current_text):
                return False # Don't Proceed After Return

            else:
                current_line = current_line + 1 # Proceed
        return True

'''
    find_start_end(line_table, start_linenum):
    returns linenum of "{" and linenum of "}"
'''
def find_start_end(line_table, start_linenum):
    current_line = start_linenum
    start = 0
    end = 0
    bracket = 0

    while(True):
        current_text = line_table.return_line(current_line).text
        if bracket == 0:
            line_table.return_line(current_line).mark()         # Mark Before-"{" Line and "{" Line
        for i in current_text:
            if i == "{":
                if bracket == 0:
                    start = current_line
                bracket += 1
            if i == "}":
                if bracket == 0:
                    continue
                if bracket == 1:
                    end = current_line
                    line_table.return_line(current_line).mark()     # Mark "}" Line
                    return (start + 1, end)
                bracket -= 1
        current_line = current_line + 1

'''
    sweep(line_table, code_list):
    rewrite the entire source code without unmarked lines.
'''
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