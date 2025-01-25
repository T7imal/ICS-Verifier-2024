import os
import subprocess

csv_path = "D:\GithubRepo\lc3tools\submits\lab1\成绩登记表-Sheet0.csv"


def verify_src(src_path: str):
    # 使用程序评测
    verifier_path = "D:/GithubRepo/lc3tools/build/bin/verifier_lab1.exe"
    submit_dir = os.path.dirname(src_path)

    # print("开始评测", src_path)

    try:
        if src_path.endswith(".txt"):
            # 复制txt文件，改为bin文件
            bin_path = src_path.replace(".txt", ".bin")
            with open(src_path, "r", encoding="utf-8") as f:
                with open(bin_path, "w", encoding="utf-8") as g:
                    g.write(f.read())
        else:
            bin_path = src_path

        # 记录下程序的输出，最后一行的格式为：
        # Total points earned: 0/100 (0%)
        # subprocess.run([verifier_path, src_path], cwd=submit_dir, check=True)
        result = subprocess.run(
            [verifier_path, bin_path], cwd=submit_dir, check=True, text=True, stdout=subprocess.PIPE
        )
        score = result.stdout.split("\n")[-2].split(" ")[-2].split("/")[0]
        if not score.isdigit():
            return None
        score = int(score)

        # 删除生成的bin文件
        if src_path.endswith(".txt"):
            os.remove(bin_path)

        return score
    except subprocess.CalledProcessError as e:
        print(f"Error running verifier: {e}")
        return None


def verify_submit(submit_dir: str):
    # 检查文件格式是否正确
    src_num = 0
    src_path = []
    report_num = 0
    report_path = []
    inner_folder_num = 0
    inner_folder_path = []
    for file in os.listdir(submit_dir):
        if file.endswith(".txt") or file.endswith(".bin"):
            src_num += 1
            src_path.append(os.path.join(submit_dir, file))
        elif file.endswith(".pdf"):
            report_num += 1
            report_path.append(os.path.join(submit_dir, file))
        elif os.path.isdir(os.path.join(submit_dir, file)):
            inner_folder_num += 1
            inner_folder_path.append(os.path.join(submit_dir, file))

    if src_num > 0 and report_num > 0:
        # 提取学号姓名
        report_file_name = report_path[0].split("\\")[-1]
        # 实验报告文件名格式为：学号_姓名_report.pdf，检查是否符合格式
        if len(report_file_name.split("_")) != 3:
            print("实验报告文件名格式错误")
            return
        student_id = report_file_name.split("_")[0]
        student_name = report_file_name.split("_")[1]
        # 验证源文件
        score = []
        for src in src_path:
            score.append(verify_src(src))
        # 去掉None
        score = [i for i in score if i is not None]
        if len(score) == 0:
            return
        max_score = max(score)

        print(f"{student_id} {student_name} 得分：{max_score}")
        # 输出到csv文件
        # 在csv文件中找到含有学号的行，在K列写入得分
        with open(csv_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        find_flag = False
        for i in range(len(lines)):
            if student_id in lines[i]:
                find_flag = True
                # 在K列写入得分
                lines[i] = lines[i].split(",")
                lines[i][10] = str(max_score)
                lines[i] = ",".join(lines[i])
                break
        if not find_flag:
            print(f"学号{student_id}在成绩登记表中未找到")
            return
        with open(csv_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
    elif inner_folder_num > 0:
        for folder in inner_folder_path:
            verify_submit(folder)


def verify_submits(submits_dir: str):
    for file in os.listdir(submits_dir):
        if os.path.isdir(os.path.join(submits_dir, file)):
            verify_submit(os.path.join(submits_dir, file))


if __name__ == "__main__":
    verify_submits("D:\GithubRepo\lc3tools\submits\lab1\submits")
