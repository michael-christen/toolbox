load("@aspect_rules_py//py:defs.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "pocket_export_html_to_csv",
    srcs = ["pocket_export_html_to_csv.py"],
    visibility = ["//:__subpackages__"],
    deps = ["@pip//beautifulsoup4"],
)

py_binary(
    name = "youtube_playlist_to_csv",
    srcs = ["youtube_playlist_to_csv.py"],
    visibility = ["//:__subpackages__"],
)
