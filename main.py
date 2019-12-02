import lex_yacc
import get_input
import optimize
import run
import data_structures

if __name__ == "__main__":
    '''
        @TODO: parse argv to get the filename
    '''
    data_structure = data_structures.Global_Data_Structure()

    #text = get_input.get_input(filename)
    text = get_input.get_input("test")

    tree = lex_yacc.parse(text)

    optimized = optimize.optimize(tree)

    #run.run(optimized)
    run.run("test", data_structure)
    
    print("End of interpreter")