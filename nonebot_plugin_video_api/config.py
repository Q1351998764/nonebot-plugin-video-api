from pydantic import BaseModel, Extra
import yaml, nonebot
from pathlib import Path
from nonebot import require
require("nonebot_plugin_localstore")

import nonebot_plugin_localstore as store

plugin_config_dir: Path = store.get_config_dir("nonebot_plugin_video_api")

CONFIG_TEMPLATE = {
    #key值设置为要触发的词
    '小姐姐':[
        {'url': 'http://api.yujn.cn/api/zzxjj.php?type=video',# 在url字段后面写接口链接
        'is_proxy': False}, # 是否使用代理,默认为False
        {'url': 'http://api.yujn.cn/api/xjj.php'}
        # 可以采用这种格式进行一个关键词设置多个链接
    ],

    #也可以以"|"分隔设置多个触发词
    'dy|抖音':[
        {'url': 'https://api.yujn.cn/api/dy_hot.php'},     
    ],

}

global_config = nonebot.get_driver().config

try:
    # 检查.env中用户是否指定配置文件目录
    config_path = global_config.nonebot_plugin_video_config
    config_path = Path(config_path)
    # 检查用户指定的config文件夹是否存在 不存在则创建
    if not config_path.exists():
        config_path.mkdir()
except:
    # 使用默认路径
    config_path = plugin_config_dir

plugin_config_file = config_path.joinpath("video_api_config.yml")
if not plugin_config_file.exists():
    with open(plugin_config_file, 'w', encoding='utf-8') as f:
        yaml.dump(CONFIG_TEMPLATE, f, allow_unicode=True)  

with open(plugin_config_file,'r', encoding='utf-8') as f:
    api_data = yaml.load(f,Loader=yaml.FullLoader)#读取yaml文件

class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    api_data = api_data
    global_config = global_config
