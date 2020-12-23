#!/usr/bin/env python
# coding=utf-8

'''
Version: 0.1
Autor: zmf96
Email: zmf96@qq.com
Date: 2020-12-14 18:23:33
LastEditors: zmf96
LastEditTime: 2020-12-22 17:13:43
FilePath: /httpbinasync/core.py
Description: 
'''
import argparse
import os
import random
import time
import uuid

from sanic import Sanic, response
from sanic.response import file, json, raw, redirect, stream, text
from sanic.log import logger
from sanic_openapi import swagger_blueprint

from helpers import get_dict, get_headers, ROBOT_TXT, ANGRY_ASCII, get_request_range

import filters
import base64
from structures import CaseInsensitiveDict
import asyncio

tmpl_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "templates")

app = Sanic(name="httpbinasync")
app.blueprint(swagger_blueprint)


"""HTTP Methods
Testing different HTTP verbs
"""


@app.route("/get", methods=("GET",))
async def view_get(request):
    """The request's query parameters.
    ---
    tags:
      - HTTP Methods
    produces:
      - application/json
    responses:
      200:
        description: The request's query parameters.
    """
    return json(
        get_dict(request, "url", "args", "headers",
                 "origin"))


@app.route("/post", methods=("POST",))
async def view_post(request):
    """The request's POST parameters.
    ---
    tags:
      - HTTP Methods
    produces:
      - application/json
    responses:
      200:()
        description: The request's POST parameters.
    """
    return json(
        get_dict(request, "url", "args", "form",
                 "json", "headers", "files", "origin"))


@app.route("/put", methods=("PUT",))
async def view_put(request):
    """The request's PUT parameters.
    ---
    tags:
      - HTTP Methods
    produces:
      - application/json
    responses:
      200:
        description: The request's PUT parameters.
    """

    return json(
        get_dict(request, "url", "args", "form", "data",
                 "origin", "headers", "files", "json")
    )


@app.route("/patch", methods=("PATCH",))
async def view_patch(request):
    """The request's PATCH parameters.
    ---
    tags:
      - HTTP Methods
    produces:
      - application/json
    responses:
      200:
        description: The request's PATCH parameters.
    """

    return json(
        get_dict(request, "url", "args", "form", "data",
                 "origin", "headers", "files", "json")
    )


@app.route("/delete", methods=("DELETE",))
async def view_delete(request):
    """The request's DELETE parameters.
    ---
    tags:
      - HTTP Methods
    produces:
      - application/json
    responses:
      200:
        description: The request's DELETE parameters.
    """

    return json(
        get_dict(request, "url", "args", "form", "data",
                 "origin", "headers", "files", "json")
    )


"""Auth
Auth methods
"""

"""Status codes
Generates responses with given status code
"""


"""Request inspection
Inspect the request data
"""


@app.route("/ip")
async def view_origin(request):
    """Returns the requester's IP Address.
    ---
    tags:
      - Request inspection
    produces:
      - application/json
    responses:
      200:
        description: The Requester's IP Address.
    """

    return json({"origin": request.headers.get("X-Forwarded-For", request.ip)})


@app.route("/headers")
async def view_headers(request):
    """Return the incoming request's HTTP headers.
    ---
    tags:
      - Request inspection
    produces:
      - application/json
    responses:
      200:
        description: The request's headers.
    """

    return json(get_dict(request, 'headers'))


@app.route("/user-agent")
async def view_user_agent(request):
    """Return the incoming requests's User-Agent header.
    ---
    tags:
      - Request inspection
    produces:
      - application/json
    responses:
      200:
        description: The request's User-Agent header.
    """

    headers = get_headers(request)

    return json({"user-agent": headers["user-agent"]})


"""Response formats
Returns responses in different data formats
"""


@app.route("/gzip")
@filters.gzip
async def view_gzip_encoded_content(request):
    """Returns GZip-encoded data.
    ---
    tags:
      - Response formats
    produces:
      - application/json
    responses:
      200:
        description: GZip-encoded data.
    """

    return json(get_dict(request, "origin", "headers", method=request.method, gzipped=True))


@app.route("/deflate")
@filters.deflate
async def view_deflate_encoded_content(request):
    """Returns Deflate-encoded data.
    ---
    tags:
      - Response formats
    produces:
      - application/json
    responses:
      200:
        description: Defalte-encoded data.
    """

    return json(get_dict(request, "origin", "headers", method=request.method, deflated=True))


@app.route("/robots.txt")
async def view_robots_page(request):
    """Returns some robots.txt rules.
    ---
    tags:
      - Response formats
    produces:
      - text/plain
    responses:
      200:
        description: Robots file
    """
    return text(ROBOT_TXT)


@app.route("/deny")
async def view_deny_page(request):
    """Returns page denied by robots.txt rules.
    ---
    tags:
      - Response formats
    produces:
      - text/plain
    responses:
      200:
        description: Denied message
    """
    return text(ANGRY_ASCII)
    # return "YOU SHOULDN'T BE HERE"


@app.route("/encoding/utf8")
async def encoding(request):
    """Returns a UTF-8 encoded body.
    ---
    tags:
      - Response formats
    produces:
      - text/html
    responses:
      200:
        description: Encoded UTF-8 content.
    """

    return file(tmpl_dir+"/UTF-8-demo.txt")


@app.route("/html")
async def view_html_page(request):
    """Returns a simple HTML document.
    ---
    tags:
      - Response formats
    produces:
      - text/html
    responses:
      200:
        description: An HTML page.
    """

    return file(tmpl_dir+"/moby.html")


@app.route("/brotli")
@filters.brotli
async def view_brotli_encoded_content(request):
    """Returns Brotli-encoded data.
    ---
    tags:
      - Response formats
    produces:
      - application/json
    responses:
      200:
        description: Brotli-encoded data.
    """

    return json(get_dict(request, "origin", "headers", method=request.method, brotli=True))


@app.route("/xml")
async def xml(request):
    """Returns a simple XML document.
    ---
    tags:
      - Response formats
    produces:
      - application/xml
    responses:
      200:
        description: An XML document.
    """
    # response = make_response(render_template("sample.xml"))
    # text.headers["Content-Type"] = "application/xml"
    return file(tmpl_dir+"/sample.xml")


@app.route("/json")
async def a_json_endpoint(request):
    """Returns a simple JSON document.
    ---
    tags:
      - Response formats
    produces:
      - application/json
    responses:
      200:
        description: An JSON document.
    """
    return json(
        {
            "slideshow": {
                "title": "Sample Slide Show",
                "date": "date of publication",
                "author": "Yours Truly",
                "slides": [
                    {"type": "all", "title": "Wake up to WonderWidgets!"},
                    {
                        "type": "all",
                        "title": "Overview",
                        "items": [
                            "Why <em>WonderWidgets</em> are great",
                            "Who <em>buys</em> WonderWidgets",
                        ],
                    },
                ],
            }
        }
    )


"""Dynamic data
Generates random and dynamic data
"""


@app.route("/base64/<value>")
def decode_base64(request, value):
    """Decodes base64url-encoded string.
    ---
    tags:
      - Dynamic data
    parameters:
      - in: path
        name: value
        type: string
        default: SFRUUEJJTiBpcyBhd2Vzb21l
    produces:
      - text/html
    responses:
      200:
        description: Decoded base64 content.
    """
    encoded = value.encode("utf-8")  # base64 expects binary string as input
    try:
        return text(base64.urlsafe_b64decode(encoded).decode("utf-8"))
    except:
        return "Incorrect Base64 data try: SFRUUEJJTiBpcyBhd2Vzb21l"


@app.route("/bytes/<n:int>")
def random_bytes(request, n):
    """Returns n random bytes generated with given seed
    ---
    tags:
      - Dynamic data
    parameters:
      - in: path
        name: n
        type: int
    produces:
      - application/octet-stream
    responses:
      200:
        description: Bytes.
    """

    n = min(n, 100 * 1024)  # set 100KB limit

    params = CaseInsensitiveDict(request.args.items())
    if "seed" in params:
        random.seed(int(params["seed"]))

    # response = make_response()

    # Note: can't just use os.urandom here because it ignores the seed
    data = bytearray(random.randint(0, 255) for i in range(n))
    # response.content_type = "application/octet-stream"
    return raw(data, content_type="application/octet-stream")


# @app.route("/stream-bytes/<int:n>")
# def stream_random_bytes(request,n):
#     """Streams n random bytes generated with given seed, at given chunk size per packet.
#     ---
#     tags:
#       - Dynamic data
#     parameters:
#       - in: path
#         name: n
#         type: int
#     produces:
#       - application/octet-stream
#     responses:
#       200:
#         description: Bytes.
#     """
#     n = min(n, 100 * 1024)  # set 100KB limit

#     params = CaseInsensitiveDict(request.args.items())
#     if "seed" in params:
#         random.seed(int(params["seed"]))

#     if "chunk_size" in params:
#         chunk_size = max(1, int(params["chunk_size"]))
#     else:
#         chunk_size = 10 * 1024

#     def generate_bytes():
#         chunks = bytearray()

#         for i in xrange(n):
#             chunks.append(random.randint(0, 255))
#             if len(chunks) == chunk_size:
#                 yield (bytes(chunks))
#                 chunks = bytearray()

#         if chunks:
#             yield (bytes(chunks))

#     headers = {"Content-Type": "application/octet-stream"}

#     return Response(generate_bytes(), headers=headers)


@app.route("/range/<numbytes:int>")
async def range_request(request, numbytes):
    """Streams n random bytes generated with given seed, at given chunk size per packet.
    ---
    tags:
      - Dynamic data
    parameters:
      - in: path
        name: numbytes
        type: int
    produces:
      - application/octet-stream
    responses:
      200:
        description: Bytes.
    """

    if numbytes <= 0 or numbytes > (100 * 1024):
        return text("number of bytes must be in the range (0, 102400]", headers={"ETag": "range%d" % numbytes, "Accept-Ranges": "bytes"}, status=404)

    params = CaseInsensitiveDict(request.args.items())
    if "chunk_size" in params:
        chunk_size = max(1, int(params["chunk_size"]))
    else:
        chunk_size = 10 * 1024

    duration = float(params.get("duration", 0))
    pause_per_byte = duration / numbytes

    request_headers = get_headers(request)
    first_byte_pos, last_byte_pos = get_request_range(
        request_headers, numbytes)
    range_length = (last_byte_pos + 1) - first_byte_pos

    if (
        first_byte_pos > last_byte_pos
        or first_byte_pos not in range(0, numbytes)
        or last_byte_pos not in range(0, numbytes)
    ):
        return text(headers={
            "ETag": "range%d" % numbytes,
            "Accept-Ranges": "bytes",
            "Content-Range": "bytes */%d" % numbytes,
            "Content-Length": "0",
        }, status=416)

    async def generate_bytes(response):
        chunks = bytearray()

        for i in range(first_byte_pos, last_byte_pos + 1):

            # We don't want the resource to change across requests, so we need
            # to use a predictable data generation function
            chunks.append(ord("a") + (i % 26))
            if len(chunks) == chunk_size:
                # yield (bytes(chunks))
                await response.write(bytes(chunks))
                time.sleep(pause_per_byte * chunk_size)
                chunks = bytearray()

        if chunks:
            time.sleep(pause_per_byte * len(chunks))
            await response.write(bytes(chunks))

    content_range = "bytes %d-%d/%d" % (first_byte_pos,
                                        last_byte_pos, numbytes)
    response_headers = {
        "Content-Type": "application/octet-stream",
        "ETag": "range%d" % numbytes,
        "Accept-Ranges": "bytes",
        "Content-Length": str(range_length),
        "Content-Range": content_range,
    }
    if (first_byte_pos == 0) and (last_byte_pos == (numbytes - 1)):
        status_code = 200
    else:
        status_code = 206

    return stream(generate_bytes,headers=response_headers,status=status_code)


@app.route("/links/<n:int>/<offset:int>")
async def link_page(request, n, offset):
    """Generate a page containing n links to other pages which do the same.
    ---
    tags:
      - Dynamic data
    parameters:
      - in: path
        name: n
        type: int
      - in: path
        name: offset
        type: int
    produces:
      - text/html
    responses:
      200:
        description: HTML links.
    """
    n = min(max(1, n), 200)  # limit to between 1 and 200 links

    link = "<a href='{0}'>{1}</a> "

    html = ["<html><head><title>Links</title></head><body>"]
    for i in range(n):
        if i == offset:
            html.append("{0} ".format(i))
        else:
            html.append(link.format(app.url_for(
                "link_page", n=n, offset=i), i))
    html.append("</body></html>")

    return response.html("".join(html))


@app.route("/links/<n:int>")
async def links(request, n):
    """Redirect to first links page."""
    return redirect(app.url_for("link_page", n=n, offset=0))


@app.route("/delay/<delay>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "TRACE"])
def delay_response(request, delay):
    """Returns a delayed response (max of 10 seconds).
    ---
    tags:
      - Dynamic data
    parameters:
      - in: path
        name: delay
        type: int
    produces:
      - application/json
    responses:
      200:
        description: A delayed response.
    """
    delay = min(float(delay), 10)

    time.sleep(delay)

    return json(
        get_dict(request, "url", "args", "form",
                 "data", "origin", "headers", "files")
    )


@app.route("/drip")
async def drip(request):
    """Drips data over a duration after an optional initial delay.
    ---
    tags:
      - Dynamic data
    parameters:
      - in: query
        name: duration
        type: number
        description: The amount of time (in seconds) over which to drip each byte
        default: 2
        required: false
      - in: query
        name: numbytes
        type: integer
        description: The number of bytes to respond with
        default: 10
        required: false
      - in: query
        name: code
        type: integer
        description: The response code that will be returned
        default: 200
        required: false
      - in: query
        name: delay
        type: number
        description: The amount of time (in seconds) to delay before responding
        default: 2
        required: false
    produces:
      - application/octet-stream
    responses:
      200:
        description: A dripped response.
    """
    args = CaseInsensitiveDict(request.args.items())
    duration = float(args.get("duration", 2)[0])
    # set 10MB limit
    numbytes = min(int(args.get("numbytes", 10)[0]), (10 * 1024 * 1024))
    code = int(args.get("code", 200)[0])

    if numbytes <= 0:
        return text("number of bytes must be positive", status=400)

    delay = float(args.get("delay", 0)[0])
    if delay > 0:
        time.sleep(delay)

    pause = duration / numbytes

    async def generate_bytes(response):
        for i in range(numbytes):
            await response.write("*")
            asyncio.sleep(pause)

    return stream(generate_bytes, content_type="application/octet-stream", chunked=False, status=code)


@app.route("/uuid")
async def view_uuid(request):
    """Return a UUID4.
    ---
    tags:
      - Dynamic data
    produces:
      - application/json
    responses:
      200:
        description: A UUID4.
    """

    return json({"uuid": str(uuid.uuid4())})


"""Cookies
Creates, reads and deletes Cookies
"""

"""Images
Returns different image formats
"""

"""Redirects
Returns different redirect responses
"""

"""Anything
Returns anything that is passed to request
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=80)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=True)
