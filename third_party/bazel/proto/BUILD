load("@build_stack_rules_proto//rules/cc:proto_cc_library.bzl", "proto_cc_library")
load("@build_stack_rules_proto//rules:proto_compile.bzl", "proto_compile")
load("//bzl:py.bzl", "grpc_py_library", "proto_py_library")
load("@io_bazel_rules_go//proto:compiler.bzl", "go_proto_compiler")
load("@io_bazel_rules_go//proto:def.bzl", "go_proto_library")
load("@rules_proto//proto:defs.bzl", "proto_library")
load(":defs.bzl", "ts_proto_library")

package(default_visibility = ["//visibility:private"])

go_proto_compiler(
    name = "vtprotobuf_compiler",
    # marshal depends on size. Pool only generates code for messages with the
    # vtprotobuf mempool annotation.
    options = ["features=marshal+unmarshal+size+pool+clone"],
    plugin = "@com_github_planetscale_vtprotobuf//cmd/protoc-gen-go-vtproto",
    suffix = "_vtproto.pb.go",
    valid_archive = False,
    deps = [
        "@com_github_planetscale_vtprotobuf//protohelpers",
        "@com_github_planetscale_vtprotobuf//types/known/anypb",
        "@com_github_planetscale_vtprotobuf//types/known/durationpb",
        "@com_github_planetscale_vtprotobuf//types/known/emptypb",
        "@com_github_planetscale_vtprotobuf//types/known/fieldmaskpb",
        "@com_github_planetscale_vtprotobuf//types/known/structpb",
        "@com_github_planetscale_vtprotobuf//types/known/timestamppb",
        "@com_github_planetscale_vtprotobuf//types/known/wrapperspb",
    ],
)

proto_library(
    name = "acl_proto",
    srcs = ["acl.proto"],
    deps = [
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "action_cache_proto",
    srcs = ["action_cache.proto"],
)

proto_library(
    name = "api_key_proto",
    srcs = ["api_key.proto"],
    deps = [
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "auditlog_proto",
    srcs = [
        "auditlog.proto",
    ],
    deps = [
        "//proto:proto_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

proto_library(
    name = "auth_proto",
    srcs = ["auth.proto"],
)

proto_library(
    name = "bazel_query_proto",
    srcs = ["bazel_query.proto"],
)

proto_library(
    name = "build_status_proto",
    srcs = [
        "build_status.proto",
    ],
    deps = [
        "@com_google_protobuf//:any_proto",
        "@com_google_protobuf//:wrappers_proto",
    ],
)

proto_library(
    name = "build_events_proto",
    srcs = [
        "build_events.proto",
    ],
    deps = [
        "//proto:proto_proto",
        "@com_google_protobuf//:any_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

proto_library(
    name = "cache_proto",
    srcs = [
        "cache.proto",
    ],
    deps = [
        "//google/rpc:rpc_proto",
        "//proto:proto_proto",
        "@com_google_protobuf//:duration_proto",
        "@com_google_protobuf//:field_mask_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

proto_library(
    name = "certgenerator_proto",
    srcs = [
        "certgenerator.proto",
    ],
)

proto_library(
    name = "config_proto",
    srcs = [
        "config.proto",
    ],
)

proto_library(
    name = "server_notification_proto",
    srcs = [
        "server_notification.proto",
    ],
)

proto_library(
    name = "distributed_cache_proto",
    srcs = [
        "distributed_cache.proto",
    ],
    deps = [
        "//github.com/planetscale/vtprotobuf/vtproto:vtproto_proto",
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "resource_proto",
    srcs = [
        "resource.proto",
    ],
    deps = [
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "execution_stats_proto",
    srcs = [
        "execution_stats.proto",
    ],
    deps = [
        "//google/longrunning:longrunning_proto",
        "//google/rpc:rpc_proto",
        "//proto:proto_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

proto_library(
    name = "failure_details_proto",
    srcs = [
        "failure_details.proto",
    ],
    deps = [
        "@com_google_protobuf//:descriptor_proto",
    ],
)

proto_library(
    name = "firecracker_proto",
    srcs = ["firecracker.proto"],
    deps = [
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "git_proto",
    srcs = ["git.proto"],
)

proto_library(
    name = "github_proto",
    srcs = ["github.proto"],
    deps = ["//proto:proto_proto"],
)

proto_library(
    name = "gcp_proto",
    srcs = ["gcp.proto"],
    deps = ["//proto:proto_proto"],
)

proto_library(
    name = "package_load_metrics_proto",
    srcs = ["package_load_metrics.proto"],
    deps = [
        "@com_google_protobuf//:duration_proto",
    ],
)

proto_library(
    name = "pagination_proto",
    srcs = ["pagination.proto"],
)

proto_library(
    name = "quota_proto",
    srcs = ["quota.proto"],
    deps = [
        "//proto:proto_proto",
        "@com_google_protobuf//:duration_proto",
    ],
)

proto_library(
    name = "publish_build_event_proto",
    srcs = [
        "publish_build_event.proto",
    ],
    deps = [
        "//google/api:api_proto",
        "//proto:proto_proto",
        "@com_google_protobuf//:duration_proto",
        "@com_google_protobuf//:empty_proto",
    ],
)

proto_library(
    name = "raft_proto",
    srcs = [
        "raft.proto",
    ],
    deps = [
        "//github.com/planetscale/vtprotobuf/vtproto:vtproto_proto",
        "//google/rpc:rpc_proto",
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "secrets_proto",
    srcs = ["secrets.proto"],
    deps = [
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "soci_proto",
    srcs = [
        "soci.proto",
    ],
    deps = ["//proto:proto_proto"],
)

proto_library(
    name = "spawn_proto",
    srcs = ["spawn.proto"],
    deps = [
        "@com_google_protobuf//:duration_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

proto_library(
    name = "spawn_diff_proto",
    srcs = ["spawn_diff.proto"],
    deps = [
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "stat_filter_proto",
    srcs = ["stat_filter.proto"],
    deps = [
        "//proto:proto_proto",
        "@com_google_protobuf//:descriptor_proto",
    ],
)

proto_library(
    name = "stats_proto",
    srcs = ["stats.proto"],
    deps = [
        "//proto:proto_proto",
        "@com_google_protobuf//:duration_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

proto_library(
    name = "target_proto",
    srcs = [
        "target.proto",
    ],
    deps = [
        "//proto:proto_proto",
        "//proto/api/v1:v1_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

proto_library(
    name = "target_pagination_proto",
    srcs = [
        "target_pagination.proto",
    ],
)

proto_library(
    name = "usage_proto",
    srcs = [
        "usage.proto",
    ],
    deps = [
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "eventlog_proto",
    srcs = [
        "eventlog.proto",
    ],
    deps = [
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "workflow_proto",
    srcs = [
        "workflow.proto",
    ],
    deps = [
        "//google/rpc:rpc_proto",
        "//proto:proto_proto",
        "@com_google_protobuf//:duration_proto",
    ],
)

proto_library(
    name = "workspace_proto",
    srcs = [
        "workspace.proto",
    ],
    deps = ["//proto:proto_proto"],
)

proto_library(
    name = "runner_proto",
    srcs = [
        "runner.proto",
    ],
    deps = ["//proto:proto_proto"],
)

proto_library(
    name = "vmexec_proto",
    srcs = ["vmexec.proto"],
    deps = [
        "//google/rpc:rpc_proto",
        "//proto:proto_proto",
        "@com_google_protobuf//:duration_proto",
    ],
)

proto_library(
    name = "vmvfs_proto",
    srcs = ["vmvfs.proto"],
    deps = ["//proto:proto_proto"],
)

proto_library(
    name = "vfs_proto",
    srcs = ["vfs.proto"],
)

proto_library(
    name = "build_event_stream_proto",
    srcs = ["build_event_stream.proto"],
    deps = [
        "//proto:proto_proto",
        "@com_google_protobuf//:any_proto",
        "@com_google_protobuf//:duration_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

proto_library(
    name = "invocation_policy_proto",
    srcs = ["invocation_policy.proto"],
    deps = [
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "strategy_policy_proto",
    srcs = ["strategy_policy.proto"],
)

proto_library(
    name = "command_line_proto",
    srcs = ["command_line.proto"],
    deps = [
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "option_filters_proto",
    srcs = ["option_filters.proto"],
)

proto_library(
    name = "invocation_proto",
    srcs = ["invocation.proto"],
    deps = [
        "//proto:proto_proto",
        "@com_google_protobuf//:duration_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

proto_library(
    name = "invocation_status_proto",
    srcs = ["invocation_status.proto"],
)

proto_library(
    name = "iprules_proto",
    srcs = ["iprules.proto"],
    deps = [
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "user_proto",
    srcs = ["user.proto"],
    exports = [":user_id_proto"],
    deps = ["//proto:proto_proto"],
)

proto_library(
    name = "user_id_proto",
    srcs = ["user_id.proto"],
)

proto_library(
    name = "group_proto",
    srcs = [
        "grp.proto",
    ],
    deps = ["//proto:proto_proto"],
)

proto_library(
    name = "context_proto",
    srcs = ["context.proto"],
    deps = [
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "raft_service_proto",
    srcs = ["raft_service.proto"],
    deps = [
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "ping_service_proto",
    srcs = ["ping_service.proto"],
)

proto_library(
    name = "buildbuddy_service_proto",
    srcs = ["buildbuddy_service.proto"],
    deps = ["//proto:proto_proto"],
)

proto_library(
    name = "semver_proto",
    srcs = ["semver.proto"],
)

proto_library(
    name = "sidecar_proto",
    srcs = ["sidecar.proto"],
)

proto_library(
    name = "repo_proto",
    srcs = ["repo.proto"],
    deps = [
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "registry_proto",
    srcs = ["registry.proto"],
    deps = ["//proto:proto_proto"],
)

proto_library(
    name = "remote_asset_proto",
    srcs = ["remote_asset.proto"],
    deps = [
        "//google/api:api_proto",
        "//google/rpc:rpc_proto",
        "//proto:proto_proto",
        "@com_google_protobuf//:duration_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

proto_library(
    name = "remote_execution_log_proto",
    srcs = ["remote_execution_log.proto"],
    deps = [
        "//google/bytestream:bytestream_proto",
        "//google/longrunning:longrunning_proto",
        "//google/rpc:rpc_proto",
        "//proto:proto_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

proto_library(
    name = "remote_execution_proto",
    srcs = ["remote_execution.proto"],
    deps = [
        "//google/api:api_proto",
        "//google/longrunning:longrunning_proto",
        "//google/rpc:rpc_proto",
        "//proto:proto_proto",
        "@com_google_protobuf//:any_proto",
        "@com_google_protobuf//:duration_proto",
        "@com_google_protobuf//:timestamp_proto",
        "@com_google_protobuf//:wrappers_proto",
    ],
)

proto_library(
    name = "execution_graph_proto",
    srcs = [
        "execution_graph.proto",
    ],
)

proto_library(
    name = "bazel_config_proto",
    srcs = ["bazel_config.proto"],
    deps = ["//proto:proto_proto"],
)

proto_library(
    name = "telemetry_proto",
    srcs = ["telemetry.proto"],
    deps = [
        "//google/rpc:rpc_proto",
    ],
)

proto_library(
    name = "scheduler_proto",
    srcs = ["scheduler.proto"],
    deps = [
        "//google/rpc:rpc_proto",
        "//proto:proto_proto",
        "@com_google_protobuf//:duration_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

proto_library(
    name = "suggestion_proto",
    srcs = ["suggestion.proto"],
    deps = [
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "trace_proto",
    srcs = ["trace.proto"],
)

proto_library(
    name = "worker_proto",
    srcs = ["worker.proto"],
)

proto_library(
    name = "stored_invocation_proto",
    srcs = ["stored_invocation.proto"],
)

proto_library(
    name = "zip_proto",
    srcs = ["zip.proto"],
    deps = [
        "//github.com/planetscale/vtprotobuf/vtproto:vtproto_proto",
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "encryption_proto",
    srcs = ["encryption.proto"],
    deps = [
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "metrics_proto",
    srcs = ["metrics.proto"],
    deps = [
        "//io/prometheus/client:client_proto",
    ],
)

proto_library(
    name = "index_proto",
    srcs = ["index.proto"],
    deps = ["//proto:proto_proto"],
)

proto_library(
    name = "search_proto",
    srcs = ["search.proto"],
    deps = [
        "//kythe/proto:proto_proto",
        "//proto:proto_proto",
    ],
)

proto_library(
    name = "codesearch_service_proto",
    srcs = ["codesearch_service.proto"],
    deps = ["//proto:proto_proto"],
)

ts_proto_library(
    name = "kythe_common_ts_proto",
    proto = "@io_kythe//kythe/proto:common_proto",
    deps = [
        ":timestamp_ts_proto",
    ],
)

ts_proto_library(
    name = "kythe_graph_ts_proto",
    proto = "@io_kythe//kythe/proto:graph_proto",
    deps = [
        ":kythe_common_ts_proto",
    ],
)

ts_proto_library(
    name = "kythe_xref_ts_proto",
    proto = "@io_kythe//kythe/proto:xref_proto",
    deps = [
        ":kythe_common_ts_proto",
    ],
)

ts_proto_library(
    name = "kythe_identifier_ts_proto",
    proto = "@io_kythe//kythe/proto:identifier_proto",
)

ts_proto_library(
    name = "kythe_filetree_ts_proto",
    proto = "@io_kythe//kythe/proto:filetree_proto",
)

proto_library(
    name = "kythe_service_proto",
    srcs = ["kythe_service.proto"],
    deps = ["//kythe/proto:proto_proto"],
)

# Go proto rules below here
go_proto_library(
    name = "prometheus_client_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/prometheus/client_model/go",
    proto = "@com_github_prometheus_client_model//io/prometheus/client:io_prometheus_client_proto",
)

go_proto_library(
    name = "acl_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/acl",
    proto = ":acl_proto",
    deps = [
        ":user_id_go_proto",
    ],
)

go_proto_library(
    name = "action_cache_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/action_cache",
    proto = ":action_cache_proto",
)

go_proto_library(
    name = "api_key_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/api_key",
    proto = ":api_key_proto",
    deps = [
        ":context_go_proto",
    ],
)

go_proto_library(
    name = "auditlog_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/auditlog",
    proto = ":auditlog_proto",
    deps = [
        ":api_key_go_proto",
        ":context_go_proto",
        ":encryption_go_proto",
        ":github_go_proto",
        ":group_go_proto",
        ":invocation_go_proto",
        ":iprules_go_proto",
        ":secrets_go_proto",
        ":workflow_go_proto",
    ],
)

go_proto_library(
    name = "auth_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/auth",
    proto = ":auth_proto",
)

go_proto_library(
    name = "bazel_query_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/bazel_query",
    proto = ":bazel_query_proto",
)

go_proto_library(
    name = "build_status_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/build_status",
    proto = ":build_status_proto",
)

go_proto_library(
    name = "build_events_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/build_events",
    proto = ":build_events_proto",
    deps = [
        ":build_status_go_proto",
    ],
)

go_proto_library(
    name = "config_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/config",
    proto = ":config_proto",
)

go_proto_library(
    name = "server_notification_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/server_notification",
    proto = ":server_notification_proto",
)

go_proto_library(
    name = "execution_stats_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/execution_stats",
    proto = ":execution_stats_proto",
    deps = [
        ":acl_go_proto",
        ":context_go_proto",
        ":invocation_status_go_proto",
        ":remote_execution_go_proto",
        ":resource_go_proto",
        ":scheduler_go_proto",
        ":stat_filter_go_proto",
        "@com_google_cloud_go_longrunning//autogen/longrunningpb",
        "@org_golang_google_genproto_googleapis_rpc//status",
    ],
)

go_proto_library(
    name = "failure_details_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/failure_details",
    proto = ":failure_details_proto",
)

go_proto_library(
    name = "firecracker_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/firecracker",
    proto = ":firecracker_proto",
    deps = [
        ":remote_execution_go_proto",
    ],
)

go_proto_library(
    name = "git_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/git",
    proto = ":git_proto",
    deps = [
    ],
)

go_proto_library(
    name = "github_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/github",
    proto = ":github_proto",
    deps = [
        ":context_go_proto",
    ],
)

go_proto_library(
    name = "gcp_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/gcp",
    proto = ":gcp_proto",
    deps = [
        ":context_go_proto",
    ],
)

go_proto_library(
    name = "pagination_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/pagination",
    proto = ":pagination_proto",
)

go_proto_library(
    name = "package_load_metrics_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/package_load_metrics",
    proto = ":package_load_metrics_proto",
)

go_proto_library(
    name = "publish_build_event_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/publish_build_event",
    proto = ":publish_build_event_proto",
    deps = [
        ":build_events_go_proto",
        "@org_golang_google_genproto_googleapis_api//annotations",
    ],
)

go_proto_library(
    name = "usage_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/usage",
    proto = ":usage_proto",
    deps = [
        ":context_go_proto",
    ],
)

go_proto_library(
    name = "build_event_stream_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/build_event_stream",
    proto = ":build_event_stream_proto",
    deps = [
        ":action_cache_go_proto",
        ":command_line_go_proto",
        ":failure_details_go_proto",
        ":invocation_policy_go_proto",
        ":package_load_metrics_go_proto",
    ],
)

go_proto_library(
    name = "quota_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/quota",
    proto = ":quota_proto",
    deps = [
        ":context_go_proto",
    ],
)

go_proto_library(
    name = "secrets_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/secrets",
    proto = ":secrets_proto",
    deps = [
        ":context_go_proto",
    ],
)

go_proto_library(
    name = "soci_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/soci",
    proto = ":soci_proto",
    deps = [
        ":registry_go_proto",
        ":remote_execution_go_proto",
    ],
)

go_proto_library(
    name = "spawn_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/spawn",
    proto = ":spawn_proto",
    deps = [
        ":context_go_proto",
        ":invocation_status_go_proto",
        ":stat_filter_go_proto",
    ],
)

go_proto_library(
    name = "spawn_diff_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/spawn_diff",
    proto = ":spawn_diff_proto",
    deps = [
        ":spawn_go_proto",
    ],
)

go_proto_library(
    name = "stat_filter_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/stat_filter",
    proto = ":stat_filter_proto",
    deps = [
        ":invocation_status_go_proto",
    ],
)

go_proto_library(
    name = "stats_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/stats",
    proto = ":stats_proto",
    deps = [
        ":context_go_proto",
        ":invocation_status_go_proto",
        ":stat_filter_go_proto",
    ],
)

go_proto_library(
    name = "target_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/target",
    proto = ":target_proto",
    deps = [
        ":build_event_stream_go_proto",
        ":context_go_proto",
        "//proto/api/v1:common_go_proto",
    ],
)

go_proto_library(
    name = "target_pagination_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/target_pagination",
    proto = ":target_pagination_proto",
)

go_proto_library(
    name = "eventlog_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/eventlog",
    proto = ":eventlog_proto",
    deps = [
        ":context_go_proto",
    ],
)

go_proto_library(
    name = "vmexec_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/vmexec",
    proto = ":vmexec_proto",
    deps = [
        ":remote_execution_go_proto",
        "@org_golang_google_genproto_googleapis_rpc//status",
    ],
)

go_proto_library(
    name = "vmvfs_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/vmvfs",
    proto = ":vmvfs_proto",
    deps = [
        ":remote_execution_go_proto",
    ],
)

go_proto_library(
    name = "vfs_go_proto",
    compilers = [
        "//proto:vtprotobuf_compiler",
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/vfs",
    proto = ":vfs_proto",
)

go_proto_library(
    name = "workflow_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/workflow",
    proto = ":workflow_proto",
    deps = [
        ":context_go_proto",
        ":firecracker_go_proto",
        ":git_go_proto",
        ":invocation_status_go_proto",
        ":remote_execution_go_proto",
        "@org_golang_google_genproto_googleapis_rpc//status",
    ],
)

go_proto_library(
    name = "workspace_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/workspace",
    proto = ":workspace_proto",
    deps = [
        ":context_go_proto",
    ],
)

go_proto_library(
    name = "raft_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/raft",
    proto = ":raft_proto",
    deps = [
        ":remote_execution_go_proto",
        ":resource_go_proto",
        "@com_github_planetscale_vtprotobuf//include/github.com/planetscale/vtprotobuf/vtproto:vtproto_go_proto",
        "@org_golang_google_genproto_googleapis_rpc//status",
    ],
)

go_proto_library(
    name = "runner_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/runner",
    proto = ":runner_proto",
    deps = [
        ":context_go_proto",
        ":git_go_proto",
        ":remote_execution_go_proto",
    ],
)

go_proto_library(
    name = "invocation_policy_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/invocation_policy",
    proto = ":invocation_policy_proto",
    deps = [
        ":strategy_policy_go_proto",
    ],
)

go_proto_library(
    name = "strategy_policy_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/strategy_policy",
    proto = ":strategy_policy_proto",
)

go_proto_library(
    name = "command_line_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/command_line",
    proto = ":command_line_proto",
    deps = [
        ":option_filters_go_proto",
    ],
)

go_proto_library(
    name = "resource_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/resource",
    proto = ":resource_proto",
    deps = [
        ":remote_execution_go_proto",
    ],
)

go_proto_library(
    name = "option_filters_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/options",
    proto = ":option_filters_proto",
)

go_proto_library(
    name = "invocation_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/invocation",
    proto = ":invocation_proto",
    deps = [
        ":acl_go_proto",
        ":api_key_go_proto",
        ":build_event_stream_go_proto",
        ":cache_go_proto",
        ":command_line_go_proto",
        ":context_go_proto",
        ":invocation_status_go_proto",
        ":stat_filter_go_proto",
        ":target_go_proto",
    ],
)

go_proto_library(
    name = "invocation_status_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/invocation_status",
    proto = ":invocation_status_proto",
)

go_proto_library(
    name = "iprules_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/iprules",
    proto = ":iprules_proto",
    deps = [
        ":context_go_proto",
    ],
)

go_proto_library(
    name = "raft_service_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/raft_service",
    proto = ":raft_service_proto",
    deps = [
        ":raft_go_proto",
    ],
)

go_proto_library(
    name = "ping_service_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/ping_service",
    proto = ":ping_service_proto",
)

go_proto_library(
    name = "buildbuddy_service_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/buildbuddy_service",
    proto = ":buildbuddy_service_proto",
    deps = [
        ":api_key_go_proto",
        ":auditlog_go_proto",
        ":bazel_config_go_proto",
        ":cache_go_proto",
        ":encryption_go_proto",
        ":eventlog_go_proto",
        ":execution_stats_go_proto",
        ":gcp_go_proto",
        ":github_go_proto",
        ":group_go_proto",
        ":invocation_go_proto",
        ":iprules_go_proto",
        ":quota_go_proto",
        ":repo_go_proto",
        ":resource_go_proto",
        ":runner_go_proto",
        ":scheduler_go_proto",
        ":search_go_proto",
        ":secrets_go_proto",
        ":stats_go_proto",
        ":suggestion_go_proto",
        ":target_go_proto",
        ":usage_go_proto",
        ":user_go_proto",
        ":workflow_go_proto",
        ":workspace_go_proto",
        ":zip_go_proto",
    ],
)

go_proto_library(
    name = "semver_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/semver",
    proto = ":semver_proto",
)

go_proto_library(
    name = "sidecar_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/sidecar",
    proto = ":sidecar_proto",
)

go_proto_library(
    name = "registry_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/registry",
    proto = ":registry_proto",
    deps = [":remote_execution_go_proto"],
)

go_proto_library(
    name = "user_id_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/user_id",
    proto = ":user_id_proto",
)

go_proto_library(
    name = "user_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/user",
    proto = ":user_proto",
    deps = [
        ":context_go_proto",
        ":group_go_proto",
        ":user_id_go_proto",
    ],
)

go_proto_library(
    name = "group_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/group",
    proto = ":group_proto",
    deps = [
        ":api_key_go_proto",
        ":context_go_proto",
        ":user_id_go_proto",
    ],
)

go_proto_library(
    name = "cache_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/cache",
    proto = ":cache_proto",
    deps = [
        ":context_go_proto",
        ":remote_execution_go_proto",
        ":resource_go_proto",
        "@org_golang_google_genproto_googleapis_rpc//status",
    ],
)

go_proto_library(
    name = "certgenerator_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/certgenerator",
    proto = ":certgenerator_proto",
    deps = [
    ],
)

go_proto_library(
    name = "context_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/context",
    proto = ":context_proto",
    deps = [
        ":user_id_go_proto",
    ],
)

go_proto_library(
    name = "bazel_config_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/bazel_config",
    proto = ":bazel_config_proto",
    deps = [
        ":api_key_go_proto",
        ":context_go_proto",
    ],
)

go_proto_library(
    name = "distributed_cache_go_proto",
    compilers = [
        "//proto:vtprotobuf_compiler",
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/distributed_cache",
    proto = ":distributed_cache_proto",
    deps = [
        ":resource_go_proto",
        "@com_github_planetscale_vtprotobuf//include/github.com/planetscale/vtprotobuf/vtproto:vtproto_go_proto",
    ],
)

go_proto_library(
    name = "remote_asset_go_proto",
    compilers = [
        "//proto:vtprotobuf_compiler",
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/remote_asset",
    proto = ":remote_asset_proto",
    deps = [
        ":remote_execution_go_proto",
        ":semver_go_proto",
        "@com_google_cloud_go_longrunning//autogen/longrunningpb",
        "@org_golang_google_genproto_googleapis_api//annotations",
        "@org_golang_google_genproto_googleapis_rpc//status",
    ],
)

go_proto_library(
    name = "remote_execution_log_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/remote_execution_log",
    proto = ":remote_execution_log_proto",
    deps = [
        ":remote_execution_go_proto",
        "@com_google_cloud_go_longrunning//autogen/longrunningpb",
        "@org_golang_google_genproto_googleapis_api//annotations",
        "@org_golang_google_genproto_googleapis_bytestream//:bytestream",
        "@org_golang_google_genproto_googleapis_rpc//status",
    ],
)

go_proto_library(
    name = "remote_execution_go_proto",
    compilers = [
        "//proto:vtprotobuf_compiler",
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/remote_execution",
    proto = ":remote_execution_proto",
    deps = [
        ":scheduler_go_proto",
        ":semver_go_proto",
        "@com_google_cloud_go_longrunning//autogen/longrunningpb",
        "@org_golang_google_genproto_googleapis_api//annotations",
        "@org_golang_google_genproto_googleapis_rpc//status",
    ],
)

go_proto_library(
    name = "repo_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/repo",
    proto = ":repo_proto",
    deps = [
        ":context_go_proto",
    ],
)

go_proto_library(
    name = "telemetry_go_proto",
    compilers = [
        "//proto:vtprotobuf_compiler",
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/telemetry",
    proto = ":telemetry_proto",
    deps = [
        "@org_golang_google_genproto_googleapis_rpc//status",
    ],
)

go_proto_library(
    name = "scheduler_go_proto",
    compilers = [
        "//proto:vtprotobuf_compiler",
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/scheduler",
    proto = ":scheduler_proto",
    deps = [
        ":acl_go_proto",
        ":context_go_proto",
        ":trace_go_proto",
        "@org_golang_google_genproto_googleapis_rpc//status",
    ],
)

go_proto_library(
    name = "suggestion_go_proto",
    compilers = [
        "//proto:vtprotobuf_compiler",
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/suggestion",
    proto = ":suggestion_proto",
    deps = [
        ":context_go_proto",
    ],
)

go_proto_library(
    name = "trace_go_proto",
    compilers = [
        "//proto:vtprotobuf_compiler",
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/trace",
    proto = ":trace_proto",
)

go_proto_library(
    name = "worker_go_proto",
    compilers = [
        "//proto:vtprotobuf_compiler",
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/worker",
    proto = ":worker_proto",
)

go_proto_library(
    name = "stored_invocation_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/stored_invocation",
    proto = ":stored_invocation_proto",
)

go_proto_library(
    name = "zip_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/zip",
    proto = ":zip_proto",
    deps = [
        ":context_go_proto",
        ":remote_execution_go_proto",
        "@com_github_planetscale_vtprotobuf//include/github.com/planetscale/vtprotobuf/vtproto:vtproto_go_proto",
    ],
)

go_proto_library(
    name = "encryption_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/encryption",
    proto = ":encryption_proto",
    deps = [
        ":context_go_proto",
    ],
)

go_proto_library(
    name = "metrics_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "//proto:vtprotobuf_compiler",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/metrics",
    proto = ":metrics_proto",
    deps = [
        ":prometheus_client_go_proto",
    ],
)

go_proto_library(
    name = "index_go_proto",
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/index",
    proto = ":index_proto",
    deps = [
        ":context_go_proto",
        ":git_go_proto",
        ":resource_go_proto",
    ],
)

go_proto_library(
    name = "search_go_proto",
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/search",
    proto = ":search_proto",
    deps = [
        ":context_go_proto",
        "@io_kythe//kythe/proto:filetree_go_proto",
        "@io_kythe//kythe/proto:graph_go_proto",
        "@io_kythe//kythe/proto:xref_go_proto",
    ],
)

go_proto_library(
    name = "codesearch_service_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/codesearch_service",
    proto = ":codesearch_service_proto",
    deps = [
        ":index_go_proto",
        ":search_go_proto",
    ],
)

go_proto_library(
    name = "kythe_service_go_proto",
    compilers = [
        "@io_bazel_rules_go//proto:go_proto",
        "@io_bazel_rules_go//proto:go_grpc_v2",
    ],
    importpath = "github.com/buildbuddy-io/buildbuddy/proto/kythe_service",
    proto = ":kythe_service_proto",
    deps = [
        "@io_kythe//kythe/proto:analysis_go_proto",
        "@io_kythe//kythe/proto:explore_go_proto",
        "@io_kythe//kythe/proto:filetree_go_proto",
        "@io_kythe//kythe/proto:graph_go_proto",
        "@io_kythe//kythe/proto:identifier_go_proto",
        "@io_kythe//kythe/proto:link_go_proto",
        "@io_kythe//kythe/proto:status_service_go_proto",
        "@io_kythe//kythe/proto:storage_go_proto",
        "@io_kythe//kythe/proto:xref_go_proto",
    ],
)

# TypeScript proto rules below here

ts_proto_library(
    name = "acl_ts_proto",
    proto = ":acl_proto",
    deps = [
        ":user_id_ts_proto",
    ],
)

ts_proto_library(
    name = "action_cache_ts_proto",
    proto = ":action_cache_proto",
)

ts_proto_library(
    name = "api_key_ts_proto",
    proto = ":api_key_proto",
    deps = [
        ":context_ts_proto",
    ],
)

ts_proto_library(
    name = "auditlog_ts_proto",
    proto = ":auditlog_proto",
    deps = [
        ":api_key_ts_proto",
        ":context_ts_proto",
        ":encryption_ts_proto",
        ":github_ts_proto",
        ":group_ts_proto",
        ":invocation_ts_proto",
        ":iprules_ts_proto",
        ":secrets_ts_proto",
        ":timestamp_ts_proto",
        ":workflow_ts_proto",
    ],
)

ts_proto_library(
    name = "bazel_config_ts_proto",
    proto = ":bazel_config_proto",
    deps = [
        ":api_key_ts_proto",
        ":context_ts_proto",
    ],
)

ts_proto_library(
    name = "config_ts_proto",
    proto = ":config_proto",
)

ts_proto_library(
    name = "server_notification_ts_proto",
    proto = ":server_notification_proto",
)

ts_proto_library(
    name = "execution_stats_ts_proto",
    proto = ":execution_stats_proto",
    deps = [
        ":acl_ts_proto",
        ":context_ts_proto",
        ":google_longrunning_ts_proto",
        ":grpc_status_ts_proto",
        ":invocation_status_ts_proto",
        ":remote_execution_ts_proto",
        ":scheduler_ts_proto",
        ":stat_filter_ts_proto",
        ":timestamp_ts_proto",
    ],
)

ts_proto_library(
    name = "git_ts_proto",
    proto = ":git_proto",
    deps = [
    ],
)

ts_proto_library(
    name = "github_ts_proto",
    proto = ":github_proto",
    deps = [
        ":context_ts_proto",
    ],
)

ts_proto_library(
    name = "gcp_ts_proto",
    proto = ":gcp_proto",
    deps = [
        ":context_ts_proto",
    ],
)

ts_proto_library(
    name = "package_load_metrics_ts_proto",
    proto = ":package_load_metrics_proto",
    deps = [
        ":duration_ts_proto",
    ],
)

ts_proto_library(
    name = "quota_ts_proto",
    proto = ":quota_proto",
    deps = [
        ":context_ts_proto",
        ":duration_ts_proto",
    ],
)

ts_proto_library(
    name = "resource_ts_proto",
    proto = ":resource_proto",
    deps = [
        ":remote_execution_ts_proto",
    ],
)

ts_proto_library(
    name = "secrets_ts_proto",
    proto = ":secrets_proto",
    deps = [
        ":context_ts_proto",
    ],
)

ts_proto_library(
    name = "spawn_ts_proto",
    proto = ":spawn_proto",
    deps = [
        ":context_ts_proto",
        ":duration_ts_proto",
        ":invocation_status_ts_proto",
        ":stat_filter_ts_proto",
        ":timestamp_ts_proto",
    ],
)

ts_proto_library(
    name = "stat_filter_ts_proto",
    proto = ":stat_filter_proto",
    deps = [
        ":descriptor_ts_proto",
        ":invocation_status_ts_proto",
    ],
)

ts_proto_library(
    name = "stats_ts_proto",
    proto = ":stats_proto",
    deps = [
        ":context_ts_proto",
        ":duration_ts_proto",
        ":invocation_status_ts_proto",
        ":stat_filter_ts_proto",
        ":timestamp_ts_proto",
    ],
)

ts_proto_library(
    name = "scheduler_ts_proto",
    proto = ":scheduler_proto",
    deps = [
        ":acl_ts_proto",
        ":context_ts_proto",
        ":duration_ts_proto",
        ":grpc_status_ts_proto",
        ":timestamp_ts_proto",
        ":trace_ts_proto",
    ],
)

ts_proto_library(
    name = "trace_ts_proto",
    proto = ":trace_proto",
)

ts_proto_library(
    name = "suggestion_ts_proto",
    proto = ":suggestion_proto",
    deps = [
        ":context_ts_proto",
    ],
)

ts_proto_library(
    name = "failure_details_ts_proto",
    proto = ":failure_details_proto",
    deps = [
        ":descriptor_ts_proto",
    ],
)

ts_proto_library(
    name = "build_event_stream_ts_proto",
    proto = ":build_event_stream_proto",
    deps = [
        ":action_cache_ts_proto",
        ":any_ts_proto",
        ":command_line_ts_proto",
        ":descriptor_ts_proto",
        ":duration_ts_proto",
        ":failure_details_ts_proto",
        ":invocation_policy_ts_proto",
        ":package_load_metrics_ts_proto",
        ":timestamp_ts_proto",
    ],
)

ts_proto_library(
    name = "build_status_ts_proto",
    proto = ":build_status_proto",
    deps = [
        ":any_ts_proto",
        ":wrappers_ts_proto",
    ],
)

ts_proto_library(
    name = "target_ts_proto",
    proto = ":target_proto",
    deps = [
        ":build_event_stream_ts_proto",
        ":context_ts_proto",
        ":timestamp_ts_proto",
        "//proto/api/v1:common_ts_proto",
    ],
)

ts_proto_library(
    name = "eventlog_ts_proto",
    proto = ":eventlog_proto",
    deps = [
        ":context_ts_proto",
    ],
)

ts_proto_library(
    name = "workflow_ts_proto",
    proto = ":workflow_proto",
    deps = [
        ":context_ts_proto",
        ":duration_ts_proto",
        ":firecracker_ts_proto",
        ":git_ts_proto",
        ":grpc_status_ts_proto",
        ":invocation_status_ts_proto",
        ":remote_execution_ts_proto",
    ],
)

ts_proto_library(
    name = "workspace_ts_proto",
    proto = ":workspace_proto",
    deps = [
        ":context_ts_proto",
    ],
)

ts_proto_library(
    name = "command_line_ts_proto",
    proto = ":command_line_proto",
    deps = [
        ":option_filters_ts_proto",
    ],
)

ts_proto_library(
    name = "option_filters_ts_proto",
    proto = ":option_filters_proto",
)

ts_proto_library(
    name = "context_ts_proto",
    proto = ":context_proto",
    deps = [
        ":user_id_ts_proto",
    ],
)

ts_proto_library(
    name = "invocation_status_ts_proto",
    proto = ":invocation_status_proto",
)

ts_proto_library(
    name = "invocation_ts_proto",
    proto = ":invocation_proto",
    deps = [
        ":acl_ts_proto",
        ":api_key_ts_proto",
        ":build_event_stream_ts_proto",
        ":cache_ts_proto",
        ":command_line_ts_proto",
        ":context_ts_proto",
        ":duration_ts_proto",
        ":invocation_status_ts_proto",
        ":stat_filter_ts_proto",
        ":target_ts_proto",
        ":timestamp_ts_proto",
    ],
)

ts_proto_library(
    name = "invocation_policy_ts_proto",
    proto = ":invocation_policy_proto",
    deps = [
        ":strategy_policy_ts_proto",
    ],
)

ts_proto_library(
    name = "strategy_policy_ts_proto",
    proto = ":strategy_policy_proto",
    deps = [],
)

ts_proto_library(
    name = "iprules_ts_proto",
    proto = ":iprules_proto",
    deps = [
        ":context_ts_proto",
    ],
)

ts_proto_library(
    name = "usage_ts_proto",
    proto = ":usage_proto",
    deps = [
        ":context_ts_proto",
    ],
)

ts_proto_library(
    name = "search_ts_proto",
    proto = ":search_proto",
    deps = [
        ":context_ts_proto",
        ":kythe_filetree_ts_proto",
        ":kythe_graph_ts_proto",
        ":kythe_xref_ts_proto",
    ],
)

ts_proto_library(
    name = "group_ts_proto",
    proto = ":group_proto",
    deps = [
        ":api_key_ts_proto",
        ":context_ts_proto",
        ":user_id_ts_proto",
    ],
)

ts_proto_library(
    name = "grpc_code_ts_proto",
    proto = "@googleapis//google/rpc:code_proto",
)

ts_proto_library(
    name = "grpc_status_ts_proto",
    proto = "@googleapis//google/rpc:status_proto",
    deps = [":any_ts_proto"],
)

ts_proto_library(
    name = "grpc_error_details_ts_proto",
    proto = "@googleapis//google/rpc:error_details_proto",
    deps = [
        ":any_ts_proto",
        ":duration_ts_proto",
    ],
)

ts_proto_library(
    name = "google_api_annotations_ts_proto",
    proto = "@googleapis//google/api:annotations_proto",
    deps = [
        ":descriptor_ts_proto",
        ":duration_ts_proto",
    ],
)

ts_proto_library(
    name = "google_longrunning_ts_proto",
    proto = "@googleapis//google/longrunning:operations_proto",
    deps = [
        ":any_ts_proto",
        ":duration_ts_proto",
        ":empty_ts_proto",
        ":grpc_status_ts_proto",
    ],
)

ts_proto_library(
    name = "empty_ts_proto",
    proto = "@com_google_protobuf//:empty_proto",
)

ts_proto_library(
    name = "timestamp_ts_proto",
    proto = "@com_google_protobuf//:timestamp_proto",
)

ts_proto_library(
    name = "descriptor_ts_proto",
    proto = "@com_google_protobuf//:descriptor_proto",
)

ts_proto_library(
    name = "duration_ts_proto",
    proto = "@com_google_protobuf//:duration_proto",
)

ts_proto_library(
    name = "any_ts_proto",
    proto = "@com_google_protobuf//:any_proto",
)

ts_proto_library(
    name = "wrappers_ts_proto",
    proto = "@com_google_protobuf//:wrappers_proto",
)

ts_proto_library(
    name = "semver_ts_proto",
    proto = ":semver_proto",
)

ts_proto_library(
    name = "field_mask_ts_proto",
    proto = "@com_google_protobuf//:field_mask_proto",
)

ts_proto_library(
    name = "vtproto_ts_proto",
    proto = "@com_github_planetscale_vtprotobuf//include/github.com/planetscale/vtprotobuf/vtproto:vtproto_proto",
    deps = ["descriptor_ts_proto"],
)

ts_proto_library(
    name = "cache_ts_proto",
    proto = ":cache_proto",
    deps = [
        ":context_ts_proto",
        ":duration_ts_proto",
        ":field_mask_ts_proto",
        ":grpc_status_ts_proto",
        ":remote_execution_ts_proto",
        ":resource_ts_proto",
        ":timestamp_ts_proto",
    ],
)

ts_proto_library(
    name = "user_id_ts_proto",
    proto = ":user_id_proto",
)

ts_proto_library(
    name = "user_ts_proto",
    proto = ":user_proto",
    deps = [
        ":context_ts_proto",
        ":group_ts_proto",
        ":user_id_ts_proto",
    ],
)

ts_proto_library(
    name = "encryption_ts_proto",
    proto = ":encryption_proto",
    deps = [":context_ts_proto"],
)

ts_proto_library(
    name = "buildbuddy_service_ts_proto",
    proto = ":buildbuddy_service_proto",
    deps = [
        ":api_key_ts_proto",
        ":auditlog_ts_proto",
        ":bazel_config_ts_proto",
        ":cache_ts_proto",
        ":encryption_ts_proto",
        ":eventlog_ts_proto",
        ":execution_stats_ts_proto",
        ":gcp_ts_proto",
        ":github_ts_proto",
        ":group_ts_proto",
        ":invocation_ts_proto",
        ":iprules_ts_proto",
        ":quota_ts_proto",
        ":repo_ts_proto",
        ":runner_ts_proto",
        ":scheduler_ts_proto",
        ":search_ts_proto",
        ":secrets_ts_proto",
        ":stats_ts_proto",
        ":suggestion_ts_proto",
        ":target_ts_proto",
        ":usage_ts_proto",
        ":user_ts_proto",
        ":workflow_ts_proto",
        ":workspace_ts_proto",
        ":zip_ts_proto",
    ],
)

ts_proto_library(
    name = "repo_ts_proto",
    proto = ":repo_proto",
    deps = [
        ":context_ts_proto",
    ],
)

ts_proto_library(
    name = "remote_execution_ts_proto",
    proto = ":remote_execution_proto",
    deps = [
        ":any_ts_proto",
        ":duration_ts_proto",
        ":google_api_annotations_ts_proto",
        ":google_longrunning_ts_proto",
        ":grpc_status_ts_proto",
        ":scheduler_ts_proto",
        ":semver_ts_proto",
        ":timestamp_ts_proto",
        ":wrappers_ts_proto",
    ],
)

ts_proto_library(
    name = "execution_graph_ts_proto",
    proto = ":execution_graph_proto",
)

ts_proto_library(
    name = "runner_ts_proto",
    proto = ":runner_proto",
    deps = [
        ":context_ts_proto",
        ":git_ts_proto",
        ":remote_execution_ts_proto",
    ],
)

ts_proto_library(
    name = "firecracker_ts_proto",
    proto = ":firecracker_proto",
    deps = [
        ":remote_execution_ts_proto",
    ],
)

ts_proto_library(
    name = "zip_ts_proto",
    proto = ":zip_proto",
    deps = [
        ":context_ts_proto",
        ":vtproto_ts_proto",
    ],
)

proto_cc_library(
    name = "acl_cc_library",
    srcs = ["acl.pb.cc"],
    hdrs = ["acl.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "acl_cpp_compile",
    outputs = [
        "acl.pb.cc",
        "acl.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "acl_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "action_cache_cc_library",
    srcs = ["action_cache.pb.cc"],
    hdrs = ["action_cache.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "action_cache_cpp_compile",
    outputs = [
        "action_cache.pb.cc",
        "action_cache.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "action_cache_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "api_key_cc_library",
    srcs = ["api_key.pb.cc"],
    hdrs = ["api_key.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "api_key_cpp_compile",
    outputs = [
        "api_key.pb.cc",
        "api_key.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "api_key_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "auditlog_cc_library",
    srcs = ["auditlog.pb.cc"],
    hdrs = ["auditlog.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "auditlog_cpp_compile",
    outputs = [
        "auditlog.pb.cc",
        "auditlog.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "auditlog_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "auth_cc_library",
    srcs = ["auth.pb.cc"],
    hdrs = ["auth.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "auth_cpp_compile",
    outputs = [
        "auth.grpc.pb.cc",
        "auth.grpc.pb.h",
        "auth.pb.cc",
        "auth.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "auth_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "bazel_config_cc_library",
    srcs = ["bazel_config.pb.cc"],
    hdrs = ["bazel_config.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "bazel_config_cpp_compile",
    outputs = [
        "bazel_config.pb.cc",
        "bazel_config.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "bazel_config_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "bazel_query_cc_library",
    srcs = ["bazel_query.pb.cc"],
    hdrs = ["bazel_query.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "bazel_query_cpp_compile",
    outputs = [
        "bazel_query.pb.cc",
        "bazel_query.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "bazel_query_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "build_event_stream_cc_library",
    srcs = ["build_event_stream.pb.cc"],
    hdrs = ["build_event_stream.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "build_event_stream_cpp_compile",
    outputs = [
        "build_event_stream.pb.cc",
        "build_event_stream.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "build_event_stream_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "build_events_cc_library",
    srcs = ["build_events.pb.cc"],
    hdrs = ["build_events.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "build_events_cpp_compile",
    outputs = [
        "build_events.pb.cc",
        "build_events.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "build_events_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "build_status_cc_library",
    srcs = ["build_status.pb.cc"],
    hdrs = ["build_status.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "build_status_cpp_compile",
    outputs = [
        "build_status.pb.cc",
        "build_status.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "build_status_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "buildbuddy_service_cc_library",
    srcs = ["buildbuddy_service.pb.cc"],
    hdrs = ["buildbuddy_service.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "buildbuddy_service_cpp_compile",
    outputs = [
        "buildbuddy_service.grpc.pb.cc",
        "buildbuddy_service.grpc.pb.h",
        "buildbuddy_service.pb.cc",
        "buildbuddy_service.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "buildbuddy_service_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "cache_cc_library",
    srcs = ["cache.pb.cc"],
    hdrs = ["cache.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "cache_cpp_compile",
    outputs = [
        "cache.pb.cc",
        "cache.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "cache_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "certgenerator_cc_library",
    srcs = ["certgenerator.pb.cc"],
    hdrs = ["certgenerator.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "certgenerator_cpp_compile",
    outputs = [
        "certgenerator.grpc.pb.cc",
        "certgenerator.grpc.pb.h",
        "certgenerator.pb.cc",
        "certgenerator.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "certgenerator_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "codesearch_service_cc_library",
    srcs = ["codesearch_service.pb.cc"],
    hdrs = ["codesearch_service.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "codesearch_service_cpp_compile",
    outputs = [
        "codesearch_service.grpc.pb.cc",
        "codesearch_service.grpc.pb.h",
        "codesearch_service.pb.cc",
        "codesearch_service.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "codesearch_service_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "command_line_cc_library",
    srcs = ["command_line.pb.cc"],
    hdrs = ["command_line.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "command_line_cpp_compile",
    outputs = [
        "command_line.pb.cc",
        "command_line.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "command_line_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "config_cc_library",
    srcs = ["config.pb.cc"],
    hdrs = ["config.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "config_cpp_compile",
    outputs = [
        "config.pb.cc",
        "config.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "config_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "context_cc_library",
    srcs = ["context.pb.cc"],
    hdrs = ["context.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "context_cpp_compile",
    outputs = [
        "context.pb.cc",
        "context.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "context_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "distributed_cache_cc_library",
    srcs = ["distributed_cache.pb.cc"],
    hdrs = ["distributed_cache.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "distributed_cache_cpp_compile",
    outputs = [
        "distributed_cache.grpc.pb.cc",
        "distributed_cache.grpc.pb.h",
        "distributed_cache.pb.cc",
        "distributed_cache.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "distributed_cache_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "encryption_cc_library",
    srcs = ["encryption.pb.cc"],
    hdrs = ["encryption.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "encryption_cpp_compile",
    outputs = [
        "encryption.pb.cc",
        "encryption.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "encryption_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "eventlog_cc_library",
    srcs = ["eventlog.pb.cc"],
    hdrs = ["eventlog.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "eventlog_cpp_compile",
    outputs = [
        "eventlog.pb.cc",
        "eventlog.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "eventlog_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "execution_graph_cc_library",
    srcs = ["execution_graph.pb.cc"],
    hdrs = ["execution_graph.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "execution_graph_cpp_compile",
    outputs = [
        "execution_graph.pb.cc",
        "execution_graph.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "execution_graph_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "execution_stats_cc_library",
    srcs = ["execution_stats.pb.cc"],
    hdrs = ["execution_stats.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "execution_stats_cpp_compile",
    outputs = [
        "execution_stats.pb.cc",
        "execution_stats.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "execution_stats_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "failure_details_cc_library",
    srcs = ["failure_details.pb.cc"],
    hdrs = ["failure_details.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "failure_details_cpp_compile",
    outputs = [
        "failure_details.pb.cc",
        "failure_details.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "failure_details_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "firecracker_cc_library",
    srcs = ["firecracker.pb.cc"],
    hdrs = ["firecracker.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "firecracker_cpp_compile",
    outputs = [
        "firecracker.pb.cc",
        "firecracker.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "firecracker_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "gcp_cc_library",
    srcs = ["gcp.pb.cc"],
    hdrs = ["gcp.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "gcp_cpp_compile",
    outputs = [
        "gcp.pb.cc",
        "gcp.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "gcp_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "git_cc_library",
    srcs = ["git.pb.cc"],
    hdrs = ["git.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "git_cpp_compile",
    outputs = [
        "git.pb.cc",
        "git.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "git_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "github_cc_library",
    srcs = ["github.pb.cc"],
    hdrs = ["github.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "github_cpp_compile",
    outputs = [
        "github.pb.cc",
        "github.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "github_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "grp_cc_library",
    srcs = ["grp.pb.cc"],
    hdrs = ["grp.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "grp_cpp_compile",
    outputs = [
        "grp.pb.cc",
        "grp.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "grp_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "index_cc_library",
    srcs = ["index.pb.cc"],
    hdrs = ["index.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "index_cpp_compile",
    outputs = [
        "index.pb.cc",
        "index.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "index_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "invocation_policy_cc_library",
    srcs = ["invocation_policy.pb.cc"],
    hdrs = ["invocation_policy.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "invocation_policy_cpp_compile",
    outputs = [
        "invocation_policy.pb.cc",
        "invocation_policy.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "invocation_policy_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "invocation_cc_library",
    srcs = ["invocation.pb.cc"],
    hdrs = ["invocation.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "invocation_cpp_compile",
    outputs = [
        "invocation.pb.cc",
        "invocation.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "invocation_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "invocation_status_cc_library",
    srcs = ["invocation_status.pb.cc"],
    hdrs = ["invocation_status.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "invocation_status_cpp_compile",
    outputs = [
        "invocation_status.pb.cc",
        "invocation_status.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "invocation_status_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "iprules_cc_library",
    srcs = ["iprules.pb.cc"],
    hdrs = ["iprules.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "iprules_cpp_compile",
    outputs = [
        "iprules.pb.cc",
        "iprules.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "iprules_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "kythe_service_cc_library",
    srcs = ["kythe_service.pb.cc"],
    hdrs = ["kythe_service.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "kythe_service_cpp_compile",
    outputs = [
        "kythe_service.grpc.pb.cc",
        "kythe_service.grpc.pb.h",
        "kythe_service.pb.cc",
        "kythe_service.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "kythe_service_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "metrics_cc_library",
    srcs = ["metrics.pb.cc"],
    hdrs = ["metrics.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "metrics_cpp_compile",
    outputs = [
        "metrics.pb.cc",
        "metrics.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "metrics_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "option_filters_cc_library",
    srcs = ["option_filters.pb.cc"],
    hdrs = ["option_filters.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "option_filters_cpp_compile",
    outputs = [
        "option_filters.pb.cc",
        "option_filters.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "option_filters_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "package_load_metrics_cc_library",
    srcs = ["package_load_metrics.pb.cc"],
    hdrs = ["package_load_metrics.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "package_load_metrics_cpp_compile",
    outputs = [
        "package_load_metrics.pb.cc",
        "package_load_metrics.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "package_load_metrics_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "pagination_cc_library",
    srcs = ["pagination.pb.cc"],
    hdrs = ["pagination.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "pagination_cpp_compile",
    outputs = [
        "pagination.pb.cc",
        "pagination.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "pagination_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "ping_service_cc_library",
    srcs = ["ping_service.pb.cc"],
    hdrs = ["ping_service.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "ping_service_cpp_compile",
    outputs = [
        "ping_service.grpc.pb.cc",
        "ping_service.grpc.pb.h",
        "ping_service.pb.cc",
        "ping_service.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "ping_service_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "publish_build_event_cc_library",
    srcs = ["publish_build_event.pb.cc"],
    hdrs = ["publish_build_event.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "publish_build_event_cpp_compile",
    outputs = [
        "publish_build_event.grpc.pb.cc",
        "publish_build_event.grpc.pb.h",
        "publish_build_event.pb.cc",
        "publish_build_event.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "publish_build_event_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "quota_cc_library",
    srcs = ["quota.pb.cc"],
    hdrs = ["quota.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "quota_cpp_compile",
    outputs = [
        "quota.pb.cc",
        "quota.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "quota_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "raft_cc_library",
    srcs = ["raft.pb.cc"],
    hdrs = ["raft.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "raft_cpp_compile",
    outputs = [
        "raft.pb.cc",
        "raft.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "raft_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "raft_service_cc_library",
    srcs = ["raft_service.pb.cc"],
    hdrs = ["raft_service.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "raft_service_cpp_compile",
    outputs = [
        "raft_service.grpc.pb.cc",
        "raft_service.grpc.pb.h",
        "raft_service.pb.cc",
        "raft_service.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "raft_service_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "registry_cc_library",
    srcs = ["registry.pb.cc"],
    hdrs = ["registry.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "registry_cpp_compile",
    outputs = [
        "registry.pb.cc",
        "registry.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "registry_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "remote_asset_cc_library",
    srcs = ["remote_asset.pb.cc"],
    hdrs = ["remote_asset.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "remote_asset_cpp_compile",
    outputs = [
        "remote_asset.grpc.pb.cc",
        "remote_asset.grpc.pb.h",
        "remote_asset.pb.cc",
        "remote_asset.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "remote_asset_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "remote_execution_log_cc_library",
    srcs = ["remote_execution_log.pb.cc"],
    hdrs = ["remote_execution_log.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "remote_execution_log_cpp_compile",
    outputs = [
        "remote_execution_log.pb.cc",
        "remote_execution_log.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "remote_execution_log_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "remote_execution_cc_library",
    srcs = ["remote_execution.pb.cc"],
    hdrs = ["remote_execution.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "remote_execution_cpp_compile",
    outputs = [
        "remote_execution.grpc.pb.cc",
        "remote_execution.grpc.pb.h",
        "remote_execution.pb.cc",
        "remote_execution.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "remote_execution_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "repo_cc_library",
    srcs = ["repo.pb.cc"],
    hdrs = ["repo.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "repo_cpp_compile",
    outputs = [
        "repo.pb.cc",
        "repo.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "repo_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "resource_cc_library",
    srcs = ["resource.pb.cc"],
    hdrs = ["resource.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "resource_cpp_compile",
    outputs = [
        "resource.pb.cc",
        "resource.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "resource_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "runner_cc_library",
    srcs = ["runner.pb.cc"],
    hdrs = ["runner.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "runner_cpp_compile",
    outputs = [
        "runner.pb.cc",
        "runner.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "runner_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "scheduler_cc_library",
    srcs = ["scheduler.pb.cc"],
    hdrs = ["scheduler.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "scheduler_cpp_compile",
    outputs = [
        "scheduler.grpc.pb.cc",
        "scheduler.grpc.pb.h",
        "scheduler.pb.cc",
        "scheduler.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "scheduler_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "search_cc_library",
    srcs = ["search.pb.cc"],
    hdrs = ["search.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "search_cpp_compile",
    outputs = [
        "search.pb.cc",
        "search.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "search_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "secrets_cc_library",
    srcs = ["secrets.pb.cc"],
    hdrs = ["secrets.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "secrets_cpp_compile",
    outputs = [
        "secrets.pb.cc",
        "secrets.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "secrets_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "semver_cc_library",
    srcs = ["semver.pb.cc"],
    hdrs = ["semver.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "semver_cpp_compile",
    outputs = [
        "semver.pb.cc",
        "semver.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "semver_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "server_notification_cc_library",
    srcs = ["server_notification.pb.cc"],
    hdrs = ["server_notification.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "server_notification_cpp_compile",
    outputs = [
        "server_notification.pb.cc",
        "server_notification.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "server_notification_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "sidecar_cc_library",
    srcs = ["sidecar.pb.cc"],
    hdrs = ["sidecar.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "sidecar_cpp_compile",
    outputs = [
        "sidecar.grpc.pb.cc",
        "sidecar.grpc.pb.h",
        "sidecar.pb.cc",
        "sidecar.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "sidecar_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "soci_cc_library",
    srcs = ["soci.pb.cc"],
    hdrs = ["soci.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "soci_cpp_compile",
    outputs = [
        "soci.grpc.pb.cc",
        "soci.grpc.pb.h",
        "soci.pb.cc",
        "soci.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "soci_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "spawn_diff_cc_library",
    srcs = ["spawn_diff.pb.cc"],
    hdrs = ["spawn_diff.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "spawn_diff_cpp_compile",
    outputs = [
        "spawn_diff.pb.cc",
        "spawn_diff.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "spawn_diff_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "spawn_cc_library",
    srcs = ["spawn.pb.cc"],
    hdrs = ["spawn.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "spawn_cpp_compile",
    outputs = [
        "spawn.pb.cc",
        "spawn.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "spawn_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "stat_filter_cc_library",
    srcs = ["stat_filter.pb.cc"],
    hdrs = ["stat_filter.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "stat_filter_cpp_compile",
    outputs = [
        "stat_filter.pb.cc",
        "stat_filter.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "stat_filter_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "stats_cc_library",
    srcs = ["stats.pb.cc"],
    hdrs = ["stats.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "stats_cpp_compile",
    outputs = [
        "stats.pb.cc",
        "stats.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "stats_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "stored_invocation_cc_library",
    srcs = ["stored_invocation.pb.cc"],
    hdrs = ["stored_invocation.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "stored_invocation_cpp_compile",
    outputs = [
        "stored_invocation.pb.cc",
        "stored_invocation.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "stored_invocation_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "strategy_policy_cc_library",
    srcs = ["strategy_policy.pb.cc"],
    hdrs = ["strategy_policy.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "strategy_policy_cpp_compile",
    outputs = [
        "strategy_policy.pb.cc",
        "strategy_policy.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "strategy_policy_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "suggestion_cc_library",
    srcs = ["suggestion.pb.cc"],
    hdrs = ["suggestion.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "suggestion_cpp_compile",
    outputs = [
        "suggestion.pb.cc",
        "suggestion.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "suggestion_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "target_pagination_cc_library",
    srcs = ["target_pagination.pb.cc"],
    hdrs = ["target_pagination.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "target_pagination_cpp_compile",
    outputs = [
        "target_pagination.pb.cc",
        "target_pagination.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "target_pagination_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "target_cc_library",
    srcs = ["target.pb.cc"],
    hdrs = ["target.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "target_cpp_compile",
    outputs = [
        "target.pb.cc",
        "target.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "target_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "telemetry_cc_library",
    srcs = ["telemetry.pb.cc"],
    hdrs = ["telemetry.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "telemetry_cpp_compile",
    outputs = [
        "telemetry.grpc.pb.cc",
        "telemetry.grpc.pb.h",
        "telemetry.pb.cc",
        "telemetry.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "telemetry_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "trace_cc_library",
    srcs = ["trace.pb.cc"],
    hdrs = ["trace.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "trace_cpp_compile",
    outputs = [
        "trace.pb.cc",
        "trace.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "trace_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "usage_cc_library",
    srcs = ["usage.pb.cc"],
    hdrs = ["usage.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "usage_cpp_compile",
    outputs = [
        "usage.pb.cc",
        "usage.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "usage_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "user_id_cc_library",
    srcs = ["user_id.pb.cc"],
    hdrs = ["user_id.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "user_id_cpp_compile",
    outputs = [
        "user_id.pb.cc",
        "user_id.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "user_id_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "user_cc_library",
    srcs = ["user.pb.cc"],
    hdrs = ["user.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "user_cpp_compile",
    outputs = [
        "user.pb.cc",
        "user.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "user_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "vfs_cc_library",
    srcs = ["vfs.pb.cc"],
    hdrs = ["vfs.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "vfs_cpp_compile",
    outputs = [
        "vfs.grpc.pb.cc",
        "vfs.grpc.pb.h",
        "vfs.pb.cc",
        "vfs.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "vfs_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "vmexec_cc_library",
    srcs = ["vmexec.pb.cc"],
    hdrs = ["vmexec.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "vmexec_cpp_compile",
    outputs = [
        "vmexec.grpc.pb.cc",
        "vmexec.grpc.pb.h",
        "vmexec.pb.cc",
        "vmexec.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "vmexec_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "vmvfs_cc_library",
    srcs = ["vmvfs.pb.cc"],
    hdrs = ["vmvfs.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "vmvfs_cpp_compile",
    outputs = [
        "vmvfs.grpc.pb.cc",
        "vmvfs.grpc.pb.h",
        "vmvfs.pb.cc",
        "vmvfs.pb.h",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:cpp",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-cpp",
    ],
    proto = "vmvfs_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "worker_cc_library",
    srcs = ["worker.pb.cc"],
    hdrs = ["worker.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "worker_cpp_compile",
    outputs = [
        "worker.pb.cc",
        "worker.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "worker_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "workflow_cc_library",
    srcs = ["workflow.pb.cc"],
    hdrs = ["workflow.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "workflow_cpp_compile",
    outputs = [
        "workflow.pb.cc",
        "workflow.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "workflow_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "workspace_cc_library",
    srcs = ["workspace.pb.cc"],
    hdrs = ["workspace.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "workspace_cpp_compile",
    outputs = [
        "workspace.pb.cc",
        "workspace.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "workspace_proto",
    visibility = ["//visibility:public"],
)

proto_cc_library(
    name = "zip_cc_library",
    srcs = ["zip.pb.cc"],
    hdrs = ["zip.pb.h"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf"],
)

proto_compile(
    name = "zip_cpp_compile",
    outputs = [
        "zip.pb.cc",
        "zip.pb.h",
    ],
    plugins = ["@build_stack_rules_proto//plugin/builtin:cpp"],
    proto = "zip_proto",
    visibility = ["//visibility:public"],
)

proto_compile(
    name = "acl_python_compile",
    outputs = [
        "acl_pb2.py",
        "acl_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "acl_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "acl_py_library",
    srcs = ["acl_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "action_cache_python_compile",
    outputs = [
        "action_cache_pb2.py",
        "action_cache_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "action_cache_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "action_cache_py_library",
    srcs = ["action_cache_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "api_key_python_compile",
    outputs = [
        "api_key_pb2.py",
        "api_key_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "api_key_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "api_key_py_library",
    srcs = ["api_key_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "auditlog_python_compile",
    outputs = [
        "auditlog_pb2.py",
        "auditlog_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "auditlog_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "auditlog_py_library",
    srcs = ["auditlog_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "auth_grpc_py_library",
    srcs = ["auth_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":auth_py_library"],
)

proto_compile(
    name = "auth_python_compile",
    outputs = [
        "auth_pb2.py",
        "auth_pb2.pyi",
        "auth_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "auth_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "auth_py_library",
    srcs = ["auth_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "bazel_config_python_compile",
    outputs = [
        "bazel_config_pb2.py",
        "bazel_config_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "bazel_config_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "bazel_config_py_library",
    srcs = ["bazel_config_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "bazel_query_python_compile",
    outputs = [
        "bazel_query_pb2.py",
        "bazel_query_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "bazel_query_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "bazel_query_py_library",
    srcs = ["bazel_query_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "build_event_stream_python_compile",
    outputs = [
        "build_event_stream_pb2.py",
        "build_event_stream_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "build_event_stream_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "build_event_stream_py_library",
    srcs = ["build_event_stream_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "build_events_python_compile",
    outputs = [
        "build_events_pb2.py",
        "build_events_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "build_events_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "build_events_py_library",
    srcs = ["build_events_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "build_status_python_compile",
    outputs = [
        "build_status_pb2.py",
        "build_status_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "build_status_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "build_status_py_library",
    srcs = ["build_status_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "buildbuddy_service_grpc_py_library",
    srcs = ["buildbuddy_service_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":buildbuddy_service_py_library"],
)

proto_compile(
    name = "buildbuddy_service_python_compile",
    outputs = [
        "buildbuddy_service_pb2.py",
        "buildbuddy_service_pb2.pyi",
        "buildbuddy_service_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "buildbuddy_service_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "buildbuddy_service_py_library",
    srcs = ["buildbuddy_service_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "cache_python_compile",
    outputs = [
        "cache_pb2.py",
        "cache_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "cache_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "cache_py_library",
    srcs = ["cache_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "certgenerator_grpc_py_library",
    srcs = ["certgenerator_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":certgenerator_py_library"],
)

proto_compile(
    name = "certgenerator_python_compile",
    outputs = [
        "certgenerator_pb2.py",
        "certgenerator_pb2.pyi",
        "certgenerator_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "certgenerator_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "certgenerator_py_library",
    srcs = ["certgenerator_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "codesearch_service_grpc_py_library",
    srcs = ["codesearch_service_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":codesearch_service_py_library"],
)

proto_compile(
    name = "codesearch_service_python_compile",
    outputs = [
        "codesearch_service_pb2.py",
        "codesearch_service_pb2.pyi",
        "codesearch_service_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "codesearch_service_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "codesearch_service_py_library",
    srcs = ["codesearch_service_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "command_line_python_compile",
    outputs = [
        "command_line_pb2.py",
        "command_line_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "command_line_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "command_line_py_library",
    srcs = ["command_line_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "config_python_compile",
    outputs = [
        "config_pb2.py",
        "config_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "config_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "config_py_library",
    srcs = ["config_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "context_python_compile",
    outputs = [
        "context_pb2.py",
        "context_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "context_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "context_py_library",
    srcs = ["context_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "distributed_cache_grpc_py_library",
    srcs = ["distributed_cache_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":distributed_cache_py_library"],
)

proto_compile(
    name = "distributed_cache_python_compile",
    outputs = [
        "distributed_cache_pb2.py",
        "distributed_cache_pb2.pyi",
        "distributed_cache_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "distributed_cache_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "distributed_cache_py_library",
    srcs = ["distributed_cache_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "encryption_python_compile",
    outputs = [
        "encryption_pb2.py",
        "encryption_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "encryption_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "encryption_py_library",
    srcs = ["encryption_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "eventlog_python_compile",
    outputs = [
        "eventlog_pb2.py",
        "eventlog_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "eventlog_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "eventlog_py_library",
    srcs = ["eventlog_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "execution_graph_python_compile",
    outputs = [
        "execution_graph_pb2.py",
        "execution_graph_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "execution_graph_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "execution_graph_py_library",
    srcs = ["execution_graph_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "execution_stats_python_compile",
    outputs = [
        "execution_stats_pb2.py",
        "execution_stats_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "execution_stats_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "execution_stats_py_library",
    srcs = ["execution_stats_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "failure_details_python_compile",
    outputs = [
        "failure_details_pb2.py",
        "failure_details_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "failure_details_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "failure_details_py_library",
    srcs = ["failure_details_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "firecracker_python_compile",
    outputs = [
        "firecracker_pb2.py",
        "firecracker_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "firecracker_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "firecracker_py_library",
    srcs = ["firecracker_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "gcp_python_compile",
    outputs = [
        "gcp_pb2.py",
        "gcp_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "gcp_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "gcp_py_library",
    srcs = ["gcp_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "git_python_compile",
    outputs = [
        "git_pb2.py",
        "git_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "git_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "git_py_library",
    srcs = ["git_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "github_python_compile",
    outputs = [
        "github_pb2.py",
        "github_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "github_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "github_py_library",
    srcs = ["github_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "grp_python_compile",
    outputs = [
        "grp_pb2.py",
        "grp_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "grp_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "grp_py_library",
    srcs = ["grp_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "index_python_compile",
    outputs = [
        "index_pb2.py",
        "index_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "index_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "index_py_library",
    srcs = ["index_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "invocation_policy_python_compile",
    outputs = [
        "invocation_policy_pb2.py",
        "invocation_policy_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "invocation_policy_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "invocation_policy_py_library",
    srcs = ["invocation_policy_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "invocation_python_compile",
    outputs = [
        "invocation_pb2.py",
        "invocation_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "invocation_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "invocation_py_library",
    srcs = ["invocation_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "invocation_status_python_compile",
    outputs = [
        "invocation_status_pb2.py",
        "invocation_status_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "invocation_status_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "invocation_status_py_library",
    srcs = ["invocation_status_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "iprules_python_compile",
    outputs = [
        "iprules_pb2.py",
        "iprules_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "iprules_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "iprules_py_library",
    srcs = ["iprules_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "kythe_service_grpc_py_library",
    srcs = ["kythe_service_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":kythe_service_py_library"],
)

proto_compile(
    name = "kythe_service_python_compile",
    outputs = [
        "kythe_service_pb2.py",
        "kythe_service_pb2.pyi",
        "kythe_service_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "kythe_service_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "kythe_service_py_library",
    srcs = ["kythe_service_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "metrics_python_compile",
    outputs = [
        "metrics_pb2.py",
        "metrics_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "metrics_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "metrics_py_library",
    srcs = ["metrics_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "option_filters_python_compile",
    outputs = [
        "option_filters_pb2.py",
        "option_filters_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "option_filters_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "option_filters_py_library",
    srcs = ["option_filters_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "package_load_metrics_python_compile",
    outputs = [
        "package_load_metrics_pb2.py",
        "package_load_metrics_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "package_load_metrics_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "package_load_metrics_py_library",
    srcs = ["package_load_metrics_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "pagination_python_compile",
    outputs = [
        "pagination_pb2.py",
        "pagination_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "pagination_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "pagination_py_library",
    srcs = ["pagination_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "ping_service_grpc_py_library",
    srcs = ["ping_service_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":ping_service_py_library"],
)

proto_compile(
    name = "ping_service_python_compile",
    outputs = [
        "ping_service_pb2.py",
        "ping_service_pb2.pyi",
        "ping_service_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "ping_service_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "ping_service_py_library",
    srcs = ["ping_service_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "publish_build_event_grpc_py_library",
    srcs = ["publish_build_event_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":publish_build_event_py_library"],
)

proto_compile(
    name = "publish_build_event_python_compile",
    outputs = [
        "publish_build_event_pb2.py",
        "publish_build_event_pb2.pyi",
        "publish_build_event_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "publish_build_event_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "publish_build_event_py_library",
    srcs = ["publish_build_event_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "quota_python_compile",
    outputs = [
        "quota_pb2.py",
        "quota_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "quota_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "quota_py_library",
    srcs = ["quota_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "raft_python_compile",
    outputs = [
        "raft_pb2.py",
        "raft_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "raft_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "raft_py_library",
    srcs = ["raft_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "raft_service_grpc_py_library",
    srcs = ["raft_service_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":raft_service_py_library"],
)

proto_compile(
    name = "raft_service_python_compile",
    outputs = [
        "raft_service_pb2.py",
        "raft_service_pb2.pyi",
        "raft_service_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "raft_service_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "raft_service_py_library",
    srcs = ["raft_service_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "registry_python_compile",
    outputs = [
        "registry_pb2.py",
        "registry_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "registry_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "registry_py_library",
    srcs = ["registry_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "remote_asset_grpc_py_library",
    srcs = ["remote_asset_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":remote_asset_py_library"],
)

proto_compile(
    name = "remote_asset_python_compile",
    outputs = [
        "remote_asset_pb2.py",
        "remote_asset_pb2.pyi",
        "remote_asset_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "remote_asset_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "remote_asset_py_library",
    srcs = ["remote_asset_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "remote_execution_log_python_compile",
    outputs = [
        "remote_execution_log_pb2.py",
        "remote_execution_log_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "remote_execution_log_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "remote_execution_log_py_library",
    srcs = ["remote_execution_log_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "remote_execution_grpc_py_library",
    srcs = ["remote_execution_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":remote_execution_py_library"],
)

proto_compile(
    name = "remote_execution_python_compile",
    outputs = [
        "remote_execution_pb2.py",
        "remote_execution_pb2.pyi",
        "remote_execution_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "remote_execution_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "remote_execution_py_library",
    srcs = ["remote_execution_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "repo_python_compile",
    outputs = [
        "repo_pb2.py",
        "repo_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "repo_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "repo_py_library",
    srcs = ["repo_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "resource_python_compile",
    outputs = [
        "resource_pb2.py",
        "resource_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "resource_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "resource_py_library",
    srcs = ["resource_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "runner_python_compile",
    outputs = [
        "runner_pb2.py",
        "runner_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "runner_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "runner_py_library",
    srcs = ["runner_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "scheduler_grpc_py_library",
    srcs = ["scheduler_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":scheduler_py_library"],
)

proto_compile(
    name = "scheduler_python_compile",
    outputs = [
        "scheduler_pb2.py",
        "scheduler_pb2.pyi",
        "scheduler_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "scheduler_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "scheduler_py_library",
    srcs = ["scheduler_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "search_python_compile",
    outputs = [
        "search_pb2.py",
        "search_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "search_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "search_py_library",
    srcs = ["search_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "secrets_python_compile",
    outputs = [
        "secrets_pb2.py",
        "secrets_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "secrets_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "secrets_py_library",
    srcs = ["secrets_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "semver_python_compile",
    outputs = [
        "semver_pb2.py",
        "semver_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "semver_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "semver_py_library",
    srcs = ["semver_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "server_notification_python_compile",
    outputs = [
        "server_notification_pb2.py",
        "server_notification_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "server_notification_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "server_notification_py_library",
    srcs = ["server_notification_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "sidecar_grpc_py_library",
    srcs = ["sidecar_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":sidecar_py_library"],
)

proto_compile(
    name = "sidecar_python_compile",
    outputs = [
        "sidecar_pb2.py",
        "sidecar_pb2.pyi",
        "sidecar_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "sidecar_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "sidecar_py_library",
    srcs = ["sidecar_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "soci_grpc_py_library",
    srcs = ["soci_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":soci_py_library"],
)

proto_compile(
    name = "soci_python_compile",
    outputs = [
        "soci_pb2.py",
        "soci_pb2.pyi",
        "soci_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "soci_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "soci_py_library",
    srcs = ["soci_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "spawn_diff_python_compile",
    outputs = [
        "spawn_diff_pb2.py",
        "spawn_diff_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "spawn_diff_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "spawn_diff_py_library",
    srcs = ["spawn_diff_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "spawn_python_compile",
    outputs = [
        "spawn_pb2.py",
        "spawn_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "spawn_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "spawn_py_library",
    srcs = ["spawn_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "stat_filter_python_compile",
    outputs = [
        "stat_filter_pb2.py",
        "stat_filter_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "stat_filter_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "stat_filter_py_library",
    srcs = ["stat_filter_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "stats_python_compile",
    outputs = [
        "stats_pb2.py",
        "stats_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "stats_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "stats_py_library",
    srcs = ["stats_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "stored_invocation_python_compile",
    outputs = [
        "stored_invocation_pb2.py",
        "stored_invocation_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "stored_invocation_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "stored_invocation_py_library",
    srcs = ["stored_invocation_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "strategy_policy_python_compile",
    outputs = [
        "strategy_policy_pb2.py",
        "strategy_policy_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "strategy_policy_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "strategy_policy_py_library",
    srcs = ["strategy_policy_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "suggestion_python_compile",
    outputs = [
        "suggestion_pb2.py",
        "suggestion_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "suggestion_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "suggestion_py_library",
    srcs = ["suggestion_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "target_pagination_python_compile",
    outputs = [
        "target_pagination_pb2.py",
        "target_pagination_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "target_pagination_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "target_pagination_py_library",
    srcs = ["target_pagination_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "target_python_compile",
    outputs = [
        "target_pb2.py",
        "target_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "target_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "target_py_library",
    srcs = ["target_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "telemetry_grpc_py_library",
    srcs = ["telemetry_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":telemetry_py_library"],
)

proto_compile(
    name = "telemetry_python_compile",
    outputs = [
        "telemetry_pb2.py",
        "telemetry_pb2.pyi",
        "telemetry_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "telemetry_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "telemetry_py_library",
    srcs = ["telemetry_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "trace_python_compile",
    outputs = [
        "trace_pb2.py",
        "trace_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "trace_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "trace_py_library",
    srcs = ["trace_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "usage_python_compile",
    outputs = [
        "usage_pb2.py",
        "usage_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "usage_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "usage_py_library",
    srcs = ["usage_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "user_id_python_compile",
    outputs = [
        "user_id_pb2.py",
        "user_id_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "user_id_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "user_id_py_library",
    srcs = ["user_id_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "user_python_compile",
    outputs = [
        "user_pb2.py",
        "user_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "user_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "user_py_library",
    srcs = ["user_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "vfs_grpc_py_library",
    srcs = ["vfs_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":vfs_py_library"],
)

proto_compile(
    name = "vfs_python_compile",
    outputs = [
        "vfs_pb2.py",
        "vfs_pb2.pyi",
        "vfs_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "vfs_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "vfs_py_library",
    srcs = ["vfs_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "vmexec_grpc_py_library",
    srcs = ["vmexec_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":vmexec_py_library"],
)

proto_compile(
    name = "vmexec_python_compile",
    outputs = [
        "vmexec_pb2.py",
        "vmexec_pb2.pyi",
        "vmexec_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "vmexec_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "vmexec_py_library",
    srcs = ["vmexec_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

grpc_py_library(
    name = "vmvfs_grpc_py_library",
    srcs = ["vmvfs_pb2_grpc.py"],
    visibility = ["//visibility:public"],
    deps = [":vmvfs_py_library"],
)

proto_compile(
    name = "vmvfs_python_compile",
    outputs = [
        "vmvfs_pb2.py",
        "vmvfs_pb2.pyi",
        "vmvfs_pb2_grpc.py",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
        "@build_stack_rules_proto//plugin/grpc/grpc:protoc-gen-grpc-python",
    ],
    proto = "vmvfs_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "vmvfs_py_library",
    srcs = ["vmvfs_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "worker_python_compile",
    outputs = [
        "worker_pb2.py",
        "worker_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "worker_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "worker_py_library",
    srcs = ["worker_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "workflow_python_compile",
    outputs = [
        "workflow_pb2.py",
        "workflow_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "workflow_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "workflow_py_library",
    srcs = ["workflow_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "workspace_python_compile",
    outputs = [
        "workspace_pb2.py",
        "workspace_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "workspace_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "workspace_py_library",
    srcs = ["workspace_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)

proto_compile(
    name = "zip_python_compile",
    outputs = [
        "zip_pb2.py",
        "zip_pb2.pyi",
    ],
    plugins = [
        "@build_stack_rules_proto//plugin/builtin:pyi",
        "@build_stack_rules_proto//plugin/builtin:python",
    ],
    proto = "zip_proto",
    visibility = ["//visibility:public"],
)

proto_py_library(
    name = "zip_py_library",
    srcs = ["zip_pb2.py"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:protobuf_python"],
)
