import re
import uuid
import os.path
try:
    import requests
except ImportError:
    raise ImportError('python-requests is necessary! `pip install requests`')

# (file pattern, server)
ZOHO_SERVERS = (
    (re.compile(r'\.(docx?|rtf|odt|sxw|html|txt)$', re.I), 'exportwriter'),
    (re.compile(r'\.(xlsx?|ods|sxc|csv|tsv)$', re.I), 'sheet'),
    (re.compile(r'\.(ppt|pps|odp|sxi)$', re.I), 'show'),
)

ZOHO_ENDPOINT = 'https://%s.zoho.com/remotedoc.im'
URL_PATTERN = re.compile(r'^https?://', re.I)

class ZohoDocsException(Exception): pass
class ZohoDocsAPIError(ZohoDocsException): pass
class ZohoDocsFileFormatError(ZohoDocsException): pass

class ZohoDocsResponse(object):
    """Hole for `requests' to write into. Also nicely parses Zoho's response into k/v pairs."""
    __keys = {}
    def write(self, data):
        self.__parse(data)
    
    def __parse(self, raw_response):
        """Response is all k/v pairs separated by a newline.

        Example response:
        URL=https://....
        RESULT=TRUE
        DOCUMENTID=...
        """
        raw_response = raw_response.strip()
        lines = raw_response.splitlines()
        for l in lines:
            l = l.strip()
            if l:
                try:
                    key, value = l.split('=', 1)

                    # Convert known values to Python types
                    if value == 'TRUE':
                        value = True
                    elif value == 'FALSE':
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
    def __init__(self, api_key, language='en'):
        self.api_key = api_key
        self.language = language
    
    def __parse_file_type(self, filename):
        """Determine which Zoho server to send request to and the file format."""
        for i in ZOHO_SERVERS:
            match = i[0].search(filename)
            if match:
                # e.g. (server, format)
                return i[1], match.group(1)
        raise ZohoDocsFileFormatError('Invalid file format!')
    
    def __request(self, server, options=None, files=None):
        if options is None:
            options = {}
        opts = {
            'apikey': self.api_key,
            'output': 'url',
            'lang': self.language,
            'mode': 'normaledit',
        }
        opts.update(options)
        
        # Zoho needs an id to be set
        if not 'id' in opts:
            opts['id'] = uuid.uuid4().hex # generate an id
        
        opts['id'] = str(opts['id'])
        
        res = ZohoDocsResponse()
        req = requests.post(ZOHO_ENDPOINT % server, data=opts, files=files)
        res.write(req.text)

        if not res['RESULT']:
            raise ZohoDocsAPIError('Request failed[%s]: "%s"' % (500, res['WARNING']))
        
        return res['URL']
    
    def new_file(self, filename, **options):
        """Tell Zoho to create a new blank document."""
        server, format = self.__parse_file_type(filename)
        opts = {
            'filename': filename,
            'format': format,
        }
        opts.update(options)
        return self.__request(server, options=opts)
    
    def open(self, file_, **options):
        """Send Zoho a filepath or file contents."""
        # Check first if it's a file path
        if isinstance(file_, basestring) and os.path.isfile(file_):
            fp = open(os.path.abspath(file_), 'rb')
            filename = os.path.basename(file_)
        # Maybe it's a file-like object?
        elif hasattr(file_, 'read') and callable(file_.read):
            fp = file_
            try:
                # Try and grab name from file object
                filename = file_.name
            except AttributeError:
                try:
                    # Hopefully it was passed in manually as an option
                    filename = options['filename']
                except KeyError:
                    raise ZohoDocsAPIError('Filename must be specified. Type could not be determined automatically.')
        else:
            raise ZohoDocsAPIError('Invalid file input: %s' % file_)
        
        server, format = self.__parse_file_type(filename)
        opts = {
            'format' : format,
            'filename': filename,
        }
        opts.update(options)
        return self.__request(server, options=opts, files={'content': (filename, fp)})
    
    def open_url(self, url, **options):
        """Pass a URL for Zoho to open."""
        match = URL_PATTERN.search(url)
        if not match:
            raise ZohoDocsAPIError('Not a valid URL. Must start with http or https: %s' % url)
        if 'filename' in options:
            filename = options['filename']
        else:
            filename = os.path.basename(url)
        server, format = self.__parse_file_type(filename)
        opts = {
            'format': format,
            'filename': filename,
            'url': url,
        }
        opts.update(options)
        return self.__request(server, options=opts)
