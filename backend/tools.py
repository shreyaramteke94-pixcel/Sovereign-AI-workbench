def calculator(expression: str) -> str:
    """
    Safely calculate a mathematical expression.
    """

    allowed_characters = "0123456789+-*/(). %"

    if not all(char in allowed_characters for char in expression):
        return "Error: Invalid characters in expression."

    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)

    except Exception as e:
        return f"Error: {str(e)}"