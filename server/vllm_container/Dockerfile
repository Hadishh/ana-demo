FROM vllm/vllm-openai:v0.7.2


# Set a working directory
WORKDIR /workspace

COPY vllm_llm.sh vllm_embedding.sh /workspace/

RUN apt-get update -y && \
    apt-get install -y netcat-traditional && \
    pip install --upgrade pip

RUN chmod +x /workspace/vllm_llm.sh /workspace/vllm_embedding.sh

CMD ["bash"]
