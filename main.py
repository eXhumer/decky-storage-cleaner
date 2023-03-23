#!/usr/bin/env python3
import shutil
import os
import urllib
import json
import math

class Plugin:
    async def _listdirs(self, rootdir):
        subdirectories = []
        for item in os.listdir(rootdir):
            subdirectories.append(item)
        
        return subdirectories

    async def list_games_with_temp_data(self, dirName):
        # store the JSON response of from GetAppList url
        response = urllib.request.urlopen('http://api.steampowered.com/ISteamApps/GetAppList/v0002/')
        all_games = json.loads(response.read())['applist']['apps']

        # list games on steam deck
        local_game_ids = await self._listdirs(self, '/home/deck/.steam/steam/steamapps/' + dirName)

        games_found = list(filter(lambda d: str(d['appid']) in local_game_ids, all_games))

        all_clean = {
            "appid": -1, 
            "name": "All Clean!" 
        }

        return json.dumps(games_found if len(games_found) > 0 else all_clean)

    async def delete_cache(self, dirName):
        shutil.rmtree('/home/deck/.steam/steam/steamapps/' + dirName)

    async def _convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    async def get_size(self, dirName):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk('/home/deck/.steam/steam/steamapps/' + dirName):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        return await self._convert_size(self, total_size)
    
    # async def _has_internet(host='http://google.com'):
    #     try:
    #         urllib.request.urlopen(host)
    #         return True
    #     except:
    #         return False