import os

def list_files_by_suffix(folder_path, suffix):
    """
    获取指定文件夹及其子文件夹中所有符合后缀条件的文件。
    
    参数:
        folder_path (str): 文件夹路径。
        suffix (str): 文件后缀（例如 '.txt' 或 '.tif'）。
        
    返回:
        list: 符合条件的文件路径列表。
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"指定的路径 {folder_path} 不是有效的文件夹。")
    
    # 初始化结果列表
    matching_files = []
    
    # 遍历文件夹及其子文件夹
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(suffix):  # 判断文件是否符合后缀
                matching_files.append(os.path.join(root, file))
    
    return matching_files

def list_all_folders(folder_path, recursive=True):
    """
    获取指定文件夹下的所有文件夹路径，可选择是否递归获取子文件夹。

    参数:
        folder_path (str): 文件夹路径。
        recursive (bool): 是否递归获取嵌套子文件夹。默认为 True。

    返回:
        list: 所有文件夹路径的列表。
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"指定的路径 {folder_path} 不是有效的文件夹。")

    folder_list = []

    if recursive:
        # 递归获取所有子文件夹
        for root, dirs, _ in os.walk(folder_path):
            for dir_name in dirs:
                folder_list.append(os.path.join(root, dir_name))
    else:
        # 仅获取直接子文件夹
        folder_list = [
            os.path.join(folder_path, name)
            for name in os.listdir(folder_path)
            if os.path.isdir(os.path.join(folder_path, name))
        ]

    return folder_list