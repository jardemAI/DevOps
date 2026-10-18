"""Small standard-library HTTP application for the DevOps lab."""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def student_details():
    return {
        "name": os.getenv("STUDENT_NAME", "Danil"),
        "surname": os.getenv("STUDENT_SURNAME", "Marchenko"),
        "group": os.getenv("STUDENT_GROUP", "IT2-2303"),
        "student_id": os.getenv("STUDENT_ID", "41587"),
    }


def application_version():
    return os.getenv("APP_VERSION", "1.0.0")


def application_metadata():
    metadata = student_details()
    metadata["version"] = application_version()
    return metadata


def readiness_status():
    return {"status": "ready", "version": application_version()}


class StudentApplicationHandler(BaseHTTPRequestHandler):
    server_version = "DevOpsStudentApp/1.0"

    def do_GET(self):
        content_type = "text/plain; charset=utf-8"
        if self.path == "/health":
            body = "OK\n"
            status = 200
        elif self.path == "/ready":
            body = json.dumps(readiness_status(), indent=2) + "\n"
            content_type = "application/json; charset=utf-8"
            status = 200
        elif self.path == "/metadata":
            body = json.dumps(application_metadata(), indent=2) + "\n"
            content_type = "application/json; charset=utf-8"
            status = 200
        elif self.path == "/version":
            body = application_version() + "\n"
            status = 200
        elif self.path in ("/", "/student"):
            details = student_details()
            body = (
                "================================\n"
                "DevOps Student Application\n"
                "================================\n\n"
                f"Name: {details['name']}\n"
                f"Surname: {details['surname']}\n"
                f"Group: {details['group']}\n"
                f"Student ID: {details['student_id']}\n\n"
                "Application is running successfully!\n"
            )
            status = 200
        else:
            body = "Not Found\n"
            status = 404

        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, fmt, *args):
        print("%s - - [%s] %s" % (self.address_string(), self.log_date_time_string(), fmt % args), flush=True)


def main():
    port = int(os.getenv("PORT", "8000"))
    details = student_details()
    print("================================", flush=True)
    print("DevOps Student Application", flush=True)
    print("================================", flush=True)
    print(f"Student: {details['name']} {details['surname']}", flush=True)
    print(f"Group: {details['group']}", flush=True)
    print(f"Student ID: {details['student_id']}", flush=True)
    print(f"Listening on port {port}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), StudentApplicationHandler).serve_forever()


if __name__ == "__main__":
    main()
