# TheZoo
Malware hosting platform with automated analysis

## 🚀 Quick Start (Recommended)

**One-command setup with file persistence fix:**
```sh
git clone https://github.com/sh1dow3r/TheZoo --recursive
cd TheZoo
python3 main.py --setup
```

## 📋 Manual Setup

Clone the repo with its submodules:
```sh
git clone https://github.com/sh1dow3r/TheZoo --recursive
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

# Blog Post

https://layer0.xyz/posts/Automated_Approach_for_Malware_Collection_and_Analysis/
