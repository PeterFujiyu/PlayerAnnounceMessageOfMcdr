# Announce Player 插件使用说明

## 插件信息
- **插件ID**: `announce_player`
- **版本**: `1.6.2`
- **名称**: `Announce Player`
- **作者**: Peter
- **链接**: [github.com/PeterFujiyu](https://github.com/PeterFujiyu)

## 功能概述
Announce Owner 插件用于在玩家上线和离线时向全体玩家发送自定义消息。管理员可以通过命令启用或禁用消息，设置消息内容和颜色，禁止或允许特定玩家修改他们的消息。

## 支持的颜色
插件支持 Minecraft `tellraw` 命令的颜色列表：
- black
- dark_blue
- dark_green
- dark_aqua
- dark_red
- dark_purple
- gold
- gray
- dark_gray
- blue
- green
- aqua
- red
- light_purple
- yellow
- white

## 配置文件路径
- `config/msg.config`

## 命令列表

### 1. `!!msg on`
启用玩家的欢迎消息。

```
用法: !!msg on
```

### 2. `!!msg off`
禁用玩家的欢迎消息。

```
用法: !!msg off
```

### 3. `!!msg online_change <message> <color>`
更改玩家上线时的欢迎消息及其颜色。

```
用法: !!msg online_change 欢迎回来 dark_blue
```

### 4. `!!msg offline_change <message> <color>`
更改玩家离线时的消息及其颜色。

```
用法: !!msg offline_change 再见 dark_red
```

### 5. `!!msg ban <player>`
禁止特定玩家修改他们的消息设置。需要权限等级 >= 2。

```
用法: !!msg ban Steve
```

### 6. `!!msg unban <player>`
允许特定玩家再次修改他们的消息设置。需要权限等级 >= 2。

```
用法: !!msg unban Steve
```

### 7. `!!msg force_online_change <player> <message> <color>`
强制更改特定玩家的上线消息及其颜色。需要权限等级 >= 2。

```
用法: !!msg force_online_change Steve 欢迎回来 dark_blue
```

### 8. `!!msg force_offline_change <player> <message> <color>`
强制更改特定玩家的离线消息及其颜色。需要权限等级 >= 2。

```
用法: !!msg force_offline_change Steve 再见 dark_red
```

## 示例

1. 启用自己的欢迎消息：

```
!!msg on
```

2. 禁用自己的欢迎消息：

```
!!msg off
```

3. 设置自己的上线消息为“欢迎回来”，颜色为 `dark_blue`：

```
!!msg online_change 欢迎回来 dark_blue
```

4. 设置自己的离线消息为“再见”，颜色为 `dark_red`：

```
!!msg offline_change 再见 dark_red
```

5. 管理员禁止玩家 Steve 修改消息设置：

```
!!msg ban Steve
```

6. 管理员允许玩家 Steve 修改消息设置：

```
!!msg unban Steve
```

7. 管理员强制更改玩家 Steve 的上线消息为“欢迎回来”，颜色为 `dark_blue`：

```
!!msg force_online_change Steve 欢迎回来 dark_blue
```

8. 管理员强制更改玩家 Steve 的离线消息为“再见”，颜色为 `dark_red`：

```
!!msg force_offline_change Steve 再见 dark_red
```

通过这些命令，您可以方便地管理玩家的欢迎和离线消息。


### 感谢MCDR还有它的开发团队
