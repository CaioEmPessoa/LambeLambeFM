import requests
from PIL import Image

class LastfmApi():
    def __init__(self, name):
        super().__init__()

        self.TYPE_DICT = {
            "track":{
                "method":"gettoptracks",
                "name":"toptracks",
                "single":"track"
            },
            "artist":{
                "method":"gettopartists",
                "name":"topartists",
                "single":"artist"
            },
            "album":{
                "method":"getTopAlbums",
                "name":"topalbums",
                "single":"album"
            }
        }

        self.NAME = name

    def request(self, type, 
                limit, period):

        type = self.TYPE_DICT[type]

        params={"method": f"user.{type["method"]}",
                "format":"json",
                "user":self.NAME,
                "limit":limit,
                "period":period,
                "api_key":"9f3fa3157847ef46f91210ac5da2116d"}


        return requests.get("https://ws.audioscrobbler.com/2.0/", params=params)

    def topstats(self, type, limit=10, period="overall"):

        type = self.TYPE_DICT[type]
        name = type["name"]
        single = type["single"]

        r = self.request(single, limit, period)

        top_tracks = r.json()[name][single]

        info_dict = {}

        for track in top_tracks:
            name = track["name"]
            img = track["image"][3]["#text"]
            info_dict[name] = img

        return info_dict

class generateCollage():    

    def get_images(self, imgs):
        imgs_list = []
        for img in imgs:
            if img == "":
                img = "https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png"
            imgs_list.append(Image.open(requests.get(img, stream=True).raw))

        return imgs_list


    def concatenate(self, imgs):
        final_size = (1500, 1500)
        single_size = int(final_size[0]/(len(imgs)/5))

        final_img = Image.new("RGB", final_size)

        h_pos = 0
        v_pos = 0
        for img in imgs:
            img.thumbnail((single_size, single_size), Image.Resampling.LANCZOS)
            final_img.paste(img, (h_pos, v_pos))

            h_pos+=single_size
            if h_pos >= final_size[0]:
                h_pos=0
                v_pos+=single_size
        
        final_img.save("img.png")

    def get_concat_h(im1, im2):
        dst = Image.new('RGB', (im1.width + im2.width, im1.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))
        return dst

    def get_concat_v(im1, im2):
        dst = Image.new('RGB', (im1.width, im1.height + im2.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (0, im1.height))
        return dst

api = LastfmApi("caioempessoa")
info = api.topstats("album", 25, "7day")

collage = generateCollage()

print(info)

images = collage.get_images([info[img] for img in info])

collage.concatenate(images)