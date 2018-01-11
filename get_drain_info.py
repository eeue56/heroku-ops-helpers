import requests 
import sys 
import argparse
from multiprocessing import Pool



def heroku_get(url, extra_headers={}):
    headers = { 'Accept': 'application/vnd.heroku+json; version=3'}
    headers.update(extra_headers)
    r = requests.get(url, headers=headers)

    return r.json()

def get_pipeline_apps(pipeline_id):
    return heroku_get(f'https://api.heroku.com/pipelines/{pipeline_id}/pipeline-couplings')

def get_log_drains(app_id):
    return heroku_get(f'https://api.heroku.com/apps/{app_id}/log-drains')

def get_app_info(app_id):
    return heroku_get(f'https://api.heroku.com/apps/{app_id}')


def build_app_drain_info(app_id):
    app_info = get_app_info(app_id)

    info = []
    info.append(f'App {app_info["name"]}')

    log_drains = get_log_drains(app_id)

    if len(log_drains) == 0:
        info.append('****  No log drains found!! ****')
    else:
        info.append(str([drain['url'] for drain in log_drains]))

    return info

def app_drain_info(app):
    return '\n'.join(build_app_drain_info(app['app']['id']))


def main():
    parser = argparse.ArgumentParser(description='Print drain information about all apps in a pipeline or a single app')

    parser.add_argument(
        '--pipeline',
        '-p',
        help='pipeline name',
        default=None
    )

    parser.add_argument(
        '--app',
        '-a',
        help='app name',
        default=None
    )

    args = parser.parse_args()

    if args.pipeline is None and args.app is None:
        print('Nothing to do..')
    elif args.pipeline:
        print('Getting pipeline apps...')
        apps = get_pipeline_apps(args.pipeline)

        to_print_info = []
        p = Pool(10)
        to_print_info = p.map(app_drain_info, apps)

        print('\n'.join(to_print_info))
    else:
        print('Getting app drain info...')
        print(app_drain_info(args.app))

if __name__ == '__main__':
    main()