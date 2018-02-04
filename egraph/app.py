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
    #df.index = list(df.index.fillna('NODATA'))
    #categories = list(df.columns.fillna('NODATA'))
    print(df)

    #df = df.fillna(0)
    #for i, d in df.iteritems():
        #print(i, d)
        #print("==== %s" % (i.replace('kW', '')))
    #series = [{'name': i, 'data': list(map(str, row.replace('kw', '')))} for i, row in df.iterrows()]
    data = []
    for d in df.iteritems():
        data.append(d)
    series = [{'name': i, 'data': row} for i, row in df.iteritems()]
    return {'key': 'usage', 'values': [0.1,0.2,0.3,0.4] }


@app.route("/", methods=['GET'])
def index():
    return flask.render_template('index.html')


@app.route("/graph", methods=['GET'])
def graph():
    df = pd.read_csv('sample_data/tepco.csv', index_col=4)
    #print(df)
    #df = df.reset_index(drop=True)
    return flask.jsonify(format_for_highcharts(df.iloc[0:,8]))

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
        port = 8000
    app.run(debug=True, host=host, port=port)


if __name__ == '__main__':
    main()
