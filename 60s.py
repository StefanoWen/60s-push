#!/usr/bin/env python3
"""
60秒读懂世界数据获取与企业微信推送脚本

本脚本使用 requests 库获取 https://60s.viki.moe/v2/60s 接口数据，
解析后发送到企业微信机器人webhook。
"""

import json
import requests
from typing import Dict, List, Any

class SixtySecondsNews:
    def __init__(self, webhook_key: str):
        """
        初始化
        
        Args:
            webhook_key: 企业微信机器人webhook key
        """
        self.api_60s_url = "https://60s.viki.moe/v2/60s"
        self.api_history_url = "https://60s.viki.moe/v2/today_in_history"
        self.api_epic_url = "https://60s.viki.moe/v2/epic"
        self.webhook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
        
    def get_60s_data(self) -> Dict[str, Any]:
        """
        使用 requests 获取60秒读懂世界数据
        
        Returns:
            dict: API返回的JSON数据
        """
        try:
            # 使用 requests 库获取数据
            response = requests.get(self.api_60s_url, timeout=30)
            response.raise_for_status()  # 检查HTTP错误
            
            data = response.json()
            return data
            
        except requests.exceptions.Timeout:
            raise Exception("60秒数据请求超时")
        except requests.exceptions.RequestException as e:
            raise Exception(f"60秒数据HTTP请求失败: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("60秒数据JSON解析失败")
        except Exception as e:
            raise Exception(f"获取60秒数据失败: {str(e)}")
    
    def parse_news_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析API返回的数据
        
        Args:
            data: API返回的原始数据
            
        Returns:
            dict: 解析后的数据
        """
        if data.get("code") != 200:
            raise Exception(f"API返回错误: {data.get('message', '未知错误')}")
            
        news_data = data.get("data", {})
        
        return {
            "date": news_data.get("date", ""),
            "day_of_week": news_data.get("day_of_week", ""),
            "lunar_date": news_data.get("lunar_date", ""),
            "news": news_data.get("news", []),
            "tip": news_data.get("tip", ""),
            "cover": news_data.get("cover", ""),
            "image": news_data.get("image", ""),
            "link": news_data.get("link", ""),
            "audio_music": news_data.get("audio", {}).get("music", ""),
            "audio_news": news_data.get("audio", {}).get("news", "")
        }

    def get_history_data(self) -> Dict[str, Any]:
        """
        使用 requests 获取历史上的今天数据
        
        Returns:
            dict: API返回的JSON数据
        """
        try:
            # 使用 requests 库获取数据
            response = requests.get(self.api_history_url, timeout=30)
            response.raise_for_status()  # 检查HTTP错误
            
            data = response.json()
            return data
            
        except requests.exceptions.Timeout:
            raise Exception("历史数据请求超时")
        except requests.exceptions.RequestException as e:
            raise Exception(f"历史数据HTTP请求失败: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("历史数据JSON解析失败")
        except Exception as e:
            raise Exception(f"获取历史数据失败: {str(e)}")

    def parse_history_data(self, data: Dict[str, Any]) -> List[str]:
        """
        解析历史上的今天数据
        
        Args:
            data: API返回的原始数据
            
        Returns:
            list: 历史事件列表（格式：年份 - 事件标题）
        """
        if data.get("code") != 200:
            raise Exception(f"历史API返回错误: {data.get('message', '未知错误')}")
            
        history_data = data.get("data", {})
        items = history_data.get("items", [])
        
        history_events = []
        for item in items:
            year = item.get("year", "")
            title = item.get("title", "")
            history_events.append(f"{year} - {title}")
            
        return history_events

    def get_epic_data(self) -> Dict[str, Any]:
        """
        使用 requests 获取Epic Games免费游戏数据
        
        Returns:
            dict: API返回的JSON数据
        """
        try:
            # 使用 requests 库获取数据
            response = requests.get(self.api_epic_url, timeout=30)
            response.raise_for_status()  # 检查HTTP错误
            
            data = response.json()
            return data
            
        except requests.exceptions.Timeout:
            raise Exception("Epic数据请求超时")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Epic数据HTTP请求失败: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("Epic数据JSON解析失败")
        except Exception as e:
            raise Exception(f"获取Epic数据失败: {str(e)}")

    def parse_epic_data(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        解析Epic Games免费游戏数据
        
        Args:
            data: API返回的原始数据
            
        Returns:
            list: 免费游戏列表
        """
        if data.get("code") != 200:
            raise Exception(f"Epic API返回错误: {data.get('message', '未知错误')}")
            
        epic_data = data.get("data", [])
        return epic_data
    
    def build_main_message(self, parsed_60s_data: Dict[str, Any], 
                          epic_games: List[Dict[str, Any]]) -> str:
        """
        构建主消息，包含60秒新闻和Epic免费游戏
        
        Args:
            parsed_60s_data: 解析后的60秒数据
            epic_games: Epic免费游戏列表
            
        Returns:
            str: markdown格式的消息内容
        """
        date = parsed_60s_data["date"]
        day_of_week = parsed_60s_data["day_of_week"]
        lunar_date = parsed_60s_data["lunar_date"]
        news_list = parsed_60s_data["news"]
        tip = parsed_60s_data["tip"]
        
        # 构建markdown内容
        markdown_content = f"""# 🗞️ 每日资讯汇总 - {date} {day_of_week}

**农历{lunar_date}**

## 📰 60秒读懂世界
"""
        
        # 添加新闻条目
        for i, news in enumerate(news_list, 1):
            markdown_content += f"{i}. {news}\n"
        
        # 添加Epic免费游戏
        if epic_games:
            markdown_content += """
## 🎮 Epic免费游戏
"""
            free_games = [game for game in epic_games if game.get("is_free_now") is True]
            if free_games:
                for game in free_games:
                    title = game.get("title", "未知游戏")
                    cover = game.get("cover", "")
                    description = game.get("description", "暂无描述")
                    original_price = game.get("original_price_desc", "未知价格")
                    free_end = game.get("free_end", "未知时间")
                    link = game.get("link", "")
                    
                    markdown_content += f"""
### {title}
{cover and f'![游戏封面]({cover})' or ''}
**描述**: {description}
**原价**: {original_price} - 免费至 {free_end}
[游戏详情]({link})
"""
            else:
                markdown_content += "暂无免费游戏\n"
        
        # 添加提示
        if tip:
            markdown_content += f"""
## 💡 小贴士
> {tip}
"""
        
        # 添加分隔线
        markdown_content += f"""
---
*数据来源: 60s.viki.moe* | *生成时间: {date}*
"""
        
        return markdown_content

    def build_history_message(self, parsed_60s_data: Dict[str, Any],
                             history_events: List[str]) -> str:
        """
        构建历史消息，包含历史上的今天事件
        
        Args:
            parsed_60s_data: 解析后的60秒数据
            history_events: 历史上的今天事件列表
            
        Returns:
            str: markdown格式的消息内容
        """
        date = parsed_60s_data["date"]
        day_of_week = parsed_60s_data["day_of_week"]
        lunar_date = parsed_60s_data["lunar_date"]
        
        # 构建markdown内容
        markdown_content = f"""# 📅 历史上的今天 - {date} {day_of_week}

**农历{lunar_date}**

## 历史事件
"""
        
        # 添加历史事件条目
        if history_events:
            for i, event in enumerate(history_events, 1):
                markdown_content += f"{i}. {event}\n"
        else:
            markdown_content += "暂无历史事件数据\n"
        
        # 添加分隔线
        markdown_content += f"""
---
*数据来源: 60s.viki.moe* | *生成时间: {date}*
"""
        
        return markdown_content
    
    def optimize_message_length(self, markdown_content: str) -> str:
        """
        优化消息长度以适应企业微信限制
        
        Args:
            markdown_content: 原始markdown内容
            
        Returns:
            str: 优化后的markdown内容
        """
        # 企业微信可能对Unicode字符、emoji和markdown语法有不同计数方式
        # 采取更激进的优化策略
        lines = markdown_content.split('\n')
        optimized_lines = []
        
        for line in lines:
            # 移除游戏封面图片（可能占用大量字符）
            if line.startswith('![') and '游戏封面' in line:
                continue
            # 简化游戏描述
            elif line.startswith('**描述**:'):
                desc = line.replace('**描述**:', '').strip()
                if len(desc) > 100:
                    line = f"**描述**: {desc[:100]}..."
            # 简化其他长文本
            elif len(line) > 200:
                line = line[:200] + '...'
            optimized_lines.append(line)
        
        optimized_content = '\n'.join(optimized_lines)
        
        # 如果仍然太长，进行截断
        if len(optimized_content) > 3500:
            optimized_content = optimized_content[:3400] + '\n...\n*消息过长已截断*'
        
        print(f"优化后消息长度: {len(optimized_content)} 字符")
        return optimized_content

    def send_to_wechat(self, markdown_content: str) -> bool:
        """
        发送消息到企业微信机器人
        
        Args:
            markdown_content: markdown格式的消息内容
            
        Returns:
            bool: 发送是否成功
        """
        # 检查消息长度（企业微信限制为4096字符）
        # 企业微信可能使用不同的字符计数方式，所以我们需要更保守的限制
        if len(markdown_content) > 3000:  # 使用更保守的限制来避免API错误
            print(f"警告: 消息长度 {len(markdown_content)} 字符可能超过企业微信限制，将进行优化")
            markdown_content = self.optimize_message_length(markdown_content)
        
        payload = {
            "msgtype": "markdown_v2",
            "markdown_v2": {
                "content": markdown_content
            }
        }
        
        try:
            # 使用 requests 发送消息到企业微信
            headers = {
                "Content-Type": "application/json"
            }
            
            print(f"正在发送消息到企业微信，消息长度: {len(markdown_content)} 字符")
            response = requests.post(
                self.webhook_url, 
                json=payload, 
                headers=headers, 
                timeout=30
            )
            
            # 打印响应状态和内容
            print(f"HTTP状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            if result.get("errcode") == 0:
                print("企业微信API返回成功")
                return True
            else:
                print(f"企业微信API返回错误: {result}")
                return False
            
        except requests.exceptions.RequestException as e:
            print(f"网络请求错误: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"响应状态码: {e.response.status_code}")
                print(f"响应内容: {e.response.text}")
            return False
        except Exception as e:
            print(f"发送到企业微信失败: {str(e)}")
            return False
    
    def build_markdown_message(self, parsed_60s_data: Dict[str, Any], history_events: List[str], epic_games: List[Dict[str, Any]]) -> str:
        """
        构建完整的markdown消息，包含60秒新闻、历史事件和Epic免费游戏
        
        Args:
            parsed_60s_data: 解析后的60秒数据
            history_events: 历史上的今天事件列表
            epic_games: Epic免费游戏列表
        
        Returns:
            str: markdown格式的消息内容
        """
        main_msg = self.build_main_message(parsed_60s_data, epic_games)
        history_msg = self.build_history_message(parsed_60s_data, history_events)
        return f"{main_msg}\n\n{history_msg}"

    def run(self):
        """
        主运行函数
        """
        try:
            print("开始获取60秒读懂世界数据...")
            # 获取60秒数据
            raw_60s_data = self.get_60s_data()
            print("60秒数据获取成功")
            parsed_60s_data = self.parse_news_data(raw_60s_data)
            print("60秒数据解析成功")

            print("开始获取历史上的今天数据...")
            # 获取历史上的今天数据
            raw_history_data = self.get_history_data()
            print("历史数据获取成功")
            history_events = self.parse_history_data(raw_history_data)
            print("历史数据解析成功")

            print("开始获取Epic免费游戏数据...")
            # 获取Epic免费游戏数据
            raw_epic_data = self.get_epic_data()
            print("Epic数据获取成功")
            epic_games = self.parse_epic_data(raw_epic_data)
            print("Epic数据解析成功")

            # 构建主消息（新闻+Epic）
            main_content = self.build_main_message(parsed_60s_data, epic_games)
            print("主消息构建成功")
            # 构建历史消息
            history_content = self.build_history_message(parsed_60s_data, history_events)
            print("历史消息构建成功")

            # 发送主消息
            main_success = self.send_to_wechat(main_content)
            if main_success:
                print("✅ 主消息发送到企业微信成功！")
            else:
                print("❌ 主消息发送失败")
            # 发送历史消息
            history_success = self.send_to_wechat(history_content)
            if history_success:
                print("✅ 历史消息发送到企业微信成功！")
            else:
                print("❌ 历史消息发送失败")
        except Exception as e:
            print(f"❌ 运行出错: {str(e)}")

def main():
    """
    主函数
    """
    # 请在此处填写您的企业微信机器人webhook key
    webhook_key = "YOUR_WEBHOOK_KEY_HERE"  # 替换为实际的webhook key
    
    if webhook_key == "YOUR_WEBHOOK_KEY_HERE":
        print("请先配置企业微信机器人的webhook key")
        print("测试模式：仅显示生成的markdown内容")
        # 测试模式：只获取数据并显示markdown内容，不发送
        try:
            news_bot = SixtySecondsNews("TEST_KEY")
            print("开始获取60秒读懂世界数据...")
            raw_60s_data = news_bot.get_60s_data()
            print("60秒数据获取成功")
            parsed_60s_data = news_bot.parse_news_data(raw_60s_data)
            print("60秒数据解析成功")
            print("开始获取历史上的今天数据...")
            raw_history_data = news_bot.get_history_data()
            print("历史数据获取成功")
            history_events = news_bot.parse_history_data(raw_history_data)
            print("历史数据解析成功")
            print("开始获取Epic免费游戏数据...")
            raw_epic_data = news_bot.get_epic_data()
            print("Epic数据获取成功")
            epic_games = news_bot.parse_epic_data(raw_epic_data)
            print("Epic数据解析成功")
            # 构建主消息
            main_content = news_bot.build_main_message(parsed_60s_data, epic_games)
            print("主消息构建成功")
            # 构建历史消息
            history_content = news_bot.build_history_message(parsed_60s_data, history_events)
            print("历史消息构建成功")
            print("\n" + "="*50)
            print("主消息 Markdown 内容:")
            print("="*50)
            print(main_content)
            print("="*50)
            print("历史消息 Markdown 内容:")
            print("="*50)
            print(history_content)
            print("="*50)
        except Exception as e:
            print(f"❌ 测试运行出错: {str(e)}")
        return
    
    # 创建实例并运行
    news_bot = SixtySecondsNews(webhook_key)
    news_bot.run()

if __name__ == "__main__":
    main()
