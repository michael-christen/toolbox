#include "examples/basic/lib/hello-time.h"

#include <ctime>
#include <iostream>

#include "pw_containers/vector.h"

void print_localtime() {
  std::time_t result = std::time(nullptr);
  std::cout << std::asctime(std::localtime(&result));
}
