#include <cstdlib>
#include <cstring>
#include <string>
#define API_VER 2
#include "framework.h"

#define N_SAMPLES 6

// 测试用例
int index1 = 0;
char true_testcases[N_SAMPLES][100] = {};
int index2 = 0;
char false_testcases[N_SAMPLES][100] = {};

// 生成测试用例
void generate_testcases(void) {
  // 设置随机数种子
  srand(1234);

  for (int i = 0; i < N_SAMPLES; i++) {
    int length = rand() % 100;
    // int length = 5;
    for (int j = 0; j <= length / 2; j++) {
      char c;
      c = rand() % 26 + 'a';
      true_testcases[i][j] = c;
      true_testcases[i][length - j - 1] = c;
      false_testcases[i][j] = c;
      false_testcases[i][length - j - 1] = c;
    }
    true_testcases[i][length] = '\0';
    false_testcases[i][length] = '\0';
    int index = 0;
    do {
      index = rand() % length;
    } while (length % 2 == 1 && index == length / 2);
    false_testcases[i][index] =
        (false_testcases[i][index] - 'a' + 1) % 26 + 'a';
  }
}

// 长度为零的字符串是回文串
void ZeroTest(lc3::sim &sim, Tester &tester, double total_points) {
  // 设置PC寄存器、需要的内存参数
  sim.writePC(0x3000);
  sim.writeMem(0x3100, 0);
  // 设置最大运行指令数并运行
  sim.setRunInstLimit(50000);
  bool success = sim.runUntilHalt();
  // 验证结果
  std::string prompt_success =
      "The program is expected to halt without any exception";
  std::string prompt_check =
      "Input is a string with length 0, output is expected to be 1";
  bool check = sim.readMem(0x3200) == 1;
  tester.verify(prompt_success, success, total_points * 1 / 5);
  tester.verify(prompt_check, check, total_points * 4 / 5);
}

// 输入长度为零，但是字符串内存位置不为零
void NonStandardInputTest(lc3::sim &sim, Tester &tester, double total_points) {
  // 设置PC寄存器、需要的内存参数
  sim.writePC(0x3000);
  sim.writeMem(0x3100, 0);
  sim.writeStringMem(0x3101, "abcd");
  // 设置最大运行指令数并运行
  sim.setRunInstLimit(50000);
  bool success = sim.runUntilHalt();
  // 验证结果
  std::string prompt_success =
      "The program is expected to halt without any exception";
  std::string prompt_check =
      "Input is a random string which length is set to 0, "
      "output is expected to be 1";
  bool check = sim.readMem(0x3200) == 1;
  tester.verify(prompt_success, success, total_points * 1 / 5);
  tester.verify(prompt_check, check, total_points * 4 / 5);
}

// 验证回文串
void TrueTest(lc3::sim &sim, Tester &tester, double total_points) {
  // 设置PC寄存器、需要的内存参数
  sim.writePC(0x3000);
  int str_size = strlen(true_testcases[index1]);
  sim.writeMem(0x3100, str_size);
  sim.writeStringMem(0x3101, true_testcases[index1]);
  // 设置最大运行指令数并运行
  sim.setRunInstLimit(50000);
  bool success = sim.runUntilHalt();
  // 验证结果
  std::string prompt_success =
      "The program is expected to halt without any exception";
  std::string prompt_check = "Input is " + std::string(true_testcases[index1]) +
                             ", output is expected to be 1";
  bool check = sim.readMem(0x3200) == 1;
  tester.verify(prompt_success, success, total_points * 1 / 5);
  tester.verify(prompt_check, check, total_points * 4 / 5);
  index1++;
}

// 验证非回文串
void FalseTest(lc3::sim &sim, Tester &tester, double total_points) {

  // 设置PC寄存器、需要的内存参数
  sim.writePC(0x3000);
  int str_size = strlen(false_testcases[index2]);
  sim.writeMem(0x3100, str_size);
  sim.writeStringMem(0x3101, false_testcases[index2]);
  // 设置最大运行指令数并运行
  sim.setRunInstLimit(50000);
  bool success = sim.runUntilHalt();
  // 验证结果
  std::string prompt_success =
      "The program is expected to halt without any exception";
  std::string prompt_check = "Input is " +
                             std::string(false_testcases[index2]) +
                             ", output is expected to be 0";
  bool check = sim.readMem(0x3200) == 0;
  tester.verify(prompt_success, success, total_points * 1 / 5);
  tester.verify(prompt_check, check, total_points * 4 / 5);
  index2++;
}

void testBringup(lc3::sim &sim) {}

void testTeardown(lc3::sim &sim) {}

void setup(Tester &tester) {
  generate_testcases();
  tester.registerTest("Zero Test", ZeroTest, 8 * 0.8, false);
  tester.registerTest("Zero Test", ZeroTest, 8 * 0.2, true);
  tester.registerTest("Non-Stantard Input Test", NonStandardInputTest, 8 * 0.8,
                      false);
  tester.registerTest("Non-Stantard Input Test", NonStandardInputTest, 8 * 0.2,
                      true);
  for (int i = 0; i < N_SAMPLES / 2; i++) {
    tester.registerTest("True Test", TrueTest, 14 * 0.8, false);
    tester.registerTest("True Test", TrueTest, 14 * 0.2, true);
    tester.registerTest("False Test", FalseTest, 14 * 0.8, false);
    tester.registerTest("False Test", FalseTest, 14 * 0.2, true);
  }
}

void shutdown(void) {}
