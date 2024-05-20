load("@aspect_rules_py//py:defs.bzl", _py_binary = "py_binary", _py_library = "py_library", _py_test = "py_test")
load("@build_stack_rules_proto//rules/py:grpc_py_library.bzl", _grpc_py_library = "grpc_py_library")
load("@build_stack_rules_proto//rules/py:proto_py_library.bzl", _proto_py_library = "proto_py_library")


def py_binary(**kwargs):
    _py_binary(**kwargs)


def py_library(**kwargs):
    _py_library(**kwargs)


def py_test(srcs, deps = [], args = [], data = [], **kwargs):
    deps = deps + [
        "@pip//pytest",
    ]
    unique_deps = {d: None for d in deps}

    _py_test(
        main = "//bzl:pytest_main.py",
        srcs = srcs + ["//bzl:pytest_main.py"],
        deps = unique_deps,
        args = args + [
            "--import-mode=importlib",
            "--config-file=$(location //:pytest.ini)",
        ] + ["$(location :%s)" % s for s in srcs],
        data = data + ["//:pytest.ini"],
        **kwargs,
    )


def grpc_py_library(**kwargs):
    _grpc_py_library(**kwargs)


def proto_py_library(**kwargs):
    _proto_py_library(**kwargs)