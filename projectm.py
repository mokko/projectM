"""
Count our *.tif|*.tiff files on M:\ and measure disk space
write a little report in dir sdata

"""
import json
import logging
import os
from os import scandir
from pathlib import Path

# import glob

start_dir = {
    "EM": "M:\MuseumPlus\Produktiv\Multimedia\EM",
    "AKu": "M:\MuseumPlus\Produktiv\Multimedia\AKU",
}


class ProjectM:
    def __init__(self) -> None:
        logging.basicConfig(
            datefmt="%Y%m%d %I:%M:%S %p",
            format="%(asctime)s ## %(message)s",
            filename="sdata/projectM.log",
            filemode="w",  # a=append
            level=logging.INFO,
        )
        self.cache_fn = "sdata/projectM.json"
        self.cache = {}

    def try_loop(self, g): #https://stackoverflow.com/questions/55265522/
        while True:
            try:
                yield next(g)
            except StopIteration:
                break
            except WinError as e:
                logging.error(f"WIN ERROR: {path}")
                continue

    def pathlib_scan(self) -> None:
        """Uses the newest library i.e. pathlib"""
        print("ENTERING PATHLIB SCAN")
        logging.info("PATHLIB SCAN")
        tif_count = 0
        total_size = 0
        for each in start_dir:
            print(f"ENTERING {each}")
            logging.info(f"STARTING on {start_dir[each]}")
            for path in self.try_loop(Path(start_dir[each]).rglob("*")):
                s = path.suffix.lower()
                if s == ".tif" or s == ".tiff":
                    path = path.resolve()
                    tif_count += 1
                    self.add_to_cache(path)
                    try:
                        size = path.stat().st_size
                    except FileNotFoundError:
                        logging.error(f"FILE NOT FOUND: {path}")
                        size = 0
                    # else:
                    #    logging.error(f"File FOUND: {path}")

                    total_size += size
                    short_path = Path(*path.parts[5:])
                    print(f"PL{tif_count}++{short_path} {size}")
                    # if tif_count == 20 or tif_count == 40:
                    #    break
                    if (tif_count / 5000).is_integer():
                        self.log_state(total_size, tif_count)
                        self.save_cache()  # how do we know it completed?
        self.save_cache()
        self.log_state(total_size, tif_count)
        logging.info("done")

    def log_state(self, size, count):
        size_in_gb = round(size / 1024 / 1024 / 1024, 1)  # KB->MB->GB
        logging.info(f"{count} tifs with a total size of {size_in_gb} GB")

    def add_to_cache(self, path):
        needle = Path(path).stem.replace("_", " ")
        short = " ".join(needle.split(" ", maxsplit=5))
        self.cache[path.as_posix()] = short

    def save_cache(self):
        with open(self.cache_fn, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    pm = ProjectM()
    pm.pathlib_scan()
