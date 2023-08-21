def evaluate_expression(exp, environment):
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
		return not evaluate_or_get_value(args[1], environment)
	elif type in ("arithmetic_expression", "comparison_expression", "logical_expression"):
		operator, left, right = args
		left_val = evaluate_or_get_value(left, environment)
		right_val = evaluate_or_get_value(right, environment)
		return eval(f"{left_val} {operator} {right_val}")
	elif type == "variable_declaration_statement":
		var_name, expression = args
		value = evaluate_expression(expression, environment)
		environment[var_name] = value
		return value

def evaluate_or_get_value(expression, environment):
	if isinstance(expression, tuple):
		if expression[0] == "call_statement":
			return execute_statement(expression, environment, {})
		return evaluate_expression(expression, environment)
	return environment[expression]

def execute_statement(statement, environment, actions):
	type, *args = statement
	if type == "variable_declaration_statement":
		var_name, value = args
		environment[var_name] = handle_variable_declaration(value, environment, actions)
	elif type == "if_statement":
		condition, suite, else_suite = args
		if evaluate_expression(condition, environment):
			result = execute_statements(suite, environment, actions)
			if result == "stop":
				return "stop"
			elif result == "skip":
				return "skip"
		elif else_suite:
			return execute_statements(else_suite, environment, actions)
	elif type == "while_statement":
		condition, suite = args
		while evaluate_expression(condition, environment):
			skip = False
			result = None
			for inner_statement in suite:
				result = execute_statement(inner_statement, environment, actions)
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
		return handle_call_statement(args, environment, actions)
	elif type == "return_statement":
		values = [evaluate_expression(exp, environment) for exp in args[0]]
		return values if len(values) != 1 else values[0]
	elif type == "print_statement":
		print(*[evaluate_or_get_value(exp, environment) for exp in args[0]])
	elif type == "ask_statement":
		input(args[0][1])

def handle_variable_declaration(value, environment, actions):
	if isinstance(value, tuple):
		if value[0] == "ask_statement":
			return input(value[1][1])
		if value[0] == "call_statement":
			return execute_statement(value, environment, actions)
	return evaluate_expression(value, environment)

def handle_call_statement(args, environment, actions):
	name, params = args
	param_values = [evaluate_expression(p, environment) for p in params]
	if name in actions:
		func_params, func_body = actions[name]
		local_env = dict(zip(func_params, param_values))
		execute_statements(func_body, local_env, actions)
		environment.update({k: v for k, v in local_env.items() if k in environment})
		return local_env.get("return_value", None)

def execute_statements(statements, environment, actions):
	for statement in statements:
		result = execute_statement(statement, environment, actions)
		if result == "stop":
			return "stop"
		if result == "skip":
			return "skip"
		if statement[0] == "return_statement":
			environment["return_value"] = result

def execute_program(program):
	environment = {}
	actions = {}
	execute_statements(program, environment, actions)