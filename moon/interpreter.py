def evaluate_expression(exp, environment):
	type, *args = exp
	if type == "integer_literal":
		return int(args[0])
	elif type == "float_literal":
		return float(args[0])
	elif type == "string_literal":
		return str(args[0])
	elif type == "boolean_literal":
		return args[0] == "true"
	elif type == "null_literal":
		return None
	elif type == "arithmetic_expression":
		operator, left, right = args
		left_val = evaluate_expression(left, environment)
		right_val = evaluate_expression(right, environment)
		return eval(f"{left_val} {operator} {right_val}")
	elif type == "comparison_expression":
		operator, left, right = args
		left_val = evaluate_expression(left, environment)
		right_val = evaluate_expression(right, environment)
		return eval(f"{left_val} {operator} {right_val}")
	elif type == "logical_expression":
		if len(args) == 3:
			operator, left, right = args
			left_val = evaluate_expression(left, environment)
			right_val = evaluate_expression(right, environment)
			return eval(f"{left_val} {operator} {right_val}")
		else:
			operator, expr = args
			return not evaluate_expression(expr, environment)
	elif type == "variable_declaration_statement":
		var_name, expression = args
		value = evaluate_expression(expression, environment)
		environment[var_name] = value
		return value

def execute_statement(statement, environment, actions):
	type, *args = statement
	if type == "variable_declaration_statement":
		var_name, value = args
		# Check if value is a call_statement
		if isinstance(value, tuple) and value[0] == "call_statement":
			# Execute the call and assign the result to the variable
			value = execute_statement(value, environment, actions)
		else:
			value = evaluate_expression(value, environment)
		environment[var_name] = value
	elif type == "if_statement":
		condition, suite = args
		if evaluate_expression(condition, environment):
			execute_statements(suite, environment, actions)
	elif type == "while_statement":
		condition, suite = args
		while evaluate_expression(condition, environment):
			execute_statements(suite, environment, actions)
	elif type == "action_statement":
		name, params, suite = args
		actions[name] = (params, suite)
	elif type == "call_statement":
		name, params = args
		param_values = [evaluate_expression(p, environment) for p in params]
		if name in actions:
			func_params, func_body = actions[name]
			local_env = dict(zip(func_params, param_values))
			execute_statements(func_body, local_env, actions)
			# Update the global variables with the local variables of the same name
			for var_name, var_value in local_env.items():
				if var_name in environment:
					environment[var_name] = var_value
			# Return the last expression result of the function
			return local_env.get("return_value", None)
	elif type == "return_statement":
		values = [evaluate_expression(exp, environment) for exp in args[0]]
		return values if len(values) != 1 else values[0]
	elif type == "print_statement":
		expressions = args[0]
		values = [evaluate_expression(exp, environment) if isinstance(exp, tuple) else environment[exp] for exp in expressions]
		print(*values)

def execute_statements(statements, environment, actions):
	for statement in statements:
		result = execute_statement(statement, environment, actions)
		# Check if it's a return statement and store the value
		if statement[0] == "return_statement":
			environment["return_value"] = result

def execute_program(program):
	environment = {}
	actions = {}
	execute_statements(program, environment, actions)