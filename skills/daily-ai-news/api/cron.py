#!/usr/bin/env python3
"""
Vercel 定时任务 - 每日更新数据
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

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handler(request):
    """定时任务处理函数"""
    try:
        logger.info("开始执行每日更新任务")

        # 抓取最新数据
        fetcher = TechNewsFetcher()
        articles = fetcher.fetch(use_rss=True)

        if not articles:
            logger.warning("未抓取到新文章")
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'success': False,
                    'message': 'No articles fetched',
                    'timestamp': datetime.utcnow().isoformat()
                })
            }

        # 分析数据
        analyzer = ArticleAnalyzer()
        result = analyzer.analyze_batch(articles)

        # 保存数据到缓存（如果需要）
        # 这里可以添加缓存逻辑

        logger.info(f"成功更新 {len(result['tweets'])} 篇文章")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                'message': 'Daily update completed',
                'count': len(result['tweets']),
                'stats': result['stats'],
                'timestamp': datetime.utcnow().isoformat()
            })
        }

    except Exception as e:
        logger.error(f"定时任务执行失败: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'success': False,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            })
        }