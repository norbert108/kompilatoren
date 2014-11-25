__author__ = 'norbert'

from plyplus import Grammar

parser = Grammar(r"""

@start: expression ;

@expression: function_call | cond_expr | loop | control_instr | print | declaration ;

type: 'int' | 'float' | 'string' ;
if: 'if ' ;
else: 'else' ;
while: 'while' ;
repeat: 'repeat' ;
until: 'until' ;
number: '\d+' ;
rel_operator: '<' | '>' | '<=' | '>=' | '==' | '!=' ;
bin_operator: '\|\|' | '\&\&' ;
identifier: '\w+' ;
value: number | '"\w+"' ;
control_instr: ('return' | 'break' | 'continue') ';' expression? ;
print: 'print' (value | identifier | function_call )+ ';' expression? ;

assign: identifier '=' value | variable '=' value ;
code_block: '\{' (expression)* '\}' ;

parameter_list: '\(' variable? (',' variable)* '\)' ;
arguments_list: '\(' (value)* '\)' ;
condition: '\(' ( identifier | identifier rel_operator identifier ) (bin_operator condition)* '\)' ;

cond_expr: if condition code_block (else condition code_block)? expression? ;
loop: (while condition code_block | repeat code_block until condition) expression? ;
function_call: identifier arguments_list ';' expression? ;
function_def: type identifier parameter_list code_block ;

variable: type identifier ;

declaration: (function_def | (type (identifier | assign) (',' (identifier | assign))* ';')) expression? ;

SPACES: '[ ]+' (%ignore) ;
WS: '[ \t\n]+' (%ignore) (%newline);

""")

result = parser.parse("""int i = 43;
""")
print result