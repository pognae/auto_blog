from dotenv import load_dotenv
import os
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from database import *
from hot_deal import getDeal



# load .env
load_dotenv()

mySecret = os.environ.get('MySecret')



# deamon = True 속성을 주어 메인 프로세스가 종료되면 같이 종료되도록 함으로써
# background에서 계속 돌아가는걸 방지하도록 하자
# sched = BackgroundScheduler(daemon=True)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}', mySecret)  # Press Ctrl+Shift+B to toggle the breakpoint.


def job(data):
    print('data : ' + data)


def main():
    # 디비 연결
    init_db()

    # 명시적이므로 method를 사용하도록 함.
    sched = BlockingScheduler(timezone='Asia/Seoul')
    # sched.add_job(job, 'interval', seconds=3, id='test', args=['hello?'])
    sched.add_job(getDeal, 'interval', seconds=3600, id='getDeal', args=['start'])
    sched.start()

    # getDeal('start')



if __name__ == '__main__':
    # print_hi('PyCharm')
    main()

