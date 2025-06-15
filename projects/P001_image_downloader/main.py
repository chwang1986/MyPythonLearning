# main.py
# 功能：用户交互入口，调用 downloader 和 db_manager 模块下载图片
# 日期：2025-06-27

import os
from src.downloader import download_image
from src.db_manager import init_database

def main():
    """主函数，获取用户输入并执行下载"""
    # 数据库路径
    db_path = os.path.join("data", "images.db")

    # 初始化数据库
    os.makedirs("data", exist_ok=True)
    init_database(db_path)

    # 获取用户输入
    url = input("请输入图片 URL: ")
    filename = input("请输入新文件名（包括扩展名，如 image.jpg）: ")
    save_dir = input("请输入保存路径（绝对路径或相对路径）: ")

    # 执行下载
    download_image(url, filename, save_dir, db_path)

if __name__ == "__main__":
    main()