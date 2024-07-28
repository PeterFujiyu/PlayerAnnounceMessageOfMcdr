from mcdreforged.api.all import *

import os
import json

PLUGIN_METADATA = {
    'id': 'announce_player',
    'version': '1.6.2',
    'name': 'Announce Player',
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
save_config(config)
