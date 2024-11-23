from google_images_search import GoogleImagesSearch
import dotenv
import os
# you can provide API key and CX using arguments,
# or you can set environment variables: GCS_DEVELOPER_KEY, GCS_CX
dotenv.load_dotenv()

gis = GoogleImagesSearch(os.getenv('GCS_DEVELOPER_KEY'), os.getenv('GCS_CX'))

# define search params
# option for commonly used search param are shown below for easy reference.
# For param marked with '##':
#   - Multiselect is currently not feasible. Choose ONE option only
#   - This param can also be omitted from _search_params if you do not wish to define any value
_search_params = {
    'q': 'amnestiy international',
    'num': 1,
}


# search first, then download and resize afterwards:
gis.search(search_params=_search_params)
for image in gis.results():
    image.url  # image direct url
    image.referrer_url  # image referrer url (source)

    image.download('.')  # download image
    image.resize(500, 500)  # resize downloaded image

    image.path  # downloaded local file path