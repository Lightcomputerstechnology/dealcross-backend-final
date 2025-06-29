import os
import re

# Mappings of old (uppercase) to new (snake_case)
replacements = {
    r'settings\.SECRET_KEY': 'settings.secret_key',
    r'settings\.ALGORITHM': 'settings.algorithm',
    r'settings\.ACCESS_TOKEN_EXPIRE_MINUTES': 'settings.access_token_expire_minutes',
    r'settings\.REDIS_URL': 'settings.redis_url',
    r'settings\.SMTP_SERVER': 'settings.smtp_server',
    r'settings\.SMTP_PORT': 'settings.smtp_port',
    r'settings\.SMTP_USERNAME': 'settings.smtp_username',
    r'settings\.SMTP_PASSWORD': 'settings.smtp_password',
    r'settings\.SMTP_FROM': 'settings.smtp_from',
}

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    for pattern, replacement in replacements.items():
        new_content = re.sub(pattern, replacement, new_content)

    if new_content != content:
        backup_path = file_path + '.bak'
        os.rename(file_path, backup_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Fixed: {file_path} (backup saved as {backup_path})")

def scan_and_fix(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                fix_file(file_path)

if __name__ == "__main__":
    project_dir = "."  # Current directory; change if needed
    scan_and_fix(project_dir)
    print("✅ All applicable settings references have been fixed across your project.")