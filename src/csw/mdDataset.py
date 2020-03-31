# -*- coding: UTF-8 -*-
#mdDataset.py
import re
from lxml import etree

class MdDataset(object):
    """Klasse MdDataset extrahiert und speichert die Infos aus dem Metadaten-Dataset"""

    def __init__(self, element):
        """Konstruktor der Klasse MdDataset
        
        Args:
            element: String mit einem csw:SearchResult 
        """
        self.__node = etree.fromstring(element)
        self.__csw = None
        self.__mdUid = None
        self.__mdName = None
        self.__capWms = None
        self.__capWfs = None
        
        self.__setCsw()
        self.__setMdUid()
        self.__setMdName()
        self.__setCaps()
    
    def __setCsw(self):
        """private Methode __setCsw extrahiert die ID des Metadaten-Datasets und verpackt sie in einen
        CSW-Aufruf der eigenen Adresse.
        """
        tmpId = self.__node.xpath('//gmd:fileIdentifier/gco:CharacterString', namespaces={'csw':'http://www.opengis.net/cat/csw/2.0.2', 'gco':'http://www.isotc211.org/2005/gco', 'gmd':'http://www.isotc211.org/2005/gmd', 'gml':'http://www.opengis.net/gml', 'gts':'http://www.isotc211.org/2005/gts', 'srv':'http://www.isotc211.org/2005/srv'})[0].text
        self.__csw = 'http://www.metaver.de/csw?Service=CSW&Request=GetRecordById&Version=2.0.2&id=' + tmpId + '&outputSchema=http://www.isotc211.org/2005/gmd&elementSetName=full'
        
    def __setMdUid(self):
        """private Methode __setMdUid extrahiert die UID des Metadaten-Datasets"""
        self.__mdUid = self.__node.xpath('//gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString', namespaces={'csw':'http://www.opengis.net/cat/csw/2.0.2', 'gco':'http://www.isotc211.org/2005/gco', 'gmd':'http://www.isotc211.org/2005/gmd', 'gml':'http://www.opengis.net/gml', 'gts':'http://www.isotc211.org/2005/gts', 'srv':'http://www.isotc211.org/2005/srv'})[0].text
    
    def __setMdName(self):
        """private Methode __setMdName extrahiert den Namen des Metadaten-Datasets"""
        self.__mdName = self.__node.xpath('//gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString', namespaces={'csw':'http://www.opengis.net/cat/csw/2.0.2', 'gco':'http://www.isotc211.org/2005/gco', 'gmd':'http://www.isotc211.org/2005/gmd', 'gml':'http://www.opengis.net/gml', 'gts':'http://www.isotc211.org/2005/gts', 'srv':'http://www.isotc211.org/2005/srv'})[0].text
    
    def __setCaps(self):
        """private Methode __setCaps extrahiert WFS- und WMS GetCapabilities-URLs"""
        listCapUrl = self.__node.xpath('//gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:linkage/gmd:URL', namespaces={'csw':'http://www.opengis.net/cat/csw/2.0.2', 'gco':'http://www.isotc211.org/2005/gco', 'gmd':'http://www.isotc211.org/2005/gmd', 'gml':'http://www.opengis.net/gml', 'gts':'http://www.isotc211.org/2005/gts', 'srv':'http://www.isotc211.org/2005/srv'})
        
        for capUrl in listCapUrl:
            if re.search("REQUEST=GetCapabilities", capUrl.text) != None:
                if re.search("SERVICE=WFS", capUrl.text) != None:
                    self.__capWfs = capUrl.text
                elif re.search("SERVICE=WMS", capUrl.text) != None:
                    self.__capWms = capUrl.text
    
    def getCsw(self):
        """Methode getCsw gibt die URL mit dem eigen CSW-Aufruf des Metadaten-Datasets zurueck
        
        Returns:
            String: ULR des eigen CSW-Aufrufs
        """
        return self.__csw
        
    def getMdUid(self):
        """Methode getMdUid gibt die UID des Metadaten-Datasets zurueck
        
        Returns:
            String: UID des Metadaten-Datasets
        """
        return self.__mdUid
    
    def getMdName(self):
        """Methode getMdName gibt den Namen des Metadaten-Datasets zurueck
        
        Returns:
            String: Name des Metadaten-Datasets
        """
        return self.__mdName
    
    def getCapWms(self):
        """Methode getCapWms gibt die WMS GetCapbilities-URL zurueck
        
        Returns:
            String: WMS GetCapbilities-URL
        """
        return self.__capWms
    
    def getCapWfs(self):
        """Methode getCapWfs gibt die WFS GetCapbilities-URL zurueck
        
        Returns:
            String: WFS GetCapbilities-URL
        """
        return self.__capWfs
    