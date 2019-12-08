'''
get_input(filename): 
Read the file specified in 'filename' and return the file as a string.
'''	
def get_input(filename):
	'''
	@TODO: Implement get_input()
	'''
	file = open(filename, 'r')
	data = file.read()
	file.close()
	return data