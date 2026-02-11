#!/usr/bin/env python3
"""
Vercel API - 数据抓取端点
"""
import os
import json
import sys
import logging
from datetime import datetime
from urllib.parse import unquote

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.fetcher import TechNewsFetcher
from utils.analyzer import ArticleAnalyzer

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

        logger.info(f"开始抓取数据，use_rss={use_rss}, limit={limit}")

        # 抓取数据
        fetcher = TechNewsFetcher()
        articles = fetcher.fetch(use_rss=(use_rss == 'true'))

        if not articles:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'No articles found'})
            }

        # 分析数据
        analyzer = ArticleAnalyzer()
        result = analyzer.analyze_batch(articles)

        # 返回结果
        response = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST',
                'Cache-Control': 'public, max-age=3600'
            },
            'body': json.dumps({
                'success': True,
                'data': {
                    'articles': result['tweets'][:limit],
                    'stats': result['stats'],
                    'timestamp': datetime.utcnow().isoformat()
                },
                'count': len(result['tweets'])
            }, ensure_ascii=False)
        }

        logger.info(f"成功抓取 {len(response['body'])} 篇文章")
        return response

    except Exception as e:
        logger.error(f"抓取数据失败: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'success': False,
                'error': str(e)
            })
        }