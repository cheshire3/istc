from mod_python import apache

class testHandler:

     def send_html(self, data, req, code=200):
        req.content_type = 'text/html; charset=utf-8'
        req.content_length = len(data)
        req.send_http_header()
        if (type(data) == unicode):
            data = data.encode('utf-8')
        req.write(data)
        req.flush()

def handler(req):
    istcH = testHandler()
    istcH.send_html('Hello World', req)
    return apache.OK
