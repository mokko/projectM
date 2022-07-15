    ##
    ## old experiments no longer used
    ##

    def walk_scan(self) -> None:
        """
        os.walk makes nonsense paths that dont exist; obviously that is a user
        error, but that error is not obvious
        """
        tif_count = 0
        total_size = 0

        for each in start_dir:
            print(f"ENTERING {each}")
            adir = start_dir[each]
            logging.info(f"STARTING on {adir}")
            for root, dirs, files in os.walk(adir):
                tif_count += 1
                for dir1 in dirs:
                    for file in files:
                        ext = Path(file).suffix
                        if ext.lower() == ".tif" or ext.lower() == ".tiff":
                            # path = Path(root).joinpath(dir1).joinpath(file).resolve()
                            path = os.path.realpath(os.path.join(root, dir1, file))
                            try:
                                size = os.stat(path).st_size
                                # size = path.stat().st_size
                            except FileNotFoundError:
                                logging.error(f"File not found: {path}")
                                size = 0
                            else:
                                logging.error(f"File FOUND: {path}")
                            total_size += size

                            needle = Path(file).stem.replace("_", " ")
                            short = " ".join(needle.split(" ", maxsplit=5))
                            self.cache[str(path)] = short
                            print(f"+ {path} {size}")

    def scantree(path):
        """scandir version of scan; runs into WinError 3 file not exist"""

        for entry in scandir(path):  # dies possibly b/c of long path
            length = len(entry.path)
            if entry.is_dir(follow_symlinks=False):
                # print (f"***{entry.path}")
                yield from scantree(entry.path)
            else:
                yield entry

    # scandir solution
    def scantree_tif(path):
        for entry in scantree(path):
            if entry.name.lower().endswith((".tif", ".tiff")):
                yield entry

    def scandir_summary(self):
        for house in start_dir:
            # print (f"**{house} {start_dir[house]}")
            adir = start_dir[house]
            logging.info(f"working on {adir}")
            tif_count = 0
            total_size = 0
            for entry in scantree_tif(adir):
                if entry.is_file:  # there could be a dir ending with tif
                    tif_count += 1
                    size = entry.stat().st_size
                    total_size += size
                    # print (f"{entry.path} {size}")
                # if tif_count == 20:
                #    break
            size_in_gb = round(total_size / 1024 / 1024 / 1024, 1)
            logging.INFO(f"{tif_count} tifs with a total size of {size_in_gb} GB")
