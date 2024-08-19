# gazelle:default_visibility //visibility:public
package(default_visibility = ["//visibility:public"])

cc_library(
    name = "module_config",
    defines = [
        # TODO: https://pwbug.dev/352389854 - Move this to per-platform config
        # when platform flags  are implemented.
        #
        # Allow us to capture two 64bit pointers in a pw::function.
        "PW_FUNCTION_INLINE_CALLABLE_SIZE=16UL",
        "PW_ASSERT_BASIC_ACTION=PW_ASSERT_BASIC_ACTION_EXIT",
    ],
    visibility = ["//visibility:public"],
)
