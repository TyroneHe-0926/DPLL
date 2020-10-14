# Copyright 2013-2020 Amirhossein Vakili and Nancy A. Day
# George i/o for sections

class Input:

    def __init__(self, uwid, asn, question, part, check, body, offset = -1):
        self.uwid = uwid
        self.asn = asn
        self.question = question
        self.part = part
        self.check = check
        self.body = body
        self.offset = offset    # The offset (lines) created by "#q" blocks that preceed this input

    def __str__(self):
        result = "+-+-+-+-+-+-+-+ Version 1.4 \n\n#q {0} check {1} in\n\n".format(self.question,self.check)
        result = result + self.body
        return result

class Feedback:

    def __init__(self, question, part, p_or_f, error, warning, comment = [], linenum = -1):
        self.question = question
        self.part = part
        self.p_or_f = p_or_f
        self.warning = warning
        self.error = error
        self.comment = comment
        self.linenum = linenum  # Line number where the feedback applies

    def __str__(self):
        if self.question == "structure":
            return "BAD STRUCTURE: please refer to George's user manual."
        result = "+-+-+-+-+-+-+-+ Version 1.4 \n\n#q {0}, part {1}\n\n".format(self.question, str(self.part))

        if self.p_or_f:
            result = result + "+ Pass\n\n"
            for w in self.warning:
                result = result + "-- Warning: " + w + "\n"
            for c in self.comment:
                result = result + "++ Comment: " + c + "\n"
            return result

        if self.error == [] and self.warning != []:
            result = result + "+ Almost Pass\n\n"
        else:
            result = result + "- Failed\n\n"
        for e in self.error:
            if self.linenum > 0:
                result = result + "-- Error on or about line (" + str(self.linenum) + "): " + e +"\n"
            else:
                result = result + "-- Error: " + e +"\n"
        for w in self.warning:
            result = result + "-- Warning: " + w +"\n"
        result = result + "\n"
        return result
