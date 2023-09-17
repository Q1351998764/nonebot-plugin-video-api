from pydantic import BaseModel, Extra
import yaml
from pathlib import Path


config_path = Path('config/video_api_config.yml')

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
# 检查config文件夹是否存在 不存在则创建
if not Path("config").exists():
    Path("config").mkdir()
if not config_path.exists():
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(CONFIG_TEMPLATE, f, allow_unicode=True)  


with open(config_path,'r') as f:
    api_data = yaml.load(f,Loader=yaml.FullLoader)#读取yaml文件

class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    api_data = api_data
    proxies_http: str = None
