'''
    get_input(filename): 
    Read the file specified in 'filename' and return the file as a string.
'''
def get_input(filename):
    '''
        @TODO: Implement get_input()
    '''
    with open(filename, 'r') as file:
	    data = file.read()
    return data