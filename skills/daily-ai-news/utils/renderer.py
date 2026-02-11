"""网页渲染模块"""
import os
from datetime import datetime
from typing import List, Dict, Optional
from jinja2 import Template, Environment, FileSystemLoader


class WebRenderer:
    """网页渲染器"""

    def __init__(self, template_dir: Optional[str] = None):
        if template_dir is None:
            # 默认使用当前目录下的 templates
            template_dir = os.path.join(os.path.dirname(__file__), "templates")

        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True
        )

        # 注册自定义过滤器
        self.env.filters['format_number'] = self._format_number
        self.env.filters['format_time'] = self._format_time
        self.env.filters['format_number'] = self._format_number

    def _format_number(self, num: int) -> str:
        """格式化数字（如 1.2K）"""
        if num >= 1000000:
            return f"{num / 1000000:.1f}M"
        elif num >= 1000:
            return f"{num / 1000:.1f}K"
        return str(num)

    def _format_time(self, time_str: str) -> str:
        """格式化时间"""
        try:
            dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
            return dt.strftime("%H:%M")
        except:
            return time_str

    def render(
        self,
        tweets: List[Dict],
        stats: Dict,
        output_path: str,
        date: Optional[datetime] = None,
        title: str = "每日 AI 速递"
    ) -> str:
        """
        渲染网页

        Args:
            tweets: 博文列表
            stats: 统计信息
            output_path: 输出文件路径
            date: 日期
            title: 页面标题

        Returns:
            输出文件路径
        """
        date = date or datetime.now()
        date_str = date.strftime("%Y-%m-%d")
        date_display = date.strftime("%Y年%m月%d日")

        # 加载模板 - 优先使用 ReadHub 风格
        try:
            template = self.env.get_template("readhub-style.html")
        except:
            template = self.env.get_template("index.html")

        # 准备模板数据
        context = {
            "title": title,
            "date": date_str,
            "date_display": date_display,
            "tweets": tweets,
            "stats": stats,
            "now": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "categories": [
                "大模型", "AI 绘画", "工具推荐", "技术分享", "行业新闻", "其他"
            ]
        }

        # 渲染
        html = template.render(context)

        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # 写入文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        return output_path

    def render_summary(
        self,
        daily_data: List[Dict],
        output_path: str,
        days: int = 7
    ) -> str:
        """
        渲染多日汇总页面

        Args:
            daily_data: 每日数据列表，每项包含 {date, tweets, stats}
            output_path: 输出文件路径
            days: 汇总天数
        """
        template = self.env.get_template("summary.html")

        context = {
            "title": f"最近 {days} 天 AI 速递汇总",
            "days": days,
            "daily_data": daily_data,
            "now": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_tweets": sum(d.get("count", len(d.get("tweets", []))) for d in daily_data)
        }

        html = template.render(context)

        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        return output_path


def generate_inline_css() -> str:
    """生成内联 CSS（用于单文件输出）"""
    return """
    <style>
        /* CSS 变量 - 支持主题切换 */
        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f8f9fa;
            --bg-card: #ffffff;
            --text-primary: #1a1a1a;
            --text-secondary: #6c757d;
            --accent: #1da1f2;
            --accent-hover: #0c85d0;
            --border: #e1e8ed;
            --shadow: rgba(0, 0, 0, 0.08);
            --shadow-hover: rgba(0, 0, 0, 0.12);
        }

        .dark-mode {
            --bg-primary: #15202b;
            --bg-secondary: #192734;
            --bg-card: #1c2938;
            --text-primary: #f7f9f9;
            --text-secondary: #8b98a5;
            --accent: #1da1f2;
            --accent-hover: #1a91da;
            --border: #38444d;
            --shadow: rgba(0, 0, 0, 0.3);
            --shadow-hover: rgba(0, 0, 0, 0.4);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            transition: background 0.3s, color 0.3s;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        /* 页头 */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
            border-bottom: 1px solid var(--border);
            margin-bottom: 30px;
        }

        .header-left h1 {
            font-size: 2rem;
            color: var(--text-primary);
        }

        .header-left .date {
            color: var(--text-secondary);
            margin-top: 5px;
        }

        .theme-toggle {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            color: var(--text-primary);
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.3s;
        }

        .theme-toggle:hover {
            background: var(--border);
        }

        /* 统计卡片 */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: var(--bg-card);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px var(--shadow);
            border: 1px solid var(--border);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px var(--shadow-hover);
        }

        .stat-card .label {
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-bottom: 8px;
        }

        .stat-card .value {
            font-size: 1.8rem;
            font-weight: bold;
            color: var(--accent);
        }

        /* 分类标签 */
        .category-filter {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }

        .category-tag {
            padding: 6px 14px;
            border-radius: 16px;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s;
            border: 1px solid var(--border);
            background: var(--bg-secondary);
            color: var(--text-primary);
        }

        .category-tag.active,
        .category-tag:hover {
            background: var(--accent);
            color: white;
            border-color: var(--accent);
        }

        /* 博文卡片 */
        .tweet-list {
            display: grid;
            gap: 20px;
        }

        .tweet-card {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px var(--shadow);
            border: 1px solid var(--border);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .tweet-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px var(--shadow-hover);
        }

        .tweet-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }

        .tweet-avatar {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: var(--bg-secondary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            color: var(--accent);
        }

        .tweet-author {
            flex: 1;
        }

        .tweet-author .name {
            font-weight: 600;
            color: var(--text-primary);
        }

        .tweet-author .username {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .tweet-category {
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8rem;
            background: var(--bg-secondary);
            color: var(--accent);
        }

        .tweet-content {
            color: var(--text-primary);
            margin-bottom: 12px;
            line-height: 1.7;
        }

        .tweet-tags {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 12px;
        }

        .tweet-tag {
            color: var(--accent);
            font-size: 0.9rem;
        }

        .tweet-metrics {
            display: flex;
            gap: 20px;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .metric {
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .tweet-link {
            margin-left: auto;
            color: var(--accent);
            text-decoration: none;
            font-size: 0.9rem;
            transition: color 0.3s;
        }

        .tweet-link:hover {
            color: var(--accent-hover);
            text-decoration: underline;
        }

        /* 页脚 */
        footer {
            text-align: center;
            padding: 40px 0;
            color: var(--text-secondary);
            border-top: 1px solid var(--border);
            margin-top: 50px;
        }

        /* 响应式 */
        @media (max-width: 768px) {
            header {
                flex-direction: column;
                gap: 15px;
                text-align: center;
            }

            .stats-grid {
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            }

            .tweet-metrics {
                flex-wrap: wrap;
            }
        }
    </style>
    """


if __name__ == "__main__":
    # 测试
    print("请通过 main.py 运行")
