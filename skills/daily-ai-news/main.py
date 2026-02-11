#!/usr/bin/env python3
"""每日 AI 速递 - 主入口"""
import os
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(__file__))

from fetcher import TechNewsFetcher
from analyzer import ArticleAnalyzer
from renderer import WebRenderer


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="每日 AI 速递 - 生成 AI 资讯网页")

    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="目标日期，格式: YYYY-MM-DD，默认为今天"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="输出文件路径，默认为 output/YYYY-MM-DD.html"
    )
    parser.add_argument(
        "--category",
        type=str,
        default=None,
        help="只包含指定分类的内容"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="最大博文数量，默认: 50"
    )
    parser.add_argument(
        "--use-rss",
        action="store_true",
        help="使用 RSS 抓取真实数据"
    )
    parser.add_argument(
        "--inline-css",
        action="store_true",
        help="生成单文件 HTML（内联 CSS）"
    )
    parser.add_argument(
        "--summary",
        type=int,
        default=None,
        help="生成最近 N 天的汇总页面"
    )
    parser.add_argument(
        "--title",
        type=str,
        default="每日 AI 速递",
        help="页面标题"
    )

    return parser.parse_args()


def get_output_path(date: datetime, custom_path: str = None) -> Path:
    """获取输出文件路径"""
    if custom_path:
        return Path(custom_path)

    # 默认输出到 output 目录
    output_dir = Path(__file__).parent.parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    date_str = date.strftime("%Y-%m-%d")
    return output_dir / f"daily-ai-news-{date_str}.html"


def generate_daily_news(args):
    """生成每日 AI 速递"""
    # 解析日期
    if args.date:
        date = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        date = datetime.now()

    print(f"📅 生成日期: {date.strftime('%Y-%m-%d')}")

    # 1. 抓取内容
    print("🔍 正在从科技媒体抓取 AI 新闻...")
    fetcher = TechNewsFetcher()
    articles = fetcher.fetch(date=date, use_rss=args.use_rss)
    print(f"   抓取到 {len(articles)} 篇文章")

    if not articles:
        print("⚠️  没有抓取到文章，请稍后重试")
        return None

    # 2. 分析内容
    print("📊 正在分析内容...")
    analyzer = ArticleAnalyzer()
    result = analyzer.analyze_batch(articles)
    print(f"   分析完成")
    print(f"   分类分布: {result['stats']['category_distribution']}")
    print(f"   平均热度: {result['stats']['avg_hot_score']:.1f}")

    # 3. 分类筛选
    if args.category:
        print(f"🏷️  筛选分类: {args.category}")
        result = analyzer.filter_by_category(result, args.category)
        print(f"   筛选后剩余 {len(result['tweets'])} 条博文")

    # 4. 获取前 N 条
    top_articles = analyzer.get_top_n(result, args.limit)
    print(f"📝 选择前 {len(top_articles)} 篇热门文章")

    # 5. 渲染网页
    print("🎨 正在生成网页...")
    renderer = WebRenderer()

    output_path = get_output_path(date, args.output)

    if args.inline_css:
        # 生成单文件 HTML
        html_content = generate_inline_html(top_articles, result["stats"], date, args.title)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
    else:
        # 使用模板渲染
        renderer.render(
            tweets=top_articles,
            stats=result["stats"],
            output_path=str(output_path),
            date=date,
            title=args.title
        )

    print(f"✅ 网页已生成: {output_path.absolute()}")
    return output_path


def generate_inline_html(tweets, stats, date, title):
    """生成内联 CSS 的单文件 HTML"""
    from renderer import generate_inline_css

    date_str = date.strftime("%Y-%m-%d")
    date_display = date.strftime("%Y年%m月%d日")

    # 文章列表 HTML
    articles_html = ""
    for article in tweets:
        source = article.get('source', article.get('author', {}).get('name', 'Unknown'))
        articles_html += f"""
        <div class="article-card" data-category="{article.get('category', '')}" data-source="{source}">
            <div class="article-header">
                <div class="article-source">{source}</div>
                <span class="article-category">{article.get('category', '其他')}</span>
            </div>

            <h3 class="article-title">{article.get('title', article.get('text', ''))[:100]}</h3>

            <div class="article-content">
                {article.get('text', '')}
            </div>

            <div class="article-metrics">
                <span class="article-time">{article.get('created_at', '')[:10] if article.get('created_at') else ''}</span>
                <a href="{article.get('url', '#')}" class="article-link" target="_blank">阅读全文 →</a>
            </div>
        </div>
        """

    # 完整 HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - {date_display}</title>
    {generate_inline_css()}
</head>
<body>
    <div class="container">
        <header>
            <div class="header-left">
                <h1>{title}</h1>
                <div class="date">{date_display}</div>
            </div>
            <button class="theme-toggle" onclick="toggleTheme()">🌓 切换主题</button>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="label">今日文章</div>
                <div class="value">{stats['total']}</div>
            </div>
            <div class="stat-card">
                <div class="label">平均热度</div>
                <div class="value">{stats['avg_hot_score']:.1f}</div>
            </div>
            <div class="stat-card">
                <div class="label">分类数量</div>
                <div class="value">{len(stats['category_distribution'])}</div>
            </div>
        </div>

        <div class="category-filter">
            <span class="category-tag active" onclick="filterCategory('全部', '全部')">全部</span>
            <span class="category-tag" onclick="filterCategory('大模型', '全部')">大模型</span>
            <span class="category-tag" onclick="filterCategory('AI 绘画', '全部')">AI 绘画</span>
            <span class="category-tag" onclick="filterCategory('工具推荐', '全部')">工具推荐</span>
            <span class="category-tag" onclick="filterCategory('技术分享', '全部')">技术分享</span>
            <span class="category-tag" onclick="filterCategory('行业新闻', '全部')">行业新闻</span>
            <span class="category-tag" onclick="filterCategory('其他', '全部')">其他</span>
        </div>

        <div class="source-filter">
            <span class="source-label">来源:</span>
            <span class="source-tag active" onclick="filterSource('全部', '全部')">全部</span>
            <span class="source-tag" onclick="filterSource('TechCrunch', '全部')">TechCrunch</span>
            <span class="source-tag" onclick="filterSource('The Verge', '全部')">The Verge</span>
            <span class="source-tag" onclick="filterSource('VentureBeat', '全部')">VentureBeat</span>
            <span class="source-tag" onclick="filterSource('MIT Technology Review', '全部')">MIT Tech Review</span>
        </div>

        <div class="article-list">
            {articles_html}
        </div>

        <footer>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>数据来源: TechCrunch, The Verge, VentureBeat, MIT Technology Review | 每日 AI 速递</p>
        </footer>
    </div>

    <script>
        let currentCategory = '全部';
        let currentSource = '全部';

        function toggleTheme() {{
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
        }}
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') document.body.classList.add('dark-mode');

        function filterCategory(category, source) {{
            currentCategory = category;
            applyFilters();

            const tags = document.querySelectorAll('.category-tag');
            tags.forEach(tag => tag.classList.remove('active'));
            event.target.classList.add('active');
        }}

        function filterSource(source, category) {{
            currentSource = source;
            applyFilters();

            const tags = document.querySelectorAll('.source-tag');
            tags.forEach(tag => tag.classList.remove('active'));
            event.target.classList.add('active');
        }}

        function applyFilters() {{
            const cards = document.querySelectorAll('.article-card');
            cards.forEach(card => {{
                const categoryMatch = currentCategory === '全部' || card.dataset.category === currentCategory;
                const sourceMatch = currentSource === '全部' || card.dataset.source === currentSource;
                card.style.display = (categoryMatch && sourceMatch) ? 'block' : 'none';
            }});
        }}
    </script>
</body>
</html>"""

    return html


def generate_summary(args):
    """生成多日汇总页面"""
    days = args.summary or 7
    print(f"📊 生成最近 {days} 天的汇总页面...")

    fetcher = TechNewsFetcher()
    analyzer = ArticleAnalyzer()
    renderer = WebRenderer()

    daily_data = []
    end_date = datetime.now()

    for i in range(days):
        date = end_date - timedelta(days=i)
        print(f"   处理日期: {date.strftime('%Y-%m-%d')}")

        # 尝试从文件加载，如果没有则抓取
        data_file = Path(__file__).parent / "data" / f"articles_{date.strftime('%Y-%m-%d')}.json"

        if data_file.exists():
            import json
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                articles = data.get("articles", [])
        else:
            articles = fetcher.fetch(date=date, use_rss=args.use_rss)

        if articles:
            result = analyzer.analyze_batch(articles)
            daily_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "date_display": date.strftime("%m月%d日"),
                "articles": analyzer.get_top_n(result, 20),  # 每天取前20条
                "stats": result["stats"]
            })

    if not daily_data:
        print("⚠️  没有找到数据")
        return None

    # 输出路径
    output_dir = Path(__file__).parent.parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"daily-ai-news-summary-{days}days.html"

    print(f"🎨 正在生成汇总网页...")
    renderer.render_summary(daily_data, str(output_path), days)

    print(f"✅ 汇总网页已生成: {output_path.absolute()}")
    return output_path


def main():
    """主函数"""
    args = parse_args()

    print("🤖 每日 AI 速递")
    print("=" * 50)

    if args.summary:
        generate_summary(args)
    else:
        generate_daily_news(args)

    print("\n✨ 完成!")


if __name__ == "__main__":
    main()
