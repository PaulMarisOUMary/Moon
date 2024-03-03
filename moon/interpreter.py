from typing import Callable

class IOType:
	def __init__(self, 
		output_method,
		input_method
	) -> None:
		self.output_method: Callable = output_method
		self.input_method: Callable = input_method

def evaluate_expression(exp, environment, io):
	type, *args = exp
	if type == "integer_literal":
		return int(args[0])
	elif type == "float_literal":
		return float(args[0])
	elif type == "string_literal":
		return str(args[0])
	elif type == "boolean_literal":
		return args[0]
	elif type == "null_literal":
		return None
	elif type == "logical_expression" and args[0] == "not":
		return not evaluate_or_get_value(args[1], environment, io)
	elif type in ("arithmetic_expression", "comparison_expression", "logical_expression"):
		operator, left, right = args
		left_val = evaluate_or_get_value(left, environment, io)
		right_val = evaluate_or_get_value(right, environment, io)
		return eval(f"{repr(left_val)} {operator} {repr(right_val)}")
	elif type == "variable_declaration_statement":
		var_name, expression = args
		value = evaluate_expression(expression, environment, io)
		environment[var_name] = value
		return value

def evaluate_or_get_value(expression, environment, io):
	if isinstance(expression, tuple):
		if expression[0] == "call_statement":
			return execute_statement(expression, environment, {}, io)
		return evaluate_expression(expression, environment, io)
	return environment[expression]

def execute_statement(statement, environment, actions, io: IOType):
	type, *args = statement
	if type == "variable_declaration_statement":
		var_name, value = args
		environment[var_name] = handle_variable_declaration(value, environment, actions, io)
	elif type == "if_statement":
		condition, suite, else_suite = args
		if evaluate_expression(condition, environment, io):
			result = execute_statements(suite, environment, actions, io)
			if result == "stop":
				return "stop"
			elif result == "skip":
				return "skip"
		elif else_suite:
			return execute_statements(else_suite, environment, actions, io)
	elif type == "while_statement":
		condition, suite = args
		while evaluate_expression(condition, environment, io):
			skip = False
			result = None
			for inner_statement in suite:
				result = execute_statement(inner_statement, environment, actions, io)
				if result == "stop":
					break
				if result == "skip":
					skip = True
					break
			if result == "stop":
				break
			if skip:
				continue
	elif type == "break_statement":
		return "stop"
	elif type == "continue_statement":
		return "skip"
	elif type == "action_statement":
		name, params, suite = args
		actions[name] = (params, suite)
	elif type == "call_statement":
		return handle_call_statement(args, environment, actions, io)
	elif type == "return_statement":
		values = [evaluate_expression(exp, environment, io) for exp in args[0]]
		return values if len(values) != 1 else values[0]
	elif type == "print_statement":
		io.output_method(*[evaluate_or_get_value(exp, environment, io) for exp in args[0]])
	elif type == "ask_statement":
		io.input_method(args[0][1])

def auto_cast(value):
	try:
		return int(value)
	except ValueError:
		try:
			return float(value.replace(",", "."))
		except ValueError:
			return value

def handle_variable_declaration(value, environment, actions, io: IOType):
    if isinstance(value, str):
        return environment[value]
    elif isinstance(value, tuple):
        if value[0] == "ask_statement":
            return auto_cast(io.input_method(value[1][1]))
        if value[0] == "call_statement":
            return execute_statement(value, environment, actions, io)
    return evaluate_expression(value, environment, io)

def handle_call_statement(args, environment, actions, io):
    name, params = args
    param_values = [evaluate_expression(p, environment, io) for p in params]
    if name in actions:
        func_params, func_body = actions[name]
        local_env = environment.copy()
        local_env.update(dict(zip(func_params, param_values)))
        execute_statements(func_body, local_env, actions, io)
        environment.update({k: v for k, v in local_env.items() if k in environment and v != environment.get(k)})
        return local_env.get("return_value", None)

def execute_statements(statements, environment, actions, io):
	for statement in statements:
		result = execute_statement(statement, environment, actions, io)
		if result == "stop":
			return "stop"
		if result == "skip":
			return "skip"
		if statement[0] == "return_statement":
			environment["return_value"] = result

def execute_program(
		program,
		output_method = print,
		input_method = input
	) -> None:
	environment = {}
	actions = {}
	execute_statements(program, environment, actions, IOType(output_method, input_method))