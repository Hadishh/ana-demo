#!/usr/bin/env bash

echo $OPENAI_API_KEY
# now every variable in .env is in your environment
vllm serve $EMBEDDER_PATH --served-model-name $EMBEDDER_MODEL_NAME \
    --dtype auto --api-key $OPENAI_API_KEY  \
    --host 0.0.0.0 --port 25602 --enforce-eager 