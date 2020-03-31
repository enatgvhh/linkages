# -*- coding: UTF-8 -*-
#mdService.py

class MdService(object):
    """Klasse MdService extrahiert und speichert die Infos aus dem Metadaten-Dienst (WFS oder WMS)"""

    def __init__(self, element):
        """Konstruktor der Klasse MdService
        
        Args:
            element: etree-node mit einem csw:GetRecordByIdResponse
        """
        self.__node = element
        self.__listMdUid = []
        self.__cap = None
        
        self.__setMdUid()
        self.__setCap()
        
    def __setMdUid(self):
        """private Methode __setMdUid extrahiert die UIDs aller Metadaten-Datasets"""
        listMdDatasetUri = self.__node.xpath('//srv:operatesOn/@xlink:href', namespaces={'xlink':'http://www.w3.org/1999/xlink', 'csw':'http://www.opengis.net/cat/csw/2.0.2', 'gco':'http://www.isotc211.org/2005/gco', 'gmd':'http://www.isotc211.org/2005/gmd', 'gml':'http://www.opengis.net/gml', 'gts':'http://www.isotc211.org/2005/gts', 'srv':'http://www.isotc211.org/2005/srv'})
        
        for mdDatasetUri in listMdDatasetUri:
            self.__listMdUid.append(mdDatasetUri)
        
    def __setCap(self):
        """private Methode __setCap extrahiert die URL zum GetCapabilities-Request des Dienstes"""
        self.__cap = self.__node.xpath('//gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:linkage/gmd:URL', namespaces={'csw':'http://www.opengis.net/cat/csw/2.0.2', 'gco':'http://www.isotc211.org/2005/gco', 'gmd':'http://www.isotc211.org/2005/gmd', 'gml':'http://www.opengis.net/gml', 'gts':'http://www.isotc211.org/2005/gts', 'srv':'http://www.isotc211.org/2005/srv'})[0].text
        
    def getListMdUid(self):
        """Methode getListMdUid gibt die UIDs aller Metadaten-Datasets zurueck
        
        Returns:
            List: UIDs aller Metadaten-Datasets des Dienstes
        """
        return self.__listMdUid
    
    def getCap(self):
        """Methode getCap gibt die URL zum GetCapabilities-Request des Dienstes zurueck
        
        Returns:
            String: URL GetCapabilities-Request des Dienstes
        """
        return self.__cap
    