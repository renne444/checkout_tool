#!/Users/dengjinxi/mambaforge/envs/yuki/bin/python
# -*- coding: UTF-8 -*-

# 由于我经常需要读、开发多个不同分支的代码，并且代码需要依赖的库比较多。如果为每个不同分支、不同用途的代码都设立完整的workspace，会产生空间不足的问题。
# 该脚本能解决在不同代码分支、不同用途的代码备份和读取。
# 本人的代码环境分为开发、阅读、迁移三部分。分别对应3个workspace，均包含完整的代码。调用checkout可先储存原有的代码，再load需要切换的代码。

from pathlib import Path
import logging
import os
import argparse
import shutil
import subprocess

path_root = Path("/Users/dengjinxi/workspace")
backup_dir_root = path_root / "code_read_backup"

def dangerous_dir_check(path):
    dangerous_path_group = [str(path_root), str(backup_dir_root), "/Users/dengjinxi", "Users"]
    for str_path in dangerous_path_group:
        if path.find(str_path) != -1 and len(path) - len(str_path) <= 1:
            raise "fuck you"

def message():
    print("请永远记住把工作目录删掉的难堪经历")

def diretory_replace(path_dir_delete, path_dir_copy):
    dangerous_dir_check(str(path_dir_delete))
    if path_dir_delete.is_dir():
        shutil.rmtree(path_dir_delete)
    shutil.copytree(path_dir_copy, path_dir_delete)
    print("fuck")

def intelligent_relative_path_generate(change_dir):
    change_path = Path(change_dir).absolute()
    if not change_path.is_dir():
        print(f"path change error: {str(change_path)} not a dir or not exist")
        return "", False

    change_abs = change_path.absolute()
    workspace_root_group = [str(path_root), str(backup_dir_root)]
    workspace_root_group = list(reversed(sorted(workspace_root_group)))
    print(f"parse path {change_abs}, workspace root group {workspace_root_group}")

    for root_path in workspace_root_group:
        begin_pos = str(change_abs).find(root_path)
        if begin_pos == -1:
            continue
        print(begin_pos)
        return str(change_abs)[begin_pos + len(str(root_path)) + 1:], True

    return change_dir, True
    

def checkout():
    pass

def backup(src_path=""):
    if src_path == "":
        logging.error("error occur: src_path is empty")
        return
    src_path = os.path.realpath(src_path)
    print(src_path)

    # add intelligent analyze   for src_path adjustment
    temp_path, ret = intelligent_relative_path_generate(src_path)
    if ret == False:
        logging.error("intelligent change false")
        return
    src_path = temp_path
    
    print("dir path intelligent analysis, path change to", temp_path)
    
    src_file = path_root / src_path
    if not src_file.is_dir():
        logging.error(f"src dir {src_file} is not exist, or not a diretory")
        return
    
    backup_file_name = ".".join(src_path.split('/'))
    print("backup file: ", backup_file_name)

    cmd_get_branch = "git rev-parse --abbrev-ref HEAD"
    
    # 先检查指令执行得怎么样
    print("error check", src_file)
    subprocess.check_call(cmd_get_branch , cwd=str(src_file), shell=True)

    branch = subprocess.check_output(cmd_get_branch, shell=True, cwd=str(src_file))
    branch = str(branch.strip(), encoding="utf-8")
   
    backup_file_name = backup_file_name + f".{branch}"
    print(backup_file_name)
    
    backup_file_path = backup_dir_root / backup_file_name
    print(f"备份目录：将目录 {str(backup_file_path)} 替换为 {str(src_file)}")
    diretory_replace(backup_file_path.absolute(), src_file.absolute())

def load(backup_path=""):
    if backup_path == "":
        logging.error("error occur: backup_path is empty")
        return

    backup_path = os.path.realpath(backup_path)
    print(backup_path)

    (_, backup_file) = os.path.split(backup_path)
    
    file_path = backup_dir_root / backup_file 
    str_path = str(file_path)
    if file_path.is_dir():
        backup_dir_array = backup_file.split(".")
        src_file = "/".join(backup_dir_array[:-1])
        print(src_file)
        src_path = path_root / src_file
        src_branch = backup_dir_array[-1]
        if src_path.is_dir() == False:
           print(f"src path = {src_path}, not exist or not a dir")
           return
        # 将src_path内容替换为file_path
        print(f"将目录{src_path}替换为{file_path}, 分支{src_branch}")
        diretory_replace(src_path.absolute(), file_path.absolute())

    elif file_path.is_file():
        if str_path.find("tar.gz") == -1:
            logging.error(f"file {str_path} is not a dir, but not a tar.gz")
        else:
            print("tar.gz logic is undefined")
    else:
        logging.error(f"path error: {str_path}")
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog= 'Backup-er',
        description= 'checkout tools for multiple code version or usage'
    )
    parser.add_argument('-l', '--load')
    parser.add_argument('-b', '--backup')
    args = parser.parse_args()
    if (args.load):
        load(args.load) 
    elif args.backup:
        backup(args.backup)
    message()
