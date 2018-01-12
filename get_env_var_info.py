import requests 
import sys 
import argparse
from multiprocessing import Pool
import functools


def heroku_get(url, extra_headers={}):
    headers = { 'Accept': 'application/vnd.heroku+json; version=3'}
    headers.update(extra_headers)
    r = requests.get(url, headers=headers)

    return r.json()

def get_pipeline_apps(pipeline_id):
    return heroku_get(f'https://api.heroku.com/pipelines/{pipeline_id}/pipeline-couplings')

def get_env_vars(app_id):
    return heroku_get(f'https://api.heroku.com/apps/{app_id}/config-vars')

def get_app_info(app_id):
    return heroku_get(f'https://api.heroku.com/apps/{app_id}')


def build_app_env_info(app_id, env_to_find=None):
    app_info = get_app_info(app_id)

    info = []
    info.append(f'App {app_info["name"]}')

    env_vars = get_env_vars(app_id)

    if env_to_find is None:
        info.append(str(env_vars))
    else:
        if env_to_find in env_vars:
            info.append(env_vars[env_to_find])
        else:
            info.append('****  Var not found!! ****')

    return info

def app_env_info(app, env_to_find=None):
    return '\n'.join(build_app_env_info(app['app']['id'], env_to_find))


def main():
    parser = argparse.ArgumentParser(description='Print env about all apps in a pipeline or a single app')

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

    parser.add_argument(
        '--name',
        help='env name to get',
        default=None
    )

    args = parser.parse_args()

    if args.pipeline is None and args.app is None:
        print('Nothing to do..')
        print('You need to tell me which pipeline or app to work with!')
    elif args.pipeline:
        if args.name:
            print(f'Finding the variable {args.name} in the given pipeline..')
        else:
            print('Getting env info for apps in the given pipeline...')
        apps = get_pipeline_apps(args.pipeline)

        p = Pool(10)
        to_print_info = p.map(functools.partial(app_env_info, env_to_find=args.name), apps)

        print('\n\n'.join(to_print_info))
    else:
        if args.name:
            print(f'Finding the variable {args.name} in the given app..')
        else:
            print('Getting app env info...')
        print(app_env_info(args.app, args.name))

if __name__ == '__main__':
    main()