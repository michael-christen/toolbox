#include "examples/basic/lib/hello-time.h"

#include <ctime>
#include <iostream>

#include <google/protobuf/util/json_util.h>

void print_localtime() {
  std::time_t result = std::time(nullptr);
  std::cout << std::asctime(std::localtime(&result));
}
