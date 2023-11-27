#include <iostream>
#include <string>

#include "examples/basic/app/hello-greet.h"
#include "examples/basic/hello.pb.h"
#include "examples/basic/lib/hello-time.h"

int main(int argc, char** argv) {
  experiments::proto::hello::Hello msg;
  msg.set_id(4);
  std::string who = "world";
  if (argc > 1) {
    who = argv[1];
  }
  std::cout << get_greet(who) << " " << msg.DebugString() << std::endl;
  print_localtime();
  return 0;
}
