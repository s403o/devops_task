# Use a minimal base image cleaned from vulnarabilities
FROM public.ecr.aws/docker/library/python:alpine3.19

# Set working directory
WORKDIR /app

# Upgrade pip to the latest version
RUN python -m pip install --no-cache-dir --upgrade pip

COPY . /app

# Install dependencies and remove package cache
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

# Set environment variable for port
ENV PORT=5000

# Expose the port
EXPOSE $PORT

# Set the entrypoint and command
CMD ["python", "app.py"]
