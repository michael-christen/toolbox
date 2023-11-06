#include <iostream>
#include <string>

#include "experiments/cpp/hello/lib/hello-time.h"
#include "experiments/cpp/hello/main/hello-greet.h"
#include "experiments/proto/hello/hello.pb.h"

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
