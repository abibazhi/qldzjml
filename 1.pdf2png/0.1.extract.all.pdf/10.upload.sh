#!/usr/bin/env bash

# =============== 配置区 ===============
LOCAL_DIR="pngs"                    # 本地目录
REMOTE_HOST="daxumi.cn"             # 远程服务器
REMOTE_USER="jm"         # 你的用户名（替换！）
REMOTE_DIR="pngs"   # 远程目标目录（替换！）
SSH_PORT="22"                       # SSH 端口，如非默认请修改
# =====================================

# 检查本地目录
if [[ ! -d "$LOCAL_DIR" ]]; then
    echo "❌ 本地目录不存在: $LOCAL_DIR"
    exit 1
fi

echo "🚀 开始上传 $LOCAL_DIR/ 到 $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR"
echo "   按 Ctrl+C 可暂停，下次运行会继续"

# 使用 rsync 同步
rsync -avz --partial --progress --rsh="ssh -p $SSH_PORT" \
    "$LOCAL_DIR/" \
    "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"

# 解释参数：
# -a: 归档模式（保留权限、时间、符号链接等）
# -v: 详细输出
# -z: 压缩传输
# --partial: 保留中断的文件，支持续传
# --progress: 显示进度
# --rsh: 指定 SSH 命令和端口

if [[ $? -eq 0 ]]; then
    echo "✅ 上传完成！"
else
    echo "❌ 上传失败，请检查网络或权限"
fi
