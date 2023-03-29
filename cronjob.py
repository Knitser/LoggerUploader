from crontab import CronTab

cron = CronTab(user='knitser')
job = cron.new(command='python main.py')
job.minute.every(2)
cron.write()
