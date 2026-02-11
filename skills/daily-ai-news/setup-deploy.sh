#!/bin/bash

# 自动部署脚本 - 每日 AI 速递

echo "🚀 每日 AI 速递 - 自动部署脚本"
echo "=================================="

# 检查必要工具
echo "🔍 检查环境..."
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI 未安装"
    echo "请运行: npm install -g vercel"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装"
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 未安装"
    exit 1
fi

# 检查必要文件
echo "📁 检查项目文件..."
required_files=(
    "vercel.json"
    "requirements.txt"
    "api/fetch-data.py"
    "api/generate-page.py"
    "templates/readhub-style.html"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ 缺少文件: $file"
        exit 1
    fi
done

echo "✅ 所有文件检查通过"

# 安装依赖
echo "📦 安装 Python 依赖..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi
echo "✅ 依赖安装完成"

# 检查 Vercel 登录状态
echo "🔐 检查 Vercel 登录状态..."
if ! vercel whoami &> /dev/null; then
    echo "🔒 请先登录 Vercel:"
    echo "   vercel login"
    echo ""
    read -p "登录完成后按回车继续..."
fi

# 初始化项目（如果需要）
if [ ! -f ".vercel" ]; then
    echo "🚀 初始化 Vercel 项目..."
    vercel init
    echo "✅ Vercel 项目初始化完成"
fi

# 提示设置环境变量
echo ""
echo "🌟 环境变量配置"
echo "=================="
echo "以下环境变量需要手动设置："
echo ""
echo "1. RSS_FEEDS"
echo "   类型: JSON Array"
echo "   内容: RSS 源列表"
echo ""
echo "2. CACHE_TTL"
echo "   类型: String"
echo "   值: 3600"
echo ""
echo "3. CACHE_KEY"
echo "   类型: String"
echo "   值: daily-ai-news"
echo ""
echo "请在终端中运行以下命令设置环境变量："
echo ""
echo "  vercel env add RSS_FEEDS"
echo "  vercel env add CACHE_TTL"
echo "  vercel env add CACHE_KEY"
echo ""

read -p "设置完成后按回车继续部署..."

# 部署到生产环境
echo "🚀 开始部署到生产环境..."
vercel --prod

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 部署成功！"
    echo ""
    echo "📋 后续步骤："
    echo "1. 复制 URL 并访问网站"
    echo "2. 测试所有功能"
    echo "3. 检查定时任务"
    echo "4. 设置监控（可选）"
    echo ""
    echo "📚 更多信息请查看："
    echo "   README-DEPLOYMENT.md"
    echo "   DEPLOYMENT_CHECKLIST.md"
    echo ""
    echo "💡 提示："
    echo "- 定时任务已配置，每天上午 9 点自动更新"
    echo "- 如需更新代码，再次运行: vercel --prod"
    echo "- 如有问题，运行: vercel logs 查看日志"
else
    echo "❌ 部署失败，请检查错误信息"
    exit 1
fi