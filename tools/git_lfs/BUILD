sh_binary(
  name = "git_lfs_bin",
  srcs = ["@git_lfs//:file"],
)
sh_binary(
  name = "git_lfs",
  srcs = ["//tools:exec_change_cwd"],
  args = ["$(location :git_lfs_bin)"],
  data = [":git_lfs_bin"],
)
package(default_visibility = ["//visibility:private"])
