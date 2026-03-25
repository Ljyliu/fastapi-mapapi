class CustomException(Exception):
    """自定义异常"""
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg

class UserAlreadyExists(CustomException):
    def __init__(self):
        super().__init__(code=400, msg="用户已存在")
    

class AuthenticationError(CustomException):
    def __init__(self):
        super().__init__(code=401, msg="认证失败,用户名或密码错误")

class EmailAlreadyExists(CustomException):
    def __init__(self):
        super().__init__(code=400, msg="邮箱已存在")