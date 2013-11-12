import os
import getpass
def ensure_django_exists():
    # look for django
    try:
        import django
    except:
        os.system('sudo apt-get install python-django')
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
    ensure_django_exists()
    ensure_database_exists()
    detrimine_starting_point()
    runserver()

if __name__ == "__main__":
    main()
