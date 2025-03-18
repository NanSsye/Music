# Music 🎶

一个用于点歌的 XYBotV2 插件，支持发送歌曲卡片消息，并支持歌曲列表选择。

<img src="https://github.com/user-attachments/assets/a2627960-69d8-400d-903c-309dbeadf125" width="400" height="600">

## 一、插件概述

Music 插件允许用户通过简单的命令点歌，并将歌曲以卡片消息的形式发送到微信聊天中。 用户可以通过关键词搜索歌曲，选择感兴趣的歌曲后，即可欣赏美妙的音乐。

## 二、功能特性

- **🎵 歌曲搜索：**  通过关键词搜索歌曲，快速找到你想要的音乐。
- **🎼 歌曲列表：**  展示搜索结果列表，方便用户选择。
- **📱 卡片消息：**  以精美的卡片消息形式发送歌曲，包含歌曲名、歌手、封面等信息。
- **⚙️ 简单易用：**  配置简单，易于上手，即插即用。

## 三、安装与配置

1.  **安装依赖**

    确保你的 Python 环境中已经安装了以下依赖库：

    ```bash
    pip install aiohttp loguru
    ```

2.  **配置文件**

    在 `plugins/Music` 目录下创建 `config.toml` 文件，并进行如下配置：

    ```toml
    [Music]
    enable = true
    command = ["点歌"]
    command-format = "点歌 <歌曲名>"
    play_command = "播放"
    ```

    配置项说明：

    -   `enable`：是否启用该插件，`true` 为启用，`false` 为禁用。
    -   `command`：触发歌曲搜索的命令列表，用户输入以该命令开头的消息时，插件会进行歌曲搜索。
    -   `command-format`：命令格式，用于提示用户如何正确使用命令。
    -   `play_command`：播放歌曲的命令前缀，用户输入以该命令开头并跟上歌曲序号时，插件会播放该歌曲。

## 四、使用方法

1.  **搜索歌曲**

    在聊天中输入以 `command` 配置项中的命令开头的消息，并跟上要搜索的歌曲名，例如：

    ```plaintext
    点歌 十年
    ```

    插件会返回相关歌曲的列表，每个歌曲前会有对应的序号和 Emoji 标识，同时提供操作提示：

    ```plaintext
    🎶----- 找到以下歌曲 -----🎶
    1. 🎵 十年 - 陈奕迅 🎤
    2. 🎵 十年 - 刘若英 🎤
    ...
    _________________________
    🎵输入 “播放 + 序号” 播放歌曲🎵
    ```

2.  **播放歌曲**

    用户输入以 `play_command` 配置项中的命令开头并跟上歌曲序号的消息，例如：

    ```plaintext
    播放 1
    ```

    插件会发送包含歌曲信息的卡片消息：

    ```
    [卡片消息示例]
    歌曲名：十年
    歌手：陈奕迅
    [歌曲封面]
    ```

## 五、错误处理

-   如果未找到相关歌曲，插件会回复 “❌未找到相关歌曲！”
-   如果输入的歌曲序号无效，插件会回复 “❌无效的歌曲序号！”
-   如果API请求失败，插件会回复 “❌点歌失败！”

## 六、注意事项

-   请确保 `config.toml` 文件中的配置正确。
-   该插件依赖于外部 API 提供歌曲搜索和播放链接，若 API 出现问题，可能会影响插件的正常使用。
-   建议在网络状况良好的环境下使用，以获得更好的体验。

**给个 ⭐ Star 支持吧！** 😊

**开源不易，感谢打赏支持！**

![image](https://github.com/user-attachments/assets/2dde3b46-85a1-4f22-8a54-3928ef59b85f)
