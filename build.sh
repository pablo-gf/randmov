#!/usr/bin/env bash
apt-get update && apt-get install -y libfreetype6-dev libpng-dev
pip install -r requirements_web.txt