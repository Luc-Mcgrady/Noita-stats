import flask
from matplotlib import pyplot as plt

import class_sum
import dict_flatten
import stat_loader


def make_server(data):
    app = flask.Flask(__name__)

    totals = class_sum.sum_classes(data)
    lines = dict_flatten.get_lines(totals)

    for line in lines:
        line.key = line.key.replace('_', ' ')

    @app.route('/')
    def main():
        return flask.render_template("line_template.html", lines=lines)

    @app.route('/graph/<path:key_path>')
    def graph(key_path: str):

        def get_keys(dct: dict, keys: list[str]):
            to_get = dct
            for key in keys:
                if not isinstance(to_get, dict):
                    to_get = to_get.__dict__
                to_get = to_get.get(key, 0)
            return to_get

        key_path = key_path.split('/')

        to_plot = [get_keys(a.__dict__, key_path) for a in data.values()]

        plt.close()
        plt.plot([str(a) for a in range(len(to_plot))], to_plot)
        plt.show()

        return '', 204

    return app


if __name__ == '__main__':
    server = make_server(stat_loader.load_stats())
    server.run()
