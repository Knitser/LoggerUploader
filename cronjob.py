from crontab import CronTab

cron = CronTab(user='root')
job = cron.new(command='python main.py')
job.minute.every(2)
cron.write()
