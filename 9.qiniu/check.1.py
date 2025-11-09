# verify_qiniu_files_resume.py
import os
import sys
import time
from pathlib import Path
import requests
from urllib.parse import quote

# ====== 配置区 ======
LOCAL_DIR = 'pngs'
DOMAIN = 'http://t4dcar0rt.hd-bkt.clouddn.com'
TIMEOUT = 10
MAX_RETRIES = 3
CHECKPOINT_FILE = 'verified_files.log'  # 记录已验证成功的文件
ERROR_LOG = 'verify_errors.log'         # 记录验证失败的文件
# ===================

def safe_url_join(base, path):
    encoded_path = quote(path.replace(os.sep, '/'), safe='/')
    return f"{base.rstrip('/')}/{encoded_path}"

def check_file_with_retry(url, max_retries=MAX_RETRIES):
    """带重试和异常处理的文件检查"""
    for attempt in range(1, max_retries + 1):
        try:
            # 先用 HEAD
            resp = requests.head(url, timeout=TIMEOUT, allow_redirects=True)
            if resp.status_code == 200:
                return True, 200
            elif resp.status_code == 404:
                return False, 404
            elif resp.status_code == 403:
                return False, 403
            # 其他状态码继续重试
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            if attempt == max_retries:
                raise e  # 最后一次失败才抛出
            time.sleep(2 ** attempt)  # 指数退避
            continue

        # 如果 HEAD 不可靠，尝试 GET（只取头）
        try:
            resp = requests.get(url, timeout=TIMEOUT, stream=True)
            status = resp.status_code
            resp.close()
            if status == 200:
                return True, 200
            elif status == 404:
                return False, 404
            elif status == 403:
                return False, 403
        except Exception:
            pass

        if attempt < max_retries:
            time.sleep(2 ** attempt)

    return False, None  # 无法确定

def load_checkpoint():
    """加载已验证的文件集合"""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def log_success(key):
    with open(CHECKPOINT_FILE, 'a', encoding='utf-8') as f:
        f.write(key + '\n')

def log_error(key, error_type):
    with open(ERROR_LOG, 'a', encoding='utf-8') as f:
        f.write(f"{key}\t{error_type}\n")

def main():
    local_root = Path(LOCAL_DIR)
    if not local_root.exists():
        print(f"❌ 本地目录不存在: {LOCAL_DIR}")
        return

    # 获取所有文件（相对路径）
    all_files = []
    for file_path in local_root.rglob('*'):
        if file_path.is_file():
            rel_path = str(file_path.relative_to(local_root)).replace(os.sep, '/')
            all_files.append(rel_path)

    all_files.sort()
    total = len(all_files)
    print(f"🔍 共 {total} 个文件待验证")

    verified = load_checkpoint()
    print(f"✅ 已验证: {len(verified)} 个（从断点继续）")

    success = 0
    missing = []
    forbidden = []

    try:
        for i, rel_path in enumerate(all_files, 1):
            if rel_path in verified:
                success += 1
                continue

            url = safe_url_join(DOMAIN, rel_path)
            print(f"[{i}/{total}] 检查: {rel_path}")

            try:
                exists, status = check_file_with_retry(url)
                if exists:
                    log_success(rel_path)
                    success += 1
                    print(f"    ✅ OK")
                else:
                    if status == 404:
                        missing.append(rel_path)
                        log_error(rel_path, "404")
                        print(f"    ❌ 404")
                    elif status == 403:
                        forbidden.append(rel_path)
                        log_error(rel_path, "403")
                        print(f"    🔒 403")
                    else:
                        log_error(rel_path, "UNKNOWN")
                        print(f"    ⚠️ 未知状态")
            except Exception as e:
                print(f"    ⛔ 网络错误（可中断）: {e}")
                print("    💾 当前进度已保存，下次可继续")
                break  # 安全退出，不继续

    except KeyboardInterrupt:
        print("\n🛑 用户中断，进度已保存。")
        return

    # 最终汇总
    print("\n" + "="*60)
    print(f"✅ 验证完成！成功: {success}/{total}")
    print(f"❌ 缺失（404）: {len(missing)}")
    for f in missing[:10]:  # 只打印前10个
        print(f"  - {f}")
    if len(missing) > 10:
        print(f"  ... 还有 {len(missing)-10} 个")

    if forbidden:
        print(f"🔒 防盗链（403）: {len(forbidden)}")
        for f in forbidden[:5]:
            print(f"  - {f}")

    print(f"\n📝 详细错误见: {ERROR_LOG}")
    print(f"💾 断点记录: {CHECKPOINT_FILE}")
    print("="*60)

if __name__ == '__main__':
    main()
