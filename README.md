# LLMAssistant 项目说明

## 项目简介
LLMAssistant 是一个基于 Python 的多功能智能助手，集成了天气查询、地震信息、电影信息、股票数据、数学计算等工具，并支持与大模型 API 对接，实现自然语言对话与自动工具调用。

## 环境依赖
- Python 3.8 及以上（推荐使用 Anaconda 环境）
- 依赖包：requests、sympy

安装依赖：
```powershell
pip install requests sympy
```
如需 Jupyter Notebook 支持：
```powershell
pip install notebook
```

## 主要文件说明
- `example.py`：主程序，包含所有功能实现
- `run.py`：一键启动脚本，自动切换目录并调用 example.py
- `movies_list.json`、`comments_list.json`：电影及评论数据
- `演示图片/`：功能演示截图
- `课程设计报告.md`、`课程设计报告.docx`：课程设计文档

## 运行方式
1. 打开终端（PowerShell），进入项目目录：
   ```powershell
   cd C:\Users\H.Seldon\Desktop\LLMAssistant
   ```
2. 一键运行：
   ```powershell
   python run.py
   ```
   或直接运行主程序：
   ```powershell
   python example.py
   ```

## 注意事项
- 若需使用股票、天气等接口，请确保网络畅通。
- 若需自定义 API Key，请在 `example.py` 中相应位置替换。
- 运行时请确保数据文件与主程序在同一目录。
- 图片演示请查看 `演示图片/` 文件夹。

## 常见问题
- **依赖未安装**：请先执行 `pip install` 命令。
- **API Key 失效**：请自行申请并替换为有效的 Key。
- **找不到数据文件**：请确认工作目录正确，或用绝对路径读取。

如有其他问题，欢迎反馈。
