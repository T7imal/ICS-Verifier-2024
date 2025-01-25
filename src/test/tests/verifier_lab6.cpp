#include <iostream>
#include <string>
#define API_VER 2
#include "framework.h"

std::string prompt_a = "Program A reporting.\n";
std::string prompt_b = "Program B reporting.\n";
// 三组连续的输出
std::string prompt_pattern = (prompt_a + prompt_b + prompt_b) +
                             (prompt_a + prompt_b + prompt_b) +
                             (prompt_a + prompt_b + prompt_b);

void test(lc3::sim &sim, Tester &tester, double total_points) {
  // 设置PC寄存器、需要的内存参数
  sim.writePC(0x200);
  // 设置最大运行指令数并运行
  sim.setRunInstLimit(300000);
  // 持续运行
  bool success = sim.run();
  // 获取输出
  std::string output = tester.getOutput();
  // 验证输出
  bool check = tester.checkContain(output, prompt_pattern);
  // 输出正确，获取4/5的分数
  tester.verify("Prompt Pattern", check, total_points * 4 / 5);
  // 输入Q/q，验证程序是否成功Halting
  tester.setInputString("Qq");
  success &= sim.run();
  tester.verify("Is Halting?", success, total_points * 1 / 5);
}

void testBringup(lc3::sim &sim) {}

void testTeardown(lc3::sim &sim) {}

void setup(Tester &tester) {
  tester.registerTest("Test", test, 80, false);
  tester.registerTest("Test", test, 20, true);
}

void shutdown(void) {}
