# 每日 AI 速递 (Daily AI News) Skill

## Description

每日 AI 速递是一个自动化的 AI 资讯收集和展示工具，从主流科技媒体（TechCrunch、The Verge、VentureBeat、MIT Technology Review 等）抓取 AI 相关新闻，精选热门内容，并生成精美的网页。

## Capabilities

- **内容抓取**: 从 X 平台抓取 AI 相关的中文博文
- **热度筛选**: 根据点赞数、转发数等指标筛选热门内容
- **智能分类**: 自动对抓取的内容进行分类（如：大模型、行业新闻、工具推荐等）
- **网页生成**: 生成精美的响应式网页，支持深色/浅色主题
- **历史存档**: 自动按日期存档每日内容

## Usage Examples

### Example 1: 生成今日 AI 速递

```
生成今日 AI 速递网页
```

### Example 2: 指定日期的速递

```
生成 2026-02-10 的 AI 速递网页
```

### Example 3: 指定分类筛选

```
生成今日 AI 速递，只包含大模型相关内容
```

### Example 4: 生成最近 7 天速递

```
生成最近 7 天的 AI 速递汇总页面
```

## Configuration

### 环境变量

在执行此 skill 前，可选设置以下环境变量：

```bash
# 输出目录
export DAILY_AI_NEWS_OUTPUT_DIR="/path/to/output"

# 抓取数量
export DAILY_AI_NEWS_LIMIT=50
```

### 命令行参数

- `--date`: 指定日期 (格式: YYYY-MM-DD)
- `--output`: 指定输出文件路径
- `--category`: 指定内容分类
- `--days`: 生成最近 N 天的汇总

## Dependencies

### Python 依赖

```python
requests>=2.31.0
beautifulsoup4>=4.12.0
jinja2>=3.1.0
```

### 安装

```bash
pip install requests beautifulsoup4 jinja2
```

## Output Format

生成的网页包含以下部分：

- **页头**: 标题、日期、主题切换按钮
- **统计**: 今日抓取数量、主要分类占比
- **内容列表**: 按热度排序的博文卡片
  - 作者信息
  - 博文内容（支持展开）
  - 热度指标（点赞、转发、评论）
  - 链接跳转
- **页脚**: 版权信息、历史归档链接

## Data Sources

- **TechCrunch** - AI 人工智能类别
- **The Verge** - AI 人工智能类别
- **VentureBeat** - AI 人工智能类别
- **MIT Technology Review** - 科技综合
- **AI News** - AI 专业媒体

所有 RSS 源会自动过滤 AI 相关内容。

## Implementation Notes

1. **抓取策略**:
   - 使用 RSS 源抓取科技媒体内容
   - 自动过滤 AI 相关新闻
   - 支持网络超时重试机制

2. **热度计算**:
   ```
   热度 = 点赞数 * 1 + 转发数 * 2 + 评论数 * 1.5
   ```

3. **分类规则**:
   - 大模型: 包含 "GPT"、"Claude"、"LLM"、"大模型" 等关键词
   - 行业新闻: 包含 "发布"、"融资"、"收购" 等关键词
   - 工具推荐: 包含 "推荐"、"工具"、"插件" 等关键词
   - 技术分享: 包含 "代码"、"教程"、"实现" 等关键词

4. **网页设计**:
   - 响应式布局（移动端适配）
   - CSS 变量支持主题切换
   - 卡片式设计，支持内容展开
   - 平滑滚动和过渡动画

## File Structure

```
skills/daily-ai-news/
├── SKILL.md           # 本文件
├── fetcher.py         # 内容抓取模块
├── analyzer.py        # 内容分析和分类
├── renderer.py        # 网页渲染
├── templates/         # Jinja2 模板
│   └── index.html
├── static/           # 静态资源
│   └── style.css
└── data/             # 存储抓取的数据
```

## Schedule

建议使用 cron 定时任务每日自动生成：

```bash
# 每天早上 8 点生成
0 8 * * * cd /path/to/skills/daily-ai-news && python main.py >> /var/log/daily-ai-news.log 2>&1
```

## License

MIT
