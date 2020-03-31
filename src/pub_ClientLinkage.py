# -*- coding: UTF-8 -*-
#ClientLinkage.py
from csw import checker

def main():
    """Main Methode definiert Parameter fuer initialen CSW-POST-Aufruf aller HH Datasets,
    die inspireidentifiziert sind und startet die Prozesskette.
    
    Post-Body:
    <?xml version="1.0" encoding="UTF-8"?>
    <csw:GetRecords xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" xmlns:gmd="http://www.isotc211.org/2005/gmd" service="CSW" version="2.0.2" resultType="results" outputFormat="application/xml" outputSchema="http://www.isotc211.org/2005/gmd" iplug="/ingrid-group:ige-iplug-HH" elementSetName="full">
      <csw:Query typeNames="csw:Record">
        <csw:Constraint version="1.1.0">
          <ogc:Filter xmlns="http://www.opengis.net/cat/csw/2.0.2" xmlns:apiso="http://www.opengis.net/cat/csw/apiso/1.0" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dct="http://purl.org/dc/terms/" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:ows="http://www.opengis.net/ows" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <ogc:And>
              <ogc:PropertyIsEqualTo>
                <ogc:PropertyName>apiso:type</ogc:PropertyName>
                <ogc:Literal>dataset</ogc:Literal>
              </ogc:PropertyIsEqualTo>
              <ogc:PropertyIsLike escapeChar="\" singleChar="?" wildCard="*">
                <ogc:PropertyName>AnyText</ogc:PropertyName>
                <ogc:Literal>inspireidentifiziert</ogc:Literal>
              </ogc:PropertyIsLike>
              <ogc:PropertyIsLike escapeChar="\" singleChar="?" wildCard="*">
                <ogc:PropertyName>AnyText</ogc:PropertyName>
                <ogc:Literal>https://registry.gdi-de.org/id/de.hh</ogc:Literal>
              </ogc:PropertyIsLike>
            </ogc:And>
          </ogc:Filter>
        </csw:Constraint>
      </csw:Query>
    </csw:GetRecords>
    """
    url = 'https://metaver.de/csw?'
    
    proxies = {
        'http': 'http://111.11.111.111:80',
        'https': 'http://111.11.111.111:80',
        }
    
    headers = {'Content-Type': 'application/xml'}   
    xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<csw:GetRecords xmlns:csw=\"http://www.opengis.net/cat/csw/2.0.2\" xmlns:gmd=\"http://www.isotc211.org/2005/gmd\" service=\"CSW\" version=\"2.0.2\" resultType=\"results\" outputFormat=\"application/xml\" outputSchema=\"http://www.isotc211.org/2005/gmd\" startPosition=\"1\" maxRecords=\"10\" iplug=\"/ingrid-group:ige-iplug-HH\" elementSetName=\"full\">\n  <csw:Query typeNames=\"csw:Record\">\n    <csw:Constraint version=\"1.1.0\">\n      <ogc:Filter xmlns=\"http://www.opengis.net/cat/csw/2.0.2\" xmlns:apiso=\"http://www.opengis.net/cat/csw/apiso/1.0\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:dct=\"http://purl.org/dc/terms/\" xmlns:gmd=\"http://www.isotc211.org/2005/gmd\" xmlns:gml=\"http://www.opengis.net/gml\" xmlns:ogc=\"http://www.opengis.net/ogc\" xmlns:ows=\"http://www.opengis.net/ows\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n        <ogc:And>\n          <ogc:PropertyIsEqualTo>\n            <ogc:PropertyName>apiso:type</ogc:PropertyName>\n            <ogc:Literal>dataset</ogc:Literal>\n          </ogc:PropertyIsEqualTo>\n          <ogc:PropertyIsLike escapeChar=\"\\\" singleChar=\"?\" wildCard=\"*\">\n            <ogc:PropertyName>AnyText</ogc:PropertyName>\n            <ogc:Literal>inspireidentifiziert</ogc:Literal>\n          </ogc:PropertyIsLike>\n          <ogc:PropertyIsLike escapeChar=\"\\\" singleChar=\"?\" wildCard=\"*\">\n            <ogc:PropertyName>AnyText</ogc:PropertyName>\n            <ogc:Literal>https://registry.gdi-de.org/id/de.hh</ogc:Literal>\n          </ogc:PropertyIsLike>\n        </ogc:And>\n      </ogc:Filter>\n    </csw:Constraint>\n  </csw:Query>\n</csw:GetRecords>"
    logfile = r'D:\HMDK_Fehler\linkage\csw_logger.log'
    writerfile = r'D:\HMDK_Fehler\linkage\csw_writer.csv'
    
    ob = checker.Checker(proxies, logfile, writerfile)
    ob.setInitialMdDatasetRequest(url, headers, xml)

if __name__ == '__main__':
    main()
    