from abc import ABC, abstractmethod, ABCMeta
from Visitor import Visitor


class AST(ABC):
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    @abstractmethod
    def accept(self, v, param):
        return v.visit(self, param)

# used for whole program
class Program(AST):
    #decl:list(ClassDecl)
    def __init__(self, decl):
        self.decl = decl
    
    def __str__(self):
        return "Program(List(" + ','.join(str(i) for i in self.decl) + "))"
    
    def accept(self, v: Visitor, param):
        return v.visitProgram(self, param)

class Decl(AST):
    __metaclass__ = ABCMeta
    pass

# used for local variable or parameter declaration 
class VarDecl(Decl):
    #variable:Id
    #varType: Type
    def __init__(self, variable, varType):
        self.variable = variable
        self.varType = varType

    def __str__(self):
        return "VarDecl(" + str(self.variable) + "," + str(self.varType) + ")"

    def accept(self, v, param):
        return v.visitVarDecl(self, param)

# used for local constant declaration
class ConstDecl(Decl):
    #constant:Id
    #constType: Type
    #value: Expr
    def __init__(self, constant, constType,value):
        self.constant = constant
        self.constType = constType
        self.value = value

    def __str__(self):
        return "ConstDecl(" + str(self.constant) + "," + str(self.constType) + "," + str(self.value) + ")"

    def accept(self, v, param):
        return v.visitConstDecl(self, param)
 
#used for a class declaration
class ClassDecl(Decl):
    #classname:Id
    #memlist:list(MemDecl)
    #parentname: Id
    def __init__(self, classname, memlist, parentname = None):
        self.classname = classname
        self.memlist = memlist
        self.parentname = parentname

    def __str__(self):
        return "ClassDecl(" + str(self.classname) + (("," + str(self.parentname)) if self.parentname else "") + ",List(" + ','.join(str(i) for i in self.memlist) + "))"

    def accept(self, v, param):
        return v.visitClassDecl(self, param) 

class SIKind(AST):
    __metaclass__ = ABCMeta

# used for instance member
class Instance(SIKind): 
    def __str__(self):
        return "Instance"
    def accept(self,v, param):
        return v.visitInstance(self,param)

# used for static member
class Static(SIKind):
    def __str__(self):
        return "Static"
    def accept(self,v, param):
        return v.visitStatic(self,param)

class MemDecl(AST):
    __metaclass__ = ABCMeta
    pass

# used for a normal or special method declaration. 
# In the case of special method declaration,the name will be Id("<init>") 
# and the return type is VoidType(). 
# In the case of normal method declaration, the name and the return type are from the declaration.
class MethodDecl(MemDecl):
    #kind: SIKind
    #name: Id
    #param: list(VarDecl)
    #returnType: Type
    #body: Block
    def __init__(self, sikind, name, param, returnType, body):
        self.sikind = sikind
        self.name = name
        self.param = param
        self.returnType = returnType
        self.body = body

    def __str__(self):
        return "MethodDecl(" + str(self.name) + ',' + str(self.sikind) + ",List(" +  ','.join(str(i) for i in self.param) + ")," + str(self.returnType) + "," + str(self.body) + ")"
    
    def accept(self, v, param):
        return v.visitMethodDecl(self, param)

# used for mutable (variable) or immutable (constant) declaration
class AttributeDecl(MemDecl):
    #kind: SIKind
    #decl: Decl
    def __init__(self, sikind, decl):
        self.sikind = sikind
        self.decl = decl
        

    def __str__(self):
        return "AttributeDecl(" + str(self.sikind) + ',' + str(self.decl) + ")"
    
    def accept(self, v, param):
        return v.visitAttributeDecl(self, param)

class Type(AST):
    __metaclass__ = ABCMeta
    pass

class IntType(Type):
    def __str__(self):
        return "IntType"

    def accept(self, v, param):
        return v.visitIntType(self, param)

class FloatType(Type):
    def __str__(self):
        return "FloatType"

    def accept(self, v, param):
        return v.visitFloatType(self, param)

class BoolType(Type):
    def __str__(self):
        return "BoolType"

    def accept(self, v, param):
        return v.visitBoolType(self, param)

class StringType(Type):
    def __str__(self):
        return "StringType"

    def accept(self, v, param):
        return v.visitStringType(self, param)

class ArrayType(Type):
    #size:int
    #eleType:Type
    def __init__(self, size, eleType):
        self.size = size
        self.eleType = eleType
        
    def __str__(self):
        return "ArrayType(" + str(self.size) +  "," + str(self.eleType) + ")"

    def accept(self, v, param):
        return v.visitArrayType(self, param)

class ClassType(Type):
    #classname:Id
    def __init__(self, classname):
        self.classname = classname
        
    def __str__(self):
        return "ClassType(" + str(self.classname)  + ")"

    def accept(self, v, param):
        return v.visitClassType(self, param)

class VoidType(Type):
    def __str__(self):
        return "VoidType"

    def accept(self, v, param):
        return v.visitVoidType(self, param)


class Stmt(AST):
    __metaclass__ = ABCMeta
    pass

class Assign(Stmt):
    #lhs:Expr
    #exp:Expr
    def __init__(self, lhs, exp):
        self.lhs = lhs
        self.exp = exp

    def __str__(self):
        return "AssignStmt(" + str(self.lhs) + "," +  str(self.exp) + ")"

    def accept(self, v, param):
        return v.visitAssign(self, param)

class If(Stmt):
    #expr:Expr
    #thenStmt:Stmt
    #elseStmt:Stmt
    def __init__(self, expr, thenStmt, elseStmt=None):
        self.expr = expr
        self.thenStmt = thenStmt
        self.elseStmt = elseStmt

    def __str__(self):
        return "If(" + str(self.expr) + "," + str(self.thenStmt) + (("," +  str(self.elseStmt)) if self.elseStmt else "")  + ")"

    def accept(self, v, param):
        return v.visitIf(self, param)

class For(Stmt):
    #id:Id
    #expr1,expr2:Expr
    #loop:Stmt
    #up:Boolean #True => increase; False => decrease
    def __init__(self, id, expr1, expr2,up,loop):
        self.id = id
        self.expr1 = expr1
        self.expr2 = expr2
        self.up = up
        self.loop = loop

    def __str__(self):
        return "For(" + str(self.id) + "," + str(self.expr1) + "," + str(self.expr2) + "," + str(self.up) + ',' + str(self.loop)  + "])"

    def accept(self, v, param):
        return v.visitFor(self, param)

class Break(Stmt):
    def __str__(self):
        return "Break"

    def accept(self, v, param):
        return v.visitBreak(self, param)
    
class Continue(Stmt):
    def __str__(self):
        return "Continue"

    def accept(self, v, param):
        return v.visitContinue(self, param)

class Return(Stmt):
    #expr:Expr
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return "Return(" + str(self.expr) + ")"

    def accept(self, v, param):
        return v.visitReturn(self, param)

class CallStmt(Stmt):
    #method:Id
    #param:list(Expr)
    def __init__(self, method, param):
        self.method = method
        self.param = param

    def __str__(self):
        return "CallStmt(" + str(self.method) + ",[" +  ','.join(str(i) for i in self.param) + "])"

    def accept(self, v, param):
        return v.visitCallStmt(self, param)

class Block(Stmt):
    #decl:list(VarDecl)
    #stmt:list(Stmt)
    def __init__(self, decl, stmt):
        self.decl = decl
        self.stmt = stmt

    def __str__(self):
        return "Block(List(" + ','.join(str(i) for i in self.decl) + "),List(" + ','.join(str(i) for i in self.stmt) + "))"

    def accept(self, v, param):
        return v.visitBlock(self, param)


class Expr(Stmt):
    __metaclass__ = ABCMeta
    pass

# used for binary expression
class BinaryOp(Expr):
    #op:string
    #left:Expr
    #right:Expr
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return "BinaryOp(" + self.op + "," + str(self.left) + "," + str(self.right) + ")"

    def accept(self, v, param):
        return v.visitBinaryOp(self, param)

#used for unary expression with orerand like !,+,-
class UnaryOp(Expr):
    #op:string
    #body:Expr
    def __init__(self, op, body):
        self.op = op
        self.body = body

    def __str__(self):
        return "UnaryOp(" + self.op + "," + str(self.body) + ")"

    def accept(self, v, param):
        return v.visitUnaryOp(self, param)

class CallExpr(Expr):
    #method:Id
    #param:list(Expr)
    def __init__(self, method, param):
        self.method = method
        self.param = param

    def __str__(self):
        return "CallExpr(" + str(self.method) + ",List(" +  ','.join(str(i) for i in self.param) + "))"

    def accept(self, v, param):
        return v.visitCallExpr(self, param)

class NewExpr(Expr):
    #classname:Id
    #param:list(Expr)
    def __init__(self, classname, param):
        self.classname = classname
        self.param = param

    def __str__(self):
        return "NewExpr(" + str(self.classname) + ",List(" +  ','.join(str(i) for i in self.param) + "))"

    def accept(self, v, param):
        return v.visitNewExpr(self, param)

class LHS(Expr):
    __metaclass__ = ABCMeta
    pass

class Id(LHS):
    #name:string
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Id(" + self.name + ")"

    def accept(self, v, param):
        return v.visitId(self, param)

class ArrayCell(LHS):
    #arr:Expr
    #idx:Expr
    def __init__(self, arr, idx):
        self.arr = arr
        self.idx = idx

    def __str__(self):
        return "ArrayCell(" + str(self.arr) + "," + str(self.idx) + ")"

    def accept(self, v, param):
        return v.visitArrayCell(self, param)

class FieldAccess(LHS):
    #obj:Expr
    #fieldname:Id
    def __init__(self, obj, fieldname):
        self.obj = obj
        self.fieldname = fieldname

    def __str__(self):
        return "FieldAccess(" + str(self.obj) + "," + str(self.fieldname) + ")"

    def accept(self, v, param):
        return v.visitFieldAccess(self, param)


class Literal(Expr):
    __metaclass__ = ABCMeta
    pass

class IntLiteral(Literal):
    #value:int
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "IntLiteral(" + str(self.value) + ")"

    def accept(self, v, param):
        return v.visitIntLiteral(self, param)

class FloatLiteral(Literal):
    #value:float
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "FloatLiteral(" + str(self.value) + ")"

    def accept(self, v, param):
        return v.visitFloatLiteral(self, param)

class StringLiteral(Literal):
    #value:string
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "StringLiteral(" + self.value + ")"

    def accept(self, v, param):
        return v.visitStringLiteral(self, param)

class BooleanLiteral(Literal):
    #value:boolean
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "BooleanLiteral(" + str(self.value) + ")"

    def accept(self, v, param):
        return v.visitBooleanLiteral(self, param)


class NullLiteral(Literal):
    def __str__(self):
        return "NullLiteral()"

    def accept(self, v, param):
        return v.visitNullLiteral(self, param)

class SelfLiteral(Literal):
    def __str__(self):
        return "SelfLiteral()"

    def accept(self, v, param):
        return v.visitSelfLiteral(self, param)
