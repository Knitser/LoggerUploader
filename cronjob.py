from crontab import CronTab


with CronTab() as cron:
    job = cron.new(command='python main.py')
    job.minutes.every(1)
    cron.write( 'output.txt' )
print('cron.write() was just executed')
