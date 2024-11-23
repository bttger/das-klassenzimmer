from google_images_search import GoogleImagesSearch
import dotenv
import os
from typing import List

# you can provide API key and CX using arguments,
# or you can set environment variables: GCS_DEVELOPER_KEY, GCS_CX
dotenv.load_dotenv()

gis = GoogleImagesSearch(os.getenv("GCS_DEVELOPER_KEY"), os.getenv("GCS_CX"))


def search_prompts_and_save_imgs(prompts: List[str], save_location_dir: str):
    result_paths = []
    for prompt in prompts:
        _search_params = {
            "q": prompt,
            "num": 1,
            "imgType": "photo",
        }
        gis.search(search_params=_search_params)
        for image in gis.results():
            image.download(save_location_dir)
            result_paths.append(image.path)

    return result_paths


if __name__ == "__main__":
    prompts = [
        "electric vehicle",
        "solar energy",
        "renewable energy",
        "electric car",
        "e-bike",
        "solar panel",
    ]
    save_location_dir = "images"
    search_prompts_and_save_imgs(prompts, save_location_dir)
