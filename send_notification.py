"""
Script to send email after test execution in CI/CD pipeline.
"""

from datetime import datetime
import threading
import csv
import smtplib
import ssl
from email.message import EmailMessage
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--username', type=str, required=True)
parser.add_argument('--password', type=str, required=True)
parser.add_argument('--receivers', type=str, nargs='+')
parser.add_argument('--env', type=str, required=True)
parser.add_argument('--run_number', type=str, required=True)
parser.add_argument('--event_name', type=str, required=True)
parser.add_argument('--workflow', type=str, required=True)
parser.add_argument('--actor', type=str, required=True)
args = parser.parse_args()

# Define email sender and receivers.
EMAIL_SENDER = args.username
EMAIL_PASSWORD = args.password
EMAIL_RECEIVERS = args.receivers

# Email subject and body templates.
SUBJECT = 'Disney Test Execution Report - {env} Environment - API Regression - {time}'
BODY = """
Test report - https://rustam-z.github.io/disney-test-api-taf/{run_number}. 
Triggered by {event_name} in {workflow}. 
Author: {actor}.
Metrics:
{test_metrics}
"""


def get_metrics() -> str:
    """
    Read metrics data from allure report and transforms the data.
    """
    file_path = '.output/allure-history/data/behaviors.csv'
    data = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data.append(row)

    passed = 0
    failed = 0
    for metric in zip(*data):
        if metric[0] == 'PASSED':
            passed += int(metric[1])
        elif metric[0] in ['FAILED', 'BROKEN']:
            failed += int(metric[1])

    return f'Failed tests: {failed} \n' \
           f'Passed tests: {passed}'


def send_email(email_receiver):
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    test_metrics = get_metrics()

    subject = SUBJECT.format(time=time, env=args.env)
    body = BODY.format(
        run_number=args.run_number,
        event_name=args.event_name,
        workflow=args.workflow,
        actor=args.actor,
        test_metrics=test_metrics
    )

    email_message = EmailMessage()
    email_message['From'] = EMAIL_SENDER
    email_message['Subject'] = subject
    email_message['To'] = email_receiver
    email_message.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email.
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_SENDER, email_receiver, email_message.as_string())
        print(f"'{email_receiver}' received the test report mail.")


def main():
    threads = []
    for email_receiver in EMAIL_RECEIVERS:
        thread = threading.Thread(target=send_email, args=(email_receiver,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
