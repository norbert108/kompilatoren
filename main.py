__author__ = 'norbert'

from plyplus import Grammar

parser = Grammar(r"""

@start: expression ;

@expression: function_call | cond_expr | declaration ;

type: 'int' | 'float' | 'string' ;
if: 'if ' ;
else: 'else ' ;
rel_operator: '<' | '>' | '<=' | '>=' | '==' ;
bin_operator: '\|\|' | '\&\&' ;
identifier: '\w+' ;
value: '\d+' | '"\w+"' ;

assign: identifier '=' value | variable '=' value ;
code_block: '\{' (expression)* '\}' ;

parameter_list: '\(' variable? (',' variable)* '\)' ;
arguments_list: '\(' (value)* '\)' ;
condition: '\(' ( identifier | identifier rel_operator identifier ) (bin_operator condition)* '\)' ;

cond_expr: if condition code_block (else condition code_block)? expression? ;
function_call: identifier arguments_list ';' expression? ;
function_def: type identifier parameter_list code_block ;


variable: type identifier ;

declaration: (function_def | (type (identifier | assign) (',' (identifier | assign))* ';')) expression? ;

SPACES: '[ ]+' (%ignore) ;
WS: '[ \t\n]+' (%ignore) (%newline);

""")

result = parser.parse("""if(dd > kk) {} else (dD) {}
""")
print result

#

# condition: '\(' ( identifier | identifier relation identifier ) (bin_operator condition)* '\)' ;
# rel_operator: '<' | '>' | '<=' | '>=' | '==' ;
# ('else if' condition code_block)* (else condition code_block)?