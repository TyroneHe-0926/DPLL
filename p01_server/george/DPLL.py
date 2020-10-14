# Run the DPLL algorithm on george formulas

# use to select random literal
import random
# used to access And, Or, Imp, etc. classes and all the helper functions
from george.frml import *

# you are encouraged to decompose your solution into multiple functions

# Boolean Valuation class
# you may add more methods to this class


class BooleanValuation:

    def __init__(self):
        # dictionary attributes that maps strings to T/F (strings)
        self.__assignment = {}

    # returns the assignment dictionary
    def get_bv(self):
        return self.__assignment

    # creates a new BV like the argument but a copy of it
    def copy_bv(self):
        bv1 = BooleanValuation()
        bv1.__assignment = self.__assignment.copy()
        return bv1

    # these assume that they will be passed a Prop or Not !!
    # assigns 'T' to literal
    def assignLiteralTrue(self, literal):
        if isProp(literal):
            x = literal.get_name()
            self.__assignment[x] = 'T'
        elif isNot(literal):
            x = literal.get_arg().get_name()
            self.__assignment[x] = 'F'

    # assigns 'F' to literal
    def assignLiteralFalse(self, literal):
        if isProp(literal):
            x = literal.get_name()
            self.__assignment[x] = 'F'
        elif isNot(literal):
            x = literal.get_arg().get_name()
            self.__assignment[x] = 'T'

    # remove literal from Boolean Valuation
    def remove(self, literal):
        if isProp(literal):
            x = literal.get_name()
        elif isNot(literal):
            x = literal.get_arg().get_name()
        del self.__assignment[x]

    # returns a string containing all truth assignments sorted alphabetically by proposition
    def __str__(self):
        tmpStr = ""
        keys = list(self.__assignment.keys())
        keys.sort()
        for key in keys:
            tmpStr += "[{0}] = {1}\n".format(key, self.__assignment[key])
        return tmpStr


# Input: a george formula
# Output: True if the formula is in CNF and False otherwise
def checkDuplicate(list):
    if len(list) == len(set(list)):
        return False
    else:
        return True


def CNFCheck(formula):
    # TODO: Implement CNFCheck function
    if(isProp(formula)):
        return True
    elif(isTop(formula)):
        return True
    elif(isBottom(formula)):
        return True
    elif(isOr(formula)):
        temp_or = []
        node_or = Or.get_args(formula)
        flag = False
        for i in node_or:
            if(isProp(i)):
                temp_or.append(Prop.get_name(i))
                if(checkDuplicate(temp_or) == True):
                    return False
                else:
                    flag = True
            if(isNot(i)):
                node_not = Not.get_arg(i)
                if(isProp(node_not)):
                    for k in temp_or:
                        if(k == Prop.get_name(node_not)):
                            return False
        return flag
    elif(isNot(formula)):
        node = Not.get_arg(formula)
        if(isProp(node)):
            return True
        else:
            return False
    elif(isAnd(formula)):
        temp = []
        temp2 = []
        temp3 = []
        children = And.get_args(formula)
        for i in children:
            if(isProp(i)):
                temp.append(Prop.get_name(i))
                temp3.append(Prop.get_name(i))
                if(checkDuplicate(temp3) == True):
                    return False
            elif(isOr(i)):
                node_or = Or.get_args(i)
                for j in node_or:
                    if(isProp(j)):
                        temp.append(Prop.get_name(j))
                        temp2.append(Prop.get_name(j))
                        if(checkDuplicate(temp2) == True):
                            return False
                    if(isNot(j)):
                        node_not = Not.get_arg(j)
                        if(isProp(node_not)):
                            for k in temp:
                                if(k == Prop.get_name(node_not)):
                                    return False
            elif(isNot(i)):
                node_not = Not.get_arg(i)
                if(isProp(node_not) == False):
                    return False
            else:
                return True
            temp2 = []
            temp = []
    else:
        return False

# Input: a george formula
# Output: a pair ("SAT"/"UNSAT"/"NOTINCNF", BV)
# BV is a boolean valuation that is printed when the formula is SAT


def hashInBV(key, BV):
    if(key in BV.__str__()):
        return True
    else:
        return False


def randomChoose(formula):
    temp = []
    children = formula.get_args()
    for child in children:
        child_child = child.get_args()
        for j in child_child:
            temp.append(j)
    return random.choice(temp)


def PLE(formula, BV):
    temp_prop = []
    temp_not = []
    temp_not_prop = []
    children = formula.get_args()
    target = Formula()
    formula_new = Formula()
    #print("Starting PLE")

    for child in children:
        child_child = child.get_args()
        for j in child_child:
            if(isProp(j)):
                temp_prop.append(j)
            elif(isNot(j)):
                temp_not.append(j)

    for i in temp_not:
        temp_not_prop.append(i.get_arg())

    for i in temp_prop:
        if i not in temp_not_prop:
            target = i

    if(type(target) != Prop):
        for i in temp_not:
            j = i.get_arg()
            if j not in temp_prop:
                target = i

    if(type(target) != Prop or type(target) != Not):
        target = randomChoose(formula)

    #print("target chosen in PLE: ", target)

    if(isNot(target)):
        not_target = target.get_arg()
        if(hashInBV(not_target.get_name(), BV) == False):
            BV.assignLiteralFalse(Prop(not_target.get_name()))
    elif(isProp(target)):
        if(hashInBV(target.get_name(), BV) == False):
            BV.assignLiteralTrue(Prop(target.get_name()))
    else:
        return EmptyClause

    for child in children:
        if(child.contains(target)):
            formula = formula.remove(child)
            formula_new = formula

    return formula_new


def check(formula, BV):
    bvHash = BV.get_bv()
    children = formula.get_args()
    temp = []
    temp_res = []
    for child in children:
        if(isProp(child)):
            if(bvHash.__getitem__(child.get_name()) == 'F'):
                return False
        elif(isNot(child)):
            if(bvHash.__getitem__(child.get_arg().get_name()) == 'T'):
                return False
        elif(isOr(child)):
            or_child = child.get_args()
            for child_child in or_child:
                temp.append(child_child)
        for i in temp:
            if(isProp(i)):
                temp_res.append(bvHash.__getitem__(i.get_name()))
            elif(isNot(i)):
                if(bvHash.__getitem__(i.get_arg().get_name()) == 'F'):
                    temp_res.append('T')
                elif(bvHash.__getitem__(i.get_arg().get_name()) == 'T'):
                    temp_res.append('F')
        if('T' not in temp_res):
            return False
        temp = []
        temp_res = []
    return True


def unit_prop(formula, BV):
    children = formula.get_args()
    target = Formula()
    target_not = Formula()
    formula_new = Formula()

    #print("Starting unit_prop")

    if(isProp(formula)):
        if(hashInBV(formula.get_name(), BV) == False):
            BV.assignLiteralTrue(Prop(formula.get_name()))
        return EmptyFormula

    for child in children:
        if(isProp(child)):
            target = child
            if(hashInBV(target.get_name(), BV) == False):
                BV.assignLiteralTrue(Prop(target.get_name()))
            formula_new = formula.remove(target)
            #print("target chosen in unitprop: ", target.get_name())
        if(child.contains(target)):
            formula_new = formula.remove(child)
        if(isNot(child)):
            target_not = child
            not_prop = target_not.get_arg()
            if(hashInBV(not_prop.get_name(), BV) == False):
                BV.assignLiteralFalse(Prop(not_prop.get_name()))
            formula_new = formula.remove(target_not)
            #print("target chosen in unitprop: !", Prop(not_prop.get_name()))
        if(child.contains(target_not)):
            formula_new = formula.remove(child)
    return formula_new


def DPLL_helper(formula, BV):

    BV_ret = BV.copy_bv()
    is_unit_prop = False

    if(formula == EmptyFormula):
        #print("achived empty formula here")
        return BV_ret
    elif(formula == EmptyClause):
        return EmptyClause
    elif(isProp(formula)):
        if(hashInBV(formula.get_name(), BV) == False):
            BV_ret.assignLiteralTrue(Prop(formula.get_name()))
        return BV_ret
    elif(isNot(formula)):
        if(hashInBV(formula.get_arg().get_name(), BV) == False):
            BV_ret.assignLiteralFalse(Prop(formula.get_arg().get_name()))
        return BV_ret

    children = formula.get_args()
    for child in children:
        if(isProp(child) or isNot(child)):
            is_unit_prop = True

    if(is_unit_prop):
        #print("formula entering unit_prop: ", formula)
        formula_new = unit_prop(formula, BV)
        #print("formula after unit_prop: ", formula_new)
    else:
        #print("formula entering PLE: ", formula)
        formula_new = PLE(formula, BV)
        #print("formula after PLE: ", formula_new)
    # print(BV_ret.get_bv())
    return DPLL_helper(formula_new, BV)


def DPLL(formula):
    # TODO: Implement DPLL function
    # Remember to use your CheckCNF() function first
    count = 0

    BV = BooleanValuation()
    if(CNFCheck(formula) == False):
        return ("NOTINCNF", BV)
    if(isTop(formula)):
        return ("SAT", BV)
    if(isBottom(formula)):
        return ("UNSAT", BV)
    if(isProp(formula)):
        if(hashInBV(formula.get_name(), BV) == False):
            BV.assignLiteralTrue(Prop(formula.get_name()))
        return ("SAT", BV)
    if(isNot(formula)):
        if(hashInBV(formula.get_arg().get_name(), BV) == False):
            BV.assignLiteralFalse(Prop(formula.get_arg().get_name()))
        return ("SAT", BV)

    children = formula.get_args()

    if(DPLL_helper(formula, BV) != EmptyClause):
        BV_ret = DPLL_helper(formula, BV)
        for i in children:
            if(isProp(i) and i.get_name() not in BV_ret.__str__()):
                BV_ret.assignLiteralTrue(Prop(i.get_name()))
            elif(isNot(i) and i.get_arg().get_name() not in BV_ret.__str__()):
                BV_ret.assignLiteralFalse(Prop(i.get_arg().get_name()))
            elif(isOr(i)):
                or_child = i.get_args()
                for j in or_child:
                    if(isProp(j) and j.get_name() not in BV_ret.__str__()):
                        BV_ret.assignLiteralTrue(Prop(j.get_name()))
                    elif(isNot(j) and j.get_arg().get_name() not in BV_ret.__str__()):
                        BV_ret.assignLiteralFalse(Prop(j.get_arg().get_name()))
        if(check(formula, BV_ret)):
            return ("SAT", BV_ret)
        elif(check(formula, BV_ret) == False):
            return DPLL_count(formula, count+1)
        else:
            return ("UNSAT", BV)


def DPLL_count(formula, count):
    BV = BooleanValuation()
    children = formula.get_args()

    if(DPLL_helper(formula, BV) != EmptyClause):
        BV_ret = DPLL_helper(formula, BV)
        for i in children:
            if(isProp(i) and i.get_name() not in BV_ret.__str__()):
                BV_ret.assignLiteralTrue(Prop(i.get_name()))
            elif(isNot(i) and i.get_arg().get_name() not in BV_ret.__str__()):
                BV_ret.assignLiteralFalse(Prop(i.get_arg().get_name()))
            elif(isOr(i)):
                or_child = i.get_args()
                for j in or_child:
                    if(isProp(j) and j.get_name() not in BV_ret.__str__()):
                        BV_ret.assignLiteralTrue(Prop(j.get_name()))
                    elif(isNot(j) and j.get_arg().get_name() not in BV_ret.__str__()):
                        BV_ret.assignLiteralFalse(Prop(j.get_arg().get_name()))
        if(check(formula, BV_ret)):
            return ("SAT", BV_ret)
        elif(check(formula, BV_ret) == False and count < 1000):
            return DPLL_count(formula, count+1)
        else:
            return ("UNSAT", BV)
    # Input: a george formula
    # Output: a pair ("SAT"/"UNSAT"/"NOTINCNF", BV)
    # BV is a boolean valuation that is printed when the formula is SAT
    # Includes heuristics/optimizations to the the DPLL algorithm


def DPLL_Optimized(formula):

    # TODO: Implement DPLL function
    # Remember to use your CheckCNF() function first
    count = 500

    BV = BooleanValuation()
    if(CNFCheck(formula) == False):
        return ("NOTINCNF", BV)
    if(isTop(formula)):
        return ("SAT", BV)
    if(isBottom(formula)):
        return ("UNSAT", BV)
    if(isProp(formula)):
        if(hashInBV(formula.get_name(), BV) == False):
            BV.assignLiteralTrue(Prop(formula.get_name()))
        return ("SAT", BV)
    if(isNot(formula)):
        if(hashInBV(formula.get_arg().get_name(), BV) == False):
            BV.assignLiteralFalse(Prop(formula.get_arg().get_name()))
        return ("SAT", BV)

    children = formula.get_args()

    if(DPLL_helper(formula, BV) != EmptyClause):
        BV_ret = DPLL_helper(formula, BV)
        for i in children:
            if(isProp(i) and i.get_name() not in BV_ret.__str__()):
                BV_ret.assignLiteralTrue(Prop(i.get_name()))
            elif(isNot(i) and i.get_arg().get_name() not in BV_ret.__str__()):
                BV_ret.assignLiteralFalse(Prop(i.get_arg().get_name()))
            elif(isOr(i)):
                or_child = i.get_args()
                for j in or_child:
                    if(isProp(j) and j.get_name() not in BV_ret.__str__()):
                        BV_ret.assignLiteralTrue(Prop(j.get_name()))
                    elif(isNot(j) and j.get_arg().get_name() not in BV_ret.__str__()):
                        BV_ret.assignLiteralFalse(Prop(j.get_arg().get_name()))
        if(check(formula, BV_ret)):
            return ("SAT", BV_ret)
        elif(check(formula, BV_ret) == False):
            return DPLL_count(formula, count+1)
        else:
            return ("UNSAT", BV)

#####################################
# The main function of this module  #
# Do not change these lines         #
#####################################


def main(inp, dpll_opt):
    import george.grgio as grgio
    import george.frml as frml

    # NOTE: george will always check if a formula is a valid propositional formula before running DPLL

    # converting string (body of inp) to Formula object
    formula = frml.str_to_formula(inp.body)

    if dpll_opt:
        # running DPLL on formula
        (result, BV) = DPLL(formula)
    else:
        (result, BV) = DPLL_Optimized(formula)

    if result == "SAT":
        tmpStr = "DPLL -> SAT" + '\n' + '\n' + str(BV)
        return grgio.Feedback(inp.question, inp.part, True, [], [], [tmpStr])
    elif result == "UNSAT":
        return grgio.Feedback(inp.question, inp.part, True, [], [], ['DPLL -> UNSAT'])
    elif result == "NOTINCNF":
        return grgio.Feedback(inp.question, inp.part, False, ['DPLL -> NOT IN CNF'], [], [])
