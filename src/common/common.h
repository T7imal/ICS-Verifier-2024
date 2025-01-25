/*
 * Copyright 2020 McGraw-Hill Education. All rights reserved. No reproduction or distribution without the prior written consent of McGraw-Hill Education.
 */
#ifndef COMMON_H
#define COMMON_H

#if __cplusplus >= 201103L
#include <cstdint>
#endif
#include <string>
#include <vector>

std::vector<std::pair<std::string, std::string>> parseCLIArgs(int argc, char * argv[]);

#endif
