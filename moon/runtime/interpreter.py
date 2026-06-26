from __future__ import annotations

from typing import Any

from ..ast_nodes import (
    ActionStatement,
    AssignStatement,
    Attribute,
    BinOp,
    BuiltinCall,
    CallExpr,
    CompareExpr,
    DictAssignStatement,
    DictExpr,
    FalseLiteral,
    FileInput,
    FloatLiteral,
    IfStatement,
    IntegerLiteral,
    ListAssignStatement,
    ListExpr,
    MethodCall,
    NoopStatement,
    NotExpr,
    NullLiteral,
    RaiseStatement,
    ResultStatement,
    SkipStatement,
    StopStatement,
    StringLiteral,
    TernaryExpr,
    TestStatement,
    ThingStatement,
    TrueLiteral,
    UnaryOp,
    UseFrom,
    UseName,
    Var,
    WhileStatement,
)
from ..errors import MoonArithmeticError, MoonRuntimeError, MoonTypeError, MoonUserError
from .builtins import BUILTINS
from .coerce import is_truthy, moon_bool
from .environment import Environment
from .objects import (
    Action,
    Bool,
    Dict,
    Float,
    Int,
    List,
    Null,
    Object,
    String,
    Thing,
    FALSE,
    NULL,
    TRUE,
)
from .signals import ResultSignal, SkipSignal, StopSignal


class Interpreter:
    def __init__(self) -> None:
        self._global = Environment()

    def run(self, node: FileInput) -> None:
        self._exec_body(node.body, self._global)

    def eval_expr(self, node: Any, env: Environment | None = None) -> Object:
        return self._eval(node, env or self._global)

    def _exec_body(self, body: list[Any], env: Environment) -> None:
        for stmt in body:
            self._exec(stmt, env)

    def _exec(self, node: Any, env: Environment) -> None:
        match node:
            case AssignStatement():
                self._exec_assign(node, env)
            case ListAssignStatement() | DictAssignStatement():
                raise MoonRuntimeError(
                    "List and dict assignment are not yet implemented",
                    loc=getattr(node, "loc", None),
                )
            case ActionStatement():
                self._exec_action(node, env)
            case ThingStatement():
                self._exec_thing(node, env)
            case WhileStatement():
                self._exec_while(node, env)
            case IfStatement():
                self._exec_if(node, env)
            case TestStatement():
                self._exec_test(node, env)
            case ResultStatement():
                self._exec_result(node, env)
            case RaiseStatement():
                self._exec_raise(node, env)
            case StopStatement():
                raise StopSignal()
            case SkipStatement():
                raise SkipSignal()
            case NoopStatement():
                pass
            case UseName() | UseFrom():
                self._exec_use(node, env)
            case _:
                self._eval(node, env)

    def _exec_assign(self, node: AssignStatement, env: Environment) -> None:
        env.set(node.name.name, self._eval(node.value, env))

    def _exec_action(self, node: ActionStatement, env: Environment) -> None:
        params = [p.name for p in node.parameters.params]
        env.set(node.name.name, Action(node.name.name, params, node.body, env))

    def _exec_thing(self, node: ThingStatement, env: Environment) -> None:
        parent: Thing | None = None
        if node.inheritance is not None:
            parent_name = node.inheritance.parent.name
            candidate = env.get(parent_name)
            if not isinstance(candidate, Thing):
                raise MoonTypeError(f"'{parent_name}' is not a thing", loc=node.loc)
            parent = candidate

        attribute_names: list[str] = []
        methods: dict[str, Action] = {}

        for item in node.body:
            if isinstance(item, Attribute):
                attribute_names.append(item.name.name)
            elif isinstance(item, ActionStatement):
                params = [p.name for p in item.parameters.params]
                methods[item.name.name] = Action(item.name.name, params, item.body, env)

        thing = Thing(node.name.name, parent, attribute_names)
        thing.methods = methods
        env.set(node.name.name, thing)

    def _exec_while(self, node: WhileStatement, env: Environment) -> None:
        while is_truthy(self._eval(node.condition, env)):
            try:
                self._exec_body(node.body, env)
            except StopSignal:
                break
            except SkipSignal:
                continue

    def _exec_if(self, node: IfStatement, env: Environment) -> None:
        if is_truthy(self._eval(node.condition, env)):
            self._exec_body(node.then_body, env)
            return
        for branch in node.elif_branches:
            if is_truthy(self._eval(branch.condition, env)):
                self._exec_body(branch.body, env)
                return
        if node.else_body is not None:
            self._exec_body(node.else_body, env)

    def _exec_test(self, node: TestStatement, env: Environment) -> None:
        try:
            self._exec_body(node.try_body, env)
        except MoonRuntimeError:
            if node.fail_body is not None:
                self._exec_body(node.fail_body, env)

    def _exec_result(self, node: ResultStatement, env: Environment) -> None:
        value = self._eval(node.value, env) if node.value is not None else NULL
        raise ResultSignal(value)

    def _exec_raise(self, node: RaiseStatement, env: Environment) -> None:
        value = self._eval(node.value, env)
        raise MoonUserError(repr(value), loc=node.loc)

    def _exec_use(self, node: UseName | UseFrom, env: Environment) -> None:
        raise NotImplementedError

    def _eval(self, node: Any, env: Environment) -> Object:
        match node:
            case NullLiteral():
                return NULL
            case TrueLiteral():
                return TRUE
            case FalseLiteral():
                return FALSE
            case IntegerLiteral(value=v):
                return Int(v)
            case FloatLiteral(value=v):
                return Float(v)
            case StringLiteral(value=v):
                return String(v)
            case Var():
                return env.get(node.name.name)
            case BinOp():
                return self._eval_binop(node, env)
            case UnaryOp():
                return self._eval_unary(node, env)
            case NotExpr():
                return moon_bool(not is_truthy(self._eval(node.operand, env)))
            case CompareExpr():
                return self._eval_compare(node, env)
            case TernaryExpr():
                return self._eval_ternary(node, env)
            case CallExpr():
                return self._eval_call(node, env)
            case BuiltinCall():
                return self._eval_builtin(node, env)
            case MethodCall():
                return self._eval_method(node, env)
            case ListExpr():
                return self._eval_list(node, env)
            case DictExpr():
                return self._eval_dict(node, env)
            case _:
                self._exec(node, env)
                return NULL

    def _eval_binop(self, node: BinOp, env: Environment) -> Object:
        op = node.op

        if op == "and":
            left = self._eval(node.left, env)
            return self._eval(node.right, env) if is_truthy(left) else left

        if op == "or":
            left = self._eval(node.left, env)
            return left if is_truthy(left) else self._eval(node.right, env)

        left = self._eval(node.left, env)
        right = self._eval(node.right, env)

        if op == "+" and isinstance(left, String) and isinstance(right, String):
            return String(left.value + right.value)

        if isinstance(left, (Int, Float)) and isinstance(right, (Int, Float)):
            return self._eval_arithmetic(op, left, right, node.loc)

        raise MoonTypeError(
            f"Unsupported operands for '{op}': "
            f"'{type(left).__name__}' and '{type(right).__name__}'",
            loc=node.loc,
        )

    def _eval_arithmetic(
        self,
        op: str,
        left: Int | Float,
        right: Int | Float,
        loc: Any,
    ) -> Int | Float:
        lv, rv = left.value, right.value
        as_float = isinstance(left, Float) or isinstance(right, Float)

        match op:
            case "+":
                result = lv + rv
            case "-":
                result = lv - rv
            case "*":
                result = lv * rv
            case "/":
                if rv == 0:
                    raise MoonArithmeticError("Division by zero", loc=loc)
                return Float(lv / rv)
            case "//":
                if rv == 0:
                    raise MoonArithmeticError("Division by zero", loc=loc)
                result = lv // rv
            case "%":
                if rv == 0:
                    raise MoonArithmeticError("Division by zero", loc=loc)
                result = lv % rv
            case "**":
                result = lv**rv
                if isinstance(result, float):
                    as_float = True
            case _:
                raise MoonTypeError(f"Unknown arithmetic operator '{op}'", loc=loc)

        return Float(float(result)) if as_float else Int(int(result))

    def _eval_unary(self, node: UnaryOp, env: Environment) -> Object:
        operand = self._eval(node.operand, env)
        match node.op:
            case "+" if isinstance(operand, (Int, Float)):
                return operand
            case "-" if isinstance(operand, Int):
                return Int(-operand.value)
            case "-" if isinstance(operand, Float):
                return Float(-operand.value)
            case _:
                raise MoonTypeError(
                    f"Unsupported unary operator '{node.op}' "
                    f"for type '{type(operand).__name__}'",
                    loc=node.loc,
                )

    def _eval_compare(self, node: CompareExpr, env: Environment) -> Object:
        left = self._eval(node.left, env)
        for op, right_node in zip(node.operators, node.operands):
            right = self._eval(right_node, env)
            if not self._compare(left, op, right, node.loc):
                return FALSE
            left = right
        return TRUE

    def _compare(self, left: Object, op: str, right: Object, loc: Any) -> bool:
        match op:
            case "is":
                return self._obj_eq(left, right)
            case "isnt":
                return not self._obj_eq(left, right)
            case _ if isinstance(left, (Int, Float)) and isinstance(
                right, (Int, Float)
            ):
                lv, rv = left.value, right.value
                match op:
                    case "<":
                        return lv < rv
                    case "<=":
                        return lv <= rv
                    case ">":
                        return lv > rv
                    case ">=":
                        return lv >= rv
                    case _:
                        raise MoonTypeError(
                            f"Unknown comparison operator '{op}'", loc=loc
                        )
            case _:
                raise MoonTypeError(
                    f"Cannot compare '{type(left).__name__}' and "
                    f"'{type(right).__name__}' with '{op}'",
                    loc=loc,
                )

    def _obj_eq(self, left: Object, right: Object) -> bool:
        if type(left) is not type(right):
            return False
        if isinstance(left, (Int, Float, String, Bool)):
            return left.value == right.value  # type: ignore
        if isinstance(left, Null):
            return True
        return left is right

    def _eval_ternary(self, node: TernaryExpr, env: Environment) -> Object:
        condition = self._eval(node.condition, env)
        return (
            self._eval(node.then_expr, env)
            if is_truthy(condition)
            else self._eval(node.else_expr, env)
        )

    def _eval_call(self, node: CallExpr, env: Environment) -> Object:
        callee = env.get(node.callee.name)

        if isinstance(callee, Thing):
            instance = callee.instantiate()
            init = callee.methods.get("init")
            if init is not None:
                args = [self._eval(a, env) for a in node.arguments]
                self._call_action(init, [instance] + args, node.loc)
            return instance

        if not isinstance(callee, Action):
            raise MoonTypeError(f"'{node.callee.name}' is not callable", loc=node.loc)

        args = [self._eval(a, env) for a in node.arguments]
        return self._call_action(callee, args, node.loc)

    def _eval_builtin(self, node: BuiltinCall, env: Environment) -> Object:
        fn = BUILTINS.get(node.name)
        if fn is None:
            raise MoonRuntimeError(f"Unknown builtin '{node.name}'", loc=node.loc)
        args = [self._eval(a, env) for a in node.arguments]
        return fn(args, node.loc)

    def _eval_method(self, node: MethodCall, env: Environment) -> Object:
        receiver = env.get(node.receiver.name)
        attr = receiver.get_attr(node.method.name)
        args = [self._eval(a, env) for a in node.arguments]

        if isinstance(attr, Action):
            return self._call_action(attr, [receiver] + args, node.loc)

        if args:
            raise MoonTypeError(f"'{node.method.name}' is not callable", loc=node.loc)
        return attr

    def _eval_list(self, node: ListExpr, env: Environment) -> Object:
        return List([self._eval(item.value, env) for item in node.items])

    def _eval_dict(self, node: DictExpr, env: Environment) -> Object:
        pairs = [
            (self._eval(item.key, env), self._eval(item.value, env))
            for item in node.items
        ]
        return Dict(pairs)

    def _call_action(self, action: Action, args: list[Object], loc: Any) -> Object:
        if not isinstance(action, Action):
            raise MoonTypeError(f"'{action!r}' is not callable", loc=loc)
        if len(args) != len(action.params):
            raise MoonRuntimeError(
                f"'{action.name}' expected {len(action.params)} argument(s), "
                f"got {len(args)}",
                loc=loc,
            )
        call_env = action.closure.child()
        for param, arg in zip(action.params, args):
            call_env.set(param, arg)
        try:
            self._exec_body(action.body, call_env)
        except ResultSignal as sig:
            return sig.value
        return NULL
