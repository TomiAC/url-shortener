from uuid import uuid4

def generate_uuid_code(length=6):
    return str(uuid4()).replace("-", "")[:length]