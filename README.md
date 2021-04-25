# 约苗公众号HPV九价、四价、二价预约、订阅（暂时只支持当社区到苗可以预约时自动提醒，并不会自动预约抢苗，需要你手动进去预约）

## 准备环境
- python3环境，包括基础的各种包（运行时缺啥补啥，pip install ...)
- 抓包软件，我使用的Fiddler,可以参考这个[博客安装使用](https://blog.csdn.net/ychgyyn/article/details/82154433), 也可以使用其他抓包方法。
## 修改配置参数信息
- 首先抓包获取tk参数，并修改main.py文件中的[tk字段](main.py#L24)（抓包流程不讲解）
- 修改抢苗的个人信息和待抢的疫苗信息：[抢苗信息](YuemiaoPublicAccount/config.py)
- 修改有可预约的疫苗时发送邮件的[邮件登录信息](thirdparty/config.py)。如何获取邮箱授权码：[获取QQ邮箱授权码方法](https://service.mail.qq.com/cgi-bin/help?subtype=1&&no=1001256&&id=28)

## 功能
 目前暂时不支持直接自动预约功能，因为技术原因，自动预约所需要的参数问题暂未解决...，只可以查询是否存在可以预约的社区医院，然后发送邮件提示用户去登录预约。

### 订阅社区医院
- 通过区域id订阅该区域的所有社区医院：

`python main.py subscribe --region_id 4101`

- 通过社区名称订阅所有相关名称的社区：

`python main.py subscribe --name 新郑市龙湖镇`

- 通过省份名称订阅该省份所有社区医院：

`python main.py subscribe --province 河南省`

### 查询可预约的社区医院
- 通过区域id查询该区域的是否有社区医院可以预约：

`python main.py order --region_id 4101`

- 通过省份名称查询该省份所有社区医院中是否有可以预约的：

 `python main.py order --province 河南省`

- 通过社区名称是直接自动预约该社区（目前暂时不支持自动预约，因为加密问题未解决）：

`python main.py order --name 新郑市龙湖镇卫生院`

### 获取社区信息
- 通过区域id获取所有社区信息：

`python main.py info --region_id 4101`
  
- 通过社区名称获取所有社区信息（社区名称支持模糊名称）：

`python main.py info --name 新郑市龙湖镇卫生院`
  
- 通过省份名称获取所有社区信息：

`python main.py info --province 河南省`

所有的保存的信息存储路径可以在字段[save_departments_info_root](YuemiaoPublicAccount/config.py)中配置

### 获取已经到苗的社区信息
- 通过省份获取到苗社区信息：

`python main.py save --province 河南省`
  
- 获取全国到苗社区信息：

`python main.py save`

## 注意事项
- 在查询是否存在可预约的社区时，程序运行之后会一直运行，直到tk值失效或者查找到了可以预约的社区（之后会发送邮件提示）才会结束
- tk值根据我目前的测试，每次抓包获取之后有两个小时的时间，两个小时之后该tk值会失效，需要重新抓包获取
- 暂不支持自动预约功能，只有预约提示功能
- 目前不支持免费短信提示方式；如果你在榛子云上充值了，可以修改[榛子云信息](thirdparty/config.py)中的各种模板参数来实现发送短信提示。

