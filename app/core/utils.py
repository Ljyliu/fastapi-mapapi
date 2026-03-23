from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    "生成密码哈希，自动处理bcrypt的72字节限制"

    # 调试信息
    print(f"[密码检查] 原始密码: '{password}'")
    print(f"[密码检查] 字符数: {len(password)}")
    
    # 转字节检查
    encoded = password.encode('utf-8')
    print(f"[密码检查] 字节数: {len(encoded)}")
    
    # 如果超长，截断
    if len(encoded) > 72:
        print(f"[警告] 密码超长 ({len(encoded)}字节)，截断到72字节")
        encoded = encoded[:72]
        truncated = encoded.decode('utf-8', errors='ignore')
        print(f"[截断后] 密码: '{truncated}'")
        print(f"[截断后] 字节: {len(truncated.encode('utf-8'))}")
        return pwd_context.hash(truncated)


    return pwd_context.hash(password)