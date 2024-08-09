from mcdreforged.api.all import *

import os
import json

PLUGIN_METADATA = {
    'id': 'announce_owner',
    'version': '1.6.2',
    'name': 'Announce Owner',
    'author': 'Peter',
    'link': 'github.com/PeterFujiyu'
}

msg_head = f"[{PLUGIN_METADATA['name']}]"
CONFIG_PATH = 'config/msg.config'
ALLOWED_COLORS = [
    'black', 'dark_blue', 'dark_green', 'dark_aqua', 'dark_red', 'dark_purple', 'gold', 
    'gray', 'dark_gray', 'blue', 'green', 'aqua', 'red', 'light_purple', 'yellow', 'white'
]

def get_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def out_msg(server: ServerInterface, msg: str, color: str):
    server.execute(f'tellraw @a {{"text":"{msg_head}{msg}","color":"{color}"}}')

def on_player_joined(server: ServerInterface, player: str, info: Info):
    config = get_config()
    player_config = config.get(player, {
        'enabled': True, 
        'msg_online': '欢迎 {player}!', 
        'color_online': 'white',
        'msg_offline': '再见 {player}!', 
        'color_offline': 'white',
        'modifiable': True
    })

    if player_config.get('enabled', True):
        custom_msg = player_config.get('msg_online', '欢迎 {player}!').replace("{player}", player)
        custom_color = player_config.get('color_online', 'white')
        out_msg(server, custom_msg, custom_color)

def on_player_left(server: ServerInterface, player: str):
    config = get_config()
    player_config = config.get(player, {
        'enabled': True, 
        'msg_online': '欢迎 {player}!', 
        'color_online': 'white',
        'msg_offline': '再见 {player}!', 
        'color_offline': 'white',
        'modifiable': True
    })

    if player_config.get('enabled', True):
        custom_msg = player_config.get('msg_offline', '再见 {player}!').replace("{player}", player)
        custom_color = player_config.get('color_offline', 'white')
        out_msg(server, custom_msg, custom_color)

def show_help(src: CommandSource):
    help_message = """
    §6Announce Owner 插件使用说明§r
    §e!!msg on§r - 启用玩家的欢迎消息
    §e!!msg off§r - 禁用玩家的欢迎消息
    §e!!msg online_change <message> <color>§r - 更改玩家上线时的欢迎消息及其颜色
    §e!!msg offline_change <message> <color>§r - 更改玩家离线时的消息及其颜色
    §e!!msg ban <player>§r - 禁止特定玩家修改他们的消息设置。需要权限等级 >= 2
    §e!!msg unban <player>§r - 允许特定玩家再次修改他们的消息设置。需要权限等级 >= 2
    §e!!msg force_online_change <player> <message> <color>§r - 强制更改特定玩家的上线消息及其颜色。需要权限等级 >= 2
    §e!!msg force_offline_change <player> <message> <color>§r - 强制更改特定玩家的离线消息及其颜色。需要权限等级 >= 2
    §e!!msg help§r - 显示此帮助信息
    """
    src.reply(help_message)

def on_load(server: ServerInterface, old_module):
    server.register_event_listener('minecraft.player.join', on_player_joined)
    server.register_event_listener('minecraft.player.leave', on_player_left)
    server.register_command(
        Literal('!!msg')
        .then(Literal('on')
            .runs(lambda src: toggle_msg(src, True)))
        .then(Literal('off')
            .runs(lambda src: toggle_msg(src, False)))
        .then(Literal('online_change')
            .then(QuotableText('message')
                .then(Text('color')
                    .runs(lambda src, ctx: change_online_msg(src, ctx['message'], ctx['color'])))))
        .then(Literal('offline_change')
            .then(QuotableText('message')
                .then(Text('color')
                    .runs(lambda src, ctx: change_offline_msg(src, ctx['message'], ctx['color'])))))
        .then(Literal('ban')
            .then(Text('player')
                .runs(lambda src, ctx: ban_player(src, ctx['player']))))
        .then(Literal('unban')
            .then(Text('player')
                .runs(lambda src, ctx: unban_player(src, ctx['player']))))
        .then(Literal('force_online_change')
            .then(Text('player')
                .then(QuotableText('message')
                    .then(Text('color')
                        .runs(lambda src, ctx: force_change_online_msg(src, ctx['player'], ctx['message'], ctx['color']))))))
        .then(Literal('force_offline_change')
            .then(Text('player')
                .then(QuotableText('message')
                    .then(Text('color')
                        .runs(lambda src, ctx: force_change_offline_msg(src, ctx['player'], ctx['message'], ctx['color']))))))
        .then(Literal('help')
            .runs(lambda src: show_help(src)))
    )

def toggle_msg(src: CommandSource, enabled: bool):
    config = get_config()
    player = src.player
    if player and is_modifiable(player):
        if player not in config:
            config[player] = {}
        config[player]['enabled'] = enabled
        save_config(config)
        src.reply(f"Your welcome message has been {'enabled' if enabled else 'disabled'}.")
    else:
        src.reply("You are not allowed to change your message settings.")

def change_online_msg(src: CommandSource, message: str, color: str):
    if color not in ALLOWED_COLORS:
        src.reply("Invalid color! Allowed colors are: " + ", ".join(ALLOWED_COLORS))
        return
    
    config = get_config()
    player = src.player
    if player and is_modifiable(player):
        if player not in config:
            config[player] = {}
        config[player]['msg_online'] = message
        config[player]['color_online'] = color
        save_config(config)
        src.reply(f"Your online message has been changed to: '{message}' with color '{color}'.")
    else:
        src.reply("You are not allowed to change your message settings.")

def change_offline_msg(src: CommandSource, message: str, color: str):
    if color not in ALLOWED_COLORS:
        src.reply("Invalid color! Allowed colors are: " + ", ".join(ALLOWED_COLORS))
        return
    
    config = get_config()
    player = src.player
    if player and is_modifiable(player):
        if player not in config:
            config[player] = {}
        config[player]['msg_offline'] = message
        config[player]['color_offline'] = color
        save_config(config)
        src.reply(f"Your offline message has been changed to: '{message}' with color '{color}'.")
    else:
        src.reply("You are not allowed to change your message settings.")

def force_change_online_msg(src: CommandSource, player: str, message: str, color: str):
    if color not in ALLOWED_COLORS:
        src.reply("Invalid color! Allowed colors are: " + ", ".join(ALLOWED_COLORS))
        return
    
    if src.has_permission(2):
        config = get_config()
        if player not in config:
            config[player] = {}
        config[player]['msg_online'] = message
        config[player]['color_online'] = color
        save_config(config)
        src.reply(f"{player}'s online message has been changed to: '{message}' with color '{color}'.")
    else:
        src.reply("You do not have permission to force change player's online message.")

def force_change_offline_msg(src: CommandSource, player: str, message: str, color: str):
    if color not in ALLOWED_COLORS:
        src.reply("Invalid color! Allowed colors are: " + ", ".join(ALLOWED_COLORS))
        return
    
    if src.has_permission(2):
        config = get_config()
        if player not in config:
            config[player] = {}
        config[player]['msg_offline'] = message
        config[player]['color_offline'] = color
        save_config(config)
        src.reply(f"{player}'s offline message has been changed to: '{message}' with color '{color}'.")
    else:
        src.reply("You do not have permission to force change player's offline message.")

def ban_player(src: CommandSource, player: str):
    if src.has_permission(2):
        config = get_config()
        if player not in config:
            config[player] = {}
        config[player]['modifiable'] = False
        save_config(config)
        src.reply(f"{player} has been banned from changing message settings.")
    else:
        src.reply("You do not have permission to ban players.")

def unban_player(src: CommandSource, player: str):
    if src.has_permission(2):
        config = get_config()
        if player not in config:
            config[player] = {}
        config[player]['modifiable'] = True
        save_config(config)
        src.reply(f"{player} has been unbanned and can now change message settings.")
    else:
        src.reply("You do not have permission to unban players.")

def is_modifiable(player: str) -> bool:
    config = get_config()
    player_config = config.get(player, {'modifiable': True})
    return player_config.get('modifiable', True)

# Ensuring the configuration is loaded and saved even if it doesn't exist initially
config = get_config()
save_config(config)
