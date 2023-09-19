from nonebot import get_driver
from nonebot import on_fullmatch, on_message
from .config import Config, plugin_config_file
from nonebot.adapters.onebot.v11 import MessageSegment
import httpx, yaml, asyncio, tempfile 
from random import choice
from nonebot.plugin import PluginMetadata
from nonebot.params import ArgPlainText, EventPlainText
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-video-api",
    description="一款可以自由增删视频指令和api的插件",
    usage="配置好后发送相应的指令即可，配置文件在cofig/video_api_config.yml",
    type="application",
    homepage="https://github.com/Q1351998764/nonebot-plugin-video-api",
    config=Config,
    supported_adapters={"~onebot.v11"},
)
plugin_config = Config.parse_obj(get_driver().config)
cmds_config = plugin_config.api_data

cmds = []
for cmd in cmds_config:
    if '|' in cmd:
        cmds = cmds + (cmd.split('|'))
    else:
        cmds.append(cmd)


keyword = on_message(priority=10, block=False)
jktj = on_fullmatch(["视频接口统计","视频接口","视频api统计","视频api"], priority=10, block=True)
add_api = on_fullmatch(["添加视频接口","添加视频api"], priority=10, block=True, permission=SUPERUSER)

lock = asyncio.Lock()

@keyword.handle()
async def handle_function(matcher: Matcher, msg = EventPlainText()):
    if msg in cmds:
        matcher.stop_propagation()
    else:
        return
    for cmd in cmds_config:
        if msg in cmd:
            urls = cmds_config[cmd] 
            url_dic = choice(urls)
            url = url_dic.get('url')
            is_proxy = False
            if url_dic.get('is_proxy'):
                is_proxy = url_dic['is_proxy']
            res = await get_video(url, is_proxy)
            if res:
                with tempfile.NamedTemporaryFile() as fp:
                    fp.write(res.content)
                    await keyword.finish(MessageSegment.video(file='file://'+ fp.name))
            else:
                for url_dic in urls:
                    url = url_dic.get('url')
                    is_proxy = False
                    if url_dic.get('is_proxy'):
                        is_proxy = url_dic['is_proxy']
                    res = await get_video(url, is_proxy)
                    if res:
                        with tempfile.NamedTemporaryFile() as fp:
                            fp.write(res.content)
                            await keyword.finish(MessageSegment.video(file='file://'+ fp.name))
                else:
                    await keyword.finish("{}接口已全部失效，请稍后再试或更换新的接口".format(msg))

async def get_video(url, is_proxy=False):
    '''
    获取视频
    
    params
    ----

    url: 视频api的url

    is_proxy: 是否使用代理
    '''
    proxies = None
    if is_proxy:
        try:
            proxy = plugin_config.global_config.proxies_http
        except:
            await keyword.finish("请先在.env中配置代理")
        proxies = {
            "all://": proxy,
        }
    header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36",
    }
    async with httpx.AsyncClient(proxies=proxies) as client:
        try:
            res = await client.get(url, follow_redirects=True, headers=header)
        except:
            return 0
        else:
            if res.status_code != 200:
                return 0
            content_type = res.headers.get('Content-Type', '').lower()
            is_video = content_type.startswith('video/')
            is_text = content_type.startswith('text/')
            is_json = content_type.startswith('application/json')
            
            if is_video:
                return res

            elif is_text:
                if not res.text.startswith('http://') and not res.text.startswith('https://'):
                    video_url = 'https://' + res.text
                try:
                    video = await client.get(video_url)
                    if video.status_code == 200:
                        return video
                    else:
                        return 0
                except:
                    return res

            elif is_json:
                video_urls = get_url_from_json(res.json())
                video_url = video_urls[0]
                # 判断链接是否是视频（去除封面）
                for i in video_urls:
                    video = await client.get(i)
                    if video.status_code == 200:
                        content_type = video.headers.get('Content-Type', '').lower()
                        is_video = content_type.startswith('video/')
                        if is_video:
                            return video
                else:
                    return 0



def get_url_from_json(json_data):
    '''
    从json中获取所有的url
    
    :params json_data: json数据
    :return url_list: url列表
    '''
    url_list = []

    def traverse_json(data):
        if isinstance(data, str):
            # 判断是否为链接
            if data.startswith("http://") or data.startswith("https://"):
                url_list.append(data)
        elif isinstance(data, dict):
            for value in data.values():
                traverse_json(value)
        elif isinstance(data, list):
            for item in data:
                traverse_json(item)

    traverse_json(json_data)
    return url_list

@jktj.handle()
async def video_jktj():
    msg = ''
    for i in cmds_config:
        msg = msg + i + "\n"
    await jktj.finish(msg)

@add_api.got("video_name", prompt="请输入调用词")
@add_api.got("video_api", prompt="请输入图片接口")
async def add_video_api(video_api:str = ArgPlainText(), video_name:str = ArgPlainText()):
    # 检查api
    res = await get_video(video_api)
    if res:
        pass
    else:
        await add_api.finish("接口测试失败，请稍后再试或更换接口")
    
    # 检测调用词是否已存在
    if video_name in cmds:
        for cmd in cmds_config:
            if video_name in cmd:
                async with lock:
                    api_info = cmds_config.get(cmd)
                    api_info.append({"url":video_api})
                    with open(plugin_config_file, 'w', encoding='utf-8') as f:
                        yaml.dump(cmds_config, f, allow_unicode=True)
                await add_api.send("添加成功")
                break
    else:
        async with lock:
            cmds.append(video_name)
            cmds_config[video_name] = [{"url":video_api}]
            with open(plugin_config_file, 'w', encoding='utf-8') as f:
                yaml.dump(cmds_config, f, allow_unicode=True)
        await add_api.send("添加成功")

