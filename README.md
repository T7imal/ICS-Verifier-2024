# USTC ICS 2024 FALL 张辉班 实验测试机

## 简介

本仓库为USTC ICS 2024 FALL 张辉班实验测试机，用于测试学生实验代码的正确性。本仓库fork自[LC3Tools](https://github.com/chiragsakhuja/lc3tools)

## 使用说明

1. 获取测试程序

    对Windows用户：打开[Release](https://github.com/T7imal/ICS-Verifier-2024/releases/tag/latest)页面下载测试程序

    对Linux用户，请自行构建，可参考[官方文档](https://github.com/chiragsakhuja/lc3tools/blob/master/docs/BUILD.md#command-line-tools-and-unit-tests)

2. 打开终端

3. 运行测试程序

    ```shell
    # Lab1 需要在包含"PBxxxxxxxx_name_report.pdf"的目录下运行，因为评测程序检测同一目录下的pdf文件来得到学号
    cd path/to/your/lab1/directory
    path/to/verifier_lab1.exe path/to/your/program.bin

    # Labx (x=2,3,4,5,6)
    path/to/verifier_labx.exe path/to/your/program.asm

    # 对于后几个实验，可以设置--ignore-privilege，因为很多同学在编写时打开了忽略特权模式
    path/to/verifier_labx.exe path/to/your/program.asm --ignore-privilege
    ```

4. 程序会在终端输出测试结果

## 其他事项

- 测试程序的其他参数如下，具体请查看[官方文档](https://github.com/chiragsakhuja/lc3tools/blob/master/docs/CLI.md#unit-tests)

    ```shell
    -h,--help              Print this message
    --print-output         Print program output
    --asm-print-level=N    Assembler output verbosity [0-9]
    --sim-print-level=N    Simulator output verbosity [0-9]
    --ignore-privilege     Ignore access violations
    --tester-verbose       Output tester messages
    --seed=N               Optional seed for randomization
    --test-filter=TEST     Only run TEST (can be repeated)
    ```

- 测试程序的编写方法参见[官方文档](https://github.com/chiragsakhuja/lc3tools/blob/master/docs/TEST.md)

- 测试程序的具体实现位于`src/test/tests/`目录下，如果感兴趣或者想当助教可以看看。根目录的Python脚本就别看了，写的很烂

- 测试结果不代表最终成绩，很多同学的程序由于不够规范，只能手动修改后再进行测试。正因如此，测试程序应该在布置实验时就提供给同学们，让同学们以测试程序得分为最终得分，可以免去很多麻烦