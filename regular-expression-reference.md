# 正则表达式参考

蒋小超  
2007-07-23  

编辑校对：胡昂  
2015-07-05

## 一、介绍

追根溯源，正则表达式是在 1956 年的时候，人类最早研究神经网络的产物，但随着时间的流逝，几乎所有编程语言都加入了对它的支持，hoho～其实这个东西也是程序员开发中比较有名的一个难点。但是不要以为它只能用于程序开发，在 Unix/Linux 系统管理中它也有极为广泛的应用。

不要认为正则表达式很可怕，用直白的话来说，正则表达式就是利用 26 个英文字符与一些特殊符号的配合来进行文字内容比对的方法，绝大部分情况下，26 个英文字符都代表它们本身，但在特殊符号的辅助下，这些英文字符也会有其他的含义，正则表达式比较困难的地方，也就在这种字符的 2 义性上面，这篇文档中对于这种具有字符 2 义性的地方，都会有专门的标注和说明。

如果用过 Dos/Windows/Linux 中的通配符，就可以理解正则表达式的作用了，通配符用 `*` 号匹配任意多的任意字符，用 `?` 号匹配任意的一个字符，正则表达式有更加复杂的一套匹配系统，可以用来匹配几乎所有希望匹配的文字内容。

## 二、文档约定

**本文档中的所有实例，都是在以下环境中调试和运行的：**

操作系统：　　CentOS4.1（Linux 2.6.9-11）
编程语言：　　TCL8.4
文本编辑器：　VIM6.3.46

**文档格式约定：**

<忽略>

注释：原文是一份 WORD 文档。

## 三、基本正则表达式

正则表达式中，26 个英文字符代表它们本身，但是下面表格中的特殊字符则赋予了更多不同的含义，一定要记住它们，因为它们是一切正则表达式的基础。

特殊字符 | 简要说明
---------|---------
`.` | 一个点，匹配任意一个字符
`*` | 星号，匹配前面模式中的零个或者任意个
`+` | 加号，匹配前面模式中的一个或者任意个
`?` | 问号，匹配前面模式中的零个或者一个
`()` | 括号，创建一个子模式
`｜` | 竖号，交替匹配
`[]` | 中括号，用来表示一个区间
`^` | 尖号，将一个模式挂靠在要匹配的字符串的最前面
`$` | 美元号，将一个模式挂靠在要匹配的字符串的最后面

别看基本正则表达式就是这么 9 个符号，但是想完全理解和用好它们，还是很困难的，为了加深理解，我来详细的说明一下，这也是我自己学习时的理解和心得，请仔细的阅读。

这些符号的作用需要多方位理解，我大概是根据符号所属的类型以及它们所起的作用这 2 个方向来理解它们的。

按照类型划分，上面表格中的特殊字符分为几个类型：

#### 1. 字符关键字

这部分关键字包括 26 个英文字符（上面的表格没有列出来）。这些关键字的特点就是它们匹配自身。

#### 2. 数量关键字

这部分关键字包括  `.`（点）、`*`（星号）、`+`（加号）、`?`（问号）这4个关键字，这中间 `.`（点）这个关键字稍微特殊一点，因为它有 2 个作用：既可以作为字符关键字表示任何字符，又可以作为数量关键字代表 1 个字符。

**【任何字符】**这个含义很深，因为——空字符也算任何字符，也就是说一个点可以表示有一个字符，也可以表示没有字符，这个概念是新手很容易犯错的地方。

数量关键字本身没有任何用处，它必须和【模式】这个概念一起共同作用，在正则表达式中，【模式】可以说是最为核心也最为广泛的内容。总体来说，模式就是用来表示自己想匹配字符的方法，但实际上模式的概念要更为复杂和广泛，这部分内容我会在后面有更详细的描述，就现在来说，你只要理解，数量关键字必须与模式一起共用就可以了。

#### 3. 模式关键字

`()`（括号）、`|`（竖号）、`[]`（中括号）、`^`（尖号）、`$`（美元号）这 5 个符号都属于模式关键字，它们要么代表模式本身（括号、竖号、中括号），要么作用于模式为模式提供其他更高级的功能（尖号、美元号）。

现在，我们从另一个角度来看这些关键字，下面的内容，详细说明这9个关键字所起的作用以及实际表达方法，这部分会有一些比较详细的说明和实例，但是在此之前，我们必须了解一下什么是模式：

**a) 什么是模式？**

模式就是一组用来匹配字符的关键字集合，一个最小的模式只有一个关键字，而大的模式则可以有无数个关键字：

`A` 这是一个模式，代表 `A` 这个字符本身
`A+` 这也是一个模式，代表一个或者任意多个 `A` 字符

正则表达式中，数量关键字都是作用于左边模式的，上面的例子中，`A` 是一个没有数量关键字的模式，而 `A+` 中的 `+` 号就向左作用于前面这个 `A` 模式，如果没有 `A` 这个模式，`+` 号本身是没有任何意义的，这里 `A` 虽然是一个字符，但是我觉得把 `A` 称为模式能更清楚的理解模式的含义。

正则表达式的核心就是对模式的掌握和操作，理解了模式就等于拿到了开启大门的钥匙。
这里我介绍一个 TCL 语言中的命令：`regexp`，这个命令的作用就是利用正则表达式来获取想要的字符，它的使用方法如下：

```tcl
regexp  [选项]  <正则表达式>  <匹配的原始字符串>  <保存匹配后字符串的变量>  [其他保存子模式匹配字符串的变量]
```

上面 regexp 中用 `[]` 括起来的部分是可选的，其他 `<>` 括起来的部分是必须的，如果正则表达式匹配从原始字符串中匹配到了内容，则命令返回1并且将匹配到的内容<保存匹配后字符串的变量>中。下面我们来看1个简单的例子：

```tcl
regexp  {A+}  "AABBCC"  match
puts  $match
```

输出：

```
AA
```

上面的 `puts` 命令用来打印 `match` 变量中的内容，`A+` 这个模式从 `AABBCC` 这个原始字符串中匹配到了 `AA` 这 2 个字符，并将它置于 `match` 这个变量中，这就是一个最基本的正则表达式使用过程。

正因为模式如此重要，下面的内容就要详细说明几个模式关键字的作用了：

**b) `()` 子模式匹配关键字**

小括号用来将一个大模式分为几段更小的模式，这样就可以更加精细的控制匹配方式了，我们来看一个例子：

```tcl
regexp -- {(AA)(BB)(CC)} "AABBCC" match sub1 sub2 sub3
puts "The match is:$match"
puts "The sub1 is:$sub1"
puts "The sub2 is:$sub2"
puts "The sub3 is:$sub3"
```

输出：

```
The match is:AABBCC
The sub1 is:AA
The sub2 is:BB
The sub3 is:CC
```

上面的例子中，处于 `{}` 之间的内容是一个完整的正则表达式，在正则表达式里面我们用 `()` 将表达式分为 3 个子模式，后面的 `match` 变量中保存所有已经匹配到的字符，而几个 `sub?` 变量则保存相应子模式中匹配到的字符。

**c) `|` 交替匹配关键字**

交替匹配用来匹配|符号二边的一个模式，比如下面的例子：

```tcl
TOPSEC|topsec
```

上面的表达式表示匹配要么是全部大写的 TOPSEC，要么是全部小写的 topsec，不能 2 个都同时匹配。

**d) `[]` 区间匹配**

区间匹配用来表示匹配一系列字符串中间的一个，比如下面的例子：

```tcl
regexp {[ADEFG]} "AAABBBCCC" match
puts $match
```

输出：

```
A
```

上面的表达式表示匹配ABCDE这5个字符中的一个，注意：只是一个
如果想匹配多个呢？可以使用数量关键字辅助：

```tcl
regexp {[ADEFG]+} "AAABBBCCC" match
puts $match
```

输出：

```
AAA
```

区间匹配还可以使用[a-z]这样的语法来表示匹配从小写a到小写z这26个小写字母中的一个
这个关键字使用必须非常小心，因为在 TCL 语言中 `[]` 还有另外一个含义：所有处于 `[]` 中的内容是一条 TCL 命令，因此在 `regexp` 中使用的时候，必须用 `{}` 将 `[]` 的其他含义取消掉，如果将 `{}` 换成 `""`，那么上面的命令会报错。

**e) `^` 挂靠匹配，将模式挂靠在字符串的开头**

这是一个很特殊的关键字，它不像其他关键字是作用于左边的模式上，而是作用于右边的模式上，千万注意这一点！它表示从要匹配的字符串的最前面开始匹配，我们来看一个比较的例子：

```tcl
regexp  {(AAA)}  "BBBAAACCC"  match
```

可以匹配到，match中的值是AAA，但是我们加上挂靠匹配字符之后呢：

```tcl
regexp  {^(AAA)}  "BBBAAACCC"  match
```

无法匹配，`match` 中的值为空，因为^符号要求必须从要匹配的字符最前面开始匹配，可惜要匹配的字符最前面是 `BBB`，所以无法匹配到。

`^` 这个字符也有2义性，如果把它放在中括号里面的话，它表示【非】的意思，比如 `[^a-z]` 表示匹配不是 `a-z` 字母的其他字符，但是不在中括号里面，比如 `^ab` 表示必须最前面是 `ab` 这 2 个字符，这是很容易搞混的地方，一定要注意了。

**f) `$` 挂靠匹配，将模式挂靠在字符串的结尾**

这个关键字与^关键字作用相反，但是它和其他关键字一样，是作用于左边的模式上，还是看看例子：

```tcl
regexp  {(AAA)$}  "BBBCCCAAA"  match
```

可以匹配到，因为要匹配的字符最后面是 `AAA`，如果要匹配的字符是 `BBBAAACCC` 这样的，就无法匹配到了。

#### 4. 数量关键字

`.`（点） 、`*`（星号）、`+`（加号）、`?`（问号）用来表示数量。

**a) `.` 匹配任意一个字符**

.（点）是一个比较特殊的字符，它虽然表示匹配任意一个字符，但实际上任意字符也包括空字符。

**b) `*` 匹配前面模式中的零个或任意多个**

零个这个概念很重要，也就是说不管有没有都会匹配，所以一般我们都会用.*这样的方式来表示任意多个任意字符，不管有没有都可以。

**c) `+` 匹配前面模式中的1个或任意多个**

**d) `?` 匹配前面模式中的0个或1个**

`?` 号还有一个术语——非贪婪模式，这也是正则表达式中非常重要的内容，所谓非贪婪模式，就是表示只要匹配到第一个就会停下来，而贪婪模式正好相反，它会尽可能多的匹配，这2种模式的最终结果就是：非贪婪模式总是获得第一个匹配，贪婪模式总是获得最后一个匹配。默认情况下，正则表达式总是处于贪婪模式下的。

#### 5. 转义字符：反斜杠

基本正则表达式中还有一个很重要的符号：\（反斜杠），它用来关闭上面这些特殊字符的特殊含义，比如：

- `\*` 表示一个星号本身
- `\+` 表示一个加号本身
- `\\` 表示一个反斜杠 `\`（o(∩_∩)o...哈哈，自己关闭了自己）

在高级正则表达式中，反斜杠还有更多的用途。

## 四、高级正则表达式

高级正则表达式是基本正则表达式的扩展，总体来说，高级表达式扩展了以下 3 个方面的功能：

#### 1. 反斜杠字符序列

个人认为反斜杠字符序列应该是高级正则表达式最为实用的扩展了，利用反斜杠加上特定字符，可以表示复杂的含义，下面的表格就是根据我的经验使用最多的反斜杠序列，我会根据使用频率从上到下的安排顺序。

反斜杠序列 | 简要说明
---------|---------
`\d` | 表示 0-9 之间的数字
`\D` | 除了 0-9 之间数字的其他字符，与 `\d` 作用相反
`\s` | 空白符，包括空格、换行、回车、制表、垂直制表、换页符等
`\S` | 非空白符，与 `\s` 作用相反
`\w` | 数字、字母和下划线
`\W` | 非数字、字母和下划线的其他字符
`\uXXXX` | 16 位 Unicode 字符编码
`\n` | 换行符，Unicode 码是 `\u000A`
`\r` | 换页符，Unicode 码是 `\u000D`
`\t` | 制表符，Unicode 码是 `\u0009`

#### 2. 字符类

除了反斜杠字符序列，高级正则表达式还支持字符类匹配，字符类就是利用一个单词代表复杂意思，大部分的字符类与反斜杠序列含义相同，但也有一些字符类是特有的，比如匹配 16 进制字符的 `xdigit`，几乎所有情况下只要使用字符类就必须将它们放在 `[[: :]]` 符号中，下面的表格列出了所有字符类：

字符类 | 简要说明
---------|---------
`[[:alnum:]]` | 大小写字母和数字，不包括下划线
`[[:alpha:]]` | 大小写字母
`[[:blank:]]` | 空格和制表符
`[[:cntrl:]]` | 控制字符，也就是 ASCII 码表中 1-31 号的字符
`[[:digit:]]` | 0-9 之间的数字，与 `\d` 的含义相同
`[[:graph:]]` | 所有可以显示的字符
`[[:lower:]]` | 小写字母
`[[:print:]]` | alnum 的另外一种表示方法
`[[:punct:]]` | 所有标点字符
`[[:space:]]` | 空白字符，与 `\s` 的含义相同
`[[:upper:]]` | 所有大写字母
`[[:xdigit:]]` | 所有 16 进制数字，包括 0-9、a-f、A-F

#### 3. 扩展的正则表达式语法

扩展语法中，我认为最为重要和方便的就是 `{}` 语法，它可以精确指定前面模式匹配的次数，`{}` 语法有 3 种基本使用方法：

- `{m}` 匹配前面模式的 m 次
- `{m,}` 匹配前面模式最少 m 次，最多无限次
- `{m,n}` 匹配前面模式最少 m 次，最多 n 次

在实际使用时还可以在 `{}` 语法后面加上 `?` 号表示非贪婪匹配。

## 五、实例详细说明

下面的实例都是可以单独运行的代码段，有兴趣的话可以自己将它们复制到文件中运行，观察一下它们的结果，然后修改表达式中的字段观察它们的不同表现，这是学习正则表达式的捷径。

#### 1. 从 tcpdump 中，提取 IP 和端口号。

```tcl
set dumpoutput {
16:49:52.278091 IP 10.11.105.15.2093 > 10.11.105.102.ssh: . ack 167128 win 14944
16:49:52.292780 IP 10.11.105.15.2093 > 10.11.105.102.ssh: . ack 167332 win 16232}

set pattern {.*(10.11.105.15)\.+?(\d+)\s+?>+?}
set status [regexp $pattern $dumpoutput tp iptp port]
puts "ip is:$iptp"
puts "port is: $port"
```

输出：

```
ip is:10.11.105.15
port is: 2093
```

上面的代码中，dumpoutput 变量是从 tcpdump 程序中截获的报文，最重要的正则表达式是 pattern 变量中的内容，观察一个正则表达式，应该首先观察它的子模式，从子模式中一般我们可以看到正则表达式中最重要最核心的部分，然后再观察外围的其他字符。

上面的代码中有 2 个子模式，第一个子模式用来匹配 IP 地址，第二个子模式则使用高级正则表达式中的反斜杠字符序列，`\d` 表示任意数值，后面的 `+?` 则用来匹配任意多个数值。

外围的代码中，大量使用了 `?` 的非贪婪特性，其中 `\s` 这个反斜杠序列表示任意空白符号。

#### 2. 从tcpdump中，提取arp应答信息

```tcl
set dumpout {17:14:24.927839 arp who-has 10.11.105.254 tell 10.11.105.102
17:14:24.927936 arp reply 10.11.105.254 is-at 00:13:72:35:a6:fd}

set pattern {arp reply 10.11.105.254}
set st [regexp -- $pattern $dumpout match]
puts $match
```

这个正则表达式很简单，就是让关键字一个一个的对应匹配，其实刚刚开始写正则表达式有一个小技巧——首先将关键字全部复制出来，然后一点一点的替换，比如将空格替换成 `\s+`，数值替换成 `\d+` 等等。

#### 3. 检查 arp 表中是否清空了指定 IP 的 arp 记录

```tcl
set pcarp {
Address                  HWtype  HWaddress           Flags Mask            Iface
10.11.105.29                     (incomplete)                              eth0
10.11.105.19             ether   00:11:D8:35:13:84   C                     eth0}

set pattern {(10.11.105.29)+?.*?incomplete+?}
set patt "\u000A*\u000D*"
regsub -all -- $patt $pcarp {} pcarp
set st [regexp -- $pattern $pcarp match]
puts $match
```

输出：

```
10.11.105.29                     (incomplete
```

上面的表达式使用了 `?` 这个非贪婪匹配关键字

#### 4. 从 FW 上获取系统当前时间

```tcl
set fwout {+00 2007-07-24 08:25:38}

set pat {.*(\+[0-9]{2})\s+([0-9]{4}-[0-9]{2}-[0-9]{2})\s+([0-9]{2}:[0-9]{2}:[0-9]{2}).*}
set st [regexp $pat $fwout - t1 t2 t3]
puts "time area:$t1\ndate:$t2\ntime:$t3"

set pat {([0-9]{2}):([0-9]{2}):([0-9]{2})}
regexp $pat $t3 - hour minute second
puts "hour:$hour\nminute:$minute\nsecond:$second"

set pat {([0-9]{4})-([0-9]{2})-([0-9]{2})}
regexp $pat $t2 - year month date
puts "year:$year\nmonth:$month\ndate:$date"
```

这个表达式使用了高级正则表达式中的概念，在模式后面用{}括起来的数字表示匹配前面的模式多少次，利用子模式可以单独提取内容。

下面的实例除非必要就不再解释，请仔细观察。

#### 5. 从 `ifconfig` 端口号中，获得 IP 地址。

```tcl
set result [exec ifconfig eth1]
set pat {(inet addr:)([^\s]+)\s+(Bcast:.*)}
regexp $pat $result - - ip
puts "ip is :$ip"
```

`regexp` 命令中的 `-` 表示不获取那个子模式中的值，因为这里使用了 2 个 `-`，因此 `ip` 变量获取的就是第 2 个子模式的值了（第一个 `-` 获取整个表达式匹配的所有字符，第二个 `-` 获取第一个子模式中的值。

## 六、后记

正则表达式使用极为灵活，特别是字符2义性的问题新手很容易出错，唯一的办法就是多使用、多练习，在错误中慢慢领会语法的含义。虽然我在写这篇文档时想尽量加入自己的经验和理解，但实际上很多东西都是只能意会的，如果非要说清楚的话，不光语言会冗长无味，而且更容易把读者带入不知所措的境地，所以这里我尽量将平时使用最为频繁的功能以及最容易犯错的地方指出来，其他的就要靠读者自己试验了～
