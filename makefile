# name Docker-img
IMAGE_NAME = obsy-gpt4all

# path to the model
MODEL_DIR = $(PWD)/models

.PHONY: build run clean

# build Docker-img
build:
	docker build -t $(IMAGE_NAME) .

# run container
run:
	docker run -it --rm -v $(MODEL_DIR):/Obsy/models $(IMAGE_NAME)

# delete stopped containers
clean:
	docker system prune -f
