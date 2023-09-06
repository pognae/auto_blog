from dotenv import load_dotenv
import os
from apscheduler.schedulers.background import BlockingScheduler
from database import *
from hot_deal import getDeal
from n2t import n2t_exe

# load .env
load_dotenv()

mySecret = os.environ.get('MySecret')
hotdeal_schedule_interval = os.environ.get('hotdeal_schedule_interval')



# deamon = True 속성을 주어 메인 프로세스가 종료되면 같이 종료되도록 함으로써
# background에서 계속 돌아가는걸 방지하도록 하자
# sched = BackgroundScheduler(daemon=True)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}', mySecret)  # Press Ctrl+Shift+B to toggle the breakpoint.


def job(data):
    print('data : ' + data)


def main(debug):
    # 디비 연결
    init_db()

    hotdeal_interval = hotdeal_schedule_interval * 3

    # 명시적이므로 method를 사용하도록 함.
    if debug == "0":
        sched = BlockingScheduler(timezone='Asia/Seoul')
        # sched.add_job(job, 'interval', seconds=3, id='test', args=['hello?'])
        sched.add_job(getDeal, 'interval', seconds=hotdeal_interval, id='getDeal', args=['start'])
        sched.start()
    elif debug == "1":
        getDeal('start')
    elif debug == "2":
        # print("N2T Start")
        n2t_exe()


if __name__ == '__main__':
    # print_hi('PyCharm')
    debug = "2"
    main(debug)

