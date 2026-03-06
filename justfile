stackcoin_root := env("STACKCOIN_ROOT", "../StackCoin")

generate:
  datamodel-codegen \
    --input {{stackcoin_root}}/openapi.json \
    --input-file-type openapi \
    --output-model-type pydantic_v2.BaseModel \
    --output src/stackcoin/models.py \
    --target-python-version 3.13 \
    --output-datetime-class datetime
  uvx ruff format src/
