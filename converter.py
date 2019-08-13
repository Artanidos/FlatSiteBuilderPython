import sys
import html
from xml.dom import minidom

def writeNumericAttribute(name, content, fp, indent=4):
    if content.attributes and name in content.attributes:
        fp.write(" " * indent + name + ": " + content.attributes[name].value + "\n")

def writeAttribute(name, content, fp, indent=4):
    if content.attributes and name in content.attributes:
        if name == "date":
            date = content.attributes[name].value
            content.attributes[name].value = date[6:10] + "-" + date[3:5] + "-" + date[0:2]
        if content.attributes[name].value == "true" or content.attributes[name].value == "false":
            fp.write(" " * indent + name + ": "  + content.attributes[name].value + "\n")
        else:
            fp.write(" " * indent + name + ": \"" + content.attributes[name].value + "\"\n")

inputFile = sys.argv[1]
xmldoc = minidom.parse(inputFile)
content = xmldoc.getElementsByTagName('Content')[0]
sections = content.getElementsByTagName('Section')

atts = ["title", "menu", "author", "layout", "keywords", "date", "logo", "language"]
outputFile = inputFile.replace(".xml", ".qml")
with open(outputFile, "w") as fp:
    fp.write("import FlatSiteBuilder 2.0\n")
    fp.write("import RevolutionSlider 1.0\n")
    fp.write("import TextEditor 1.0\n\n")
    fp.write("Content {\n")
    for att in atts:
        writeAttribute(att, content, fp)
    for section in sections:
        fp.write("    Section {\n")
        writeAttribute("fullwidth", section, fp, 8)
        for node in section.childNodes:
            if node.nodeName == "Text":
                fp.write("        Text {\n")
                writeAttribute("adminlabel", node, fp, 12)
                fp.write("            text: \"" + html.escape(node.firstChild.wholeText) + "\"\n")
                fp.write("        }\n")
            elif node.nodeName == "RevolutionSlider":
                fp.write("        RevolutionSlider {\n")
                rs_atts = ["adminlabel","fullwidth", "fullscreen"]
                for att in rs_atts:
                    writeAttribute(att, node, fp, 12)
                for slide in node.childNodes:
                    fp.write("            Slide {\n")
                    writeAttribute("src", slide, fp, 16)
                    writeAttribute("adminlabel", slide, fp, 16)
                    fp.write("                text: \"" + html.escape(slide.firstChild.wholeText) + "\"\n")
                    fp.write("            }\n")
                fp.write("        }\n")
            elif node.nodeName == "Row":
                fp.write("        Row {\n")
                for column in node.childNodes:
                    if column.nodeName == "Column":
                        fp.write("            Column {\n")
                        writeNumericAttribute("span", column, fp, 16)
                        for n in column.childNodes:
                            fp.write("                " + n.nodeName + " {\n")
                            if n.nodeName == "AdvancedImage":
                                ai_atts = ["src", "alt", "title", "url", "animation", "adminlabel"]
                                for att in ai_atts:
                                    writeAttribute(att, n, fp, 20)
                            elif n.nodeName == "Text":
                                writeAttribute("adminlabel", n, fp, 20)
                                fp.write(" " * 20 + "text: \"" + html.escape(n.firstChild.wholeText) + "\"\n")
                            fp.write("                }\n")
                        fp.write("            }\n")
                fp.write("        }\n")
        fp.write("    }\n")
    fp.write("}\n")