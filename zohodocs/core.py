import re
import urllib
import uuid
import os.path
import tempfile
try:
    import pycurl
except ImportError:
    raise ImportError('PyCurl is necessary! `pip install pycurl`')

SERVERS = (
    (re.compile(r'\.(docx?|rtf|odt|sxw|html|txt)$', re.I), 'export.writer'),
    (re.compile(r'\.(xlsx?|ods|sxc|csv|tsv)$', re.I), 'sheet'),
    (re.compile(r'\.(ppt|pps|odp|sxi)$', re.I), 'show'),
)

ZOHO_ENDPOINT = 'https://%s.zoho.com/remotedoc.im'
URL_PATTERN = re.compile(r'^https?://')

class ZohoDocsException(Exception):
    pass

class ZohoDocsAPIError(ZohoDocsException):
    pass

class ZohoDocsFileFormatError(ZohoDocsException):
    pass

class ZohoDocsResponse(object):
    __keys = {}
    def write(self, data):
        self.__parse(data)
    
    def __parse(self, raw_response):
        raw_response.strip()
        lines = raw_response.splitlines()
        for l in lines:
            l.strip()
            if l:
                try:
                    key, value = l.split('=', 1)
                    if value == 'TRUE':
                        value = True
                    elif value == 'False':
                        value = False
                    elif value == 'NULL':
                        value = None
                    self.__keys[key] = value
                except ValueError:
                    pass
            
    def __getitem__(self, key):
        return self.__keys[key]
    
    def __contains__(self, key):
        return key in self.__keys

class ZohoDocs(object):
    def __init__(self, api_key, save_url=None, language='en'):
        self.api_key = api_key
        self.save_url = save_url
        self.language = language
    
    def __parse_file_type(self, filename):
        for i in SERVERS:
            match = i[0].search(filename)
            if match:
                return i[1], match.group(1)
        raise ZohoDocsFileFormatError('Invalid file format!')
    
    def __request(self, server, **options):
        endpoint = ZOHO_ENDPOINT % server
        opts = {
            'apikey': self.api_key,
            'output': 'url',
            'lang': self.language,
            'mode': 'normaledit',
        }
        opts.update(options)
        if not 'id' in opts:
            opts['id'] = uuid.uuid4().hex # Keep Zoho from bitching about a missing id
        conn = pycurl.Curl()
        res = ZohoDocsResponse()
        conn.setopt(pycurl.URL, endpoint)
        conn.setopt(pycurl.HEADER, False)
        conn.setopt(pycurl.POST, True)
        conn.setopt(pycurl.HTTPPOST, list([(k, opts[k]) for k in opts]))
        conn.setopt(pycurl.WRITEFUNCTION, res.write)
        conn.perform()
        conn.close()
        if not res['RESULT']:
            raise ZohoDocsAPIError('Request failed[%s]: "%s"' % (500, res['WARNING']))
        return res['URL']
    
    def new_file(self, filename, **options):
        server, format = self.__parse_file_type(filename)
        opts = {
            'filename': filename,
            'format': format,
        }
        opts.update(options)
        return self.__request(server, **opts)
    
    def open(self, file_, **options):
        if isinstance(file_, basestring) and os.path.isfile(file_):
            options['content'] = (pycurl.FORM_FILE, os.path.abspath(file_))
            filename = os.path.basename(file_)
        elif hasattr(file_, 'read') and callable(file_.read):
            options['content'] = (pycurl.FORM_CONTENTS, file_.read())
            try:
                filename = file_.name
            except AttributeError:
                try:
                    filename = opts['filename']
                except KeyError:
                    raise ZohoDocsAPIError('Filename must be specified. Type could not be determined automatically.')
        
        server, format = self.__parse_file_type(filename)
        opts = {
            'format' : format,
            'filename': filename,
        }
        opts.update(options)
        return self.__request(server, **opts)
    
    def open_url(self, url, **options):
        match = URL_PATTERN.search(url)
        if not match:
            raise ZohoDocsAPIError('Not a valid URL. Must start with http or https: %s' % url)
        filename = os.path.basename(url)
        server, format = self.__parse_file_type(filename)
        opts = {
            'format': format,
            'filename': filename,
            'url': url,
        }
        opts.update(options)
        return self.__request(server, **opts)