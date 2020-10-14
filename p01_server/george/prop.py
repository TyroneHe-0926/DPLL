# Copyright 2013-2020 Amirhossein Vakili and Nancy A. Day
# check PROP

import george.ex as ex
import copy


class Formula:
    str_NOT = '! '
    str_AND = ' & '
    str_OR = r' \| '
    str_IMP = ' => '
    str_IFF = ' <=> '
    str_bottom = 'False'
    str_top = 'True'

    def __init__(self):
        pass


class Bottom(Formula):
    def __init__(self):
        pass

    def __eq__(self, other):
        return isinstance(other, Bottom)

    def __str__(self, pr=0):
        return Formula.str_bottom


class Top(Formula):
    def __init__(self):
        pass

    def __eq__(self, other):
        return isinstance(other, Top)

    def __str__(self, pr=0):
        return Formula.str_top


class Variable(Formula):
    @staticmethod
    def __tc(name):
        if not isinstance(name, str):
            raise ex.TypeCheckingError('Variable: a variable must be a string.')

    def __init__(self, name):
        Variable.__tc(name)
        self.__name = name

    def get_name(self):
        return copy.copy(self.__name)

    def get_l(self):
        return None

    def get_r(self):
        return None

    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        return self.__name == other.get_name()

    def __str__(self, pr=0):
        return self.__name


class Not(Formula):
    @staticmethod
    def __tc(l):
        if not isinstance(l, Formula):
            raise ex.TypeCheckingError('Not: the operand of Not is not a well-formed formula.')

    def __init__(self, l):
        Not.__tc(l)
        self.__l = l

    def get_l(self):
        return copy.copy(self.__l)

    def get_r(self):
        return None

    def __eq__(self, other):
        if not isinstance(other, Not):
            return False
        return self.__l == other.get_l()


    def __str__(self, pr=0):
        s = Formula.str_NOT + self.__l.__str__(9)
        if pr > 9:
            return '(' + s + ')'
        return s


class And(Formula):
    @staticmethod
    def __tc(l, r):
        if not isinstance(l, Formula):
            raise ex.TypeCheckingError('And: the left operand of And is not a well-formed formula.')
        if not isinstance(l, Formula):
            raise ex.TypeCheckingError('And: the right operand of And is not a well-formed formula.')

    def __init__(self, l, r):
        And.__tc(l, r)
        self.__l = l
        self.__r = r

    def get_l(self):
        return copy.copy(self.__l)

    def get_r(self):
        return copy.copy(self.__r)

    def __eq__(self, other):
        if not isinstance(other, And):
            return False
        if self.__l != other.get_l():
            return False
        return self.__r == other.get_r()

    def __str__(self, pr=0):
        s = self.__l.__str__(7) + Formula.str_AND + self.__r.__str__(8)
        if pr > 7:
            return '(' + s + ')'
        return s


class Or(Formula):
    @staticmethod
    def __tc(l, r):
        if not isinstance(l, Formula):
            raise ex.TypeCheckingError('Or: the left operand of Or is not a well-formed formula.')
        if not isinstance(l, Formula):
            raise ex.TypeCheckingError('Or: the right operand of Or is not a well-formed formula.')

    def __init__(self, l, r):
        Or.__tc(l, r)
        self.__l = l
        self.__r = r

    def get_l(self):
        return copy.copy(self.__l)

    def get_r(self):
        return copy.copy(self.__r)

    def __eq__(self, other):
        if not isinstance(other, Or):
            return False
        if self.__l != other.get_l():
            return False
        return self.__r == other.get_r()

    def __str__(self, pr=0):
        s = self.__l.__str__(5) + Formula.str_OR + self.__r.__str__(6)
        if pr > 5:
            return '(' + s + ')'
        return s


class Imp(Formula):
    @staticmethod
    def __tc(l, r):
        if not isinstance(l, Formula):
            raise ex.TypeCheckingError('Imp: the left operand of Imp is not a well-formed formula.')
        if not isinstance(l, Formula):
            raise ex.TypeCheckingError('Imp: the right operand of Imp is not a well-formed formula.')

    def __init__(self, l, r):
        Imp.__tc(l, r)
        self.__l = l
        self.__r = r

    def get_l(self):
        return copy.copy(self.__l)

    def get_r(self):
        return copy.copy(self.__r)

    def __eq__(self, other):
        if not isinstance(other, Imp):
            return False
        if self.__l != other.get_l():
            return False
        return self.__r == other.get_r()

    def __str__(self, pr=0):
        s = self.__l.__str__(4) + Formula.str_IMP + self.__r.__str__(3)
        if pr > 3:
            return '(' + s + ')'
        return s


class Iff(Formula):
    @staticmethod
    def __tc(l, r):
        if not isinstance(l, Formula):
            raise ex.TypeCheckingError('Iff: the left operand of Iff is not a well-formed formula.')
        if not isinstance(r, Formula):
            raise ex.TypeCheckingError('Iff: the right operand of Iff is not a well-formed formula.')

    def __init__(self, l, r):
        Iff.__tc(l, r)
        self.__l = l
        self.__r = r

    def get_l(self):
        return copy.copy(self.__l)

    def get_r(self):
        return copy.copy(self.__r)

    def __eq__(self, other):
        if not isinstance(other, Iff):
            return False
        if self.__l != other.get_l():
            return False
        return self.__r == other.get_r()

    def __str__(self, pr=0):
        s = self.__l.__str__(1) + Formula.str_IFF + self.__r.__str__(2)
        if pr > 1:
            return '(' + s + ')'
        return s


#########
# Lexer #
#########

reserved_words = {'False': 'BOTTOM',
                  'True': 'TOP'}

tokens = ['ID', 'LPAREN', 'RPAREN', 'NOT', 'AND', 'OR', 'IMP', 'IFF'] + list(reserved_words.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NOT = r'!'
t_OR = r'\|\|'
t_AND = r'&'
t_IMP = r'=>'
t_IFF = r'<=>'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved_words.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno = t.lexer.lineno + len(t.value)

t_ignore = ' \r\t'

def t_comment(t):
    r'%[^\n]*\n'
    t.lexer.lineno += 1

def t_error(t):
    raise ex.SyntaxError('illegal character \"{0}\"'.format(t.value[0]), t.lexer.lineno)

import george.ply.lex as lex

lexer = lex.lex()

##########
# Parser #
##########

precedence = [('left', 'IFF'),
              ('right', 'IMP'),
              ('left', 'OR'),
              ('left', 'AND'),
              ('left', 'NOT')]


def p_formula_bottom(p):
    'formula : BOTTOM'
    p[0] = Bottom()


def p_formula_top(p):
    'formula : TOP'
    p[0] = Top()


def p_formula_id(p):
    'formula : ID'
    p[0] = Variable(p[1])


def p_formula_not(p):
    'formula : NOT formula'
    p[0] = Not(p[2])


def p_formula_and(p):
    'formula : formula AND formula'
    p[0] = And(p[1], p[3])


def p_formula_or(p):
    'formula : formula OR formula'
    p[0] = Or(p[1], p[3])


def p_formula_imp(p):
    'formula : formula IMP formula'
    p[0] = Imp(p[1], p[3])


def p_formula_iff(p):
    'formula : formula IFF formula'
    p[0] = Iff(p[1], p[3])


def p_formula_paren(p):
    'formula : LPAREN formula RPAREN'
    p[0] = p[2]


def p_error(p):
    if p is None:
        raise ex.SyntaxError("Unexpected end of input")

    i = 0
    temp = p
    near = ""
    while temp and i < 10:
        near = near + ' ' + str(temp.value)
        temp = yacc.token()
        i += 1
    message = 'Syntax error near: {0}'.format(near)
    raise ex.SyntaxError(message, p.lineno)


import george.ply.yacc as yacc

parser = yacc.yacc(start='formula',errorlog=yacc.NullLogger())


def str_to_formula(s):
    lexer.lineno = 0
    return parser.parse(s, tracking=True)


#####################################
# The main function of this module: #
#####################################

def main(inp):
    import george.grgio as grgio
    import george.frml as frml
    try:
        p = frml.str_to_formula(inp.body)
        if p.is_prop():
            return grgio.Feedback(inp.question, inp.part, True, [], [], ['PROP -> syntax is checked.'])
        else:
            return grgio.Feedback(inp.question, inp.part, False, [], ['this formula is not a\
 propositional logic formula'])
    except ex.SyntaxError as exc:
        return grgio.Feedback(inp.question, inp.part, False, [exc.message], [], [], exc.linenum)

#############################
#############################
### Test cases start here: ##
#############################
#############################


if __name__ == '__main__':

    p = Variable('p')
    F = Bottom()
    
    Tests = [Not(And(p, p)),
             Or(F, F),
             And(Top(), Top()),
             And(Not(p), Not(p)),
             And(And(p, p), p),
             And(p, And(p, p)),
             Imp(p, Imp(p, p)),
             Imp(Imp(p, p), p),
             And(p, Iff(p, p)),
             Iff(Iff(p, p), p),
             Iff(p, Iff(p, p))]

    # Testing 'to_str', 'str_to_formula', '__eq__'

    for test in Tests:
        print(str_to_formula(str(test)) == test)


    data ='''
%123 456

p v !p
    '''
    print(str_to_formula(data).__str__())
