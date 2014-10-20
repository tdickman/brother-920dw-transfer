import requests
from xml.etree import ElementTree
import urllib
from os import walk
from pypdfocr import pypdfocr
import os


class Download:
    def __init__(self):
        pass

    def find_files(self):
        r = requests.get('http://10.10.100.1/:sda1/DCIM:.xml:Document:Sub')
        data = r.text.replace('<![CDATA[', '').replace(']]>', '')
        tree = ElementTree.fromstring(data)
        self.p = pypdfocr.PyPDFOCR()
        self.p.lang = 'eng'
        self.p.debug = False
        self.p._setup_external_tools()

        files = []
        for child in tree.findall('.//Document'):
            files.append({
                'name': child.find('.//NAME').text,
                'path': child.find('.//FPATH').text
                })

        return files

    def file_exists(self, path, file_name):
        for (dirpath, dirnames, filenames) in walk(path):
            if file_name in filenames:
                return True
        return False

    def download_file(self, file, ocr=True):
        if not self.file_exists('files', file['name'].replace('PDF', 'pdf')):
            print "Retrieving {}".format(file['name'])
            dest_file = "files/{}".format(file['name'])
            get_it = urllib.URLopener()
            get_it.retrieve("http://10.10.100.1/{}".format(file['path']), dest_file)
            self.ocr(dest_file)

    def ocr(self, original_filename):
        self.p.run_conversion(original_filename)
        dest_filename = original_filename.replace('.PDF', "_ocr.pdf")
        os.remove(original_filename)
        os.rename(dest_filename, original_filename.replace('PDF', 'pdf'))


if __name__ == "__main__":
    d = Download()
    for file in d.find_files():
        d.download_file(file)
