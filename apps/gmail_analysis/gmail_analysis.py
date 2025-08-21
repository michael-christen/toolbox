import os.path, pickle, base64, email
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service(credentials_file: str, token_pickle: str):
    creds = None
    if os.path.exists(token_pickle):
        with open(token_pickle, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_pickle, 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def get_labels(service):
    results = service.users().labels().list(userId='me').execute()
    return results.get('labels', [])

def get_email_count(service, days: int):
    # Query for last N days
    after = (datetime.utcnow() - timedelta(days=days)).strftime("%Y/%m/%d")
    query = f"after:{after}"
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    count = len(messages)
    return count

def get_email_count(service, start, end) -> int:
    """Count emails between start and end dates."""
    query = f"after:{start.strftime('%Y/%m/%d')} before:{end.strftime('%Y/%m/%d')}"
    results = service.users().messages().list(userId='me', q=query).execute()
    count = len(results.get('messages', []))
    return count

def update_log(date, count, filename):
    row = {"date": date.strftime("%Y-%m-%d"), "count": count}
    df = pd.DataFrame([row])
    if os.path.exists(filename):
        old = pd.read_csv(filename)
        if row["date"] in old["date"].values:
            return old  # skip if already exists
        df = pd.concat([old, df])
    df.to_csv(filename, index=False)
    return df

def plot_counts(df, plot_location):
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date").plot(kind="line", y="count", marker="o", figsize=(10,5))
    plt.title("Emails Received Per Day")
    plt.ylabel("Count")
    plt.xlabel("Date")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(plot_location)

def main():
    # XXX: Argument
    credentials_file = '/home/mchristen/devel/secrets/gmail_oauth_my_gmail_project_client_secret_48644508553-b19iehdnb78h9drviqem4c8t2quo1dmm.apps.googleusercontent.com.json'
    token_pickle = '/tmp/token.pickle'
    log_name = '/tmp/email_counts.csv'
    plot_location = '/tmp/gmail_plot.png'
    service = get_gmail_service(credentials_file, token_pickle)
    # labels = get_labels(service)

    # pick a backfill start date
    start_date = datetime(2025, 5, 1)   # change as needed
    end_date = datetime.today()

    date = start_date
    while date < end_date:
        next_day = date + timedelta(days=1)
        count = get_email_count(service, date, next_day)
        df = update_log(date, count, log_name)
        print(f"Logged {date.strftime('%Y-%m-%d')}: {count}")
        date = next_day

    plot_counts(df, plot_location)

if __name__ == "__main__":
    main()
