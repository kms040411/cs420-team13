import lex_yacc
import get_input
import optimize
import run
import data_structures
import sys
import uce

if __name__ == "__main__":
    '''
        @TODO: parse argv to get the filename
    '''
    if len(sys.argv) < 2:
        print("usage: " + sys.argv[0] + " [input file name]")
        sys.exit(0)
    text = get_input.get_input(sys.argv[1])
    text = uce.unreachable_code_elimination(text)
    tree = lex_yacc.parse(text)
    if (len(sys.argv) >= 3 and sys.argv[2] == 'op') or (len(sys.argv) >= 4 and sys.argv[3] == 'op'):
        optimize.optimize_init(tree)
    print_linenum = True
    if (len(sys.argv) >= 3 and sys.argv[2] == 'off_line') or (len(sys.argv) >= 4 and sys.argv[3] == 'off_line'):
        print_linenum = False
    run.run(tree, print_linenum)
    sys.exit(0)