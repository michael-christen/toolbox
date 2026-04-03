import argparse
import os.path
import pickle
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt
import pandas as pd
from google.auth.transport import requests
from google_auth_oauthlib import flow
from googleapiclient import discovery

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_gmail_service(
    credentials_file: str, token_pickle: str
) -> discovery.Resource:
    creds = None
    if os.path.exists(token_pickle):
        with open(token_pickle, "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(requests.Request())
        else:
            app_flow = flow.InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES
            )
            creds = app_flow.run_local_server(port=0)
        with open(token_pickle, "wb") as token:
            pickle.dump(creds, token)
    return discovery.build("gmail", "v1", credentials=creds)


def get_email_count(
    service: discovery.Resource, start: datetime, end: datetime
) -> int:
    """Count emails between start and end dates."""
    query = (
        f"after:{start.strftime('%Y/%m/%d')} "
        f"before:{end.strftime('%Y/%m/%d')}"
    )
    count = 0
    page_token = None
    while True:
        kwargs = {"userId": "me", "q": query}
        if page_token:
            kwargs["pageToken"] = page_token
        results = (
            service.users()  # type: ignore[attr-defined]
            .messages().list(**kwargs).execute()
        )
        count += len(results.get("messages", []))
        page_token = results.get("nextPageToken")
        if not page_token:
            break
    return count


def update_log(date: datetime, count: int, filename: str) -> pd.DataFrame:
    row = {"date": date.strftime("%Y-%m-%d"), "count": count}
    df = pd.DataFrame([row])
    if os.path.exists(filename):
        old = pd.read_csv(filename)
        if row["date"] in old["date"].values:
            return old  # skip if already exists
        df = pd.concat([old, df])
    df.to_csv(filename, index=False)
    return df


def plot_counts(df: pd.DataFrame, plot_location: str) -> None:
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date").plot(
        kind="line", y="count", marker="o", figsize=(10, 5)
    )
    plt.title("Emails Received Per Day")
    plt.ylabel("Count")
    plt.xlabel("Date")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(plot_location)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze daily email counts via Gmail API."
    )
    parser.add_argument(
        "--credentials",
        required=True,
        help="Path to OAuth2 client secrets JSON file",
    )
    parser.add_argument(
        "--token",
        default="/tmp/token.pickle",
        help="Path to token pickle file (default: /tmp/token.pickle)",
    )
    parser.add_argument(
        "--log",
        default="/tmp/email_counts.csv",
        help="Path to CSV log file (default: /tmp/email_counts.csv)",
    )
    parser.add_argument(
        "--plot",
        default="/tmp/gmail_plot.png",
        help="Path to output plot image (default: /tmp/gmail_plot.png)",
    )
    parser.add_argument(
        "--start",
        default="2025-05-01",
        help=(
            "Start date for backfill in YYYY-MM-DD format"
            " (default: 2025-05-01)"
        ),
    )
    args = parser.parse_args()

    service = get_gmail_service(args.credentials, args.token)

    start_date = datetime.strptime(args.start, "%Y-%m-%d")
    end_date = datetime.today()

    date = start_date
    while date < end_date:
        next_day = date + timedelta(days=1)
        count = get_email_count(service, date, next_day)
        df = update_log(date, count, args.log)
        print(f"Logged {date.strftime('%Y-%m-%d')}: {count}")
        date = next_day

    plot_counts(df, args.plot)


if __name__ == "__main__":
    main()
