# heroku-ops-helpers
Helpers for working with Heroku

## Installation

- Heroku CLI
- Python 3.6
- `pip install requests`


## Usage

### Get drain info

Useful for making sure that all your apps have the right logs set up.

```
usage: get_drain_info.py [-h] [--pipeline PIPELINE] [--app APP]

Print drain information about all apps in a pipeline or a single app

optional arguments:
  -h, --help            show this help message and exit
  --pipeline PIPELINE, -p PIPELINE
                        pipeline name
  --app APP, -a APP     app name
```

### Get env info

Get all the config env variables. Optionally give a name of a varaiable to get.

```
usage: get_env_var_info.py [-h] [--pipeline PIPELINE] [--app APP]
                           [--name NAME]

Print env about all apps in a pipeline or a single app

optional arguments:
  -h, --help            show this help message and exit
  --pipeline PIPELINE, -p PIPELINE
                        pipeline name
  --app APP, -a APP     app name
  --name NAME           env name to get
```