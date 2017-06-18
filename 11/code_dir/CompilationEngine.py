from SymbolTable import SymbolTable

class CompilationEngine(object):
    
    class TokensDecorator(object):

        def __init__(self, tokenizer):
            self.stack = []
            self.tokens = tokenizer

        def hasMoreTokens(self):
            return self.stack or self.tokens.hasMoreTokens()

        def advance(self):
            if self.stack:
                self.stack.pop()
            else:
                self.tokens.advance()

        def tokenType(self):
            if self.stack:
                return self.stack[-1](0)
            return self.tokens.tokenType()

        def getToken(self):
            if self.stack:
                return self.stack[-1](1)
            return str(self.tokens.getToken())

        def putBack(self, tp):
            self.stack.append(tp)

    
    vmArithmetics = {
        '+': 'add',
        '-': 'sub',
        '=': 'eq',
        '>': 'gt',
        '<': 'lt',
        '&': 'and',
        '|': 'or'
    }
        
    osArithmetics = {
        '*': 'Math.multiply',
        '/': 'Math.divide'
    }


    def __init__(self, tokenizer, writer):
        self.tokens = CompilationEngine.TokensDecorator(tokenizer)
        self.symbols = SymbolTable()
        self.vmWriter = writer
        self.ifCounter = 0

    def CompileClass(self):
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # class
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # classname
        self.className = self.tokens.getToken()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # {
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # ->
        while (True):
            if self.tokens.getToken() not in ['static', 'field']:
                break
            self.CompileClassVarDec()
        while (True):
            if self.tokens.tokenType() != 'keyword':
                break
            self.CompileSubroutineDec()

    def CompileClassVarDec(self):
        kind = self.tokens.getToken()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # type
        type = self.tokens.getToken()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # varname
        varname = self.tokens.getToken()
        self.symbols.define(varname, type, kind)
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # , or ;
        while (self.tokens.getToken() == ','):
            assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # varname
            varname = self.tokens.getToken()
            self.symbols.define(varname, type, kind)
            assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # , or ;
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();

    def CompileSubroutineDec(self):
        self.symbols.startSubroutine()
        token = self.tokens.getToken()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # rettype
        self.retType = self.tokens.getToken()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # routinename
        self.routineName = self.tokens.getToken()
        if token == 'method':
            self.symbols.define('dummy', 'dummy', 'arg')
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # (
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # first arg or )
        self.compileParameterList()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.compileSubroutineBody(token)

    def compileSubroutineBody(self, token):
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # var of statement start
        self.numLocals = 0
        while self.tokens.getToken() == 'var':
            self.compileVarDec()
        self.vmWriter.writeFunction(self.className + '.' + self.routineName, self.numLocals)

        if token == 'constructor':
            numFieldVars = self.symbols.numVars('field')
            self.vmWriter.writePush('constant', numFieldVars)
            self.vmWriter.writeCall('Memory.alloc', '1')
            self.vmWriter.writePop('pointer', '0')
        elif token == 'method':
            self.vmWriter.writePush('argument', '0')
            self.vmWriter.writePop('pointer', '0')
        elif token == 'function':
            pass
        else:
            raise Exception('Unkown type of routine {0}'.format(token))

        self.compileStatements()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();

    def compileParameterList(self):
        varKind = 'arg'
        if self.tokens.tokenType() != 'symbol':
            varType = self.tokens.getToken()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # arg name
            varName = self.tokens.getToken() 
            self.symbols.define(varName, varType, varKind)
            assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # , or )
            while self.tokens.getToken() == ',':
                assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # vartype
                varType = self.tokens.getToken()
                assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # varname
                varName = self.tokens.getToken() 
                self.symbols.define(varName, varType, varKind)
                assert(self.tokens.hasMoreTokens()); self.tokens.advance();

    def compileVarDec(self):
        self.numLocals += 1
        varKind = 'var'
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # vartype
        varType = self.tokens.getToken()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # varname
        varName = self.tokens.getToken()
        self.symbols.define(varName, varType, varKind)
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # , or ;
        while self.tokens.getToken() == ',':
            self.numLocals += 1
            assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # varname
            varName = self.tokens.getToken()
            self.symbols.define(varName, varType, varKind)
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();

    def compileStatements(self):
        while True:
            if self.tokens.getToken() == 'let':
                self.compileLet()
            elif self.tokens.getToken() == 'do':
                self.compileDo()
            elif self.tokens.getToken() == 'while':
                self.compileWhile()
            elif self.tokens.getToken() == 'return':
                self.compileReturn()
            elif self.tokens.getToken() == 'if':
                self.compileIf()
            else:
                break

    def compileDo(self):
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        token = self.tokens.getToken()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        if (self.tokens.getToken() == '('): # subroutinename(args)
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.vmWriter.writePush('pointer', '0')
            numArgs = self.CompileExpressionList()
            self.vmWriter.writeCall(self.className + '.' + token, numArgs + 1)
            self.vmWriter.writePop('temp', '0')
        else: # someclass.subroutinename(args)
            className = token
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            routineName = self.tokens.getToken()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();

            numArgs = 0
            succ = True
            try:
                type = self.symbols.typeOf(className)
                kind = self.symbols.kindOf(className)
                index = self.symbols.indexOf(className)
                if kind == 'field':
                    kind = 'this'
                self.vmWriter.writePush(kind, index)
                numArgs += 1
            except:
                succ = False
                
            numArgs += self.CompileExpressionList()
            if succ:
                self.vmWriter.writeCall(type + '.' + routineName, numArgs)
            else:
                self.vmWriter.writeCall(className + '.' + routineName, numArgs)
            self.vmWriter.writePop('temp', '0')
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();

    def compileLet(self):
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # identifier
        token = self.tokens.getToken()
        type = self.symbols.typeOf(token)
        kind = self.symbols.kindOf(token)
        index = self.symbols.indexOf(token)
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        if self.tokens.getToken() == '[':
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.vmWriter.writePush(kind, index)
            self.CompileExpression()
            self.vmWriter.writeArithmetic('add')
            self.vmWriter.writePop('pointer', 1)
            assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # =
            assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # assignexpr
            self.CompileExpression()
            self.vmWriter.writePop('that', 0)
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        else:
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.CompileExpression()
            if kind == 'field':
                kind = 'this'
            self.vmWriter.writePop(kind, index)
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();

    def compileWhile(self):
        jumpLabel = 'whilejump' + str(self.ifCounter)
        self.ifCounter += 1
        breakLabel = 'whilebreak' + str(self.ifCounter)
        self.ifCounter += 1
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # (
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # expstart
        self.vmWriter.writeLabel(jumpLabel)
        self.CompileExpression()
        self.vmWriter.writeArithmetic('not')
        self.vmWriter.writeIf(breakLabel)
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # {
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # statementsstart
        self.compileStatements()
        self.vmWriter.writeGoto(jumpLabel)
        self.vmWriter.writeLabel(breakLabel)
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # after }

    def compileReturn(self):
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        if self.tokens.getToken() != ';':
            self.CompileExpression()
        else:
            self.vmWriter.writePush('constant', '0')
        self.vmWriter.writeReturn()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();

    def compileIf(self):
        ifjump = 'ifjump' + str(self.ifCounter)
        self.ifCounter += 1
        elsjump = 'elsjump' + str(self.ifCounter)
        self.ifCounter += 1
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # (
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # expstart
        self.CompileExpression()
        self.vmWriter.writeArithmetic('not')
        self.vmWriter.writeIf(ifjump)
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # {
        assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        self.compileStatements()
        assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # after }
        self.vmWriter.writeGoto(elsjump)
        self.vmWriter.writeLabel(ifjump)
        if self.tokens.getToken() == 'else':
            assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # {
            assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # statements start
            self.compileStatements()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # after }
        self.vmWriter.writeLabel(elsjump)

    def CompileExpression(self):
        self.CompileTerm()
        while self.tokens.getToken() in '+-*/&|<>=':
            oper = self.tokens.getToken()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.CompileTerm()
            if oper in CompilationEngine.vmArithmetics:
                self.vmWriter.writeArithmetic(
                    CompilationEngine.vmArithmetics[oper])
            else:
                self.vmWriter.writeCall(
                    CompilationEngine.osArithmetics[oper], 2)
            

    def CompileTerm(self):
        token = self.tokens.getToken() 
        if token in '-~':
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.CompileTerm()
            oper = 'not' if token == '~' else 'neg'
            self.vmWriter.writeArithmetic(oper)
        elif token == '(':
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            self.CompileExpression()
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        elif token == 'false':
            self.vmWriter.writePush('constant', '0')
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        elif token == 'true':
            self.vmWriter.writePush('constant', '1')
            self.vmWriter.writeArithmetic('neg')
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        elif token == 'this':
            self.vmWriter.writePush('pointer', '0')
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        elif token == 'null':
            self.vmWriter.writePush('constant', '0')
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        elif self.tokens.tokenType() == 'stringConstant':
            token = self.tokens.getToken()
            self.vmWriter.writePush('constant', len(token))
            self.vmWriter.writeCall('String.new', 1)
            self.vmWriter.writePop('temp', '4')
            for ch in token:
                self.vmWriter.writePush('temp', '4')
                self.vmWriter.writePush('constant', ord(ch))
                self.vmWriter.writeCall('String.appendChar', 2)
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        elif token.isdigit():
            self.vmWriter.writePush('constant', token)
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
        else:
            assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            if self.tokens.getToken() == '(':
                assert(self.tokens.hasMoreTokens()); self.tokens.advance();
                self.vmWriter.writePush('pointer', '0')
                numArgs = self.CompileExpressionList()
                self.vmWriter.writeCall(token, numArgs + 1)
                assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            elif self.tokens.getToken() == '[':
                assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # expstart
                type = self.symbols.typeOf(token)
                kind = self.symbols.kindOf(token)
                index = self.symbols.indexOf(token)
                self.vmWriter.writePush(kind, index)
                self.CompileExpression()
                self.vmWriter.writeArithmetic('add')

                self.vmWriter.writePush('pointer', '1')
                self.vmWriter.writePop('temp', '5')

                self.vmWriter.writePop('pointer', '1')
                self.vmWriter.writePush('that', '0')

                self.vmWriter.writePush('temp', '5')
                self.vmWriter.writePop('pointer', '1')
                assert(self.tokens.hasMoreTokens()); self.tokens.advance();
            elif self.tokens.getToken() == '.':
                assert(self.tokens.hasMoreTokens()); self.tokens.advance(); #funcname
                funcName = self.tokens.getToken()
                assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # (
                assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # explist start

                numArgs = 0
                className = token
                try:
                    type = self.symbols.typeOf(className)
                    kind = self.symbols.kindOf(className)
                    index = self.symbols.indexOf(className)
                    if kind == 'field':
                        kind = 'this'
                    self.vmWriter.writePush(kind, index)
                    numArgs += 1
                    className = type
                except:
                    pass

                numArgs += self.CompileExpressionList()
                self.vmWriter.writeCall(className + '.' + funcName, numArgs)
                assert(self.tokens.hasMoreTokens()); self.tokens.advance(); # after )
            else:
                type = self.symbols.typeOf(token)
                kind = self.symbols.kindOf(token)
                index = self.symbols.indexOf(token)
                if (kind == 'field'):
                    self.vmWriter.writePush('this', index)
                else:
                    self.vmWriter.writePush(kind, index)

    def CompileExpressionList(self):
        numExpr = 0
        if self.tokens.getToken() != ')':
            numExpr += 1
            self.CompileExpression()
            while self.tokens.getToken() == ',':
                numExpr += 1
                assert(self.tokens.hasMoreTokens()); self.tokens.advance();
                self.CompileExpression()
        return numExpr
