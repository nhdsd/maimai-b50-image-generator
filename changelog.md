# 版本日志

## [v1.2.0](https://github.com/nhdsd/maimai-b50-image-generator/releases/tag/v1.2.0)

<details>

> 此版本是从上一个发布候选版本(`rc`)转化而来的，没有实质性更改。

**修复**
因`GitHub`的`Markdown`渲染不支持，移除了`README.md`和`changelog.md`中位于`<details>`标签中的信息框。

`2025.04.15` | 正式版

</details>

## [v1.2.0-rc3](https://github.com/nhdsd/maimai-b50-image-generator/releases/tag/v1.2.0-rc3)

<details>

**修复**
- 牌子转化函数转换不完全([#2](https://github.com/nhdsd/maimai-b50-image-generator/issues/2))

> 基础包中本次修复对应的牌子文件目前缺失(需要下载附加包补全)，后续正式版将会把文件移动到基础包。

`2025.04.13` | 发布候选

</details>

## [v1.2.0-rc2](https://github.com/nhdsd/maimai-b50-image-generator/releases/tag/v1.2.0-rc2)

<details>

**修复**
- 修正了未完成的`README.md`以及其中的错误链接。

`2025.04.13` | 发布候选

</details>

## [v1.2.0-rc1](https://github.com/nhdsd/maimai-b50-image-generator/releases/tag/v1.2.0-rc1)

<details>

**新功能**
- 配置项`plate_override`：为`true`时，将在有牌子时覆盖本地的自定义姓名框设置。默认为`false`。
- 配置项`local_first`：为`true`时，将优先尝试从本地加载缓存的曲目与谱面数据。默认为`false`。

**更改的功能**
- 默认头像与姓名框改为游客样式。
- 配置项`icon`和`plate`：现在接受整数作为参数，这将使得程序从`static/icon`和`static/plate`下加载对应编号的文件。
  > 此功能需要增补资源包作为支持才能发挥功能。
- 自定义头像与姓名框的文件改为至`custom`文件夹读取。

**弃用**
- 自根目录读取自定义头像与姓名框

这些功能将在`2.0.0`版本中彻底删除。

`2025.04.13` | 发布候选

</details>

## [v1.1.0](https://github.com/nhdsd/maimai-b50-image-generator/releases/tag/v1.1.0)

<details>

> 此版本是从上一个发布候选版本(`rc`)转化而来的，没有实质性更改。

`2025.04.11` | 正式版

</details>

## [v1.1.0-rc1](https://github.com/nhdsd/maimai-b50-image-generator/releases/tag/v1.1.0-rc1)

<details>

**新功能**
- 自定义头像与姓名框\*
- 新的配置方式\*
- 生成计时\*
- 网络IO提示

**带有\*的功能可以被`WIP`标识关闭。**

**弃用**
- 自`user.txt`读取配置

这些功能将在`2.0.0`版本中彻底删除。

`2025.04.08` | 发布候选

</details>

## [v1.0.0](https://github.com/nhdsd/maimai-b50-image-generator/releases/tag/v1.0.0)

<details>

- 基本功能实现

`2025.04.07` | 正式版

</details>
