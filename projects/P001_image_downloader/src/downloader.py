# downloader.py
# 功能：从 URL 下载图片，计算哈希值并保存，检查重复性
# 日期：2025-06-27

import os
import requests
import hashlib
import logging
import logging.config
import json
from src.db_manager import check_duplicate, save_image_info

# 配置日志 日志配置文件
with open('config/logging.json', 'r') as f:
    logging.config.dictConfig(json.load(f))
logger = logging.getLogger(__name__)

def calculate_image_hash(content):
    """
    计算图片内容的 SHA256 哈希值
    参数：
        content: 图片的二进制内容
    返回：
        str: SHA256 哈希值（十六进制）
    """
    try:
        sha256 = hashlib.sha256()
        sha256.update(content)
        image_hash = sha256.hexdigest()
        logging.debug("计算哈希值成功: %s", image_hash[:10] + "...")
        return image_hash
    except Exception as e:
        logging.error("计算哈希值失败: %s", e)
        raise

def download_image(url, filename, save_dir, db_path):
    """
    下载图片并保存到指定目录，检查重复并存储信息
    参数：
        url: 图片的 URL
        filename: 保存的文件名（包括扩展名）
        save_dir: 保存目录路径
        db_path: 数据库文件路径
    返回：
        bool: 下载是否成功
    """
    try:
        # 确保保存目录存在
        os.makedirs(save_dir, exist_ok=True)
        logging.info("确保目录存在: %s", save_dir)

        # 下载图片
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            logging.error("下载失败，状态码: %s, URL: %s", response.status_code, url)
            print(f"下载失败，状态码: {response.status_code}")
            return False

        image_content = response.content
        image_hash = calculate_image_hash(image_content)
        logging.info("图片下载成功，URL: %s, 哈希值: %s", url, image_hash[:10] + "...")

        # 检查重复
        duplicate = check_duplicate(db_path, image_hash)
        if duplicate:
            logging.info("跳过重复图片: %s, 已有路径: %s", filename, duplicate[1])
            print(f"图片已存在: {duplicate[0]}，路径: {duplicate[1]}")
            return True

        # 保存图片
        save_path = os.path.join(save_dir, filename)
        logging.debug(f"保存图片为{save_path}")

        with open(save_path, 'wb') as f:
            f.write(image_content)
        size = os.path.getsize(save_path)
        logging.debug("图片已保存: %s, 大小: %d 字节", save_path, size)

        # 保存信息到数据库
        save_image_info(db_path, url, filename, save_path, size, image_hash)
        print(f"图片下载成功: {filename}，路径: {save_path}，大小: {size} 字节")
        return True

    except requests.exceptions.RequestException as e:
        logging.error("网络错误，URL: %s, 错误: %s", url, e)
        print(f"下载失败: {e}")
        return False
    except Exception as e:
        logging.error("下载过程中发生错误: %s", e)
        print(f"发生错误: {e}")
        return False