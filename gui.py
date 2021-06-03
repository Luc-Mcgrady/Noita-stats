import stat_loader
import class_sum
import dict_flatten

import flask


def make_server(data):
    app = flask.Flask(__name__)

    totals = class_sum.sum_classes(data)

    lines = dict_flatten.get_lines(totals)

    @app.route('/')
    def main():
        return flask.render_template("line_template.html", lines=lines)

    return app


if __name__ == '__main__':
    server = make_server(stat_loader.load_stats())
    server.run()
