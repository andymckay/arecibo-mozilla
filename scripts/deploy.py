# sure this will get more complicated
import os

def cmd(cmd):
    os.system(cmd)

def log(msg):
    print msg

def checkout(paths):
    for path in paths:
        log('Checking out: %s' % path)
        cmd('cd %s; git pull' % path)

def restart_apache():
    log('Restarting Apache')
    cmd('/etc/init.d/apache2 restart')

checkout(['/home/andy/arecibo',
          '/home/andy/arecibo-mozilla'])
restart_apache()

