load("//bzl:py.bzl", "py_binary")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "gmail_analysis",
    srcs = ["gmail_analysis.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@toolbox_pip//google_api_python_client",
        "@toolbox_pip//google_auth",
        "@toolbox_pip//google_auth_oauthlib",
        "@toolbox_pip//matplotlib",
        "@toolbox_pip//pandas",
    ],
)
