from BKOOLVisitor import BKOOLVisitor
from BKOOLParser import BKOOLParser
from AST import *

class ASTGeneration(BKOOLVisitor):

    def visitProgram(self,ctx:BKOOLParser.ProgramContext):
        # return Program([self.visit(x) for x in ctx.class_dec()])
        # return Program([decl for decls in ctx.class_dec() for decl in self.visit(decls)])
        lst = []
        for x in ctx.class_dec():
            lst += [self.visit(x)]
        return Program(lst)
    def visitClass_dec(self,ctx:BKOOLParser.Class_decContext):
        # return ClassDecl(Id(ctx.ID().getText()),[self.visit(x) for x in ctx.memdecl()], Id(ctx.ID().getText()) if ctx.ID())
        a =  [self.visit(x) for x in ctx.member()]
        lst = []
        for i in range(0, len(a)):
            if isinstance(a[i],list):
                lst += a[i]
            else:
                lst.append(a[i])
        return ClassDecl(Id(ctx.ID(0).getText()),lst,
                Id(ctx.ID(1).getText()) if ctx.ID(1) else None)

    def visitMember(self,ctx:BKOOLParser.MemberContext):
        #member : (attibute | method_dec)+ ;
        lst = []
        for i in range(0, ctx.getChildCount()):
            if ctx.attribute(i):
                temp = self.visit(ctx.attribute(i))
                if not isinstance(temp,list):
                    temp = [temp]
                lst += temp
                
            elif ctx.method_dec(i):
                temp = self.visit(ctx.method_dec(i))
                if isinstance(temp,list):
                    lst += temp
                else:
                    lst.append(temp)
        return lst

    def visitAttribute(self,ctx:BKOOLParser.AttributeContext):
        #attibute : constant_dec | var_dec ;
        #return AttributeDecl()
        return self.visit(ctx.getChild(0))
    def visitConstant_dec(self,ctx:BKOOLParser.Constant_decContext):
        #constant_dec : (STATIC)? FINAL bktype ID '=' exp SEMI ;
        #ConstDecl
        skind = Static() if ctx.STATIC() else Instance()
        const_dec = ConstDecl(Id(ctx.ID().getText()),self.visit(ctx.bktype()),self.visit(ctx.exp()))
        return AttributeDecl(skind,const_dec)
    def visitVar_dec(self,ctx:BKOOLParser.Var_decContext):
        #var_dec : STATIC? ID (COMMA ID)* COLON bktype SEMI ;
        lst=[]
        skind = Static() if ctx.STATIC() else Instance()
        for x in ctx.ID():
            lst += [AttributeDecl(skind,VarDecl(Id(x.getText()),self.visit(ctx.bktype())))]
        return lst

    def visitMethod_dec(self,ctx:BKOOLParser.Method_decContext):
        #method_dec : (bktype | VOID)? STATIC? ID LB list_of_para? RB block_statement ;
        #kind: SIKind
        #name: Id
        #param: list(VarDecl)
        #returnType: Type
        #body: Block
        
        
        skind = Static() if ctx.STATIC() else Instance()
        name = Id(ctx.ID().getText())
        param = self.visit(ctx.list_of_para()) if ctx.list_of_para() else []
        returnType = self.visit(ctx.bktype()) if ctx.bktype() else VoidType()
        block = self.visit(ctx.block_statement())
        return MethodDecl(skind,name,param,returnType,block)
    
        #chua xongggggggggggggg




    def visitList_of_para(self,ctx:BKOOLParser.List_of_paraContext):
        #list_of_para : para (SEMI para)* ;
        lst_variable = []
        for x in ctx.para():
            lst_variable += self.visit(x)
        return lst_variable
        
    def visitPara(self,ctx:BKOOLParser.ParaContext):
        #para : ID (COMMA ID)* COLON bktype
        return [VarDecl(Id(x.getText()),self.visit(ctx.bktype())) for x in ctx.ID()]
    def visitStmt(self,ctx:BKOOLParser.StmtContext):
        return self.visit(ctx.getChild(0))
    def visitCall_statement(self,ctx:BKOOLParser.Call_statementContext):
        #call_statement : funccall SEMI;
        
        return self.visit(ctx.funccall())
    def visitFunccall(self,ctx:BKOOLParser.FunccallContext):
        #funccall: (THIS|ID) DOT ID LB (exp (COMMA exp)*)? RB ;
        
        lst_exp = [self.visit(x) for x in ctx.exp()]
        
        if ctx.THIS():
            return CallStmt(SelfLiteral(),Id(ctx.ID().getText()),lst_exp)
        else:
            return CallStmt(Id(ctx.ID(0).getText()),Id(ctx.ID(1).getText()),lst_exp)
    def visitBlock_statement(self,ctx:BKOOLParser.Block_statementContext):
        #block_statement : LP attibute* stmt*   RP ;
        lst_attribute = []
        lst_stmt = []
        for x in ctx.attribute():
            lst_attribute += self.visit(x)
        for y in ctx.stmt():
            lst_stmt += [self.visit(y)]
        return Block(lst_attribute,lst_stmt)
    def visitAssignment_statement(self,ctx:BKOOLParser.Assignment_statementContext):
        #assignment_statement : lhs ASSIGN exp SEMI ;
        
        return Assign(self.visit(ctx.lhs()),self.visit(ctx.exp()))
        #coi lai .g4
    def visitLhs(self,ctx:BKOOLParser.LhsContext):
        #lhs :   (local_var | var_dec | arraytype);
        if ctx.local_var():
            return self.visit(ctx.local_var())
        elif ctx.var_dec():
            return self.visit(ctx.var_dec())
        else: return self.visit(ctx.arraytype())
    def visitLocal_var(self,ctx:BKOOLParser.Local_varContext):
        #local_var: THIS DOT ID | ID ;
        if ctx.getChildCount() == 3:
            return FieldAccess(SelfLiteral(),Id(ctx.ID().getText()))
        else: 
            return Id(ctx.ID().getText())
            #..chưa làm
    def visitExp(self,ctx:BKOOLParser.ExpContext):
        
        if ctx.getChildCount() == 3:
            op = str(ctx.getChild(1).getText())
            return BinaryOp(op,self.visit(ctx.exp2(0)),self.visit(ctx.exp2(1)))     
        else:
            return self.visit(ctx.exp2(0))
            
    def visitExp2(self,ctx:BKOOLParser.Exp2Context):
        if ctx.getChildCount() == 3:
            op = str(ctx.getChild(1).getText())
            return BinaryOp(op,
                            self.visit(ctx.exp3(0)),
                            self.visit(ctx.exp3(1)))
        else:
            return self.visit(ctx.exp3(0))

    def visitExp3(self,ctx:BKOOLParser.Exp3Context):
        if ctx.getChildCount() == 3:
            op = str(ctx.getChild(1).getText())
            return BinaryOp(op,
                            self.visit(ctx.exp3()),
                            self.visit(ctx.exp4()))
        else:
            return self.visit(ctx.exp4())        
    
    def visitExp4(self,ctx:BKOOLParser.Exp4Context):
        if ctx.getChildCount() == 3:
            op = str(ctx.getChild(1).getText())
            return BinaryOp(op,
                            self.visit(ctx.exp4()),
                            self.visit(ctx.exp5()))
        else:
            
            return self.visit(ctx.exp5())        
        
    def visitExp5(self,ctx:BKOOLParser.Exp5Context):
        
        if ctx.getChildCount() == 3:
            op = str(ctx.getChild(1).getText())
            return BinaryOp(op,
                            self.visit(ctx.exp5()),
                            self.visit(ctx.exp6()))
        else:
            return self.visit(ctx.exp6())        
        
    def visitExp6(self,ctx:BKOOLParser.Exp6Context):
        if ctx.getChildCount() == 3:
            op = str(ctx.getChild(1).getText())
            return BinaryOp(op,
                            self.visit(ctx.exp6(),
                            self.visit(ctx.exp7())))
        else:
            return self.visit(ctx.exp7())        
        
    def visitExp7(self,ctx:BKOOLParser.Exp7Context):
        if ctx.getChildCount() == 2:
            op = str(ctx.getChild(0).getText())
            return UnaryOp(op,
                            self.visit(ctx.exp7()))
        else:
            return self.visit(ctx.exp8())        
    def visitExp8(self,ctx:BKOOLParser.Exp8Context):
        if ctx.getChildCount() == 2:
            op = str(ctx.getChild(0).getText())
            return UnaryOp(op,
                            self.visit(ctx.exp8()))
        else:
            return self.visit(ctx.exp9())            
    def visitExp9(self,ctx:BKOOLParser.Exp9Context):
        if ctx.getChildCount() == 3:
            return self.visit(ctx.exp())
        else:
            return self.visit(ctx.exp10())
    ################       LSB exp RSB | exp10 ;
    def visitExp10(self,ctx:BKOOLParser.Exp10Context):
        if ctx.getChildCount() == 3:
            op = str(ctx.getChild(1).getText())
            return BinaryOp(op,
                            self.visit(ctx.exp10()),
                            self.visit(ctx.exp11()))
        else:
            return self.visit(ctx.exp11())   
    def visitExp11(self,ctx:BKOOLParser.Exp11Context):
        if ctx.getChildCount() == 3:
            op = str(ctx.getChild(1).getText())
            return BinaryOp(op,
                            self.visit(ctx.exp12()),
                            self.visit(ctx.exp11()))
        else:
            return self.visit(ctx.exp12())       
    def visitExp12(self,ctx:BKOOLParser.Exp12Context):
    #exp12   : ID | literal |index_exp | member_access | object_creation |funccall| THIS | LB exp? RB ;

        if ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.literal():
            return self.visit(ctx.literal())
        elif ctx.index_exp():
            return self.visit(ctx.index_exp())
        elif ctx.member_access():
            return self.visit(ctx.member_access())
        elif ctx.object_creation():
            return self.visit(ctx.object_creation())
        elif ctx.funccall():
            return self.visit(ctx.funccall())
        elif ctx.THIS():
            return self.visit(ctx.THIS().getText())
        else:
            return self.visit(ctx.exp())
            
    def visitIndex_exp(self,ctx:BKOOLParser.Index_expContext):
            #index_exp: (ID|member_access|funccall) LSB exp RSB;
        if ctx.ID():
            return ArrayCell(Id(ctx.ID().getText()),self.visit(ctx.exp()))
        elif ctx.member_access():
            return ArrayCell(self.visit(ctx.member_access()),self.visit(ctx.exp()))
        else: 
            return ArrayCell(self.visit(ctx.funccall()),self.visit(ctx.exp()))
    def visitList_exp(self,ctx:BKOOLParser.List_expContext):
    #list_exp: exp (COMMA exp)*;
        list_exp = []
        for x in ctx.exp():
                x = self.visit(x)
                if isinstance(x, list):
                    for i in x:
                        list_exp.append(i)
                else:
                    list_exp.append(x)
        return list_exp 
    def visitMember_access(self,ctx:BKOOLParser.Member_accessContext):
        #instance_attribute | static_attribute | instance_method | static_method ;
        
        return self.visit(ctx.getChild(0))
    def visitInstance_attribute(self,ctx:BKOOLParser.Instance_attributeContext):
        #instance_attribute: (ID | THIS) LB list_exp? RB DOT ID;
    #obj: Expr
    #method:Id
    #param:list(Expr)
        
        if ctx.ID():
            obj = Id(ctx.ID(0).getText())
            id = Id(ctx.ID(1).getText())
        else:
            obj = SelfLiteral()
            id = Id(ctx.ID()).getText()
        param = self.visit(ctx.list_exp()) if ctx.list_exp() else []
        return CallExpr(obj,id,param)
        
    def visitStatic_attribute(self,ctx:BKOOLParser.Static_attributeContext):
        #(ID|THIS) DOT ID;
        
        if ctx.THIS():
            return FieldAccess(SelfLiteral(),Id(ctx.ID(0).getText()))
        else:
            return FieldAccess(Id(ctx.ID(0).getText()),Id(ctx.ID(1).getText()))
    def visitObject_creation(self,ctx:BKOOLParser.Object_creationContext):
        #object_creation: NEW ID LB list_exp? RB;
        #classname:Id
        #param:list(Expr)
        if ctx.list_exp():
            return NewExpr(Id(ctx.ID().getText()),self.visit(ctx.list_exp()))
        else:
            return NewExpr(Id(ctx.ID().getText()),[])
    def visitIf_statement(self,ctx:BKOOLParser.If_statementContext):
        #if_statement : IF exp THEN stmt (ELSE stmt)? ;
        thenstmt = self.visit(ctx.stmt(0))
        if(ctx.stmt(1)):
            elstmt = self.visit(ctx.stmt(1))
        else: 
            elstmt = []
        return If(self.visit(ctx.exp()),thenstmt,elstmt)
    def visitFor_statement(self,ctx:BKOOLParser.For_statementContext):
        #for_statement : FOR ID ASSIGN exp (TO | DOWNTO) exp DO stmt ;
    #id:Id
    #expr1,expr2:Expr
    #loop:Stmt
    #up:Boolean #True => increase; False => decrease        
		#FOR identifier Assign expression (TO|DOWNTO) expression DO statements
        if ctx.TO():
            up = "True"
        else:
            up = "False"
        return For(Id(ctx.ID().getText()),self.visit(ctx.exp(0)),self.visit(ctx.exp(1)),up,self.visit(ctx.stmt()))
		
    def visitBreak_statement(self,ctx:BKOOLParser.Break_statementContext):
        return Break()
    def visitContinue_statement(self,ctx:BKOOLParser.Continue_statementContext):
        return Continue()
    def visitReturn_statement(self,ctx:BKOOLParser.Return_statementContext):
        return Return(self.visit(ctx.exp()))
    def visitMethod_invocation_statement(self,ctx:BKOOLParser.Method_invocation_statementContext):
    #method_invocation_statement : (instance_method | static_method) SEMI ;
        if ctx.instance_method():
            return self.visit(ctx.instance_method())
        else:
            return self.visit(ctx.static_method())
    def visitInstance_method (self,ctx:BKOOLParser.Instance_methodContext):
        #instance_method : THIS DOT ID LB list_exp? RB;
        
        obj = SelfLiteral()
        id = Id(ctx.ID().getText())
        param = self.visit(ctx.list_exp()) if ctx.list_exp() else []


        return CallStmt(obj,id,param)
                
        
    def visitStatic_method(self,ctx:BKOOLParser.Static_methodContext):
        #static_method : ID DOT ID LB list_exp? RB;

        obj = Id(ctx.ID(0).getText())
        id = Id(ctx.ID(1).getText())
        param = self.visit(ctx.list_exp()) if ctx.list_exp() else []


        return CallStmt(obj,id,param)
    def visitLiteral(self, ctx:BKOOLParser.LiteralContext):
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        elif ctx.STRINGLIT():
            return StringLiteral(str(ctx.STRINGLIT().getText()))
        elif ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        elif ctx.BOOLLIT():
            return BooleanLiteral(bool(ctx.BOOLLIT().getText()))

    def visitBktype(self,ctx:BKOOLParser.BktypeContext):
        return self.visit(ctx.getChild(0))
    def visitClasstype(self,ctx:BKOOLParser.ClasstypeContext):
        #classtype : ID | NIL; //
        if ctx.ID():
            return ClassType(ctx.ID().getText())
        else:

            return ClassType(self.visit(ctx.getChild(0)))
        
    def visitArraytype(self,ctx:BKOOLParser.ArraytypeContext):
        #arraytype : (primitivetype|ID) LSB (INTLIT|ID|exp) RSB ;

        #size = str(ctx.getChild(2))
    
        
        if ctx.primitivetype():
            if ctx.INTLIT():
                size = (ctx.INTLIT().getText())
            elif ctx.ID():
                size = Id(ctx.ID().getText())
            else:
                size = self.visit(ctx.exp())
            return ArrayType(size,self.visit(ctx.primitivetype()))
        else:
            if ctx.INTLIT():
                size = ctx.INTLIT().getText()
            elif ctx.ID(1):
                size = Id(ctx.ID(1).getText())
            else:
                size = self.visit(ctx.exp())    
            return ArrayType(size,ClassType(ctx.ID(0).getText()))

    def visitPrimitivetype(self,ctx:BKOOLParser.PrimitivetypeContext):
    	
        if ctx.BOOLTYPE():
            return BoolType()
        elif ctx.INTTYPE():
            return IntType()
        elif ctx.FLOATTYPE():
            return FloatType()
        elif ctx.STRINGTYPE():
            return StringType()
        else:
            return VoidType()


        

    
