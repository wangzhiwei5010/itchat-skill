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

### logout()
退出微信登录。

**返回值:**
- 无

**示例:**
```python
bot.logout()
```

## 消息发送

### send_message(to_name, message, msg_type="text")
向指定好友发送消息。

**参数:**
- `to_name` (str): 接收者昵称或备注名
- `message` (str): 消息内容
- `msg_type` (str): 消息类型，支持 "text" 或 "image"

**返回值:**
- `bool`: 发送是否成功

**示例:**
```python
# 发送文本消息
bot.send_message("张三", "你好，这是一条测试消息")

# 发送图片
bot.send_message("张三", "/path/to/image.jpg", msg_type="image")
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
