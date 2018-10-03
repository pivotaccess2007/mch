#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

import csv
from decimal import *
from django.http import HttpResponse
from mako.template import Template
import ho.pisa as xhtml2pdf
import settings
from xml.dom.minidom import Document
import xlwt

class ExportUtil:

    @staticmethod
    def export(fieldnames, records, exportType):

        ext = 'csv'
        mime = 'text/csv'

        if '200' == exportType:
            mime = 'text/xml'
            ext = 'xml'
        if '300' == exportType:
            mime = 'text/html'
        if '400' == exportType:
            mime = 'application/pdf'
            ext = 'pdf'
        if '500' == exportType:
            mime = 'application/vnd.ms-excel'
            ext = 'xls'

    # Create the HttpResponse object with the appropriate header.
        response = HttpResponse(mimetype=mime)
        if not '300' == exportType:
            response['Content-Disposition'] = 'attachment; filename=export.' + ext

        if '200' == exportType:
            response = ExportUtil.exportToXML(response, records)
        elif '300' == exportType:
            response = ExportUtil.exportToHtml(response, records)
        elif '400' == exportType:
            response = ExportUtil.exportToPdf(response, records)
        elif '500' == exportType:
            response = ExportUtil.exportToXls(response, records , fieldnames)
        else:
            response = ExportUtil.exportToCSV(response, records, fieldnames)

        return response

    @staticmethod
    def exportToCSV(response, records, fieldnames):
        csv.register_dialect('apwstringsquoted', quoting=csv.QUOTE_ALL)

        writer = csv.DictWriter(response, fieldnames, dialect='apwstringsquoted')
        # headers
        headers = {}
        for n in fieldnames:
            headers[n] = n
        writer.writerow(headers)

        writer.writerows(row for row in records)

        return response
    
    @staticmethod
    def exportToPdf(response, records):
        template = Template(filename=settings.TEMPLATE_DIRS[0] + '/html_table_export.html')
        template.output_encoding = 'utf-8'

        html_text = template.render(params={'records': records})

        pdf = xhtml2pdf.CreatePDF(html_text, response)
        if not pdf.err:
            xhtml2pdf.startViewer(response)

        return response

    @staticmethod
    def exportToHtml(response, records):
        template = Template(filename=settings.TEMPLATE_DIRS[0] + '/html_table_export.html')
        template.output_encoding = 'utf-8'
        
        html_text = template.render(params={'records': records})
        
        response.write(html_text)

        return response

    @staticmethod
    def exportToXML(response, records, name="records"):
        "The keys are element names and the values are text"
        xml = Document()

        items = xml.createElement(name)
        
        xml.appendChild(items)

        for record in records:
            for key, val in record.items():
                node = xml.createElement(str(key))
                node.appendChild(xml.createTextNode(str(val)))
                items.appendChild(node)
                
        response.write(xml.toprettyxml())
            
        return response

    @staticmethod
    def exportToXls(response, data, headings):
        
        book = xlwt.Workbook(encoding='utf-8')
        sheet = book.add_sheet('export dd')

#        headings = []
#        for key, value in data[0].items():
#            headings.append(key)
#        
        rowx = 0
        for colx, value in enumerate(headings):
            sheet.write(rowx, colx, value)
        sheet.set_panes_frozen(True) # frozen headings instead of split panes
        sheet.set_horz_split_pos(rowx+1) # in general, freeze after last heading row
        sheet.set_remove_splits(True) # if user does unfreeze, don't leave a split there

        for row in data:
            rowx += 1

            for c, key in enumerate(row):
                sheet.write(rowx, c, row[key])

        book.save(response)

        return response
