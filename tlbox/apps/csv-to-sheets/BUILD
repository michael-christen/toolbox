load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "csv2sheets",
    srcs = ["csv2sheets.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pip//gspread",
        "@pip//oauth2client",
    ],
)
