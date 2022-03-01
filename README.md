
## Building

Build is done via github actions. Locally, you can test the release builds as follows:

```bash
docker buildx build \
    --tag base \
    --target base \
    --file ./Build/release/backend/Dockerfile .

docker buildx build \
    --tag realfullstack/backend/main_dev:local \
    --target main_dev \
    --file ./Build/release/backend/Dockerfile .

docker buildx build \
    --tag realfullstack/backend/nginx:local \
    --target nginx \
    --file ./Build/release/backend/Dockerfile .

```
