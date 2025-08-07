generate:
  rm -rf stackcoin
  uvx openapi-python-client generate --url http://localhost:4000/api/openapi --config openapi-python-client-config.yml
  uvx ruff format

dev:
  uv pip install -e "stackcoin @ ./stackcoin"

