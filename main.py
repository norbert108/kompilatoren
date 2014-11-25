__author__ = 'norbert'

from plyplus import Grammar

parser = Grammar(r"""

@start: expression ;

@expression: function_call | cond_expr | loop | control_instr | print | return | arytm_expression | function_def | assign_c | declaration ;


type: 'int' | 'float' | 'string' ;
if: 'if ' ;
else: 'else' ;
while: 'while' ;
repeat: 'repeat' ;
until: 'until' ;
arytm_operator: '\+' | '\*' ;
rel_operator: '<' | '>' | '<=' | '>=' | '==' | '!=' ;
bin_operator: '\|\|' | '\&\&' ;
identifier: '\w+' ;

number: '\d+' ;
value: number | '"\w+"' ;

control_instr: ('break' | 'continue') expression? ;
return: 'return' (value | identifier | function_call | arytm_expression) ';' expression? ;
print: 'print' (value | identifier | function_call | arytm_expression )+ ';' expression? ;

assign: identifier '=' (function_call | value | identifier | arytm_expression ) expression? ;
assign_c: assign ';' ;
code_block: '\{' (expression)* '\}' ;

parameter_list: '\(' variable? (',' variable)* '\)' ;
arguments_list: '\(' (value | arytm_expression | identifier)? (',' (value | arytm_expression | identifier))* '\)' ;
condition: '\(' ( identifier | identifier rel_operator identifier ) (bin_operator ( identifier | identifier rel_operator identifier ) | condition)* '\)' ;

arytm_expression: (((number | identifier | arytm_expression) arytm_operator (number | identifier | arytm_expression)+ ) | '\(' arytm_expression '\)' ) expression? ;
cond_expr: if condition (code_block | expression) (else (code_block | expression) )? expression? ;
loop: (while condition code_block | repeat code_block until condition) expression? ;
function_call: identifier arguments_list expression? ;
function_def: type identifier parameter_list code_block expression?;

variable: type identifier ;

declaration: type (assign | identifier) (',' (assign | identifier))* ';' expression? ;

SPACES: '[ ]+' (%ignore) ;
WS: '[ \t\n]+' (%ignore) (%newline);

""")

result = parser.parse("""
float a = 0, b = 0, c = 0;

int gcd(int m, int n) {

int res = 0;
if (m!=n && a) {
    if (m > n)
        res = gcd(m+n, n);
    else
        res = gcd(n+m, m);
}
else
    res = m;

print res;
return res;
}

while(a >= b ) {
    a = 12*(a+ba);
}
""").pretty()
print result