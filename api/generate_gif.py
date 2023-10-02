from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from PIL import Image, ImageDraw
from datetime import datetime
from io import BytesIO
import time

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/gif')
        self.end_headers()

        query = urlparse(self.path).query
        query_components = parse_qs(query)
        end_time_str = query_components.get("end_time", [None])[0]

        if not end_time_str:
            return

        end_time = datetime.fromisoformat(end_time_str)
        remaining_seconds = int((end_time - datetime.utcnow()).total_seconds())

        frames = []
        for i in range(52, 6, -1):
            frame = Image.new('RGBA', (100, 100), 'white')
            d = ImageDraw.Draw(frame)
            d.text((10, 40), f"{remaining_seconds} s", fill=(0, 0, 0))
            frames.append(frame)
            remaining_seconds -= 1

        gif_buffer = BytesIO()
        frames[0].save(gif_buffer, save_all=True, append_images=frames[1:], loop=0, duration=1000)

        gif_buffer.seek(0)
        self.wfile.write(gif_buffer.read())
