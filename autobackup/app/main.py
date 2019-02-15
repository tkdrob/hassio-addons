#!/usr/bin/env python
from __future__ import unicode_literals
import logging
import requests
import simplejson as json
import sys
import os
import uuid
import datetime
import pytz
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import http.server
import cgi
import tarfile
from operator import itemgetter


############################################################################################
LOGFORMAT = logging.Formatter('%(asctime)-15s %(levelname)-5s -- %(message)s')
LOGGER = logging.getLogger('hassio_backup')
LOGGER.setLevel(logging.DEBUG)
consolehandler = logging.StreamHandler()
consolehandler.setFormatter(LOGFORMAT)
consolehandler.setLevel(logging.INFO)
LOGGER.addHandler(consolehandler)
GAUTH = GoogleAuth(settings_file=os.path.join(os.path.dirname(os.path.abspath(__file__)),"settings.yaml"))


class Main():

    def __init__(self, *args, **kwargs):
        LOGGER.info(' ')
        LOGGER.info('############## AUTO SNAPSHOT TASK STARTED ################')
        # init config
        self.parse_config()
        # init Google authentication
        self.init_google()
        # run backup
        self.new_snapshot()
        # purge old snapshots
        self.purge_hassio_snapshots()
        self.purge_google_snapshots()
        LOGGER.info('############## AUTO SNAPSHOT TASK COMPLETED ################')
        

    def init_google(self):
        '''initialize google auth'''
        self.gdrive = None
        if self.config["google_drive"]["enabled"]:
            try:
                GAUTH.LoadCredentials()
                GAUTH.Refresh()
            except Exception as exc:
                LOGGER.error(exc)
                LOGGER.warning("You need to authenticate Google through the webinterface!")
                httpd = AuthWebServer(('', 8055), StoppableHttpRequestHandler)
                httpd.serve_forever()
                httpd.server_close()
            self.gdrive = GoogleDrive(GAUTH)
            # look for our backup folder
            backupdir_id = None
            file_list = self.gdrive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
            for gfile in file_list:
                if gfile["mimeType"] == "application/vnd.google-apps.folder" and gfile['title'] == self.config["google_drive"]["backup_folder"]:
                    backupdir_id = gfile["id"]
                    break
            # create the folder if it doesn't exist
            if not backupdir_id:
                result = self.gdrive.CreateFile({'title': self.config["google_drive"]["backup_folder"], 'mimeType': 'application/vnd.google-apps.folder'})
                result.Upload()
                backupdir_id = result['id']
            LOGGER.debug("Found backup folder on Google Drive with id: %s" % backupdir_id)
            self.gdrive_folder = backupdir_id

    def parse_config(self):
        ''' grab config from file and environmental variables '''
        self.hassio_token = os.environ["HASSIO_TOKEN"]
        # grab from (hassio) config file
        with open("/data/options.json") as f:
            data = f.read()
            config = json.loads(data)
        log_file = config["log_file"]
        if log_file:
            logformat = logging.Formatter(LOGFORMAT)
            filehandler = logging.FileHandler(log_file, 'w')
            filehandler.setFormatter(LOGFORMAT)
            loglevel = eval("logging." + config["log_level"])
            filehandler.setLevel(loglevel)
            LOGGER.addHandler(filehandler)
        LOGGER.debug("Using config: %s" % config)
        self.config = config

    def get_snapshots(self):
        ''' get all existing snapshots in hassio'''
        result = self.__hassio_api("snapshots")
        if result and "data" in result and "snapshots" in result["data"]:
            return result["data"]["snapshots"]
        return []

    def get_snapshots_info(self):
        ''' get all existing snapshots in hassio with full info'''
        all_snapshots = []
        for item in self.get_snapshots():
            snapshot_data = self.__hassio_api("snapshots/%s/info" % item["slug"])
            all_snapshots.append(snapshot_data["data"])
        return all_snapshots

    def new_snapshot(self):
        ''' create a new snapshot'''
        name = self.get_local_datetime().strftime("autobackup %Y-%m-%d %H:%M:%S")
        # the config folders are always back-upped
        folders = ["ssl", "addons/local", "homeassistant"]
        # append share folder if configured
        if self.config["backup_share"]["enabled"] and not self.config["backup_share"]["subfolders"]:
            folders.append("share")
        options = { "name": name, "folders": folders}
        # append addons 
        if self.config["backup_addons"]["enabled"]:
            options["addons"] = []
            for item in self.get_addons():
                if item["installed"]:
                    # only include installed addons
                    if ((item["name"] in self.config["backup_addons"]["whitelist"] or 
                            item["slug"] in self.config["backup_addons"]["whitelist"]) or 
                                not self.config["backup_addons"]["whitelist"]):
                        # addon is in the whitelist or there is no whitelist configured at all
                        if not (item["name"] in self.config["backup_addons"]["blacklist"] or 
                                    item["slug"] in self.config["backup_addons"]["blacklist"]):
                            # addon is not in the blacklist so add it to the list
                            options["addons"].append(item["slug"])
        # create the snapshot
        LOGGER.info("Creating new hassio snapshot %s - This may take some time..." % options["name"])
        result = self.__hassio_api("snapshots/new/partial", options, post=True)
        snapshot_id = result["data"]["slug"]
        filename_short = "%s.tar" % snapshot_id
        filename_full = os.path.join("/backup", filename_short)
        # append share subfolders manually if needed
        self.append_share_folders(filename_full)
        LOGGER.info("New snapshot creation completed with id %s" % snapshot_id)
        if self.gdrive:
            LOGGER.info("Uploading %s to Google Drive" % filename_short)
            meta = {
                'name': filename_short,
                'title': filename_short,
                'description': name,
                'mimeType': 'application/tar',
                'parents': [{
                    'kind': 'drive#fileLink',
                    'id': self.gdrive_folder
                }]
            }
            new_file = self.gdrive.CreateFile(meta)
            new_file.SetContentFile(filename_full)
            new_file.Upload()
            LOGGER.info("Upload of %s to Google Drive completed" % filename_short)

    def append_share_folders(self, backupfile):
        ''' append subfolders from share to existing backupfile'''
        if not self.config["backup_share"]["subfolders"]:
            return
        LOGGER.info("Appending share subfolders to snapshot...")
        # create the tarfile for the share folder
        share_tmp_file = "share.tar.gz"
        if os.path.exists(share_tmp_file):
            os.remove(share_tmp_file)
        share_tmp_tar = tarfile.open(share_tmp_file, 'w:gz')
        for subfolder in self.config["backup_share"]["subfolders"]:
            folderpath = "/share/%s" % subfolder
            LOGGER.debug("Appending %s to backup..." % folderpath)
            share_tmp_tar.add(folderpath)
        share_tmp_tar.close()
        # modify the backup tarfile
        with tarfile.open(backupfile, 'r:') as backup_tar:
            backup_tar.extract('./snapshot.json')
            with open('snapshot.json') as json_file:
                json_data = json.load(json_file)
        json_data['folders'].append('share')
        with tarfile.open(backupfile, 'a:') as backup_tar:
            with open('snapshot.json', 'w') as outfile:
                json.dump(json_data, outfile, indent=4)
            backup_tar.add('snapshot.json', arcname='./snapshot.json')
            backup_tar.add(share_tmp_file, arcname='./%s' % share_tmp_file)
        # cleanup temp
        os.remove(share_tmp_file)
        os.remove('snapshot.json')

    def get_addons(self):
        ''' get hassio_addons '''
        result = self.__hassio_api("addons")
        if result and "data" in result and "addons" in result["data"]:
            return result["data"]["addons"]
        return []

    def purge_hassio_snapshots(self):
        ''' purge old snapshots from hassio'''
        num_keep = self.config["auto_purge"]
        if num_keep < 1:
            return
        snapshots = sorted(self.get_snapshots(), key=itemgetter('date'))
        num_snapshots = len(snapshots)
        del_count = 0
        if num_snapshots > num_keep:
            LOGGER.info("Purging old snapshots on hassio...")
            for snapshot in snapshots[:num_snapshots - num_keep]:
                LOGGER.debug("Purging old snapshot %s on hassio (id: %s)" % (snapshot["name"], snapshot["slug"]))
                self.__hassio_api('snapshots/%s/remove' % snapshot["slug"], post=True)

    def purge_google_snapshots(self):
        '''purge old snapshots from google drive'''
        if not self.gdrive:
            return
        num_keep = self.config["google_drive"]["auto_purge"]
        query = {
            'q': "'%s' in parents and trashed=false" % self.gdrive_folder,
            'orderBy': "modifiedDate",
            'spaces': "drive"
        }
        items = self.gdrive.ListFile(query).GetList()
        num_files = len(items)
        if num_files > num_keep:
            LOGGER.info("Purging old snapshots on Google Drive...")
            for file in items[:num_files - num_keep]:
                LOGGER.debug("Purging old snapshot %s on Google Drive (filename: %s)" % (file["description"], file["title"]))
                file.Delete()

    def __hassio_api(self, endpoint, params=None, post=False):
        '''get/post info from the hassio rest api'''
        result = {}
        if not params:
            params = {}
        headers = {"X-HASSIO-KEY": self.hassio_token}
        url = "http://hassio/%s" % endpoint
        try:
            if post:
                response = requests.post(url, json=params, headers=headers)
            else:
                response = requests.get(url, params=params, headers=headers)
            if response and response.content and response.status_code == 200:
                result = json.loads(response.content.decode('utf-8', 'replace'))
            else:
                raise Exception(str(response))
        except Exception as exc:
            LOGGER.error("Error in __get_data: %s - %s" % (str(exc), response.content))
            LOGGER.error("endpoint: %s - params: %s" %(endpoint, params))
            result = None
        # return result
        return result

    @staticmethod
    def get_local_datetime ():
        ''' helper method to get the local dateime'''
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        pst_now = utc_now.astimezone(pytz.timezone(os.environ["TZ"]))
        return pst_now


class StoppableHttpRequestHandler(http.server.BaseHTTPRequestHandler):
    """http request handler with QUIT stopping the server"""
    def do_QUIT (self):
        """send 200 OK response, and set server.stop to True"""
        self.send_response(200)
        self.end_headers()
        self.server.stop = True
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        auth_url = GAUTH.GetAuthUrl()
        html = """
            <html><body>
            <h1>Google authentication</h1>
            <a href='%s' target='_blank'>Please visit this URL</a>
            <br><br><br>
            <form method="POST" action="/send">
            <label>Enter the code you received from Google: </label>
            <input type="text" name="google_code"/><input type="submit" value="Send"/>
            </form></body></html>""" % auth_url
        self.wfile.write(html.encode("utf-8"))
        return
    #Handler for the POST requests
    def do_POST(self):
        if self.path=="/send":
            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
            })
            google_code = form["google_code"].value
            LOGGER.info("Received Google code: %s" % google_code)
            self.send_response(200)
            self.end_headers()
            try:
                GAUTH.Auth(google_code)
                GAUTH.SaveCredentials()
            except Exception as exc:
                LOGGER.error(exc)
                self.wfile.write(exc)
            self.wfile.write("All done!".encode("utf-8"))
            self.server.stop = True
            return

class AuthWebServer(http.server.HTTPServer):
    """http server that reacts to self.stop flag"""
    def serve_forever (self):
        """Handle one request at a time until stopped."""
        self.stop = False
        while not self.stop:
            self.handle_request()


#Main entry point
Main()