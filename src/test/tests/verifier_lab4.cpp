#include <iostream>
#define API_VER 2
#include "framework.h"

#define N_SAMPLES 10

int earn_array[30];
int spend_array[30];
int savings_array[30];

// 测试函数
int earn(int n) {
  if (earn_array[n] != -1) {
    return earn_array[n];
  }
  if (n == 0) {
    earn_array[n] = 6;
  } else {
    earn_array[n] = earn(n - 1) * 2;
  }
  return earn_array[n];
}

int spend(int n) {
  if (spend_array[n] != -1) {
    return spend_array[n];
  }
  if (n == 0) {
    spend_array[n] = 2;
  } else if (spend(n - 1) >= earn(n - 1)) {
    spend_array[n] = 2;
  } else {
    spend_array[n] = spend(n - 1) * 4;
  }
  return spend_array[n];
}

int savings(int n) {
  if (savings_array[n] != -1) {
    return savings_array[n];
  }
  if (n == 0) {
    savings_array[n] = 10;
  } else {
    savings_array[n] = savings(n - 1) + earn(n - 1) - spend(n - 1);
  }
  return savings_array[n];
}

void test(lc3::sim &sim, Tester &tester, double total_points) {
  for (int i = 1; i < 1 + N_SAMPLES; i++) {
    // 记录运行指令数
    int before = sim.getInstExecCount();

    int input = i;
    // 设置PC寄存器、需要的内存参数
    sim.writePC(0x3000);
    sim.writeMem(0x3100, input);
    // 设置最大运行指令数并运行
    sim.setRunInstLimit(50000);
    bool success = sim.runUntilHalt();

    // 检查指令数
    int after = sim.getInstExecCount();
    // bool is_inefficient = false;
    // if (after - before >= 50000) {
    //   is_inefficient = true;
    // }

    // 验证结果
    std::string prompt_success =
        "The program is expected to halt without any exception";
    std::string prompt_check = "Input is " + std::to_string(input) +
                               ", output is expected to be " +
                               std::to_string(savings(input));
    bool check = sim.readMem(0x3200) == savings(input);
    tester.verify(prompt_success, success, total_points / N_SAMPLES * 1 / 5);
    tester.verify(prompt_check, check, total_points / N_SAMPLES * 4 / 5);
  }
}

void test_nonrandom(lc3::sim &sim, Tester &tester, double total_points) {
  for (int i = 1; i < 1 + N_SAMPLES; i++) {
    // 重置寄存器为0
    for (int j = 0; j < 8; j++) {
      sim.writeReg(j, 0);
    }

    // 记录运行指令数
    int before = sim.getInstExecCount();

    int input = i;
    // 设置PC寄存器、需要的内存参数
    sim.writePC(0x3000);
    sim.writeMem(0x3100, input);
    // 设置最大运行指令数并运行
    sim.setRunInstLimit(50000);
    bool success = sim.runUntilHalt();

    // 检查指令数
    int after = sim.getInstExecCount();
    // bool is_inefficient = false;
    // if (after - before >= 50000) {
    //   is_inefficient = true;
    // }

    // 验证结果
    std::string prompt_success =
        "The program is expected to halt without any exception";
    std::string prompt_check = "Input is " + std::to_string(input) +
                               ", output is expected to be " +
                               std::to_string(savings(input));
    bool check = sim.readMem(0x3200) == savings(input);
    tester.verify(prompt_success, success, total_points / N_SAMPLES * 1 / 5);
    tester.verify(prompt_check, check, total_points / N_SAMPLES * 4 / 5);
  }
}

void testBringup(lc3::sim &sim) {}

void testTeardown(lc3::sim &sim) {}

void setup(Tester &tester) {
  for (int i = 0; i < 30; i++) {
    earn_array[i] = -1;
    spend_array[i] = -1;
    savings_array[i] = -1;
  }
  tester.registerTest("Test", test_nonrandom, 80, false);
  tester.registerTest("Test", test, 20, true);
}

void shutdown(void) {}
