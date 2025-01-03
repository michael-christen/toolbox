load("@aspect_bazel_lib//lib:tar.bzl", "mtree_spec", "tar")
load("@aspect_bazel_lib//lib:transitions.bzl", "platform_transition_filegroup")

# XXX: Move to tools/rules/python defs.bzl
load("@aspect_rules_py//py:defs.bzl", _py_binary = "py_binary", _py_library = "py_library")
load("@build_stack_rules_proto//rules/py:grpc_py_library.bzl", _grpc_py_library = "grpc_py_library")
load("@build_stack_rules_proto//rules/py:proto_py_library.bzl", _proto_py_library = "proto_py_library")
load("@rules_oci//oci:defs.bzl", "oci_image", "oci_tarball")

# TODO(#52): Add aspect_rules_py back for py_test
load("@rules_python//python:defs.bzl", _py_test = "py_test")

def py_binary(**kwargs):
    _py_binary(**kwargs)

def py_library(**kwargs):
    _py_library(**kwargs)

def py_test(srcs, deps = [], args = [], data = [], timeout = "short", **kwargs):
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
        timeout = timeout,
        **kwargs
    )

def grpc_py_library(tags = [], **kwargs):
    # Don't evaluate mypy on this library
    new_tags = ["no-mypy"]
    _grpc_py_library(tags = tags + new_tags, **kwargs)

def proto_py_library(srcs = [], tags = [], data = [], **kwargs):
    # Add .pyi as a data dependency
    new_data = []
    for src in srcs:
        new_data.append("{}i".format(src))

    # Don't evaluate mypy on this library
    new_tags = ["no-mypy"]
    _proto_py_library(srcs = srcs, tags = tags + new_tags, data = data + new_data, **kwargs)

def _py_layers(name, binary):
    """
    Create three layers for a py_binary target: interpreter, third-party dependencies, and application code.

    This allows a container image to have smaller uploads, since the application layer usually changes more
    than the other two.

    Args:
        name: Prefix for generated targets, to ensure they are unique within the package.
        binary: The name of the py_binary to bundle in the container.

    Returns:
        A list of labels for the layers, which are tar files
    """

    # Produce layers in this order, as the app changes most often
    layers = ["interpreter", "packages", "app"]

    # Produce the manifest for a tar file of our py_binary, but don't tar it up yet, so we can split
    # into fine-grained layers for better docker performance.
    mtree_spec(
        name = name + ".mf",
        srcs = [binary],
    )

    # match *only* external repositories that have the string "python"
    # e.g. this will match
    #   `/hello_world/hello_world_bin.runfiles/rules_python~0.21.0~python~python3_9_aarch64-unknown-linux-gnu/bin/python3`
    # but not match
    #   `/hello_world/hello_world_bin.runfiles/_main/python_app`
    PY_INTERPRETER_REGEX = "\\.runfiles/.*python.*-.*"

    # match *only* external pip like repositories that contain the string "site-packages"
    SITE_PACKAGES_REGEX = "\\.runfiles/.*/site-packages/.*"

    native.genrule(
        name = name + ".interpreter_tar_manifest",
        srcs = [name + ".mf"],
        outs = [name + ".interpreter_tar_manifest.spec"],
        cmd = "grep '{}' $< >$@".format(PY_INTERPRETER_REGEX),
    )

    native.genrule(
        name = name + ".packages_tar_manifest",
        srcs = [name + ".mf"],
        outs = [name + ".packages_tar_manifest.spec"],
        cmd = "grep '{}' $< >$@".format(SITE_PACKAGES_REGEX),
    )

    # Any lines that didn't match one of the two grep above
    native.genrule(
        name = name + ".app_tar_manifest",
        srcs = [name + ".mf"],
        outs = [name + ".app_tar_manifest.spec"],
        cmd = "grep -v '{}' $< | grep -v '{}' >$@".format(SITE_PACKAGES_REGEX, PY_INTERPRETER_REGEX),
    )

    result = []
    for layer in layers:
        layer_target = "{}.{}_layer".format(name, layer)
        result.append(layer_target)
        tar(
            name = layer_target,
            srcs = [binary],
            mtree = "{}.{}_tar_manifest".format(name, layer),
        )

    return result

def py_image(name, binary, image_tags, tars = [], base = None, entrypoint = None, **kwargs):
    """
    A macro that generates an OCI container image to run a py_binary target.

    The created target can be passed on to anything that expects an oci_image target, such as `oci_push`.

    An implicit `oci_tarball` target is created for the image in question, which can be used to load
    this image into a running docker daemon automatically for testing. This is named `name + "_load_docker"`.

        ```sh
        bazel run //path/to:<my_oci_image>_load_docker
        ```

    Args:
        name: A unique name for this target.
        binary: The name of the py_binary to bundle in the container.
        image_tags: A list of tags to apply to the image.
        tars: A list of additional tar files to include in the image.
        base: The base image to use for the container. If not provided, the default is "@python_base".
        entrypoint: The entrypoint for the container. If not provided, it is inferred from the binary.
        **kwargs: are passed to oci_image

    Example:
        py_image(
            name = "my_oci_image",
            binary = "//path/to:my_py_binary",
            tars = ["//path/to:my_extra_tar"],
            base = "@python_base",
            entrypoint = ["/my_py_binary/my_py_binary"],
            image_tags = ["my-tag:latest"],
        )
    """

    base = base or "@ubuntu_base"

    # If the user didn't provide an entrypoint, infer the one for the binary
    bin_name = binary.split(":")[1]
    workspace_path = ""
    if binary.startswith("//"):
        workspace_path = binary.split(":")[0][2:]
    else:
        workspace_path = native.package_name()

    # TODO: Once aspect-build/rules_py#229 makes it into a rules_py release, we can use the
    # entrypoint directly without this `bash <entrypoint>` workaround.
    entrypoint = entrypoint or ["bash", "/{}/{}".format(workspace_path, bin_name)]

    # Define the image we want to provide
    oci_image(
        name = name + "_base_img",
        tars = tars + _py_layers(name, binary),
        base = base,
        entrypoint = entrypoint,
        **kwargs
    )

    # Transition the image to the platform we're building for
    platform_transition_filegroup(
        name = name,
        srcs = [name + "_base_img"],
        target_platform = select({
            "@platforms//cpu:arm64": "//tools/platforms:container_aarch64_linux",
            "@platforms//cpu:x86_64": "//tools/platforms:container_x86_64_linux",
        }),
    )

    # Create a tarball that can be loaded into a docker daemon
    oci_tarball(
        name = name + "_load_docker",
        image = name,
        repo_tags = image_tags,
    )
