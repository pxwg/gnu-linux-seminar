# 燎原沙龙：从论文撰写看 Linux 与 GNU 工具的应用

> 写在前面 (Disclaimer)
- 我们不会讲解 Linux 的安装与配置，也不会讲解 GNU 工具的使用细节。在 AI 时代高速发展的今天，这些内容已经有大量的资源可以学习，直接问 AI 就能得到答案。
- 我们将聚焦于“如何以物理系学生的视角，利用 Linux 与 GNU 工具解决实际问题”，并以“论文写作”为例进行讲解。
- 重点不在于“学会使用某个工具”，而在于“知道怎样的解决方案是好的”。这样，在鱼龙混杂的开源世界中，你才能找到适合自己的工具与方法。

> 计算机第零定律：计算机被设计以解决问题
> 计算机第一定律：计算机不会解决问题

> 事实：计算机只能读取输入并给出输出 (I/O)

> 总结：以计算机解决问题 = 抽象，直至一系列 I/O

## About Me

```
name: Xinyu Xiang (向昕宇)
department: Department of Physics
website: https://homeward-sky.top/
```

```
     .--.          ,= ,-_-. =.
    |o_o |        ((_/)o o(\_))
    |:_/ |         `-'(. .)`-'
   //   \ \            \_/
  (|     | )
 /'\_   _/`\
 \___)=(___/
  Linux (Tux)     GNU (GNU Head)
```

## Idea

**Linux and GNU and Open Source is a VERY HUGE topic!**

We HAVE to break it down into smaller pieces.

*IDEA* (it is not a name of an IDE) is:
- Focusing on one topic
- From this topic, we can extend to other

Before we start, let me introduce two main topics here:

### GNU

GNU 是一个递归缩写，代表“GNU 不是 Unix”（GNU's Not Unix），即

```
GNU(0) = GNU
GNU(n) = (GNU(n-1) is Not Unix)
```

#### 命令行工具调用

在 GNU 系统中，我们通常通过命令行界面（CLI）与系统进行交互。
我们一般会通过终端（Terminal）或者终端模拟器（Terminal Emulator）来输入命令。
命令行工具通常遵循以下基本结构：
```bash
command [options] [arguments]
```
中间用空格相连接

例如，`echo` 命令用于在终端输出文本：
```bash
echo "Hello, World!"
```
输出
```txt
Hello, World!
```

更重要的，对于例如 `Ubuntu` 这样的发行版，我们通常会使用包管理器（Package Manager）来安装、更新和管理软件包。
例如，使用 `apt` 包管理器安装 `curl` 工具：
```bash
sudo apt update
sudo apt install curl
```
其中，`sudo` 用于以超级用户权限执行命令，`apt update` 用于更新软件包列表，`apt install curl` 用于安装 `curl` 工具。

如果你想要获得对于某个`command`的帮助信息，可以使用 `--help` 选项：
```bash
command --help
```
或者使用 `man` 命令查看手册
```bash
man command
```
例如，查看 `ls` 命令的帮助信息：
```bash
ls --help
```
或者
```bash
man ls
```

### Linux

Linux is a Kernel written in C.

- Linux Kernel + GNU Tools = CompleteOS
- CompleteOS + Distro Info (like package manager, name) = Linux Distro
- Linux Distro + Desktop Environment (I will not mention) = Linux System

## Spark

*Idea*: ALL big things would be constructed with (and decomposed to) some *proper* abstracts.

作为物理系学生，我们通常不以“构建新的计算机、系统、软件”为生。而是以计算机解决我们生活中的 *problems* 为主要目的。

### Problem Solving with Computers

- 解决问题：目标 => IO + 步骤 + 需求
- 计算机处理：单一工具应用 + 多个工具组合
- 优化：更为贴近需求 + 一次编码，多次复用

> Single Point of Truth, Don't Repeat Yourself

> 为每个子任务选择合适的工具

因此，我们的 `SOC` 应该是：

1. 将`目标`拆分为一系列 `IO` (输入输出) 步骤
2. 将问题的 `IO` 链接到不同的计算机`工具`
3. 根据`步骤`，将不同的工具`组合`起来

> Unix Philosophy 1: "Do One Thing and Do It Well"

这对应 IO 拆分与工具选择——基于 Unix 哲学，每个 IO 都应该对应一个单一功能的工具。

> Unix Philosophy 2: "Write Programs to Work Together"

这对应工具组合。上一个工具的输出作为下一个工具的输入：
- 管道 (Pipes)
- 套接字 (Sockets)
- 文件 (Files)
- etc.
等方式以**纯文本**形式连接起来，完成复杂任务。

#### Example

任务：将文本文件中的所有小写字母转换为大写，并输出到另一个文件中。

##### 问题拆分：

- 定位：到达 `input.txt` 文件所处的目录
- 输入：文本文件 `input.txt`
- 查找小写字母
- 转换为大写
- 输出：结果文件 `output.txt`

##### 工具选择：

- 到达目录：`cd /path/to/directory`
- 读取文件内容：`cat input.txt`
- 转换大小写：`tr 'a-z' 'A-Z'`
- 输出到文件：`> output.txt`

##### 目标实现：

工具链需要读取 `input.txt`，然后通过管道将输出传递给下一个工具，直到最终输出到 `output.txt`。

假设 `input.txt` 内容如下：
```
Hello World
```
首先，我们需要读取文件内容：
```bash
cat input.txt
```
这将会输出标准输出 (stdout)。
```bash
> Hello World
```

我们需要把这个标准输出“灌进”下一个工具 `tr`，将小写字母转换为大写。这就需要用到“管道”技术，将前一个工具的输出作为下一个工具的输入：
```bash
cat input.txt | tr 'a-z' 'A-Z'
```
其中，`|` 符号表示管道，将 `cat` 命令的输出传递给 `tr`。
这将会输出：
```txt
HELLO WORLD
```

最后，我们需要将这个输出重定向到 `output.txt` 文件中，总结便是：
```bash
cat input.txt | tr 'a-z' 'A-Z' > output.txt
```
最后执行
```bash
cat output.txt
```
将会看到 `output.txt` 文件内容为：
```txt
HELLO WORLD
```
这便完成了我们的任务。

> 当然，这个步骤可能并不是最佳，你可以用我们之前的哲学来优化它。

- 这个步骤不满足 `Single Point of Truth, Don't Repeat Yourself` 原则


## First Problem: Note-Taking and Paper Writing

我们懂了“输入->处理->输出”的逻辑，现在让我们解决物理系学生一个痛点——写论文。

- 目标：写一篇学术论文

第一步拆解是目标对应的输入与输出：

- 输入：使用电脑输入`文字`与`公式`
- 输出：生成`PDF`文件

### 从键盘到文件

首先，我们得要用键盘将文本写入到文件之中。这需要一个文本编辑器 (Text Editor)。
在 `GNU` 的世界中，人们常常使用 `Emacs` 进行文本编辑，当然，最“经典”的应该是`>`或者`>>`重定向符号将文本写入文件中，比如：
```bash
echo "This is a sample text." > paper.txt & cat paper.txt
```
或者使用 `sed` 进行文本处理：
```bash
sed -i '1i This is a sample text.' paper.txt & cat paper.txt
```
其中 `&` 用于将两个命令连接在一起，前一个命令执行完毕后，紧接着执行后一个命令。

输出全部都是：
```txt
This is a sample text.
```
意味着文本已经成功写入 `paper.txt` 文件中。

在 `Linux` 的世界中，人们还会使用 `Vi`、`Vim`、`Neovim`、`nano`、`helix` 等文本编辑器。
当然，你如果有了 GUI 环境，那么可用的就更多了！比如 `VSCode`、`Sublime Text`、`Atom` 等等。
但总而言之，你终究得要学会：将文本写入文件之中。而这些工具就是帮助你实现这个目标的。

> 比如我现在就在使用 `Neovim` 写并展示文档。

### 从文件到 PDF

接下来，人们需要将文本文件转换为 PDF 文件，这意味着我们需要
- 按照某种特定的格式来撰写文本文件
- 使用某种工具将文本文件转换为 PDF 文件
这种特定的格式被称为`标记语法`，而转换为 PDF 的工具则是对应的`编译器`。

目前主流的用于论文排版的标记型语言是 `LaTeX` 与 `Typst`。当然，前者更为流行，并且广泛地被学术界使用。

以 `LaTeX` 为例，在将工具安装在电脑的时候，我们需要安装
- 编译器本体
- 宏包 (Packages)
- 以及特定的字体
完成之后，我们可以在`CLI`中使用例如`pdflatex`的命令将 `.tex` 文件编译为 PDF 文件。
假设我们有一个名为 `paper.tex` 的 LaTeX 文件，内容如下：
```latex
\documentclass{article}
\begin{document}
Hello, World!
\end{document}
```
我们可以使用以下命令将其编译为 PDF 文件：
```bash
pdflatex paper.tex
```

### 小结：初步的论文写作流程

编辑器 + 标记语法 -> 保存文件
`编译器 保存文件.tex/typ` -> 生成 PDF 文件

> 问题

1. 标记语法通常存在输入的复杂性，例如 1/2 在 LaTeX 中：
```txt
\frac{1}{2}
```
Typst 从设计之初规避了上述问题，但迎来了新的问题：
若要输入`\bigoplus`，需要输入
```txt
plus.big
```
这谁能记得住？查询过程也严重影响了编辑的专注度

2. 编译过程需要：

打开一个新的终端窗口 -> `cd` 到文件目录 -> 输入编译命令 -> 等待编译完成 -> 预览 PDF 文件

非常麻烦，尤其是当报错的时候，你需要重新检查代码，修改，然后重新编译。
非常不“心流”

> 目标：优化论文写作流程，不再因为繁难的语法与编译过程分心

### 优化：单元与速度

为了解决这个问题，我们首先需要认识到当前问题的基本结构：
- 输入单元：
  - 计算机的输入是以“符号”为单元来输入的
  - 人类理解的输入是以“词语”为单元来输入的
  - 标记语法的输入是以“命令”为单元来输入的

输入：
```
keyboard: c -> ca -> cat
human: ? -> ? -> cat (with its meaning: 猫)
```

修改：
```
cta -> cat
human: cta -> cat (expected)
keyboard: cta -> ct -> c -> ca -> cat (reality)
```

语法：
```
keyboard: \ -> \f -> \fr -> \fra -> \frac
latex: ? -> ? -> ... -> \frac (with it's syntax: \frac{numerator}{denominator})
```

如你所见，无论是
- 编辑
- 编译
传统基于键盘的输入模式都并不是完全符合人类与计算机语言的底层逻辑的。

> 问题在于：我们需要更高效的输入与编辑单元，以词组/句/段/命令为单位进行输入与编辑。

这事实上已经存在一系列工具来实现这个目标。

目前主流的工具包括：
- LSP (Language Server Protocol)
- Tree-sitter
以及为了实现这些工具的最快捷部署与应用，我们将介绍
- Docker

同时，为了解决编译过程的繁琐，我们将介绍
- Makefile

#### 词组单位与命令单位编辑

##### 命令单位编辑：LSP

LSP 是一种协议，允许编辑器与语言服务器进行通信，以提供智能代码补全、错误检查、重构等功能。

基本逻辑：
```
┌──────────┐    ┌─────────────────┐    ┌─────────────────┐
│   File   │───▶│ Editor (Client) │───▶│ Language Server │
└──────────┘    └─────────────────┘    └─────────────────┘
                         ▲                       │
                         │      response         │
                         └───────────────────────┘
```
LSP 允许编辑器通过发送请求 (例如，请求代码补全) 给语言服务器，语言服务器处理请求并返回响应 (例如，提供补全建议)。

自动补全是 LSP 的一个重要功能，它事实上帮助我们
- 只输入简短的部分指令
- 获得以“单命令”为单位的补全建议

现在工作流程变为
```
   ┌──────────┐      ┌───────────────┐      ┌─────────────────┐      ┌────────┐
   │ Keyboard │─────▶│ Input: "\fr"  │──┬──▶│ Filter/Display  │─────▶│ Select │
   └──────────┘      └───────┬───────┘  │   │  [ \frac... ]   │      └────────┘
                             │          │   └────────▲────────┘
   Create Context            │          │            │
 ────────────────────────────┼──────────┼────────────┼──────────────────────────
   Async Data Loop           │          │            │
                             │          │            │
          (1) Send Request   │          │            │ (2) Return Items
      ┌──────────────────────▼─┐        │      ┌─────┴──────────────────┐
      │   CompletionRequest    │        │      │    Completion Items    │
      │   Payload: { "\fr" }   │        └──────┤ [\frac, \frame, ...]   │
      └───────────┬────────────┘               └───────────▲────────────┘
                  │                                        │
                  │                                        │
      ┌───────────▼────────────┐               ┌───────────┴────────────┐
      │    Language Client     │───────▶───────│    Language Server     │
      └────────────────────────┘    Network    └────────────────────────┘
                                      or
                                    IPC Pipe
```
在用户看来，他们只需要输入 `\fr`，LSP 就会提供 `\frac` 的补全建议，用户选择后即可完成输入。
这大大提高了输入效率，减少了记忆负担。

无论在`VSCode`、`Neovim`还是`Emacs`中，都有对应的 LSP 插件可以使用。这事实上也是 Unix 哲学的体现：
- 编辑器专注实现编辑功能
- 语言服务器专注实现语言智能功能
- 两者通过 LSP 协议协同工作

> 当然，LSP 存在属于自己的局限性，比如它的单位是以“命令”为单位的，对于代码结构性的理解并不友好。
 
##### 词组/结构单位编辑：Tree-sitter and Text Objects in Neovim

###### Text Objects

我想单独讲一讲 Vim/Neovim 中的 Text Objects 概念。

- 情况 1：词汇单位的编辑

考虑英文纠错
```txt
This is a SMiple text.
```
一般文本编辑器的修复策略是：
- 将光标移动到错误单词 `SMiple` 处 (鼠标或者键盘)
- 连续多次按 Backspace 删除错误单词
- 重新输入正确单词 `simple`
容易发现，按下 Backspace 多次并不符合 `Single Point of Truth, Don't Repeat Yourself` 原则。
原因在于：我们并没有以“单词”为单位进行编辑，而是以“字符”为单位进行编辑。

Vim 中分割了“普通模式”(Normal Mode) 与“插入模式”(Insert Mode)。在普通模式下，我们可以使用 `dw` 命令删除一个单词 (Delete Word)。
而单独按下`w`则是将光标移动到下一个单词的开头 (Word)。
这样，我们只需要
- 按下 `b` 移动到单词开头
- 按下 `cw` (Change Word) 删除单词并进入插入模式
- 输入正确单词 `simple`
```txt
This is a SMiple text.
```

- 情况 2：环绕元素的编辑

考虑 LaTeX 常见的公式输入
```latex
\somecommand{argument}
```
我们现在想要将 `argument` 修改为 `newarg`。

一般文本编辑器的修复策略是：
- 将光标移动到 `argument` 处 (鼠标或者键盘)
- 连续多次按 Backspace 删除 `argument` (注意不删除大括号)
- 重新输入 `newarg`
同理，按下 Backspace 多次并不符合 `Single Point of Truth, Don't Repeat Yourself` 原则。
并且，注意不删除大括号的操作也增加了复杂度和心智负担。

回忆人类理解我们编辑的方式，我们的认识仍然是：删除`被大括号环绕的内容`

Vim 中的解决方案是使用 Text Objects 的概念。
结构：word (w)，Word (W)，sentence (s)，paragraph (p)，括号包裹 (`(`、`[`、`{` 等)，引号包裹 (`"`、`'` 等) 等等。
位置：inside (i)，around (a)
此时，我们可以使用 `ci{` 命令 (Change Inside Curly Braces) 来删除大括号内的内容并进入插入模式。
修改过程变为：
- 按下 `ci{` 删除 `argument` 并进入插入模式
- 输入 `newarg`

- 情况 3：代码块的编辑

考虑在 Markdown 中编辑一个代码块
```markdown
```python
print("Hello, World!")
```
现在我希望将代码块的内容变为
```python
# This is a sample Python function
def greet():
    print("Hello, World!")
```
同理，传统的编辑方式是：
- 鼠标流
  - 将光标移动到代码块内
  - 选中代码块内容
  - 删除选中内容
  - 输入新的代码块内容
- 键盘流 (bro 我不觉得你会这样做)

其实鼠标流挺不错的。但是仍然存在手动选中内容的心智负担。

有没有像是 Text Objects 一样的概念呢？
比如，直接使用 `cic` (Change Inside Code Block) 来删除代码块内的内容并进入插入模式。

好吧，很遗憾，Vim 的这个实现强烈依赖于特定的“硬编码”的字符，对于代码块这种结构并不友好。

然而，从语法设计的角度来看，代码块是有明确边界的，将会在语法树 (AST) 中作为节点存在。
下面是一个代码块的语法树表示：
```
┌─────────────────────────────────────┐
│  节点：fenced_code_block_delimiter  │
│  (边界起点)                         │
│  内容：```                          │
└─────────────────────────────────────┘
          │
          V
┌────────────────────────────┐
│  节点：code_fence_content  │
│  (核心子树)                │ <-- 用户实际编辑的内容
│  内容：... (用户代码)      │
└────────────────────────────┘
          │
          V
┌─────────────────────────────────────┐
│  节点：fenced_code_block_delimiter  │
│  (边界终点)                         │
│  内容：```                          │
└─────────────────────────────────────┘
```
只要我们做替换：空格、括号边界 -> 节点边界，我们就可以实现对节点边界内的内容进行直接的编辑

这正是 Tree-sitter 的用武之地——它解析语法树，通过编辑器的兼容层与之交互，便可以实现对代码结构的理解与操作。

> 事实上，大部分语言的编译器本质上也是基于语法树进行解析的。但是，这又是Unix 哲学的魅力时刻：编译器专注于编译，并没有统一的语法树交互接口。而 Tree-sitter 则专注于语法树的解析与交互，提供了一个统一的接口供编辑器使用。

###### Tree-sitter

Tree-sitter 是一个用于增量解析代码的库，能够生成代码的抽象语法树 (AST)，并允许编辑器实时更新和查询这些树结构。
Neovim 有一个内置的 Tree-sitter 兼容层，可以通过安装相应的语言解析器来支持多种编程语言，实现
- 语法高亮
- 代码折叠
- 结构化选择与编辑
前两者比较常见，而后者则是我们刚刚提到的 Tree-sitter + Text Objects 概念的实现基础。
只要能够用通用的方式解析语法树，提取特定节点，我们就可以定义针对特定节点的 Text Objects，并绑定快捷键，从而实现对代码结构的高效编辑。

> 由于这次讲座不是Neovim 专题，我就不展开细讲 Tree-sitter 的安装与配置了。

### 部署工具：App Store in Linux

- App Store in MacOS: just click and install
- Package Manager in Linux: command line + GUI + 大量的 **dependencies** management

设想如下情况
```
          ┌──────────┐                  ┌──────────┐
          │   LSP A  │                  │   LSP B  │
          └────┬──┬──┘                  └───┬──┬───┘
               │  │                         │  │
      ┌────────┘  └───────┐         ┌───────┘  └────────┐
      │                   │         │                   │
      ▼                   ▼         ▼                   ▼
 ┌────────────┐    ┌────────────┐ ┌────────────┐    ┌────────────┐
 │   Lib C    │    │   Lib B    │ │   Lib B    │    │   Lib D    │
 │  (v2.0.1)  │    │  (v1.0.2)  │ │  (v2.0.3)  │    │  (v1.5.0)  │
 └────────────┘    └──────┬─────┘ └─────┬──────┘    └────────────┘
                          │             │
                          │             │
                          ▼             ▼
                   ┌───────────────────────────┐
                   │   !! CRITICAL ERROR !!    │
                   │    /usr/lib/libB.so       │
                   │    Target Collision!      │
                   └───────────────────────────┘
```
如果你同时安装 LSP A 与 LSP B，会导致库 B 的版本冲突，从而引发一系列问题。

> 语义化版本控制：x.y.z (Major.Minor.Patch)，大版本更新之间很可能存在不兼容的 Breaking Changes

又或者(更为直观的例子)，你在 2023 年用 TeXLive 2023 写了一篇论文，用到了某个特定的宏包。 到了 2026 年，你需要修改这篇论文。此时你的电脑上已经是 TeXLive 2026，很多宏包的 API 可能已经变了，编译直接报错。
```
Timeline A: 2017 (Past)                Timeline B: 2026 (Now)
        (Original Environment)              (Current Host System)
   ═══════════════════════════════     ═══════════════════════════════
   ┌─────────────────────────────┐     ┌─────────────────────────────┐
   │        TeXLive 2017         │     │        TeXLive 2026         │
   └──────────────┬──────────────┘     └──────────────┬──────────────┘
                  │                                   │
          ┌───────┴───────┐                   ┌───────┴───────┐
          ▼               ▼                   ▼               ▼
   ┌────────────┐   ┌────────────┐     ┌────────────┐   ┌────────────┐
   │   beamer   │   │    tikz    │     │   beamer   │   │    tikz    │
   │   v3.67    │   │   v3.1.8   │     │   v3.71    │   │  v3.1.10   │
   └──────┬─────┘   └────────────┘     └──────┬─────┘   └────────────┘
          │                                   │
          │                                   │   API Breaking Change
          │                                   │   (Removed \oldmacro)
          ▼                                   ▼
   ┌────────────┐                      ┌─────────────────────────────┐
   │  Success!  │                      │   !! COMPILATION ERROR !!   │
   │  paper.pdf │                      │    Undefined command:       │
   └────────────┘                      │    \oldmacroname            │
                                       └─────────────────────────────┘
```
但你应该不会尝试在同一台电脑上安装 TeXLive 2023 与 TeXLive 2026 来解决这个问题吧？

> 这个问题甚至存在于 Windows 与 MacOS 上

##### 问题：为什么 App Store 没有这个问题？

Answer：App Store 在打包应用程序时，会将所有的依赖打包在一起分发，这样就避免了版本冲突的问题。

> 这个操作不是特别符合 Unix 哲学，也不适合 Linux 的很多工作环境 (嵌入式系统等)，但对于桌面用户来说，是一个非常方便的解决方案。

#### Linux 下的解决方案：Docker

基本想法是：将应用程序与其所有依赖打包在一个独立的环境 (被称为`容器`) 中运行，从而避免版本冲突的问题。
```
   ┌─────────────────┐   ┌─────────────────┐
   │    Container A  │   │   Container B   │
   │ ┌─────────────┐ │   │ ┌─────────────┐ │
   │ │    App A    │ │   │ │    App B    │ │
   │ └─────────────┘ │   │ └─────────────┘ │
   │ ┌─────────────┐ │   │ ┌─────────────┐ │
   │ │ Lib B(v1.0) │ │   │ │ Lib B(v2.0) │ │ <── No Conflict!
   │ └─────────────┘ │   │ └─────────────┘ │
   │ ┌─────────────┐ │   │ ┌─────────────┐ │
   │ │ Guest OS FS │ │   │ │ Guest OS FS │ │
   │ └──────┬──────┘ │   │ └──────┬──────┘ │
   └────────┼────────┘   └────────┼────────┘
            │                     │
   ═════════▼═════════════════════▼═════════
          Shared Linux Kernel (Host)
   ═════════════════════════════════════════
```


或许部署 LSP 服务器比较复杂，我们来讲讲如何解决 TeXLive 版本冲突的问题。
此时，我们可以为每个 TeXLive 版本创建一个 Docker 容器：
```bash
docker run -v $(pwd):/workdir -w /workdir danteev/texlive:TL2017 pdflatex playground.tex
```
解释一下：
- `docker run`：运行一个新的容器
- `-v $(pwd):/workdir`：将当前目录挂载到容器内的 `/workdir` 目录
- `-w /workdir`：设置工作目录为 `/workdir`
- `danteev/texlive:TL2017`：使用 `danteev` 用户在 Docker Hub 上发布的 TeXLive 2017 镜像
- `pdflatex playground.tex`：在容器内运行 `pdflatex` 命令编译 `playground.tex` 文件

> 你也可以加入 `--rm` 选项，在容器运行结束后自动删除容器

> 查找合适的 Docker 镜像可以直接在 [Docker Hub](https://hub.docker.com/) 上搜索，或者自己打包
> docker 的核心思想与其说是“安装软件”，不如说是“交付环境”
> 因此，一个更像是“App Store”的 Linux 工具或许是`nix`，但它的学习曲线较陡峭，我也不会，所以这里就不展开讲解了。

##### 打包

Docker 的关键在于
- 模拟操作系统环境
- 在这个环境中运行应用程序
因此，如果我们希望分发一个包含特定版本 LSP 的容器，我们需要创建一个 Docker 镜像 (Image)。
其中，我们需要
- 基础镜像 (Base Image)：规定了容器的操作系统环境
- 安装步骤 (Installation Steps)：定义了如何安装 LSP 及其依赖

上述步骤可以通过编写一个 `Dockerfile` 来实现 (这个过程被成为“打包”)。例如，假设我们要创建一个包含特定版本 LSP 的容器，我们可以编写如下的 `Dockerfile`：

<!-- TODO: 样例 -->

### 优化：编译与整合

上述过程并不符合`Single Point of Truth, Don't Repeat Yourself` 原则。
你每次都要单独用比如说`docker run ... pdflatex`命令来编译文件，实在是太麻烦了。

#### 抽象

我们同样抽象出当前的工作流程：
对于标准的 LaTeX 项目文件：
```
project/
├── main.tex
├── sections/
│   ├── introduction.tex
│   ├── methods.tex
│   └── results.tex
├── figures/
│   ├── figure1.png
│   └── figure2.png
└── bibliography.bib
```
依赖关系显然为：
```
                         ┌──────────────┐
                         │   main.pdf   │
                         └──────┬───────┘
                                │ depends on
                         ┌──────▼────────┐
                         │   main.tex    │
                         └───┬───┬───┬───┘
                             │   │   │
              ┌──────────────┘   │   └──────────────┐
              │                  │                  │
    ┌─────────▼──────────┐  ┌────▼─────┐  ┌────────▼────────┐
    │ sections/          │  │ figures/ │  │ bibliography.bib│
    ├────────────────────┤  ├──────────┤  └─────────────────┘
    │ introduction.tex   │  │figure1   │
    │ methods.tex        │  │figure2   │
    │ results.tex        │  └──────────┘
    └────────────────────┘
```
我们注意到，编译产物对于各个文件的依赖关系是`树状`的。

这个依赖的树结构可以更为复杂！有时候我们会写实验报告，这个时候，整个文件的插图来源于
- 照片
- tikz 绘图
- 实验数据脚本绘制的图片
前两者还比较简单，但实验数据脚本绘制的图片就比较复杂了。

```
project/
├── main.tex
├── sections/
│   ├── introduction.tex
│   ├── methods.tex
│   └── results.tex
├── figures/
│   ├── figure1.png
│   └── figure2.png
├── scripts/
│   ├── data_analysis.py
│   └── plot_results.py
├── data/
│   ├── raw_data.csv
│   └── processed_data.csv
└── bibliography.bib
```

直接的处理逻辑还是很直接：
- 输入：实验数据文件
- 处理：`python scripts/data_analysis.py data/raw_data.csv` 处理数据，生成 `processed_data.csv`
- 处理：`python scripts/plot_results.py data/processed_data.csv figures/figure1.png` 绘制图片
- 输出：图片文件
然后再执行一次编译操作输出新的 PDF 文件。

> 然而，这样的重复操作显然违背了 Single Point of Truth, Don't Repeat Yourself 原则！

不过好在，这些数据结构仍然具有比较明确的依赖关系：
```
                              ┌──────────────┐
                              │   main.pdf   │
                              └──────┬───────┘
                                     │
                              ┌──────▼────────┐
                              │   main.tex    │
                              └──┬────┬───┬───┘
                                 │    │   │
                   ┌─────────────┘    │   └─────────────┐
                   │                  │                 │
          ┌────────▼────────┐         │           ┌─────▼──────────┐
          │   sections/     │         │           │bibliography.bib│
          ├─────────────────┤         │           └────────────────┘
          │introduction.tex │         │
          │methods.tex      │         │
          │results.tex      │         │
          └────┬────┬───┬───┘         │
               │    │   │             │
               │    │   └─────┐       │
               │    └───┐     │       │
               └────┐   │     │       │
                    │   │     │       │
          ┌─────────┴───┴─────┴───────┴──────┐
          │         figures/                 │  ← 多个父节点！
          ├──────────────────────────────────┤
          │  figure1.png    figure2.png      │
          └─────────┬────────────┬───────────┘
                    │            │
                    │  ┌─────────┘
                    │  │ generated by
          ┌─────────┴──┴──────────┐
          │   plot_results.py     │
          └───────────┬───────────┘
                      │ python scripts/plot_results.py data/processed_data.csv
          ┌───────────▼────────────┐
          │  processed_data.csv    │
          └───────────┬────────────┘
                      │ python scripts/data_analysis.py data/raw_data.csv
          ┌───────────▼────────────┐
          │   data_analysis.py     │
          └───────────┬────────────┘
                      │ reads
          ┌───────────▼────────────┐
          │    raw_data.csv        │  ← 原始输入
          └────────────────────────┘
```
注意 (虽然在论文写作中不常见)，有些文件可能会被多个父节点依赖 (例如 `figures/figure1.png` 可能既被 `main.tex` 直接引用，也被 `sections/results.tex` 引用)。这使得整个依赖不再是树结构，而允许环结构 (但不允许自环结构)，即形成“有向无环图”

> 小结：编译问题的复杂性，最终被归结于手动执行多次以“有向无环图”刻画的依赖链的繁琐性

> 思考：如果我们预先规定依赖关系之间的图结构，是否就可以自动化地完成编译过程？

答案是肯定的。这正是 `Makefile` 的作用。

#### Makefile 简介

既然我们声称
- 依赖关系是有向无环图
- 每个节点的生成都可以通过某种命令完成
- Makefile 可以根据依赖关系自动化地完成编译过程

那么 Makefile 必然要完成的工作是：
- 描述图结构 (Vertexes and Edges)
- 描述节点的生成命令

> 描述图结构

图$\Gamma(V, E)$可以通过：
- Fix 一个顶点$v \in V$
- 列出链接它的所有边$E_{v} = \left\{ e \in E | v \in \partial e \right\}$
- 遍历所有顶点

来描述。

其中第二步等同于
- 列出所有依赖于$v$的顶点集合$D_{v} = \left\{ u \in V | (u, v) \in E \right\}$

转换为计算机语言，我们可以使用如下的语法：
```make
target: dependency1 dependency2 ...
```
来描述这样的依赖关系。

> 描述节点的生成命令

给定了依赖关系，生成节点的命令可以在下一行直接声明(记得缩进是用 Tab 键，而不是空格)：
```make
target: dependency1 dependency2 ...
    command arg1 arg2 ... dependency1 dependency2 ...
```
遍历所有顶点，便可以描述完整的图结构与生成命令。

回到我们最终的论文写作流程，我们可以编写如下的 `Makefile`：
```make
main.pdf: main.tex figure1.png figure2.png bibliography.bib
	latexmk -pdf main.tex
    # pdflatex main.tex

figure1.png: processed_data.csv plot_results.py
	python plot_results.py processed_data.csv figure1.png

processed_data.csv: raw_data.csv data_analysis.py
	python data_analysis.py raw_data.csv processed_data.csv
```
这样就描述了整个依赖图结构与生成命令。

接下来，想要生成 PDF 文件时，我们只需要在终端中运行：
```bash
make main.pdf
```
如果只想要生成图片看看效果，可以直接运行：
```bash
make figure1.png
```

现在还存在几个问题：
- 如果某个文件没有变化，是否还需要重新生成？
- 如果某个文件变化了，是否需要重新生成所有依赖它的文件？
- 如果某个文件生成失败，是否需要继续生成其他文件？
Make 工具通过检查文件的时间戳来解决这些问题，从而实现增量编译。

> 现代的 LaTeX 编译工具 `latexmk` 本身就已经实现了类似的功能，因此在实际使用中，我们只需要在 Makefile 中调用 `latexmk` 即可，或者干脆直接使用 `latexmk` 来管理 LaTeX 项目的编译过程(不过，对于当前实验报告的复杂依赖关系，Makefile 是更贴合需求的选择)。

### 进一步优化

当然，从舒适程度的角度来说，我肯定还想要：
- 只输入 `make` 就可以生成最终的 PDF 文件
- 自动预览生成的 PDF 文件
- 与 Docker 容器结合使用
- etc.

这都可以通过进一步优化 `Makefile` 来实现。例如：
- 与 Docker 结合使用
```make
PDFLATEX_DOCKER = docker run -v $(pwd):/workdir -w /workdir danteev/texlive:TL2017 pdflatex
```
接着在生成命令中使用 `$(PDFLATEX_DOCKER)` 替代 `pdflatex` 即可。
- 只输入 `make` 即可生成 PDF 文件
```make
all: main.pdf
```
- 预览 PDF 文件
```make
.PHONY: all clean view
all: main.pdf
    @echo "Compilation complete: main.pdf generated."
view: main.pdf
    xdg-open main.pdf
```
- 清理中间文件
```make
clean-mid:
    rm -f *.aux *.log *.toc *.out *.bbl *.blg *.fls *.fdb_latexmk *.synctex.gz
```
- 清理所有生成文件
```make
clean: clean-mid
    rm -f main.pdf figure1.png processed_data.csv
```
然后直接按照`make clean`即可清理所有生成文件，其他的命令同理。

总之，Makefile 的强大之处在于它能够根据文件的依赖关系自动化地管理编译过程，从而大大简化了复杂项目的构建工作。
我强烈推荐任何一个物理系学生都应该学会使用 Makefile 来管理他们的论文写作与实验报告编写工作流程。

> 不过我发现，如果涉及高强度 AI 交互，比如说维护一个完全用 AI 生成的 beamer，而我只修改一个论文，那么这个时候 Makefile 的优势就不明显了。当然，如果用 claude code，那还是非常可以的。
> 但鉴于我没钱，所以我一般还是复制到 gemini 网页端再搬回去，这个过程就没法自动化了 (原因竟然是没钱，开源运动最终也要靠钱推动啊)。

## 结语

回顾我们今天的旅程，我并没有教`ls`的具体参数，也没有教你如何配置一个酷炫的桌面。
这些东西 Makes no sense for AI 时代的我们。

我们今天关注的是如下几个核心理念：

- Unix Philosophy: 组合简单的工具（IO 重定向、管道）解决复杂问题。
- Text Editing: 从“字符流”进化到“结构化编辑”（LSP, Tree-sitter），让人脑与电脑的频率对齐。
- Environment: 使用容器（Docker）封装环境，拒绝熵增，保证可复现性。
- Automation: 使用编排工具（Make）管理依赖与流程，释放你的大脑内存。

最重要的事情永远不是学习一个`术`，而是理解背后的`道`。老子有言曰：

> 有术无道止于术，有道无术术可求

与诸君共勉，谢谢大家！
