import argparse
import pathlib
import numpy as np

import cv2 as cv
import glob
import os
import re


parser = argparse.ArgumentParser()

parser.add_argument('--games-folder', type=pathlib.Path, required=True, help='Game folder')
parser.add_argument('--output-folder', type=pathlib.Path, required=True, help='Good games output folder')
parser.add_argument('--quality', type=int, required=True, help='Conversion Quality')
parser.add_argument('--size-ratio', type=float, required=True, help='Size ratio')

args = parser.parse_args()

gamesFolder:str = str(args.games_folder)
outputFolder:str = str(args.output_folder)
imageQuality:int = args.quality
sizeRatio:float = args.size_ratio

if not os.path.exists(gamesFolder):
    print("Error: source folder does not exist")
    exit(-1)


searchStr = rf'{os.path.join(gamesFolder, "**","*.png")}'
pngFilePaths = glob.glob(searchStr, recursive=True,)
print("Info: %s image files found" % len(pngFilePaths))

if len(pngFilePaths) == 0:
    print("Info: Nothing to do...")

for i, pngFilePath in enumerate(pngFilePaths):
    print("Info: Converting %s/%s -> %s" % (i,len(pngFilePaths), pngFilePath))
    jpgFilePath = os.path.relpath(pngFilePath,gamesFolder)
    jpgFilePath = os.path.join(outputFolder, jpgFilePath[:-3] + "jpg");

    dirPath=os.path.dirname(jpgFilePath)
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

    # Load .png image
    img = cv.imdecode(np.fromfile(pngFilePath, dtype=np.uint8), cv.IMREAD_UNCHANGED)
    img = cv.resize(img, (0, 0), fx=sizeRatio, fy=sizeRatio)

    # Save .jpg image
    is_success, im_buf_arr = cv.imencode(".jpg",img, [cv.IMWRITE_JPEG_QUALITY, imageQuality] )
    im_buf_arr.tofile(jpgFilePath)

