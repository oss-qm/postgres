#!/bin/bash

set -e

libtoolize
aclocal
autoreconf -fi -I config

