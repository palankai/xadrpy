from xadrpy.core.workers.daemon import DaemonContainer
from apscheduler.scheduler import Scheduler 

class SchedulerContainer( DaemonContainer ):
    
    def __init__(self, environment):
        super(Scheduler, self).__init__(environment)
        gconfig = environment.get("gconfig", {})
        options = environment.get("options", {})
        self.scheduler = Scheduler(gconfig, **options)
    
    def on_start(self):
        self.scheduler.start()
    
    def on_stop(self):
        self.scheduler.stop()
        
    def unschedule_func(self, func):
        self.scheduler.unschedule_func(func)
    
    def unschedule_job(self, job):
        self.scheduler.unschedule_job(job)
        
        
    def add_interval_job(self, func, weeks=0, days=0, hours=0, minutes=0, seconds=0, start_date=None, args=None, kwargs=None, **options):
        return self.scheduler.add_interval_job(func=func, 
                                        weeks=weeks, 
                                        days=days, 
                                        hours=hours, 
                                        minutes=minutes, 
                                        seconds=seconds, 
                                        start_date=start_date, 
                                        args=args, 
                                        kwargs=kwargs, 
                                        **options)
        
    def add_cron_job(self, func, year=None, month=None, day=None, week=None, day_of_week=None, hour=None, minute=None, second=None, start_date=None, args=None, kwargs=None, **options):
        return self.scheduler.add_cron_job(func=func, 
                                    year=year, 
                                    month=month, 
                                    day=day, 
                                    week=week, 
                                    day_of_week=day_of_week, 
                                    hour=hour, 
                                    minute=minute, 
                                    second=second, 
                                    start_date=start_date, 
                                    args=args, 
                                    kwargs=kwargs,
                                    **options)
    
    def add_date_job(self, func, date, args=None, kwargs=None, **options):
        return self.scheduler.add_date_job(func=func, 
                                    date=date, 
                                    args=args, 
                                    kwargs=kwargs,
                                    **options)
    
    def get_jobs(self):
        return self.scheduler.get_jobs()
    
    def add_job(self, trigger, func, args, kwargs, jobstore='default', **options):
        return self.scheduler.add_job(trigger=trigger, 
                                      func=func, 
                                      args=args, 
                                      kwargs=kwargs, 
                                      jobstore=jobstore,
                                      **options)
        
    def add_listener(self, callback, mask):
        self.scheduler.add_listener(callback, mask)
    
    def remove_listener(self, callback):
        self.scheduler.remove_listener(callback)
