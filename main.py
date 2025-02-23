import tomllib
import aiohttp
from loguru import logger

from WechatAPI import WechatAPIClient
from utils.decorators import *
from utils.plugin_base import PluginBase


class Music(PluginBase):
    description = "点歌"
    author = "老夏的金库"
    version = "1.1.0"

    def __init__(self):
        super().__init__()

        with open("plugins/Music/config.toml", "rb") as f:
            plugin_config = tomllib.load(f)

        config = plugin_config["Music"]

        self.enable = config["enable"]
        self.command = config["command"]
        self.command_format = config["command-format"]
        self.play_command = config.get("play_command", "播放")  # 新增播放命令
        self.search_results = {}  # 用于存储搜索结果，格式为 {chat_id: {song_list}}
        self.api_url = "https://www.hhlqilongzhu.cn/api/dg_wyymusic.php"  # 使用新的API

    async def _fetch_song_list(self, song_name: str) -> list:
        """
        调用API获取歌曲列表.
        """
        params = {
            "gm": song_name,
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.api_url, params=params) as resp:
                    text = await resp.text()  # 获取 TEXT 格式的返回结果
                    logger.debug(f"API 响应: {text}")  # 记录API响应
                    song_list = self._parse_song_list(text)  # 解析歌曲列表
                    return song_list
        except aiohttp.ClientError as e:
            logger.error(f"API 请求失败: {e}")
            return []

    def _parse_song_list(self, text: str) -> list:
        """
        解析 TEXT 格式的歌曲列表.
        """
        song_list = []
        lines = text.splitlines()
        for line in lines:
            parts = line.split(" -- ")
            if len(parts) == 2:
                try:
                    num_title, singer = parts  # 将序号和歌曲信息分开
                    num = num_title.split("、")[0].strip()  # 提取序号
                    title = num_title.split("、")[1].strip()  # 提取歌名
                    song_list.append({"num": num, "title": title, "singer": singer.strip()})  # 去除空格
                except Exception as e:
                    logger.warning(f"解析歌曲列表失败，行内容：{line}， 错误信息: {e}")  # 记录错误信息
        return song_list

    async def _fetch_song_data(self, song_name: str, index: int) -> dict:
        """
        调用API获取歌曲信息，需要指定歌曲序号.
        """
        params = {
            "gm": song_name,
            "n": index,
            "type": "json",  # 尝试使用 JSON 格式获取歌曲信息
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.api_url, params=params) as resp:
                    data = await resp.json()
                    logger.debug(f"获取歌曲详情API 响应: {data}")  # 记录API响应
                    if data["code"] == 200: # 判断是否成功获取数据
                        return data  # 返回歌曲信息
                    else:
                        logger.warning(f"获取歌曲信息失败，API返回：{data}")
                        return None
        except aiohttp.ClientError as e:
            logger.error(f"API 请求失败: {e}")
            return None
        except Exception as e:
            logger.exception(f"解析歌曲信息失败: {e}")
            return None

    @on_text_message
    async def handle_text(self, bot: WechatAPIClient, message: dict):
        if not self.enable:
            return

        content = str(message["Content"]).strip()
        command = content.split(" ")

        if command[0] not in self.command and command[0] != self.play_command:
            return

        if command[0] in self.command:  # 处理 "点歌" 命令
            if len(command) == 1:
                await bot.send_at_message(message["FromWxid"], f"-----XYBot-----\n❌命令格式错误！{self.command_format}",
                                          [message["SenderWxid"]])
                return

            song_name = content[len(command[0]):].strip()

            song_list = await self._fetch_song_list(song_name)

            if not song_list:
                await bot.send_at_message(message["FromWxid"], f"-----XYBot-----\n❌未找到相关歌曲！",
                                          [message["SenderWxid"]])
                return

            # 构建歌曲列表
            response_text = "🎶----- 找到以下歌曲 -----🎶\n"
            for i, song in enumerate(song_list):
                response_text += f"{i + 1}. 🎵 {song['title']} - {song['singer']} 🎤\n"
            response_text += "_________________________\n"
            response_text += f"🎵输入 “{self.play_command} + 序号” 播放歌曲🎵"

            self.search_results[message["FromWxid"]] = song_list  # 保存搜索结果
            await bot.send_at_message(message["FromWxid"], response_text, [message["SenderWxid"]])

        elif command[0] == self.play_command:  # 处理 "播放" 命令
            try:
                index = int(command[1].strip())  # 序号从 1 开始
                if message["FromWxid"] in self.search_results and 1 <= index <= len(
                        self.search_results[message["FromWxid"]]):
                    song_name = content[len(command[0]):].strip()
                    selected_song = self.search_results[message["FromWxid"]][index - 1]  # 根据index 获取歌曲信息
                    song_data = await self._fetch_song_data(selected_song["title"], index)  # 获取歌曲详情
                    if song_data:
                        title = song_data["title"]
                        singer = song_data["singer"]
                        url = song_data.get("link", "")  # 确保有默认值
                        music_url = song_data.get("music_url", "").split("?")[0]  # 确保有默认值, 并分割
                        cover_url = song_data.get("cover", "")  # 确保有默认值
                        lyric = song_data.get("lrc", "")  # 确保有默认值

                        xml = f"""<appmsg appid="wx79f2c4418704b4f8" sdkver="0"><title>{title}</title><des>{singer}</des><action>view</action><type>3</type><showtype>0</showtype><content/><url>{url}</url><dataurl>{music_url}</dataurl><lowurl>{url}</lowurl><lowdataurl>{music_url}</lowdataurl><recorditem/><thumburl>{cover_url}</thumburl><messageaction/><laninfo/><extinfo/><sourceusername/><sourcedisplayname/><songlyric>{lyric}</songlyric><commenturl/><appattach><totallen>0</totallen><attachid/><emoticonmd5/><fileext/><aeskey/></appattach><webviewshared><publisherId/><publisherReqId>0</publisherReqId></webviewshared><weappinfo><pagepath/><username/><appid/><appservicetype>0</appservicetype></weappinfo><websearch/><songalbumurl>{cover_url}</songalbumurl></appmsg><fromusername>{bot.wxid}</fromusername><scene>0</scene><appinfo><version>1</version><appname/></appinfo><commenturl/>"""
                        await bot.send_app_message(message["FromWxid"], xml, 3)
                    else:
                        await bot.send_at_message(message["FromWxid"], f"-----XYBot-----\n❌获取歌曲信息失败！",
                                                  [message["SenderWxid"]])
                else:
                    await bot.send_at_message(message["FromWxid"], f"-----XYBot-----\n❌无效的歌曲序号！",
                                              [message["SenderWxid"]])
            except ValueError:
                await bot.send_at_message(message["FromWxid"], f"-----XYBot-----\n❌请输入有效的歌曲序号！",
                                          [message["SenderWxid"]])