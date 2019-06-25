import os
import sys

currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
# print(parentUrl)
sys.path.append(parentUrl)

if __name__ == '__main__':

    import time
    from functools import wraps

    from pymongo import MongoClient
    from apscheduler.schedulers.blocking import BlockingScheduler

    scheduler = BlockingScheduler()

    print("start")

    # 新增一条日志到MongoDB， timer_jobs_log
    def add_log_to_mongo_timer_jobs_log(log_data):
        host = '127.0.0.1'
        port = 27017
        conn = MongoClient(host=host, port=port)
        log_db = conn['timer_log']
        log_t = log_db['timer_jobs_log']
        log_t.save(log_data)


    # 日志装饰器
    def add_log(job_label):
        def decorate(func):
            @wraps(func)
            def _wrap(*args, **kwargs):
                try:

                    add_log_to_mongo_timer_jobs_log({"_id": int(time.time()),
                                                     "data": {
                                                         "title": func.__name__,
                                                         "content": job_label,
                                                     }, "type": "start"})

                    # 执行的任务
                    func(*args, **kwargs)

                    add_log_to_mongo_timer_jobs_log({"_id": int(time.time()),
                                                     "data": {
                                                         "title": func.__name__,
                                                         "content": job_label,
                                                     }, "type": "end"})

                except Exception as e:
                    print(e.args)

            return _wrap

        return decorate


    @add_log("test")
    def test():
        print("ceshi")


    # 添加定时任务

    scheduler.add_job(test, 'cron', hour=11, minute=45)

    # 启动任务
    scheduler.start()
