def create_stack():
    """
    Khởi tạo một ngăn xếp mới.
    Returns:
        list: Một danh sách rỗng.
    """
    return []

def is_empty(stack):
    """
    Kiểm tra xem ngăn xếp có đang rỗng hay không.
    Args:
        stack (list): Ngăn xếp cần kiểm tra.
    Returns:
        bool: True nếu ngăn xếp rỗng, False nếu có chứa phần tử.
    """
    return len(stack) == 0

def push(stack, item):
    """
    Thêm một phần tử vào ngăn xếp.
    Args:
        stack (list): Ngăn xếp hiện tại.
        item (any): Phần tử cần thêm vào.
    """
    stack.append(item)

def pop(stack):
    """
    Lấy và xóa phần tử ở đỉnh của ngăn xếp.
    Args:
        stack (list): Ngăn xếp hiện tại.
    Returns:
        any: Phần tử ở đỉnh ngăn xếp, hoặc None nếu ngăn xếp đang rỗng.
    """
    if not is_empty(stack):
        return stack.pop()
    return None