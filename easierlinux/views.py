from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils import simplejson
import json
import os
import crypt
import urllib
import urllib2
import re
from models import Status

default_hostapd_conf = """interface=wlan0
driver=rtl871xdrv
ssid=SetupRaspberryPi
channel=1"""

def get_status(request=None):
    status = Status.objects.all()
    if status:
        return status[0]
    else:
        status = Status(step=1, running_status='normal')
        status.save()
    return status

def set_status(request=None, step=0, running_status=''):
    status = Status.objects.all()
    if status:
        status = status[0]
        if step:
            status.step = step
        if running_status:
            status.running_status = running_status
        status.save()
    else:
        status = Status(step=step, running_status=running_status)
        status.save()
    return HttpResponseRedirect('/')
    

def reset_hostapd_conf_to_default(request=None):
    os.system('echo "%s" | sudo tee /etc/hostapd/hostapd.conf' % (default_hostapd_conf))
    #os.system('sleep 5; sudo service hostapd restart &')
    return

def get_users(request=None):
    users = os.popen("sudo getent shadow | egrep '^[^:]*:[*!]:' -v | cut -f1 -d:").read()
    users = users.split('\n')
    try:
        users.remove('pi')
    except:
        pass
    return users

def delete_users(request=None):
    users = os.popen("sudo getent shadow | egrep '^[^:]*:[*!]:' -v | cut -f1 -d:").read()
    users = users.split('\n')
    try:
        users.remove('pi')
    except:
        pass
    for user in users:
        os.system('sudo userdel -r %s' % user) 
    return 

def reset_to_factory_settings_command(request=None):
    context = {'running_status': 'reset to factory settings'}
    return render_to_response('home.html', context)

def reset_to_factory_settings(request=None):
    delete_users()
    set_status(None, 1) 
    reset_hostapd_conf_to_default()
    change_hostname(None, 'RaspberryPi')
    reboot()
    context = {'step': 'reboot'}
    return render_to_response('home.html', context)

def reboot(request=None):
    os.system('sudo shutdown -r now &')
    context = {'step': 'reboot'}
    return render_to_response('home.html', context)

def create_secure_access_point(request=None, ssid=None, passphrase=None):
    hostapd_conf = """interface=wlan0
driver=rtl871xdrv
ssid=%s
hw_mode=g
channel=1
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=%s
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP""" % (ssid, passphrase)
    os.system('echo "%s" | sudo tee /etc/hostapd/hostapd.conf' % (hostapd_conf))
    #os.system('sudo service hostapd restart &')
    return

def get_internet_status(request=None):
    answer = 'disconected'
    try:
        # this code is from http://stackoverflow.com/questions/3764291/checking-network-connection
        # Warning: that IP address is for Google and could change at any time
        response=urllib2.urlopen('http://74.125.228.100',timeout=1)
        answer = 'connected'
    except urllib2.URLError as err: pass
    if request:
        return HttpResponse(answer)
    else:
        return answer

def change_hostname(request=None, hostname=None):
    f = open('/etc/hosts', 'r')
    etc_hosts = f.read()
    f.close()
    m = re.search('127\.0\.1\.1\s*[\w\d]+', etc_hosts)
    if m:
        etc_hosts = etc_hosts.replace(m.group(), '127.0.1.1       %s' % hostname)
        os.system('echo "%s" | sudo tee /etc/hosts' % (etc_hosts)) 
    else:
        os.system('echo "127.0.1.1       %s" | sudo tee -a /etc/hosts' % (hostname)) 
    
    os.system('echo "%s" | sudo tee /etc/hostname' % (hostname))
    os.system('sudo /etc/init.d/hostname.sh &')
    return
   

def get_external_ip_address():
    url = "http://icanhazip.com"
    request = urllib.urlopen(url).read()
 
    return re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", request)[0]

def step_2(request):
    if not request.POST:
        return HttpResponse('error')
    username = request.POST['username']
    password = request.POST['password']
    encPass = crypt.crypt(password,"22")
    create_user_command = "sudo useradd -p "+encPass+ " -s "+ "/bin/bash "+ "-d "+ "/home/" + username+ " -m "+ " -c \""+ username+"\" " + username   
    output = os.popen(create_user_command).read()
    os.system('echo "%s ALL=(ALL) NOPASSWD: ALL" | sudo tee -a /etc/sudoers' % (username))
        
    create_secure_access_point(None, username.capitalize()+'PiAdmin', password)
    change_hostname(None, username.capitalize() + 'Pi')
    reboot()
    return HttpResponse('')

def go_to_step(request, step):
    set_status(None, 4, 'normal')
    return HttpResponseRedirect('/')

def boot_up_gui(request=None):
    os.system('update-rc.d lightdm enable 2')
    os.system('sed /etc/lightdm/lightdm.conf -i -e "s/^#autologin-user=.*/autologin-user=%s/"' % (user))
    return

def overclock(request=None):
    return

def keyboard(request=None):
    return

def timezone(request=None):
    return 

def home(request):
    status = get_status()
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if not (len(password) >= 8 and len(password) <= 16 and password == confirm_password):
            return HttpResponse('bad password') 
        
        context = {'step': 2, 'ssid': username.capitalize()+'PiAdmin', 'passphrase': password, 'username': username, 'password': password}
        set_status(None, 3, 'normal')
    else:
        context = {'step': status.step}
    context['request'] = request
    try:
        context['ifconfigoutput'] = os.popen('ifconfig').read()
        context['eth0_ip_address'] = os.popen("ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'").read()
        context['is_internet_on'] = get_internet_status()
        context['external_ip_address'] = get_external_ip_address()
        users = os.popen("sudo getent shadow | egrep '^[^:]*:[*!]:' -v | cut -f1 -d:").read()
        users = users.split('\n')
        context['users'] = users
    except:
        pass
    return render_to_response("home.html", context)
