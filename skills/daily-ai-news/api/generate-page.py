#!/usr/bin/env python3
"""
Vercel API - 页面生成端点
"""
import os
import json
import sys
import logging
from datetime import datetime

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.fetcher import TechNewsFetcher
from utils.analyzer import ArticleAnalyzer
from utils.renderer import WebRenderer

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handler(request):
    """Vercel 请求处理函数"""
    try:
        # 解析查询参数
        query = request.query
        use_rss = query.get('use_rss', 'true').lower() == 'true'
        limit = int(query.get('limit', 50))
        date = query.get('date')

        logger.info(f"开始生成页面，use_rss={use_rss}, limit={limit}")

        # 处理日期
        if date:
            from datetime import datetime
            target_date = datetime.strptime(date, '%Y-%m-%d')
        else:
            target_date = datetime.now()

        # 抓取数据
        fetcher = TechNewsFetcher()
        articles = fetcher.fetch(date=target_date, use_rss=(use_rss == 'true'))

        if not articles:
            # 返回默认页面
            return generate_error_page()

        # 分析数据
        analyzer = ArticleAnalyzer()
        result = analyzer.analyze_batch(articles)
        top_articles = analyzer.get_top_n(result, limit)

        # 渲染页面
        renderer = WebRenderer()
        output_path = f"/tmp/output-{datetime.now().strftime('%Y%m%d-%H%M%S')}.html"

        renderer.render(
            tweets=top_articles,
            stats=result["stats"],
            output_path=output_path,
            date=target_date,
            title="每日 AI 速递"
        )

        # 读取生成的 HTML
        with open(output_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 返回 HTML
        response = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html; charset=utf-8',
                'Access-Control-Allow-Origin': '*',
                'Cache-Control': 'public, max-age=1800'
            },
            'body': html_content
        }

        logger.info(f"页面生成成功，大小: {len(html_content)} 字节")
        return response

    except Exception as e:
        logger.error(f"生成页面失败: {str(e)}")
        return generate_error_page()

def generate_error_page():
    """生成错误页面"""
    html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日 AI 速递</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f7f8fa;
            color: #333;
            padding: 40px 20px;
            text-align: center;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        h1 {
            color: #086ad8;
            margin-bottom: 20px;
        }
        .retry-btn {
            background: #086ad8;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 20px;
        }
        .retry-btn:hover {
            background: #0551a5;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 每日 AI 速递</h1>
        <p>抱歉，页面生成时出现了错误。</p>
        <p>请稍后重试或联系管理员。</p>
        <button class="retry-btn" onclick="location.reload()">重新加载</button>
    </div>
    <script>
        // 5秒后自动重试
        setTimeout(() => {
            location.reload();
        }, 5000);
    </script>
</body>
</html>
"""
    return {
        'statusCode': 500,
        'headers': {
            'Content-Type': 'text/html; charset=utf-8'
        },
        'body': html
    }