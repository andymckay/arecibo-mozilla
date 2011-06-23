# sure this will get more complicated
import os

def cmd(cmd):
    os.system(cmd)

def log(msg):
    print msg

def checkout_arecibo(path):
    log('Checking out Arecibo')
    cmd('cd %s; git pull' % path)

def checkout_arecibo_mozilla(path):
    log('Checking out Arecibo Mozilla')
    cmd('cd %s; git pull' % path)

def restart_apache():
    log('Restarting Apache')
    cmd('/etc/init.d/apache2 restart')

arecibo_path = '/home/andy/arecibo'
arecibo_mozilla_path = '%s/listener/normal/custom' % arecibo_path

checkout_arecibo(arecibo_path)
checkout_arecibo_mozilla(arecibo_mozilla_path)
# todo: run migration
restart_apache()

