// Generated from main/bkool/parser/BKOOL.g4 by ANTLR 4.7.1
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link BKOOLParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface BKOOLVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link BKOOLParser#program}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProgram(BKOOLParser.ProgramContext ctx);
	/**
	 * Visit a parse tree produced by {@link BKOOLParser#classdecl}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitClassdecl(BKOOLParser.ClassdeclContext ctx);
	/**
	 * Visit a parse tree produced by {@link BKOOLParser#memdecl}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMemdecl(BKOOLParser.MemdeclContext ctx);
	/**
	 * Visit a parse tree produced by {@link BKOOLParser#bkooltype}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBkooltype(BKOOLParser.BkooltypeContext ctx);
}