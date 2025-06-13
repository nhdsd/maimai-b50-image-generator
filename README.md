# Maimai B50 Image Generator

让你无需加入任何QQ群也能生成舞萌的B50图片，社恐玩家的不二之选。  

> [!NOTE]
> 请查看[#4](https://github.com/nhdsd/maimai-b50-image-generator/issues/4)。当该 issue open 时则说明有生效中的公告。

## 使用方法

<details open>

### 0 安装`Python`
前往[`Python`官网](https://www.python.org/)安装。

### 1 注册查分账号
在[水鱼查分器](https://www.diving-fish.com/maimaidx/prober/)注册一个自己的账号，并按照网页提示导入你的数据。

### 2 下载最新版脚本
在[Release](https://github.com/nhdsd/maimai-b50-image-generator/releases)处下载最新版本。[从最新commit构建...](#非发布版) | [预发布版...](#预发布版)

### 3 下载资源文件
在[OneDrive](https://1drv.ms/u/c/68dff5f977fb346f/EasYNIMQBYlMsJFdviOkQfkBY7lDnkbooSRIxhd2ABxYIw?e=lYwnxL)处下载基础资源文件，
然后把`static`文件夹复制到程序根目录下。

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

<details> <summary>可选步骤</summary>

### 7 自定义头像与姓名框
在`custom`目录下保存你的头像与姓名框图片，然后[修改配置](#8-修改配置)。 

### 8 修改配置
用任意的文本编辑器打开`config.json`即可修改。[修改`config.json`...](#配置文件) | [配置文件的格式...](#JSON文件)

### 9 使用附加包提供的头像与姓名框
附加包提供了一些常见的头像与姓名框。在[OneDrive](https://1drv.ms/u/c/68dff5f977fb346f/EX_PkI8HREtHgI6Fyh1fy14BNFor-yevkQ314XCw9wRV3w?e=k7VWuB)处下载后
把`static`文件夹复制到程序根目录处与原有的文件夹合并即可。附加包中的头像与姓名框的编号为文件名中的数字，不含前导零。

</details>
</details>

## 帮助 & 疑难解答

<details open>

### 非发布版

目前此仓库分为`dev`和`main`两个分支。`dev`分支上的版本为非发布版。使用`git`将其`clone`后即可使用。

**非发布版的稳定性无法保证。** 当然，我们也无法保证发布版一定能100%无差错地运行，但是非发布版的问题总体更多，发生问题的概率总体更高。

### 预发布版
[Release](https://github.com/nhdsd/maimai-b50-image-generator/releases)中有一些`Pre-release`版本，它们是**预发布版**。按照使用正式版的方法使用它们即可。
预发布版的新特性与在[非发布版](#非发布版)中一样可以禁用。

**预发布版的稳定性只能得到部分保证。** 当然，我们也无法保证发布版一定能100%无差错地运行，但是预发布版的问题总体更多，发生问题的概率总体更高，不过相比非发布版它会更稳定。

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
**打开根目录下的`config.json`即可更改。** 参见[修改`config.json`...](#配置文件)

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
* [compound]根标签
|-- * [str]username | 查分器用户名。
|-- ~ [str, int]plate | 姓名框文件名或是编号。
|-- ~ [str, int]icon | 头像文件名或是编号。
|-- ~ [bool]plate_override | 是否允许牌子设置覆盖自定义姓名框设置。(false)
|-- ~ [bool]local_first | 是否优先从本地加载资源文件。(false)
|-- ~ [str(enum)]source | 数据来源。("diving_fish")

* 为必选项，[]中为类别，()中为默认值。
```
enum 类型配置项的所有可选项：
```
source | "diving_fish", "diving_fish_local"
```
你可以自行按照需求修改，删除此文件将重置所有配置。

### JSON文件
虽然我们在上文中提到可以使用文本编辑器打开`config.json`进行编辑，但是这是一个具有特定格式的`JSON`文件，破坏其格式会影响此程序运行。
查看[此教程](https://www.runoob.com/json/json-syntax.html)可以让你对此有初步了解，避免意外破坏格式。

</details>

## 开发中特性
- 从本地读取B50数据。
- 删去冗余逻辑，精简代码。

## 致谢

本项目的实现离不开：
- [alexliu07/maimai-b50-pc](https://github.com/alexliu07/maimai-b50-pc)。该项目启发了此项目的创建。此项目的代码是在该项目代码的基础上修改得到的；
- [Yuri-YuzuChaN/maimaiDX](https://github.com/Yuri-YuzuChaN/maimaiDX)。
  该项目是[alexliu07/maimai-b50-pc](https://github.com/alexliu07/maimai-b50-pc)的基础，
  本项目对[alexliu07/maimai-b50-pc](https://github.com/alexliu07/maimai-b50-pc)的修改也来自该项目。此外，部分[资源文件](#3-下载资源文件)也来自该项目；
- [Diving-Fish/maimaidx-prober](https://github.com/Diving-Fish/maimaidx-prober)。[水鱼查分器](https://www.diving-fish.com/maimaidx/prober/)项目。该项目为本项目的实现提供了API。

## 许可证

此项目使用[**MIT**许可证](./LICENSE)。

## 版本日志

参见[此处](./changelog.md)。
