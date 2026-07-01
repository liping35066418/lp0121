import re
import sys
import subprocess
import os

def validate_session_id(session_id):
    if not session_id:
        return False, "Session ID为空"
    
    pattern = r'^\.\d+:[0-9a-fA-F]+_[0-9a-fA-F]+\.[0-9a-fA-F]+\.[0-9a-fA-F]+:Trae CN\.T\(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{2}:\d{2}\)$'
    
    if re.match(pattern, session_id):
        return True, "验证通过"
    else:
        return False, f"格式不正确"

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def commit_with_validation(session_id):
    print("="*80)
    print("🔍 开始验证Session ID...")
    
    is_valid, message = validate_session_id(session_id)
    if not is_valid:
        print(f"❌ 验证失败: {message}")
        print(f"   输入的Session ID: {session_id}")
        print(f"   长度: {len(session_id)} 字符")
        print("="*80)
        return False
    
    print(f"✅ 验证通过")
    print(f"   Session ID长度: {len(session_id)} 字符")
    print(f"   Session ID: {session_id}")
    print("="*80)
    
    print("\n📦 执行 git add -A...")
    success, stdout, stderr = run_command("git add -A")
    if not success:
        print(f"❌ git add 失败: {stderr}")
        return False
    print("✅ git add 成功")
    
    print("\n📝 执行 git commit...")
    commit_cmd = f'git commit -m "{session_id}"'
    success, stdout, stderr = run_command(commit_cmd)
    if not success:
        print(f"❌ git commit 失败: {stderr}")
        return False
    print(f"✅ git commit 成功: {stdout.strip()}")
    
    print("\n🚀 执行 git push origin main...")
    success, stdout, stderr = run_command("git push origin main")
    if not success:
        print(f"❌ git push 失败: {stderr}")
        return False
    print(f"✅ git push 成功")
    
    print("\n📋 获取Commit ID...")
    success, stdout, stderr = run_command("git rev-parse HEAD")
    if not success:
        print(f"❌ 获取Commit ID失败: {stderr}")
        return False
    commit_id = stdout.strip()
    
    print("\n✅✅✅ 提交完成！")
    print(f"   Commit ID: {commit_id}")
    print(f"   提交信息长度: {len(session_id)} 字符")
    print("="*80)
    
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python3 commit_with_verify.py <session_id>")
        sys.exit(1)
    
    session_id = sys.argv[1]
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    success = commit_with_validation(session_id)
    sys.exit(0 if success else 1)