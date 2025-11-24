FROM python:3.11

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Set a working directory
WORKDIR /workspace

COPY vllm_llm.sh vllm_embedding.sh /workspace/

RUN apt-get update -y && \
    apt-get install -y netcat-traditional && \
    pip install --upgrade pip

RUN pip cache purge

RUN pip install --no-cache-dir vllm==0.7.2
RUN pip install --no-cache-dir transformers==4.54.0
RUN chmod +x /workspace/vllm_llm.sh /workspace/vllm_embedding.sh

CMD ["bash"]
