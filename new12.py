import asyncio

import httpx
import requests
import re
from bs4 import BeautifulSoup
import json
import html
import pandas as pd
import openpyxl as xls
import time

variations = []
liste = []
res = []
links = []


async def get_data(client, x):
    global group_link, linkler
    url = "https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll/trendyolmilla-elbise-x-b101476-c56"
    querystring = {"pi": f"{x}", "culture": "tr-TR", "userGenderId": "1", "pId": "0", "scoringAlgorithmId": "2",
                   "categoryRelevancyEnabled": "false", "isLegalRequirementConfirmed": "false",
                   "searchStrategyType": "DEFAULT", "productStampType": "TypeA"}
    headers = {
        "cookie": "__cflb=02DiuFo6dq2oaeSzjVDtZq29bSZMcYKtvJoVP6um1T71W; _cfuvid=Defb5B4o1Tzz_IqY.wZrqZ3kRMd_tOMcpG1zwFBUhjU-1649218660271-0-604800000",
        "authority": "public.trendyol.com",
        "sec-ch-ua": "^\^"
    }

    # Extract Product data from the response JSON

    r = await client.get(url, headers=headers, params=querystring, timeout=None)
    try:
        data = r.json()
        products = data.get("result", {}).get("products", [])
        for product in products:
            product_name = product.get("name", "")
            brand = product.get('brand', {}).get("name")
            category = product.get("categoryName", "")
            list_price = product.get("price", {}).get("sellingPrice")
            sale_price = product.get("price", {}).get("discountedPrice")
            product_id = product.get("productGroupId", "")

            # Products URLS of Category we want to scrape
            product_url = f"https://trendyol.com{product.get('url', '')}"
            group_api = "https://public.trendyol.com/discovery-web-websfxproductgroups-santral/api/v1/product-groups/"
            group_link = group_api + str(product_id)

            links.append(group_link)

    except:
        pass
    return links


async def main():
    async with httpx.AsyncClient() as client:
        dnm = []
        x = range(1, 140)
        for item in x:
            res.append(get_data(client, item))

        results = await asyncio.gather(*res)
    return results


if __name__ == '__main__':
    start = time.perf_counter()
    res = asyncio.run(main())
    fin = time.perf_counter() - start

    df = pd.DataFrame(links)
    df.drop_duplicates(inplace=True)
    print(len(df))
    # drop first row
    # df = df.drop(df.index[0])

    # df.iloc[1:, :]
    # df.drop(df.columns, inplace=True, axis=1)
    # df = df.rename(columns={0: None})

    # Remove the header column
    # df = df.iloc[0:]

    # df = df.reset_index(drop=True)

    # df1 = df.tail(-1)
    # print(df1)
    # Check the updated dataframe
    # print(df.head())

    asd = df.to_csv('stores.txt', header=False, index=False)

    for link in links:
        print(link)
    print(len(df))
    print('Done')
    print(fin)
