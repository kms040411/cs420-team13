import lex_yacc
import get_input
import optimize
import run
import data_structures

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

    #text = get_input.get_input(filename)
    text = get_input.get_input("test")

    tree = lex_yacc.parse(text)

    print(tree.start_lineno, tree.end_lineno, tree.content[1].content.body.left.left.end_lineno)
    dsf(tree.content[1])

    optimized = optimize.optimize(tree)

    #run.run(optimized)
    run.run(optimized)
    
    print("End of interpreter")