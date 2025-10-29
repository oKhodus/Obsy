# v.python
FROM python:3.11-slim

# work dir
WORKDIR /Obsy

# copy requirements
COPY requirements.txt .

# install requirements
RUN pip install --no-cache-dir -r requirements.txt

# copy all project's code to the container
COPY . .

# cmd run
CMD [ "python", "generate.py"]