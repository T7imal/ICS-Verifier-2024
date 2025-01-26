#include <iostream>
#include <string>
#define API_VER 2
#include "framework.h"

#define N_SAMPLES 50

// 测试函数
int compute(int a0) {
  if (a0 < 0) {
    return -1;
  }

  int ans = 0;
  while (a0 != 1 || ans == 0) {
    if (a0 % 2 == 0) {
      a0 = a0 / 2;
    } else {
      a0 = 3 * a0 + 1;
    }
    ans++;
  }
  return ans;
}

void test(lc3::sim &sim, Tester &tester, double total_points) {
  for (int i = 1; i < 1 + N_SAMPLES; i++) {
    int a0 = i;
    int expected = compute(a0);

    // 设置PC寄存器、需要的寄存器参数
    sim.writePC(0x3000);
    sim.writeMem(0x3100, a0);

    // 设置最大运行指令数并运行
    sim.setRunInstLimit(1000000);
    bool success = sim.runUntilHalt();

    // 验证输出、验证成功Halting
    std::string prompt_success =
        "The program is expected to halt without any exception";
    std::string prompt_check = "Input is " + std::to_string(a0) +
                               ", output is expected to be " +
                               std::to_string(expected);
    bool check = sim.readMem(0x3101) == expected;
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

    int a0 = i;
    int expected = compute(a0);

    // 设置PC寄存器、需要的寄存器参数
    sim.writePC(0x3000);
    sim.writeMem(0x3100, a0);

    // 设置最大运行指令数并运行
    sim.setRunInstLimit(1000000);
    bool success = sim.runUntilHalt();

    // 验证输出、验证成功Halting
    std::string prompt_success =
        "The program is expected to halt without any exception";
    std::string prompt_check = "Input is " + std::to_string(a0) +
                               ", output is expected to be " +
                               std::to_string(expected);
    bool check = sim.readMem(0x3101) == expected;
    tester.verify(prompt_success, success, total_points / N_SAMPLES * 1 / 5);
    tester.verify(prompt_check, check, total_points / N_SAMPLES * 4 / 5);
  }
}

void testBringup(lc3::sim &sim) {}

void testTeardown(lc3::sim &sim) {}

void setup(Tester &tester) {
  tester.registerTest("Test", test_nonrandom, 80, false);
  tester.registerTest("Test", test, 20, true);
}

void shutdown(void) {}
