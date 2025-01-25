#include <cstdint>
#include <iostream>
#include <list>
#include <string>
#define API_VER 2
#include "framework.h"
#include <filesystem>

#define N_SAMPLES 100

int studentID = 0;
int key = 0;

// 在当前目录下寻找报告文件，从文件名中读取学号
int getStudentID() {
  for (const auto &entry : std::filesystem::directory_iterator(".")) {
    std::string filename = entry.path().filename().string();
    if (filename.find(".pdf") != std::string::npos) {
      int studentID = 0;
      bool flag = false;
      // 从文件名中读取学号，其为文件名中连续的数字
      for (int i = 0; i < filename.size(); i++) {
        if (filename[i] >= '0' && filename[i] <= '9') {
          studentID = studentID * 10 + filename[i] - '0';
          flag = true;
        } else if (flag) {
          break;
        }
      }
      return studentID;
    }
  }
  return 0;
}

// 根据学号计算密钥
uint16_t secretKey(int studentID) {
  std::list<int> list;
  while (studentID) {
    list.push_front((studentID % 10) % 2);
    studentID /= 10;
  }
  // 改写为二进制数
  int key = 0;
  for (int i : list) {
    key = key * 2 + i;
  }
  return key;
}

// 由于lab1只涉及寄存器操作，因此不重置测试机，直接重置PC寄存器、设置输入寄存器、
// 设置其他寄存器为0，在同一次测试中递增输入寄存器，且不执行HALT指令
void test(lc3::sim &sim, Tester &tester, double total_points) {
  for (int i = -50; i < -50 + N_SAMPLES; i++) {
    // 设置PC寄存器、需要的寄存器参数
    sim.writePC(0x3000);
    sim.writeReg(0, uint16_t(i));

    // 设置最大运行指令数并运行
    sim.setRunInstLimit(5000);
    bool success = sim.runUntilHalt();

    // 验证结果
    std::string prompt_success =
        "The program is expected to halt without any exception";
    std::string prompt_check = "Input is " + std::to_string(uint16_t(i)) +
                               ", output is expected to be " +
                               std::to_string(key ^ uint16_t(i));
    bool check = sim.readReg(3) == (key ^ uint16_t(i));
    tester.verify(prompt_success, success, total_points / N_SAMPLES * 1 / 5);
    tester.verify(prompt_check, check, total_points / N_SAMPLES * 4 / 5);
  }
}

void test_nonrandom(lc3::sim &sim, Tester &tester, double total_points) {
  for (int i = -50; i < -50 + N_SAMPLES; i++) {
    // 重置寄存器为0
    for (int j = 0; j < 8; j++) {
      sim.writeReg(j, 0);
    }

    // 设置PC寄存器、需要的寄存器参数
    sim.writePC(0x3000);
    sim.writeReg(0, uint16_t(i));

    // 设置最大运行指令数并运行
    sim.setRunInstLimit(5000);
    bool success = sim.runUntilHalt();

    // 验证结果
    std::string prompt_success =
        "The program is expected to halt without any exception";
    std::string prompt_check = "Input is " + std::to_string(uint16_t(i)) +
                               ", output is expected to be " +
                               std::to_string(key ^ uint16_t(i));
    bool check = sim.readReg(3) == (key ^ uint16_t(i));
    tester.verify(prompt_success, success, total_points / N_SAMPLES * 1 / 5);
    tester.verify(prompt_check, check, total_points / N_SAMPLES * 4 / 5);
  }
}

void testBringup(lc3::sim &sim) {}

void testTeardown(lc3::sim &sim) {}

void setup(Tester &tester) {
  studentID = getStudentID();
  key = secretKey(studentID);
  tester.registerTest("test", test_nonrandom, 80, false);
  tester.registerTest("test", test, 20, true);
}

void shutdown(void) {}
