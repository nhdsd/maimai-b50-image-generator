# 版本日志

## [v1.2.0-rc2](https://github.com/nhdsd/maimai-b50-image-generator/releases/tag/v1.2.0-rc2)

**修复**
- 修正了未完成的`README.md`以及其中的错误链接。

`2025.04.13` | 发布候选

## [v1.2.0-rc1](https://github.com/nhdsd/maimai-b50-image-generator/releases/tag/v1.2.0-rc1)

**新功能**
- 配置项`plate_override`：为`true`时，将在有牌子时覆盖本地的自定义姓名框设置。默认为`false`。
- 配置项`local_first`：为`true`时，将优先尝试从本地加载缓存的曲目与谱面数据。默认为`false`。

**更改的功能**
- 默认头像与姓名框改为游客样式。
- 配置项`icon`和`plate`：现在接受整数作为参数，这将使得程序从`static/icon`和`static/plate`下加载对应编号的文件。
  > 此功能需要增补资源包作为支持才能发挥功能。
- 自定义头像与姓名框的文件改为至`custom`文件夹读取。

> [!WARNING]
> **自此版本起标记为弃用的功能：**
> - 自根目录读取自定义头像与姓名框
> 
> 这些功能将在`2.0.0`版本中彻底删除。

`2025.04.13` | 发布候选

## [v1.1.0](https://github.com/nhdsd/maimai-b50-image-generator/releases/tag/v1.1.0)

> 此版本是从上一个发布候选版本(`rc`)转化而来的，没有实质性更改。

`2025.04.11` | 正式版

## [v1.1.0-rc1](https://github.com/nhdsd/maimai-b50-image-generator/releases/tag/v1.1.0-rc1)

**新功能**
- 自定义头像与姓名框\*
- 新的配置方式\*
- 生成计时\*
- 网络IO提示

**带有\*的功能可以被`WIP`标识关闭。**

> [!WARNING]
> **自此版本起标记为弃用的功能：**
> - 自`user.txt`读取配置
> 
> 这些功能将在`2.0.0`版本中彻底删除。

`2025.04.08` | 发布候选版

## [v1.0.0](https://github.com/nhdsd/maimai-b50-image-generator/releases/tag/v1.0.0)

- 基本功能实现

`2025.04.07` | 正式版
