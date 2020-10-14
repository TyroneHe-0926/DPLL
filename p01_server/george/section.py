# Copyright 2013-2020 Amirhossein Vakili and Nancy A. Day
# divide george file into sections to be checked 

import george.grgio as grgio
import george.ex as ex

tokens = ['SHARP']

t_SHARP = r'\#[^\#]*'

t_ignore = ' \r\n\t'

def t_error(t):
    raise ex.SyntaxError('illegal character \"{0}\"'.format(t.value[0]), t.lexer.lineno)

import george.ply.lex as lex

lexer = lex.lex()

def my_ignore(c):
    return c in t_ignore

def task(inp):
    if inp[1] =='q' or inp[1] == 'u' or inp[1] == 'a':
        i = 2
    else:
        i = 6
    while i < len(inp) and my_ignore(inp[i]):
        i += 1
    j = i + 1
    while j < len(inp) and (not my_ignore(inp[j])):
        j += 1

    if inp[1] == 'c':
        r = inp[j:]
    else:
        r = ""
    return (inp[i:j], r)

import george.frml as frml

def main(data,dpll_opt):
    # fileLineNum is the line number of the start of the current block
    # minus the lines in "#q" blocks
    fileLineNum = 1


    try:
        # NAD 2016-09-14 handling empty file
        if (len(data) == 0):
            raise ex.SyntaxError('empty file.')
        i = 0
        while data[i] != '#':
            if data[i] == '\n':
                fileLineNum += 1
            i += 1
        #print("fileLineNum: ", fileLineNum)
        #print("")

        lexer.input(data)
        tokens = []
        for tok in lexer:
            tokens = tokens + [tok.value]
        if len(tokens) < 3:
            raise ex.SyntaxError('an input has at least 3 sections.')
        if tokens[0][1] != 'u':
            raise ex.SyntaxError('username must be mentioned first.')
        if tokens[1][1] != 'a':
            raise ex.SyntaxError('after username, assignment number is expected.')
        if tokens[2][1] != 'q':
            raise ex.SyntaxError('after assignment number, a question is expected.')
        uwid = task(tokens[0])[0]
        asn = task(tokens[1])[0]

        # Add to the fileLineNum the lines in the "#u" and "#a" blocks
        fileLineNum += tokens[0].count('\n') + tokens[1].count('\n')
        #print(tokens)
        inps = []   # List of grgio.Input classes to be parsed
        offset = 0  # The cumulative number of lines added by "#q" blocks
        numlines = 0
        for i in range(2, len(tokens)):
            #print(tokens[i])
            if tokens[i][1] == 'q':
                offset += tokens[i].count('\n') # Add number of lines in current "#q" block
                part = 1
                Q = task(tokens[i])[0]
                j = i + 1
                if j >= len(tokens):
                    flag = False
                else:
                    flag = tokens[j][1] == 'c'
                if not flag:
                    inps.append(grgio.Input(uwid, asn, Q, part, 'NONE', '', offset)) # append a "#check NONE" block
                while flag:
                    check, body = task(tokens[j])
                    inps.append(grgio.Input(uwid, asn, Q, part, check, body, offset)) # append a "#check" block
                    part += 1
                    j += 1
                    if j < len(tokens):
                        flag = tokens[j][1] == 'c'
                    else:
                        flag = False

        result = []
        for inp in inps:
            numlines = inp.body.count('\n') # Number of newlines in input body
            if inp.check == 'DPLL':
                import george.DPLL as dpll
                temp = dpll.main(inp,dpll_opt)
                if not temp.linenum == -1:  
                    temp.linenum += fileLineNum + inp.offset
                result.append(temp)
            else:
                result.append(grgio.Feedback(inp.question, inp.part, True, [], [], ['nothing was checked for \'{0}\'.'.format(inp.check)]))
                
             # increment the fileLineNum to point to the start of the next block (minus "#q" blocks)
            fileLineNum += numlines
        return result

    except ex.SyntaxError as exc:
        if not hasattr(exc, "lineno"):
            exc.lineno = 0
        return [grgio.Feedback("structure", 0, False, [exc.message], [], [], exc.lineno)]


