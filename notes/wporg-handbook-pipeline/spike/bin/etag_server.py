"""Static file server that mimics raw.githubusercontent.com's caching behaviour closely
enough for the wporg-markdown importer: strong ETag (sha1 of body), 304 on If-None-Match,
query strings ignored (the importer appends ?v=<time()>). Logs every request with status.

Usage: python3 -I etag_server.py <root-dir> <port> [--no-etag]
"""
import hashlib
import http.server
import os
import sys
import urllib.parse

ROOT = os.path.abspath(sys.argv[1])
PORT = int(sys.argv[2])
NO_ETAG = "--no-etag" in sys.argv


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = urllib.parse.urlsplit(self.path).path
        fs = os.path.normpath(os.path.join(ROOT, urllib.parse.unquote(path).lstrip("/")))
        if not fs.startswith(ROOT) or not os.path.isfile(fs):
            self.send_response(404)
            self.end_headers()
            return
        body = open(fs, "rb").read()
        etag = '"%s"' % hashlib.sha1(body).hexdigest()
        if not NO_ETAG and self.headers.get("If-None-Match") == etag:
            self.send_response(304)
            self.send_header("ETag", etag)
            self.end_headers()
            return
        self.send_response(200)
        ctype = "application/json" if fs.endswith(".json") else "text/plain; charset=utf-8"
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        if not NO_ETAG:
            self.send_header("ETag", etag)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s\n" % (fmt % args))


http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
