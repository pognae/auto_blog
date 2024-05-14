from dotenv import load_dotenv
import os
# from hot_deal import getDeal
# from n2t import n2t_exe
from blog.naver.login import login


# load .env
load_dotenv()

#3600초 = 1시간
hotdeal_schedule_interval = os.environ.get('hotdeal_schedule_interval')


def main():
    login()

'''
    # 디비 연결
    init_db()

    # getDeal('init') #티스토리 api 종료로 에러 발생

    # hotdeal_interval = int(hotdeal_schedule_interval) * 1 #티스토리 api 종료로 에러 발생
    write_interval = int(hotdeal_schedule_interval) * 24

    sched = BlockingScheduler(timezone='Asia/Seoul')
    # sched.add_job(getDeal, 'interval', seconds=hotdeal_interval, id='getDeal', args=['start']) #티스토리 api 종료로 에러 발생
    sched.add_job(n2t_exe, 'interval', seconds=write_interval, id='n2t_exe', args=['start'])
    sched.start()
'''

if __name__ == '__main__':
    main()


