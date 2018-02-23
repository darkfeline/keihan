import argparse
import csv
import sys

import jinja2


def main(argv):
    parser = argparse.ArgumentParser(prog=argv[0], description=__doc__)
    parser.add_argument('template')
    parser.add_argument('cluster_rows')
    args = parser.parse_args(argv[1:])
    _render(args.template, args.cluster_rows)


def _render(template_file: str, cluster_rows_file: str):
    env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)
    with open(template_file) as f:
        template = env.from_string(f.read())
    with open(cluster_rows_file) as f:
        reader = csv.reader(f, dialect='excel-tab')
        cluster_rows = list(reader)
    print(template.render({
        'clusters': cluster_rows,
    }))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
