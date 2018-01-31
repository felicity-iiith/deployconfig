Repo containing the docker stacks required for deployment.

This repo is kept opensource in an effort to explain how dockerized deployment works

The `dockercmds` file lists commands useful for testing individual services during development

Environment variables are stored in .env files.
The following might be neat for your bashrc:
```bash
dotenv () {
  set -a
  [ -f $1 ] && . $1
  set +a
}
```

Lines commented out in the compose files might be helpful while development

# Example run
Dev
```bash
dotenv dev.env
docker-compose -f auth.yml up
```

Prod
```bash
dotenv prod.env
docker stack deploy -c auth.yml auth
```

# Directory Structure
```
.
├── deployconfig
├── misc_portals
└── portals
    ├── portal_1
    │   ├── backend
    │   └── frontend
    └── portal_2
        ├── backend
        └── frontend
```

# Ports
- 8*** auth
- 9*** portals
- 7*** mailtrain
- 10*** h5ai
