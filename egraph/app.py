import argparse
import os

import flask
import pandas as pd
from six.moves import configparser
from six.moves.urllib import parse


app = flask.Flask(__name__)
app.config['DEBUG'] = True


def get_app():
    return app

def format_for_highcharts(df):
    """
    see https://www.highcharts.com/demo
    :param df: pd.DataFrame
    :return:
    """
    print(df)
    df.index = list(df.index.fillna('NODATA'))
    categories = list(df.columns.fillna('NODATA'))

    df = df.fillna(0)
    series = [{'name': i, 'data': list(map(str, row))} for i, row in df.iterrows()]
    return {'categories': categories, 'series': series}


@app.route("/", methods=['GET'])
def index():
    print(os.getcwd())
    return flask.render_template('index.html')


@app.route("/graph", methods=['GET'])
def graph():
    print(os.getcwd())
    df = pd.read_csv('sample_data/tepco.csv', index_col=0)
    return flask.jsonify(format_for_highcharts(df.T))

def parse_command_line_args():
    description = 'Starts the API service for egraph'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('config_file', type=str, nargs='?',
                        default='/etc/egraph.conf',
                        help='the path for the config file to be read.')
    return parser.parse_args()


def main():
    global config
    args = parse_command_line_args()
    config = configparser.ConfigParser()
    config.read(args.config_file)
    try:
        host = config.get('default', 'host')
    except (configparser.NoOptionError, KeyError, configparser.NoSectionError):
        host = '127.0.0.1'
    try:
        port = config.getint('default', 'port')
    except (configparser.NoOptionError, KeyError, configparser.NoSectionError):
        port = 5000
    app.run(debug=True, host=host, port=port)


if __name__ == '__main__':
    main()
