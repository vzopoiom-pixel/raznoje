from http.server import HTTPServer, BaseHTTPRequestHandler
import os


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")


        if "/shutdown" in self.path:
            print("Выключение!")
            os.system("shutdown /s /t 3")
        elif "/reboot" in self.path:
            print("Перезагрузка!")
            os.system("shutdown /r /t 3")

    def log_message(self, format, *args):
        print(f"Запрос: {args[0]}")


print("Сервер запущен на порту 8080...")
HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()