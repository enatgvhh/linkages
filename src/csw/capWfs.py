# -*- coding: UTF-8 -*-
#capWfs.py

class CapWfs(object):
    """Klasse CapWfs extrahiert und speichert die Infos aus dem WFS GetCapabilities Response"""

    def __init__(self, element):
        """Konstruktor der Klasse CapWfs
        
        Args:
            element: etree-node mit einem wfs GetCapabilities Response
        """
        self.__node = element
        self.__cswUrl = None
        self.__listMdUid = []
        self.__listLayerName = []
        
        self.__setCswUrl()
        self.__setLayerUid()
        self.__setLayerName()
        
    def __setCswUrl(self):
        """private Methode __setCswUrl extrahiert die URL des CSW-Aufrufs auf den Metadatensatz des WFS"""
        self.__cswUrl = self.__node.xpath('//inspire_common:MetadataUrl/inspire_common:URL', namespaces={'ows':'http://www.opengis.net/ows/1.1', 'inspire_common':'http://inspire.ec.europa.eu/schemas/common/1.0', 'inspire_dls':'http://inspire.ec.europa.eu/schemas/inspire_dls/1.0'})[0].text
           
    def __setLayerUid(self):
        """private Methode __setLayerUid extrahiert fuer alle Layer die UID zum jeweiligen Metadaten-Dataset"""
        listLayerMdUid = self.__node.xpath('//inspire_dls:SpatialDataSetIdentifier/inspire_common:Code', namespaces={'ows':'http://www.opengis.net/ows/1.1', 'inspire_common':'http://inspire.ec.europa.eu/schemas/common/1.0', 'inspire_dls':'http://inspire.ec.europa.eu/schemas/inspire_dls/1.0'})
        
        for layerMdUid in listLayerMdUid:
            self.__listMdUid.append(layerMdUid.text)

    def __setLayerName(self):
        """private Methode __setLayerName extrahiert den Namen fuer alle Layer"""
        listLayerName = self.__node.xpath("//*[local-name() = 'FeatureTypeList']/*[local-name() = 'FeatureType']/*[local-name() = 'Name']")
        
        for layerName in listLayerName:
            self.__listLayerName.append(layerName.text)

    def getCswUrl(self):
        """Methode getCswUrl gibt die URL fuer den CSW-Aufruf auf den Metadatensatz des WFS zurueck
        
        Returns:
            String: URL CSW-Aufruf fuer WFS Metadaten
        """
        return self.__cswUrl
    
    def getListMdUid(self):
        """Methode getListMdUid gibt eine List mit den UIDs zu allen Metadaten-Datasets zurueck
        
        Returns:
            List: UIDs aller Metadaten-Datasets des Dienstes
        """
        return self.__listMdUid
    
    def getListLayerName(self):
        """Methode getListLayerName gibt eine List mit den Namen aller Layer zurueck
        
        Returns:
            List: Namen aller Layer des Dienstes
        """
        return self.__listLayerName