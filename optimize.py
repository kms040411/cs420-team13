'''
    optimize(text):
    Optimize the given tree and return optimized tree.
'''
def optimize(tree):
    '''
        @TODO: Implement optimize()
    '''
    result = dead_code_elimination(tree)
    result = loop_unrolling(result)
    return result

def dead_code_elimination(tree):
    pass

def loop_unrolling(tree):
    pass