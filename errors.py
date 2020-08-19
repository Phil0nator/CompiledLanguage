cc = {}
class Error:
    def __init__(self, start, end, error, details):
        self.start=start
        self.end=end
        self.error=error
        self.details=details
    def as_string(self):
        result = f'{self.error}:{self.details}\n'
        result += f'File : {cc["FILES"][len(cc["FILES"])-1-self.start.fn]}, line : {self.start.ln+1}'
        return result

def throw(e):
    print(e.as_string())
    exit(1)

class UnexpectedTokenError(Error):
    def __init__(self, start, end, details):
        super().__init__(start,end,"Unexpected Token", details)

class InvalidVariableDeclarator(Error):
    def __init__(self, start, end, details):
        super().__init__(start,end,"Invalid Variable Declaration", details)

class UndefinedVariable(Error):
    def __init__(self, start, end, details):
        super().__init__(start,end,"Unkown Reference to Variable", details)

class InvalidFunctionDeclarator(Error):
    def __init__(self, start, end, details):
            super().__init__(start,end,"Invalid Function Declaration", details)

class InvalidFunctionParameterDeclaration(Error):
    def __init__(self, start, end, details):
            super().__init__(start,end,"Invalid Function Parameter Declaration", details)

class UnkownStatementInitiator(Error):
    def __init__(self, start, end, details):
            super().__init__(start,end,"Unkown Statement Initiator", details)

class EmptyFunction(Error):
    def __init__(self, start, end, details):
            super().__init__(start,end,"Empty Function Declaration", details)

class InvalidVariableAssignment(Error):
    def __init__(self, start, end, details):
            super().__init__(start,end,"Invalid Variable Assignment", details)

class ExpressionOverflow(Error):
    def __init__(self, start, end, details):
            super().__init__(start,end,"Expression too long (Use parenthesis to split up your expression)", details)

class InvalidExpressionComponent(Error):
    def __init__(self, start, end, details):
            super().__init__(start,end,"Invalid Expression Component", details)

class InvalidParameter(Error):
    def __init__(self, start, end, details):
            super().__init__(start,end,"Invalid Parameter", details)

class InvalidFunctionReturnDestination(Error):
    def __init__(self, start, end, details):
            super().__init__(start,end,"Invalid Function Return Destination", details)

class EmptyIncludeStatement(Error):
    def __init__(self, start, end, details):
            super().__init__(start,end,"Empty Include Statement", details)

class InvalidDefineDirective(Error):
    def __init__(self, start, end, details):
            super().__init__(start,end,"Invalid Define Directive", details)

class InvalidASMBlock(Error):
    def __init__(self, start, end, details):
        super().__init__(start,end,"Invalid Assembly Block", details)