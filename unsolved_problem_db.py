import json
from time import sleep
import requests
import pymysql
import sqlite3
from unsolved_db_setting import db_setting


def get_problem_by_level(level):
    """
    정보 조회 - level을 입력하면 백준 사이트에서 해당 level에 해당하는 문제들을 반환해줌
    :param level:
    :return: 해당 level의 문제들
    """
    url = f"https://solved.ac/api/v3/search/problem?query=tier%3A{level}"
    r_level_problem = requests.get(url)
    if r_level_problem.status_code == requests.codes.ok:
        level_problem = json.loads(r_level_problem.content.decode('utf-8'))
        pages = (level_problem.get("count") - 1) // 100 + 1
    else:
        print("난이도별  문제 요청 실패")

    problems = []
    for page in range(pages):
        page_url = f"{url}&page={page + 1}"
        print(page_url)
        r_level_problem = requests.get(page_url)
        if r_level_problem.status_code == requests.codes.ok:
            level_problem = json.loads(r_level_problem.content.decode('utf-8'))
            items = level_problem.get("items")
            for item in items:
                problems.append(item)
        else:
            print("난이도별  문제 요청 실패")
    return problems

def init_problem():
    """
    정보 조회 - 레벨별로 문제를 호출하여 db에 삽입
    """
    db = pymysql.connect(
        user='root',
        passwd='990312aa',
        host='localhost',
        db='unsolved',
    )
    cur = db.cursor()

    for level in range(30):
        level_problems = get_problem_by_level(level + 1)
        problems = []
        for level_problem in level_problems:
            problem = [level_problem.get("problemId"), level_problem.get("titleKo"), level_problem.get("level")]
            problems.append(problem)
        insert_sql = "INSERT IGNORE INTO problem(boj_id, title, tier) VALUES (%s, %s ,%s);"
        cur.executemany(insert_sql, problems)
        db.commit()
    cur.close()
    db.close()


# db_setting(group_id)
# print(get_unsolved_by_group(group_id))

db_setting()
init_problem()
