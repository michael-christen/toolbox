# Copyright 2024 The Pigweed Authors
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

# Don't autogenerate any protos here
# gazelle:ignore
load("@pigweed//pw_build:pigweed.bzl", "pw_cc_test")
load(
    "@pigweed//pw_protobuf_compiler:pw_proto_library.bzl",
    "nanopb_proto_library",
    "nanopb_rpc_proto_library",
)
load("@rules_python//python:proto.bzl", "py_proto_library")

package(default_visibility = ["//visibility:public"])

filegroup(
    name = "python_source",
    srcs = glob(
        ["*.py"],
        allow_empty = True,
    ) + [
    ],
    visibility = ["//visibility:public"],
)

cc_library(
    name = "blinky",
    srcs = ["blinky.cc"],
    hdrs = ["blinky.h"],
    implementation_deps = [
        "@pigweed//pw_log",
        "@pigweed//pw_preprocessor",
    ],
    deps = [
        "//examples/pigweed/apps/blinky/system",
        "//examples/pigweed/modules/timer_future",
        "@pigweed//pw_async2:coro",
        "@pigweed//pw_async2:coro_or_else_task",
        "@pigweed//pw_async2:dispatcher",
        "@pigweed//pw_chrono:system_clock",
        "@pigweed//pw_function",
        "@pigweed//pw_sync:interrupt_spin_lock",
        "@pigweed//pw_sync:lock_annotations",
        "@pigweed//pw_system:async",
    ],
)

pw_cc_test(
    name = "blinky_test",
    srcs = ["blinky_test.cc"],
    deps = [
        ":blinky",
        "@pigweed//pw_allocator:testing",
        "@pigweed//pw_async2:dispatcher",
        "@pigweed//pw_digital_io:digital_io_mock",
        "@pigweed//pw_thread:sleep",
        "@pigweed//pw_unit_test",
    ],
    # XXX: Make a macro for this?
    timeout="short",
)

cc_library(
    name = "service",
    srcs = ["service.cc"],
    hdrs = ["service.h"],
    deps = [
        ":blinky",
        ":nanopb_rpc",
        "@pigweed//pw_allocator:allocator",
        "@pigweed//pw_assert:check",
        "@pigweed//pw_async2:dispatcher",
    ],
)

proto_library(
    name = "blinky_proto",
    srcs = ["blinky.proto"],
    deps = [
        "@pigweed//pw_protobuf:common_proto",
    ],
)

nanopb_proto_library(
    name = "nanopb",
    deps = [":blinky_proto"],
)

nanopb_rpc_proto_library(
    name = "nanopb_rpc",
    nanopb_proto_library_deps = [":nanopb"],
    deps = [":blinky_proto"],
)

py_proto_library(
    name = "blinky_pb2",
    deps = [":blinky_proto"],
)
