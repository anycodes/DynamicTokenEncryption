from token_generator import TokenGenerator
from encryption import Encryptor
from audit_logger import AuditLogger

class SecureTokenSystem:
    def __init__(self):
        self.token_generator = TokenGenerator()
        self.encryptor = Encryptor()
        self.logger = AuditLogger()

    def generate_token(self, request_id, instance_id, data_key, user_id):
        """
        生成令牌
        """
        if not all([request_id, instance_id, data_key, user_id]):
            self.logger.log_error('Missing required parameters for token generation')
            raise ValueError('Missing required parameters')

        token_data = self.token_generator.generate_token(request_id, instance_id, data_key)
        self.logger.log_token_generation(user_id, token_data['token'], 'SUCCESS')
        return token_data

    def verify_token(self, token, request_id, instance_id, data_key, nonce, timestamp, user_id):
        """
        验证令牌
        """
        if not all([token, request_id, instance_id, data_key, nonce, timestamp, user_id]):
            self.logger.log_error('Missing required parameters for token verification')
            raise ValueError('Missing required parameters')

        is_valid = self.token_generator.verify_token(token, request_id, instance_id, data_key, nonce, timestamp)
        is_expired = self.token_generator.is_token_expired(timestamp)

        if is_valid and not is_expired:
            self.logger.log_token_verification(user_id, token, 'SUCCESS')
            return True
        else:
            self.logger.log_token_verification(user_id, token, 'FAILURE')
            return False

    def encrypt_data(self, plaintext, user_id):
        """
        加密数据
        """
        if not plaintext or not user_id:
            self.logger.log_error('Missing required parameters for encryption')
            raise ValueError('Missing required parameters')

        encrypted = self.encryptor.encrypt(plaintext)
        self.logger.log_encryption(user_id, 'data', 'SUCCESS')
        return encrypted

    def decrypt_data(self, ciphertext, user_id):
        """
        解密数据
        """
        if not ciphertext or not user_id:
            self.logger.log_error('Missing required parameters for decryption')
            raise ValueError('Missing required parameters')

        try:
            decrypted = self.encryptor.decrypt(ciphertext)
            self.logger.log_decryption(user_id, 'data', 'SUCCESS')
            return decrypted
        except Exception as e:
            self.logger.log_decryption(user_id, 'data', 'FAILURE')
            self.logger.log_error(f'Decryption failed: {str(e)}')
            raise

# 创建一个全局实例，方便直接导入使用
secure_token_system = SecureTokenSystem()

# 为了方便使用，也可以直接导出类的方法
generate_token = secure_token_system.generate_token
verify_token = secure_token_system.verify_token
encrypt_data = secure_token_system.encrypt_data
decrypt_data = secure_token_system.decrypt_data