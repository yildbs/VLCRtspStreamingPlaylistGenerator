import glob
import os
import time
import json
import csv


try:
    with open('Config.json') as f:
        Config = json.load(f)
except FileExistsError:
    print('There is not Config.json')
    exit(1)

print(Config)

outputprefix = Config['outputprefix']
videolistcsv = Config['videolistcsv']
ipaddress = Config['ipaddress']
useslash = Config['useslash'] == 'True'

slash = "/" if useslash else "\\"

videolist = []
try:
    with open(videolistcsv, "r") as f:
        data = csv.reader(f)
        for port, videopath in data:
            videolist.append([port, videopath])
except FileExistsError:
    print('There is not '+ videolistcsv)
    exit(1)

generated = []

for port, videopath in videolist:
    batch_filename = 'Playlist_' + str(port) + '_' + videolistcsv + '.bat'

    if batch_filename not in generated:
        generated.append(batch_filename)
        try:
            os.remove(batch_filename)
        except:
            pass

    videofullpath = outputprefix + slash + videopath
    videofullpath = videofullpath.replace('\\', '/') if useslash else videofullpath.replace('/', '\\')

    vlccommand = 'vlc -vvv "' + videofullpath + '" --play-and-exit :sout=#rtp{sdp=rtsp://' + ipaddress + ':' + str(port) + '/1}'
    command = "echo " + vlccommand + " >> " + batch_filename
    os.system(command)


#####################################################################################################
batchfiles = glob.glob('Playlist*.bat')
for batchfile in batchfiles:
    with open(batchfile, "r") as f:
        content = f.readlines()

        duplicated = content
        for _ in range(10): # 2 pow 10
            duplicated += content

        duplicated = duplicated[:3000]
    with open(batchfile, "w") as f:
        f.write(''.join(duplicated))



