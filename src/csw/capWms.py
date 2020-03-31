# -*- coding: UTF-8 -*-
#capWms.py

class CapWms(object):
    """Klasse CapWms extrahiert und speichert die Infos aus dem WMS GetCapabilities Response"""

    def __init__(self, element):
        """Konstruktor der Klasse CapWms
        
        Args:
            element: etree-node mit einem wms GetCapabilities Response
        """
        self.__node = element
        self.__cswUrl = None
        self.__listMdUid = []
        self.__listCswUrl = []
        
        self.__setCswUrl()
        self.__setLayerUid()
        self.__setCswLayerUrl()
        
    def __setCswUrl(self):
        """private Methode __setCswUrl extrahiert den CSW-Aufruf auf den Metadatensatz des WMS"""
        self.__cswUrl = self.__node.xpath('//inspire_common:MetadataUrl/inspire_common:URL', namespaces={'ows':'http://www.opengis.net/ows/1.1', 'inspire_common':'http://inspire.ec.europa.eu/schemas/common/1.0', 'inspire_dls':'http://inspire.ec.europa.eu/schemas/inspire_dls/1.0'})[0].text
           
    def __setLayerUid(self):
        """private Methode __setLayerUid extrahiert fuer jeden Layer die UID zum jeweiligen Metadaten-Dataset"""
        listLayerMdUid = self.__node.xpath("//*[local-name() = 'Identifier']")
        
        for layerMdUid in listLayerMdUid:
            self.__listMdUid.append(layerMdUid.text)
    
    def __setCswLayerUrl(self):
        """private Methode __setCswLayerUrl extrahiert fuer jeden Layer die URL zum jeweiligen CSW-Aufruf des Metadaten-Datasets"""
        listCswLayerUrl = self.__node.xpath("//*[local-name() = 'MetadataURL']/*[local-name() = 'OnlineResource']")
        
        for cswLayerUrl in listCswLayerUrl:
            for dictKey, dictValue in cswLayerUrl.items():
                if dictKey == '{http://www.w3.org/1999/xlink}href':
                    self.__listCswUrl.append(dictValue)
            
    def getCswUrl(self):
        """Methode getCswUrl gibt die URL fuer den CSW-Aufruf auf den Metadatensatz des WMS zurueck
        
        Returns:
            String: URL mit CSW-Aufruf fuer WMS Metadaten
        """
        return self.__cswUrl
    
    def getListMdUid(self):
        """Methode getListMdUid gibt eine List mit UIDs zu allen Metadaten-Datasets des Dienstes zurueck
        
        Returns:
            List: UIDs aller Metadaten-Datasets des Dienstes
        """
        return self.__listMdUid
    
    def getListCswLayerUrl(self):
        """Methode getListCswLayerUrl gibt eine List mit den URLs der CSW-Aufrufe zu allen Metadaten-Dataset des Dienstes zurueck
        
        Returns:
            List: URL CSW-Aufrufe aller Metadaten-Datasets des Dienstes
        """
        return self.__listCswUrl
    