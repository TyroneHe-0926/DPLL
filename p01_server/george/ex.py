# Copyright 2013-2020 Amirhossein Vakili and Nancy A. Day
# George errors

class TypeCheckingError(Exception):

    def __init__(self, message, linenum = -1):
        self.message = message
        self.linenum = linenum

    def __str__(self):
        return self.message

class MissUseError(Exception):

    def __init__(self, message, linenum = -1):
        self.message = message
        self.linenum = linenum

    def __str__(self):
        return self.message

class SyntaxError(Exception):

    def __init__(self, message, linenum = -1):
        self.message = message
        self.linenum = linenum

    def __str__(self):
        return self.message


    
