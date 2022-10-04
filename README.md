# 🎼 cadenza 🎶

[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## what is it?

cadenza is a browser based [pyteal](https://github.com/algorand/pyteal) editor & compiler, built for algorand's 2022 Q1 internal hackathon. 

it can currently deploy stateful apps as well, but there is no UI feature to interact with them (yet!).

[live demo here](http://35.222.183.190:5000/): but it is probably better to run it locally and consider it as a UI to your sandbox for now.

## installation

Make sure you have [sandbox](https://github.com/algorand/sandbox) running. 

- clone this repo
- `cd src/server` 
- `python -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`
- Start the server with `python app.py` or `flask run --host=0.0.0.0`

Now you should see the editor at `http://localhost:5000`. 


## how do i use it?
* you can use the editor to input your own pyteal code.
* there is some default boilerplate code available for you, and you can find more useful utils at the [pyteal-utils](https://github.com/algorand/pyteal-utils) repo. 
* pyteal written in cadenza **must** have the `router` object as the entry point for stateful apps, and the approval and clear state program will automatically be generated from this.
* the compiler always compiles to the latest pyteal version available.
* compile button tries to compile the pyteal and upon success, returns the base64 encoding of the program.
* deploy button tries to compile and deploy the program on a private network on sandbox (on dev mode, so consensus and block finality is immediate!), and upon success, returns the application creation response.
* double clicking the console will clear all the logs.

## how was it built?
* frontend: mostly vanilla javascript with the [ace editor](https://ace.c9.io/) integration
* backend: python & flask, with help from pyteal, py-algorand-sdk, and sandbox

![cadenza architecture](https://user-images.githubusercontent.com/86622919/162258699-9708ea60-6c79-44f0-ae16-fdbab13881bb.png)

## tests
there aren't that many tests right now, but you can run them by booting up a default sandbox instance and running:
`python -m pytest`

## bugs 🐞
use at your own risk! 

report them to [me](https://github.com/algochoi) on github or open up an issue in the repo 🎶. 

pr's are always welcomed 🎼
