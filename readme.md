# Dynamic Token Encryption System for Serverless Architectures

> ⚠️ FOR EDUCATIONAL PURPOSES ONLY - This is a reference implementation for learning serverless security concepts. Production deployment requires thorough security review, proper key management integration, and code adaptation to match specific requirements and security standards.

## Important Disclaimer

**NOTE: This project is for educational purposes only. The code provided has not been integrated into any production system and should not be used as-is in a production environment without thorough security review and testing.**

For experimental environments:
1. In the initialization method, consider retrieving key information provided by the service provider.
2. Simulate the server-side encryption logic.
3. Remove any existing key information from environment variables.
4. Allow users to use the system normally after this setup.

In other words, users of this system in an experimental setting should simulate the encryption logic that would typically be performed by the service provider. This approach allows for a more realistic testing environment while maintaining the educational nature of the project.

Example of simulated initialization:

```python
def simulate_provider_initialization():
    # Simulate retrieving keys from a secure service
    provider_keys = get_mock_provider_keys()
    
    # Simulate server-side encryption
    encrypted_keys = encrypt_sensitive_data(provider_keys)
    
    # Remove original keys from environment
    for key in provider_keys:
        if key in os.environ:
            del os.environ[key]
    
    # Set encrypted keys in environment
    for key, value in encrypted_keys.items():
        os.environ[f"ENCRYPTED_{key}"] = value

    print("Simulated provider encryption completed.")

# Call this function before your actual initialization
simulate_provider_initialization()
```

This simulation helps in understanding the full lifecycle of key management and encryption in a serverless environment, while emphasizing that in a real-world scenario, these operations would be handled by the service provider's secure systems.

## Project Overview

This project implements a dynamic token encryption system designed to enhance data security in serverless architectures. It includes token generation, validation, data encryption/decryption, and audit logging functionalities.

## File Structure

- `token_generator.py`: Implements dynamic token generation and validation logic
- `encryption.py`: Handles data encryption and decryption
- `audit_logger.py`: Manages audit log recording
- `secure_token_system.py`: Core system integrating all module functionalities
- `test_secure_token_system.py`: Test file for the system

## Setup Guide

1. Install dependencies:
   ```
   pip install cryptography
   ```

2. Configure environment variables (optional):
   - `SECRET_KEY`: Key for token generation
   - `ENCRYPTION_KEY`: Key for data encryption
   - `LOG_LEVEL`: Logging level
   - `AUDIT_LOG_FILE`: Path for audit log file

3. Import and use in your code:
   ```python
   from secure_token_system import generate_token, verify_token, encrypt_data, decrypt_data

   # Usage examples
   token_data = generate_token(request_id, instance_id, data_key, user_id)
   is_valid = verify_token(token, request_id, instance_id, data_key, nonce, timestamp, user_id)
   encrypted = encrypt_data(sensitive_data, user_id)
   decrypted = decrypt_data(encrypted_data, user_id)
   ```

## Alibaba Cloud Function Compute Example

This example demonstrates how the system might be used in a serverless environment like Alibaba Cloud Function Compute. It covers the configuration, initialization, and usage phases.

### 1. User Configuration Phase

When creating a function, users configure the following to enable encryption:

1. Set environment variables:
   - `ENABLE_ENCRYPTION`: Set to "true" to enable encryption
   - `ENCRYPTION_KEYS`: Names of environment variables to encrypt, comma-separated

2. Set the initializer function in the function configuration

Example configuration (used when creating or updating the function):
```yaml
environmentVariables:
  ENABLE_ENCRYPTION: "true"
  ENCRYPTION_KEYS: "DB_PASSWORD,API_KEY,SECRET_TOKEN"
  DB_PASSWORD: "original_database_password"
  API_KEY: "original_api_key"
  SECRET_TOKEN: "original_secret_token"

initializer:
  handler: index.initialize
  initializer: index.initialize
```

### 2. Server-Side Initialization Phase

The server executes the following during function initialization:

```python
import os
from secure_token_system import SecureTokenSystem

secure_system = None
original_env = {}

def initialize(context):
    global secure_system, original_env
    secure_system = SecureTokenSystem()

    if os.environ.get('ENABLE_ENCRYPTION') == 'true':
        encryption_keys = os.environ.get('ENCRYPTION_KEYS', '').split(',')
        for key in encryption_keys:
            if key in os.environ:
                # Save original value
                original_env[key] = os.environ[key]
                # Encrypt environment variable
                encrypted_value = secure_system.encrypt_data(os.environ[key], 'server_admin')
                # Replace original env var with encrypted value
                os.environ[key] = encrypted_value

    print("Function initialized with encrypted environment variables.")

# Ensure initialization function is called when function instance is created
initialize(None)
```

This initialization process:
1. Checks if encryption is enabled
2. Encrypts specified environment variables
3. Replaces original environment variable values with encrypted ones

### 3. User Usage Phase

Users can use a helper function to get decrypted environment variables in their function:

```python
def get_decrypted_env(key):
    if key in os.environ:
        encrypted_value = os.environ[key]
        return secure_system.decrypt_data(encrypted_value, 'function_user')
    return None

def handler(event, context):
    # Usage example
    db_password = get_decrypted_env('DB_PASSWORD')
    api_key = get_decrypted_env('API_KEY')

    # User's business logic
    result = do_something_with_secrets(db_password, api_key)

    return {
        "statusCode": 200,
        "body": {
            "message": "Function executed successfully",
            "result": result
        }
    }

def do_something_with_secrets(db_password, api_key):
    # Actual business logic here
    return "Processed data using secrets"
```

In this example:

1. Users don't need to handle encryption and decryption logic directly.
2. The `get_decrypted_env` function encapsulates the decryption process, making it simple to use.
3. Users can use these encrypted values like regular environment variables, just through `get_decrypted_env`.

Important notes:
- This method protects sensitive information in environment variables. Even if someone can view the environment variables, they will only see encrypted values.
- Decryption occurs at runtime, ensuring sensitive information is only decrypted when needed.
- In a production environment, you should add more error handling and logging.
- Consider using Alibaba Cloud's Key Management Service (KMS) for enhanced security.

## Security Considerations

1. Server-side encryption/decryption:
   - In production, perform encryption and decryption operations in a trusted server-side environment.
   - Consider using Hardware Security Modules (HSM) or Key Management Services (KMS) for key storage and management.

2. Binary data protection:
   - For binary data, consider using specialized encryption algorithms and additional protection measures.
   - Use secure memory allocation and clearing techniques when handling sensitive data in memory.

3. Client-side usage:
   - Clients should only call secure API interfaces and not directly handle encryption logic.
   - Use HTTPS to ensure secure communication between client and server.

4. Key management:
   - Implement key rotation mechanisms.
   - Use secure methods for storing and transmitting keys, avoiding hardcoding.

5. Audit and monitoring:
   - Implement comprehensive logging and real-time monitoring systems.
   - Conduct regular security audits and penetration testing.

## Contribution

Issues and suggestions for improvements are welcome. If you want to contribute code, please open an issue first to discuss what you would like to change.
