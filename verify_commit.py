import re
import sys

def validate_session_id(session_id):
    if not session_id:
        return False, "Session ID为空"
    
    pattern = r'^\.\d+:[0-9a-fA-F]+_[0-9a-fA-F]+\.[0-9a-fA-F]+\.[0-9a-fA-F]+:Trae CN\.T\(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{2}:\d{2}\)$'
    
    if re.match(pattern, session_id):
        return True, "验证通过"
    else:
        return False, f"格式不正确，请检查Session ID格式。预期格式: .数字:十六进制_十六进制.十六进制.十六进制:Trae CN.T(YYYY/MM/DD HH:MM:SS)"

def commit_with_validation(session_id):
    is_valid, message = validate_session_id(session_id)
    if not is_valid:
        print(f"❌ 验证失败: {message}")
        print(f"   输入的Session ID: {session_id}")
        return False
    
    print(f"✅ 验证通过: {message}")
    print(f"   Session ID长度: {len(session_id)} 字符")
    print(f"   Session ID: {session_id}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python verify_commit.py <session_id>")
        sys.exit(1)
    
    session_id = sys.argv[1]
    success = commit_with_validation(session_id)
    sys.exit(0 if success else 1)