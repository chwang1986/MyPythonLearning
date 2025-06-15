# db_manager.py
# 功能：封装 SQLite 数据库操作，包括创建、插入和查询图片信息
# 日期：2025-06-27

import sqlite3
from datetime import datetime
import logging
import logging.config
import json

# 加载 JSON 日志配置文件
with open('config/logging.json', 'r') as f:
    logging.config.dictConfig(json.load(f))
logger = logging.getLogger(__name__)

def init_database(db_path):
    """
    初始化数据库，创建 images 表
    参数：
        db_path: 数据库文件路径
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                filename TEXT NOT NULL,
                path TEXT NOT NULL,
                size INTEGER NOT NULL,
                hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()
        logging.info("数据库初始化成功: %s", db_path)
    except sqlite3.Error as e:
        logging.error("数据库初始化失败: %s", e)
        raise
    finally:
        conn.close()

def check_duplicate(db_path, image_hash):
    """
    检查数据库中是否已有相同哈希值的图片
    参数：
        db_path: 数据库文件路径
        image_hash: 图片的 SHA256 哈希值
    返回：
        tuple (filename, path) 如果存在，否则 None
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT filename, path FROM images WHERE hash = ?", (image_hash,))
        result = cursor.fetchone()
        if result:
            logging.info("发现重复图片，哈希值: %s, 文件名: %s", image_hash, result[0])
        return result
    except sqlite3.Error as e:
        logging.error("检测重复图片失败: %s", e)
        return None
    finally:
        conn.close()

def save_image_info(db_path, url, filename, path, size, image_hash):
    """
    保存图片信息到数据库
    参数：
        db_path: 数据库文件路径
        url: 图片原始 URL
        filename: 新文件名
        path: 存储路径
        size: 文件大小（字节）
        image_hash: 图片的 SHA256 哈希值
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO images (url, filename, path, size, hash, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (url, filename, path, size, image_hash, created_at))
        conn.commit()
        logging.info("图片信息保存成功: %s, %s", filename, path)
    except sqlite3.Error as e:
        logging.error("保存图片信息失败: %s", e)
        raise
    finally:
        conn.close()