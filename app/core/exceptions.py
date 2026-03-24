class UserAlreadyExists(Exception):
    """用户已存在"""
    pass

class AuthenticationError(Exception):
    """认证失败
    用户不存在或密码错误"""
    pass

class EmailAlreadyExists(Exception):
    """邮箱已存在"""
    pass