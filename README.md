# 60秒读懂世界企业微信推送脚本

本项目可自动获取「60秒读懂世界」新闻、历史上的今天、Epic 免费游戏信息，并推送到企业微信机器人。

## 功能简介
- 获取 https://60s.viki.moe/v2/60s 的每日新闻
- 获取历史上的今天事件
- 获取 Epic Games 免费游戏信息
- 自动生成 Markdown 消息并推送到企业微信机器人
- 支持 GitHub Actions 定时自动推送

## 使用方法

### 1. 克隆项目
```bash
git clone https://github.com/StefanoWen/60s-push.git
cd 60s-push
```

### 2. 安装依赖
```bash
pip install requests
```

### 3. 配置企业微信机器人 Webhook Key
编辑 `60s.py`，将如下内容：
```python
webhook_key = "YOUR_WEBHOOK_KEY_HERE"  # 替换为实际的webhook key
```
替换为你的企业微信机器人 webhook key。

### 4. 本地运行
```bash
python 60s.py
```

### 5. GitHub Actions 自动推送
- 在你的 GitHub 仓库设置中，添加名为 `WEBHOOK_KEY` 的 Secret，值为你的企业微信机器人 webhook key。
- Actions 会每天北京时间 10:00 自动运行并推送。

## 目录结构
```
60s.py                  # 主程序
.github/workflows/      # GitHub Actions 工作流
README.md               # 项目说明
```

## 注意事项
- 企业微信机器人消息有长度限制，脚本已自动优化消息长度。
- 若未配置 webhook key，脚本将以测试模式运行，仅输出 Markdown 内容。

## License
MIT
