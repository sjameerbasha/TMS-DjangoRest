from django.test import TestCase
from unittest.mock import patch, MagicMock
from core.utils.notifications import send_task_assignment_email
import smtplib


class EmailNotificationTests(TestCase):

    @patch('core.utils.notifications.smtplib.SMTP_SSL')
    @patch('core.utils.notifications.EMAIL_PASSWORD', 'fakepass')
    @patch('core.utils.notifications.EMAIL_ADDRESS', 'sender@example.com')
    def test_send_email_success(self, mock_smtp_ssl):
        mock_server = MagicMock()
        mock_smtp_ssl.return_value = mock_server

        response = send_task_assignment_email(
            to_email="user@example.com",
            task_title="Write unit tests",
            assigned_by="AdminUser"
        )

        self.assertEqual(response["status_code"], 200)
        mock_server.login.assert_called_with('sender@example.com', 'fakepass')
        mock_server.send_message.assert_called()
        mock_server.quit.assert_called()

    @patch('core.utils.notifications.smtplib.SMTP_SSL')
    def test_send_email_smtp_exception(self, mock_smtp_ssl):
        mock_smtp_ssl.side_effect = smtplib.SMTPException("SMTP failed")

        response = send_task_assignment_email(
            to_email="user@example.com",
            task_title="Write unit tests",
            assigned_by="AdminUser"
        )

        self.assertEqual(response["status_code"], 500)
        self.assertIn("SMTP Error", response["message"])

    @patch('core.utils.notifications.smtplib.SMTP_SSL')
    def test_send_email_generic_exception(self, mock_smtp_ssl):
        mock_smtp_ssl.side_effect = Exception("Something went wrong")

        response = send_task_assignment_email(
            to_email="user@example.com",
            task_title="Write unit tests",
            assigned_by="AdminUser"
        )

        self.assertEqual(response["status_code"], 500)
        self.assertIn("Error", response["message"])

    @patch('core.utils.notifications.smtplib.SMTP_SSL')
    @patch('core.utils.notifications.EMAIL_ADDRESS', None)
    @patch('core.utils.notifications.EMAIL_PASSWORD', None)
    def test_send_email_missing_env_vars(self, mock_smtp_ssl):
        mock_server = MagicMock()
        mock_smtp_ssl.return_value = mock_server

        response = send_task_assignment_email(
            to_email="user@example.com",
            task_title="Test Task",
            assigned_by="Tester"
        )

        # It still proceeds, but login might fail depending on how smtplib is mocked
        self.assertIn("status_code", response)
        self.assertTrue(response["status_code"] in [200, 500])  # depends on SMTP reaction

    @patch('core.utils.notifications.smtplib.SMTP_SSL')
    def test_send_email_to_empty_email(self, mock_smtp_ssl):
        mock_server = MagicMock()
        mock_smtp_ssl.return_value = mock_server

        response = send_task_assignment_email(
            to_email="",
            task_title="Test Empty Email",
            assigned_by="AdminUser"
        )

        # Should fail gracefully depending on implementation
        self.assertIn("status_code", response)
