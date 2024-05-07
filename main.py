from dotenv import load_dotenv
import os
from apscheduler.schedulers.background import BlockingScheduler
from database import *
from hot_deal import getDeal
# from n2t import n2t_exe

# load .env
load_dotenv()

#3600초 = 1시간
hotdeal_schedule_interval = os.environ.get('hotdeal_schedule_interval')


def main(debug):
    # 디비 연결
    init_db()

    hotdeal_interval = int(hotdeal_schedule_interval) * 3
    # write_interval = int(hotdeal_schedule_interval) * 24

    sched = BlockingScheduler(timezone='Asia/Seoul')
    sched.add_job(getDeal, 'interval', seconds=hotdeal_interval, id='getDeal', args=['start'])
    # sched.add_job(n2t_exe, 'interval', seconds=write_interval, id='n2t_exe', args=['start'])
    sched.start()


if __name__ == '__main__':
    debug = "0"
    main(debug)
    