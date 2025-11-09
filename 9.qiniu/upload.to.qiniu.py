# upload_to_qiniu.py
import os
import sys
from pathlib import Path
from qiniu import Auth, put_file, BucketManager, build_batch_stat
import logging

# ====== 配置区 ======
ACCESS_KEY = '_8Oc6nRUdP4vr3SkmRLImYWBZuxyi5JtS8NfIe72'
SECRET_KEY = 'Bcnodp9At74I4yDoCvrQOXGh_4sxhVrafjV85pIR'
BUCKET_NAME = 'qldzj'
LOCAL_DIR = 'pngs'          # 本地目录
LOG_FILE = 'uploaded_files.log'  # 记录已上传的文件（用于断点续传）
MAX_RETRIES = 3             # 上传失败重试次数
# ===================

# 初始化
q = Auth(ACCESS_KEY, SECRET_KEY)
bucket = BucketManager(q)

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("upload.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger()

# 读取已上传的文件列表（断点续传关键）
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        uploaded = set(line.strip() for line in f if line.strip())
else:
    uploaded = set()

def get_bucket_region(bucket_name):
    """自动探测 Bucket 所在区域（避免手动指定错误）"""
    from qiniu import CdnManager
    try:
        # 用 stat 接口探测
        ret, info = bucket.stat(bucket_name, 'probe-file')
        if info.status_code == 200 or info.status_code == 612:
            return None  # 使用默认区域（通常为华东 z0）
        elif info.status_code == 631:
            # 可能是其他区域，这里简化处理：默认用 z0（华东）
            return None
    except:
        pass
    return None  # 默认区域

def file_exists_in_bucket(key):
    """检查文件是否已存在于七牛云（通过 stat 接口）"""
    ret, info = bucket.stat(BUCKET_NAME, key)
    return info.status_code == 200

def upload_file(local_path, key):
    """上传单个文件，带重试"""
    if key in uploaded:
        logger.info(f"跳过（已记录）: {key}")
        return True

    # 可选：再检查一次远程是否存在（更保险）
    # if file_exists_in_bucket(key):
    #     logger.info(f"跳过（已存在）: {key}")
    #     with open(LOG_FILE, 'a', encoding='utf-8') as f:
    #         f.write(key + '\n')
    #     return True

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"上传 ({attempt}/{MAX_RETRIES}): {key}")
            ret, info = put_file(
                up_token=q.upload_token(BUCKET_NAME, key),
                key=key,
                file_path=local_path,
                version='v2'
            )
            if info.status_code == 200:
                with open(LOG_FILE, 'a', encoding='utf-8') as f:
                    f.write(key + '\n')
                logger.info(f"✅ 成功: {key}")
                return True
            else:
                logger.warning(f"上传失败 ({key}): {info.text}")
        except Exception as e:
            logger.error(f"异常 ({key}): {e}")
        if attempt < MAX_RETRIES:
            logger.info(f"等待后重试... ({key})")
            import time
            time.sleep(2 ** attempt)  # 指数退避

    logger.error(f"❌ 最终失败: {key}")
    return False

def main():
    local_root = Path(LOCAL_DIR)
    if not local_root.exists():
        logger.error(f"目录不存在: {LOCAL_DIR}")
        return

    all_files = []
    for file_path in local_root.rglob('*'):
        if file_path.is_file():
            # 生成七牛云的 key（相对路径，如 pngs/a/b.png）
            key = str(file_path.relative_to(local_root)).replace(os.sep, '/')
            all_files.append((str(file_path), key))

    logger.info(f"共发现 {len(all_files)} 个文件，开始上传...")

    success = 0
    for local_path, key in all_files:
        if upload_file(local_path, key):
            success += 1

    logger.info(f"上传完成！成功: {success}/{len(all_files)}")

if __name__ == '__main__':
    main()
