#!/usr/bin/env python3
"""Static file server that behaves like raw.githubusercontent.com for the importer:
strong ETag (md5 of the body) on every 200, and 304 when If-None-Match matches.
The wporg-markdown importer stores the ETag per post and skips unchanged files on 304,
so `python3 -m http.server` (no ETag) would make every re-import rewrite every post.

Usage: python3 -I serve.py <root-dir> [port]      (binds 0.0.0.0; default port 8765)
"""
import functools
import hashlib
import http.server
import os
import sys
import urllib.parse


class Handler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.translate_path(urllib.parse.urlsplit(self.path).path)
        if os.path.isfile(path):
            with open(path, "rb") as f:
                body = f.read()
            etag = '"%s"' % hashlib.md5(body).hexdigest()
            if self.headers.get("If-None-Match") == etag:
                self.send_response(304)
                self.send_header("ETag", etag)
                self.end_headers()
                return None
            self.send_response(200)
            ctype = "application/json" if path.endswith(".json") else "text/plain; charset=utf-8"
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("ETag", etag)
            self.end_headers()
            import io
            return io.BytesIO(body)
        return super().send_head()


def main():
    root = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8765
    handler = functools.partial(Handler, directory=root)
    http.server.ThreadingHTTPServer(("0.0.0.0", port), handler).serve_forever()


if __name__ == "__main__":
    main()
