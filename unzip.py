import zipfile
import py7zr
import rarfile
import os
import argparse


def detect_encoding(filename: str):
    try:
        filename.encode("cp437").decode("cp437")
        return "cp437"
    except UnicodeEncodeError:
        return "utf-8"


def unzip_file(zip_path: str, extract_to: str):
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            for member in zip_ref.infolist():
                # 忽略 _MACOSX 文件夹
                if member.filename.startswith("__MACOSX/"):
                    continue

                # 检查文件名编码并进行转换
                encoding = detect_encoding(member.filename)
                if encoding == "cp437":
                    try:
                        member.filename = member.filename.encode("cp437").decode("utf-8")
                    except:
                        member.filename = member.filename.encode("cp437").decode("gbk")
                # 如果是 utf-8 编码，则不需要转换

                zip_ref.extract(member, extract_to)
    except zipfile.BadZipFile:
        # 尝试用7z格式解压
        try:
            with py7zr.SevenZipFile(zip_path, mode="r") as z:
                z.extractall(extract_to)
        except py7zr.Bad7zFile:
            # 尝试用rar格式解压
            try:
                with rarfile.RarFile(zip_path, "r") as z:
                    z.extractall(extract_to)
            except rarfile.BadRarFile:
                print(f"无法解压 {zip_path}")


def unzip_submits(submits_zip_path: str):
    # 解压总压缩文件
    submits_unzip_dir = os.path.dirname(submits_zip_path)
    submits_name = os.path.basename(submits_zip_path).split(".")[:-1]
    submits_name = ".".join(submits_name)
    submits_dir = os.path.join(submits_unzip_dir, submits_name)
    unzip_file(submits_zip_path, submits_dir)

    # 解压每个学生的提交文件
    for file in os.listdir(submits_dir):
        if file.endswith(".zip") or file.endswith(".7z") or file.endswith(".rar"):
            zip_path = os.path.join(submits_dir, file)
            unzip_dir = os.path.join(submits_dir, file.split(".")[0])
            # 去掉解压路径中的空格
            unzip_dir = unzip_dir.replace(" ", "")
            unzip_file(zip_path, unzip_dir)
            os.remove(zip_path)

    return submits_dir


if __name__ == "__main__":
    # 输入任意个压缩文件路径
    parser = argparse.ArgumentParser()
    parser.add_argument("submits_zip_path", nargs="+", help="压缩文件路径")
    args = parser.parse_args()

    for submits_zip_path in args.submits_zip_path:
        unzip_submits(submits_zip_path)
