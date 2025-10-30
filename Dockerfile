# v.python
FROM python:3.13-slim

# work dir
WORKDIR /Obsy

# copy requirements
COPY requirements.txt .

# install requirements
RUN pip install --no-cache-dir -r requirements.txt

# copy all project's code to the container
COPY . .

# CPU-only
ENV LLAMA_CUDA=0

# cmd run
CMD [ "python", "generate.py"]

# docker run -it --rm -v $(pwd)/models:/Obsy/models obsy-gpt4all