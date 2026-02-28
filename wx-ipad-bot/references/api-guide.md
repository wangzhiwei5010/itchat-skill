# API 接口指南

## 目录
- [概述](#概述)
- [核心类](#核心类)
- [登录与认证](#登录与认证)
- [消息发送](#消息发送)
- [联系人管理](#联系人管理)
- [群组操作](#群组操作)
- [消息处理](#消息处理)

## 概述
本文档详细描述了 `wechat_bot.py` 脚本中提供的 API 接口。

**依赖库:**
- `itchat-uos>=1.5.0.dev0`: itchat 的社区维护版本，专门修复了 iPad 协议的兼容性问题
- `requests>=2.28.0`: HTTP 请求库

**关于 itchat-uos:**
- 保持与原版 itchat 的 API 完全兼容
- 修复了 iPad 协议的登录兼容性问题
- 支持最新版本的微信客户端
- 由社区持续维护和更新

## 核心类

### WeChatBot
微信机器人核心类，封装所有微信操作功能。

**初始化参数:**
- `login_state_file` (str): 登录状态保存文件路径，默认 "login_state.json"

**示例:**
```python
bot = WeChatBot(login_state_file="my_login_state.json")
```

## 登录与认证

### login()
登录微信账号，使用二维码扫描方式。

**返回值:**
- `bool`: 登录是否成功

**示例:**
```python
if bot.login():
    print("登录成功")
else:
    print("登录失败")
```

**注意事项:**
- 首次登录需要扫描二维码
- 登录成功后会保存状态到文件，后续可快速重连
- 建议不要频繁登录和退出
- 支持自动登录检查，如已有保存的状态则自动登录

### check_login_status()
检查是否有保存的登录状态。

**返回值:**
- `bool`: 是否存在有效的登录状态

**示例:**
```python
if bot.check_login_status():
    print("已有登录状态，可以直接使用")
else:
    print("需要重新登录")
```

### logout()
退出微信登录。

**返回值:**
- 无

**示例:**
```python
bot.logout()
```

## 消息发送

### send_message(to_name, message, msg_type="text", use_username=False)
向指定好友发送消息。

**参数:**
- `to_name` (str): 接收者昵称、备注名或微信ID
- `message` (str): 消息内容
- `msg_type` (str): 消息类型，支持 "text" 或 "image"
- `use_username` (bool): 是否直接使用 to_name 作为微信ID
  - False: 通过昵称或备注名查找好友（默认）
  - True: 直接使用 to_name 作为微信ID，不进行查找

**返回值:**
- `bool`: 发送是否成功

**示例:**
```python
# 使用昵称/备注名发送文本消息
bot.send_message("张三", "你好，这是一条测试消息")

# 使用微信ID直接发送消息（更快速，避免查找）
bot.send_message("wxid_xxxxxxxxxxxxx", "通过ID发送的消息", use_username=True)

# 发送图片
bot.send_message("张三", "/path/to/image.jpg", msg_type="image")
```

**注意事项:**
- 使用微信ID发送时，ID 格式通常为 `wxid_` 开头的字符串
- 微信ID 可以通过 `get_friends()` 方法获取，字段名为 `UserName`
- 使用微信ID发送更高效，避免昵称/备注名的查找过程

**获取微信ID的方法:**
```python
# 方法1: 通过获取好友列表
friends = bot.get_friends()
for friend in friends:
    display_name = friend['RemarkName'] if friend['RemarkName'] else friend['NickName']
    print(f"{display_name} -> {friend['UserName']}")

# 方法2: 使用命令行工具
python scripts/wechat_bot.py get_friends
# 输出文件: friends_list.json，包含 UserName 字段
```

**支持的文件类型:**
- 文本: 直接传入文本字符串
- 图片: 传入图片文件路径

### send_group_message(group_name, message)
向指定群组发送消息。

**参数:**
- `group_name` (str): 群名称
- `message` (str): 消息内容

**返回值:**
- `bool`: 发送是否成功

**示例:**
```python
bot.send_group_message("工作群", "大家好，今天下午3点开会")
```

## 联系人管理

### get_friends()
获取当前账号的所有好友列表。

**返回值:**
- `list`: 好友列表，每个元素是包含好友信息的字典

**好友信息字典结构:**
```python
{
    'NickName': '好友昵称',
    'RemarkName': '备注名',
    'UserName': '微信用户名(唯一标识)',
    'Province': '省份',
    'City': '城市',
    'Signature': '个性签名'
}
```

**示例:**
```python
friends = bot.get_friends()
for friend in friends:
    print(f"{friend['RemarkName'] or friend['NickName']}")
```

## 群组操作

### get_groups()
获取当前账号的所有群组列表。

**返回值:**
- `list`: 群组列表，每个元素是包含群组信息的字典

**群组信息字典结构:**
```python
{
    'NickName': '群名称',
    'UserName': '群组唯一标识',
    'MemberCount': 成员数量
}
```

**示例:**
```python
groups = bot.get_groups()
for group in groups:
    print(f"{group['NickName']} - {group['MemberCount']} 成员")
```

### get_group_members(group_name)
获取指定群组的成员列表。

**参数:**
- `group_name` (str): 群名称

**返回值:**
- `list`: 群成员列表

**成员信息字典结构:**
```python
{
    'NickName': '成员昵称',
    'AttrStatus': 成员属性状态
}
```

**示例:**
```python
members = bot.get_group_members("工作群")
for member in members:
    print(member['NickName'])
```

## 消息处理

### register_message_handler(handler_func)
注册自定义消息处理函数。

**参数:**
- `handler_func` (function): 消息处理函数，接收消息对象作为参数

**消息对象结构:**
```python
{
    'FromUserName': '发送者ID',
    'ToUserName': '接收者ID',
    'Content': '消息内容',
    'CreateTime': 时间戳,
    'MsgType': '消息类型',
    'Type': '消息子类型'
}
```

**示例:**
```python
def my_message_handler(msg):
    print(f"收到消息: {msg['Content']}")
    # 智能体可以在这里分析消息并生成回复

bot.register_message_handler(my_message_handler)
bot.run()
```

### run()
运行机器人，保持在线并监听消息。

**返回值:**
- 无

**示例:**
```python
bot.login()
bot.register_message_handler(my_message_handler)
bot.run()  # 保持运行，按 Ctrl+C 退出
```

## 错误处理

所有 API 方法在执行失败时都会打印错误信息，返回值表示操作是否成功。

**常见错误:**
- 未登录: 执行操作前未调用 login()
- 好友不存在: 发送消息时找不到指定好友
- 群组不存在: 群组操作时找不到指定群组
- 网络错误: 微信服务器连接失败

**建议:**
- 在调用 API 前检查返回值
- 使用 try-except 捕获异常
- 记录错误日志以便排查问题

## 使用建议

1. **登录频率**: 避免频繁登录和退出，使用热重载保持登录状态
2. **消息发送**: 控制发送频率，避免触发微信安全检测
3. **资源管理**: 使用完毕后及时调用 logout() 退出登录
4. **错误处理**: 始终检查 API 返回值，处理错误情况

## 关于 itchat-uos

**为什么使用 itchat-uos:**
- 原版 itchat 已停止维护，对新版微信兼容性较差
- iPad 协议需要特定的兼容性支持
- itchat-uos 是社区维护的增强版本，持续更新

**安装方式:**
```bash
pip install itchat-uos>=1.5.0.dev0
```

**API 兼容性:**
- itchat-uos 与原版 itchat API 完全兼容
- 现有代码无需修改，只需更换依赖包
- 提供更好的 iPad 协议支持

**已知优势:**
- ✅ 修复了 iPad 协议登录问题
- ✅ 支持最新版本的微信客户端
- ✅ 提高登录稳定性
- ✅ 减少登录失败率
- ✅ 保持与原版 API 100% 兼容

**注意事项:**
- itchat-uos 仍基于逆向工程实现，可能随微信更新失效
- 建议定期更新 itchat-uos 版本
- 生产环境使用需考虑账号安全风险
- 遵守微信用户协议，避免频繁操作

**版本选择:**
- 推荐使用最新开发版: `itchat-uos>=1.5.0.dev0`
- 查看最新版本: `pip search itchat-uos` 或访问 GitHub 仓库
