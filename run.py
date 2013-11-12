import os
import getpass
import subprocess
import sys

def ensure_sudo_doesnt_require_password():
    username = getpass.getuser()
    pattern = "%s ALL=(ALL) NOPASSWD: ALL" % username
    sudoers = os.popen('sudo cat /etc/sudoers').read()
    if not pattern in sudoers: 
        os.system('echo "%s ALL=(ALL) NOPASSWD: ALL" | sudo tee -a /etc/sudoers' % (username))

def ensure_django_exists():
    # look for django
    try:
        import django
    except:
        #os.system('sudo apt-get install python-django')
        os.system('sudo apt-get install python-pip python-dev build-essential')
        os.system('sudo pip install django')
        os.system('python run.py')
        import sys
        sys.exit()

def ensure_database_exists():

    # check for database
    database_exists = os.path.exists('dev.db')
    if not database_exists:
        os.system('python manage.py syncdb')

def runserver():
    os.system('python manage.py runserver 0.0.0.0:8000')

def detrimine_starting_point():
    starting_point = ''
    if getpass.getuser() == 'root':
        starting_point = 'create primary user account'
    else:
        pass
    print 'Starting point: %s' % (starting_point)

def main():
    ensure_sudo_doesnt_require_password()
    ensure_django_exists()
    ensure_database_exists()
    detrimine_starting_point()
    runserver()

if __name__ == "__main__":
    main()
