#include "hw_drivers/lis3mdl/lis3mdl.h"

#include <chrono>
#include <cstdint>
#include <vector>

#include "pw_bytes/array.h"
#include "pw_i2c/address.h"
#include "pw_i2c/initiator_mock.h"
#include "pw_result/result.h"
#include "pw_unit_test/framework.h"

#include "hw_drivers/lis3mdl/lis3mdl.emb.h"
#include "hw_drivers/lis3mdl/lis3mdl.pb.h"


using namespace std::chrono_literals;

namespace hw_drivers {
namespace lis3mdl {

namespace {

TEST(I2CTestSuite, I2CTransactions) {
  constexpr pw::i2c::Address kAddress =
  pw::i2c::Address::SevenBit<0x01>(); constexpr auto kExpectedWrite =
  pw::bytes::Array<1, 2, 3>(); auto expected_transactions =
  pw::i2c::MakeExpectedTransactionArray(
    {pw::i2c::WriteTransaction(pw::OkStatus(), kAddress, kExpectedWrite,
    1ms)}
  );
  pw::i2c::MockInitiator initiator(expected_transactions);
  pw::ConstByteSpan kActualWrite = pw::bytes::Array<1, 2, 3>();
  pw::Status status = initiator.WriteFor(kAddress, kActualWrite, 1ms);
  EXPECT_EQ(status, pw::OkStatus());
  EXPECT_EQ(status.code(), 0);
  EXPECT_EQ(initiator.Finalize(), pw::OkStatus());
}

}

}
}
