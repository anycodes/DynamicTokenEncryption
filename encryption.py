import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64


class Encryptor:
    def __init__(self):
        # 从环境变量获取加密密钥，如果不存在则使用默认值
        self.key = os.environ.get('ENCRYPTION_KEY', 'default_encryption_key').encode()
        # 确保密钥长度为32字节（256位）
        self.key = self.key.ljust(32)[:32]

    def encrypt(self, plaintext):
        """
        加密明文
        :param plaintext: 待加密的明文
        :return: 加密后的密文（Base64编码）
        """
        # 生成随机IV（初始化向量）
        iv = os.urandom(16)

        # 创建加密器
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # 对明文进行填充
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()

        # 加密
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # 将IV和密文组合，并进行Base64编码
        encrypted = base64.b64encode(iv + ciphertext)

        return encrypted.decode()

    def decrypt(self, ciphertext):
        """
        解密密文
        :param ciphertext: 待解密的密文（Base64编码）
        :return: 解密后的明文
        """
        # Base64解码
        encrypted = base64.b64decode(ciphertext.encode())

        # 分离IV和密文
        iv = encrypted[:16]
        ciphertext = encrypted[16:]

        # 创建解密器
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # 解密
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

        # 去除填充
        unpadder = padding.PKCS7(128).unpadder()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

        return decrypted.decode()