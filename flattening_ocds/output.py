"""Code to output a parsed flattened JSON schema in various spreadsheet
formats."""

import openpyxl
import csv
import os


class SpreadsheetOutput(object):
    # output_name is given a default here, partly to help with tests,
    # but should have been defined by the time we get here.
    def __init__(self, parser, main_sheet_name='main', output_name='release'):
        self.parser = parser
        self.main_sheet_name = main_sheet_name
        self.output_name = output_name

    def open(self):
        pass

    def write_sheet(self, sheet_name, sheet_header):
        raise NotImplementedError

    def write_sheets(self):
        self.open()

        self.write_sheet(self.main_sheet_name, self.parser.main_sheet)
        for sheet_name, sheet_header in sorted(self.parser.sub_sheets.items()):
            self.write_sheet(sheet_name, list(sheet_header))

        self.close()

    def close(self):
        pass


class XLSXOutput(SpreadsheetOutput):
    def open(self):
        self.workbook = openpyxl.Workbook()

    def write_sheet(self, sheet_name, sheet_header):
        worksheet = self.workbook.create_sheet()
        worksheet.title = sheet_name
        worksheet.append(sheet_header)

    def close(self):
        self.workbook.remove_sheet(self.workbook.active)
        self.workbook.save(self.output_name)


class CSVOutupt(SpreadsheetOutput):
    def open(self):
        try:
            os.makedirs(self.output_name)
        except OSError:
            pass

    def write_sheet(self, sheet_name, sheet_header):
        with open(os.path.join(self.output_name, sheet_name+'.csv'), 'w') as csv_file:
            csv_sheet = csv.writer(csv_file)
            csv_sheet.writerow(sheet_header)


FORMATS = {
    'xlsx': XLSXOutput,
    'csv': CSVOutupt
}
FORMATS_SUFFIX = {
    'xlsx': '.xlsx',
    'csv': '' # This is the suffix for the directory
}
