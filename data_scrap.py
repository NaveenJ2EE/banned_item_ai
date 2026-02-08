from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()

arguments = {
    "keywords": "gun,pistol,revolver",
    "limit": 500,
    "format": "jpg",
    "output_directory": "data/train/gun",
    "no_directory": False
}

response.download(arguments)