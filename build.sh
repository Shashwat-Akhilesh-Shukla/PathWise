#!/usr/bin/env bash
set -e

# Install libGL for OpenCV (krutrim_cloud dependency)
apt-get update && apt-get install -y libgl1

pip install -r requirements.txt
