import os, sys, time, getpass
from fabric.api import *
from fabric.colors import red, green, blue, cyan, magenta, white, yellow
from fabric.api import put, run, settings, sudo
from fabric.operations import prompt
from fabric.contrib import django

env.VENDOR_PATH					= "/home/ubuntu/code"
env.BUILD_FOLDER				= "/home/ubuntu/build"
env.PROJECT_PATH				= os.path.dirname(os.path.abspath(__file__))
env.MAIN_PROJECT_PATH			= "/home/ubuntu/{{ cookiecutter.project_name }}/"
env.BRANCH_NAME					= 'master'
env.user						= 'ubuntu'
env.key_filename				= '/Users/%s/.ssh/id_rsa' % getpass.getuser()

env.roledefs = {
	'master' : ['1.1.1.1'],
	'staging' : ['1.1.1.1'],
}

is_staging = None
if 'staging' in env.roles:
	is_staging = True
	env.BRANCH_NAME	= 'staging'
elif 'data' in env.roles:
	env.BRANCH_NAME	= 'master'

def install_async_workers():
	""" if you want to run gunicorn with async works, you need this libraries"""
	sudo('apt-get install libevent-dev')
	sudo('pip install -U greenlet')
	sudo('pip install -U gevent')
	sudo('pip install -U gunicorn')

def start_celery_queues(restart_nginx=False):
	""" Start gunicorn app servers """
	put('config/supervisor_gunicorn.conf', '/etc/supervisor/conf.d/gunicorn.conf', use_sudo=True)
	put('config/supervisor_processing.conf', '/etc/supervisor/conf.d/processing.conf', use_sudo=True)
	if restart_nginx:
		sudo('supervisorctl update')
		sudo('supervisorctl reload')	
		sudo("/etc/init.d/nginx restart")


def deploy(has_migration=False):
	""" Full restart needed if migration is present"""
	with cd(env.MAIN_PROJECT_PATH):
		sudo("pip install -r requirements/common.txt")
		run('git pull origin %s' % env.BRANCH_NAME )
		run('./manage.py migrate')
		compress_assets()
		transfer_assets()	
			
		if is_staging:
			settings_file = 'rewire/local_settings.staging'
		else:
			settings_file = 'rewire/local_settings.prod'
		run("cp %s rewire/local_settings.py" % settings_file )
		if has_migration:
			sudo("supervisorctl reload")
		else:
			with settings(warn_only=True):
				print(cyan("restarting gunicorn using PKILL"))
				sudo("pkill -9 -f gunicorn")
		cleanup_assets()

def run_command(command):
	""" run a command on the server using sudo """
	sudo("%s" % command)

def setup_installs():
	""" installs all apt-get packages required for rewire repo to run """
	packages = [
		'build-essential',
		'gcc',
		'libreadline-dev',
		'libpcre3-dev',
		'libssl-dev',
		'sysstat',
		'iotop',
		'git',
		'python-dev',
		'locate',
		'python-software-properties',
		'software-properties-common',
		'libpcre3-dev',
		'libncurses5-dev',
		'libdbd-pg-perl',
		'libssl-dev',
		'make',
		'libyaml-0-2',
		'python-setuptools',
		'python-yaml',
		'curl',
		'libjpeg8',
		'libjpeg62-dev',
		'libfreetype6',
		'libfreetype6-dev',
		'python-imaging',
		'supervisor',
	]
	sudo('apt-get -y update')
	sudo('DEBIAN_FRONTEND=noninteractive apt-get -y --force-yes upgrade')
	sudo('DEBIAN_FRONTEND=noninteractive apt-get -y --force-yes install %s' % ' '.join(packages))
		
	with settings(warn_only=True):
		sudo('mkdir -p %s' % env.VENDOR_PATH)
		sudo('chown %s.%s %s' % (env.user, env.user, env.VENDOR_PATH))

	
def setup_nginx():
	""" installs latest NGINX from source """	
	NGINX_VERSION = '1.7.3'
	with cd(env.MAIN_PROJECT_PATH), settings(warn_only=True):
		sudo("groupadd nginx")
		sudo("useradd -g nginx -d /var/www/htdocs -s /bin/false nginx")
		run('wget http://nginx.org/download/nginx-%s.tar.gz' % NGINX_VERSION)
		run('tar -xzf nginx-%s.tar.gz' % NGINX_VERSION)
		run('rm nginx-%s.tar.gz' % NGINX_VERSION)
		with cd('nginx-%s' % NGINX_VERSION):
			run('./configure --with-http_ssl_module --with-http_stub_status_module --with-http_gzip_static_module')
			run('make')
			sudo('make install')
			
def soft_deploy(has_migration=False):
	""" If you are running a migration, you need a full restart """
	with cd(env.MAIN_PROJECT_PATH):
		run('git pull')
		sudo("pip install -r requirements/common.txt")
		run('./manage.py migrate')
		if is_staging:
			settings_file = 'rewire/local_settings.staging'
		else:
			settings_file = 'rewire/local_settings.prod'
		run("cp %s rewire/local_settings.py" % settings_file )
		if has_migration:
			sudo("supervisorctl reload")
		else:
			with settings(warn_only=True):
				print(cyan("restarting gunicorn using PKILL"))
				sudo("pkill -9 -f gunicorn")

def config_nginx(restart=False):
	""" copy over nginx configuration """
	put("config/nginx.conf", "/usr/local/nginx/conf/nginx.conf", use_sudo=True)
	sudo("mkdir -p /usr/local/nginx/config/sites-enabled")
	sudo("mkdir -p /var/logs/nginx")
	put("config/nginx.rewire.conf", "/usr/local/nginx/config/sites-enabled/rewire.conf", use_sudo=True)
	put("config/nginx-init", "/etc/init.d/nginx", use_sudo=True)
	sudo("chmod 0755 /etc/init.d/nginx")
	sudo("/usr/sbin/update-rc.d -f nginx defaults")
	if restart:
		sudo("/etc/init.d/nginx restart")
	
	
def compress_assets(bundle=False):
	""" Use jammit to compress asset """
	with cd(env.MAIN_PROJECT_PATH):
		run('jammit -c assets.yml --base-url http://{{ cookiecutter.project_name }} --output static')
		print(cyan("building shit on server"))

def transfer_assets():
	""" Transfer compressed assets to EC2 """
	# put('static.tgz', '%s' % env.MAIN_PROJECT_PATH)
	# import time
	# time.sleep(2)
	# with cd(env.MAIN_PROJECT_PATH):
	# 	run('tar xvf static.tgz')
	# 	run('rm -f static.tgz')

def cleanup_assets(version='9.2'):
	""" Delete compress (static.tgz) files locally. """
	#local('rm -f static.tgz')

def setup_postgres(add_to_list=False):
	""" install postgres, from source ... bitch """
	if add_to_list:
		sudo("mkdir -p /etc/apt/sources.list.d/")
		sudo('echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" >> /etc/apt/sources.list.d/pgdg.list')
		sudo('wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -')
		sudo('sudo apt-get update')
	
	shmmax = 2300047872
	sudo('wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | sudo apt-key add -')
	sudo('apt-get update')
	sudo('apt-get -y install postgresql-%s postgresql-client-%s postgresql-contrib-%s libpq-dev' %(version,version,version))
	put('config/postgresql.conf', '/etc/postgresql/%s/main/postgresql.conf' % version, use_sudo=True)
	sudo('echo "%s" > /proc/sys/kernel/shmmax' % shmmax)
	sudo('echo "\nkernel.shmmax = %s" > /etc/sysctl.conf' % shmmax)
	sudo('sysctl -p')
	sudo('/etc/init.d/postgresql stop')
	sudo('/etc/init.d/postgresql start')
	