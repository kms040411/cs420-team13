'''
    optimize(text):
    Optimize the given text and return optimized text.
'''
def optimize(text):
    '''
        @TODO: Implement optimize()
    '''
    result = dead_code_elimination(text)
    result = loop_unrolling(text)
    return result

def dead_code_elimination(text):
    pass

def loop_unrolling(text):
    pass