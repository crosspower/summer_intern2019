import math
import os
from importlib import import_module

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

import services

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


class Search(BaseModel):
    search_word: str


@app.post("/")
async def root(search: Search):
    result = []
    for service_name in services.__all__:
        service_module = import_module("services." + service_name)

        result.extend(service_module.get_product_info(search.search_word))
    # 価格が安い順にソート
    return sorted(result,
                  key=lambda product: product['price']
                  if product['price'] != None else math.inf)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
