from hashlib import sha512


class Hasher:
    @staticmethod
    def hash_password(password: str):
        salt = 'test_website'.encode('utf-8')
        return sha512(salt + password.encode('utf-8')).hexdigest()
