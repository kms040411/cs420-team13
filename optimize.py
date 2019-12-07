import lex_yacc

'''
    optimize(tree):
    Optimize the given tree and return optimized tree.
'''
def optimize(tree):
    if(tree.type == lex_yacc.AST_TYPE.PROGRAM):
    	for func in tree.content:
    		optimize(func)
    elif(tree.type == lex_yacc.AST_TYPE.FUNCTION):
    	func = tree.content
    	print(func.return_type + ' ' + func.name +  '(', end = '')
    	for param in func.params:
    		param_type = param[0]
    		param_name = param[1]
    		if(type(param_type) == lex_yacc.arr_type):
    			print(param_type.type + ' ' + param_name, )
    			for dim in dims:
    				print('[' + dim + ']')
    		elif(type(param_type) == lex_yacc.ptr_type):
    			pass
    		else:
    			pass
    	print('){')




    return tree
