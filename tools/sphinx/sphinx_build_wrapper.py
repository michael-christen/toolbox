import os
import shutil
import sys
import tempfile

import sphinx.cmd.build


def main():
    # In Bazel's linux-sandbox, the tree artifact containing the sphinx sources
    # is provided via a directory symlink (or file symlinks) into bazel-out.
    # This causes two problems:
    #
    # 1. MyST resolves relative .md links via os.path.realpath, giving bazel-out
    #    paths. Sphinx's env.srcdir must match those paths for env.path2doc() to
    #    convert them to docnames, or cross-file references break.
    #
    # 2. autoapi writes .rst files to {srcdir}/autoapi. If srcdir is bazel-out,
    #    that directory is read-only (completed build outputs).
    #
    # Fix: when symlinks are detected, copy the entire sandbox tree (following
    # symlinks) to a fresh tmpdir. With real files, realpath(file) == abspath(file),
    # so MyST and sphinx agree on srcdir, and autoapi can write freely.
    if len(sys.argv) >= 3:
        sandbox_srcdir = os.path.abspath(sys.argv[-2])
        needs_deref = False
        try:
            for f in os.listdir(sandbox_srcdir):
                fpath = os.path.join(sandbox_srcdir, f)
                if os.path.realpath(fpath) != os.path.abspath(fpath):
                    needs_deref = True
                    break
        except OSError:
            pass

        if needs_deref:
            sandbox_root = os.path.dirname(sandbox_srcdir)
            tmpdir = tempfile.mkdtemp()
            shutil.copytree(
                sandbox_root,
                tmpdir,
                symlinks=False,
                dirs_exist_ok=True,
                ignore_dangling_symlinks=True,
            )
            real_srcdir = os.path.join(tmpdir, os.path.basename(sandbox_srcdir))
            outdir = sys.argv[-1]
            sys.argv = sys.argv[:-2] + [real_srcdir, outdir]

    return sphinx.cmd.build.main()


if __name__ == "__main__":
    sys.exit(main())
