import hashlib
import time
import uuid
import os

class TokenGenerator:
    def __init__(self):
        self.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

    def generate_token(self, request_id, instance_id, data_key):
        """
        生成动态令牌
        :param request_id: 请求ID
        :param instance_id: 实例ID
        :param data_key: 数据标识符
        :return: 生成的令牌
        """
        timestamp = str(int(time.time()))
        nonce = str(uuid.uuid4())

        # 组合所有元素
        token_elements = [
            request_id,
            instance_id,
            nonce,
            timestamp,
            data_key,
            self.secret_key
        ]

        # 使用SHA-256哈希函数生成令牌
        token = hashlib.sha256(''.join(token_elements).encode()).hexdigest()

        return {
            'token': token,
            'nonce': nonce,
            'timestamp': timestamp
        }

    def verify_token(self, token, request_id, instance_id, data_key, nonce, timestamp):
        """
        验证令牌
        :param token: 待验证的令牌
        :param request_id: 请求ID
        :param instance_id: 实例ID
        :param data_key: 数据标识符
        :param nonce: 随机字符串
        :param timestamp: 时间戳
        :return: 验证是否通过
        """
        # 重新生成令牌
        token_elements = [
            request_id,
            instance_id,
            nonce,
            timestamp,
            data_key,
            self.secret_key
        ]

        expected_token = hashlib.sha256(''.join(token_elements).encode()).hexdigest()

        # 验证令牌是否匹配
        return token == expected_token

    def is_token_expired(self, timestamp, max_age=300):
        """
        检查令牌是否过期
        :param timestamp: 令牌生成时的时间戳
        :param max_age: 令牌的最大有效期（秒），默认为5分钟
        :return: 是否过期
        """
        current_time = int(time.time())
        token_time = int(timestamp)
        return (current_time - token_time) > max_age