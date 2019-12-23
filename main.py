import lex_yacc
import get_input
import optimize
import run
import data_structures
import sys
import uce

def dsf(tree):
    if tree == None:
        return
    print(tree.start_lineno, tree.end_lineno)
    print(tree.type)
    if tree.type == lex_yacc.AST_TYPE.FOR:
        print(tree.content.body)
    dsf(tree.left)
    dsf(tree.right)

if __name__ == "__main__":
    '''
        @TODO: parse argv to get the filename
    '''
    #data_structure = data_structures.Global_Data_Structure()
    if len(sys.argv) < 2:
        print("usage: " + sys.argv[0] + " [input file name]")
        sys.exit(0)
    text = get_input.get_input(sys.argv[1])
    text = uce.unreachable_code_elimination(text)
    # print(text) #test
    tree = lex_yacc.parse(text)
    if(len(sys.argv) == 3 and sys.argv[2] == 'op'):
        optimize.optimize_init(tree)
    run.run(tree)
    sys.exit(0) #for testings
    
    #print(tree.start_lineno, tree.end_lineno, tree.content[1].content.body.left.left.end_lineno)
    #dsf(tree.content[1])
    

    # text = get_input.get_input('optimized.c')
    # optimized = lex_yacc.parse(text)
    # run.run(optimized)
    
    # print("End of interpreter")