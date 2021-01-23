import datetime
import time
import subprocess
from notion.client import NotionClient
from notion.collection import NotionDate
from notion.block import TodoBlock

token_path = "C:/Users/longr/OneDrive/Документы/Tokens/notion.txt"
datebook_tracker = "https://www.notion.so/demidovviktor/Datebook-823380ba5b694821ab31b648ac047b88"
schedule_tracker = "https://www.notion.so/demidovviktor/b8737a5e998b4382b3f43f48de1ac17e?v=db0e98a6b9bb4455bdb4a03ffe30e37d"


def bold(text):
    return "**" + text + "**"


def italic(text):
    return "*" + text + "*"


def weekly_agenda(url):
    page = client.get_collection_view(url)
    current_week = datetime.datetime.today().isocalendar()[1]
    for row in page.collection.get_rows():
        row_date = str(row.Date.start).split("-")
        row_week = datetime.datetime(int(row_date[0]), int(row_date[1]), int(row_date[2])).isocalendar()[1]
        row.Week = str(row_week == current_week)


def monthly_agenda(url):
    page = client.get_collection_view(url)
    current_month = datetime.datetime.today().month
    for row in page.collection.get_rows():
        row_date = str(row.Date.start).split("-")
        row_month = int(row_date[1])
        row.Month = str(row_month == current_month)


def daily_agenda(destination, source):
    destination_page = client.get_block(destination)
    source_page = client.get_collection_view(source)
    current_day = datetime.datetime.today().day
    for row in source_page.collection.get_rows():
        row_date = str(row.Date.start).split("-")
        row_date = str(row_date).replace("'", "")
        row_date = str(row_date).replace("]", "")
        row_date = str(row_date).replace("[", "")
        row_date = str(row_date).replace(",", "")
        row_date = str(row_date).split(" ")
        row_day = int(row_date[2])
        if row_day == current_day:
            child = destination_page.children.add_new(TodoBlock, title=str(row.Name + " [" + bold(str(row.Tags[0])) + "]"))



if __name__ == '__main__':
    file = open(token_path, encoding="utf-8")
    token = file.readline()
    client = NotionClient(token_v2=token)
    daily_agenda(datebook_tracker, schedule_tracker)
    while True:
        weekly_agenda(schedule_tracker)
        monthly_agenda(schedule_tracker)
        time.sleep(10)