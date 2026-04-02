import os
import sys

import sphinx.cmd.build


def main():
    # In Bazel's linux-sandbox, the srcdir directory itself is real/writable,
    # but its files are symlinks into the read-only execroot. MyST resolves
    # relative .md links via os.path.realpath on those symlinks, giving
    # execroot paths. Sphinx's env.srcdir must match those paths for
    # env.path2doc() to
    # convert them to docnames, so we derive the execroot-based srcdir from a
    # file symlink.
    #
    # autoapi writes .rst files to {srcdir}/autoapi; with the execroot srcdir
    # that would hit a read-only filesystem, so we override autoapi_root to
    # point back to the writable linux-sandbox srcdir.
    if len(sys.argv) >= 3:
        sandbox_srcdir = os.path.abspath(sys.argv[-2])
        execroot_srcdir = sandbox_srcdir
        for f in os.listdir(sandbox_srcdir):
            freal = os.path.realpath(os.path.join(sandbox_srcdir, f))
            fdir = os.path.dirname(freal)
            if fdir != sandbox_srcdir:
                execroot_srcdir = fdir
                break
        if execroot_srcdir != sandbox_srcdir:
            outdir = sys.argv[-1]
            sys.argv = (
                sys.argv[:-2]
                + [
                    "-D",
                    "autoapi_root=" + os.path.join(sandbox_srcdir, "autoapi"),
                ]
                + [execroot_srcdir, outdir]
            )
    return sphinx.cmd.build.main()


if __name__ == "__main__":
    sys.exit(main())
