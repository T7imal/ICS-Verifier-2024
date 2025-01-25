import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import subprocess
import threading
from tqdm import tqdm

lock = threading.Lock()


# submit_dir
# ├── lab1.bin / lab2.asm / lab3.asm / lab4.asm / lab5.asm / lab6.asm
# ├── PB23000001_张三_report.pdf
# 错误时返回空字典，正确时返回字典
def verify_single_submit(
    lab_index: int, submit_dir: str, verifier_path: str, copy_wrong_formatted: bool, submits_dir: str
):
    # 若submit_dir中只有一个文件夹，则进入文件夹
    if len(os.listdir(submit_dir)) == 1 and os.path.isdir(
        os.path.join(submit_dir, os.listdir(submit_dir)[0])
    ):
        return verify_single_submit(
            lab_index,
            os.path.join(submit_dir, os.listdir(submit_dir)[0]),
            verifier_path,
            copy_wrong_formatted,
            submits_dir,
        )

    # 检查文件格式是否正确
    format_error = False
    # 此时submit_dir中应该有且仅有一个源文件和一个实验报告
    src_num = 0
    src_path = ""
    report_num = 0
    report_path = ""
    for file in os.listdir(submit_dir):
        if file.endswith(".bin") or file.endswith(".asm"):
            src_num += 1
            src_path = os.path.join(submit_dir, file)
        elif file.endswith(".pdf"):
            report_num += 1
            report_path = os.path.join(submit_dir, file)

    if src_num != 1 or report_num != 1:
        print(submit_dir + "源文件或实验报告数量错误")
        format_error = True

    # 检查实验报告文件名格式是否正确
    report_file_name = os.path.basename(report_path)
    if len(report_file_name.split("_")) != 3:
        print(submit_dir + "实验报告文件名格式错误")
        format_error = True

    if copy_wrong_formatted:
        if format_error:
            # 在submits_dir的上一层新建文件夹，将格式错误的文件夹复制到其中
            wrong_formatted_dir = os.path.join(
                os.path.dirname(submits_dir), f"lab{lab_index}_wrong_formatted"
            )
            if not os.path.exists(wrong_formatted_dir):
                os.mkdir(wrong_formatted_dir)
            os.system(f"cp -r {submit_dir} {wrong_formatted_dir}")
        return {}

    if format_error:
        return {}

    student_id = report_file_name.split("_")[0]
    student_name = report_file_name.split("_")[1]

    # 验证源文件
    verifier_result = subprocess.run(
        [verifier_path, src_path, "--seed=1234", "--ignore-privilege"],
        cwd=submit_dir,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        errors="ignore",
    )
    # 当正确汇编时，输出的最后一行格式为"Total points earned: 0/100 (0%)"
    # 检查是否成功汇编
    if "Total points earned:" not in verifier_result.stdout:
        print(submit_dir + "未成功汇编")
        return {}
    score = verifier_result.stdout.split("\n")[-2].split(" ")[-2].split("/")[0]

    result = {}
    result["student_id"] = student_id
    result["student_name"] = student_name
    result["score"] = score
    return result


def verify_submits(
    lab_index: int, submits_dir: str, verifier_path: str, output_csv: str, copy_wrong_formatted: bool
):
    if copy_wrong_formatted:
        # 将submits_dir中所有非文件夹的文件复制到指定文件夹中
        # 重新创建文件夹
        wrong_formtted_dir = os.path.join(os.path.dirname(submits_dir), f"lab{lab_index}_wrong_formatted")
        if os.path.exists(wrong_formtted_dir):
            os.system(f"rm -rf {wrong_formtted_dir}")
        os.mkdir(wrong_formtted_dir)

        for file in os.listdir(submits_dir):
            if os.path.isfile(os.path.join(submits_dir, file)):
                os.system(f"cp {os.path.join(submits_dir, file)} {wrong_formtted_dir}")

    results = []
    submit_dirs = [d for d in os.listdir(submits_dir) if os.path.isdir(os.path.join(submits_dir, d))]
    with ThreadPoolExecutor() as executor:
        future_to_submit = {
            executor.submit(
                verify_single_submit,
                lab_index,
                os.path.join(submits_dir, submit_dir),
                verifier_path,
                copy_wrong_formatted,
                submits_dir,
            ): submit_dir
            for submit_dir in submit_dirs
        }

        for future in tqdm(
            as_completed(future_to_submit), total=len(future_to_submit), desc="Verifying submissions"
        ):
            submit_dir = future_to_submit[future]
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as exc:
                print(f"{submit_dir} 生成结果时发生异常: {exc}")

    for result in results:
        print(f"{result['student_id']} {result['student_name']} 得分：{result['score']}")
        with lock:
            # 输出到csv文件
            with open(output_csv, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # 找到学号对应的行，检查姓名是否一致，若不一致则报错，若一致则找到lab_index对应的列并更新
            # 第K列为lab1，第L列为lab2，以此类推
            found = False
            for i in range(len(lines)):
                if result["student_id"] in lines[i]:
                    found = True
                    if result["student_name"] not in lines[i]:
                        print(f"学号 {result['student_id']} 对应的姓名不一致")
                        break
                    lines[i] = lines[i].split(",")
                    lines[i][lab_index + 9] = result["score"]
                    lines[i] = ",".join(lines[i])
                    break

            if not found:
                print(f"学号 {result['student_id']} 不存在")
                continue

            with open(output_csv, "w", encoding="utf-8") as f:
                f.writelines(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--lab-index", type=int, help="实验序号，取值为1-6")
    parser.add_argument("-v", "--verifier-path", type=str, help="verifier可执行文件路径")
    parser.add_argument("-i", "--input-submits", type=str, help="输入学生提交文件夹路径")
    parser.add_argument("-o", "--output-csv", type=str, help="输出csv文件路径")
    parser.add_argument("--copy-wrong-formatted", action="store_true", help="复制格式错误的文件")

    args = parser.parse_args()

    lab_index = args.lab_index
    if lab_index not in [1, 2, 3, 4, 5, 6]:
        print("仅支持实验1-6")
        exit(1)
    verifier_path = args.verifier_path
    if not os.path.isfile(verifier_path):
        print("verifier文件不存在")
        exit(1)
    # 转换为绝对路径
    verifier_path = os.path.abspath(verifier_path)

    input_submits = args.input_submits
    if not os.path.isdir(input_submits):
        print("文件夹不存在")
        exit(1)
    # 转换为绝对路径
    input_submits = os.path.abspath(input_submits)

    output_csv = args.output_csv
    if not os.path.isfile(output_csv):
        print("csv文件不存在")
        exit(1)
    # 转换为绝对路径
    output_csv = os.path.abspath(output_csv)

    # 若copy_wrong_formatted为True，则不进行测试，而是将
    copy_wrong_formatted = args.copy_wrong_formatted

    verify_submits(lab_index, input_submits, verifier_path, output_csv, copy_wrong_formatted)
