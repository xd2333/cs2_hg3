import os
import sys
from typing import List, Tuple
from pathlib import Path
from PIL import Image


class SegmentInfo:
    def __init__(self, index: str, x: int, y: int, fwidth: int, fheight: int):
        self.Index = index
        self.X = x
        self.Y = y
        self.FullWidth = fwidth
        self.FullHeight = fheight


def main(folder: str):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".hg3"):
                strFile = os.path.join(root, file)
                print(strFile)
                offset_table = get_offset_table(strFile)

                if len(offset_table) > 1:
                    working_dir = strFile[:-4] + os.sep
                    if not os.path.exists(working_dir):
                        os.mkdir(working_dir)
                    make_hg3_info(strFile)
                    enlarge_segments(strFile, offset_table)


def make_hg3_info(strFile: str):
    working_dir = strFile[:-4] + os.sep

    newName = f"{working_dir}[{Path(strFile).stem}].png"

    # Save transparent img named "[XXXX]" as HG3 info
    image = Image.new("RGBA", (10, 10))
    image.save(newName)


def enlarge_segments(strFile: str, offset_table: List[SegmentInfo]):
    working_dir = strFile[:-4] + os.sep
    base_dir = strFile.split(os.sep)[0]+os.sep
    for info in offset_table:
        name_org = f"{working_dir}{Path(strFile).stem}_{info.Index.zfill(4)}.png"
        newName = f"{working_dir}{info.Index}.png"

        if not os.path.exists(name_org):
            continue

        image = Image.new("RGBA", (info.FullWidth, info.FullHeight))
        img_org = Image.open(name_org)

        image.paste(img_org, (info.X, info.Y))
        image.save(newName)
        print(f"org: {name_org}，dst: {newName}")
        print(
            f"Index: {info.Index}, X: {info.X}, Y: {info.Y}, W: {info.FullWidth}, H: {info.FullHeight}")
        os.remove(name_org)


def get_offset_table(strFileName: str) -> List[SegmentInfo]:
    with open(strFileName, "rb") as f:
        byteBuffer = f.read()

    intPos = byteBuffer.find(b"stdinfo\x00")
    intCrtPos = intPos

    list_segments = []
    while intPos != -1:
        index = int.from_bytes(
            byteBuffer[intPos - 4:intPos], byteorder="little")
        intX = int.from_bytes(
            byteBuffer[intPos + 28:intPos + 32], byteorder="little")
        intY = int.from_bytes(
            byteBuffer[intPos + 32:intPos + 36], byteorder="little")
        intW = int.from_bytes(
            byteBuffer[intPos + 36:intPos + 40], byteorder="little")
        intH = int.from_bytes(
            byteBuffer[intPos + 40:intPos + 44], byteorder="little")

        list_segments.append(SegmentInfo(str(index), intX, intY, intW, intH))

        intPos = byteBuffer.find(b"stdinfo\x00", intPos + 8)

    return list_segments


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python script.py <folder>")
        sys.exit()

    folder = sys.argv[1]
    main(folder)
