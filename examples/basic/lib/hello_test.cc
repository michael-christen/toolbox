#include <gtest/gtest.h>

unsigned int Factorial(unsigned int number) {
  return number <= 1 ? number : Factorial(number - 1) * number;
}

TEST(FactorialTest, BasicCases) {
  EXPECT_EQ(Factorial(1), 1u);
  EXPECT_EQ(Factorial(2), 2u);
  EXPECT_EQ(Factorial(3), 6u);
  EXPECT_EQ(Factorial(10), 3628800u);
}
