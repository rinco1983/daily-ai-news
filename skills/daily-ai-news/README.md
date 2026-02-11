# 每日 AI 速递 - ReadHub 风格版

## 设计理念

本项目采用 ReadHub 的设计风格，打造简洁、现代、高效的 AI 资讯聚合平台。设计特点包括：

- **简洁卡片式布局**：清晰的层次结构，突出重点信息
- **专业的配色方案**：深蓝色主色调，符合商业审美
- **流畅的交互体验**：hover 效果、过渡动画、深色模式
- **响应式设计**：完美适配桌面、平板、手机端

## 页面特色

### 1. 视觉设计
- **主色调**：`#086ad8` ReadHub 经典蓝
- **配色系统**：
  - 浅色模式：白色背景，灰色文字
  - 深色模式：深蓝背景，浅色文字
- **卡片阴影**：层次分明，悬浮效果
- **圆角设计**：统一 4px-8px 圆角

### 2. 交互功能
- **主题切换**：支持明暗主题一键切换
- **分类筛选**：可按文章分类快速筛选
- **来源筛选**：可按媒体来源筛选内容
- **悬浮效果**：卡片 hover 时微动画

### 3. 内容展示
- **来源标识**：每个文章显示来源图标
- **分类标签**：清晰的内容分类标识
- **热力指数**：AI 智能计算的热度分数
- **时间戳**：文章发布时间
- **摘要预览**：两行摘要，快速浏览

## 使用方法

### 命令行运行

```bash
# 生成每日 AI 速递（使用 RSS 真实数据）
python3 main.py --use-rss

# 指定输出路径
python3 main.py --use-rss --output /path/to/output.html

# 生成单文件版本（内联 CSS）
python3 main.py --use-rss --inline-css

# 生成最近 N 天汇总
python3 main.py --use-rss --summary 7
```

### 部署说明

1. **依赖安装**
```bash
pip install requests beautifulsoup4 jinja2
```

2. **配置 RSS 源**
在 `fetcher.py` 中添加新的 RSS 源：
```python
self.rss_sources = [
    {
        "name": "媒体名称",
        "url": "https://example.com/rss",
        "category": "分类名称"
    }
]
```

3. **自定义样式**
修改 `templates/readhub-style.html` 中的 CSS 变量来调整颜色主题

## 页面截图

### 浅色模式
![Light Mode](./docs/light-mode.png)

### 深色模式
![Dark Mode](./docs/dark-mode.png)

## 数据源

- **TechCrunch** - 全球科技媒体
- **The Verge** - 科技与生活
- **VentureBeat** - AI 专题
- **MIT Technology Review** - 学术前沿
- **AI News** - 专业 AI 媒体

## 技术栈

- **后端**：Python 3.9+
- **模板引擎**：Jinja2
- **HTML/CSS**：原生 CSS3 + CSS 变量
- **前端交互**：原生 JavaScript
- **数据抓取**：Requests + BeautifulSoup4

## 许可证

MIT License

---

*设计参考：[ReadHub](https://readhub.cn)*