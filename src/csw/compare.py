# -*- coding: UTF-8 -*-
#checker.py
import pandas as pd
import numpy as np
from csw import mdDataset
from csw import mdService
from csw import capWfs
from csw import capWms

class Compare(object):
    """Klasse Compare fuehrt die Tests aus.
    """

    def __init__(self, md_dataset: mdDataset, md_wfs: mdService, md_wms: mdService, cap_wfs: capWfs, cap_wms: capWms):
        """Konstruktor der Klasse Compare
        
        Args:
            md_dataset: Objekt der Klasse MdDataset
            md_wfs: Objekt der Klasse MdService
            md_wms: Objekt der Klasse MdService
            cap_wfs: Objekt der Klasse CapWfs
            cap_wms: Objekt der Klasse CapWms
        """
        self.md_dataset = md_dataset
        self.md_wfs = md_wfs
        self.md_wms = md_wms
        self.cap_wfs = cap_wfs
        self.cap_wms = cap_wms
        self.__testResults = []
        
    def runTests(self):
        """Methode runTest fuehrt alle Test aus.
        
        Returns:
            pandas.DataFrame: DataFrame mit Test-Results
        """
        self.__testResults.append(self.md_dataset.getMdName())
        self.__testResults.append(self.md_dataset.getMdUid())
        self.__testResults.append(self.md_dataset.getCsw())
        self.__testResults.append(str(len(self.md_dataset.getCapWfs())))
        self.__testResults.append(str(len(self.md_dataset.getCapWms())))
        self.__test1()
        self.__test2()
        self.__test3()
        self.__test4()
        self.__test5()
        self.__test6()
        self.__test7()
        
        df = pd.DataFrame(np.array([self.__testResults]),columns=['md_ds_name', 'md_ds_uri', 'md_ds_wcs', 'md_ds_count_wfs', 'md_ds_count_wms', 'test1_md_ds_uri2md_wfs_uri', 'test1_count', 'test2_wfs_capabilities','test3_md_ds_uri2md_wms_uri', 'test3_count', 'test4_wms_capabilities', 'test5_md_ds_uri2cap_wfs_uri', 'test5_count', 'test6_md_ds_uri2cap_wms_uri', 'test6_count', 'test7_md_csw2cap_wms_csw', 'test7_count'])           
        return df
    
    def __test1(self):
        """private Methode __test1 prueft Uebereinstimmung des Daten-Metadatensatz
        Ressourcenidentifikators (URI) mit der URI-Referenz im WFS-Metadatensatz.
        Bei Gleichheit: PASSED else FAILED (1/1)
               
        Referenziert der WFS-Metadatensatz n Daten-Metadatensaetze: Es wird nur der Start
        Daten-Metadatensatz geprueft, alle weiteren werden ignoriert (Pruefung erfolgt ueber
        eigenen Daten-Metadatensatz).
        Bei Gleichheit Start Metadaten-Dataset: PASSED_MANUAL else FAILED (1/n)
        """
        result = 'FAILED'
        countTrue = 0
        
        for e in self.md_wfs.getListMdUid():
            if e.casefold() == self.md_dataset.getMdUid().casefold():
                if len(self.md_wfs.getListMdUid()) == 1:
                    result = 'PASSED'
                else:
                    result = 'PASSED_MANUAL'
                    
                countTrue += 1
                break
        
        countStr = str(countTrue) + " from " + str(len(self.md_wfs.getListMdUid())) + " ds"
        self.__testResults.append(result)
        self.__testResults.append(countStr)
    
    def __test2(self):
        """private Methode __test2 prueft Uebereinstimmung des WFS-GetCapabilities-Aufrufs
        im Daten-Metadatensatz zum WFS-Metadatensatz.
        Bei Gleichheit: PASSED else FAILED
        """
        result = 'FAILED'
        
        if self.md_dataset.getCapWfs()[0].casefold() == self.md_wfs.getCap().casefold():
            result = 'PASSED'
         
        self.__testResults.append(result)
                   
    def __test3(self):
        """private Methode __test3 prueft Uebereinstimmung des Daten-Metadatensatz
        Ressourcenidentifikators (URI) mit der URI-Referenz im WMS-Metadatensatz.
        Bei Gleichheit: PASSED else FAILED (1/1)
               
        Referenziert der WMS-Metadatensatz n Daten-Metadatensaetze: Es wird nur der Start
        Daten-Metadatensatz geprueft, alle weiteren werden ignoriert (Pruefung erfolgt ueber
        eigenen Daten-Metadatensatz).
        Bei Gleichheit Start Daten-Metadatensatz: PASSED_MANUAL else FAILED (1/n)
        """
        result = False
        countTrue = 0
        
        for e in self.md_wms.getListMdUid():
            if e.casefold() == self.md_dataset.getMdUid().casefold():
                if len(self.md_wms.getListMdUid()) == 1:
                    result = 'PASSED'
                else:
                    result = 'PASSED_MANUAL'
                    
                countTrue += 1
                break
        
        countStr = str(countTrue) + " from " + str(len(self.md_wms.getListMdUid())) + " ds"  
        self.__testResults.append(result)
        self.__testResults.append(countStr) 
        
    def __test4(self):
        """private Methode __test4 prueft Uebereinstimmung des WMS-GetCapabilities-Aufrufs
        im Daten-Metadatensatz zum WMS-Metadatensatz.
        Bei Gleichheit: PASSED else FAILED
        """
        result = 'FAILED'
        
        if self.md_dataset.getCapWms()[0].casefold() == self.md_wms.getCap().casefold():
            result = 'PASSED'
         
        self.__testResults.append(result)
        
    def __test5(self):
        """private Methode __test5 prueft Uebereinstimmung des Daten-Metadatensatz
        Ressourcenidentifikators (URI) mit den URI-Referenzen im WFS-GetCapabilities-Dokument.
        Bei Gleichheit: PASSED else FAILED (n/n)
               
        Referenziert der WFS-Metadatensatz n Daten-Metadatensaetze: Es wird nur der Start
        Daten-Metadatensatz geprueft, alle weiteren werden ignoriert (Pruefung erfolgt ueber
        eigenen Daten-Metadatensatz).
        Bei Gleichheit Start Daten-Metadatensatz: PASSED_MANUAL else FAILED (n/n)
        """
        result = 'FAILED'
        tmpList = list(dict.fromkeys(self.cap_wfs.getListMdUid()))
        countDs = len(tmpList)
        countTrue = 0
        
        for e in self.cap_wfs.getListMdUid():
            if e.casefold() == self.md_dataset.getMdUid().casefold():
                if countDs == 1:
                    result = 'PASSED'
                else:
                    result = 'PASSED_MANUAL'
                    
                countTrue += 1
        
        countStr = str(countTrue) + " from " + str(len(self.cap_wfs.getListLayerName())) + " layer in " + str(countDs) + " ds"   
        self.__testResults.append(result)
        self.__testResults.append(countStr)
    
    def __test6(self):
        """private Methode __test6 prueft Uebereinstimmung des Daten-Metadatensatz
        Ressourcenidentifikators (URI) mit den URI-Referenzen im WMS-GetCapabilities-Dokument.
        Bei Gleichheit: PASSED else FAILED (n/n)
               
        Referenziert der WMS-Metadatensatz n Daten-Metadatensaetze: Es wird nur der Start
        Daten-Metadatensatz geprueft, alle weiteren werden ignoriert (Pruefung erfolgt ueber
        eigenen Daten-Metadatensatz).
        Bei Gleichheit Start Daten-Metadatensatz: PASSED_MANUAL else FAILED (n/n)
        """
        result = 'FAILED'
        tmpList = list(dict.fromkeys(self.cap_wms.getListMdUid()))
        countDs = len(tmpList)
        countTrue = 0
        
        for e in self.cap_wms.getListMdUid():
            if e.casefold() == self.md_dataset.getMdUid().casefold():
                if countDs == 1:
                    result = 'PASSED'
                else:
                    result = 'PASSED_MANUAL'
                    
                countTrue += 1
        
        countStr = str(countTrue) + " from " + str(len(self.cap_wms.getListLayerName())) + " layer in " + str(countDs) + " ds" 
        self.__testResults.append(result)
        self.__testResults.append(countStr)
    
    def __test7(self):
        """private Methode __test7 prueft Uebereinstimmung des Daten-Metadatensatz
        CSW-Aufufs mit den CSW-Aufrufen je Layer im WMS-GetCapabilities.
        Bei Gleichheit: PASSED else FAILED (n/n)
               
        Referenziert der WMS-Metadatensatz n Daten-Metadatensaetze: Es wird nur der Start
        Daten-Metadatensatz geprueft, alle weiteren werden ignoriert (Pruefung erfolgt ueber
        eigenen Daten-Metadatensatz).
        Bei Gleichheit Start Daten-Metadatensatz: PASSED_MANUAL else FAILED (n/n)
        """
        result = 'FAILED'
        tmpList = list(dict.fromkeys(self.cap_wms.getListCswLayerUrl()))
        countDs = len(tmpList)
        countTrue = 0
        
        for e in self.cap_wms.getListCswLayerUrl():
            if e.casefold() == self.md_dataset.getCsw().casefold():
                if countDs == 1:
                    result = 'PASSED'
                else:
                    result = 'PASSED_MANUAL'
                    
                countTrue += 1
        
        countStr = str(countTrue) + " from " + str(len(self.cap_wms.getListLayerName())) + " layer in " + str(countDs) + " ds" 
        self.__testResults.append(result)
        self.__testResults.append(countStr)
    