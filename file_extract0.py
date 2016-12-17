from PIL import Image
from PIL.ExifTags import TAGS


class FileExtract:

    def get_exif(fn):
        ret = {}
        i = Image.open(fn)
        try:
            info = i._getexif()
            for t, v in info.items():
                try:
                    decoded = TAGS.get(t, t)
                    ret[decoded] = v
                except:
                    pass
            if "GPSInfo" in ret:
                return ret["GPSInfo"]
        except:
            return {}

    def process_gps(self, tags):
        gps = {}
        # 1 and 3 are not present if the coords keys are not present and will
        # be null if no coords
        if (1 in tags) and (not tags[1] == "\x00"):
            gps["y"] = self.dmsdec(tags[2][0][0], tags[2][0][1], tags[2][1][0],
                                   tags[2][1][1], tags[2][2][0], tags[2][2][1],
                                   tags[1])
            gps["x"] = self.dmsdec(tags[4][0][0], tags[4][0][1], tags[4][1][0],
                                   tags[4][1][1], tags[4][2][0], tags[4][2][1],
                                   tags[3])
            print gps
        return gps

    def dmsdec(dn, dd, mn, md, sn, sd, o="N"):
        degree = float(dn) / float(dd)
        minute = float(mn) / float(md) / 60
        second = float(sn) / float(sd) / 3600
        coord = degree + minute + second
        if(o == "S" or o == "W"):
            coord = coord * -1
        return coord

    def get_tags(self, file_location):
        with open(file_location, 'rb') as f:
            tags = self.process_gps(self.get_exif(f))
        return tags
