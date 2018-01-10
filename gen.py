from __future__ import print_function
import os, shutil
import yaml
import random, string

try:
    passwords = yaml.load(open('portals_passwords.yml'))
except Exception:
    passwords = {}

def genRandomPassword():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(25))

def getPassword(portal):
    password = passwords.get(portal)
    if password is None:
        password = genRandomPassword()
    passwords[portal] = password
    return password

os.chdir('../portals')

portals = [ portal for portal in os.listdir('./') if os.path.isdir(portal) ]

print("\n=============== Building frontend ===============\n")
for portal in portals:
    print("\n##### " + portal + "\n")
    os.chdir(portal + "/frontend")
    os.system("yarn install")
    os.system("INFERNO_APP_BACKEND_URL=/k/{0}/api PUBLIC_URL='/k/{0}/' yarn build".format(portal))
    os.chdir("../../")

print("\n=============== Making MySQL init file ===============\n")
initdbfile = open('../deployconfig/portals_initdb.sql', 'w')
for portal in portals:
    print("CREATE USER IF NOT EXISTS '{}'@'%' IDENTIFIED BY '{}';".format(portal, getPassword(portal)), file=initdbfile)
    print("CREATE DATABASE IF NOT EXISTS {};".format(portal), file=initdbfile)
    print("GRANT ALL PRIVILEGES ON {0}.* TO '{0}'@'%' IDENTIFIED BY '{1}';".format(portal, getPassword(portal)), file=initdbfile)
print("FLUSH PRIVILEGES;", file=initdbfile)

print("\n=============== Making docker compose file ===============\n")
services = {}
for portal in portals:
    services[portal + '_backend'] = {
        "image": "node:8",
        "working_dir": "/home/node/app",
        "environment": [
            "NODE_ENV=production",
            "DBURI=mysql://%s:%s@portaldb/%s" % (portal, getPassword(portal), portal),
            "PUBLIC_API_URL=https://felicity.iiit.ac.in/k/%s/api" % portal,
            "PUBLIC_FRONTEND_URL=https://felicity.iiit.ac.in/k/%s" % portal,
        ],
        "volumes": [ "../portals/%s/backend:/home/node/app" % portal ],
        "command": "bash -c 'yarn install && yarn start'"
    }
    services[portal + '_frontend'] = {
        "image": "node:8",
        "working_dir": "/home/node/app",
        "environment": [ "NODE_ENV=production" ],
        "volumes": [ "../portals/%s/frontend/build:/home/node/app" % portal ],
        "command": "bash -c 'yarn global add serve && serve -s'"
    }

os.chdir('../deployconfig')

kongconf = yaml.load(open('kong.yml'))
kongconf['services'].update(services)
yaml.dump(kongconf, open('portals.yml', 'w'), default_flow_style=False)
yaml.dump(passwords, open('portals_passwords.yml', 'w'), default_flow_style=False)
