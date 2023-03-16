from flask_apscheduler import APScheduler
class SchedulerConfig(object):
    SCHEDULER_API_ENABLED = True
    scheduler = APScheduler()
scheduler=SchedulerConfig.scheduler
"""
@scheduler.task('interval', id='do_job_1', seconds=30, misfire_grace_time=900)
def data_import_from_file_schedule():
    print("excute")
"""
@scheduler.task('cron', id='import_data_from_file_schedule', day='*', hour=21, minute =28 ,misfire_grace_time=900)
def importDataFromFileScheduler():
    from Services.ImportDataFromFileServices import ImportDataFromFileService
    import_data_from_file=ImportDataFromFileService()
    import_data_from_file.start()

from Services.ExtractDataServices import ExtractDataServices
@scheduler.task('cron', id='extract_data_scheduler', day='*', hour=22, minute=28 ,misfire_grace_time=900)
def extractDataScheduler():
    #from Services.extract_data import ExtractData
    extract_data=ExtractDataServices()
    extract_data.start()


@scheduler.task('cron', id='testt', day='*', hour=20, minute=57 ,misfire_grace_time=900)
def extract_data_schedulertest():
    print("Test schedule")