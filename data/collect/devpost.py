from collections import defaultdict

from scraper import get_submission_url, get_project_links, get_contributors
import db

# grab all the info from devpost! CURRENTLY TESTING ONLY
# select rows from the database and page scrape
# currently returns a histogram of # contributors per project
def get_num_contrib_hist(conn, verbose=False, silent=True):
    query = "SELECT title, start_date, end_date FROM hackathon LIMIT 10"
    with conn.cursor() as cursor:
        cursor.execute(query)
        hist = defaultdict(int)
        for x in range(0, cursor.rowcount):
            row = cursor.fetchone()
            if verbose and not silent:
                print(row['title'], end=' ', flush=True)
            elif not silent:
                print('.', end=' ', flush=True)
            submission_url = get_submission_url(row['title'], row['start_date'], row['end_date'])
            if verbose and not silent:
                print(submission_url)
            elif not silent:
                pass
            if submission_url is not None:
                project_links = get_project_links(submission_url)

                for project_link in project_links:
                    num_contribs = len(get_contributors(project_link))
                    hist[num_contribs] += 1
        if not verbose and not silent:
            print()
        return hist

if __name__=='__main__':
    print(get_num_contrib_hist(db.get_conn(), silent=False))
