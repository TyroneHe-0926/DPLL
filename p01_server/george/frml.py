# Copyright 2013-2020 Amirhossein Vakili and Nancy A. Day
# Parse george formulas

import copy

from functools import wraps

import george.ply.lex as lex
import george.ply.yacc as yacc

import george.ex as ex
import george.const as const

#Parent class for all propositional logic constructs
class Formula:

    def __init__(self):
        pass

#Bottom is False
class Bottom(Formula):

    def __init__(self):
        pass

    def __eq__(self, other):
        return isinstance(other, Bottom)

    def __str__(self, pr=0):
        return const.str_BOTTOM

    def is_prop(self):
        return True

#Top is True
class Top(Formula):

    def __init__(self):
        pass

    def __eq__(self, other):
        return isinstance(other, Top)

    def __str__(self, pr=0):
        return const.str_TOP

    def is_prop(self):
        return True

# Child class of Formula representing a proposition (example: p, q, r, etc.)
class Prop(Formula):

    @staticmethod
    def __tc(name):
        if not isinstance(name, str):
            raise ex.TypeCheckingError('Prop: a\
 propositional variable must be a string.')

    def __init__(self, name):
        Prop.__tc(name)
        self.__name = name #name of the proposition (example: p, q, r, etc.)

    # returns the name attribute of Prop
    def get_name(self):
        return copy.copy(self.__name)

    def __eq__(self, other):
        if not isinstance(other, Prop):
            return False
        return self.__name == other.get_name()

    def __str__(self, pr=0):
        return self.__name

    def is_prop(self):
        return True

    def contains(self, literal):
        return self == literal


def is_atomic(f):
    if isinstance(f, Bottom):
        return True
    if isinstance(f, Top):
        return True
    if isinstance(f, Prop):
        return True
    return False

# Child class of Formula representing a negation i.e. !
class Not(Formula):

    @staticmethod
    def __tc(l):
        if not isinstance(l, Formula):
            raise ex.TypeCheckingError('Not: the operand of\
 Not is not a well-formed formula.')

    def __init__(self, l):
        Not.__tc(l)
        self.__l = l

    # returns the child node of Not
    def get_arg(self):
        return copy.copy(self.__l)

    # returns the child node of Not
    # same as above function but left in for backward compatibility
    def get_l(self):
        return copy.copy(self.__l)

    def __eq__(self, other):
        if not isinstance(other, Not):
            return False
        return self.__l == other.get_l()

    def __str__(self, pr=0):
        s = const.str_NOT + ' ' + self.__l.__str__(10)
        if pr > 10:
            return '(' + s + ')'
        return s

    def is_prop(self):
        return self.__l.is_prop()

    def contains(self, literal):
        return self == literal

# Child class of Formula representing a conjunction i.e. &
class And(Formula):

    @staticmethod
    def __tc(l):
        if not isinstance(l, list):
            raise ex.TypeCheckingError('And: a list of formulae must be provided.')
        if len(l) < 2:
            raise ex.TypeCheckingError('And: at least 2 operands must be provided.')
        for f in l:
            if not isinstance(f, Formula):
                raise ex.TypeCheckingError('And: an operand of And is not a well-formed formula.')

    # And is allowed to take only one argument
    def __init__(self, l):
        And.__tc(l)
        arg = []
        for p in l:
            if isinstance(p, And):
                arg = arg + p.get_l()
            else:
                arg.append(p)
        self.__l = arg

    # returns all children nodes of And
    def get_args(self):
        return copy.copy(self.__l)

    # same purpose of previous function; left for backward compatibility
    def get_l(self):
        return copy.copy(self.__l)

    def set_args(self, argList):
        self.__l = argList

    # returns conjunct = c from the conjunction
    def remove(self, c):
        new_args = list(filter(lambda x: not(x == c), self.get_args()))
        if len(new_args) > 1:
            return And(new_args)
        elif len(new_args) == 1:
            return new_args[0]
        else:
            return EmptyFormula()

    # replaces conjunct "old" with conjunct "new"
    def replace(self, old, new):
        new_args = [new if item == old else item for item in self.get_args()]
        return And(new_args)

    # checks if two conjunctions are equal
    # usage: conj1 = conj2 where conj1 and conj2 are objects of type And
    def __eq__(self, other):
        if not isinstance(other, And):
            return False
        other_l = other.get_l()
        if len(self.__l) != len(other_l):
            return False
        for f in self.__l:
            if self.__l.count(f) != other_l.count(f):
                return False
        return True

    def __str__(self, pr=0):
        s = self.__l[0].__str__(8)
        for f in self.__l[1:]:
            s = s + ' ' + const.str_AND + ' ' + f.__str__(8)
        if pr > 8:
            return '(' + s + ')'
        return s

    def is_prop(self):
        for f in self.__l:
            if not f.is_prop():
                return False
        return True

# Child class of Formula representing a conjunction i.e. |
class Or(Formula):

    @staticmethod
    def __tc(l):
        if not isinstance(l, list):
            raise ex.TypeCheckingError('Or: a list of formulae must be provided.')
        if len(l) < 2:
            raise ex.TypeCheckingError('Or: at least 2 operands must be provided.')
        for f in l:
            if not isinstance(f, Formula):
                raise ex.TypeCheckingError('Or: an operand of And is not a well-formed formula.')

    # And is allowed to take only one argument
    def __init__(self, l):
        Or.__tc(l)
        arg = []
        for p in l:
            if isinstance(p, Or):
                arg = arg + p.get_args()
            else:
                arg.append(p)
        self.__l = arg

    # returns all children nodes of Or
    def get_args(self):
        return copy.copy(self.__l)

    # same purpose of previous function; left for backward compatibility
    def get_l(self):
        return copy.copy(self.__l)

    def set_args(self, argList):
        self.__l = argList

    # removes literal from the disjunction
    def remove(self, lit):
        args = self.get_args()
        new_args = list(filter(lambda x : not(x == lit), args))
        if len(new_args) > 1:
            return Or(new_args)
        elif len(new_args) == 1:
            return new_args[0]
        else:
            return EmptyClause()

    # checks if two disjunctions are equal
    # usage: dis1 = dis2 where dis1 and dis2 are objects of type Or
    def __eq__(self, other):
        if not isinstance(other, Or):
            return False
        other_l = other.get_args()
        if len(self.__l) != len(other_l):
            return False
        for f in self.__l:
            if self.__l.count(f) != other_l.count(f):
                return False
        return True

    def __str__(self, pr=0):
        s = self.__l[0].__str__(6)
        for f in self.__l[1:]:
            s = s + ' ' + const.str_OR + ' ' + f.__str__(6)
        if pr > 6:
            return '(' + s + ')'
        return s

    def is_prop(self):
        for f in self.__l:
            if not f.is_prop():
                return False
        return True

    def contains(self, literal):
        for f in self.__l:
            if f.contains(literal):
                return True
        return False

# Child class of Formula representing an implication i.e. =>
class Imp(Formula):

    @staticmethod
    def __tc(l, r):
        if not isinstance(l, Formula):
            raise ex.TypeCheckingError('Imp: the left operand of\
 Imp is not a well-formed formula.')
        if not isinstance(l, Formula):
            raise ex.TypeCheckingError('Imp: the right operand of\
 Imp is not a well-formed formula.')

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
        s = self.__l.__str__(5) + ' ' + const.str_IMP + ' ' + self.__r.__str__(4)
        if pr > 4:
            return '(' + s + ')'
        return s

    def is_prop(self):
        if not self.__l.is_prop():
            return False
        return self.__r.is_prop()

# Child class of Formula representing an implication i.e. <=>
class Iff(Formula):

    @staticmethod
    def __tc(l, r):
        if not isinstance(l, Formula):
            raise ex.TypeCheckingError('Iff: the left operand of\
 Iff is not a well-formed formula.')
        if not isinstance(r, Formula):
            raise ex.TypeCheckingError('Iff: the right operand of\
 Iff is not a well-formed formula.')

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
        s = self.__l.__str__(2) + ' ' +  const.str_IFF + ' ' + self.__r.__str__(3)
        if pr > 2:
            return '(' + s + ')'
        return s

    def is_prop(self):
        if not self.__l.is_prop():
            return False
        return self.__r.is_prop()

# Child class of Formula representing an empty formula
class EmptyFormula(Formula):
    def __init__(self):
        pass

    def __eq__(self, other):
        return isinstance(other, EmptyFormula)

    def __str__(self, pr=0):
        return const.str_EMPTY

    def is_prop(self):
        return True

# Child class of Formula representing a formula containing an empty clause
class EmptyClause(Formula):
    def __init__(self):
        pass

    def __eq__(self, other):
        return isinstance(other, EmptyClause)

    def __str__(self, pr=0):
        return const.str_EMPTYCLAUSE

    def is_prop(self):
        return True

    def contains(self,literal):
        return False

# returns True if formula is of type And, False otherwise
def isAnd(formula):
    return isinstance(formula, And)

# returns True if formula is of type Or, False otherwise
def isOr(formula):
    return isinstance(formula, Or)

# returns True if formula is of type Prop, False otherwise
def isProp(formula):
    return isinstance(formula, Prop)

# returns True if formula is of type Not, False otherwise
def isNot(formula):
    return isinstance(formula, Not)

# returns True if formula is of type Iff, False otherwise
def isIff(formula):
    return isinstance(formula, Iff)

# returns True if formula is of type Iff, False otherwise
def isImp(formula):
    return isinstance(formula, Imp)

# returns True if formula is of type Top, False otherwise
def isTop(formula):
    return isinstance(formula, Top)

# returns True if formula is of type Top, False otherwise
def isBottom(formula):
    return isinstance(formula, Bottom)

# returns True if formula is of type EmptyFormula, False otherwise
def isEmptyFormula(formula):
    return isinstance(formula, EmptyFormula)

# returns True if formula is of type EmptyClause, False otherwise
def isEmptyClause(formula):
    return isinstance(formula, EmptyClause)


#########
# Lexer #
#########

reserved_words = {const.str_BOTTOM: 'BOTTOM',
                  const.str_TOP: 'TOP',
                  const.str_FORALL: 'FORALL',
                  const.str_EXISTS : 'EXISTS',
                  'sub' : 'SUB',
                  'sube' : 'SUBE',
                  'in' : 'IN',
                  'union' : 'UNION',
                  'inter' : 'INTERSECTION',
                  'dom' : 'DOMAIN',
                  'ran' : 'RANGE'}

tokens = ['ID',
          'NUMBER',
          'LPAREN',
          'RPAREN',
          'NOT',
          'AND',
          'OR',
          'IMP',
          'IFF',
          'EQ',
          'NOT_EQ',
          'COLON',
          'COMMA',
          'INN',
          'GR',
          'LS',
          'GRE',
          'LSE',
          'STAR',
          'POWER',
          'DIV',
          'ADD',
          'MINUS',
          'BAR',
          'LBRACKET',
          'RBRACKET',
          'PRIME',
          'SEMI',
          'TRANSPOSE',
          'DOMR',
          'RANR',
          'DOMS',
          'RANS',
          'OVER',
          'LIMAGE',
          'RIMAGE',
          'LNCB',
          'RNCB'] +\
                  list(reserved_words.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NOT = r'!'
t_AND = r'&'
t_OR = r'\|'  # r'\|\|'
t_IMP =  r'=>'
t_IFF = r'<=>'
t_EQ = r'=='
t_NOT_EQ = r'!='
t_COLON = r'\.'
t_COMMA = r','
t_INN = r':'
t_GR = r'>'
t_LS = r'<'
t_GRE = r'>='
t_LSE = r'<='
t_STAR = r'\*'
t_POWER = r'\^'
t_DIV = r'/'
t_ADD = r'\+'
t_MINUS = r'\-'
t_BAR = r'\|\|'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_PRIME = r"'"
t_SEMI = r';'
t_TRANSPOSE = r'~'
t_DOMR = r'<\|'
t_RANR = r'\|>'
t_DOMS = r'<\-\|'
t_RANS = r'\|\->'
t_OVER = r'\(\+\)'
t_LIMAGE = r'\(\|'
t_RIMAGE = r'\|\)'
t_LNCB = r'\['
t_RNCB = r'\]'

def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9\']*[!\?]?"
    t.type = reserved_words.get(t.value, 'ID')
    return t


def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

t_ignore = ' \r\t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno = t.lexer.lineno + len(t.value)

def t_comment(t):
    r'%[^\n]*\n?'
    t.lexer.lineno += 1

def t_error(t):
    raise ex.SyntaxError('illegal character \"{0}\"'.format(t.value[0]), t.lexer.lineno)

lexer = lex.lex(optimize = 1, lextab = 'frml_lexer.py')


##########
# Parser #
##########

precedence = [('left', 'FORALL', 'EXISTS'),
              ('left', 'IFF'),
              ('right', 'IMP'),
              ('left', 'OR'),
              ('left', 'AND'),
              ('left', 'NOT'),
              ('right','SUB', 'SUBE'),
              ('left', 'GR', 'LS', 'GRE', 'LSE'),
              ('left', 'IN'),
              ('left', 'INTERSECTION', 'SEMI', 'DOMR', 'RANR', 'DOMS', 'RANS', 'OVER'),
              ('left', 'PRIME', 'TRANSPOSE'),
              ('left', 'POWER'),
              ('left', 'STAR', 'DIV'),
              ('left', 'ADD', 'MINUS')]


def p_formula_bottom(p):
    'formula : BOTTOM'
    p[0] = Bottom()


def p_formula_top(p):
    'formula : TOP'
    p[0] = Top()


def p_formula_id(p):
    'formula : ID'
    p[0] = Prop(p[1])


def p_term_tuple(p):
    'term_tuple : LPAREN term_list RPAREN'
    p[0] = p[2]

def p_term_tuple_seq(p):
    '''term_tuple_seq : term_tuple
                      | term_tuple_seq COMMA term_tuple'''
    if len(p) != 2:
        p[0] = App(FunSym('@cons',2),[p[1],p[3]]) #p[1] + [p[3]]
    else:
        p[0] = p[1]

def p_formula_eq(p):
    'formula : term EQ term'
    p[0] = Eq(p[1], p[3])

def p_formula_not_eq(p):
    'formula : term NOT_EQ term'
    p[0] = Not(Eq(p[1], p[3]))


def p_formula_not(p):
    'formula : NOT formula'
    p[0] = Not(p[2])


def p_formula_and(p):
    'formula : formula AND formula'
    if isinstance(p[1], And):
        if isinstance(p[3], And):
            p[0] = And(p[1].get_l() + p[3].get_l())
        else:
            p[0] = And(p[1].get_l() + [p[3]] )
    else:
        if isinstance(p[3], And):
            p[0] = And([p[1]] + p[3].get_l())
        else:
            p[0] = And([p[1], p[3]])


def p_formula_or(p):
    'formula : formula OR formula'
    if isinstance(p[1], Or):
        if isinstance(p[3], Or):
            p[0] = Or(p[1].get_l() + p[3].get_l())
        else:
            p[0] = Or(p[1].get_l() + [p[3]])
    else:
        if isinstance(p[3], Or):
            p[0] = Or([p[1]] + p[3].get_l())
        else:
            p[0] = Or([p[1], p[3]])


def p_formula_imp(p):
    'formula : formula IMP formula'
    p[0] = Imp(p[1], p[3])

def p_formula_iff(p):
    'formula : formula IFF formula'
    p[0] = Iff(p[1], p[3])

def p_id_list_1(p):
    'id_list : ID'
    p[0] = [p[1]]


def p_id_list_2(p):
    'id_list : id_list COMMA ID'
    p[0] = [p[3]] + p[1]


def p_formula_paren(p):
    'formula : LPAREN formula RPAREN'
    p[0] = p[2]


def p_term_id(p):
    'term : ID'
    p[0] = Var(p[1])

def p_member_seq_1(p):
    'member_seq : COLON id_in_id_seq'
    p[0] = p[2]

def p_member_seq_2(p):
    'member_seq : '
    p[0] = []

def p_id_in_id_seq_1(p):
    'id_in_id_seq : ID INN ID'
    p[0] = [(p[1], p[3])]

def p_id_in_id_seq_2(p):
    'id_in_id_seq : id_in_id_seq COMMA ID INN ID'
    p[0] = p[1] + [(p[3], p[5])]

def p_term_paren(p):
    'term : LPAREN term RPAREN'
    p[0] = p[2]

def p_term_list_1(p):
    'term_list : term'
    p[0] = [p[1]]

def p_term_list_2(p):
    'term_list : term_list COMMA term'
    p[0] = p[1] + [p[3]]

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

# suppress warning messages from conflicts
parser_formula = yacc.yacc(start='formula',errorlog=yacc.NullLogger())

def str_to_formula(s):
    lexer.lineno = 0
    return parser_formula.parse(s, lexer = lexer, tracking=True)



