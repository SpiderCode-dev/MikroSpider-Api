from jwt import encode, decode

def create_token(data: dict, key: str) -> str:
    token: str = encode(payload=data, key=key, algorithm="HS256")
    return token

def validate_token(token: str,  key: str) -> dict:
    data: dict = decode(token, key=key, algorithms=['HS256'])
    return data