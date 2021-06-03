import stat_loader
import class_sum

import json
import tkinter as tk

import flask


def make_server(data):
    app = flask.Flask(__name__)

    totals = class_sum.sum_classes(data)

    def get_lines(dct: dict, indent=True) -> list[tuple[int, str, str]]:  # (indent, key, value)
        out = []
        for key, val in dct.items():
            if isinstance(val, dict):
                new_out = get_lines(val, indent)
                if len(new_out):
                    out.append((int(indent), str(key), ''))
                    out += new_out
                    out[-1] = (int(-indent), *out[-1][1:])
            else:
                out.append((0, str(key), str(val)))
        return out

    @app.route('/')
    def main():
        lines = get_lines(totals)
        return flask.render_template("line_template.html", lines=lines)

    return app


if __name__ == '__main__':
    server = make_server(stat_loader.load_stats())
    server.run()
