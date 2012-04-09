# python-zohodocs
  
  A simple library for interacting with Zoho Docs ([Writer](https://writer.zoho.com/), [Sheet](https://sheet.zoho.com), and [Show](https://show.zoho.com/))

## Installation
```$ pip install zohodocs```

## Getting Started
  
```python
from zohodocs import ZohoDocs
```

### Creating a new Document
  
```python
z = ZohoDocs(API_KEY)
print z.new_file('document1.doc')
```

### Opening a Document
  
  All methods return a URL which links to the editor. Optional arguments match with Zoho's documented API: https://apihelp.wiki.zoho.com/Open-Document.html
  
```python
z = ZohoDocs(API_KEY)
# Local document
print z.open('/var/www/document.doc')
# File pointer
fp = open('/var/www/document.doc', 'r')
print z.open(fp)
# URL
print z.open_url('http://example.com/document.doc')
# Optional arguments
print z.open('/var/www/document.doc', id='myid', saveurl='http://example.com/save.php')
```

## License 

(The MIT License)

Copyright (c) 2011 Matt Robenolt &lt;matt@ydekproductions.com&gt;

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
