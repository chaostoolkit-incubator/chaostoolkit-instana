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

To use the probes and actions from this package, add the following secrets and configuration to your environment or experiments file:

### Secrets 

* `INSTANA_API_TOKEN` - Token for accessing the Instana API

### Configuration

* `INSTANA_HOST` - Host of the Instana instance that you wish to connect to

A [collection of samples](samples/) are provided so you can see existing probes and actions.

### Discovery

You may use the Chaos Toolkit to discover the capabilities of this extension:

```
$ chaos discover chaostoolkit-instana --no-install
```

If you have logged in against a Instana environment, this will discover
information about it along the way.


## Configuration



## Test

To run the tests for the project execute the following:

```
$ pip install -r requirements-dev.txt
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
$ pip install -e .
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.
