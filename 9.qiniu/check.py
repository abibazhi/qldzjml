# verify_qiniu_files.py
import os
import sys
from pathlib import Path
import requests
from urllib.parse import quote

# ====== 配置区 ======
LOCAL_DIR = 'pngs'
DOMAIN = 'http://t4dcar0rt.hd-bkt.clouddn.com'  # 你的七牛外链域名
TIMEOUT = 10  # 请求超时（秒）
MAX_RETRIES = 2
# ===================

def safe_url_join(base, path):
    """安全拼接 URL，自动处理斜杠和编码"""
    # 七牛云 key 中的特殊字符（如空格、中文）需 URL 编码
    encoded_path = quote(path.replace(os.sep, '/'), safe='/')
    if base.endswith('/'):
        base = base.rstrip('/')
    return f"{base}/{encoded_path}"

def check_file_exists(url):
    """用 HEAD 检查文件是否存在"""
    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = requests.head(url, timeout=TIMEOUT, allow_redirects=True)
            if resp.status_code == 200:
                return True
            elif resp.status_code == 404:
                return False
            # 其他状态码（如 403）也视为异常
        except Exception as e:
            if attempt == MAX_RETRIES:
                print(f"⚠️  请求失败（{url}）: {e}")
                return False
            continue
    return False

def main():
    local_root = Path(LOCAL_DIR)
    if not local_root.exists():
        print(f"❌ 本地目录不存在: {LOCAL_DIR}")
        return

    all_files = []
    for file_path in local_root.rglob('*'):
        if file_path.is_file():
            rel_path = str(file_path.relative_to(local_root)).replace(os.sep, '/')
            all_files.append(rel_path)

    print(f"🔍 共发现 {len(all_files)} 个本地文件，开始验证...")

    missing = []
    error_403 = []
    success = 0

    for rel_path in sorted(all_files):
        url = safe_url_join(DOMAIN, rel_path)
        if check_file_exists(url):
            success += 1
            print(f"✅ OK: {rel_path}")
        else:
            # 再试一次用 GET（有些 CDN 对 HEAD 限制）
            try:
                resp = requests.get(url, timeout=TIMEOUT, stream=True)
                if resp.status_code == 200:
                    success += 1
                    print(f"✅ OK (via GET): {rel_path}")
                    resp.close()
                    continue
            except:
                pass

            if requests.head(url, timeout=TIMEOUT).status_code == 403:
                error_403.append(rel_path)
                print(f"❌ 403 Forbidden（可能防盗链）: {rel_path}")
            else:
                missing.append(rel_path)
                print(f"❌ 404 Not Found: {rel_path}")

    print("\n" + "="*50)
    print(f"✅ 成功: {success}")
    print(f"❌ 缺失（404）: {len(missing)}")
    for f in missing:
        print(f"  - {f}")
    if error_403:
        print(f"🔒 防盗链拦截（403）: {len(error_403)}")
        for f in error_403:
            print(f"  - {f}")
    print("="*50)

if __name__ == '__main__':
    main()
