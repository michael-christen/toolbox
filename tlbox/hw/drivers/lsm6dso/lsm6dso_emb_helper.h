#pragma once

#include <array>

#include "tlbox/hw/drivers/lsm6dso/lsm6dso.emb.h"

namespace hw_drivers {
namespace lsm6dso {

// Thin wrapper around lsm6dso.emb.h Data to own the data
struct Lsm6dsoEmbHelper {
 public:
  std::array<std::byte, Data::MaxSizeInBytes()> bytes{std::byte{0}};
};

}
}
