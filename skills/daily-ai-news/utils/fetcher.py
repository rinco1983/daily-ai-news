"""内容抓取模块 - 从科技媒体 RSS 抓取 AI 相关新闻"""
import os
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from translator import MockTranslator


class TechNewsFetcher:
    """科技新闻内容抓取器"""
    """科技新闻内容抓取器"""

    def __init__(self):
        # 科技媒体 RSS 源
        self.rss_sources = [
            {
                "name": "TechCrunch",
                "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
                "category": "科技媒体"
            },
            {
                "name": "The Verge",
                "url": "https://www.theverge.com/rss/artificial-intelligence/index.xml",
                "category": "科技媒体"
            },
            {
                "name": "VentureBeat",
                "url": "https://venturebeat.com/category/ai/feed/",
                "category": "科技媒体"
            },
            {
                "name": "MIT Technology Review",
                "url": "https://www.technologyreview.com/feed/",
                "category": "科技媒体"
            },
            {
                "name": "AI News",
                "url": "https://artificialintelligence-news.com/feed/",
                "category": "AI 专业"
            }
        ]

        # AI 相关关键词（用于过滤）
        self.ai_keywords = [
            "AI", "artificial intelligence", "人工智能", "machine learning", "机器学习",
            "deep learning", "深度学习", "neural network", "神经网络", "LLM", "GPT",
            "Claude", "ChatGPT", "openai", "google deepmind", "gemini", "copilot",
            "midjourney", "stable diffusion", "diffusion model", "transformer",
            "generative", "生成式", "reinforcement learning", "强化学习",
            "computer vision", "nlp", "natural language processing", "robotics",
            "autonomous", "automation", "智能", "大模型", "agentic", "多模态"
        ]

        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }

        # 翻译器
        self.translator = MockTranslator()

    def _is_ai_related(self, text: str) -> bool:
        """判断内容是否与 AI 相关"""
        if not text:
            return False
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in self.ai_keywords)

    def _fetch_rss(self, url: str) -> Optional[BeautifulSoup]:
        """获取 RSS feed"""
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, "xml")
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  获取 RSS 失败: {url[:50]}... - {e}")
            return None

    def _parse_rss_item(self, item, source_name: str) -> Optional[Dict]:
        """解析 RSS 单个条目"""
        try:
            # 提取基本信息
            title = item.find("title")
            link = item.find("link")
            description = item.find("description")
            pub_date = item.find("pubDate")
            author = item.find("author") or item.find("dc:creator")
            category = item.find("category")

            if not title or not link:
                return None

            title_text = title.get_text(strip=True)
            link_text = link.get_text(strip=True) or link.get("href", "")

            # 清理描述（移除 HTML 标签）
            desc_text = ""
            if description:
                desc_soup = BeautifulSoup(description.get_text(), "html.parser")
                desc_text = desc_soup.get_text(strip=True)[:500]  # 限制长度

            # 检查是否与 AI 相关
            if not self._is_ai_related(title_text + " " + desc_text):
                return None

            # 解析发布时间
            pub_time = pub_date.get_text(strip=True) if pub_date else ""
            try:
                pub_dt = datetime.strptime(pub_time, "%a, %d %b %Y %H:%M:%S %z")
                pub_dt = pub_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
            except:
                pub_dt = pub_time

            # 生成中文翻译
            translations = self.translator.generate_chinese_translation(title_text, desc_text)

            return {
                "id": link_text.split("/")[-1][:50],
                "title": title_text,
                "title_cn": translations["title_cn"],
                "text": f"{title_text}\n\n{desc_text}",
                "text_cn": translations["text_cn"],
                "author": {
                    "id": source_name,
                    "username": source_name.lower().replace(" ", "_"),
                    "name": author.get_text(strip=True) if author else source_name,
                    "avatar": ""
                },
                "metrics": {
                    "like_count": 0,
                    "retweet_count": 0,
                    "reply_count": 0
                },
                "created_at": pub_dt,
                "url": link_text,
                "source": source_name,
                "category_text": category.get_text(strip=True) if category else ""
            }
        except Exception as e:
            print(f"   ⚠️  解析条目失败: {e}")
            return None

    def fetch_by_rss(self, date: datetime = None) -> List[Dict]:
        """使用 RSS 抓取内容"""
        date = date or datetime.now()
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)

        all_articles = []

        print(f"   开始抓取 {len(self.rss_sources)} 个 RSS 源...")

        for source in self.rss_sources:
            print(f"   📡 {source['name']}: ", end="", flush=True)
            soup = self._fetch_rss(source["url"])

            if not soup:
                print("失败")
                continue

            items = soup.find_all("item")
            count = 0

            for item in items:
                article = self._parse_rss_item(item, source["name"])
                if article:
                    all_articles.append(article)
                    count += 1

            print(f"成功，获取 {count} 篇")

        return all_articles

    def fetch_mock(self, date: datetime = None) -> List[Dict]:
        """模拟抓取（用于测试）"""
        date = date or datetime.now()
        date_str = date.strftime("%Y-%m-%d")

        # 模拟数据
        mock_articles = [
            {
                "id": f"1_{date_str}",
                "title": "GPT-5 Leaks: OpenAI's Next Model to Feature Real-Time Multimodal Understanding",
                "title_cn": "GPT-5 曝光：OpenAI 下一代模型将具备实时多模态理解能力",
                "text": "Reports indicate that GPT-5 will possess real-time multimodal understanding capabilities. This breakthrough could revolutionize how AI interacts with the world.",
                "text_cn": "消息称 GPT-5 将具备实时多模态理解能力。这一突破可能彻底改变 AI 与世界的互动方式。预计将在自然语言处理、图像识别和音频理解方面取得重大进展。",
                "author": {"id": "TechCrunch", "username": "techcrunch", "name": "TechCrunch", "avatar": ""},
                "metrics": {"like_count": 0, "retweet_count": 0, "reply_count": 0},
                "created_at": f"{date_str}T10:30:00Z",
                "url": "https://techcrunch.com/2026/02/11/gpt5-leaks/",
                "source": "TechCrunch",
                "category_text": "AI"
            },
            {
                "id": f"2_{date_str}",
                "title": "Claude Sonnet 4.5's Code Understanding Boosts Developer Productivity by 200%",
                "title_cn": "Claude Sonnet 4.5 的代码理解能力使开发者生产力提升 200%",
                "text": "Developers report significant productivity gains using Claude Sonnet 4.5 for coding tasks. The model's ability to understand and write complex code has improved dramatically.",
                "text_cn": "开发者报告使用 Claude Sonnet 4.5 进行编码任务时生产力显著提升。该模型理解和编写复杂代码的能力大幅提升，大大减少了开发时间和错误率。",
                "author": {"id": "The Verge", "username": "theverge", "name": "The Verge", "avatar": ""},
                "metrics": {"like_count": 0, "retweet_count": 0, "reply_count": 0},
                "created_at": f"{date_str}T09:15:00Z",
                "url": "https://www.theverge.com/2026/02/11/claude-sonnet-4-5-coding",
                "source": "The Verge",
                "category_text": "Technology"
            },
            {
                "id": f"3_{date_str}",
                "title": "Stable Diffusion 3.0 Released with Major Quality Improvements",
                "title_cn": "Stable Diffusion 3.0 发布，画质显著提升",
                "text": "Stability AI has released Stable Diffusion 3.0 with significant improvements in image quality and generation speed. The update includes new features for text rendering and composition.",
                "text_cn": "Stability AI 发布了 Stable Diffusion 3.0，在图像质量和生成速度方面有显著改进。更新包括文本渲染和构图的新功能，为创作者提供了更强大的工具。",
                "author": {"id": "VentureBeat", "username": "venturebeat", "name": "VentureBeat", "avatar": ""},
                "metrics": {"like_count": 0, "retweet_count": 0, "reply_count": 0},
                "created_at": f"{date_str}T11:45:00Z",
                "url": "https://venturebeat.com/2026/02/11/stable-diffusion-3-0/",
                "source": "VentureBeat",
                "category_text": "AI"
            },
            {
                "id": f"4_{date_str}",
                "title": "Breakthrough in LLM Inference Cost Optimization",
                "title_cn": "LLM 推理成本优化取得突破",
                "text": "New quantization techniques enable small language models to perform at the level of much larger ones. This could democratize access to powerful AI.",
                "text_cn": "新的量化技术使小型语言模型能够达到更大规模模型的效果。这可能普及对强大 AI 的访问，降低人工智能使用成本。",
                "author": {"id": "MIT Technology Review", "username": "mit_tech_review", "name": "MIT Technology Review", "avatar": ""},
                "metrics": {"like_count": 0, "retweet_count": 0, "reply_count": 0},
                "created_at": f"{date_str}T08:20:00Z",
                "url": "https://www.technologyreview.com/2026/02/11/llm-optimization/",
                "source": "MIT Technology Review",
                "category_text": "Research"
            },
            {
                "id": f"5_{date_str}",
                "title": "Google Gemini 2.5 Introduces Advanced Code Execution Capabilities",
                "title_cn": "Google Gemini 2.5 引入高级代码执行能力",
                "text": "Google's latest Gemini model can now execute Python code directly, providing developers with a powerful tool for data analysis and prototyping.",
                "text_cn": "Google 的最新 Gemini 模型现在可以直接执行 Python 代码，为开发者提供数据分析和原型设计的强大工具，大大提高了开发效率。",
                "author": {"id": "AI News", "username": "ai_news", "name": "AI News", "avatar": ""},
                "metrics": {"like_count": 0, "retweet_count": 0, "reply_count": 0},
                "created_at": f"{date_str}T12:00:00Z",
                "url": "https://artificialintelligence-news.com/2026/02/11/google-gemini-2-5/",
                "source": "AI News",
                "category_text": "AI"
            },
            {
                "id": f"6_{date_str}",
                "title": "Agentic AI Systems: The Next Frontier in Artificial Intelligence",
                "title_cn": "智能代理 AI 系统：人工智能的下一个前沿",
                "text": "Research shows that agentic AI systems capable of autonomous planning and execution are becoming increasingly sophisticated. This shift could transform enterprise automation.",
                "text_cn": "研究表明，能够自主规划和执行的智能代理 AI 系统正变得越来越复杂。这种转变可能会改变企业自动化，提高工作效率和决策质量。",
                "author": {"id": "The Verge", "username": "theverge", "name": "The Verge", "avatar": ""},
                "metrics": {"like_count": 0, "retweet_count": 0, "reply_count": 0},
                "created_at": f"{date_str}T13:30:00Z",
                "url": "https://www.theverge.com/2026/02/11/agentic-ai-systems/",
                "source": "The Verge",
                "category_text": "AI"
            },
            {
                "id": f"7_{date_str}",
                "title": "Multimodal AI Models Achieve Human-Level Performance on Complex Tasks",
                "title_cn": "多模态 AI 模型在复杂任务上达到人类水平表现",
                "text": "New benchmarks show that the latest multimodal AI models can match or exceed human performance on complex reasoning tasks that require understanding text, images, and audio simultaneously.",
                "text_cn": "最新的基准测试显示，最新的多模态 AI 模型可以在需要同时理解文本、图像和音频的复杂推理任务上匹配或超越人类表现，标志着人工智能的重大进步。",
                "author": {"id": "TechCrunch", "username": "techcrunch", "name": "TechCrunch", "avatar": ""},
                "metrics": {"like_count": 0, "retweet_count": 0, "reply_count": 0},
                "created_at": f"{date_str}T14:15:00Z",
                "url": "https://techcrunch.com/2026/02/11/multimodal-benchmark/",
                "source": "TechCrunch",
                "category_text": "AI"
            }
        ]

        return mock_articles

    def fetch(self, date: datetime = None, use_rss: bool = False) -> List[Dict]:
        """
        抓取内容

        Args:
            date: 目标日期
            use_rss: 是否使用 RSS（False 则使用模拟数据）
        """
        if use_rss:
            return self.fetch_by_rss(date)
        else:
            return self.fetch_mock(date)

    def save_to_file(self, articles: List[Dict], date: datetime = None) -> str:
        """保存到文件"""
        date = date or datetime.now()
        date_str = date.strftime("%Y-%m-%d")

        # 确保 data 目录存在
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(data_dir, exist_ok=True)

        filepath = os.path.join(data_dir, f"articles_{date_str}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "date": date_str,
                "count": len(articles),
                "articles": articles
            }, f, ensure_ascii=False, indent=2)

        return filepath


# 保留旧的类名作为别名，确保兼容性
TwitterFetcher = TechNewsFetcher


if __name__ == "__main__":
    # 测试
    fetcher = TechNewsFetcher()
    print("使用 RSS 抓取...")
    articles = fetcher.fetch(use_rss=True)
    print(f"抓取到 {len(articles)} 篇文章")
    filepath = fetcher.save_to_file(articles)
    print(f"保存到: {filepath}")
