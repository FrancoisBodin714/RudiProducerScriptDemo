# -*- coding: utf-8 -*-
#LIBRARY for publishing data from local file

import os
import logging
import io
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import time
import uuid
import hashlib
import configparser


VERBOSE = False

def getVERBOSE():
      global VERBOSE
      return VERBOSE

def setVerbose():
      global VERBOSE
      VERBOSE = True

def unsetVerbose():
      global VERBOSE
      VERBOSE = False

class LocalFiles:

      def __init__(self):

        self.config = configparser.ConfigParser()
        self.config.read('localFiles.ini')
        
        # apply if not already performed
        logging.basicConfig(filename='localFiles.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
        logging.info('localFiles init')
        
        self.tmp = self.config['DEFAULT']['tmp']
        logging.info("config tmp="+self.tmp)

        self.delay = int(self.config['DEFAULT']['delay'])
        logging.info("config delay="+str(self.delay))

        self.datasetstatusdir = self.config['DEFAULT']['datasetstatusdir']
        logging.info("config datasetstatusdir="+self.datasetstatusdir)

        self.datasetstatus = self.config['DEFAULT']['datasetstatus']
        logging.info("config datasetstatus="+self.datasetstatus)

        self.tmpmetafile = self.config['DEFAULT']['tmpmetafile']
        logging.info("config tmpmetafile="+self.tmpmetafile)

        self.producer = self.config['DATASOURCE']['producer']
        logging.info("config producer="+self.producer)

        self.datasource_protocol = self.config['DATASOURCE']['protocol']
        logging.info("config datasource protocol="+self.datasource_protocol)

        self.datasource_directory = self.config['DATASOURCE']['directory']
        logging.info("config datasource directory="+self.datasource_directory)

        if self.datasetstatus != None and self.datasetstatusdir != None:
            try:
                self.fis = open(self.datasetstatusdir+self.datasetstatus,"r")
                self.DataSetStatus = self.fis.read()
                self.DataSetStatus = json.loads(self.DataSetStatus)
                self.fis.close()
                logging.info('Datasetstatus Loaded')
            except:
                logging.info('No Datasetstatus Loaded')
                self.DataSetStatus = json.loads('{"not-a-data-set": 0.0}')

      def saveDataSetStatus(self):
        logging.info('saveDataSetStatus')
        if os.path.isfile(self.datasetstatusdir+self.datasetstatus):
            print("File "+self.datasetstatusdir+self.datasetstatus+" exists")
            os.system("cp "+self.datasetstatusdir+self.datasetstatus+" "+
                      self.datasetstatusdir+self.datasetstatus+"."+str(datetime.now().timestamp()))
        try:
            file_dst  = open(self.datasetstatusdir+self.datasetstatus,"w")
            file_dst.write(json.dumps(self.DataSetStatus))
            file_dst.close()        
        except:
            logging.warning("Failed saveDataSetStatus")

      def pingServer(self):
            return (200,"files are local")

      def checkServer(self):
            logging.info('checkServer')
            #Check if datasource_directory is here
            #Check if description for meta_data is here
            #for each data set add a .ini with all required information to build the meta-data
            try:
                  self.numberofdatasets = 0
                  obj_dir = os.scandir(self.datasource_directory)
                  for entry in obj_dir :
                        if entry.is_dir() or entry.is_file():
                              if entry.name.endswith(".ini"):
                                    self.numberofdatasets += 1
            except:
                  return False
            return True

      def parseIniMetaDataFile(self,path):
            if getVERBOSE():
                  print("Parsing ",path)
            try:
                  self.configMetaData.read(path)
                  try:
                        kw = self.configMetaData['METADATA']['descriptor_keywords']
                        kw = [x.strip() for x in kw.split(';')]
                  except:
                        kw = ""
                  descMeta= {"descriptor_file": self.configMetaData['METADATA']['descriptor_file'],
                  "descriptor_metadata_info_created": self.configMetaData['METADATA']['descriptor_metadata_info_created'],
                  "descriptor_metadata_info_updated": self.configMetaData['METADATA']['descriptor_metadata_info_updated'],
                  "descriptor_keywords": kw,
                  "descriptor_contact_id": self.configMetaData['METADATA']['descriptor_contact_id'],
                  "descriptor_resource_languages": self.configMetaData['METADATA']['descriptor_resource_languages'],
                  "descriptor_resource_title": self.configMetaData['METADATA']['descriptor_resource_title'],
                  "descriptor_global_id": self.configMetaData['METADATA']['descriptor_global_id'],
                  "descriptor_local_id": self.configMetaData['METADATA']['descriptor_local_id'],
                  "descriptor_synopsis": self.configMetaData['METADATA']['descriptor_synopsis'],
                  "descriptor_summary": self.configMetaData['METADATA']['descriptor_summary'],
                  "descriptor_summary_file": self.configMetaData['METADATA']['descriptor_summary_file'],
                  "descriptor_theme": self.configMetaData['METADATA']['descriptor_theme'],
                  "descriptor_producer_organization_id" : self.configMetaData['METADATA']['descriptor_producer_organization_id'],
                  "descriptor_dataset_dates_created" : self.configMetaData['METADATA']['descriptor_dataset_dates_created'],
                  "descriptor_dataset_dates_updated": self.configMetaData['METADATA']['descriptor_dataset_dates_updated'],
                  "descriptor_licence_type" : self.configMetaData['METADATA']['descriptor_licence_type'],
                  "descriptor_file_type" : self.configMetaData['METADATA']['descriptor_file_type'],
                  "descriptor_ready_for_publication" : self.configMetaData['METADATA']['descriptor_ready_for_publication'],
                  "descriptor_this_is_an_update" : self.configMetaData['METADATA']['descriptor_this_is_an_update'],
                  "descriptor_licence_label" : self.configMetaData['METADATA']['descriptor_licence_label']
                  }

                  if os.path.isfile(self.datasource_directory+descMeta["descriptor_summary_file"]):
                        src = self.datasource_directory+descMeta["descriptor_summary_file"]
                        if getVERBOSE():
                              print("SUMMARY : ",src)
                        sumfile = open(src,"r")          
                        txt = sumfile.read()
                        if getVERBOSE():
                              print(txt)
                        descMeta["descriptor_summary"] = txt
                        sumfile.close()
                  if getVERBOSE():
                        print("===================================")
                        print(descMeta)
                  return descMeta
            except Exception as ex:
                  logging.exception("Issue with parseIniMetaDataFile")
                  print("Issue with parseIniMetaDataFile")                  
                  exit()
                  return None

      def downloadMetadata(self,saveToFile=True):
            logging.info('downloadMetadata')
            self.configMetaData = configparser.ConfigParser()
            self.numberofdatasets = 0
            try:
                  self.list_metadata=[]
                  obj_dir = os.scandir(self.datasource_directory)
                  for entry in obj_dir :
                        if entry.is_dir() or entry.is_file():
                              if entry.name.endswith(".ini"):
                                    self.numberofdatasets += 1
                                    md = self.parseIniMetaDataFile(self.datasource_directory+entry.name)
                                    self.list_metadata.append(md)
            except:
                  logging.warning("Issue with downloadMetadata") 
                  print("Issue with downloadMetadata")
                  return None
            return self.list_metadata

      def downloadDataSet(self,id):
            #Assume for now that the file is there
            return True
        
      def IsDataSetModified(self,ids,jsd, userecords=False):
            logging.info('IsDataSetModified')
            modified_ids = False
            if ids == None:
                  logging.warning("IsDataSetModified ids parameter is None")
                  return False
            if jsd == None:
                  logging.warning("IsDataSetModified jsd parameter is None")
                  return False
            try:
                  if self.DataSetStatus[ids] != None:
                        maxdate = float(self.DataSetStatus[ids])
                        dt_object = datetime.fromtimestamp(int(maxdate))
                        print("       Last modifications : ",dt_object)
            except:
                  maxdate = 0.0
                  print("initialising to 0")

      def BrowseDataSet(self, publisher= None):
            dsToConsider=[]
            for m in self.list_metadata:
                  dsToConsider.append(m['descriptor_local_id'])
            return dsToConsider

      def getFileNameFromLocalId(self,lid):
            if lid == None:
                  return None
            for md in  self.list_metadata:
                  if md["descriptor_local_id"] == lid:
                        return md["descriptor_file"]
            return None

      def getDataSetMetaData(self,lid):
            if lid == None:
                  return None
            for md in  self.list_metadata:
                  if md["descriptor_local_id"] == lid:
                        return md
            return None

      def getDataSetType(self,lid):
            if lid == None:
                  return None
            for md in self.list_metadata:
                  if md["descriptor_local_id"] == lid:
                        return md["descriptor_file_type"]
            return None

