# -*- coding: UTF-8 -*-
#checker.py
import sys
import requests
import logging
import pandas as pd
import numpy as np
from lxml import etree
from csw import mdDataset
from csw import mdService
from csw import capWfs
from csw import capWms
from csw import compare

class Checker(object):
    """Klasse Checker fuehrt alle verketteten Requests (CSW und GetCapabilities) aus und
    initialisiert die Ueberpruefung der Linkages.
    """

    def __init__(self, proxies, logfile, writerfile):
        """Konstruktor der Klasse Checker
        
        Args:
            proxies: Dictionary {'http': 'http://111.11.111.111:80}
            logfile: String mit Path/File.log
            writerfile: String mit Path/File.csv
        """
        self.__proxies = proxies
        logging.basicConfig(filename=logfile, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        self.__logger = logging.getLogger('loggerCSW')
        self.__filePath = writerfile
        self.df = pd.DataFrame()
        
        self.md_dataset = None
        self.md_wfs = None
        self.md_wms = None
        self.cap_wfs = None
        self.cap_wms = None
        
    def __clearSearchResult(self):
        self.md_dataset = None
        self.md_wfs = None
        self.md_wms = None
        self.cap_wfs = None
        self.cap_wms = None
    
    def setInitialMdDatasetRequest(self, url, headers, xml):
        """Methode setInitialMdDatasetRequest startet den gesamten Prozess mit einem
        initialen CSW-Post-Request.
        
         Args:
            url: String mit CSW-URL ('https://metaver.de/csw?')
            headers: Dictionary {'Content-Type': 'application/xml'}
            xml: String mit CSW-Post-Body
        """
        try:
            r = requests.post(url, data=xml, headers=headers, proxies=self.__proxies)        
            et = etree.fromstring(r.content)
            eList = et.xpath('//csw:SearchResults/*', namespaces={'csw':'http://www.opengis.net/cat/csw/2.0.2', 'gco':'http://www.isotc211.org/2005/gco', 'gmd':'http://www.isotc211.org/2005/gmd', 'gml':'http://www.opengis.net/gml', 'gts':'http://www.isotc211.org/2005/gts', 'srv':'http://www.isotc211.org/2005/srv'})  
            self.__logger.info('SearchResults: ' + str(len(eList)))
        except:
            message = "initial csw request failed: " + str(sys.exc_info()[0]) + "; " + str(sys.exc_info()[1])
            self.__logger.error(message)
            sys.exit()
        
        if eList:  
            for item in eList:
                self.__clearSearchResult()
                try:
                    self.md_dataset = mdDataset.MdDataset(etree.tostring(item, encoding='unicode'))
                    
                    if len(self.md_dataset.getCapWfs()) == 1 and len(self.md_dataset.getCapWms()) == 1:
                        self.__setGetCapabilitiesWfsRequest()
                        self.__setMdWfsRequest()
                        self.__setGetCapabilitiesWmsRequest()
                        self.__setMdWmsRequest()

                        comp = compare.Compare(self.md_dataset, self.md_wfs, self.md_wms, self.cap_wfs, self.cap_wms)
                        self.df = self.df.append(comp.runTests())
                    else:
                        countList = []
                        countList.append(self.md_dataset.getMdName())
                        countList.append(self.md_dataset.getMdUid())
                        countList.append(self.md_dataset.getCsw())

                        if len(self.md_dataset.getCapWfs()) == 0:
                            countList.append(str(0))
                        else:
                            countList.append(str(len(self.md_dataset.getCapWfs())))

                        if len(self.md_dataset.getCapWms()) == 0:
                            countList.append(str(0))
                        else:
                            countList.append(str(len(self.md_dataset.getCapWms())))

                        dfTemp = pd.DataFrame(np.array([countList]),columns=['md_ds_name', 'md_ds_uri', 'md_ds_wcs', 'md_ds_count_wfs', 'md_ds_count_wms'])           
                        self.df = self.df.append(dfTemp)
                except:
                    message = "error: " + str(sys.exc_info()[0]) + "; " + str(sys.exc_info()[1])
                    self.__logger.error(message)
                    self.__logger.error('ERROR BY Result: ' + self.md_dataset.getMdName() + ", " + self.md_dataset.getMdUid() + ", " + self.md_dataset.getCsw())
                    
        self.df = self.df.reset_index()
        self.df = self.df.drop(columns='index')
        self.df.to_csv(self.__filePath, sep=';', na_rep='', index=True)
        
    def __setGetCapabilitiesWfsRequest(self):
        """private Methode __setGetCapabilitiesWfsRequest fuehrt WFS GetCapabilities-Request aus"""
        #https://geodienste.hamburg.de ohne proxie
        #r = requests.get(self.md_dataset.getCapWfs()[0], proxies=self.__proxies)
        r = requests.get(self.md_dataset.getCapWfs()[0])
        et = etree.fromstring(r.content)
        self.cap_wfs = capWfs.CapWfs(et)

    def __setMdWfsRequest(self):
        """private Methode __setMdWfsRequest fuehrt CSW Aufruf fuer WFS-Metadaten aus"""
        r = requests.get(self.cap_wfs.getCswUrl(), proxies=self.__proxies)
        et = etree.fromstring(r.content)
        self.md_wfs = mdService.MdService(et)

    def __setGetCapabilitiesWmsRequest(self):
        """private Methode __setGetCapabilitiesWmsRequest fuehrt WMS GetCapabilities-Request aus"""
        #https://geodienste.hamburg.de ohne proxie
        #r = requests.get(self.md_dataset.getCapWfs()[0], proxies=self.__proxies)
        r = requests.get(self.md_dataset.getCapWms()[0])
        et = etree.fromstring(r.content)
        self.cap_wms = capWms.CapWms(et)

    def __setMdWmsRequest(self):
        """private Methode __setMdWmsRequest fuehrt CSW Aufruf fuer WMS-Metadaten aus"""
        r = requests.get(self.cap_wms.getCswUrl(), proxies=self.__proxies)
        et = etree.fromstring(r.content)
        self.md_wms = mdService.MdService(et)

        