from typing import Any, Callable, Dict, List, Optional, Tuple, Union

# Interpreter types
TStatement = Tuple[Any]
TProgram = List[TStatement]

TEnvironment = Dict[str, Any]

TStatementCallback = Optional[Callable]
TOutputCallback = Callable[[object], None]
TInputCallback = Callable[[object], str]

class BreakType:
	pass

class ContinueType: # ? Should be renamed to Skip
	pass

class ReturnType:
	def __init__(self, value) -> None:
		self.value = value

def custom_repr(value: object):
	if isinstance(value, bool):
		return str(value).lower()
	elif isinstance(value, type(None)):
		return "null"
	else:
		return str(value)

def autocast(value):
	try:
		return int(value)
	except ValueError:
		try:
			return float(value.replace(",", "."))
		except ValueError:
			return value


def execute_statement(
		statement: TStatement,
		environment: TEnvironment,
		/,
		statement_callback: TStatementCallback,
		output_callback: TOutputCallback = print,
		input_callback: TInputCallback = input,
		*args,
		**kwargs,
) -> Any:
	def execute(
			e_statement: TStatement,
			e_environment: TEnvironment = environment,
			call_statement: TStatementCallback = statement_callback,
			call_output: TOutputCallback = output_callback,
			call_input: TInputCallback = input_callback,
			*e_args,
			**e_kwargs,
	):
		return execute_statement(
			e_statement,
			e_environment,
			call_statement,
			call_output,
			call_input,
			*e_args,
			**e_kwargs,
		)
	if statement_callback:
		statement_callback(environment)
	statement_type, *next = statement

	match statement_type:
		# Primitive Types
		case "integer_literal" | "float_literal" | "string_literal" | "boolean_literal":
			return next[0]
		case "null_literal":
			return None
		
		# Composite Types
		case "list_statement":
			raise NotImplementedError
		case "dict_statement":
			raise NotImplementedError

		# Variable Declaration and Initialization
		case "variable_declaration_statement":
			varname, expressions = next
			varvalue = execute(expressions)
			environment[varname] = varvalue

		# Expressions
		case "arithmetic_expression" | "comparison_expression" | "logical_expression":
			operator, *expressions = next
			if operator == "not":
				return not execute(expressions[0])

			left, right = expressions
			leftvalue = execute(left)
			rightvalue = execute(right)

			return eval(f"{repr(leftvalue)} {operator} {repr(rightvalue)}")

		# Control Structures
		case "if_statement":
			# CONTAINS BLOCK
			condition, if_expressions, else_expressions = next
			executed_condition = execute(condition)
			if executed_condition:
				for expression in if_expressions: # type: ignore
					result = execute(expression)
					if isinstance(result, (BreakType, ContinueType, ReturnType)):
						return result
			elif else_expressions:
				for expression in else_expressions: # type: ignore
					result = execute(expression)
					if isinstance(result, (BreakType, ContinueType)):
						return result

		# Loop structure
		case "while_statement":
			# CONTAINS BLOCK
			condition, block_expressions = next
			while execute(condition):
				result = None
				for expression in block_expressions: # type: ignore
					result = execute(expression)
					if isinstance(result, (BreakType, ContinueType, ReturnType)):
						break
				if isinstance(result, BreakType):
					break
				elif isinstance(result, ReturnType):
					return result
				elif isinstance(result, ContinueType):
					continue 

		case "break_statement":
			return BreakType()

		case "continue_statement":
			return ContinueType()

		# Try-Catch and raise

		# Functions
		case "action_statement":
			# CONTAINS BLOCK
			funcname, params, block_expressions = next
			environment[funcname] = (params, block_expressions)

		case "call_statement":
			funcname, params = next
			param_values = [execute(p) for p in params] # type: ignore
			
			func_params, block_expressions = environment[funcname]

			sub_environment = environment.copy()
			sub_environment.update(dict(zip(func_params, param_values)))
			result = None
			for expression in block_expressions:
				result = execute(expression, sub_environment)
				if isinstance(result, ReturnType):
					result = result.value
					break
			environment.update({k: v for k, v in sub_environment.items() if k in environment and v != environment.get(k)})
			return result

		case "return_statement":
			expressions = next[0]
			result = execute(expressions[0])
			return ReturnType(result)

		# Classes

		# Modules

		# Built-in
		case "print_statement":
			if len(next) > 1:
				raise ValueError("print")
			output_callback(
				*[
					custom_repr(
						execute(expression)
					)
					for expression in next[0] # type: ignore
				]
			)
		case "ask_statement":
			prompt = execute(next[0])
			return autocast(
					input_callback(
					prompt
				)
			)

		# Variable
		case _:
			if isinstance(statement, str):
				return environment[statement] # environment.get(statement, None)
			else:
				print(f"Un-case {statement}")

def execute_program(
		program: TProgram,
		/,
		statement_callback: TStatementCallback = None,
		output_callback: TOutputCallback = print,
		input_callback: TInputCallback = input,
	) -> None:
	environment = dict()

	if not program:
		raise ValueError("No instruction")

	for statement in program:
		execute_statement(
			statement,
			environment,
			statement_callback,
			output_callback,
			input_callback
		)