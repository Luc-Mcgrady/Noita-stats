# This is the file that is compiled for releases
import flask
import webbrowser
from matplotlib import pyplot as plt

import class_sum
import dict_flatten
import stat_loader


def get_keys(keys: list[str], dct: dict):
    """Go several keys into a dict"""
    to_get = dct
    for key in keys:
        if not isinstance(to_get, dict):  # Get attributes if object isn't dict
            to_get = to_get.__dict__
        to_get = to_get.get(key, 0)
    return to_get


def graph_keys(key_path: list[str], data: dict):
    """Redundant function which I planned to use in both the graph and graph/time functions but became overly complex"""
    to_plot = [get_keys(key_path, a.__dict__) for a in data.values()]

    plt.plot([str(a) for a in range(len(to_plot))], to_plot)


def make_server(data: dict[str, dict]):
    app = flask.Flask(__name__)

    totals = class_sum.sum_dict_classes(data)
    lines = dict_flatten.get_lines(totals)

    for line in lines:
        line.key = line.key.replace('_', ' ')

    @app.route('/')
    def main():
        return flask.render_template("line_template.html", lines=lines)

    @app.route('/graph/<path:key_path>')
    def graph(key_path: str):
        key_path_array = key_path.split('/')

        plt.close()
        graph_keys(key_path_array, data)
        plt.title(f"Graph of \"{key_path.replace('_', ' ')}\" per run")

        plt.show()

        return '', 204  # Returns nothing to prevent website switch

    @app.route('/graph_time/<path:key_path>')
    def graph_over_time(key_path: str):
        key_path_array = key_path.split('/')
        to_plot = [
            get_keys(key_path_array, a.__dict__) / get_keys(["stats", "playtime"], a.__dict__)
            # Only functional difference from regular graph function ^
            for a in data.values()]

        plt.close()
        plt.plot([str(a) for a in range(len(to_plot))], to_plot)
        plt.title(f"Graph of\n\"{key_path.replace('_', ' ')}\"\ndivided by playtime per run")

        plt.show()

        return '', 204  # Returns nothing to prevent website switch

    return app


if __name__ == '__main__':
    server = make_server(stat_loader.load_stats())
    webbrowser.open("http://127.0.0.1:5010")  # Relies on browser being slower than server start
    server.run(port="5010", threaded=False)
