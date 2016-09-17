#!/bin/bash

python3 /home/yakov/applications/kinopubupd.py
unzip -o /home/yakov/dist/plex/bundles/plex.kino.pub.zip -d /home/yakov/dist/plex/
service plexmediaserver stop
cp -fR /home/yakov/dist/plex/Kinopub.bundle /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/
service plexmediaserver start
/home/yakov/applications/plexupdate.sh -a -c -p

#root crontab line
#0 4 * * * /home/yakov/applications/plexfullupdate.sh