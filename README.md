# 🧰 luogu-cli – 洛谷命令行工具

一个用 Python 编写的命令行工具，用于从 [洛谷（Luogu）](https://www.luogu.com.cn) 下载题目描述、样例输入输出、题解等内容，方便本地学习与练习。

---

## 📦 功能特性

- ✅ `lgcli parse PID`：下载指定题目的题面、样例和题解
- ✅ `lgcli view PID`：在终端中查看题目描述（支持 Markdown 渲染）
- ✅ `lgcli solution PID`：列出所有题解或查看某一篇详细内容
- ✅ 使用 `rich` 渲染终端 Markdown，支持彩色样式
- ✅ 支持打包为单文件 `.exe`（通过 PyInstaller）

---

## 🧩 依赖库

确保你已安装以下 Python 包：

```bash
pip install rich requests beautifulsoup4 python-dotenv
```

---

## ⚙️ 配置 Cookie

你需要先登录洛谷官网，并获取以下 Cookie 值填入 `.env` 文件中：

```env
CLIENT_ID=你的client_id
UID=你的uid
CF_CLEARANCE=你的cf_clearance
C3VK=你的c3vk
```

> 注意：这些值可以在浏览器开发者工具的“Application > Cookies”中找到。

---

## 🚀 使用方式

### 1. 下载题目信息

```bash
python main.py parse P1145
```

这会创建一个以题目编号命名的目录（如 `P1145/`），包含：
- `P1145.md`：题面描述
- `samples/`：样例输入输出
- `solutions/`：题解 Markdown 文件

---

### 2. 查看题目描述

```bash
python main.py view P1145
```

使用 `rich` 在终端中渲染 Markdown 格式的题目内容。

---

### 3. 查看题解列表或具体内容

```bash
python main.py solution P1145
```

列出所有题解标题：

```
可用题解：
1. 题解1_xxxxx
2. 题解2_yyyyyy
```

查看具体题解内容：

```bash
python main.py solution P1145 --id 题解1_xxxxx
```

---

## 🚗 下一步发展

- 📝 提交代码
- 🚩参加比赛
- ...

---

## 📜 许可证

本项目采用 LGPL License。