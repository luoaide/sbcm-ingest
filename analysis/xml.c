// https://www.msweet.org/mxml/mxml.html

// GENERIC CoT MESSAGE:
// <?xml version='1.0' standalone='yes'?>
// <event version="2.0"
//     uid="J-01334"
//     type="a-h-A-M-F-U-M"
//     time="2005-04-05T11:43:38.07Z"
//     start="2005-04-05T11:43:38.07Z"
//     stale="2005-04-05T11:45:38.07Z"
// >
//     <detail>
//     </detail>
//     <point 
//         lat="30.0090027"
//         lon="-85.9578735"
//         ce="45.3"
//         hae="-42.6"
//         le="99.5"
//     /> 
// </event>

#include <mxml.h>

mxml_node_t *createNewCoT() {
    mxml_node_t *xml;
    mxml_node_t *event;
    mxml_node_t *detail;
    mxml_node_t *point;

    xml = mxmlNewXML("1.0");
    mxmlElementSetAttr(xml, "standalone", "'yes'");

    event = mxmlNewElement(xml, "event");
    mxmlElementSetAttr(event, "version", "2.0");
    mxmlElementSetAttr(event, "uid", "TEST");
    mxmlElementSetAttr(event, "type", "a-h-A-M-F-U-M");
    mxmlElementSetAttr(event, "time", "2005-04-05T11:43:38.07Z");
    mxmlElementSetAttr(event, "start", "2005-04-05T11:43:38.07Z");
    mxmlElementSetAttr(event, "stale", "2005-04-05T11:43:38.07Z");

    detail = mxmlNewElement(event, "detail");

    point = mxmlNewElement(event, "point");
    mxmlElementSetAttr(point, "lat", "30.0090027");
    mxmlElementSetAttr(point, "lon", "-85.9578735");
    mxmlElementSetAttr(point, "ce", "45.3");
    mxmlElementSetAttr(point, "hae", "-42.5");
    mxmlElementSetAttr(point, "le", "99.5");

    return xml;
}

int main(int, argc, char *argv[]) {

}