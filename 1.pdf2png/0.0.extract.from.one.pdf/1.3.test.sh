# 测试提取宽度
param_file="038-789.params"
width=$(awk '{for(i=1;i<=NF;i++) if($i=="-X") print $(i+1); exit}' "$param_file")
echo "提取的宽度: $width"  # 应该输出 1144
