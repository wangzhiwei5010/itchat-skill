#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信 iPad 协议机器人核心脚本
提供登录、消息收发、联系人管理、群组操作等功能
"""

import itchat
import json
import sys
import argparse
from pathlib import Path


class WeChatBot:
    """微信机器人核心类"""
    
    def __init__(self, login_state_file="login_state.json"):
        """
        初始化机器人
        
        Args:
            login_state_file: 登录状态保存文件路径
        """
        self.login_state_file = login_state_file
        self.is_logged_in = False
        self.message_queue = []
        
    def check_login_status(self):
        """
        检查登录状态
        
        Returns:
            bool: 是否已登录（登录状态文件存在且有效）
        """
        login_file = Path(self.login_state_file)
        if not login_file.exists():
            return False
        
        try:
            # 尝试读取登录状态文件
            with open(self.login_state_file, 'r', encoding='utf-8') as f:
                login_data = json.load(f)
            
            # 检查是否包含必要的登录信息
            if not login_data:
                return False
            
            # 检查登录状态是否有效（根据 itchat 的状态存储结构）
            if 'itchat_login_state' in login_data:
                return True
            
            return False
        except Exception:
            return False
    
    def login(self, force=False):
        """
        登录微信
        
        Args:
            force: 是否强制重新登录（忽略已有的登录状态）
            
        Returns:
            bool: 登录是否成功
        """
        # 检查登录状态
        if not force and self.check_login_status():
            try:
                # 尝试使用已有登录状态
                itchat.auto_login(hotReload=True, statusStorageDir=self.login_state_file)
                self.is_logged_in = True
                print("✓ 已自动登录（使用保存的登录状态）")
                return True
            except Exception as e:
                print(f"自动登录失败，需要重新登录: {str(e)}")
        
        try:
            # 登录并启用热重载，保持登录状态
            print("请扫描二维码登录微信...")
            itchat.auto_login(hotReload=True, statusStorageDir=self.login_state_file)
            self.is_logged_in = True
            print("✓ 登录成功！")
            return True
        except Exception as e:
            print(f"✗ 登录失败: {str(e)}")
            return False
    
    def logout(self):
        """退出登录"""
        try:
            itchat.logout()
            self.is_logged_in = False
            print("已退出登录")
        except Exception as e:
            print(f"退出登录失败: {str(e)}")
    
    def send_message(self, to_name, message, msg_type="text", use_username=False):
        """
        发送消息
        
        Args:
            to_name: 接收者昵称、备注名或微信ID
            message: 消息内容
            msg_type: 消息类型 (text/image/file)
            use_username: 是否直接使用 to_name 作为微信ID（True=直接使用ID，False=通过昵称/备注查找）
            
        Returns:
            bool: 发送是否成功
        """
        if not self.is_logged_in:
            print("请先登录微信")
            return False
        
        try:
            target_username = None
            
            if use_username:
                # 直接使用微信ID
                target_username = to_name
                print(f"使用微信ID: {to_name}")
            else:
                # 通过昵称或备注名查找好友
                friends = itchat.search_friends(name=to_name)
                if not friends:
                    print(f"未找到好友: {to_name}")
                    return False
                target_username = friends[0]['UserName']
            
            if msg_type == "text":
                # 发送文本消息
                result = itchat.send(message, toUserName=target_username)
                if result:
                    print(f"消息已发送给 {to_name}")
                    return True
                else:
                    print("消息发送失败")
                    return False
                    
            elif msg_type == "image":
                # 发送图片
                itchat.send_image(message, toUserName=target_username)
                print(f"图片已发送给 {to_name}")
                return True
                
            else:
                print(f"不支持的消息类型: {msg_type}")
                return False
                return False
                
        except Exception as e:
            print(f"发送消息失败: {str(e)}")
            return False
    
    def send_group_message(self, group_name, message):
        """
        发送群消息
        
        Args:
            group_name: 群名称
            message: 消息内容
            
        Returns:
            bool: 发送是否成功
        """
        if not self.is_logged_in:
            print("请先登录微信")
            return False
        
        try:
            # 查找群组
            groups = itchat.search_chatrooms(name=group_name)
            if not groups:
                print(f"未找到群组: {group_name}")
                return False
            
            # 发送群消息
            result = itchat.send(message, toUserName=groups[0]['UserName'])
            if result:
                print(f"消息已发送到群 {group_name}")
                return True
            else:
                print("群消息发送失败")
                return False
                
        except Exception as e:
            print(f"发送群消息失败: {str(e)}")
            return False
    
    def get_friends(self):
        """
        获取好友列表
        
        Returns:
            list: 好友列表，每个元素包含好友信息字典
        """
        if not self.is_logged_in:
            print("请先登录微信")
            return []
        
        try:
            friends = itchat.get_friends(update=True)[1:]  # 排除自己
            friend_list = []
            
            for friend in friends:
                friend_info = {
                    'NickName': friend.get('NickName', ''),
                    'RemarkName': friend.get('RemarkName', ''),
                    'UserName': friend.get('UserName', ''),
                    'Province': friend.get('Province', ''),
                    'City': friend.get('City', ''),
                    'Signature': friend.get('Signature', '')
                }
                friend_list.append(friend_info)
            
            return friend_list
            
        except Exception as e:
            print(f"获取好友列表失败: {str(e)}")
            return []
    
    def get_groups(self):
        """
        获取群组列表
        
        Returns:
            list: 群组列表
        """
        if not self.is_logged_in:
            print("请先登录微信")
            return []
        
        try:
            groups = itchat.get_chatrooms(update=True)
            group_list = []
            
            for group in groups:
                group_info = {
                    'NickName': group.get('NickName', ''),
                    'UserName': group.get('UserName', ''),
                    'MemberCount': group.get('MemberCount', 0)
                }
                group_list.append(group_info)
            
            return group_list
            
        except Exception as e:
            print(f"获取群组列表失败: {str(e)}")
            return []
    
    def get_group_members(self, group_name):
        """
        获取群组成员
        
        Args:
            group_name: 群名称
            
        Returns:
            list: 群成员列表
        """
        if not self.is_logged_in:
            print("请先登录微信")
            return []
        
        try:
            groups = itchat.search_chatrooms(name=group_name)
            if not groups:
                print(f"未找到群组: {group_name}")
                return []
            
            # 获取群成员详细信息
            group_members = itchat.update_chatroom(
                groups[0]['UserName'], 
                detailedMember=True
            )
            
            member_list = []
            for member in group_members['MemberList']:
                member_info = {
                    'NickName': member.get('NickName', ''),
                    'AttrStatus': member.get('AttrStatus', 0)
                }
                member_list.append(member_info)
            
            return member_list
            
        except Exception as e:
            print(f"获取群组成员失败: {str(e)}")
            return []
    
    def register_message_handler(self, handler_func):
        """
        注册消息处理器
        
        Args:
            handler_func: 消息处理函数，接收消息对象作为参数
        """
        @itchat.msg_register(itchat.content.TEXT)
        def text_reply(msg):
            # 将消息加入队列
            self.message_queue.append(msg)
            # 调用自定义处理器
            if handler_func:
                handler_func(msg)
        
        print("消息处理器已注册")
    
    def run(self):
        """运行机器人，保持在线"""
        if not self.is_logged_in:
            print("请先登录微信")
            return
        
        print("机器人正在运行，按 Ctrl+C 退出...")
        itchat.run(debug=False)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="微信 iPad 协议机器人")
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 登录命令
    login_parser = subparsers.add_parser('login', help='登录微信')
    login_parser.add_argument('--force', action='store_true', help='强制重新登录（忽略已有登录状态）')
    
    # 发送消息命令
    send_parser = subparsers.add_parser('send', help='发送消息')
    send_parser.add_argument('--to', required=True, help='接收者昵称、备注名或微信ID')
    send_parser.add_argument('--message', required=True, help='消息内容')
    send_parser.add_argument('--type', default='text', help='消息类型 (text/image)')
    send_parser.add_argument('--use-id', action='store_true', help='使用微信ID定位（不通过昵称/备注查找）')
    
    # 发送群消息命令
    group_parser = subparsers.add_parser('send_group', help='发送群消息')
    group_parser.add_argument('--group', required=True, help='群名称')
    group_parser.add_argument('--message', required=True, help='消息内容')
    
    # 获取好友列表命令
    subparsers.add_parser('get_friends', help='获取好友列表')
    
    # 获取群组列表命令
    subparsers.add_parser('get_groups', help='获取群组列表')
    
    # 获取群成员命令
    members_parser = subparsers.add_parser('get_group_members', help='获取群成员')
    members_parser.add_argument('--group', required=True, help='群名称')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    bot = WeChatBot()
    
    if args.command == 'login':
        force_login = getattr(args, 'force', False)
        if bot.login(force=force_login):
            if not force_login:
                print("✓ 登录状态有效，保持在线状态...")
            itchat.run(debug=False)
    
    elif args.command == 'send':
        if bot.login():
            bot.send_message(args.to, args.message, args.type, use_username=getattr(args, 'use_id', False))
            bot.logout()
    
    elif args.command == 'send_group':
        if bot.login():
            bot.send_group_message(args.group, args.message)
            bot.logout()
    
    elif args.command == 'get_friends':
        if bot.login():
            friends = bot.get_friends()
            print(f"\n好友列表 (共 {len(friends)} 人):")
            for idx, friend in enumerate(friends[:20], 1):  # 只显示前20个
                display_name = friend['RemarkName'] if friend['RemarkName'] else friend['NickName']
                print(f"{idx}. {display_name} ({friend['NickName']})")
            
            if len(friends) > 20:
                print(f"... 还有 {len(friends) - 20} 位好友")
            
            # 保存完整列表到文件
            output_file = "friends_list.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(friends, f, ensure_ascii=False, indent=2)
            print(f"\n完整好友列表已保存到 {output_file}")
            
            bot.logout()
    
    elif args.command == 'get_groups':
        if bot.login():
            groups = bot.get_groups()
            print(f"\n群组列表 (共 {len(groups)} 个):")
            for idx, group in enumerate(groups, 1):
                print(f"{idx}. {group['NickName']} ({group['MemberCount']} 成员)")
            
            # 保存完整列表到文件
            output_file = "groups_list.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(groups, f, ensure_ascii=False, indent=2)
            print(f"\n完整群组列表已保存到 {output_file}")
            
            bot.logout()
    
    elif args.command == 'get_group_members':
        if bot.login():
            members = bot.get_group_members(args.group)
            print(f"\n群 {args.group} 成员列表 (共 {len(members)} 人):")
            for idx, member in enumerate(members[:20], 1):
                print(f"{idx}. {member['NickName']}")
            
            if len(members) > 20:
                print(f"... 还有 {len(members) - 20} 位成员")
            
            # 保存完整列表到文件
            output_file = f"group_members_{args.group}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(members, f, ensure_ascii=False, indent=2)
            print(f"\n完整成员列表已保存到 {output_file}")
            
            bot.logout()


if __name__ == "__main__":
    main()
