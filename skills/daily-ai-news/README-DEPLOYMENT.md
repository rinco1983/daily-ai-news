# 🚀 每日 AI 速递 - Vercel 部署指南

## 部署前准备 ✅

### 已完成的准备工作：
- ✅ 项目结构调整完成
- ✅ API 端点实现
- ✅ 环境变量配置
- ✅ 依赖包安装
- ✅ 错误处理机制
- ✅ 定时任务配置

## 部署步骤 🔧

### 第 1 步：登录 Vercel

```bash
# 终端中运行
vercel login
```

按照提示完成登录过程。

### 第 2 步：初始化项目

```bash
# 自动检测项目结构
vercel init
```

选择配置：
- Framework Preset: `Other`
- Build Command: 留空（默认）
- Output Directory: 留空（默认）
- Install Command: `pip install -r requirements.txt`

### 第 3 步：设置环境变量

```bash
# 添加 RSS 源配置
vercel env add RSS_FEEDS

# 输入以下内容（JSON 格式）：
[
  {"name": "TechCrunch", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
  {"name": "The Verge", "url": "https://www.theverge.com/rss/artificial-intelligence/index.xml"},
  {"name": "VentureBeat", "url": "https://venturebeat.com/category/ai/feed/"},
  {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/feed/"}
]

# 添加缓存配置
vercel env add CACHE_TTL
# 输入：3600

vercel env add CACHE_KEY
# 输入：daily-ai-news
```

### 第 4 步：首次部署

```bash
vercel --prod
```

等待部署完成（约 1-2 分钟）。

### 第 5 步：验证部署

部署完成后，Vercel 会提供一个 URL。访问该 URL 验证：
- 页面正常显示
- 双语功能正常
- 深色模式切换正常
- 响应式设计正常

## 定时任务 ⏰

项目已自动配置每天上午 9 点更新：
```json
"crons": [
  {
    "path": "/api/cron",
    "schedule": "0 9 * * *"
  }
]
```

## 监控和维护 📊

### 查看日志
```bash
vercel logs
```

### 实时日志
```bash
vercel logs --follow
```

### 重新部署（更新代码后）
```bash
vercel --prod
```

## 常见问题 ❓

### Q: 部署失败？
A: 检查依赖安装：`pip install -r requirements.txt`

### Q: 数据不更新？
A: 清理缓存：`vercel domains --purge`

### Q: 页面显示错误？
A: 查看日志：`vercel logs`

### Q: 环境变量未生效？
A: 确认已添加并重新部署

## 成功标准 ✅

部署成功后，检查以下项目：
- [ ] 网站正常访问
- [ ] 显示 AI 新闻内容
- [ ] 双语功能正常
- [ ] 深色模式正常
- [ ] 定时任务执行

## 🎉 预期效果

部署完成后，您将获得：
- 🌐 一个完整的 AI 新闻网站
- 🌐 双语阅读体验
- 🌐 每日自动更新
- 🌐 专业的设计风格
- 🌐 完全免费的服务

---

**预计部署时间：15-30 分钟**
**维护成本：几乎为零**

准备好开始部署了吗？只需按照以上步骤操作即可！