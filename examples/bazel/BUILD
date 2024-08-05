load(":foo.bzl", "foo_binary", "hello_world")
load(":file_count.bzl", "file_count_rule")

print("BUILD file")
foo_binary(name = "bin1", username = "Alice")
foo_binary(name = "bin2", username = "Bob")

hello_world(
    name = "hello",
    username = "Alice",
    template = "file.cc.tpl",
)

cc_binary(
    name = "hello_bin",
    srcs = [":hello"],
)

# Make it visible and accessible
exports_files(["file.cc.tpl"])

cc_library(
    name = 'lib',
    srcs = [
        'lib.h',
        'lib.cc',
    ],
)

cc_binary(
    name = 'app',
    srcs = [
        'app.h',
        'app.cc',
        'main.cc',
    ],
    deps = ['lib'],
)

file_count_rule(
    name = 'file_count',
    deps = ['app'],
    extension = 'h',
)
