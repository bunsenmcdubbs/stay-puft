from requests import request
import json
import sys
from datetime import datetime

import db

HACKALIST_API_URL = 'http://www.hackalist.org/api/1.0/%d/%02d.json'

def fetch_month(year, month):
    res = request('GET', HACKALIST_API_URL%(year, month)).content
    data = list(json.loads(res).values())[0]
    return data

def save_to_database(hackathons, conn):
    add_hackathon = "INSERT INTO hackathon (title, start_date, end_date, city, host, length, num_participants, allows_hs, cost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    fix_date = lambda d, y: datetime.strptime("{} {}".format(d, y), '%B %d %Y')
    fix_bool = lambda x: int(x == 'yes') if x is not None else None
    with conn.cursor() as cursor:
        for h in hackathons:
            data = (
                h['title'],
                fix_date(h['startDate'], h['year']),
                fix_date(h['endDate'], h['year']),
                h['city'],
                h['host'],
                h['length'] if h['length'].isdigit() else None,
                h['size'],
                fix_bool(h['highSchoolers']),
                h['cost']
                )
            try:
                cursor.execute(add_hackathon, data)
            except (UnicodeEncodeError) as e:
                print("encoding error, not latin probably, skipped!", data)
            except (Exception) as e:
                print(data)
                raise e
        conn.commit()

if __name__=="__main__":
    args = sys.argv
    months = []
    if len(args) == 3:
        months = [int(args[2])]
    else:
        months = range(1,13)
    year = int(args[1])
    for month in months:
        hackathons = fetch_month(year, month)
        conn = db.get_conn()
        save_to_database(hackathons, conn)
    
