#!/usr/bin/env bash
# enable auto-export
set -o allexport
# load all VAR=VALUE lines from .env
# (ignores blank lines and lines starting with “#”)
source .env
# disable auto-export
set +o allexport

echo $OPENAI_API_KEY
# now every variable in .env is in your environment
NVIDIA_VISIBLE_DEVICES=0 vllm serve $EMBEDDER_PATH --served-model-name e5-large \
    --dtype auto --api-key $OPENAI_API_KEY  \
    --host 0.0.0.0 --port 25602 --enforce-eager 