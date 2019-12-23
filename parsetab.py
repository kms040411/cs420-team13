
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftLESSGREATERleftPLUSMINUSleftMULTIPLYDIVIDECOMMA DIVIDE DOUBLEPLUS ELSE EQ FLOAT FLOAT_VAL FOR GREATER ID IF INT INT_VAL LBRACE LESS LPAREN MINUS MULTIPLY PLUS PRINTF PTR_AMP RBRACE RETURN RPAREN SEMI SQ_LBRACKET SQ_RBRACKET STRING VOID WHILEprogram : function program\n\t\t\t   | functionfunction : type id variable_declaration block\n\t\t\t\t| VOID id variable_declaration blocktype : INT\n\t\t\t| FLOATid : IDvariable_declaration : LPAREN declarations RPARENdeclarations : type id_ptr_or_array COMMA declarations\n\t\t\t\t\t| type id_ptr_or_array\n\t\t\t\t\t| VOIDid_ptr_or_array : id\n\t\t\t\t\t   | id array_decs\n\t\t\t\t\t   | ptrs idarray_decs : SQ_LBRACKET expression SQ_RBRACKET array_decs\n\t\t\t\t  | SQ_LBRACKET expression SQ_RBRACKETptrs : MULTIPLY ptrs\n\t\t    | MULTIPLYblock : LBRACE statements RBRACEstatements : semi_statement\n\t\t\t\t  | non_semi_statement\n\t\t\t      | semi_statement SEMI statements\n\t\t\t      | non_semi_statement statements\n\t\t\t      | emptysemi_statement : var_declaration\n\t\t\t\t\t  | var_assignment\n\t\t\t\t\t  | function_app\n\t\t\t\t\t  | return_expr\n\t\t\t\t\t  | expressionnon_semi_statement : conditional\n\t\t\t\t\t\t  | for\n\t\t\t\t\t\t  | whileconditional : if elif_elseif : IF LPAREN expression RPAREN blockelif_else : ELSE IF LPAREN expression RPAREN block elif_else\n\t\t\t\t | ELSE block\n\t\t\t\t | emptyfor : FOR LPAREN loop_init_or_empty SEMI semi_statement_or_empty SEMI semi_statement_or_empty RPAREN blockloop_init_or_empty : loop_init\n\t\t\t\t\t\t  | expression\n\t\t\t\t\t\t  | emptysemi_statement_or_empty : semi_statement\n\t\t\t\t\t\t       | emptyloop_init : type var_assignment\n\t\t\t\t | semi_statementwhile : WHILE LPAREN expression RPAREN blockvar_declaration : type var_and_assignvar_assignment : id_ptr_or_array EQ expressionvar_and_assign : var_assignment COMMA var_and_assign\n\t\t\t\t\t  | var_assignment\n\t\t\t\t\t  | id_ptr_or_array COMMA var_and_assign\n\t\t\t\t\t  | id_ptr_or_arrayreturn_expr : RETURN expression\n\t\t\t\t   | RETURNfunction_app : PRINTF LPAREN STRING print_formats RPAREN\n\t\t\t\t\t| ID LPAREN arguments RPARENprint_formats : COMMA expression print_formats\n\t\t\t\t\t | emptyarguments : expression COMMA arguments\n\t\t\t\t | expression\n\t\t\t\t | emptyempty :expression : expression PLUS expression\n\t\t\t\t  | expression MINUS expression\n\t\t\t \t  | expression MULTIPLY expression\n\t\t\t  \t  | expression DIVIDE expression\n\t\t\t  \t  | expression LESS expression\n\t\t\t  \t  | expression GREATER expression\n\t\t  \t\t  | LPAREN expression RPAREN\n\t\t  \t\t  | MINUS expression\n\t\t  \t\t  | PTR_AMP expression\n\t\t  \t\t  | MULTIPLY expression\n\t\t  \t\t  | id_ptr_or_array DOUBLEPLUS\n\t\t  \t\t  | DOUBLEPLUS id_ptr_or_array\n\t\t  \t\t  | id_ptr_or_array\n\t\t  \t\t  | function_app\n\t\t  \t\t  | var_assignment\n\t\t\t  \t  | INT_VAL\n\t\t\t  \t  | FLOAT_VAL'
    
_lr_action_items = {'VOID':([0,2,12,14,19,53,88,],[4,4,18,-3,-4,-19,18,]),'INT':([0,2,12,14,15,19,22,29,30,31,44,53,54,79,81,82,88,106,127,140,142,145,146,148,150,],[5,5,5,-3,5,-4,5,-30,-31,-32,-62,-19,5,-33,-37,5,5,-36,5,-46,-34,5,-62,-35,-38,]),'FLOAT':([0,2,12,14,15,19,22,29,30,31,44,53,54,79,81,82,88,106,127,140,142,145,146,148,150,],[6,6,6,-3,6,-4,6,-30,-31,-32,-62,-19,6,-33,-37,6,6,-36,6,-46,-34,6,-62,-35,-38,]),'$end':([1,2,7,14,19,53,],[0,-2,-1,-3,-4,-19,]),'ID':([3,4,5,6,15,17,22,29,30,31,32,35,37,38,39,40,41,44,48,52,53,54,56,57,58,59,60,61,65,72,76,79,81,82,83,85,87,89,97,98,106,111,122,125,126,127,140,142,145,146,148,150,],[9,9,-5,-6,36,9,36,-30,-31,-32,9,36,36,36,-18,36,9,-62,9,-18,-19,36,36,36,36,36,36,36,36,36,-17,-33,-37,36,36,36,36,-17,9,9,-36,9,36,36,36,36,-46,-34,36,-62,-35,-38,]),'MULTIPLY':([5,6,9,15,17,22,25,26,28,29,30,31,32,33,35,36,37,38,39,40,41,42,43,44,47,52,53,54,56,57,58,59,60,61,65,66,68,69,70,71,72,73,74,75,77,78,79,81,82,83,84,85,86,87,91,92,93,94,95,96,97,98,99,101,103,106,109,111,112,114,115,116,117,122,124,125,126,127,131,133,134,136,140,141,142,145,146,148,150,],[-5,-6,-7,39,52,39,-77,-76,58,-30,-31,-32,52,-75,39,-7,39,39,39,39,52,-78,-79,-62,-12,52,-19,39,39,39,39,39,39,39,39,-73,58,-75,-76,-77,39,58,58,-72,58,-74,-33,-37,39,39,-13,39,-14,39,58,58,-65,-66,58,58,52,52,58,-69,58,-36,58,52,-77,-76,58,58,58,39,-56,39,39,39,-16,-55,58,58,-46,-15,-34,39,-62,-35,-38,]),'LPAREN':([8,9,10,15,22,29,30,31,34,35,36,37,38,39,40,44,45,46,49,53,54,56,57,58,59,60,61,65,72,79,81,82,83,85,87,105,106,122,125,126,127,140,142,145,146,148,150,],[12,-7,12,35,35,-30,-31,-32,67,35,72,35,35,35,35,-62,82,83,87,-19,35,35,35,35,35,35,35,35,35,-33,-37,35,35,35,35,126,-36,35,35,35,35,-46,-34,35,-62,-35,-38,]),'SQ_LBRACKET':([9,36,47,131,],[-7,-7,85,85,]),'COMMA':([9,36,42,43,47,51,63,64,66,69,70,71,74,75,77,78,84,86,91,92,93,94,95,96,99,100,101,103,124,128,129,131,133,134,141,],[-7,-7,-78,-79,-12,88,97,98,-73,-75,-76,-77,-70,-72,-71,-74,-13,-14,-63,-64,-65,-66,-67,-68,-48,122,-69,125,-56,97,98,-16,-55,122,-15,]),'RPAREN':([9,16,18,24,25,26,27,28,33,36,37,42,43,47,51,62,63,64,66,68,69,70,71,72,73,74,75,77,78,84,86,91,92,93,94,95,96,99,100,101,102,103,104,115,117,118,119,120,121,123,124,125,131,133,134,135,136,138,139,141,143,145,147,],[-7,50,-11,-25,-26,-27,-28,-29,-75,-7,-54,-78,-79,-12,-10,-47,-50,-52,-73,101,-75,-76,-77,-62,-53,-70,-72,-71,-74,-13,-14,-63,-64,-65,-66,-67,-68,-48,-62,-69,124,-60,-61,130,132,-9,-49,-51,133,-58,-56,-62,-16,-55,-62,-59,144,-42,-43,-15,-57,-62,149,]),'EQ':([9,33,36,47,64,69,84,86,129,131,141,],[-7,65,-7,-12,65,65,-13,-14,65,-16,-15,]),'SEMI':([9,21,24,25,26,27,28,33,36,37,42,43,47,62,63,64,66,69,70,71,73,74,75,77,78,82,84,86,91,92,93,94,95,96,99,101,107,108,109,110,112,113,114,119,120,124,127,128,129,131,133,137,138,139,141,],[-7,54,-25,-26,-27,-28,-29,-75,-7,-54,-78,-79,-12,-47,-50,-52,-73,-75,-76,-77,-53,-70,-72,-71,-74,-62,-13,-14,-63,-64,-65,-66,-67,-68,-48,-69,127,-39,-29,-41,-26,-45,-27,-49,-51,-56,-62,-44,-52,-16,-55,145,-42,-43,-15,]),'RBRACE':([9,15,20,21,22,23,24,25,26,27,28,29,30,31,33,36,37,42,43,44,47,53,54,55,62,63,64,66,69,70,71,73,74,75,77,78,79,81,84,86,90,91,92,93,94,95,96,99,101,106,119,120,124,131,133,140,141,142,146,148,150,],[-7,-62,53,-20,-21,-24,-25,-26,-27,-28,-29,-30,-31,-32,-75,-7,-54,-78,-79,-62,-12,-19,-62,-23,-47,-50,-52,-73,-75,-76,-77,-53,-70,-72,-71,-74,-33,-37,-13,-14,-22,-63,-64,-65,-66,-67,-68,-48,-69,-36,-49,-51,-56,-16,-55,-46,-15,-34,-62,-35,-38,]),'PLUS':([9,25,26,28,33,36,42,43,47,66,68,69,70,71,73,74,75,77,78,84,86,91,92,93,94,95,96,99,101,103,109,112,114,115,116,117,124,131,133,134,136,141,],[-7,-77,-76,56,-75,-7,-78,-79,-12,-73,56,-75,-76,-77,56,-70,-72,56,-74,-13,-14,-63,-64,-65,-66,56,56,56,-69,56,56,-77,-76,56,56,56,-56,-16,-55,56,56,-15,]),'MINUS':([9,15,22,25,26,28,29,30,31,33,35,36,37,38,39,40,42,43,44,47,53,54,56,57,58,59,60,61,65,66,68,69,70,71,72,73,74,75,77,78,79,81,82,83,84,85,86,87,91,92,93,94,95,96,99,101,103,106,109,112,114,115,116,117,122,124,125,126,127,131,133,134,136,140,141,142,145,146,148,150,],[-7,38,38,-77,-76,57,-30,-31,-32,-75,38,-7,38,38,38,38,-78,-79,-62,-12,-19,38,38,38,38,38,38,38,38,-73,57,-75,-76,-77,38,57,-70,-72,57,-74,-33,-37,38,38,-13,38,-14,38,-63,-64,-65,-66,57,57,57,-69,57,-36,57,-77,-76,57,57,57,38,-56,38,38,38,-16,-55,57,57,-46,-15,-34,38,-62,-35,-38,]),'DIVIDE':([9,25,26,28,33,36,42,43,47,66,68,69,70,71,73,74,75,77,78,84,86,91,92,93,94,95,96,99,101,103,109,112,114,115,116,117,124,131,133,134,136,141,],[-7,-77,-76,59,-75,-7,-78,-79,-12,-73,59,-75,-76,-77,59,59,-72,59,-74,-13,-14,59,59,-65,-66,59,59,59,-69,59,59,-77,-76,59,59,59,-56,-16,-55,59,59,-15,]),'LESS':([9,25,26,28,33,36,42,43,47,66,68,69,70,71,73,74,75,77,78,84,86,91,92,93,94,95,96,99,101,103,109,112,114,115,116,117,124,131,133,134,136,141,],[-7,-77,-76,60,-75,-7,-78,-79,-12,-73,60,-75,-76,-77,60,-70,-72,60,-74,-13,-14,-63,-64,-65,-66,-67,-68,60,-69,60,60,-77,-76,60,60,60,-56,-16,-55,60,60,-15,]),'GREATER':([9,25,26,28,33,36,42,43,47,66,68,69,70,71,73,74,75,77,78,84,86,91,92,93,94,95,96,99,101,103,109,112,114,115,116,117,124,131,133,134,136,141,],[-7,-77,-76,61,-75,-7,-78,-79,-12,-73,61,-75,-76,-77,61,-70,-72,61,-74,-13,-14,-63,-64,-65,-66,-67,-68,61,-69,61,61,-77,-76,61,61,61,-56,-16,-55,61,61,-15,]),'SQ_RBRACKET':([9,36,42,43,47,66,69,70,71,74,75,77,78,84,86,91,92,93,94,95,96,99,101,116,124,131,133,141,],[-7,-7,-78,-79,-12,-73,-75,-76,-77,-70,-72,-71,-74,-13,-14,-63,-64,-65,-66,-67,-68,-48,-69,131,-56,-16,-55,-15,]),'DOUBLEPLUS':([9,15,22,29,30,31,33,35,36,37,38,39,40,44,47,53,54,56,57,58,59,60,61,65,69,72,79,81,82,83,84,85,86,87,106,122,125,126,127,131,140,141,142,145,146,148,150,],[-7,41,41,-30,-31,-32,66,41,-7,41,41,41,41,-62,-12,-19,41,41,41,41,41,41,41,41,66,41,-33,-37,41,41,-13,41,-14,41,-36,41,41,41,41,-16,-46,-15,-34,41,-62,-35,-38,]),'LBRACE':([11,13,50,80,130,132,144,149,],[15,15,-8,15,15,15,15,15,]),'PRINTF':([15,22,29,30,31,35,37,38,39,40,44,53,54,56,57,58,59,60,61,65,72,79,81,82,83,85,87,106,122,125,126,127,140,142,145,146,148,150,],[34,34,-30,-31,-32,34,34,34,34,34,-62,-19,34,34,34,34,34,34,34,34,34,-33,-37,34,34,34,34,-36,34,34,34,34,-46,-34,34,-62,-35,-38,]),'RETURN':([15,22,29,30,31,44,53,54,79,81,82,106,127,140,142,145,146,148,150,],[37,37,-30,-31,-32,-62,-19,37,-33,-37,37,-36,37,-46,-34,37,-62,-35,-38,]),'PTR_AMP':([15,22,29,30,31,35,37,38,39,40,44,53,54,56,57,58,59,60,61,65,72,79,81,82,83,85,87,106,122,125,126,127,140,142,145,146,148,150,],[40,40,-30,-31,-32,40,40,40,40,40,-62,-19,40,40,40,40,40,40,40,40,40,-33,-37,40,40,40,40,-36,40,40,40,40,-46,-34,40,-62,-35,-38,]),'INT_VAL':([15,22,29,30,31,35,37,38,39,40,44,53,54,56,57,58,59,60,61,65,72,79,81,82,83,85,87,106,122,125,126,127,140,142,145,146,148,150,],[42,42,-30,-31,-32,42,42,42,42,42,-62,-19,42,42,42,42,42,42,42,42,42,-33,-37,42,42,42,42,-36,42,42,42,42,-46,-34,42,-62,-35,-38,]),'FLOAT_VAL':([15,22,29,30,31,35,37,38,39,40,44,53,54,56,57,58,59,60,61,65,72,79,81,82,83,85,87,106,122,125,126,127,140,142,145,146,148,150,],[43,43,-30,-31,-32,43,43,43,43,43,-62,-19,43,43,43,43,43,43,43,43,43,-33,-37,43,43,43,43,-36,43,43,43,43,-46,-34,43,-62,-35,-38,]),'FOR':([15,22,29,30,31,44,53,54,79,81,106,140,142,146,148,150,],[45,45,-30,-31,-32,-62,-19,45,-33,-37,-36,-46,-34,-62,-35,-38,]),'WHILE':([15,22,29,30,31,44,53,54,79,81,106,140,142,146,148,150,],[46,46,-30,-31,-32,-62,-19,46,-33,-37,-36,-46,-34,-62,-35,-38,]),'IF':([15,22,29,30,31,44,53,54,79,80,81,106,140,142,146,148,150,],[49,49,-30,-31,-32,-62,-19,49,-33,105,-37,-36,-46,-34,-62,-35,-38,]),'ELSE':([44,53,142,146,],[80,-19,-34,80,]),'STRING':([67,],[100,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,2,],[1,7,]),'function':([0,2,],[2,2,]),'type':([0,2,12,15,22,54,82,88,127,145,],[3,3,17,32,32,32,111,17,32,32,]),'id':([3,4,15,17,22,32,35,37,38,39,40,41,48,54,56,57,58,59,60,61,65,72,76,82,83,85,87,97,98,111,122,125,126,127,145,],[8,10,47,47,47,47,47,47,47,47,47,47,86,47,47,47,47,47,47,47,47,47,86,47,47,47,47,47,47,47,47,47,47,47,47,]),'variable_declaration':([8,10,],[11,13,]),'block':([11,13,80,130,132,144,149,],[14,19,106,140,142,146,150,]),'declarations':([12,88,],[16,118,]),'statements':([15,22,54,],[20,55,90,]),'semi_statement':([15,22,54,82,127,145,],[21,21,21,113,138,138,]),'non_semi_statement':([15,22,54,],[22,22,22,]),'empty':([15,22,44,54,72,82,100,125,127,134,145,146,],[23,23,81,23,104,110,123,104,139,123,139,81,]),'var_declaration':([15,22,54,82,127,145,],[24,24,24,24,24,24,]),'var_assignment':([15,22,32,35,37,38,39,40,54,56,57,58,59,60,61,65,72,82,83,85,87,97,98,111,122,125,126,127,145,],[25,25,63,71,71,71,71,71,25,71,71,71,71,71,71,71,71,112,71,71,71,63,63,128,71,71,71,25,25,]),'function_app':([15,22,35,37,38,39,40,54,56,57,58,59,60,61,65,72,82,83,85,87,122,125,126,127,145,],[26,26,70,70,70,70,70,26,70,70,70,70,70,70,70,70,114,70,70,70,70,70,70,26,26,]),'return_expr':([15,22,54,82,127,145,],[27,27,27,27,27,27,]),'expression':([15,22,35,37,38,39,40,54,56,57,58,59,60,61,65,72,82,83,85,87,122,125,126,127,145,],[28,28,68,73,74,75,77,28,91,92,93,94,95,96,99,103,109,115,116,117,134,103,136,28,28,]),'conditional':([15,22,54,],[29,29,29,]),'for':([15,22,54,],[30,30,30,]),'while':([15,22,54,],[31,31,31,]),'id_ptr_or_array':([15,17,22,32,35,37,38,39,40,41,54,56,57,58,59,60,61,65,72,82,83,85,87,97,98,111,122,125,126,127,145,],[33,51,33,64,69,69,69,69,69,78,33,69,69,69,69,69,69,69,69,69,69,69,69,64,64,129,69,69,69,33,33,]),'if':([15,22,54,],[44,44,44,]),'ptrs':([15,17,22,32,35,37,38,39,40,41,52,54,56,57,58,59,60,61,65,72,82,83,85,87,97,98,111,122,125,126,127,145,],[48,48,48,48,48,48,48,76,48,48,89,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,]),'var_and_assign':([32,97,98,111,],[62,119,120,62,]),'elif_else':([44,146,],[79,148,]),'array_decs':([47,131,],[84,141,]),'arguments':([72,125,],[102,135,]),'loop_init_or_empty':([82,],[107,]),'loop_init':([82,],[108,]),'print_formats':([100,134,],[121,143,]),'semi_statement_or_empty':([127,145,],[137,147,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> function program','program',2,'p_program','lex_yacc.py',237),
  ('program -> function','program',1,'p_program','lex_yacc.py',238),
  ('function -> type id variable_declaration block','function',4,'p_function','lex_yacc.py',251),
  ('function -> VOID id variable_declaration block','function',4,'p_function','lex_yacc.py',252),
  ('type -> INT','type',1,'p_type','lex_yacc.py',265),
  ('type -> FLOAT','type',1,'p_type','lex_yacc.py',266),
  ('id -> ID','id',1,'p_id','lex_yacc.py',276),
  ('variable_declaration -> LPAREN declarations RPAREN','variable_declaration',3,'p_varaible_declaration','lex_yacc.py',286),
  ('declarations -> type id_ptr_or_array COMMA declarations','declarations',4,'p_declarations','lex_yacc.py',296),
  ('declarations -> type id_ptr_or_array','declarations',2,'p_declarations','lex_yacc.py',297),
  ('declarations -> VOID','declarations',1,'p_declarations','lex_yacc.py',298),
  ('id_ptr_or_array -> id','id_ptr_or_array',1,'p_id_ptr_or_array','lex_yacc.py',323),
  ('id_ptr_or_array -> id array_decs','id_ptr_or_array',2,'p_id_ptr_or_array','lex_yacc.py',324),
  ('id_ptr_or_array -> ptrs id','id_ptr_or_array',2,'p_id_ptr_or_array','lex_yacc.py',325),
  ('array_decs -> SQ_LBRACKET expression SQ_RBRACKET array_decs','array_decs',4,'p_array_decs','lex_yacc.py',338),
  ('array_decs -> SQ_LBRACKET expression SQ_RBRACKET','array_decs',3,'p_array_decs','lex_yacc.py',339),
  ('ptrs -> MULTIPLY ptrs','ptrs',2,'p_ptrs','lex_yacc.py',349),
  ('ptrs -> MULTIPLY','ptrs',1,'p_ptrs','lex_yacc.py',350),
  ('block -> LBRACE statements RBRACE','block',3,'p_block','lex_yacc.py',360),
  ('statements -> semi_statement','statements',1,'p_statements','lex_yacc.py',370),
  ('statements -> non_semi_statement','statements',1,'p_statements','lex_yacc.py',371),
  ('statements -> semi_statement SEMI statements','statements',3,'p_statements','lex_yacc.py',372),
  ('statements -> non_semi_statement statements','statements',2,'p_statements','lex_yacc.py',373),
  ('statements -> empty','statements',1,'p_statements','lex_yacc.py',374),
  ('semi_statement -> var_declaration','semi_statement',1,'p_semi_statement','lex_yacc.py',398),
  ('semi_statement -> var_assignment','semi_statement',1,'p_semi_statement','lex_yacc.py',399),
  ('semi_statement -> function_app','semi_statement',1,'p_semi_statement','lex_yacc.py',400),
  ('semi_statement -> return_expr','semi_statement',1,'p_semi_statement','lex_yacc.py',401),
  ('semi_statement -> expression','semi_statement',1,'p_semi_statement','lex_yacc.py',402),
  ('non_semi_statement -> conditional','non_semi_statement',1,'p_non_semi_statement','lex_yacc.py',412),
  ('non_semi_statement -> for','non_semi_statement',1,'p_non_semi_statement','lex_yacc.py',413),
  ('non_semi_statement -> while','non_semi_statement',1,'p_non_semi_statement','lex_yacc.py',414),
  ('conditional -> if elif_else','conditional',2,'p_conditional','lex_yacc.py',425),
  ('if -> IF LPAREN expression RPAREN block','if',5,'p_if','lex_yacc.py',437),
  ('elif_else -> ELSE IF LPAREN expression RPAREN block elif_else','elif_else',7,'p_elif_else','lex_yacc.py',446),
  ('elif_else -> ELSE block','elif_else',2,'p_elif_else','lex_yacc.py',447),
  ('elif_else -> empty','elif_else',1,'p_elif_else','lex_yacc.py',448),
  ('for -> FOR LPAREN loop_init_or_empty SEMI semi_statement_or_empty SEMI semi_statement_or_empty RPAREN block','for',9,'p_for','lex_yacc.py',466),
  ('loop_init_or_empty -> loop_init','loop_init_or_empty',1,'p_loop_init_or_empty','lex_yacc.py',476),
  ('loop_init_or_empty -> expression','loop_init_or_empty',1,'p_loop_init_or_empty','lex_yacc.py',477),
  ('loop_init_or_empty -> empty','loop_init_or_empty',1,'p_loop_init_or_empty','lex_yacc.py',478),
  ('semi_statement_or_empty -> semi_statement','semi_statement_or_empty',1,'p_semi_statement_or_empty','lex_yacc.py',488),
  ('semi_statement_or_empty -> empty','semi_statement_or_empty',1,'p_semi_statement_or_empty','lex_yacc.py',489),
  ('loop_init -> type var_assignment','loop_init',2,'p_loop_init','lex_yacc.py',499),
  ('loop_init -> semi_statement','loop_init',1,'p_loop_init','lex_yacc.py',500),
  ('while -> WHILE LPAREN expression RPAREN block','while',5,'p_while','lex_yacc.py',513),
  ('var_declaration -> type var_and_assign','var_declaration',2,'p_var_declaration','lex_yacc.py',523),
  ('var_assignment -> id_ptr_or_array EQ expression','var_assignment',3,'p_var_assignment','lex_yacc.py',563),
  ('var_and_assign -> var_assignment COMMA var_and_assign','var_and_assign',3,'p_var_and_assign','lex_yacc.py',573),
  ('var_and_assign -> var_assignment','var_and_assign',1,'p_var_and_assign','lex_yacc.py',574),
  ('var_and_assign -> id_ptr_or_array COMMA var_and_assign','var_and_assign',3,'p_var_and_assign','lex_yacc.py',575),
  ('var_and_assign -> id_ptr_or_array','var_and_assign',1,'p_var_and_assign','lex_yacc.py',576),
  ('return_expr -> RETURN expression','return_expr',2,'p_return_expr','lex_yacc.py',589),
  ('return_expr -> RETURN','return_expr',1,'p_return_expr','lex_yacc.py',590),
  ('function_app -> PRINTF LPAREN STRING print_formats RPAREN','function_app',5,'p_function_app','lex_yacc.py',597),
  ('function_app -> ID LPAREN arguments RPAREN','function_app',4,'p_function_app','lex_yacc.py',598),
  ('print_formats -> COMMA expression print_formats','print_formats',3,'p_print_formats','lex_yacc.py',617),
  ('print_formats -> empty','print_formats',1,'p_print_formats','lex_yacc.py',618),
  ('arguments -> expression COMMA arguments','arguments',3,'p_arguments','lex_yacc.py',634),
  ('arguments -> expression','arguments',1,'p_arguments','lex_yacc.py',635),
  ('arguments -> empty','arguments',1,'p_arguments','lex_yacc.py',636),
  ('empty -> <empty>','empty',0,'p_empty','lex_yacc.py',652),
  ('expression -> expression PLUS expression','expression',3,'p_expression','lex_yacc.py',662),
  ('expression -> expression MINUS expression','expression',3,'p_expression','lex_yacc.py',663),
  ('expression -> expression MULTIPLY expression','expression',3,'p_expression','lex_yacc.py',664),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression','lex_yacc.py',665),
  ('expression -> expression LESS expression','expression',3,'p_expression','lex_yacc.py',666),
  ('expression -> expression GREATER expression','expression',3,'p_expression','lex_yacc.py',667),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression','lex_yacc.py',668),
  ('expression -> MINUS expression','expression',2,'p_expression','lex_yacc.py',669),
  ('expression -> PTR_AMP expression','expression',2,'p_expression','lex_yacc.py',670),
  ('expression -> MULTIPLY expression','expression',2,'p_expression','lex_yacc.py',671),
  ('expression -> id_ptr_or_array DOUBLEPLUS','expression',2,'p_expression','lex_yacc.py',672),
  ('expression -> DOUBLEPLUS id_ptr_or_array','expression',2,'p_expression','lex_yacc.py',673),
  ('expression -> id_ptr_or_array','expression',1,'p_expression','lex_yacc.py',674),
  ('expression -> function_app','expression',1,'p_expression','lex_yacc.py',675),
  ('expression -> var_assignment','expression',1,'p_expression','lex_yacc.py',676),
  ('expression -> INT_VAL','expression',1,'p_expression','lex_yacc.py',677),
  ('expression -> FLOAT_VAL','expression',1,'p_expression','lex_yacc.py',678),
]
