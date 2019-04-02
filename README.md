 # Chaos Toolkit Instana Extension

[![Build Status](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-instana.svg?branch=master)](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-instana)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-instana.svg)](https://www.python.org/)
[![Requirements Status](https://requires.io/github/chaostoolkit-incubator/chaostoolkit-instana/requirements.svg?branch=master)](https://requires.io/github/chaostoolkit-incubator/chaostoolkit-instana/requirements/?branch=master)
[![Has wheel](https://img.shields.io/pypi/wheel/chaostoolkit-instana.svg)](http://pythonwheels.com/)


This extension package provides probes and actions for Chaos Engineering
experiments against a Instana instance using the
[Chaos Toolkit][chaostoolkit].

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org

## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```
$ pip install -U chaostoolkit-instana
```

## Usage

To use the probes and actions from this package, add the following to your
experiment file. The from_time and to_time are milliseconds sincee epoche.  If 
the from_time and to_time are omitted, no events will 
be returned. If you just specify from_time events will be returned from the time value given to the curent time. 

```json
	{
        "type": "probe",
        "name": "get-all-events-in-window-from-instana",
        "provider": {
            "secrets": ["instana"],
            "type": "python",
            "module": "chaosinstana.probes",
                "func": "get_all_events_in_window",
                "arguments": {
                    "from_time": "1554143400000",
                    "to_time": "1554237055206"
                }
        }
    }
```
Using fluent time ranges

```json
	{
        "type": "probe",
        "name": "get-all-events-in-window-from-instana",
        "provider": {
            "secrets": ["instana"],
            "type": "python",
            "module": "chaosinstana.probes",
                "func": "get_all_events_in_window",
                "arguments": {
                        "from_time": "10 minutes ago",
                        "to_time": "5 minutes ago"
                }
        }
    }
```
That's it!

Please explore the code to see existing probes and actions.

## Samples

Samples are provided in the samples directory

* [Sample showing retrieving all events in a specific millisecond-specified time window](samples/all-events-experiment-millis-window.json)
* [Sample showing retrieving all events from five minutes ago to now](samples/all-events-experiment-5-mins-ago-window.json)

* [Sample showing retrieving all events from 10 minutes ago to 5 minutes ago](samples/all-events-experiment-from-10-mins-ago-to-5-mins-ago.json)

* [Sample attempting to retrieve events with no window specified - this gives an empty result set](samples/all-events-experiment-no-window.json)

* [Sample showing retrieving all events from a specified time in milliseconds](samples/all-events-to-current-time-experiment.json)


## Configuration

This extension to the Chaos Toolkit need's an API token that's passed as a 
secret - here we are getting the secret from the environment, we also use 
configuration to specify the instana_host as this changes depending on the way you use instana.

```json
 {
     "secrets": {
        "instana": {
            "instana_api_token": {
                "type": "env",
                "key": "INSTANA_API_TOKEN"
            }
        }
    },
    "configuration": {
            "instana_host": "https://instana-project.instana.io"
    }
 }
```
## Test

To run the tests for the project execute the following:

```
$ pip install -r requirements-dev.txt -r requirements.txt
$ pytest
```


## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt
```

Then, point your environment to this directory:

```console
$ python setup.py develop
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.


