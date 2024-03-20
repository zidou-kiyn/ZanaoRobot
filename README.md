# 注意事项

本项目可以一键拷贝使用，只要环境搭建好（nodejs、python的requests、openai、pyexecjs库），接着修改js文件中的YOUR_USER_TOKEN和robot中的YOUR_API_KEY
使用本项目被管理员禁言与作者无关（）

# Github仓库地址

[zidou-kiyn/ZanaoRobot: 逆向生涯_01_大闹“赞噢校园集市” (github.com)](https://github.com/zidou-kiyn/ZanaoRobot)

# 引言

> 感谢赏脸点进这篇我~耗尽毕生**coding_ability**~完成的小玩意儿的小老弟、小老妹还有小哥哥、小姐姐们。

首先，该项目的起因是在集市冲浪时，惊叹于**瓶酱**教授的风姿，又苦于自身的交际能力过于薄弱，结合当今风头正盛的***LLM（大语言模型）***，就想着开发一个能够代替我对集市中的帖子进行评论的robot。

其次，我就要解释一下标题'逆向生涯\_01\_大闹“赞噢校园集市”'的含义了。

**大闹**是诙谐的说法，在该项目中，我通过**逆向工程**的手段获得了校园集市**sign**的加密算法，从而通过**python**发送请求给赞噢校园集市的服务器进行帖子列表的获取和评论的发送。

又对接了*openai*的***ChatGPT-Turbo-1106***模型api对每一条帖子进行回复。

<img src="https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104220632.png" style="zoom: 50%;" />

限于大模型的数据量和我自身编写的prompt的不足，导致回复的内容颇有不符之处。导致管理员接到其他用户举报后禁言了我的账号。

<img src="https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104220407.png" style="zoom: 50%;" />

---

# 分析

## 抓包工具-Fidder

我们想要获取集市的接口，就要有一个合适的抓包工具。

在这个项目的分析中，我使用的是***Fidder***，一个耳熟能详的工具。

> 在这里附上CSDN上的一位大佬撰写的Fidder的配置和介绍
>
> [Fiddler安装与使用教程（1） —— 软测大玩家-CSDN博客](https://blog.csdn.net/weixin_38306507/article/details/132559736)

<img src="https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104222015.png" style="zoom:50%;" />

---

## 分析请求帖子接口

接下来就是打开抓包工具，打开集市小程序的首页，分析***请求（request）***的构成

经过观察，我们很快就发现了得到帖子列表的接口。

单击在右侧窗口可以发现这是一个**GET**请求。

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104222347.png)

单击后我们也可以发现返回的数据赫然便是帖子的数据，正是我们要的接口！

<img src="https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104222714.png" style="zoom: 80%;" />

接下来，对***请求头（headers）***、***请求参数（params）***进行分析

### 请求头

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/image-20240104223053068.png)

在请求头中我们可以看到几个特有的参数（需要添加到请求头中的参数以粗体显示），分别是：

- **X-Sc-Ah**：这是一串加密后的字段，暂时还不知道是什么，需要通过**逆向**获得。
- **X-Sc-Alias**：这一看就是郑州大学的缩写，可以固定，不用逆向。
- X-Sc-Appid：Appid应该是微信小程序的一个id，我之后试过，不添加这个参数也可以请求，略过。
- X-Sc-Cloud：是一个固定值，同样的可以不加入请求头，略过。
- **X-Sc-Nd**：也是一串变化的数值，需要**逆向**获得
- **X-Sc-Od**：这一段是一个很奇怪的字符串，但是是固定的，后面我发现这是用户token，可以直接固定，略过。
- X-Sc-Platform：请求的平台，可以不添加到请求头中。
- **X-Sc-Td**：一段变化的数值，在逆向的时候发现是***时间戳（timestamp）***
- X-Sc-Version：版本号，不需要，略过。

### 请求参数

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/image-20240104223800465.png)

这两个参数都是可以固定的，我们在请求的时候加上即可。

---

## 分析评论帖子接口

我们打开抓包工具，并对一个帖子进行回复，定位评论接口的位置。

定位到的接口如图所示，这是一个post请求。包含请求头和请求体。

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/image-20240104224129588.png)

### 请求头

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104224228.png)

可见与前文的请求头需要的参数是相同的

### 请求体

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104224412.png)

- **id**：通过观察请求接口返回的帖子信息，可以知道id与thread_id是同一个东西，用来定位帖子，即帖子ID。
- **content**：这便是评论的内容了。
- reply_comment_id：与回复评论有关，默认即可。
- root_comment_id：与回复评论有关，默认即可。

---

## 总结

分析完上述内容，对该项目的开发就有了一个清晰的思路：

1. 对小程序加密算法进行逆向
2. 使用python构建请求
3. 使用python对接openai的大语言模型

# 小程序逆向

要对小程序进行逆向，首先我们要做好充分的准备。

## 准备工具

- **UnpackMiniApp**：对微信小程序进行解密的工具
- **unveilr**：对解密后的微信小程序进行反编译的工具（注意，这个叫unveilr，是**免费**工具。不叫*unveiler*！！！）
- **微信开发者工具**：调试反编译后的微信小程序的工具（出自微信官方，~以魔法打败魔法！~）

以上工具我已经上传到[ZanaoRobot/resources at main · zidou-kiyn/ZanaoRobot (github.com)](https://github.com/zidou-kiyn/ZanaoRobot/tree/main/resources)中，访问即可下载

解压密码为：**zidoukn.cn**

（没错，就是我的博客网址）

## 获取微信小程序所在包

这里使用的是电脑端。

### 定位路径

微信客户端在设置中打开**文件夹位置**，通过相对路径，找到**WeChat Files/Applet/**这个路径

<img src="https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104232011.png" style="zoom:50%;" />

<img src="https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104231927.png" style="zoom:67%;" />

### 删除所有小程序

将该目录下除却`publicLib`和`publicTestLib`的文件夹删除，方便排除其他无关小程序，定位到集市小程序

如下所示

<img src="https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104232313.png" style="zoom:50%;" />

### 获取集市小程序包

启动赞噢校园集市小程序

在新生成的文件夹中寻找到小程序的包（只有一个文件），如图所示，可以看到生成的文件名就是上面抓包抓到的Appid，因此，也可以不用删除其他小程序获得该包

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104232538.png)

复制该包的文件路径

### 解包

打开`UnpackMiniApp.exe`，对该包进行解包

结果会出现在`UnpackMiniApp.exe`同目录的`wxpack`文件夹中

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104232812.png)

（强迫症这里将生成的包重命名为`__APP__.wxapkg`注意后缀，把显示后缀打开，不然就23333...)

结果如下

<img src="https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104233011.png" style="zoom:67%;" />

复制这个文件**所在目录**的路径

### 解密

在`unveilr.exe`所在目录的打开终端

输入以下内容

```cmd
unveilr.exe <目录路径>
```

成功结果如下

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104233406.png)

这时候那个目录下面生成了`__APP__`这么个文件夹

## 微信开发者工具使用

### 初始配置

使用微信开发者工具的时候我们可以登录使用。并且[申请一个测试号](https://developers.weixin.qq.com/miniprogram/dev/devtools/sandbox.html)。（扫个码就能申请，很快）

在首页我们导入一个项目

<img src="https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104233855.png" style="zoom:50%;" />

选择刚刚生成的这个文件夹

<img src="https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104233925.png" style="zoom: 50%;" />

<img src="https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104234004.png" style="zoom:50%;" />

- 项目名称：随意
- 目录：选择刚刚生成的文件夹
- AppID：使用测试号
- 开发模式：默认
- 后端服务：不使用云服务

然后**确定**

<img src="https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104234132.png" style="zoom: 33%;" />

对弹出的警告-**信任并运行**

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104234258.png)

进行一些初始设置：

1. 点开详情
2. 点击本地设置
3. **取消**将JS编译成ESS
4. **打勾**不检验合法域名···

---

此时，“手机”界面上显示编译`.wxml`文件错误，这一般是没有格式化的问题

我们点击console中的路径，进入这个`.wxml`文件并对它进行格式化

<img src="https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104234608.png" style="zoom:50%;" />

在文件中右键，格式化文档。ctrl+s保存。

<img src="https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104234656.png" style="zoom:50%;" />

这时候发现左侧窗口能运行了，但是会登陆失败。

我们是无法登录的，但是在这个过程中我们却能逆向到加密算法！！！

---

### 定位加密算法

> 这一个步骤需要准备pycharm（或者vscode等IDE），以及nodejs的环境。配置百度即可。

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104235134.png)

在调试器的`Network`中我们可以看到`wxlogin`这个请求（我点了一遍刷新，所以有两个）

点击其中一个，并且在弹出的窗口中点击***启动器（Initiator）***，进入最后一个调用的***堆栈（stack）***

<img src="https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104235334.png"  />

点击左下角的图标，进行格式化。

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104235430.png)

可以发现最后一个调用的堆栈停在`O.send(P)`

我们在这一行打上断点，刷新，当程序`debugger`到的时候，在控制台输出一下这个P是什么。（刷新在运行窗口的上面有个标志）

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104235621.png)

发现P是一个`code=***`的字符串。当我们回到***源文件（Sources）***，放行之后，发现运行窗口就浮现登陆失败。说明这个P是登录校验所用的东西。

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240104235743.png)

---

不过我们不需要分析这些，因为看到前两行P是`t.data`后，我又去断点打印t的值，发现t里面含有我们所需要的那些加密数据，并且早已生成。

不过既然没有进行混淆，我们就直接**search**！

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240105000444.png)

快捷键是ctrl+shift+F，注意是右上角的search，才能在源文件中搜索

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240105000527.png)

太好了，可以看到只有一个文件，我们进入，格式化，再使用ctrl+F在这个源文件中单独搜索，就找到了加密位置！

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240105000608.png)

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240105000624.png)

---

### 扣代码

> 接下来就是扣js代码，在pycharm中使用js复现辣！
>
> 在这里打上断点，并且让程序运行到这里。
>
> 然后我们一个个去扣m啊，h啊，b啊这些值分别是怎么生成的

程序断到这里后，我们使用ctrl+F在源文件中搜索m =，找到m的生成位置。发现m其实是这行代码生成的`i.Utils.getRandNum(20)`，看方法名，应该是得到一个随机数字。这里还有一个`i`类，直接扣下来！

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240105001145.png)

> 扣代码呢，其实就是把代码复制到自己的js文件中去调试运行。
>
> 这里我在pycharm新建一个js文件，然后把这行代码复制进去

这里进入`getRandNum()`方法里面，发现这个方法可以独立运行，所以就不用扣`i`辣，直接改写方法就能运行

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240105001447.png)

成功获取Nd的值！

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240105001611.png)

同理找到h的生成方法，进入，发现其实是一个得到时间戳的函数，那就直接复制

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240105001708.png)

成功运行！

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240105001900.png)

---

以上这两个都是小case，开胃菜

后面获得`X-Sc-Ah`才是大头！

我们发现，b是这行代码生成的

`b = r(g + "_" + m + "_" + h + "_1b6d2514354bc407afdd935f45521a8c");`

其中有四个位置的量

1. **r()**：一个未知方法
2. g：其实就是alias，郑州大学的就是”zzu“直接固定即可
3. m：就是上面随机生成的20位数值
4. h：就是时间戳

所以现在只有一个难点：扣`r()`方法

进去后里面有很多方法，还有一个导出的方法，我们只要把首尾给去掉，再修改一下导出函数即可（这个js很短，灰常简单，这就是**全扣**）

（由于上文的h会影响到下面的一个方法，所以要把上面的**h改成td**！！！！）

全扣的代码如下

```javascript
function n(n, r) {
    var t = (65535 & n) + (65535 & r);
    return (n >> 16) + (r >> 16) + (t >> 16) << 16 | 65535 & t
}
function r(r, t, e, o, u, c) {
    return n((f = n(n(t, r), n(o, c))) << (i = u) | f >>> 32 - i, e);
    var f, i
}
function t(n, t, e, o, u, c, f) {
    return r(t & e | ~t & o, n, t, u, c, f)
}
function e(n, t, e, o, u, c, f) {
    return r(t & o | e & ~o, n, t, u, c, f)
}
function o(n, t, e, o, u, c, f) {
    return r(t ^ e ^ o, n, t, u, c, f)
}
function u(n, t, e, o, u, c, f) {
    return r(e ^ (t | ~o), n, t, u, c, f)
}
function c(r, c) {
    var f, i, a, h, g;
    r[c >> 5] |= 128 << c % 32,
    r[14 + (c + 64 >>> 9 << 4)] = c;
    var l = 1732584193
      , v = -271733879
      , d = -1732584194
      , C = 271733878;
    for (f = 0; f < r.length; f += 16)
        i = l,
        a = v,
        h = d,
        g = C,
        l = t(l, v, d, C, r[f], 7, -680876936),
        C = t(C, l, v, d, r[f + 1], 12, -389564586),
        d = t(d, C, l, v, r[f + 2], 17, 606105819),
        v = t(v, d, C, l, r[f + 3], 22, -1044525330),
        l = t(l, v, d, C, r[f + 4], 7, -176418897),
        C = t(C, l, v, d, r[f + 5], 12, 1200080426),
        d = t(d, C, l, v, r[f + 6], 17, -1473231341),
        v = t(v, d, C, l, r[f + 7], 22, -45705983),
        l = t(l, v, d, C, r[f + 8], 7, 1770035416),
        C = t(C, l, v, d, r[f + 9], 12, -1958414417),
        d = t(d, C, l, v, r[f + 10], 17, -42063),
        v = t(v, d, C, l, r[f + 11], 22, -1990404162),
        l = t(l, v, d, C, r[f + 12], 7, 1804603682),
        C = t(C, l, v, d, r[f + 13], 12, -40341101),
        d = t(d, C, l, v, r[f + 14], 17, -1502002290),
        l = e(l, v = t(v, d, C, l, r[f + 15], 22, 1236535329), d, C, r[f + 1], 5, -165796510),
        C = e(C, l, v, d, r[f + 6], 9, -1069501632),
        d = e(d, C, l, v, r[f + 11], 14, 643717713),
        v = e(v, d, C, l, r[f], 20, -373897302),
        l = e(l, v, d, C, r[f + 5], 5, -701558691),
        C = e(C, l, v, d, r[f + 10], 9, 38016083),
        d = e(d, C, l, v, r[f + 15], 14, -660478335),
        v = e(v, d, C, l, r[f + 4], 20, -405537848),
        l = e(l, v, d, C, r[f + 9], 5, 568446438),
        C = e(C, l, v, d, r[f + 14], 9, -1019803690),
        d = e(d, C, l, v, r[f + 3], 14, -187363961),
        v = e(v, d, C, l, r[f + 8], 20, 1163531501),
        l = e(l, v, d, C, r[f + 13], 5, -1444681467),
        C = e(C, l, v, d, r[f + 2], 9, -51403784),
        d = e(d, C, l, v, r[f + 7], 14, 1735328473),
        l = o(l, v = e(v, d, C, l, r[f + 12], 20, -1926607734), d, C, r[f + 5], 4, -378558),
        C = o(C, l, v, d, r[f + 8], 11, -2022574463),
        d = o(d, C, l, v, r[f + 11], 16, 1839030562),
        v = o(v, d, C, l, r[f + 14], 23, -35309556),
        l = o(l, v, d, C, r[f + 1], 4, -1530992060),
        C = o(C, l, v, d, r[f + 4], 11, 1272893353),
        d = o(d, C, l, v, r[f + 7], 16, -155497632),
        v = o(v, d, C, l, r[f + 10], 23, -1094730640),
        l = o(l, v, d, C, r[f + 13], 4, 681279174),
        C = o(C, l, v, d, r[f], 11, -358537222),
        d = o(d, C, l, v, r[f + 3], 16, -722521979),
        v = o(v, d, C, l, r[f + 6], 23, 76029189),
        l = o(l, v, d, C, r[f + 9], 4, -640364487),
        C = o(C, l, v, d, r[f + 12], 11, -421815835),
        d = o(d, C, l, v, r[f + 15], 16, 530742520),
        l = u(l, v = o(v, d, C, l, r[f + 2], 23, -995338651), d, C, r[f], 6, -198630844),
        C = u(C, l, v, d, r[f + 7], 10, 1126891415),
        d = u(d, C, l, v, r[f + 14], 15, -1416354905),
        v = u(v, d, C, l, r[f + 5], 21, -57434055),
        l = u(l, v, d, C, r[f + 12], 6, 1700485571),
        C = u(C, l, v, d, r[f + 3], 10, -1894986606),
        d = u(d, C, l, v, r[f + 10], 15, -1051523),
        v = u(v, d, C, l, r[f + 1], 21, -2054922799),
        l = u(l, v, d, C, r[f + 8], 6, 1873313359),
        C = u(C, l, v, d, r[f + 15], 10, -30611744),
        d = u(d, C, l, v, r[f + 6], 15, -1560198380),
        v = u(v, d, C, l, r[f + 13], 21, 1309151649),
        l = u(l, v, d, C, r[f + 4], 6, -145523070),
        C = u(C, l, v, d, r[f + 11], 10, -1120210379),
        d = u(d, C, l, v, r[f + 2], 15, 718787259),
        v = u(v, d, C, l, r[f + 9], 21, -343485551),
        l = n(l, i),
        v = n(v, a),
        d = n(d, h),
        C = n(C, g);
    return [l, v, d, C]
}
function f(n) {
    var r, t = "", e = 32 * n.length;
    for (r = 0; r < e; r += 8)
        t += String.fromCharCode(n[r >> 5] >>> r % 32 & 255);
    return t
}
function i(n) {
    var r, t = [];
    for (t[(n.length >> 2) - 1] = void 0,
    r = 0; r < t.length; r += 1)
        t[r] = 0;
    var e = 8 * n.length;
    for (r = 0; r < e; r += 8)
        t[r >> 5] |= (255 & n.charCodeAt(r / 8)) << r % 32;
    return t
}
function a(n) {
    var r, t, e = "";
    for (t = 0; t < n.length; t += 1)
        r = n.charCodeAt(t),
        e += "0123456789abcdef".charAt(r >>> 4 & 15) + "0123456789abcdef".charAt(15 & r);
    return e
}
function h(n) {
    return unescape(encodeURIComponent(n))
}
function g(n) {
    return function(n) {
        return f(c(i(n), 8 * n.length))
    }(h(n))
}
function l(n, r) {
    return function(n, r) {
        var t, e, o = i(n), u = [], a = [];
        for (u[15] = a[15] = void 0,
        o.length > 16 && (o = c(o, 8 * n.length)),
        t = 0; t < 16; t += 1)
            u[t] = 909522486 ^ o[t],
            a[t] = 1549556828 ^ o[t];
        return e = c(u.concat(i(r)), 512 + 8 * r.length),
        f(c(a.concat(e), 640))
    }(h(n), h(r))
}
function get_b(n, r, t) {
    return r ? t ? l(r, n) : a(l(r, n)) : t ? g(n) : a(g(n))
}



b = get_b("zzu" + "_" + m + "_" + td + "_1b6d2514354bc407afdd935f45521a8c")
```

其他的值基本是固定的，不过X-Sc-Od是用户token，直接复制fidder中的值即可

## 完整js代码

整理一下，方便python调用js文件，整理后的代码如下

记得替换`YOUR_USER_TOKEN`

```javascript
function get_m(e) {
    for (var t = "", r = 0; r < e; r++)
        t += Math.floor(10 * Math.random());
    return t
}

m = get_m(20)


function get_h() {
    var e = (new Date).getTime().toString().substr(0, 10);
    return parseInt(e, 10)
}

td = get_h()


function n(n, r) {
    var t = (65535 & n) + (65535 & r);
    return (n >> 16) + (r >> 16) + (t >> 16) << 16 | 65535 & t
}

function r(r, t, e, o, u, c) {
    return n((f = n(n(t, r), n(o, c))) << (i = u) | f >>> 32 - i, e);
    var f, i
}

function t(n, t, e, o, u, c, f) {
    return r(t & e | ~t & o, n, t, u, c, f)
}

function e(n, t, e, o, u, c, f) {
    return r(t & o | e & ~o, n, t, u, c, f)
}

function o(n, t, e, o, u, c, f) {
    return r(t ^ e ^ o, n, t, u, c, f)
}

function u(n, t, e, o, u, c, f) {
    return r(e ^ (t | ~o), n, t, u, c, f)
}

function c(r, c) {
    var f, i, a, h, g;
    r[c >> 5] |= 128 << c % 32,
        r[14 + (c + 64 >>> 9 << 4)] = c;
    var l = 1732584193
        , v = -271733879
        , d = -1732584194
        , C = 271733878;
    for (f = 0; f < r.length; f += 16)
        i = l,
            a = v,
            h = d,
            g = C,
            l = t(l, v, d, C, r[f], 7, -680876936),
            C = t(C, l, v, d, r[f + 1], 12, -389564586),
            d = t(d, C, l, v, r[f + 2], 17, 606105819),
            v = t(v, d, C, l, r[f + 3], 22, -1044525330),
            l = t(l, v, d, C, r[f + 4], 7, -176418897),
            C = t(C, l, v, d, r[f + 5], 12, 1200080426),
            d = t(d, C, l, v, r[f + 6], 17, -1473231341),
            v = t(v, d, C, l, r[f + 7], 22, -45705983),
            l = t(l, v, d, C, r[f + 8], 7, 1770035416),
            C = t(C, l, v, d, r[f + 9], 12, -1958414417),
            d = t(d, C, l, v, r[f + 10], 17, -42063),
            v = t(v, d, C, l, r[f + 11], 22, -1990404162),
            l = t(l, v, d, C, r[f + 12], 7, 1804603682),
            C = t(C, l, v, d, r[f + 13], 12, -40341101),
            d = t(d, C, l, v, r[f + 14], 17, -1502002290),
            l = e(l, v = t(v, d, C, l, r[f + 15], 22, 1236535329), d, C, r[f + 1], 5, -165796510),
            C = e(C, l, v, d, r[f + 6], 9, -1069501632),
            d = e(d, C, l, v, r[f + 11], 14, 643717713),
            v = e(v, d, C, l, r[f], 20, -373897302),
            l = e(l, v, d, C, r[f + 5], 5, -701558691),
            C = e(C, l, v, d, r[f + 10], 9, 38016083),
            d = e(d, C, l, v, r[f + 15], 14, -660478335),
            v = e(v, d, C, l, r[f + 4], 20, -405537848),
            l = e(l, v, d, C, r[f + 9], 5, 568446438),
            C = e(C, l, v, d, r[f + 14], 9, -1019803690),
            d = e(d, C, l, v, r[f + 3], 14, -187363961),
            v = e(v, d, C, l, r[f + 8], 20, 1163531501),
            l = e(l, v, d, C, r[f + 13], 5, -1444681467),
            C = e(C, l, v, d, r[f + 2], 9, -51403784),
            d = e(d, C, l, v, r[f + 7], 14, 1735328473),
            l = o(l, v = e(v, d, C, l, r[f + 12], 20, -1926607734), d, C, r[f + 5], 4, -378558),
            C = o(C, l, v, d, r[f + 8], 11, -2022574463),
            d = o(d, C, l, v, r[f + 11], 16, 1839030562),
            v = o(v, d, C, l, r[f + 14], 23, -35309556),
            l = o(l, v, d, C, r[f + 1], 4, -1530992060),
            C = o(C, l, v, d, r[f + 4], 11, 1272893353),
            d = o(d, C, l, v, r[f + 7], 16, -155497632),
            v = o(v, d, C, l, r[f + 10], 23, -1094730640),
            l = o(l, v, d, C, r[f + 13], 4, 681279174),
            C = o(C, l, v, d, r[f], 11, -358537222),
            d = o(d, C, l, v, r[f + 3], 16, -722521979),
            v = o(v, d, C, l, r[f + 6], 23, 76029189),
            l = o(l, v, d, C, r[f + 9], 4, -640364487),
            C = o(C, l, v, d, r[f + 12], 11, -421815835),
            d = o(d, C, l, v, r[f + 15], 16, 530742520),
            l = u(l, v = o(v, d, C, l, r[f + 2], 23, -995338651), d, C, r[f], 6, -198630844),
            C = u(C, l, v, d, r[f + 7], 10, 1126891415),
            d = u(d, C, l, v, r[f + 14], 15, -1416354905),
            v = u(v, d, C, l, r[f + 5], 21, -57434055),
            l = u(l, v, d, C, r[f + 12], 6, 1700485571),
            C = u(C, l, v, d, r[f + 3], 10, -1894986606),
            d = u(d, C, l, v, r[f + 10], 15, -1051523),
            v = u(v, d, C, l, r[f + 1], 21, -2054922799),
            l = u(l, v, d, C, r[f + 8], 6, 1873313359),
            C = u(C, l, v, d, r[f + 15], 10, -30611744),
            d = u(d, C, l, v, r[f + 6], 15, -1560198380),
            v = u(v, d, C, l, r[f + 13], 21, 1309151649),
            l = u(l, v, d, C, r[f + 4], 6, -145523070),
            C = u(C, l, v, d, r[f + 11], 10, -1120210379),
            d = u(d, C, l, v, r[f + 2], 15, 718787259),
            v = u(v, d, C, l, r[f + 9], 21, -343485551),
            l = n(l, i),
            v = n(v, a),
            d = n(d, h),
            C = n(C, g);
    return [l, v, d, C]
}

function f(n) {
    var r, t = "", e = 32 * n.length;
    for (r = 0; r < e; r += 8)
        t += String.fromCharCode(n[r >> 5] >>> r % 32 & 255);
    return t
}

function i(n) {
    var r, t = [];
    for (t[(n.length >> 2) - 1] = void 0,
             r = 0; r < t.length; r += 1)
        t[r] = 0;
    var e = 8 * n.length;
    for (r = 0; r < e; r += 8)
        t[r >> 5] |= (255 & n.charCodeAt(r / 8)) << r % 32;
    return t
}

function a(n) {
    var r, t, e = "";
    for (t = 0; t < n.length; t += 1)
        r = n.charCodeAt(t),
            e += "0123456789abcdef".charAt(r >>> 4 & 15) + "0123456789abcdef".charAt(15 & r);
    return e
}

function h(n) {
    return unescape(encodeURIComponent(n))
}

function g(n) {
    return function (n) {
        return f(c(i(n), 8 * n.length))
    }(h(n))
}

function l(n, r) {
    return function (n, r) {
        var t, e, o = i(n), u = [], a = [];
        for (u[15] = a[15] = void 0,
             o.length > 16 && (o = c(o, 8 * n.length)),
                 t = 0; t < 16; t += 1)
            u[t] = 909522486 ^ o[t],
                a[t] = 1549556828 ^ o[t];
        return e = c(u.concat(i(r)), 512 + 8 * r.length),
            f(c(a.concat(e), 640))
    }(h(n), h(r))
}

function get_b(n, r, t) {
    return r ? t ? l(r, n) : a(l(r, n)) : t ? g(n) : a(g(n))
}


b = get_b("zzu" + "_" + m + "_" + td + "_1b6d2514354bc407afdd935f45521a8c")

function get_result() {
    result = {
        "X-Sc-Ah": b,
        "X-Sc-Alias": "zzu",
        "X-Sc-Nd": m,
        "X-Sc-Od": "YOUR_USER_TOKEN",
        "X-Sc-Td": td
    }
    return result
}
```

---

# Openai-API对接

## 推荐店铺

这里我并不推荐你们用自己的Openai账号（账号自带5刀的额度，但只能使用3.5模型）

而推荐你们购买**[V3小店的转发api](https://api.v3.cm/register?aff=hU0W)**（并非宣传，不过用的雀氏是我的邀请链接）理由如下：

1. **V3小店的账号是满速账号**。一分钟单IP可以请求几百次，但是你自己的号一分钟只能请求3次，而且速度没有他的快
2. **优惠、便宜**。V3小店12.5RMB可以得到5刀的额度，并且没有倍率套路，**算下来每一元可以生成6300-8800个GTP-4的Tokens**

3. **可以调用所有模型**。你自己的账号只能调用3.5模型。不过4是真的贵！

当然，如果你只想体验一下，完全没必要，用账号里的5刀额度就行！

## python对接GPT（以转发API为例）

### 环境搭建

首先要安装python的openai库，在cmd中输入如下指令

这里我使用了清华源，这样就可以不用科学上网，也能获得较好的下载速度

`pip install openai -i https://pypi.tuna.tsinghua.edu.cn/simple`

### 示例代码

这是最新版本的openai库的写法，需要看官方文档

注意，网上一般都是`openai==0.28`这个版本的调用。

记得替换`YOUR_API_KEY`

```python
from openai import OpenAI

# 构建client 并且绑定api_key和base_url
client = OpenAI(api_key="YOUR_API_KEY",
                base_url="https://api.v3.cm/v1")


def ask(question):
    """
    使用 OpenAI GPT-3.5 Turbo 模型模拟齐天大圣的角色回答问题。
    这个函数发送一个请求到 OpenAI 的 GPT-3.5 Turbo 模型，并设置场景为“齐天大圣用文言文回答问题”。该函数接收一个问题（以文言文的形式），并返回模型的回答。
    参数:
        question (str): 用户以文言文提出的问题。
    返回:
        str: 如果请求成功，返回模型生成的回答；如果出现异常，返回 False。
    异常处理:
        如果在请求过程中发生任何异常（如网络问题、API错误等），函数将捕获异常并返回 False。
    """
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "你现在需要扮演齐天大圣，用文言文跟我交流。"},
            {"role": "user", "content": question}
        ]
    )
    return completion.choices[0].message.content


```

---

# 爬虫代码

## 环境搭建

需要用python调用js代码，所以需要安装PyExecJS库

`pip install PyExecJS -i https://pypi.tuna.tsinghua.edu.cn/simple`

由于需要使用requests发送请求

`pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple`

## 代码示例

```python
import requests
import time
import execjs

# 定义API的URL地址
urls = {
    "list": "https://api.x.zanao.com/thread/v2/list",  # 获取列表的API地址
    "comment": "https://c.zanao.com/sc-api/comment/post",  # 发送评论的API地址
}

# 存储用户认证信息的cookies
cookies = {
    'user_token': "YOUR_USER_TOKEN"
}

# 从本地文件读取JavaScript代码
with open("zanao.js", "r", encoding="utf-8") as f:
    js = f.read()

def get_JS_result():
    """
    执行JavaScript代码并获取结果。

    使用execjs库编译并执行在 'zanao.js' 文件中的JavaScript代码，
    并调用 'get_result' 函数获取结果。

    返回:
        dict: 包含多个由JavaScript代码生成的键值对。
    """
    result = execjs.compile(js).call("get_result")
    return result

def get_headers():
    """
    生成并返回请求头。

    使用JavaScript函数生成特定的请求头参数。

    返回:
        dict: 包含HTTP请求所需的头部信息。
    """
    result = get_JS_result()
    headers = {
        'Accept': 'application/json, text/plain, */*',
        "X-Sc-Nd": result["X-Sc-Nd"],
        "X-Sc-Od": result["X-Sc-Od"],
        "X-Sc-Ah": result["X-Sc-Ah"],
        "X-Sc-Td": str(result["X-Sc-Td"]),
        'X-Sc-Alias': result["X-Sc-Alias"],
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090819) XWEB/8519 Flue'
    }
    return headers

def get_params(timestamp):
    """
    根据提供的时间戳生成并返回请求参数。

    参数:
        timestamp (int): 时间戳。

    返回:
        dict: 包含HTTP请求所需的参数。
    """
    params = {
        "from_time": str(timestamp),
        "hot": "1"
    }
    return params

def get_hot_list():
    """
    获取热门列表。

    通过发送HTTP POST请求到API端点，并处理响应数据，
    以获取热门话题列表。

    返回:
        list: 包含热门话题的列表，每个话题是一个字典。
    """
    url = urls["list"]
    headers = get_headers()
    params = get_params(round(time.time()))
    responses = requests.post(url, headers=headers, params=params)
    list = responses.json()["data"]["list"]
    result = []
    for i in list:
        tmp = {
            "id": i["thread_id"],
            "title": i["title"],
            "content": i["content"],
            'finish_status': i['finish_status'],
            "nickname": i["nickname"]
        }
        result.append(tmp)
    return result

def post_comment(id, comment):
    """
    向指定ID的帖子发表评论。

    参数:
        id: 帖子ID。
        comment: 要发布的评论内容。

    返回:
        response: 服务器的响应对象。
    """
    url = urls["comment"]
    headers = get_headers()
    data = {
        "id": id,
        "content": comment,
        "reply_comment_id": "0",
        "root_comment_id": "0",
        "cert_show": "0",
        "isIOS": "false"
    }
    response = requests.post(url, headers=headers, data=data,cookies=cookies)
    return response

```

# Logger日志类

我直接使用GPT-4生成一个Logger类/滑稽

```python
import logging
import datetime

class Logger:
    def __init__(self, file_name):
        # 创建一个日志记录器
        self.logger = logging.getLogger(name=file_name)
        self.logger.setLevel(logging.INFO)

        # 设置日志输出格式
        formatter = logging.Formatter('[%(asctime)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        # 创建一个文件处理器，用于写入日志文件，指定UTF-8编码
        file_handler = logging.FileHandler(file_name, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # 创建一个控制台处理器，用于输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log(self, message):
        # 记录日志信息
        self.logger.info(message)

```

# 主逻辑代码

## 代码示例

```python
import json, time, os
import Logger
import ZanaoSpider
import ZanaoRobot

DATA_PATH = "data/Data.json"  # 定义数据文件的路径

def load_data(file_name):
    """
    从指定的文件名加载数据。
    
    参数:
        file_name (str): 数据文件的名称。
    
    返回:
        list: 从文件中加载的数据列表。
    """
    if os.path.exists(file_name):
        with open(file_name.format(file_name), "r", encoding="utf-8") as f:
            data = json.loads(f.read())
    else:
        data = []
    return data

def dump_data(file_name, data):
    """
    将数据保存到指定的文件中。
    
    参数:
        file_name (str): 数据文件的名称。
        data (list): 要保存的数据。
    """
    with open(file_name.format(file_name), "w", encoding="utf-8") as f:
        f.write(json.dumps(data))

def get_uncommented_post(data):
    """
    获取未评论的帖子列表。
    
    参数:
        data (list): 已处理帖子的ID列表。
    
    返回:
        list: 未评论的帖子列表。
    """
    result = []
    hot_list = ZanaoSpider.get_hot_list()  # 获取热门帖子列表
    for hot in hot_list:
        if not (hot["id"] in data or hot['finish_status'] != "10"):
            result.append(hot)
        else:
            data.append(hot["id"])
    dump_data(DATA_PATH, data)  # 更新数据文件
    return result

logger = Logger.Logger("log/log.txt")  # 初始化日志记录器

while True:
    try:
        data = load_data(DATA_PATH)  # 加载数据

        posts = get_uncommented_post(data)  # 获取未评论的帖子

        data = load_data(DATA_PATH)  # 重新加载数据

        for hot in posts:
            # 构造查询问题
            question = ("发帖人网名；{{{}}} 帖子标题：{{{}}} 帖子内容：{{{}}}".format(
                hot["nickname"],hot["title"],hot["content"])).replace("\r\n", " ")

            msg = ZanaoRobot.ask(question)  # 获取自动回复的内容
            comment_response = ZanaoSpider.post_comment(hot["id"], "{}".format(msg)) # 发送回复
            data.append(hot["id"])  # 更新已处理的帖子ID
            # 记录日志
            logger.log("帖子ID:{} 帖子标题:{} 帖子内容:{} 回复内容:{}".format(hot["id"], hot["title"],
                                                                              hot["content"], msg)
                       .replace("\r\n", ""))
            time.sleep(10)  # 等待10秒
        dump_data(DATA_PATH, data)  # 保存数据
        time.sleep(3600)  # 等待1小时
    except Exception as e:
        logger.log("发生错误...{}".format(e))  # 记录错误信息
        dump_data(DATA_PATH, data)  # 保存数据
        exit(-1)  # 发生异常时退出程序

```

## 效果截图

![](https://cdn.jsdelivr.net/gh/zidou-kiyn/Blog-Pic/ZanaoRobot/20240105015740.png)
