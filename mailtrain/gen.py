import os
from string import Template

password = os.environ.get('MAILTRAIN_MYSQL_PASSWORD')
template = Template(open('production.toml.tmpl').read())
out = template.substitute({ 'password': password })
print(out, open('production.toml.tmpl').read())
open('production.toml', 'w').write(out)
