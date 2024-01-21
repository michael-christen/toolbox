load("@rules_python//python:defs.bzl", "py_library")
load("@aspect_rules_py//py:defs.bzl", "py_binary")

py_binary(
    name = "pocket_export_html_to_csv_bin",
    srcs = ["pocket_export_html_to_csv.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pip//beautifulsoup4"],
)

py_binary(
    name = "youtube_playlist_to_csv_bin",
    srcs = ["youtube_playlist_to_csv.py"],
    visibility = ["//:__subpackages__"],
)

package(default_visibility = ["//visibility:private"])
