#!/usr/bin/env bash

echo $OPENAI_API_KEY

# now every variable in .env is in your environment
vllm serve $LLM_PATH --served-model-name $LLM_MODEL_NAME \
    --api-key $OPENAI_API_KEY  \
    --host 0.0.0.0 --port 25601 --tensor-parallel-size 2 \
    --max-model-len 32768