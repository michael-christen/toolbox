"""Generate a baseline_coverage.dat to get accurate coverage.

`bazel coverage` doesn't include files that weren't included at all, here we
find all the other files we want and generate a baseline, which gets merged in
to the overall coverage report.
"""
import argparse
import glob
import pathlib
import subprocess


def main(root_dir: pathlib.Path):
    files = sorted(find_files(root_dir))
    for file in files:
        print('TN:')
        print(f'SF:{file}')
        print('DA:0,0')
        print('end_of_record')


def find_files(root_dir: pathlib.Path) -> list[pathlib.Path]:
    file_suffixes = [
        '.h',
        '.cc',
        '.rs',
        '.py',
    ]
    # Relative to root
    ignored_directories = [
        pathlib.Path(p) for p in [
            'nobazel',
            'tools',
        ]]
    suffix_args = []
    for i, suffix in enumerate(file_suffixes):
        suffix_args.extend(['-name', f'*{suffix}'])
        if i < len(file_suffixes) - 1:
            suffix_args.append('-o')
    # Using find rather than glob at the moment because it allows me to avoid
    # symlinks easily and I didn't want to bother with anything else
    find_result = subprocess.check_output(
        ['find', root_dir, '('] + suffix_args + [')']
    ).decode('utf-8')
    paths = []
    for line in find_result.splitlines():
        found_path = pathlib.Path(line).relative_to(root_dir)
        # Exclude ignored_directories
        ignore_file = False
        for ignore_dir in ignored_directories:
            if found_path.is_relative_to(ignore_dir):
                ignore_file = True
                break
        if ignore_file:
            continue
        paths.append(found_path)
    return paths


if __name__ == '__main__':
    # XXX: Pass it in
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', type=pathlib.Path)
    args = parser.parse_args()
    main(root_dir=args.root_dir)
