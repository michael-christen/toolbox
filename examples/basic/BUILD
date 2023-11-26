load("@crate_index//:defs.bzl", "aliases", "all_crate_deps")
load("@rules_rust//rust:defs.bzl", "rust_binary", "rust_doc")

package(default_visibility = ["//visibility:public"])

rust_binary(
    name = "hello_world",
    srcs = ["src/main.rs"],
    aliases=aliases(),
    deps = [
      "@crate_index//:ferris-says",
    ],
    # XXX: Not getting to work ...
    # deps = all_crate_deps(),
    # proc_macro_deps = all_crate_deps(
    #     proc_macro = True,
    # ),
)

rust_doc(
    name = "hello_world_doc",
    crate = ":hello_world",
)
