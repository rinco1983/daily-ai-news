"""内容分析和分类模块"""
from typing import List, Dict, Tuple
from collections import Counter
import re


class ArticleAnalyzer:
    """文章分析器"""

    # 分类关键词映射
    CATEGORY_KEYWORDS = {
        "大模型": [
            "GPT", "Claude", "LLM", "大模型", "ChatGPT", "Gemini", "Qwen",
            "文心", "通义", "DeepSeek", "Kimi", "月之暗面", "智谱"
        ],
        "AI 绘画": [
            "Midjourney", "Stable Diffusion", "DALL-E", "AI 绘画", "AI 艺术",
            "文生图", "图生图", "ControlNet", "LoRA", "SDXL"
        ],
        "工具推荐": [
            "推荐", "工具", "插件", "扩展", "好用", "发现", "神器",
            "AI 工具", "效率", "助手", "自动化"
        ],
        "技术分享": [
            "代码", "教程", "实现", "原理", "源码", "论文", "研究",
            "算法", "架构", "部署", "训练", "微调"
        ],
        "行业新闻": [
            "发布", "融资", "收购", "合作", "上线", "发布", "新闻",
            "公告", "财报", "股价", "公司", "企业"
        ]
    }

    def __init__(self):
        pass

    def calculate_hot_score(self, tweet: Dict) -> float:
        """
        计算热度分数

        热度 = 点赞数 * 1 + 转发数 * 2 + 评论数 * 1.5
        """
        metrics = tweet.get("metrics", {})
        likes = metrics.get("like_count", 0)
        retweets = metrics.get("retweet_count", 0)
        replies = metrics.get("reply_count", 0)
        views = metrics.get("impression_count", 0)

        # 基础热度
        score = likes * 1 + retweets * 2 + replies * 1.5

        # 如果有浏览量，加入计算（可选）
        if views > 0:
            score += (views * 0.001)

        return score

    def categorize(self, tweet: Dict) -> Tuple[str, float]:
        """
        对博文进行分类

        Returns:
            (分类名称, 置信度)
        """
        text = tweet.get("text", "").lower()
        scores = {}

        for category, keywords in self.CATEGORY_KEYWORDS.items():
            score = 0
            for kw in keywords:
                if kw.lower() in text:
                    score += 1
            scores[category] = score

        # 找到分数最高的分类
        max_score = max(scores.values())
        if max_score > 0:
            for category, score in scores.items():
                if score == max_score:
                    # 简单的置信度计算
                    confidence = min(score / len(self.CATEGORY_KEYWORDS[category]) * 2, 1)
                    return category, confidence

        # 默认分类
        return "其他", 0

    def extract_tags(self, tweet: Dict) -> List[str]:
        """提取话题标签"""
        text = tweet.get("text", "")
        # 匹配 #hashtag 格式
        hashtags = re.findall(r'#(\w+)', text)
        return hashtags

    def extract_mentions(self, tweet: Dict) -> List[str]:
        """提取 @提及"""
        text = tweet.get("text", "")
        mentions = re.findall(r'@(\w+)', text)
        return mentions

    def extract_urls(self, tweet: Dict) -> List[str]:
        """提取链接"""
        text = tweet.get("text", "")
        urls = re.findall(r'https?://[^\s]+', text)
        return urls

    def analyze_batch(self, tweets: List[Dict]) -> Dict:
        """
        批量分析博文

        Returns:
            {
                "tweets": 分析后的博文列表,
                "stats": 统计信息,
                "top_tweets": 热门博文
            }
        """
        analyzed_tweets = []
        category_count = Counter()
        total_hot_score = 0

        for tweet in tweets:
            # 计算热度
            hot_score = self.calculate_hot_score(tweet)
            tweet["hot_score"] = hot_score
            total_hot_score += hot_score

            # 分类
            category, confidence = self.categorize(tweet)
            tweet["category"] = category
            tweet["category_confidence"] = confidence
            category_count[category] += 1

            # 提取标签等
            tweet["tags"] = self.extract_tags(tweet)
            tweet["mentions"] = self.extract_mentions(tweet)
            tweet["urls"] = self.extract_urls(tweet)

            analyzed_tweets.append(tweet)

        # 按热度排序
        analyzed_tweets.sort(key=lambda x: x.get("hot_score", 0), reverse=True)

        # 统计信息
        stats = {
            "total": len(tweets),
            "category_distribution": dict(category_count),
            "avg_hot_score": total_hot_score / len(tweets) if tweets else 0,
            "total_hot_score": total_hot_score
        }

        return {
            "tweets": analyzed_tweets,
            "stats": stats
        }

    def filter_by_category(self, analyzed: Dict, category: str) -> Dict:
        """按分类筛选"""
        filtered_tweets = [
            t for t in analyzed["tweets"]
            if t["category"] == category or t["category"].startswith(category)
        ]

        return {
            "tweets": filtered_tweets,
            "stats": {
                "total": len(filtered_tweets),
                "category": category
            }
        }

    def get_top_n(self, analyzed: Dict, n: int = 50) -> List[Dict]:
        """获取前 N 条热门博文"""
        return analyzed["tweets"][:n]


if __name__ == "__main__":
    # 测试
    from fetcher import TwitterFetcher
    import json

    fetcher = TwitterFetcher()
    tweets = fetcher.fetch(use_api=False)

    analyzer = TweetAnalyzer()
    result = analyzer.analyze_batch(tweets)

    print(f"分析完成，共 {result['stats']['total']} 条博文")
    print(f"分类分布: {result['stats']['category_distribution']}")
    print(f"平均热度: {result['stats']['avg_hot_score']:.1f}")
    print("\n热门博文:")
    for i, tweet in enumerate(result["tweets"][:5], 1):
        print(f"{i}. [{tweet['category']}] {tweet['text'][:50]}... (热度: {tweet['hot_score']:.1f})")
