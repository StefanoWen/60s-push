# 60秒读懂世界企业微信推送脚本

这是一个Python脚本，用于自动获取"60秒读懂世界"的新闻数据，并通过企业微信机器人推送到群聊。

## 功能特点

- 使用 `httpie` 命令行工具获取API数据
- 解析JSON响应并构建企业微信markdown格式消息
- 支持测试模式，可以预览生成的markdown内容
- 完整的错误处理和日志输出

## 安装依赖

确保已安装以下工具：

```bash
# 安装 httpie
pip3 install httpie

# 或者使用包管理器安装
# macOS: brew install httpie
# Ubuntu/Debian: sudo apt-get install httpie
```

## 配置使用

1. **获取企业微信机器人webhook key**：
   - 在企业微信中创建一个群聊
   - 添加群机器人，获取webhook URL中的key参数

2. **修改脚本配置**：
   打开 `60s.py` 文件，找到以下行并替换为你的webhook key：

   ```python
   webhook_key = "YOUR_WEBHOOK_KEY_HERE"  # 替换为实际的webhook key
   ```

3. **运行脚本**：
   ```bash
   cd /Users/PINES/Desktop/toolbox/documents/research/60s
   python3 60s.py
   ```

## 测试模式

如果没有配置webhook key，脚本会自动进入测试模式，仅显示生成的markdown内容而不实际发送。

## 定时执行

可以使用crontab设置定时任务，例如每天上午9点执行：

```bash
# 编辑crontab
crontab -e

# 添加以下行（请根据实际路径调整）
0 9 * * * cd /Users/PINES/Desktop/toolbox/documents/research/60s && /usr/bin/python3 60s.py
```

## API说明

- 数据来源：`https://60s.viki.moe/v2/60s`
- 返回格式：JSON
- 成功状态码：200

## 消息格式

推送的消息包含：
- 📰 今日要闻列表
- 💡 小贴士
- 🖼️ 相关图片
- 🔗 原文链接
- 📅 日期信息（公历+农历）

## 错误处理

脚本包含完整的错误处理，包括：
- API请求失败
- JSON解析错误
- 网络超时
- 企业微信推送失败

## 许可证

MIT License
