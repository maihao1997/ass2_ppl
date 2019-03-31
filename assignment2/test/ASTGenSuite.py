import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):
    def test_simple_program(self):
        """Simple program: class main {} """
        input = """class main {}"""
        expect = str(Program([ClassDecl(Id("main"),[])]))
        self.assertTrue(TestAST.test(input,expect,300))

    def test_simple_program1(self):
        input = """class Rectangle extends Shape {
                    
                }"""
        expect = str(Program([ClassDecl(Id("Rectangle"),[],Id("Shape"))]))
        self.assertTrue(TestAST.test(input,expect,301))

    def test_simple_program2(self):
        input = """class Rectangle extends Shape {
                    static final int numOfShape = 0;
                }"""
        expect = str(Program([ClassDecl(Id("Rectangle"),[AttributeDecl(Static(),ConstDecl(Id("numOfShape"),IntType(),IntLiteral(0)))],Id("Shape"))]))
        self.assertTrue(TestAST.test(input,expect,302))

    def test_simple_program3(self):
        input = """class Shape {
                    static final int numOfShape = 0;
                }"""
        expect = str(Program([ClassDecl(Id("Shape"),[AttributeDecl(Static(),ConstDecl(Id("numOfShape"),IntType(),IntLiteral(0)))])]))
        self.assertTrue(TestAST.test(input,expect,303))

    def test_simple_program4(self):
        input = """class Shape {
                    static final int numOfShape = 0;
                    final int immuAttribute = 0;
                    length,width: float;
                }"""
        expect = str(Program([ClassDecl(Id("Shape"),[AttributeDecl(Static(),ConstDecl(Id("numOfShape"),IntType(),IntLiteral(0))),AttributeDecl(Instance(),ConstDecl(Id("immuAttribute"),IntType(),IntLiteral(0))),AttributeDecl(Instance(),VarDecl(Id("length"),FloatType())),AttributeDecl(Instance(),VarDecl(Id("width"),FloatType()))])]))
        self.assertTrue(TestAST.test(input,expect,304))

    def test_simple_program5(self):
        input = """class Shape {
                    final int My1stCons = 1 + 5;
                    static final int My2ndCons = 2;
                }"""
        expect = str(Program([ClassDecl(Id("Shape"),[AttributeDecl(Instance(),ConstDecl(Id("My1stCons"),IntType(),BinaryOp("+",IntLiteral(1),IntLiteral(5)))),AttributeDecl(Static(),ConstDecl(Id("My2ndCons"),IntType(),IntLiteral(2)))])]))
        self.assertTrue(TestAST.test(input,expect,305))

    def test_simple_program6(self):
        input = """class Shape {
                    my1stVar: int;
                    myArrayVar: int[5];
                    static my2ndVar, my3rdVar: Shape;
                    static my2ndArray, my3rdArray: Shape[6];
                }"""
        expect = str(Program([ClassDecl(Id("Shape"),[AttributeDecl(Instance(),VarDecl(Id("my1stVar"),IntType())),AttributeDecl(Instance(),VarDecl(Id("myArrayVar"),ArrayType(5,IntType()))),AttributeDecl(Static(),VarDecl(Id("my2ndVar"),ClassType("Shape"))),AttributeDecl(Static(),VarDecl(Id("my3rdVar"),ClassType("Shape"))),AttributeDecl(Static(),VarDecl(Id("my2ndArray"),ArrayType(6,ClassType("Shape")))),AttributeDecl(Static(),VarDecl(Id("my3rdArray"),ArrayType(6,ClassType("Shape"))))])]))
        self.assertTrue(TestAST.test(input,expect,306))
    
    def test_simple_program7(self):
        input = """class Shape {
                        float getArea(){
                        }
                    }"""
        ### Truyen Instance() zo truoc
        expect = str(Program([ClassDecl(Id("Shape"),[MethodDecl(Instance(),Id("getArea"),[],FloatType(),Block([],[]))])]))
        self.assertTrue(TestAST.test(input,expect,307))    
    def test_simple_program8(self):
        input = """class Shape {
                        float getArea(){
                            return this.length*this.width;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("Shape"),[MethodDecl(Instance(),Id("getArea"),[],FloatType(),Block([],[Return(BinaryOp("*",FieldAccess(SelfLiteral(),Id("length")),FieldAccess(SelfLiteral(),Id("width"))))]))])]))
        self.assertTrue(TestAST.test(input,expect,308))
    def test_simple_program9(self):
        input = """class Shape {
                        void static getArea(a, b, c: int){
                            return this.length*this.width;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("Shape"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType()),VarDecl(Id("c"),IntType())],VoidType(),Block([],[Return(BinaryOp("*",FieldAccess(SelfLiteral(),Id("length")),FieldAccess(SelfLiteral(),Id("width"))))]))])])) 
        self.assertTrue(TestAST.test(input,expect,309))
    def test_simple_program10(self):
        input = """class Shape {
                        void static getArea(a, b, c: int){
                            return this.length*this.width;
                        }
                    }
                    class abc {
                        my1stVar: int;
                        myArrayVar: int[5];
                        static my2ndVar, my3rdVar: Shape;
                        static my2ndArray, my3rdArray: Shape[6];
                    }"""
        expect = str(Program([ClassDecl(Id("Shape"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType()),VarDecl(Id("c"),IntType())],VoidType(),Block([],[Return(BinaryOp("*",FieldAccess(SelfLiteral(),Id("length")),FieldAccess(SelfLiteral(),Id("width"))))]))]),ClassDecl(Id("abc"),[AttributeDecl(Instance(),VarDecl(Id("my1stVar"),IntType())),AttributeDecl(Instance(),VarDecl(Id("myArrayVar"),ArrayType(5,IntType()))),AttributeDecl(Static(),VarDecl(Id("my2ndVar"),ClassType("Shape"))),AttributeDecl(Static(),VarDecl(Id("my3rdVar"),ClassType("Shape"))),AttributeDecl(Static(),VarDecl(Id("my2ndArray"),ArrayType(6,ClassType("Shape")))),AttributeDecl(Static(),VarDecl(Id("my3rdArray"),ArrayType(6,ClassType("Shape"))))])])) 
        self.assertTrue(TestAST.test(input,expect,310))
    def test_simple_program11(self):
        input = """class abc {
                        void static getArea(a, b, c: int){
                            return a;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType()),VarDecl(Id("c"),IntType())],VoidType(),Block([],[Return(Id("a"))]))])]))    
        self.assertTrue(TestAST.test(input,expect,311))
    def test_simple_program12(self):
        input = """class abc {
                        string getArea(a, b, c: int){
                            return abae[1+2];
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("getArea"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType()),VarDecl(Id("c"),IntType())],StringType(),Block([],[Return(ArrayCell(Id("abae"),BinaryOp("+",IntLiteral(1),IntLiteral(2))))]))])]))    
        self.assertTrue(TestAST.test(input,expect,312))

    def test_simple_program13(self):
        input = """class abc {
                        void getArea(a, b, c: string){
                            return b[[4]];
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("getArea"),[VarDecl(Id("a"),StringType()),VarDecl(Id("b"),StringType()),VarDecl(Id("c"),StringType())],VoidType(),Block([],[Return(ArrayCell(Id("b"),IntLiteral(4)))]))])]))    
        self.assertTrue(TestAST.test(input,expect,313))

    def test_simple_program14(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            {
                                this.length := length;
                                this.length := length;
                            }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[Block([],[Assign(FieldAccess(SelfLiteral(),Id("length")),Id("length")),Assign(FieldAccess(SelfLiteral(),Id("length")),Id("length"))])]))])]))    
        self.assertTrue(TestAST.test(input,expect,314))
    def test_simple_program15(self):
        input = """class abc {
                        void static getArea(length,width:float){
                                %%start of declaration part
                                r,s:float;
                                a,b:int[5];
                                %%list of statements
                                r := r ;
                                s:=r*r*this.myPI;
                                a[0]:= 2.0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([AttributeDecl(Instance(),VarDecl(Id("r"),FloatType())),AttributeDecl(Instance(),VarDecl(Id("s"),FloatType())),AttributeDecl(Instance(),VarDecl(Id("a"),ArrayType(5,IntType()))),AttributeDecl(Instance(),VarDecl(Id("b"),ArrayType(5,IntType())))],[Assign(Id("r"),Id("r")),Assign(Id("s"),BinaryOp("*",BinaryOp("*",Id("r"),Id("r")),FieldAccess(SelfLiteral(),Id("myPI")))),Assign(ArrayType(0,ClassType("a")),FloatLiteral(2.0))]))])]))    
        self.assertTrue(TestAST.test(input,expect,315))
    
    def test_simple_program16(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            this.aPI := 3.14;
                            value := x.foo(5);
                            l[3] := value * 2;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[Assign(FieldAccess(SelfLiteral(),Id("aPI")),FloatLiteral(3.14)),Assign(Id("value"),CallStmt(Id("x"),Id("foo"),[IntLiteral(5)])),Assign(ArrayType(3,ClassType("l")),BinaryOp("*",Id("value"),IntLiteral(2)))]))])]))    
        self.assertTrue(TestAST.test(input,expect,316))
    def test_simple_program17(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            if a > 1 then
                                io.write("Suy nua thi");
                            else
                                io.write("Anh sai roi");
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[If(BinaryOp(">",Id("a"),IntLiteral(1)),CallStmt(Id("io"),Id("write"),[StringLiteral("Suy nua thi")]),CallStmt(Id("io"),Id("write"),[StringLiteral("Anh sai roi")]))]))])]))    
        self.assertTrue(TestAST.test(input,expect,317))

    def test_simple_program19(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            if a <= b + c then
                                value := x.foo(5);
                                l[3] := value * 2;
                                io.write("Suy nua thi");
                                if b < 0 then
                                    b := c + 3;
                                else
                                    b[1] := a;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[If(BinaryOp("<=",Id("a"),BinaryOp("+",Id("b"),Id("c"))),Assign(Id("value"),CallStmt(Id("x"),Id("foo"),[IntLiteral(5)]))),Assign(ArrayType(3,ClassType("l")),BinaryOp("*",Id("value"),IntLiteral(2))),CallStmt(Id("io"),Id("write"),[StringLiteral("Suy nua thi")]),If(BinaryOp("<",Id("b"),IntLiteral(0)),Assign(Id("b"),BinaryOp("+",Id("c"),IntLiteral(3))),Assign(ArrayType(1,ClassType("b")),Id("a")))]))])]))    
        self.assertTrue(TestAST.test(input,expect,319))

    def test_simple_program20(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            if a[3] == 1 then
                                io.write("Suy nua thi");
                                if b < 0 then
                                    b := c + 3;
                                else
                                    b[1] := a;
                                    io.write("Phia sau mot co gai");
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[If(BinaryOp("==",ArrayCell(Id("a"),IntLiteral(3)),IntLiteral(1)),CallStmt(Id("io"),Id("write"),[StringLiteral("Suy nua thi")])),If(BinaryOp("<",Id("b"),IntLiteral(0)),Assign(Id("b"),BinaryOp("+",Id("c"),IntLiteral(3))),Assign(ArrayType(1,ClassType("b")),Id("a"))),CallStmt(Id("io"),Id("write"),[StringLiteral("Phia sau mot co gai")])]))])]))    
        self.assertTrue(TestAST.test(input,expect,320))
    

    def test_simple_program21(self):
            input = """class abc {
                        void static getArea(length,width:float){
                            for x := 5 downto 2 do
                                io.writeIntLn(x);
                        }
                    }"""
            expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[For(Id("x"),IntLiteral(5),IntLiteral(2),False,CallStmt(Id("io"),Id("writeIntLn"),[Id("x")]))]))])]))    
            self.assertTrue(TestAST.test(input,expect,321))

    def test_simple_program22(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            for x := 5 downto 2 do
                                io.writeIntLn(x);
                            for i := 1 to 100 do {
                                io.writeIntLn(i);
                                Intarray[i] := i + 1;
                            }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[For(Id("x"),IntLiteral(5),IntLiteral(2),False,CallStmt(Id("io"),Id("writeIntLn"),[Id("x")])),For(Id("i"),IntLiteral(1),IntLiteral(100),True,Block([],[CallStmt(Id("io"),Id("writeIntLn"),[Id("i")]),Assign(ArrayType(Id("i"),ClassType("Intarray")),BinaryOp("+",Id("i"),IntLiteral(1)))]))]))])]))    
        self.assertTrue(TestAST.test(input,expect,322))
    def test_simple_program23(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            for x := 5 downto 2 do
                                io.writeIntLn(x);
                                break;
                            for i := 1 to 100 do {
                                break;
                                io.writeIntLn(i);
                                Intarray[i] := i + 1;
                            }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[For(Id("x"),IntLiteral(5),IntLiteral(2),False,CallStmt(Id("io"),Id("writeIntLn"),[Id("x")])),Break(),For(Id("i"),IntLiteral(1),IntLiteral(100),True,Block([],[Break(),CallStmt(Id("io"),Id("writeIntLn"),[Id("i")]),Assign(ArrayType(Id("i"),ClassType("Intarray")),BinaryOp("+",Id("i"),IntLiteral(1)))]))]))])]))    
        self.assertTrue(TestAST.test(input,expect,323))    
    def test_simple_program24(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            for x := 5 downto 2 do
                                io.writeIntLn(x);
                                if x == 3 then
                                    break;
                            for i := 1 to 100 do {
                                io.writeIntLn(i);
                                Intarray[i] := i + 1;
                            }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[For(Id("x"),IntLiteral(5),IntLiteral(2),False,CallStmt(Id("io"),Id("writeIntLn"),[Id("x")])),If(BinaryOp("==",Id("x"),IntLiteral(3)),Break()),For(Id("i"),IntLiteral(1),IntLiteral(100),True,Block([],[CallStmt(Id("io"),Id("writeIntLn"),[Id("i")]),Assign(ArrayType(Id("i"),ClassType("Intarray")),BinaryOp("+",Id("i"),IntLiteral(1)))]))]))])]))    
        self.assertTrue(TestAST.test(input,expect,324))
    def test_simple_program25(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            for x := 5 downto 2 do
                                io.writeIntLn(x);
                            for i := 1 to 100 do {
                                io.writeIntLn(i);
                                Intarray[i] := i + 1;
                                if (a*3 < 10) then
                                    continue;
                            }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[For(Id("x"),IntLiteral(5),IntLiteral(2),False,CallStmt(Id("io"),Id("writeIntLn"),[Id("x")])),For(Id("i"),IntLiteral(1),IntLiteral(100),True,Block([],[CallStmt(Id("io"),Id("writeIntLn"),[Id("i")]),Assign(ArrayType(Id("i"),ClassType("Intarray")),BinaryOp("+",Id("i"),IntLiteral(1))),If(BinaryOp("<",BinaryOp("*",Id("a"),IntLiteral(3)),IntLiteral(10)),Continue())]))]))])]))    
        self.assertTrue(TestAST.test(input,expect,325))

    def test_simple_program26(self):
        input = """class abc {
                        string static getArea(length,width:float){
                            for x := 5 downto 2 do
                                io.writeIntLn(x);
                            for i := 1 to 100 do {
                                io.writeIntLn(i);
                                Intarray[i] := i + 1;
                            }

                            return this.a;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],StringType(),Block([],[For(Id("x"),IntLiteral(5),IntLiteral(2),False,CallStmt(Id("io"),Id("writeIntLn"),[Id("x")])),For(Id("i"),IntLiteral(1),IntLiteral(100),True,Block([],[CallStmt(Id("io"),Id("writeIntLn"),[Id("i")]),Assign(ArrayType(Id("i"),ClassType("Intarray")),BinaryOp("+",Id("i"),IntLiteral(1)))])),Return(FieldAccess(SelfLiteral(),Id("a")))]))])]))    
        self.assertTrue(TestAST.test(input,expect,326))
    def test_simple_program27(self):
        input = """class abc {
                        int static getArea(length,width:float){
                            for x := 5 downto 2 do
                                io.writeIntLn(x);
                            for i := 1 to 100 do {
                                if a < 1 then
                                    continue;
                                else
                                    break;
                                io.writeIntLn(i);
                                Intarray[i] := i + 1;
                            }

                            return 0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],IntType(),Block([],[For(Id("x"),IntLiteral(5),IntLiteral(2),False,CallStmt(Id("io"),Id("writeIntLn"),[Id("x")])),For(Id("i"),IntLiteral(1),IntLiteral(100),True,Block([],[If(BinaryOp("<",Id("a"),IntLiteral(1)),Continue(),Break()),CallStmt(Id("io"),Id("writeIntLn"),[Id("i")]),Assign(ArrayType(Id("i"),ClassType("Intarray")),BinaryOp("+",Id("i"),IntLiteral(1)))])),Return(IntLiteral(0))]))])]))    
        self.assertTrue(TestAST.test(input,expect,327))
    def test_simple_program28(self):
        input = """class abc {
                        void static getArea(){
                            for x := 5 downto 2 do
                                Sha.getString();
                                io.writeIntLn(x);
                            for i := 1 to 100 do {
                                io.writeIntLn(i);
                                Intarray[i] := i + 1;
                            }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[],VoidType(),Block([],[For(Id("x"),IntLiteral(5),IntLiteral(2),False,CallStmt(Id("Sha"),Id("getString"),[])),CallStmt(Id("io"),Id("writeIntLn"),[Id("x")]),For(Id("i"),IntLiteral(1),IntLiteral(100),True,Block([],[CallStmt(Id("io"),Id("writeIntLn"),[Id("i")]),Assign(ArrayType(Id("i"),ClassType("Intarray")),BinaryOp("+",Id("i"),IntLiteral(1)))]))]))])]))    
        self.assertTrue(TestAST.test(input,expect,328))
    def test_simple_program29(self):
        input = """class abc {
                        int static getArea(length,width:float){
                            for x := 5 downto 2 do
                                io.writeIntLn(x);
                            for i := 1 to 100 do {
                                io.writeIntLn(i);
                                Intarray[i] := i + 1;
                            }
                            return a.getNumber(10);
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],IntType(),Block([],[For(Id("x"),IntLiteral(5),IntLiteral(2),False,CallStmt(Id("io"),Id("writeIntLn"),[Id("x")])),For(Id("i"),IntLiteral(1),IntLiteral(100),True,Block([],[CallStmt(Id("io"),Id("writeIntLn"),[Id("i")]),Assign(ArrayType(Id("i"),ClassType("Intarray")),BinaryOp("+",Id("i"),IntLiteral(1)))])),Return(CallStmt(Id("a"),Id("getNumber"),[IntLiteral(10)]))]))])]))    
        self.assertTrue(TestAST.test(input,expect,329))

    def test_simple_program30(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            b.getMax(a[5]);
                            for x := 5 downto 2 do
                                io.writeIntLn(x);
                            for i := 1 to 100 do {
                                io.writeIntLn(i);
                                Intarray[i] := i + 1;
                            }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[CallStmt(Id("b"),Id("getMax"),[ArrayCell(Id("a"),IntLiteral(5))]),For(Id("x"),IntLiteral(5),IntLiteral(2),False,CallStmt(Id("io"),Id("writeIntLn"),[Id("x")])),For(Id("i"),IntLiteral(1),IntLiteral(100),True,Block([],[CallStmt(Id("io"),Id("writeIntLn"),[Id("i")]),Assign(ArrayType(Id("i"),ClassType("Intarray")),BinaryOp("+",Id("i"),IntLiteral(1)))]))]))])]))    
        self.assertTrue(TestAST.test(input,expect,330))
    def test_simple_program30(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            b.getMax(a[5]);
                            for x := 5 downto 2 do
                                io.writeIntLn(x);
                            for i := 1 to 100 do {
                                io.writeIntLn(i);
                                Intarray[i] := i + 1;
                            }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[CallStmt(Id("b"),Id("getMax"),[ArrayCell(Id("a"),IntLiteral(5))]),For(Id("x"),IntLiteral(5),IntLiteral(2),False,CallStmt(Id("io"),Id("writeIntLn"),[Id("x")])),For(Id("i"),IntLiteral(1),IntLiteral(100),True,Block([],[CallStmt(Id("io"),Id("writeIntLn"),[Id("i")]),Assign(ArrayType(Id("i"),ClassType("Intarray")),BinaryOp("+",Id("i"),IntLiteral(1)))]))]))])]))    
        self.assertTrue(TestAST.test(input,expect,330))

    def test_simple_program31(self):
        input = """class abc {
                        int  Mouse(a,b : int){
                            b.getMax("anhmuonemsongsao");
                            return 0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("Mouse"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType())],IntType(),Block([],[CallStmt(Id("b"),Id("getMax"),[StringLiteral("anhmuonemsongsao")]),Return(IntLiteral(0))]))])]))    
        self.assertTrue(TestAST.test(input,expect,331))

    def test_simple_program32(self):
        input = """class abc {
                        int  Mouse(a,b : int){
                            b.getMax("anhmuonemsongsao", a + b / 10);
                            return 0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("Mouse"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType())],IntType(),Block([],[CallStmt(Id("b"),Id("getMax"),[StringLiteral("anhmuonemsongsao"),BinaryOp("+",Id("a"),BinaryOp("/",Id("b"),IntLiteral(10)))]),Return(IntLiteral(0))]))])]))    
        self.assertTrue(TestAST.test(input,expect,332))

    def test_simple_program33(self):
        input = """class abc {
                        int  Mouse(a,b : int){
                            b.getMax("nobody","anhmuonemsongsao");
                            return 0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("Mouse"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType())],IntType(),Block([],[CallStmt(Id("b"),Id("getMax"),[StringLiteral("nobody"),StringLiteral("anhmuonemsongsao")]),Return(IntLiteral(0))]))])]))    
        self.assertTrue(TestAST.test(input,expect,333))

    def test_simple_program34(self):
        input = """class abc {
                        int  Mouse(a,b : int){
                            b.getMax("anhmuonemsongsao","kietlac", a%10);
                            return 0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("Mouse"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType())],IntType(),Block([],[CallStmt(Id("b"),Id("getMax"),[StringLiteral("anhmuonemsongsao"),StringLiteral("kietlac"),BinaryOp("%",Id("a"),IntLiteral(10))]),Return(IntLiteral(0))]))])]))   
        self.assertTrue(TestAST.test(input,expect,334))

    def test_simple_program35(self):
        input = """class abc {
                        int  Mouse(a,b : int){
                            b.getMax(c.giet(), 10);
                            return 0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("Mouse"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType())],IntType(),Block([],[CallStmt(Id("b"),Id("getMax"),[CallStmt(Id("c"),Id("giet"),[]),IntLiteral(10)]),Return(IntLiteral(0))]))])]))   
        self.assertTrue(TestAST.test(input,expect,335))

    def test_simple_program36(self):
        input = """class abc {
                        int  Mouse(a,b : int){
                            b.getMax(b, -a);
                            return 0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("Mouse"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType())],IntType(),Block([],[CallStmt(Id("b"),Id("getMax"),[Id("b"),UnaryOp("-",Id("a"))]),Return(IntLiteral(0))]))])]))   
        self.assertTrue(TestAST.test(input,expect,336))

    def test_simple_program37(self):
        input = """class abc {
                        int  Mouse(a,b : int){
                            b.getMax(c.getT(e, a));
                            return 0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("Mouse"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType())],IntType(),Block([],[CallStmt(Id("b"),Id("getMax"),[CallStmt(Id("c"),Id("getT"),[Id("e"),Id("a")])]),Return(IntLiteral(0))]))])]))   
        self.assertTrue(TestAST.test(input,expect,337))

    def test_simple_program38(self):
        input = """class abc {
                        int  Mouse(a,b : int){
                            b.getMax("e", a*10/b);
                            return this.t;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("Mouse"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType())],IntType(),Block([],[CallStmt(Id("b"),Id("getMax"),[StringLiteral("e"),BinaryOp("/",BinaryOp("*",Id("a"),IntLiteral(10)),Id("b"))]),Return(FieldAccess(SelfLiteral(),Id("t")))]))])]))   
        self.assertTrue(TestAST.test(input,expect,338))

    def test_simple_program39(self):
        input = """class abc {
                        int  Cat(a,b : int){
                            b.getMax(Cat.e(), "anh");
                            return 0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("Cat"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType())],IntType(),Block([],[CallStmt(Id("b"),Id("getMax"),[CallStmt(Id("Cat"),Id("e"),[]),StringLiteral("anh")]),Return(IntLiteral(0))]))])]))   
        self.assertTrue(TestAST.test(input,expect,339))

    def test_simple_program40(self):
        input = """class abc {
                        int  Mouse(a,b : int){
                            b.getMax(-z, 10);
                            a := -temp;
                            return 0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("Mouse"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType())],IntType(),Block([],[CallStmt(Id("b"),Id("getMax"),[UnaryOp("-",Id("z")),IntLiteral(10)]),Assign(Id("a"),UnaryOp("-",Id("temp"))),Return(IntLiteral(0))]))])]))   
        self.assertTrue(TestAST.test(input,expect,340))

    def test_simple_program41(self):
        input = """class abc {
                        int  Mouse(a,b : int){
                            b.getMax(--z, 10);
                            return 0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("Mouse"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType())],IntType(),Block([],[CallStmt(Id("b"),Id("getMax"),[UnaryOp("-",UnaryOp("-",Id("z"))),IntLiteral(10)]),Return(IntLiteral(0))]))])]))   
        self.assertTrue(TestAST.test(input,expect,341))

    def test_simple_program42(self):
        input = """class abc {
                        int  Dog(a,b : int){
                            b.getMax(Cat.getName(), Mouse.getName());
                            return 0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("Dog"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType())],IntType(),Block([],[CallStmt(Id("b"),Id("getMax"),[CallStmt(Id("Cat"),Id("getName"),[]),CallStmt(Id("Mouse"),Id("getName"),[])]),Return(IntLiteral(0))]))])]))   
        self.assertTrue(TestAST.test(input,expect,342))

    def test_simple_program43(self):
        input = """class abc {
                        int  Mouse(a,b : int){
                            b.getMax(a[i], b[j], c[z]);
                            return 0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("Mouse"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType())],IntType(),Block([],[CallStmt(Id("b"),Id("getMax"),[ArrayCell(Id("a"),Id("i")),ArrayCell(Id("b"),Id("j")),ArrayCell(Id("c"),Id("z"))]),Return(IntLiteral(0))]))])]))

        self.assertTrue(TestAST.test(input,expect,343))

    def test_simple_program44(self):
        input = """class Example1 {
                    int factorial(n:int){
                        if n == 0 then return 1; 
                        else return n * this.factorial(n - 1);
                    }
                    void main(){
                        x:int;
                        x := io.readInt();
                        io.writeIntLn(this.factorial(x));
                    }
                }"""
        expect = str(Program([ClassDecl(Id("Example1"),[MethodDecl(Instance(),Id("factorial"),[VarDecl(Id("n"),IntType())],IntType(),Block([],[If(BinaryOp("==",Id("n"),IntLiteral(0)),Return(IntLiteral(1)),Return(BinaryOp("*",Id("n"),CallStmt(SelfLiteral(),Id("factorial"),[BinaryOp("-",Id("n"),IntLiteral(1))]))))])),MethodDecl(Instance(),Id("main"),[],VoidType(),Block([AttributeDecl(Instance(),VarDecl(Id("x"),IntType()))],[Assign(Id("x"),CallStmt(Id("io"),Id("readInt"),[])),CallStmt(Id("io"),Id("writeIntLn"),[CallStmt(SelfLiteral(),Id("factorial"),[Id("x")])])]))])]))

        self.assertTrue(TestAST.test(input,expect,344))

    def test_simple_program45(self):
        input = """class Example1 {
                    int factorial(n:int){
                        if n == 0 then return 1; 
                        else return n * this.factorial(n - 1);
                    }
                    void main(){
                        x:int;
                        x := io.read("Nhap vao");
                        x := io.readInt();
                        io.writeIntLn(this.factorial(x));
                    }
                }"""
        expect = str(Program([ClassDecl(Id("Example1"),[MethodDecl(Instance(),Id("factorial"),[VarDecl(Id("n"),IntType())],IntType(),Block([],[If(BinaryOp("==",Id("n"),IntLiteral(0)),Return(IntLiteral(1)),Return(BinaryOp("*",Id("n"),CallStmt(SelfLiteral(),Id("factorial"),[BinaryOp("-",Id("n"),IntLiteral(1))]))))])),MethodDecl(Instance(),Id("main"),[],VoidType(),Block([AttributeDecl(Instance(),VarDecl(Id("x"),IntType()))],[Assign(Id("x"),CallStmt(Id("io"),Id("read"),[StringLiteral("Nhap vao")])),Assign(Id("x"),CallStmt(Id("io"),Id("readInt"),[])),CallStmt(Id("io"),Id("writeIntLn"),[CallStmt(SelfLiteral(),Id("factorial"),[Id("x")])])]))])]))

        self.assertTrue(TestAST.test(input,expect,345))

    def test_simple_program46(self):
        input = """class Example1 {
                    int factorial(n:int){
                        if n == 0 then return 1; 
                        else return n * this.factorial(n - 1);
                        break;
                    }
                }"""
        expect = str(Program([ClassDecl(Id("Example1"),[MethodDecl(Instance(),Id("factorial"),[VarDecl(Id("n"),IntType())],IntType(),Block([],[If(BinaryOp("==",Id("n"),IntLiteral(0)),Return(IntLiteral(1)),Return(BinaryOp("*",Id("n"),CallStmt(SelfLiteral(),Id("factorial"),[BinaryOp("-",Id("n"),IntLiteral(1))])))),Break()]))])]))

        self.assertTrue(TestAST.test(input,expect,346))

    def test_simple_program47(self):
        input = """class Example1 {
                    int factorial(n:int){
                        if n * 1.6e-1 == 0 then return 1; 
                        else return n * this.factorial(n - 1);
                        break;
                    }
                }"""
        expect = str(Program([ClassDecl(Id("Example1"),[MethodDecl(Instance(),Id("factorial"),[VarDecl(Id("n"),IntType())],IntType(),Block([],[If(BinaryOp("==",BinaryOp("*",Id("n"),FloatLiteral(0.16)),IntLiteral(0)),Return(IntLiteral(1)),Return(BinaryOp("*",Id("n"),CallStmt(SelfLiteral(),Id("factorial"),[BinaryOp("-",Id("n"),IntLiteral(1))])))),Break()]))])]))

        self.assertTrue(TestAST.test(input,expect,347))

    def test_simple_program48(self):
        input = """class Rectangle extends Shape {
                        float getArea(){
                            return this.length*this.width;
                        }
                }"""
        expect = str(Program([ClassDecl(Id("Rectangle"),[MethodDecl(Instance(),Id("getArea"),[],FloatType(),Block([],[Return(BinaryOp("*",FieldAccess(SelfLiteral(),Id("length")),FieldAccess(SelfLiteral(),Id("width"))))]))],Id("Shape"))]))
        self.assertTrue(TestAST.test(input,expect,348))

    def test_simple_program49(self):
        input = """class Example2 {
                    void main(){
                        s:Shape;
                        s := new Rectangle(3,4);
                        io.writeFloatLn(s.getArea());
                        s := new Triangle(3,4);
                        io.writeFloatLn(s.getArea());
                    }
                }"""
        expect = str(Program([ClassDecl(Id("Example2"),[MethodDecl(Instance(),Id("main"),[],VoidType(),Block([AttributeDecl(Instance(),VarDecl(Id("s"),ClassType("Shape")))],[Assign(Id("s"),NewExpr(Id("Rectangle"),[IntLiteral(3),IntLiteral(4)])),CallStmt(Id("io"),Id("writeFloatLn"),[CallStmt(Id("s"),Id("getArea"),[])]),Assign(Id("s"),NewExpr(Id("Triangle"),[IntLiteral(3),IntLiteral(4)])),CallStmt(Id("io"),Id("writeFloatLn"),[CallStmt(Id("s"),Id("getArea"),[])])]))])]))
        self.assertTrue(TestAST.test(input,expect,349))

    def test_simple_program50(self):
        input = """class Shape {
                    length,width:float;
                    float getArea() {}
                    Shape(length,width:float){
                        this.length := length;
                        this.width := width;
                    }
                }"""
        expect = str(Program([ClassDecl(Id("Shape"),[AttributeDecl(Instance(),VarDecl(Id("length"),FloatType())),AttributeDecl(Instance(),VarDecl(Id("width"),FloatType())),MethodDecl(Instance(),Id("Shape"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[Assign(FieldAccess(SelfLiteral(),Id("length")),Id("length")),Assign(FieldAccess(SelfLiteral(),Id("width")),Id("width"))]))])]))
        self.assertTrue(TestAST.test(input,expect,350))
    def test_simple_program51(self):
        input = """class abc {
                        string static getArea(length,width:float){
                            for x := 5 + a.getT() downto 2 do
                                io.writeIntLn(x);
                            for i := 1 - b.getN() to 100 do {
                                io.writeIntLn(i);
                                Intarray[i] := i + 1;
                            }

                            return this.a;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],StringType(),Block([],[For(Id("x"),BinaryOp("+",IntLiteral(5),CallStmt(Id("a"),Id("getT"),[])),IntLiteral(2),False,CallStmt(Id("io"),Id("writeIntLn"),[Id("x")])),For(Id("i"),BinaryOp("-",IntLiteral(1),CallStmt(Id("b"),Id("getN"),[])),IntLiteral(100),True,Block([],[CallStmt(Id("io"),Id("writeIntLn"),[Id("i")]),Assign(ArrayType(Id("i"),ClassType("Intarray")),BinaryOp("+",Id("i"),IntLiteral(1)))])),Return(FieldAccess(SelfLiteral(),Id("a")))]))])]))    
        self.assertTrue(TestAST.test(input,expect,351))

    def test_simple_program52(self):
        input = """class abc {
                        string static getArea(length,width:float){
                            for x := 5*ee.g(a,b) downto 2 do
                                io.writeIntLn(x);
                            for i := 1 to 100 do {
                                io.writeIntLn(i);
                                Intarray[i] := i + 1;
                            }

                            return this.a;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],StringType(),Block([],[For(Id("x"),BinaryOp("*",IntLiteral(5),CallStmt(Id("ee"),Id("g"),[Id("a"),Id("b")])),IntLiteral(2),False,CallStmt(Id("io"),Id("writeIntLn"),[Id("x")])),For(Id("i"),IntLiteral(1),IntLiteral(100),True,Block([],[CallStmt(Id("io"),Id("writeIntLn"),[Id("i")]),Assign(ArrayType(Id("i"),ClassType("Intarray")),BinaryOp("+",Id("i"),IntLiteral(1)))])),Return(FieldAccess(SelfLiteral(),Id("a")))]))])]))    
        self.assertTrue(TestAST.test(input,expect,352))

    def test_simple_program53(self):
        input = """class abc {
                        int static getArea(length,width:float){
                            for x := 5 + b * 2 % 10 downto 2 do
                                io.writeIntLn(x);
                            for i := 1 to 100 do {
                                io.writeIntLn(i);
                                Intarray[i] := i + 1;
                            }

                            return this.a;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],IntType(),Block([],[For(Id("x"),BinaryOp("+",IntLiteral(5),BinaryOp("%",BinaryOp("*",Id("b"),IntLiteral(2)),IntLiteral(10))),IntLiteral(2),False,CallStmt(Id("io"),Id("writeIntLn"),[Id("x")])),For(Id("i"),IntLiteral(1),IntLiteral(100),True,Block([],[CallStmt(Id("io"),Id("writeIntLn"),[Id("i")]),Assign(ArrayType(Id("i"),ClassType("Intarray")),BinaryOp("+",Id("i"),IntLiteral(1)))])),Return(FieldAccess(SelfLiteral(),Id("a")))]))])]))    
        self.assertTrue(TestAST.test(input,expect,353))

    def test_simple_program54(self):
        input = """class abc {
                        float static getArea(length,width:float){
                            for x := 5 downto 2 do
                                io.writeIntLn(x);
                            for i := 1 - b to 100 do {
                                io.writeIntLn(i);
                                Intarray[i] := i + 1;
                                if a != 1 then
                                    return t;
                            }

                            return this.a;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],FloatType(),Block([],[For(Id("x"),IntLiteral(5),IntLiteral(2),False,CallStmt(Id("io"),Id("writeIntLn"),[Id("x")])),For(Id("i"),BinaryOp("-",IntLiteral(1),Id("b")),IntLiteral(100),True,Block([],[CallStmt(Id("io"),Id("writeIntLn"),[Id("i")]),Assign(ArrayType(Id("i"),ClassType("Intarray")),BinaryOp("+",Id("i"),IntLiteral(1))),If(BinaryOp("!=",Id("a"),IntLiteral(1)),Return(Id("t")))])),Return(FieldAccess(SelfLiteral(),Id("a")))]))])]))    
        self.assertTrue(TestAST.test(input,expect,354))

    def test_simple_program55(self):
        input = """class Example1 {
                    int factorial(n:int){
                        if n * 1.6e-1 == 0 then return 1; 
                        else return n * this.factorial(n - 1);
                        break;
                    }
                }"""
        expect = str(Program([ClassDecl(Id("Example1"),[MethodDecl(Instance(),Id("factorial"),[VarDecl(Id("n"),IntType())],IntType(),Block([],[If(BinaryOp("==",BinaryOp("*",Id("n"),FloatLiteral(0.16)),IntLiteral(0)),Return(IntLiteral(1)),Return(BinaryOp("*",Id("n"),CallStmt(SelfLiteral(),Id("factorial"),[BinaryOp("-",Id("n"),IntLiteral(1))])))),Break()]))])]))

        self.assertTrue(TestAST.test(input,expect,355))
    def test_simple_program56(self):
        input = """class Example1 {
                    int factorial(n:int){
                        if (n * 1.6e-1 == 0) || (a / 5 + 4) then return 1; 
                        else return n * this.factorial(n - 1);
                        break;
                    }
                }"""
        expect = str(Program([ClassDecl(Id("Example1"),[MethodDecl(Instance(),Id("factorial"),[VarDecl(Id("n"),IntType())],IntType(),Block([],[If(BinaryOp("||",BinaryOp("==",BinaryOp("*",Id("n"),FloatLiteral(0.16)),IntLiteral(0)),BinaryOp("+",BinaryOp("/",Id("a"),IntLiteral(5)),IntLiteral(4))),Return(IntLiteral(1)),Return(BinaryOp("*",Id("n"),CallStmt(SelfLiteral(),Id("factorial"),[BinaryOp("-",Id("n"),IntLiteral(1))])))),Break()]))])]))

        self.assertTrue(TestAST.test(input,expect,356))

    def test_simple_program57(self):
        input = """class Example1 {
                    int factorial(n:int){
                        if (n == 0 || k <= 4) && (m > 5) then return 1; 
                        else return n * this.factorial(n - 1);
                        break;
                    }
                }"""
        expect = str(Program([ClassDecl(Id("Example1"),[MethodDecl(Instance(),Id("factorial"),[VarDecl(Id("n"),IntType())],IntType(),Block([],[If(BinaryOp("&&",BinaryOp("<=",BinaryOp("==",Id("n"),BinaryOp("||",IntLiteral(0),Id("k"))),IntLiteral(4)),BinaryOp(">",Id("m"),IntLiteral(5))),Return(IntLiteral(1)),Return(BinaryOp("*",Id("n"),CallStmt(SelfLiteral(),Id("factorial"),[BinaryOp("-",Id("n"),IntLiteral(1))])))),Break()]))])]))

        self.assertTrue(TestAST.test(input,expect,357))

    def test_simple_program58(self):
        input = """class Example1 {
                    int factorial(n:int){
                        if n * 1.6e-1 == 0 || a < b + 34 then return 1; 
                        else return n * this.factorial(n - 1, "bae");
                        break;
                    }
                }"""
        expect = str(Program([ClassDecl(Id("Example1"),[MethodDecl(Instance(),Id("factorial"),[VarDecl(Id("n"),IntType())],IntType(),Block([],[If(BinaryOp("<",BinaryOp("==",BinaryOp("*",Id("n"),FloatLiteral(0.16)),BinaryOp("||",IntLiteral(0),Id("a"))),BinaryOp("+",Id("b"),IntLiteral(34))),Return(IntLiteral(1)),Return(BinaryOp("*",Id("n"),CallStmt(SelfLiteral(),Id("factorial"),[BinaryOp("-",Id("n"),IntLiteral(1)),StringLiteral("bae")])))),Break()]))])]))

        self.assertTrue(TestAST.test(input,expect,358))

    def test_simple_program59(self):
        input = """class Example1 {
                    int factorial(n:int){
                        if n * 1.6e-1 == 0 && (a - b == 2) then return 1; 
                        else return n * this.factorial(n - 1);
                        break;
                    }
                }"""
        expect = str(Program([ClassDecl(Id("Example1"),[MethodDecl(Instance(),Id("factorial"),[VarDecl(Id("n"),IntType())],IntType(),Block([],[If(BinaryOp("==",BinaryOp("*",Id("n"),FloatLiteral(0.16)),BinaryOp("&&",IntLiteral(0),BinaryOp("==",BinaryOp("-",Id("a"),Id("b")),IntLiteral(2)))),Return(IntLiteral(1)),Return(BinaryOp("*",Id("n"),CallStmt(SelfLiteral(),Id("factorial"),[BinaryOp("-",Id("n"),IntLiteral(1))])))),Break()]))])]))

        self.assertTrue(TestAST.test(input,expect,359))

    def test_simple_program60(self):
        input = """class Example1 {
                    int factorial(n:int){
                        if n * 1.6e-1 == 0 then return 1; 
                        else return n.get("hahahh") * this.factorial(n - 1);
                        break;
                    }
                }"""
        expect = str(Program([ClassDecl(Id("Example1"),[MethodDecl(Instance(),Id("factorial"),[VarDecl(Id("n"),IntType())],IntType(),Block([],[If(BinaryOp("==",BinaryOp("*",Id("n"),FloatLiteral(0.16)),IntLiteral(0)),Return(IntLiteral(1)),Return(BinaryOp("*",CallStmt(Id("n"),Id("get"),[StringLiteral("hahahh")]),CallStmt(SelfLiteral(),Id("factorial"),[BinaryOp("-",Id("n"),IntLiteral(1))])))),Break()]))])]))

        self.assertTrue(TestAST.test(input,expect,360))

    def test_simple_program61(self):
        input = """class Example1 {
                    int factorial(n:int){
                        if n * 1.6e-1 == 0 && (!a - !b == 2) then return 1; 
                        else return n * this.factorial(n - 1);
                        break;
                    }
                }"""
        expect = str(Program([ClassDecl(Id("Example1"),[MethodDecl(Instance(),Id("factorial"),[VarDecl(Id("n"),IntType())],IntType(),Block([],[If(BinaryOp("==",BinaryOp("*",Id("n"),FloatLiteral(0.16)),BinaryOp("&&",IntLiteral(0),BinaryOp("==",BinaryOp("-",UnaryOp("!",Id("a")),UnaryOp("!",Id("b"))),IntLiteral(2)))),Return(IntLiteral(1)),Return(BinaryOp("*",Id("n"),CallStmt(SelfLiteral(),Id("factorial"),[BinaryOp("-",Id("n"),IntLiteral(1))])))),Break()]))])]))

        self.assertTrue(TestAST.test(input,expect,361))

    def test_simple_program62(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            {
                                this.length := length;
                                this.length := ! length;
                            }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[Block([],[Assign(FieldAccess(SelfLiteral(),Id("length")),Id("length")),Assign(FieldAccess(SelfLiteral(),Id("length")),UnaryOp("!",Id("length")))])]))])]))    
        self.assertTrue(TestAST.test(input,expect,362))

    def test_simple_program63(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            {
                                this.length := length;
                                this.length := ! length;
                                a := a + [a + 1];
                                return a;
                                
                            }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[Block([],[Assign(FieldAccess(SelfLiteral(),Id("length")),Id("length")),Assign(FieldAccess(SelfLiteral(),Id("length")),UnaryOp("!",Id("length"))),Assign(Id("a"),BinaryOp("+",Id("a"),BinaryOp("+",Id("a"),IntLiteral(1)))),Return(Id("a"))])]))])]))    
        self.assertTrue(TestAST.test(input,expect,363))

    def test_simple_program64(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            {
                                this.length := length;
                                this.length := ! length;
                                a := a + [a + Mouse.get()];
                                return a;
                                
                            }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[Block([],[Assign(FieldAccess(SelfLiteral(),Id("length")),Id("length")),Assign(FieldAccess(SelfLiteral(),Id("length")),UnaryOp("!",Id("length"))),Assign(Id("a"),BinaryOp("+",Id("a"),BinaryOp("+",Id("a"),CallStmt(Id("Mouse"),Id("get"),[])))),Return(Id("a"))])]))])]))    
        self.assertTrue(TestAST.test(input,expect,364))

    def test_simple_program65(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            {
                                this.length := length;
                                this.length := ! length;
                                a := a + [a + b % 10];
                                return a;
                                
                            }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[Block([],[Assign(FieldAccess(SelfLiteral(),Id("length")),Id("length")),Assign(FieldAccess(SelfLiteral(),Id("length")),UnaryOp("!",Id("length"))),Assign(Id("a"),BinaryOp("+",Id("a"),BinaryOp("+",Id("a"),BinaryOp("%",Id("b"),IntLiteral(10))))),Return(Id("a"))])]))])]))    
        self.assertTrue(TestAST.test(input,expect,365))

    def test_simple_program66(self):
        input = """class abc {
                        void getArea(a, b, c, d:string){
                            {
                                this.length := length;
                                this.length := ! length;
                                a := a + [a + b % 10];
                                if(a == b) then
                                    io.write("ABC");
                                return a;
                                
                            }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("getArea"),[VarDecl(Id("a"),StringType()),VarDecl(Id("b"),StringType()),VarDecl(Id("c"),StringType()),VarDecl(Id("d"),StringType())],VoidType(),Block([],[Block([],[Assign(FieldAccess(SelfLiteral(),Id("length")),Id("length")),Assign(FieldAccess(SelfLiteral(),Id("length")),UnaryOp("!",Id("length"))),Assign(Id("a"),BinaryOp("+",Id("a"),BinaryOp("+",Id("a"),BinaryOp("%",Id("b"),IntLiteral(10))))),If(BinaryOp("==",Id("a"),Id("b")),CallStmt(Id("io"),Id("write"),[StringLiteral("ABC")])),Return(Id("a"))])]))])]))    
        self.assertTrue(TestAST.test(input,expect,366))

    def test_simple_program67(self):
        input = """class abc {
                        void getArea(a, b, c, d:string){
                            {
                                this.length := -length;
                                this.length := !length;
                                a := a + [a + b % 10];
                                if(a == b) then
                                    io.write("ABC");
                                return a;
                                
                            }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("getArea"),[VarDecl(Id("a"),StringType()),VarDecl(Id("b"),StringType()),VarDecl(Id("c"),StringType()),VarDecl(Id("d"),StringType())],VoidType(),Block([],[Block([],[Assign(FieldAccess(SelfLiteral(),Id("length")),UnaryOp("-",Id("length"))),Assign(FieldAccess(SelfLiteral(),Id("length")),UnaryOp("!",Id("length"))),Assign(Id("a"),BinaryOp("+",Id("a"),BinaryOp("+",Id("a"),BinaryOp("%",Id("b"),IntLiteral(10))))),If(BinaryOp("==",Id("a"),Id("b")),CallStmt(Id("io"),Id("write"),[StringLiteral("ABC")])),Return(Id("a"))])]))])]))    
        self.assertTrue(TestAST.test(input,expect,367))

    def test_simple_program68(self):
        input = """class abc {
                        void getArea(a, b, c, d:string){
                            {
                                this.length := length;
                                this.length := ! length;
                                a := a + [a + b % 10];
                                if(a == b) then
                                    io.write("ABC");
                                else
                                    io.read();
                                return a*a*b-5;
                                
                            }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("getArea"),[VarDecl(Id("a"),StringType()),VarDecl(Id("b"),StringType()),VarDecl(Id("c"),StringType()),VarDecl(Id("d"),StringType())],VoidType(),Block([],[Block([],[Assign(FieldAccess(SelfLiteral(),Id("length")),Id("length")),Assign(FieldAccess(SelfLiteral(),Id("length")),UnaryOp("!",Id("length"))),Assign(Id("a"),BinaryOp("+",Id("a"),BinaryOp("+",Id("a"),BinaryOp("%",Id("b"),IntLiteral(10))))),If(BinaryOp("==",Id("a"),Id("b")),CallStmt(Id("io"),Id("write"),[StringLiteral("ABC")]),CallStmt(Id("io"),Id("read"),[])),Return(BinaryOp("-",BinaryOp("*",BinaryOp("*",Id("a"),Id("a")),Id("b")),IntLiteral(5)))])]))])]))    
        self.assertTrue(TestAST.test(input,expect,368))

    def test_simple_program69(self):
        input = """class abc {
                        void getArea(a, b, c, d:string){
                            {
                                this.length := length;
                                this.length := ! length;
                                a := a + [a + b % 10];
                                if(a == b) then
                                    io.write("ABC");
                                    for a := 1*b.get("length") to 100 do
                                        tong := tong + 1;
                                return tong;
                                
                            }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("getArea"),[VarDecl(Id("a"),StringType()),VarDecl(Id("b"),StringType()),VarDecl(Id("c"),StringType()),VarDecl(Id("d"),StringType())],VoidType(),Block([],[Block([],[Assign(FieldAccess(SelfLiteral(),Id("length")),Id("length")),Assign(FieldAccess(SelfLiteral(),Id("length")),UnaryOp("!",Id("length"))),Assign(Id("a"),BinaryOp("+",Id("a"),BinaryOp("+",Id("a"),BinaryOp("%",Id("b"),IntLiteral(10))))),If(BinaryOp("==",Id("a"),Id("b")),CallStmt(Id("io"),Id("write"),[StringLiteral("ABC")])),For(Id("a"),BinaryOp("*",IntLiteral(1),CallStmt(Id("b"),Id("get"),[StringLiteral("length")])),IntLiteral(100),True,Assign(Id("tong"),BinaryOp("+",Id("tong"),IntLiteral(1)))),Return(Id("tong"))])]))])]))    
        self.assertTrue(TestAST.test(input,expect,369))

    def test_simple_program70(self):
        input = """class abc {
                        void getArea(a, b, c, d:string){
                            {
                                this.length := length;
                                this.length := ! length;
                                a := a + [a + b % 10];
                                if(a == b) then
                                    io.write("ABC");
                                    break;
                                return a;
                                
                            }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Instance(),Id("getArea"),[VarDecl(Id("a"),StringType()),VarDecl(Id("b"),StringType()),VarDecl(Id("c"),StringType()),VarDecl(Id("d"),StringType())],VoidType(),Block([],[Block([],[Assign(FieldAccess(SelfLiteral(),Id("length")),Id("length")),Assign(FieldAccess(SelfLiteral(),Id("length")),UnaryOp("!",Id("length"))),Assign(Id("a"),BinaryOp("+",Id("a"),BinaryOp("+",Id("a"),BinaryOp("%",Id("b"),IntLiteral(10))))),If(BinaryOp("==",Id("a"),Id("b")),CallStmt(Id("io"),Id("write"),[StringLiteral("ABC")])),Break(),Return(Id("a"))])]))])]))    
        self.assertTrue(TestAST.test(input,expect,370))

    def test_simple_program71(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            if a == 1 then
                                io.write("Suy nua thi");
                                if b < 0 then
                                    b := c + 3;
                                else
                                    b[1] := a.get().length;

                                this.valid := a;

                            return temp;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[If(BinaryOp("==",Id("a"),IntLiteral(1)),CallStmt(Id("io"),Id("write"),[StringLiteral("Suy nua thi")])),If(BinaryOp("<",Id("b"),IntLiteral(0)),Assign(Id("b"),BinaryOp("+",Id("c"),IntLiteral(3))),Assign(ArrayType(1,ClassType("b")),BinaryOp(".",Id("a"),CallExpr(Id("get"),Id("length"),[])))),Assign(FieldAccess(SelfLiteral(),Id("valid")),Id("a")),Return(Id("temp"))]))])]))
        self.assertTrue(TestAST.test(input,expect,371))
    def test_simple_program72(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            if a == 1 then
                                io.write("Suy nua thi");
                                if b < 0 then
                                    b := c + 3;
                                else
                                    b[1] := a;
                                for x := 5 downto 2 do
                                    io.writeIntLn(x);
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[If(BinaryOp("==",Id("a"),IntLiteral(1)),CallStmt(Id("io"),Id("write"),[StringLiteral("Suy nua thi")])),If(BinaryOp("<",Id("b"),IntLiteral(0)),Assign(Id("b"),BinaryOp("+",Id("c"),IntLiteral(3))),Assign(ArrayType(1,ClassType("b")),Id("a"))),For(Id("x"),IntLiteral(5),IntLiteral(2),False,CallStmt(Id("io"),Id("writeIntLn"),[Id("x")]))]))])]))    
        self.assertTrue(TestAST.test(input,expect,372))


    def test_simple_program73(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            if a == 1 then
                                io.write("Suy nua thi");
                                if b < 0 then
                                    b := c + 3;
                                else
                                    b[1] := a;
                                    for i := 1 to 100 do {
                                        io.writeIntLn(i);
                                        Intarray[i] := i + 1;
                                    }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[If(BinaryOp("==",Id("a"),IntLiteral(1)),CallStmt(Id("io"),Id("write"),[StringLiteral("Suy nua thi")])),If(BinaryOp("<",Id("b"),IntLiteral(0)),Assign(Id("b"),BinaryOp("+",Id("c"),IntLiteral(3))),Assign(ArrayType(1,ClassType("b")),Id("a"))),For(Id("i"),IntLiteral(1),IntLiteral(100),True,Block([],[CallStmt(Id("io"),Id("writeIntLn"),[Id("i")]),Assign(ArrayType(Id("i"),ClassType("Intarray")),BinaryOp("+",Id("i"),IntLiteral(1)))]))]))])]))    
        self.assertTrue(TestAST.test(input,expect,373))
    def test_simple_program74(self):
        input = """class abc {
                        string static getArea(length,width:float){
                            if a == 1 then
                                io.write("Suy nua thi");
                                if b < 0 then
                                {   b := c + 3;
                                    c := Shape.Ten().ten;
                                }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],StringType(),Block([],[If(BinaryOp("==",Id("a"),IntLiteral(1)),CallStmt(Id("io"),Id("write"),[StringLiteral("Suy nua thi")])),If(BinaryOp("<",Id("b"),IntLiteral(0)),Block([],[Assign(Id("b"),BinaryOp("+",Id("c"),IntLiteral(3))),Assign(Id("c"),BinaryOp(".",Id("Shape"),CallExpr(Id("Ten"),Id("ten"),[])))]))]))])]))    
        self.assertTrue(TestAST.test(input,expect,374))
    def test_simple_program75(self):
        input = """class abc {
                        void static getArea(length,width:float){
                            if a == 1 then
                                io.write("Suy nua thi");
                                if b < 0 then
                                    b := c.get("Mouse") + 3 - c.get("Cat");
                                else
                                    b[1] := a;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([],[If(BinaryOp("==",Id("a"),IntLiteral(1)),CallStmt(Id("io"),Id("write"),[StringLiteral("Suy nua thi")])),If(BinaryOp("<",Id("b"),IntLiteral(0)),Assign(Id("b"),BinaryOp("-",BinaryOp("+",CallStmt(Id("c"),Id("get"),[StringLiteral("Mouse")]),IntLiteral(3)),CallStmt(Id("c"),Id("get"),[StringLiteral("Cat")]))),Assign(ArrayType(1,ClassType("b")),Id("a")))]))])]))    
        self.assertTrue(TestAST.test(input,expect,375))
    def test_simple_program76(self):
        input = """class Example2 {
                    void main(){
                        s:Shape;
                        s := new Rectangle("et",4);
                        io.writeFloatLn(s.getArea());
                        s := new Triangle(3,4);
                        io.writeFloatLn(s.getArea());
                    }
                }"""
        expect = str(Program([ClassDecl(Id("Example2"),[MethodDecl(Instance(),Id("main"),[],VoidType(),Block([AttributeDecl(Instance(),VarDecl(Id("s"),ClassType("Shape")))],[Assign(Id("s"),NewExpr(Id("Rectangle"),[StringLiteral("et"),IntLiteral(4)])),CallStmt(Id("io"),Id("writeFloatLn"),[CallStmt(Id("s"),Id("getArea"),[])]),Assign(Id("s"),NewExpr(Id("Triangle"),[IntLiteral(3),IntLiteral(4)])),CallStmt(Id("io"),Id("writeFloatLn"),[CallStmt(Id("s"),Id("getArea"),[])])]))])]))
        self.assertTrue(TestAST.test(input,expect,376))
    def test_simple_program77(self):
        input = """class Example2 {
                    void main(){
                        s:Shape;
                        s := new Rectangle(3,4, 0);
                        io.writeFloatLn(s.getArea());
                        this.B := new Triangle(3,4, "TAnv");
                        io.writeFloatLn(s.getArea());
                    }
                }"""
        expect = str(Program([ClassDecl(Id("Example2"),[MethodDecl(Instance(),Id("main"),[],VoidType(),Block([AttributeDecl(Instance(),VarDecl(Id("s"),ClassType("Shape")))],[Assign(Id("s"),NewExpr(Id("Rectangle"),[IntLiteral(3),IntLiteral(4),IntLiteral(0)])),CallStmt(Id("io"),Id("writeFloatLn"),[CallStmt(Id("s"),Id("getArea"),[])]),Assign(FieldAccess(SelfLiteral(),Id("B")),NewExpr(Id("Triangle"),[IntLiteral(3),IntLiteral(4),StringLiteral("TAnv")])),CallStmt(Id("io"),Id("writeFloatLn"),[CallStmt(Id("s"),Id("getArea"),[])])]))])]))
        self.assertTrue(TestAST.test(input,expect,377))
    def test_simple_program78(self):
        input = """class Example2 {
                    void main(){
                        s:Shape;
                        s := new Rectangle(r.getVa(),4);
                        io.writeFloatLn(s.getArea());
                        s := new Triangle(3,4);
                        io.writeFloatLn(s.getArea());
                    }
                }"""
        expect = str(Program([ClassDecl(Id("Example2"),[MethodDecl(Instance(),Id("main"),[],VoidType(),Block([AttributeDecl(Instance(),VarDecl(Id("s"),ClassType("Shape")))],[Assign(Id("s"),NewExpr(Id("Rectangle"),[CallStmt(Id("r"),Id("getVa"),[]),IntLiteral(4)])),CallStmt(Id("io"),Id("writeFloatLn"),[CallStmt(Id("s"),Id("getArea"),[])]),Assign(Id("s"),NewExpr(Id("Triangle"),[IntLiteral(3),IntLiteral(4)])),CallStmt(Id("io"),Id("writeFloatLn"),[CallStmt(Id("s"),Id("getArea"),[])])]))])]))
        self.assertTrue(TestAST.test(input,expect,378))
    def test_simple_program79(self):
        input = """class Example2 {
                    void main(){
                        s:Shape;
                        s := new Rectangle(3,4,Mouse.get("Anh"));
                        io.writeFloatLn(s.getArea());
                        s := new Triangle(3,4);
                        io.writeFloatLn(s.getArea());
                    }
                }"""
        expect = str(Program([ClassDecl(Id("Example2"),[MethodDecl(Instance(),Id("main"),[],VoidType(),Block([AttributeDecl(Instance(),VarDecl(Id("s"),ClassType("Shape")))],[Assign(Id("s"),NewExpr(Id("Rectangle"),[IntLiteral(3),IntLiteral(4),CallStmt(Id("Mouse"),Id("get"),[StringLiteral("Anh")])])),CallStmt(Id("io"),Id("writeFloatLn"),[CallStmt(Id("s"),Id("getArea"),[])]),Assign(Id("s"),NewExpr(Id("Triangle"),[IntLiteral(3),IntLiteral(4)])),CallStmt(Id("io"),Id("writeFloatLn"),[CallStmt(Id("s"),Id("getArea"),[])])]))])]))
        self.assertTrue(TestAST.test(input,expect,379))
    def test_simple_program80(self):
        input = """class Example2 {
                    void main(){
                        s:Shape;
                        s := new Rectangle(b, e, f);
                        io.writeFloatLn(s.getArea());
                        s := new Triangle();
                        io.writeFloatLn(s.getArea());
                    }
                }"""
        expect = str(Program([ClassDecl(Id("Example2"),[MethodDecl(Instance(),Id("main"),[],VoidType(),Block([AttributeDecl(Instance(),VarDecl(Id("s"),ClassType("Shape")))],[Assign(Id("s"),NewExpr(Id("Rectangle"),[Id("b"),Id("e"),Id("f")])),CallStmt(Id("io"),Id("writeFloatLn"),[CallStmt(Id("s"),Id("getArea"),[])]),Assign(Id("s"),NewExpr(Id("Triangle"),[])),CallStmt(Id("io"),Id("writeFloatLn"),[CallStmt(Id("s"),Id("getArea"),[])])]))])]))
        self.assertTrue(TestAST.test(input,expect,380))
    def test_simple_program81(self):
        input = """class Shape {
                        void static getArea(a, b, c: int){
                            if (a < (b - c)) then
                                return a;
                            return this.length*this.width;
                        }
                    }
                    class abc {
                        my1stVar: int;
                        myArrayVar: int[5];
                        static my2ndVar, my3rdVar: Shape;
                        static my2ndArray, my3rdArray: Shape[6];
                    }"""
        expect = str(Program([ClassDecl(Id("Shape"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType()),VarDecl(Id("c"),IntType())],VoidType(),Block([],[If(BinaryOp("<",Id("a"),BinaryOp("-",Id("b"),Id("c"))),Return(Id("a"))),Return(BinaryOp("*",FieldAccess(SelfLiteral(),Id("length")),FieldAccess(SelfLiteral(),Id("width"))))]))]),ClassDecl(Id("abc"),[AttributeDecl(Instance(),VarDecl(Id("my1stVar"),IntType())),AttributeDecl(Instance(),VarDecl(Id("myArrayVar"),ArrayType(5,IntType()))),AttributeDecl(Static(),VarDecl(Id("my2ndVar"),ClassType("Shape"))),AttributeDecl(Static(),VarDecl(Id("my3rdVar"),ClassType("Shape"))),AttributeDecl(Static(),VarDecl(Id("my2ndArray"),ArrayType(6,ClassType("Shape")))),AttributeDecl(Static(),VarDecl(Id("my3rdArray"),ArrayType(6,ClassType("Shape"))))])])) 
        self.assertTrue(TestAST.test(input,expect,381))

    def test_simple_program82(self):
        input = """class Shape {
                        void static getArea(a, b, c: int){
                            my1stVar := 10000;
                            return this.length*this.width;
                        }
                    }
                    class abc {
                        my1stVar: int;
                        myArrayVar: int[5];
                        static my2ndVar, my3rdVar: Shape;
                        static my2ndArray, my3rdArray: Shape[6];
                    }"""
        expect = str(Program([ClassDecl(Id("Shape"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("a"),IntType()),VarDecl(Id("b"),IntType()),VarDecl(Id("c"),IntType())],VoidType(),Block([],[Assign(Id("my1stVar"),IntLiteral(10000)),Return(BinaryOp("*",FieldAccess(SelfLiteral(),Id("length")),FieldAccess(SelfLiteral(),Id("width"))))]))]),ClassDecl(Id("abc"),[AttributeDecl(Instance(),VarDecl(Id("my1stVar"),IntType())),AttributeDecl(Instance(),VarDecl(Id("myArrayVar"),ArrayType(5,IntType()))),AttributeDecl(Static(),VarDecl(Id("my2ndVar"),ClassType("Shape"))),AttributeDecl(Static(),VarDecl(Id("my3rdVar"),ClassType("Shape"))),AttributeDecl(Static(),VarDecl(Id("my2ndArray"),ArrayType(6,ClassType("Shape")))),AttributeDecl(Static(),VarDecl(Id("my3rdArray"),ArrayType(6,ClassType("Shape"))))])])) 
        self.assertTrue(TestAST.test(input,expect,382))

    def test_simple_program83(self):
        input = """class abc {
                        void static getArea(length,width:float){
                                %%start of declaration part
                                r,s:float;
                                a,b:string[5];
                                %%list of statements
                                r := this.length ;
                                s:=r*r*this.myPI;
                                a[0]:= 2.0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([AttributeDecl(Instance(),VarDecl(Id("r"),FloatType())),AttributeDecl(Instance(),VarDecl(Id("s"),FloatType())),AttributeDecl(Instance(),VarDecl(Id("a"),ArrayType(5,StringType()))),AttributeDecl(Instance(),VarDecl(Id("b"),ArrayType(5,StringType())))],[Assign(Id("r"),FieldAccess(SelfLiteral(),Id("length"))),Assign(Id("s"),BinaryOp("*",BinaryOp("*",Id("r"),Id("r")),FieldAccess(SelfLiteral(),Id("myPI")))),Assign(ArrayType(0,ClassType("a")),FloatLiteral(2.0))]))])]))    
        self.assertTrue(TestAST.test(input,expect,383))

    def test_simple_program84(self):
        input = """class abc {
                        void static getArea(length,width:float){
                                %%start of declaration part
                                r,s:float;
                                a,b:int[5];
                                %%list of statements
                                r := r ;
                                s:=r*r*this.myPI("Ne", a);
                                a[0]:= 2.0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([AttributeDecl(Instance(),VarDecl(Id("r"),FloatType())),AttributeDecl(Instance(),VarDecl(Id("s"),FloatType())),AttributeDecl(Instance(),VarDecl(Id("a"),ArrayType(5,IntType()))),AttributeDecl(Instance(),VarDecl(Id("b"),ArrayType(5,IntType())))],[Assign(Id("r"),Id("r")),Assign(Id("s"),BinaryOp("*",BinaryOp("*",Id("r"),Id("r")),CallStmt(SelfLiteral(),Id("myPI"),[StringLiteral("Ne"),Id("a")]))),Assign(ArrayType(0,ClassType("a")),FloatLiteral(2.0))]))])]))    
        self.assertTrue(TestAST.test(input,expect,384))


    def test_simple_program85(self):
        input = """class abc {
                        void static getArea(length,width:float){
                                %%start of declaration part
                                r,s:float;
                                a,b:int[5];
                                %%list of statements
                                r := r ;
                                s:=r*r*this.myPI;
                                a[0]:= 2.0;

                                return this.length;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([AttributeDecl(Instance(),VarDecl(Id("r"),FloatType())),AttributeDecl(Instance(),VarDecl(Id("s"),FloatType())),AttributeDecl(Instance(),VarDecl(Id("a"),ArrayType(5,IntType()))),AttributeDecl(Instance(),VarDecl(Id("b"),ArrayType(5,IntType())))],[Assign(Id("r"),Id("r")),Assign(Id("s"),BinaryOp("*",BinaryOp("*",Id("r"),Id("r")),FieldAccess(SelfLiteral(),Id("myPI")))),Assign(ArrayType(0,ClassType("a")),FloatLiteral(2.0)),Return(FieldAccess(SelfLiteral(),Id("length")))]))])]))    
        self.assertTrue(TestAST.test(input,expect,385))

    def test_simple_program86(self):
        input = """class abc {
                        void static getArea(length,width:float){
                                %%start of declaration part
                                r,s:string;
                                a,b:int[5];
                                %%list of statements
                                r := r ;
                                s:=r*r*this.myPI;
                                a[0]:= 2.0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([AttributeDecl(Instance(),VarDecl(Id("r"),StringType())),AttributeDecl(Instance(),VarDecl(Id("s"),StringType())),AttributeDecl(Instance(),VarDecl(Id("a"),ArrayType(5,IntType()))),AttributeDecl(Instance(),VarDecl(Id("b"),ArrayType(5,IntType())))],[Assign(Id("r"),Id("r")),Assign(Id("s"),BinaryOp("*",BinaryOp("*",Id("r"),Id("r")),FieldAccess(SelfLiteral(),Id("myPI")))),Assign(ArrayType(0,ClassType("a")),FloatLiteral(2.0))]))])]))    
        self.assertTrue(TestAST.test(input,expect,386))

    def test_simple_program87(self):
        input = """class abc {
                        void static getArea(length,width:float){
                                %%start of declaration part
                                r,s:float;
                                a,b:int[5];
                                %%list of statements
                                r := r ;
                                s:=r*r*this.myPI % 10;
                                a[0]:= 2.0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("length"),FloatType()),VarDecl(Id("width"),FloatType())],VoidType(),Block([AttributeDecl(Instance(),VarDecl(Id("r"),FloatType())),AttributeDecl(Instance(),VarDecl(Id("s"),FloatType())),AttributeDecl(Instance(),VarDecl(Id("a"),ArrayType(5,IntType()))),AttributeDecl(Instance(),VarDecl(Id("b"),ArrayType(5,IntType())))],[Assign(Id("r"),Id("r")),Assign(Id("s"),BinaryOp("%",BinaryOp("*",BinaryOp("*",Id("r"),Id("r")),FieldAccess(SelfLiteral(),Id("myPI"))),IntLiteral(10))),Assign(ArrayType(0,ClassType("a")),FloatLiteral(2.0))]))])]))    
        self.assertTrue(TestAST.test(input,expect,387))

    def test_simple_program88(self):
        input = """class abc {
                        float static getArea(a,b,c:string){
                            for x := 5 downto 2 do
                                Sha.getString();
                                io.writeIntLn(x);
                            for i := 1 to 100 do {
                                io.writeIntLn(i);
                                Intarray[i] := i + 1;
                                a := 5;
                            }

                            return 0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[VarDecl(Id("a"),StringType()),VarDecl(Id("b"),StringType()),VarDecl(Id("c"),StringType())],FloatType(),Block([],[For(Id("x"),IntLiteral(5),IntLiteral(2),False,CallStmt(Id("Sha"),Id("getString"),[])),CallStmt(Id("io"),Id("writeIntLn"),[Id("x")]),For(Id("i"),IntLiteral(1),IntLiteral(100),True,Block([],[CallStmt(Id("io"),Id("writeIntLn"),[Id("i")]),Assign(ArrayType(Id("i"),ClassType("Intarray")),BinaryOp("+",Id("i"),IntLiteral(1))),Assign(Id("a"),IntLiteral(5))])),Return(IntLiteral(0))]))])]))    
        self.assertTrue(TestAST.test(input,expect,388))

    def test_simple_program89(self):
        input = """class abc {
                        void static getArea(){
                            for x := 5 downto 2 do
                                Sha.getString();
                                io.writeIntLn(x);
                            for i := 1 to 100 do {
                                io.writeIntLn(i);
                                Intarray[i] := i + 1;
                                if (i == 10) then
                                    a := 3;
                                    continue;
                            }
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("abc"),[MethodDecl(Static(),Id("getArea"),[],VoidType(),Block([],[For(Id("x"),IntLiteral(5),IntLiteral(2),False,CallStmt(Id("Sha"),Id("getString"),[])),CallStmt(Id("io"),Id("writeIntLn"),[Id("x")]),For(Id("i"),IntLiteral(1),IntLiteral(100),True,Block([],[CallStmt(Id("io"),Id("writeIntLn"),[Id("i")]),Assign(ArrayType(Id("i"),ClassType("Intarray")),BinaryOp("+",Id("i"),IntLiteral(1))),If(BinaryOp("==",Id("i"),IntLiteral(10)),Assign(Id("a"),IntLiteral(3))),Continue()]))]))])]))    
        self.assertTrue(TestAST.test(input,expect,389))

    def test_simple_program90(self):
        input = """class Shape {
                        float getArea(){
                            a := "b";
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("Shape"),[MethodDecl(Instance(),Id("getArea"),[],FloatType(),Block([],[Assign(Id("a"),StringLiteral("b"))]))])]))
        self.assertTrue(TestAST.test(input,expect,390))

    def test_simple_program91(self):
        input = """class Shape {
                        float getArea(){
                            a := 3 - this.N;
                            return a % 10;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("Shape"),[MethodDecl(Instance(),Id("getArea"),[],FloatType(),Block([],[Assign(Id("a"),BinaryOp("-",IntLiteral(3),FieldAccess(SelfLiteral(),Id("N")))),Return(BinaryOp("%",Id("a"),IntLiteral(10)))]))])]))
        self.assertTrue(TestAST.test(input,expect,391))

    def test_simple_program92(self):
        input = """class Shape {
                        float getArea(abc, c: int){
                            if(c == 1 && (abc < 1)) then return 0;
                            tong := tong*abc + 1;
                            return this.getArea(abc/2, c-1);
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("Shape"),[MethodDecl(Instance(),Id("getArea"),[VarDecl(Id("abc"),IntType()),VarDecl(Id("c"),IntType())],FloatType(),Block([],[If(BinaryOp("==",Id("c"),BinaryOp("&&",IntLiteral(1),BinaryOp("<",Id("abc"),IntLiteral(1)))),Return(IntLiteral(0))),Assign(Id("tong"),BinaryOp("+",BinaryOp("*",Id("tong"),Id("abc")),IntLiteral(1))),Return(CallStmt(SelfLiteral(),Id("getArea"),[BinaryOp("/",Id("abc"),IntLiteral(2)),BinaryOp("-",Id("c"),IntLiteral(1))]))]))])]))
        self.assertTrue(TestAST.test(input,expect,392))

    def test_simple_program93(self):
        input = """class Shape {
                        float getArea(){
                            this.Temp := 10;
                            return this.Temp;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("Shape"),[MethodDecl(Instance(),Id("getArea"),[],FloatType(),Block([],[Assign(FieldAccess(SelfLiteral(),Id("Temp")),IntLiteral(10)),Return(FieldAccess(SelfLiteral(),Id("Temp")))]))])]))
        self.assertTrue(TestAST.test(input,expect,393))

    def test_simple_program94(self):
        input = """class Shape {
                        float getArea(){
                            this.getName := this.B;
                            return 0;
                        }
                    }"""
        expect = str(Program([ClassDecl(Id("Shape"),[MethodDecl(Instance(),Id("getArea"),[],FloatType(),Block([],[Assign(FieldAccess(SelfLiteral(),Id("getName")),FieldAccess(SelfLiteral(),Id("B"))),Return(IntLiteral(0))]))])]))
        self.assertTrue(TestAST.test(input,expect,394))
    def test_simple_program94(self):
        input = """class Shape {
                    s := new A(new B(new C()));
                    }"""
        expect = str(Program([ClassDecl(Id("Shape"),[MethodDecl(Instance(),Id("getArea"),[],FloatType(),Block([],[Assign(FieldAccess(SelfLiteral(),Id("getName")),FieldAccess(SelfLiteral(),Id("B"))),Return(IntLiteral(0))]))])]))
        self.assertTrue(TestAST.test(input,expect,394))
