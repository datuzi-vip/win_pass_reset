# Windows 密码修改工具

面向小白用户的 Windows 密码修改桌面工具，支持：

- 修改当前登录用户自己的密码（需输入旧密码）
- 管理员重置其他本地用户密码（需管理员权限）

## 支持系统

- Windows 8.1 / 10 / 11
- Windows Server 2012 / 2012 R2 / 2016 / 2019 / 2022 / 2025

不支持 Windows 7 及 Windows Server 2008 R2。

## 开发环境

- Python 3.14
- PySide6（原生组件 + Element Plus QSS 样式）

架构说明见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

## 安装依赖

```powershell
.venv\Scripts\pip install -r requirements.txt
```

## 运行

```powershell
.venv\Scripts\python run.py
```

## 打包

```powershell
.venv\Scripts\pyinstaller build\win_pass_reset.spec `
  --workpath build\pyinstaller_work `
  --distpath dist
```

输出：`dist\WinPassReset.exe`

## 管理员模式

在「管理员重置他人密码」标签页中，若当前非管理员权限，点击「以管理员身份运行」将通过 UAC 提权重启程序。
