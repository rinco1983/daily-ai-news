#!/bin/bash

# Vercel 部署脚本

echo "🚀 开始部署每日 AI 速递到 Vercel..."

# 检查环境
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI 未安装，请先安装："
    echo "   npm install -g vercel"
    exit 1
fi

# 检查必要文件
files=("vercel.json" "requirements.txt" "api/fetch-data.py" "api/generate-page.py" "utils/fetcher.py")
for file in "${files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ 缺少必要文件: $file"
        exit 1
    fi
done

echo "✅ 检查通过，开始部署..."

# 登录 Vercel
echo "🔐 请登录 Vercel..."
vercel login

# 部署到 Vercel
echo "📦 部署项目..."
vercel --prod

echo "🎉 部署完成！"
echo ""
echo "📋 后续步骤："
echo "1. 访问项目 URL"
echo "2. 配置环境变量（参考 .env.example）"
echo "3. 设置定时任务"
echo "4. 监控运行状态"
echo ""
echo "💡 提示："
echo "- 首次部署可能需要 1-2 分钟"
echo "- 如需更新，再次运行此脚本即可"