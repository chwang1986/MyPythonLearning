import os

def create_directory(path):
    """创建文件夹，如果已存在则跳过"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"创建文件夹: {path}")
    else:
        print(f"文件夹已存在，跳过: {path}")

def create_file(path, content):
    """创建文件并写入内容，如果文件已存在则跳过"""
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"创建文件: {path}")
    else:
        print(f"文件已存在，跳过: {path}")

def setup_learning_structure():
    """在当前目录（MyPythonLearning）下创建或补全学习文件夹结构"""
    # 当前目录作为根目录
    root_dir = "."

    # 子目录
    directories = [
        os.path.join(root_dir, "projects"),
        os.path.join(root_dir, "exercises", "basics"),
        os.path.join(root_dir, "exercises", "intermediate"),
        os.path.join(root_dir, "exercises", "advanced"),
        os.path.join(root_dir, "exercises", "daily_challenges"),
        os.path.join(root_dir, "notes"),
        os.path.join(root_dir, "experiments")
    ]

    for directory in directories:
        create_directory(directory)
    
    print(f"文件夹结构检查/补全完成，位于: {os.path.abspath(root_dir)}")

if __name__ == "__main__":
    setup_learning_structure()