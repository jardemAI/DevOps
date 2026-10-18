import os
import unittest
from unittest.mock import patch

from app.server import application_metadata, application_version, readiness_status, student_details


class StudentDetailsTests(unittest.TestCase):
    def test_metadata_includes_student_and_version(self):
        with patch.dict(os.environ, {"APP_VERSION": "3.0.0"}, clear=True):
            self.assertEqual(application_metadata(), {
                "name": "Danil",
                "surname": "Marchenko",
                "group": "IT2-2303",
                "student_id": "41587",
                "version": "3.0.0",
            })

    def test_application_version_can_be_configured(self):
        with patch.dict(os.environ, {"APP_VERSION": "2.1.0"}, clear=False):
            self.assertEqual(application_version(), "2.1.0")

    def test_readiness_status_reports_ready_and_version(self):
        with patch.dict(os.environ, {"APP_VERSION": "3.1.0"}, clear=True):
            self.assertEqual(readiness_status(), {"status": "ready", "version": "3.1.0"})

    def test_environment_variables_override_defaults(self):
        with patch.dict(os.environ, {
            "STUDENT_NAME": "TestName",
            "STUDENT_SURNAME": "TestSurname",
            "STUDENT_GROUP": "TEST-1",
            "STUDENT_ID": "999",
        }, clear=False):
            self.assertEqual(student_details(), {
                "name": "TestName",
                "surname": "TestSurname",
                "group": "TEST-1",
                "student_id": "999",
            })

    def test_defaults_are_personalized(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(student_details(), {
                "name": "Danil",
                "surname": "Marchenko",
                "group": "IT2-2303",
                "student_id": "41587",
            })


if __name__ == "__main__":
    unittest.main()
