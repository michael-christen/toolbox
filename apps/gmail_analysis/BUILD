load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "gmail_analysis",
    srcs = ["gmail_analysis.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pip//google_api_python_client",
        "@pip//google_auth",
        "@pip//google_auth_oauthlib",
        "@pip//matplotlib",
        "@pip//pandas",
    ],
)
