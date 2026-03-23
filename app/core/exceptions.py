class UserAlreadyExists(Exception):
    """用户已存在"""
    pass

class UserNotFound(Exception):
    """用户不存在"""
    pass

class EmailAlreadyExists(Exception):
    """邮箱已存在"""
    pass