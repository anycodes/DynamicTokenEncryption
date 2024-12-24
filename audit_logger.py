import logging
import json
import os
from datetime import datetime


class AuditLogger:
    def __init__(self):
        # 从环境变量获取日志级别，默认为INFO
        log_level = os.environ.get('LOG_LEVEL', 'INFO')

        # 设置日志格式
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        self.logger = logging.getLogger('AuditLogger')

        # 从环境变量获取日志文件路径，如果不存在则使用默认值
        log_file = os.environ.get('AUDIT_LOG_FILE', 'audit.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)

    def log_event(self, event_type, user_id, action, resource, status, details=None):
        """
        记录审计事件
        :param event_type: 事件类型（如 'TOKEN_GENERATION', 'DATA_ACCESS'）
        :param user_id: 用户ID
        :param action: 执行的操作
        :param resource: 操作的资源
        :param status: 操作状态（如 'SUCCESS', 'FAILURE'）
        :param details: 额外的详细信息（可选）
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'action': action,
            'resource': resource,
            'status': status
        }

        if details:
            log_entry['details'] = details

        self.logger.info(json.dumps(log_entry))

    def log_token_generation(self, user_id, token_id, status):
        """
        记录令牌生成事件
        """
        self.log_event('TOKEN_GENERATION', user_id, 'GENERATE', token_id, status)

    def log_token_verification(self, user_id, token_id, status):
        """
        记录令牌验证事件
        """
        self.log_event('TOKEN_VERIFICATION', user_id, 'VERIFY', token_id, status)

    def log_data_access(self, user_id, data_key, action, status):
        """
        记录数据访问事件
        """
        self.log_event('DATA_ACCESS', user_id, action, data_key, status)

    def log_encryption(self, user_id, data_key, status):
        """
        记录加密事件
        """
        self.log_event('ENCRYPTION', user_id, 'ENCRYPT', data_key, status)

    def log_decryption(self, user_id, data_key, status):
        """
        记录解密事件
        """
        self.log_event('DECRYPTION', user_id, 'DECRYPT', data_key, status)

    def log_error(self, error_message, details=None):
        """
        记录错误事件
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': 'ERROR',
            'message': error_message
        }

        if details:
            log_entry['details'] = details

        self.logger.error(json.dumps(log_entry))