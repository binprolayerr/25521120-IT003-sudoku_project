def create_stack():
    return []

def is_empty(stack):
    return len(stack) == 0

def push(stack, item):
    stack.append(item)

def peek(stack):
    if not is_empty(stack):
        return stack[-1]
    return None

def pop(stack):
    if not is_empty(stack):
        return stack.pop()
    return None