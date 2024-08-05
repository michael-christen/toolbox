# Custom macros of common cc rules to enable common modifications
load("@rules_cc//cc:defs.bzl", _cc_library = "cc_library")

def cc_library(**kwargs):
    _cc_library(**kwargs)
