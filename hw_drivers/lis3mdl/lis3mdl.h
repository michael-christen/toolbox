#pragma once

#include "hw_drivers/lis3mdl/lis3mdl.emb.h"
#include "hw_drivers/lis3mdl/lis3mdl.pb.h"

namespace hw_drivers {
namespace lis3mdl {


// XXX:
// - "solve" configuration and test that
// - function to go from configuration to ControlView
//   - maybe include in same thing
//
// - function to compute reading based on settings and DataView
// - maybe start math functions to handle these
//
// - [ ] may be try to detect bounding issue if not "locked"


// XXX: Setup error result support ...
LIS3MDLConfiguration SolveConfiguration(const LIS3MDLConfiguration& desired_configuration,
    ControlView* control);


class LIS3MDL {
  public:
};

}
}
