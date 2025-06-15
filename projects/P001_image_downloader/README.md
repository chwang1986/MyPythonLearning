# Image Downloader Project

## 功能
- 从指定 URL 下载图片，保存到用户指定的路径和文件名。
- 计算图片的 SHA256 哈希值作为唯一标识，防止重复下载。
- 将图片信息（URL、文件名、路径、大小、哈希值、创建时间）存入 SQLite 数据库。
- 使用日志记录操作细节，保存到 `data/logs/downloader.log`。
- 提供模块化接口，供其他项目复用下载和数据库功能。

## 文件结构
```
MyPythonLearning/projects/image_downloader/
├── data/
│   ├── images.db              # SQLite 数据库
│   └── migrations/            # 数据库迁移脚本
│       └── init_db.sql        # 初始建表脚本
├── src/
│   ├── __init__.py           # 标记为 Python 包
│   ├── downloader.py         # 下载和存储逻辑
│   └── db_manager.py         # 数据库操作
|—— config/
|   └── logging.json          # 日志配置文件
├── tests/
│   └── test_downloader.py    # 测试脚本（占位，待实现）
├── README.md                 # 项目说明
└── main.py                   # 主程序入口
```
- **data/**: 存储数据库和日志
  - **images.db**: SQLite 数据库，存储图片信息
  - **migrations/init_db.sql**: 数据库初始化脚本
  - **logs/downloader.log**: 日志文件
- **src/**: 核心代码
  - **downloader.py**: 下载和存储逻辑
  - **db_manager.py**: 数据库操作
- **tests/**: 单元测试（待实现）
- **main.py**: 主程序入口
- **requirements.txt**: 依赖清单,这里就不弄了，因为我没有新建虚拟环境
- **README.md**: 项目说明

## 安装
1. 确保自己已经安装 requests 库。
2. 初始化数据库：
   ```bash
   sqlite3 data/images.db < data/migrations/init_db.sql
   ```

## 使用
1. 运行主程序：
   ```bash
   python main.py
   ```
2. 输入提示：
   - 图片 URL（如 `https://www.python.org/static/img/python-logo.png`）
   - 新文件名（如 `python_logo.png`）
   - 存储路径（如 `D:\Images` 或 `images`）
3. 输出：
   - 成功：图片保存，信息存入数据库，日志记录。
   - 重复：提示图片已存在，显示已有文件名和路径。
   - 失败：打印错误信息，日志记录。

## 模块化复用
其他项目可导入 `src/downloader.py` 和 `src/db_manager.py`：
```python
from src.downloader import download_image
from src.db_manager import check_duplicate

# 下载图片
download_image("https://example.com/image.jpg", "image.jpg", "images", "data/images.db")

# 检查重复
result = check_duplicate("data/images.db", image_hash)
```

## 数据库结构
- 表：`images`
- 字段：
  - `id`: INTEGER, 主键，自增
  - `url`: TEXT, 图片原始 URL
  - `filename`: TEXT, 新文件名
  - `path`: TEXT, 存储路径
  - `size`: INTEGER, 文件大小（字节）
  - `hash`: TEXT, SHA256 哈希值
  - `created_at`: TEXT, 创建时间（YYYY-MM-DD HH:MM:SS）


## 日志
- 日志保存到 `data/logs/downloader.log`。
- 包含 INFO（操作记录）、ERROR（错误信息）等级别。

## 开始日期
2025-06-15

## 后续计划
- 添加单元测试（`tests/test_downloader.py`）。
- 支持批量下载。
- 验证 URL 是否为图片。