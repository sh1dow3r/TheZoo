# TheZoo
Malware hosting platform with automated analysis

## 🚀 Quick Start (Recommended)

**One-command setup with file persistence fix:**
```sh
git clone https://github.com/sh1dow3r/TheZoo
cd TheZoo
python3 main.py --setup
```

## 📋 Manual Setup

Clone the repo (submodules are auto-initialized by the setup script):
```sh
git clone https://github.com/sh1dow3r/TheZoo
cd TheZoo
```

Generate configuration only:
```sh
python3 main.py
```

Review the project configuration at `./mwdb-vars.env` file.

Start all services manually:
```sh
docker compose up --build -d
```

## 💡 Usage Options

```sh
python3 main.py                 # Generate configuration only
python3 main.py --setup         # Complete automated setup (recommended)
python3 main.py --help          # Show help
```

## 🛡️ File Persistence Fix

**Important**: This version includes a fix for file deletion after Karton processing.

- **MWDB files** are stored in `mwdb-files` bucket
- **Karton tasks** use `karton` bucket  
- **Files persist** after analysis completion
- **Template-based configuration** ensures consistent setup

### Configuration Templates

The platform uses configuration templates to ensure consistent setup:
- `config-templates/karton.ini.template` - Karton configuration template
- `config-templates/mwdb.ini.template` - MWDB configuration template

These templates are automatically processed during setup to generate the actual configuration files with proper credentials and bucket separation.

See [`BUCKET_SEPARATION_FIX.md`](BUCKET_SEPARATION_FIX.md) for technical details.

## 🌐 Access Points

- **MWDB Web Interface**: http://localhost:8080
- **Karton Dashboard**: http://localhost:8000
- **MinIO Console**: http://localhost:9001

**Default credentials**: `admin` / (see generated password in `mwdb-vars.env`)

### 🧪 Smoke test

After setup, a smoke test uploads a small sample automatically. You can also upload via MWDB UI or:
```sh
python3 - <<'PY'
import requests, os
s=requests.Session()
env=dict(l.split('=',1) for l in open('mwdb-vars.env') if '=' in l and not l.startswith('#'))
t=s.post('http://localhost:8080/api/auth/login',json={'login':'admin','password':env['MWDB_ADMIN_PASSWORD']}).json()['token']
H={'Authorization':'Bearer '+t}
os.makedirs('TheZoo_volume/samples',exist_ok=True)
open('TheZoo_volume/samples/test.bin','wb').write(os.urandom(2048))
with open('TheZoo_volume/samples/test.bin','rb') as f:
    print(s.post('http://localhost:8080/api/file',headers=H,files={'file':('test.bin',f,'application/octet-stream')}).text)
PY
```

# Blog Post

https://layer0.xyz/posts/Automated_Approach_for_Malware_Collection_and_Analysis/
