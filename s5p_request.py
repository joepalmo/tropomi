import argparse
from sentinelsat import SentinelAPI, geojson_to_wkt, read_geojson
import os
from tqdm import tqdm
from datetime import date

parser = argparse.ArgumentParser(description="download TROPOMI data")
parser.add_argument('product', type=str)

args = parser.parse_args()

DOWNLOAD_DIR = "../data/{}".format(args.product)

producttype_dict = {"NO2": "L2__NO2___",
                    "O3": "L2__O3____",
                    "HCHO": "L2__HCHO__",}

producttype = producttype_dict[args.product]

DHUS_USER = "s5pguest"
DHUS_PASSWORD = "s5pguest"
DHUS_URL = "https://s5phub.copernicus.eu/dhus/"

api = SentinelAPI(DHUS_USER, DHUS_PASSWORD, DHUS_URL)

date_range = ('20200314', '20200320')

footprint = geojson_to_wkt(read_geojson('geojson/LAbasin.geojson'))

query_body = {
        "date": date_range,
        "platformname": "Sentinel-5 Precursor",
        "producttype": producttype
    }

products = api.query(footprint, **query_body)

# display results
tqdm.write(
    (
        "Number of products found: {number_product}\n"
        "Total products size: {size:.2f} GB\n"
    ).format(
        number_product=len(products),
        size=api.get_products_size(products)
        )
)

api.download_all(products, directory_path=DOWNLOAD_DIR)
