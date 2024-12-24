import os
import json
import uuid
from secure_token_system import SecureTokenSystem


class MockFunctionContext:
    def __init__(self):
        self.request_id = str(uuid.uuid4())
        self.instance_id = f"instance-{uuid.uuid4().hex[:8]}"
        self.function_name = "test-function"
        self.function_handler = "index.handler"
        self.memory_limit_in_mb = 128
        self.time_limit_in_seconds = 3

    def get_request_id(self):
        return self.request_id

    def get_instance_id(self):
        return self.instance_id


class MockServerConfig:
    def __init__(self):
        self.sensitive_data = {
            "api_key": "very_secret_api_key",
            "database_password": "super_secure_password",
            "admin_token": "top_secret_admin_token"
        }


class MockServer:
    def __init__(self):
        self.config = MockServerConfig()
        self.secure_system = SecureTokenSystem()
        self.encrypted_data = {}

    def initialize(self):
        print("Server initializing...")
        context = MockFunctionContext()
        for key, value in self.config.sensitive_data.items():
            encrypted = self.secure_system.encrypt_data(value, f"server_admin-{context.get_instance_id()}")
            self.encrypted_data[key] = encrypted
        print("Server initialized with encrypted data.")


class MockClient:
    def __init__(self, secure_system):
        self.secure_system = secure_system
        self.user_id = "client_user_001"

    def request_data(self, data_key, server):
        context = MockFunctionContext()
        print(f"Client requesting data for key: {data_key}")
        print(f"Request ID: {context.get_request_id()}")
        print(f"Instance ID: {context.get_instance_id()}")

        token_data = self.secure_system.generate_token(
            context.get_request_id(),
            context.get_instance_id(),
            data_key,
            f"{self.user_id}-{context.get_instance_id()}"
        )

        is_valid = self.secure_system.verify_token(
            token_data['token'],
            context.get_request_id(),
            context.get_instance_id(),
            data_key,
            token_data['nonce'],
            token_data['timestamp'],
            f"{self.user_id}-{context.get_instance_id()}"
        )

        if is_valid:
            encrypted_data = server.encrypted_data.get(data_key)
            if encrypted_data:
                decrypted_data = self.secure_system.decrypt_data(
                    encrypted_data,
                    f"{self.user_id}-{context.get_instance_id()}"
                )
                print(f"Decrypted data for {data_key}: {decrypted_data}")
            else:
                print(f"No data found for key: {data_key}")
        else:
            print("Token verification failed.")


def run_test():
    secure_system = SecureTokenSystem()

    server = MockServer()
    server.initialize()

    client = MockClient(secure_system)

    # 模拟多次函数调用
    for _ in range(3):
        client.request_data("api_key", server)
        client.request_data("database_password", server)

    # 测试不存在的键
    client.request_data("non_existent_key", server)

    # 模拟不同实例的调用
    for _ in range(2):
        MockClient(secure_system).request_data("admin_token", server)


if __name__ == "__main__":
    run_test()