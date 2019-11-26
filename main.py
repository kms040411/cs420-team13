import lex_yacc
import get_input
import optimize
import run
import data_structures

if __name__ == "__main__":
    '''
        @TODO: parse argv to get the filename
    '''
    text = get_input.get_input(filename)
    tree = lex_yacc.parse(text)
    optimized = optimize.optimize(tree)
    run.run(optimized)
    print("End of interpreter")