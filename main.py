from dotenv import load_dotenv
import os
from apscheduler.schedulers.background import BlockingScheduler
from database import *
from hot_deal import getDeal
from n2t import n2t_exe

# load .env
load_dotenv()

mySecret = os.environ.get('MySecret')
#3600초 = 1시간
hotdeal_schedule_interval = os.environ.get('hotdeal_schedule_interval')


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}', mySecret)  # Press Ctrl+Shift+B to toggle the breakpoint.


def job(data):
    print('data : ' + data)


def main(debug):
    # 디비 연결
    init_db()

    hotdeal_interval = int(hotdeal_schedule_interval) * 3
    write_interval = int(hotdeal_schedule_interval) * 24

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
        n2t_exe('start')
    elif debug == 'operate':
        sched = BlockingScheduler(timezone='Asia/Seoul')
        sched.add_job(getDeal, 'interval', seconds=hotdeal_interval, id='getDeal', args=['start'])
        sched.add_job(n2t_exe, 'interval', seconds=write_interval, id='n2t_exe', args=['start'])
        sched.start()


if __name__ == '__main__':
    # print_hi('PyCharm')
    debug = "0"
    main(debug)
    