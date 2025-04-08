# Maimai B50 Image Generator

让你无需加入任何QQ群也能生成舞萌的B50图片，社恐玩家的不二之选。  

## 使用方法

### 0 安装`Python`
前往[`Python`官网](https://www.python.org/)安装。

### 1 注册查分账号
在[水鱼查分器](https://www.diving-fish.com/maimaidx/prober/)注册一个自己的账号，并按照网页提示导入你的数据。

### 2 下载最新版脚本
在[Release](https://github.com/nhdsd/maimai-b50-image-generator/releases)处下载最新版本。[从最新commit构建...](#非发布版) | [预发布版...](#预发布版)

### 3 下载资源文件
前往[OneDrive](https://yuzuai-my.sharepoint.com/:u:/g/personal/yuzuchan_yuzuai_onmicrosoft_com/EaS3jPYdMwxGiU3V_V64nRIBk6QA5Gdhs2TkJQ2bLssxbw?e=Mm6cWY)或者[私人云盘](https://share.yuzuchan.moe/d/aria/Resource.zip?sign=LOqwqDVm95dYnkEDYKX2E-VGj0xc_JxrsFnuR1BcvtI=:0)下载文件，把解压后的`static`文件夹移动至本程序目录下。

### 4 安装依赖
在程序根目录下，启动`Powershell`或者命令提示符，然后运行：
```bash
pip install -r requirements.txt
```
等待命令运行完毕。[报错了...](#pip运行失败)

### 5 运行脚本
运行`b50.py`。第一次运行时它会询问你的用户名，请输入你在[注册查分账号](#1-注册查分账号)步骤中得到的用户名。后续生成均会沿用该用户名而不再询问。[更改用户名...](#更改用户名)

### 6 查看输出
在`output`文件夹中，查看输出的B50。[图片数据不对...](#图片数据错误) | [没生成图片...](#图片未生成)

---

> [!NOTE]
> 以下步骤为可选的。

### 7 自定义头像与姓名框
在程序根目录下保存你的头像与姓名框图片，然后修改`config.json`。 [修改`config.json`...](#配置文件)

## 帮助 & 疑难解答

### 非发布版

目前此仓库仅仅是一个`Python`脚本，因此你可以`git clone`此仓库，以直接使用最新的非发布版本。  
直接对此仓库施行`git clone`后请将`b50.py`中`WIP = True`改为`WIP = False`，以禁用未完成并会可能引起错误的特性，除非你是有意想测试/完善此特性。详见[开发中特性](#开发中特性)。

> [!WARNING]
> **非发布版的稳定性无法保证。** 当然，我们也无法保证发布版一定能100%无差错地运行，但是非发布版的问题总体更多，发生问题的概率总体更高。

### 预发布版
[Release](https://github.com/nhdsd/maimai-b50-image-generator/releases)中有一些`Pre-release`版本，它们是**预发布版**。按照使用正式版的方法使用它们即可。
预发布版的新特性与在[非发布版](#非发布版)中一样可以禁用。

> [!WARNING]
> **预发布版的稳定性只能得到部分保证。** 当然，我们也无法保证发布版一定能100%无差错地运行，但是预发布版的问题总体更多，发生问题的概率总体更高，不过相比非发布版它会更稳定。

### `pip`运行失败

如果提示：
```
pip : 无法将“pip”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请
确保路径正确，然后再试一次。
所在位置 行:1 字符: 1
+ pip
+ ~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (pip) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
```
(Powershell)  
```
'pip' 不是内部或外部命令，也不是可运行的程序
或批处理文件。
```
(命令提示符)  
可以先考虑换用另一种终端。如果仍然出现上述错误，请**检查你的环境变量**。如果你不清楚这是什么，**请重新安装`Python`，并确保你勾选了`Add Python to system PATH`。**  
**如果出现的不是上述错误，可能是`pip`自身运行出现问题，请考虑检查网络环境。**

### 更改用户名
**打开根目录下的`config.json`即可更改。**参见[修改`config.json`...](#配置文件)

### 图片数据错误
在极端情况下有些账号无法从API处获取正确的信息。这会导致生成器按照错误的信息生成，自然得到的是错误的图片。此时**请[重新注册一次查分账号](#1-注册查分账号)，按照[此处](#更改用户名)的说明修改后再试一次**。

### 图片未生成
请在根目录下启动`Powershell`或命令提示符并运行：
```bash
py ./b50.py
```
- **如果提示失败并给出了解决方案，请先按照指示操作。**
- **如果没有给出解决方案，请注意是否出现了`ImportError`，若出现了，请检查[安装依赖](#4-安装依赖)步骤是否正常进行。**
- **如果出现类似[此处](#pip运行失败)的报错，请参见相应的解决方案。**
- **如果上述方法均无效，请截屏并[提交 issue](https://github.com/nhdsd/maimai-b50-image-generator/issues/new)。**

### 配置文件
自[`1.1.0-rc1`](https://github.com/nhdsd/maimai-b50-image-generator/releases/tag/v1.1.0-rc1)起，脚本的配置改为使用`JSON`文件。
文件的格式如下：
```
* 根标签。(Compound)
|-- * username | 查分器用户名。(String)
|-- ~ plate | 姓名框文件名。也可以是以此软件根目录为起点的相对路径。(String)
|-- ~ icon | 头像文件名。也可以是以此软件根目录为起点的相对路径。(String)

[* 为必选项。]
```
你可以自行按照需求修改，删除此文件将重置所有配置。

## 开发中特性

- ~~自定义头像与姓名框。~~(已完成，`v1.1.0-rc1`测试中)
- 重构代码。

## 致谢

本项目的实现离不开：
- [alexliu07/maimai-b50-pc](https://github.com/alexliu07/maimai-b50-pc)。该项目启发了此项目的创建。此项目的代码是在该项目代码的基础上修改得到的；
- [Yuri-YuzuChaN/maimaiDX](https://github.com/Yuri-YuzuChaN/maimaiDX)。该项目是[alexliu07/maimai-b50-pc](https://github.com/alexliu07/maimai-b50-pc)的基础，本项目对[alexliu07/maimai-b50-pc](https://github.com/alexliu07/maimai-b50-pc)的修改也来自该项目。此外，[资源文件](#3-下载资源文件)也来自该项目；
- [Diving-Fish/maimaidx-prober](https://github.com/Diving-Fish/maimaidx-prober)。[水鱼查分器](https://www.diving-fish.com/maimaidx/prober/)项目。该项目为本项目的实现提供了API。

## 许可证

此项目使用[**MIT**许可证](./LICENSE)。

## 版本日志

### [v1.1.0-rc1](https://github.com/nhdsd/maimai-b50-image-generator/releases/tag/v1.1.0-rc1) (Pre-release) (20250408)

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
> 根据Semver规范，这些功能将在`2.0.0`版本中彻底删除。

### [v1.0.0](https://github.com/nhdsd/maimai-b50-image-generator/releases/tag/v1.0.0) (20250407)

- 基本功能实现
