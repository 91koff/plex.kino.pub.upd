import requests
import os.path


def download(url, output, output2):
    print(url)
    response = requests.get(url)
    if response.status_code != 200:
        #print("HTTP code: " + str(response.status_code))
        return False
    else:
        with open(output, "wb") as file:
            file.write(response.content)
            file.close()
        with open(output2, "wb") as file2:
            file2.write(response.content)
            file2.close()
        return True


def getcurrentversion(path):
    versionfile = path + "currentversion.txt"
    if os.path.isfile(versionfile):
        fver = open(versionfile, "r")
        currentversion = fver.readline()
        fver.close()
        print("current version (from file) = " + currentversion)
    else:
        currentversion = "0.0.0"
        fver = open(versionfile, "w")
        fver.writelines(currentversion)
        fver.close()
        print("current version = " + currentversion)
    return currentversion


def getdownloadinfo(url="", device="", version=""):
    if device == "plex":
        pluginname = "plex.kino.pub"
        return url + device + "/" + pluginname + "-" + version + ".zip", pluginname + "-" + version + ".zip"
    else:
        raise NotImplementedError


def formatversionstring(x, y, z):
    return str(x) + "." + str(y) + "." + str(z)


def getnextversion(version):
        major = int(version[0])
        minor = int(version[2])
        build = int(version[4])
        print("->" + version)
        if build in range(9):
            build += 1
            #print("b->", formatversionstring(major, minor, build))
        elif build == 9 and minor in range(9):
            build = 0
            minor += 1
            #print("min->", formatversionstring(major, minor, build))
        elif minor == 9 and major >= 0:
            build = 0
            minor = 0
            major += 1
            #print("maj->", formatversionstring(major, minor, build))
        else:
            print("something gone wrong!!!")
        return formatversionstring(major, minor, build)


def updatecurrentversioninfo(path):
    versionfile = path + "currentversion.txt"
    if os.path.isfile(versionfile):
        fver = open(versionfile, "r")
        currentversion = fver.readline()
        fver.close()
        newcurrentversion = getnextversion(currentversion)
        fver = open(versionfile, "w")
        fver.writelines(newcurrentversion)
        fver.close()
    print("new current version = " + newcurrentversion)
    return newcurrentversion

url_base = "http://plugins.service-kp.com/"
# TODO: implement input params -p|--path
working_path = "./"
#working_path = "/home/yakov/dist/plex/"
# TODO: implement input params -d|--device
device = "plex"
#destination_path = "/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-ins/"
#destination_path = "./var/"

current_version = getcurrentversion(working_path)
url_download = getdownloadinfo(url_base, device, current_version)[0]
output_filename = working_path + getdownloadinfo(url_base, device, current_version)[1]
current_filename = working_path + "plex.kino.pub.zip"

# def unzip(zipfile, extractionpath):
#     zip_ref = zipfile.ZipFile(zipfile, 'r')
#     zip_ref.extractall(extractionpath)
#     zip_ref.close()
#
#
# def installplugin(file, path):
#     unzip(file, path)
#     os.system("cd " + file + " " + path)

if not os.path.isfile(current_filename):
    while not download(url_download, output_filename, current_filename):
        next_version = updatecurrentversioninfo(working_path)
        url_download = getdownloadinfo(url_base, device, next_version)[0]
        output_filename = working_path + getdownloadinfo(url_base, device, next_version)[1]
    while download(url_download, output_filename, current_filename):
        next_version = updatecurrentversioninfo(working_path)
        url_download = getdownloadinfo(url_base, device, next_version)[0]
        output_filename = working_path + getdownloadinfo(url_base, device, next_version)[1]
else:
    while download(url_download, output_filename, current_filename):
        next_version = updatecurrentversioninfo(working_path)
        url_download = getdownloadinfo(url_base, device, next_version)[0]
        output_filename = working_path + getdownloadinfo(url_base, device, next_version)[1]
