<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-video-api

_✨ 一款可以自由增删视频指令和api的插件 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Q1351998764/nonebot-plugin-video-api.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-video-api">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-video-api.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>



## 📖 介绍

在我调用各种视频api的时候，觉得每个api取一个指令并写一个小插件太麻烦了，因此写了本插件，只需配置yml即可增添视频api以及触发指令

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-video-api

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

    pip install nonebot-plugin-video-api
    
打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_video_api"]

</details>

## ⚙️ 配置
配置可参考https://github.com/Q1351998764/nonebot-plugin-picture-api


- 注: 本插件的默认配置使用nonebot_plugin_localstore生成，linux系统中位置为~/.config/nonebot-plugin-video-api/video_api_config.yml，该文件会在插件第一次运行时自动生成。当然，本插件的配置文件目录也可以由用户手动指定，如下所示

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| nonebot_plugin_video_config | 否 | 无 | 配置文件目录 |

- 其内容如同介绍中的截图所示。
写法如下所示：
```
dy|抖音:
- url: https://api.yujn.cn/api/dy_hot.php
```

其中，dy|抖音 代表api的触发指令，用"dy"或者是"抖音"均可触发。url后跟api；is_proxy代表是否使用代理，可不写，默认false

也可在一个关键词下设置多个url，如下所示：

```
小姐姐:
- is_proxy: false
  url: http://api.yujn.cn/api/zzxjj.php?type=video
- url: http://api.yujn.cn/api/xjj.php
```
其中，is_proxy没写，采用默认值false

注：不论接口是直接返回图片，还是返回json，或者是返回图片链接，都可以按照上面的方式配置。

~~大概配置就这样~~。

## 🎉 使用
配置完后直接对机器人发送配置的指令即可，机器人将随机调用该指令下的一个接口。  

目前本插件新增指令添加视频接口的功能，指令为"添加视频接口"或"添加视频api"，添加成功后不需要重启nb即可立即使用接口。可以为一个关键词添加多个接口，在触发关键词时会随机调用
可参考
https://github.com/Q1351998764/nonebot-plugin-picture-api
