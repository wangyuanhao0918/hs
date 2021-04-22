# -*- encoding=utf-8 -*-


from .cryption import Cryption


class Phone(object):

    @classmethod
    def encrypt(cls, number: str, fixed:bool=False) -> str:
        """
        加密手机号
        :param number: 手机号
        :return: 加密后手机号
        """
        return Cryption.encrypt(data=number, fixed=fixed)

    @classmethod
    def decrypt(cls, encrypt_str: str, fixed:bool=False) -> str:
        """
        解密手机号
        :param cryption_str: 加密字符串
        :return: 解密后的手机号
        """
        return Cryption.decrypt(data=encrypt_str, fixed=fixed)

    @classmethod
    def encryption_phone(cls, encrypt_str:str, fixed:bool=False) -> str:
        """脱敏手机号"""
        decrypt_phone = cls.decrypt(encrypt_str, fixed=fixed)
        head = decrypt_phone[0: 3]
        tail = decrypt_phone[7: 12]
        phone = head + '****' + tail
        return phone
