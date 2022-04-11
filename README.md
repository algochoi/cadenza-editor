# 🎼 cadenza 🎶

[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## what is it?

cadenza is a browser based [pyteal](https://github.com/algorand/pyteal) editor & compiler, built for algorand's 2022 Q1 internal hackathon. 

it can currently deploy stateful apps as well, but there is no UI feature to interact with them (yet!).

[live demo here](http://35.222.183.190:5000/): but it is probably better to run it locally and consider it as a UI to your sandbox for now.

## installation

### tldr

clone this repo, go into the `src/server` directory, then `pip install -r requirements.txt`. you can locally start your server by `flask run`, and you'll see the editor on localhost port 5000. in order to compile and deploy apps, you need to have [sandbox](https://github.com/algorand/sandbox) running. 

## how do i use it?
* you can use the editor to input your own pyteal code.
* there is some default boilerplate code available for you, and you can find more useful utils at the [pyteal-utils](https://github.com/algorand/pyteal-utils) repo. 
* pyteal written in cadenza **must** have the `approval()` function as the entry point for stateful apps.
* the clear program is always defined to be `int 1`.
* the compiler always compiles to the latest pyteal version available.
* compile button tries to compile the pyteal and upon success, returns the base64 encoding of the program.
* deploy button tries to compile and deploy the program on a private network on sandbox (on dev mode, so consensus and block finality is immediate!), and upon success, returns the application creation response.
* double clicking the console will clear all the logs.

## how was it built?
* frontend: mostly vanilla javascript with the [ace editor](https://ace.c9.io/) integration
* backend: python & flask, with help from pyteal, py-algorand-sdk, and sandbox

![cadenza architecture](https://user-images.githubusercontent.com/86622919/162258699-9708ea60-6c79-44f0-ae16-fdbab13881bb.png)

## bugs 🐞
use at your own risk! 

report them to [me](https://github.com/algochoi) on github or open up an issue in the repo 🎶. 

pr's are always welcomed 🎼
