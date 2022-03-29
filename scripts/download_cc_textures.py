from sys import version_info, path
if version_info.major == 2:
    raise Exception("This script only works with python3.x!")

import os
import csv
import requests
path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.utility.SetupUtility import SetupUtility
from pathlib import Path
import shutil

if __name__ == "__main__":
    # setting the default header, else the server does not allow the download
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    # set the download directory relative to this one
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cc_texture_dir = os.path.join(current_dir, "..", "resources", "cctextures")

    if not os.path.exists(cc_texture_dir):
        os.makedirs(cc_texture_dir)
    else:
        pass
        # raise Exception("The folder already exists!")

    # download the csv file, which contains all the download links
    csv_url = "https://cc0textures.com/api/v1/downloads_csv"
    csv_file_path = os.path.join(cc_texture_dir, "full_info.csv")
    request = requests.get(csv_url, headers=headers)
    with open(csv_file_path, "wb") as file:
        file.write(request.content)

    # extract the download links with the asset name
    data = {}
    with open(csv_file_path, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for line in csv_reader:
            if line["Filetype"] == "zip" and line["DownloadAttribute"] == "2K-JPG":
                data[line["AssetID"]] = line["PrettyDownloadLink"]

    excluding_list = ["sign", "roadlines", "manhole", "backdrop", "foliage", "TreeEnd", "TreeStump",
                      "3DBread", "3DApple", "FlowerSet", "FoodSteps", "PineNeedles", "Grate",
                      "PavingEdge", "Painting", "RockBrush", "WrinklesBrush", "Sticker", "3DRock",
                      'Planks007', 'Chip002']

    # download each asset and create a folder for it (unpacking + deleting the zip included)
    for index, (asset, link) in enumerate(data.items()):
        do_not_use = False
        for exclude_element in excluding_list:
            if asset.lower().startswith(exclude_element.lower()):
                do_not_use = True
                break
        current_folder =  os.path.join(cc_texture_dir, asset)
        if Path(current_folder).exists():
            do_not_use = True
        if do_not_use:
            continue
        print("Download asset: {} of {}/{}".format(asset, index, len(data)))
        if not os.path.exists(current_folder):
            os.makedirs(current_folder)
        current_file_path = os.path.join(current_folder, "{}.zip".format(asset))
        response = requests.get(link, headers=headers)
        try:
            SetupUtility.extract_from_response(current_folder, response)
        except:
            shutil.rmtree(current_folder)
            print("add to excluding list", asset)


    print("Done downloading textures, saved in {}".format(cc_texture_dir))