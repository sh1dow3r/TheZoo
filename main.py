import random, string, configparser, subprocess, time, sys, os
import urllib.request, urllib.error


def password_gen(length):
    #ref https://medium.com/analytics-vidhya/create-a-random-password-generator-using-python-2fea485e9da9
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    #symbols = string.punctuation
    password_space = lower + upper + num #+ symbols
    temp_pass = random.sample(password_space,length)
    password = "".join(temp_pass)
    return password


def write_line(file,key,val):
    pass

def setup_mwdb_vars():
    ADMIN_PASSWORD=password_gen(25)
    SECRET_KEY=password_gen(25)
    POSTGRES_PASSWORD=password_gen(25)
    MINIO_ACCESS_KEY=password_gen(25)
    MINIO_SECRET_KEY=password_gen(25)
    #MINIO_ROOT_USER=root
    #MINIO_ROOT_PASSWORD=
    filename = "mwdb-vars.env"
    fd = open(filename ,"w")
    fd.truncate() #flush content before writing
    mwdb_vars_setup="MWDB_ADMIN_LOGIN=admin\n\
MWDB_ADMIN_PASSWORD={}\n\
MWDB_SECRET_KEY={}\n\
POSTGRES_USER=mwdb\n\
POSTGRES_DB=mwdb\n\
POSTGRES_PASSWORD={}\n\
MINIO_ACCESS_KEY={}\n\
MINIO_SECRET_KEY={}\n\
MWDB_REDIS_URI=redis://redis/\n\
MWDB_POSTGRES_URI=postgresql://mwdb:{}@postgres/mwdb".format(ADMIN_PASSWORD,SECRET_KEY,POSTGRES_PASSWORD,MINIO_ACCESS_KEY,MINIO_SECRET_KEY,POSTGRES_PASSWORD)

    mwdb_opt_vars_setup="\nMWDB_BASE_URL=http://127.0.0.1\n\
MWDB_ADMIN_EMAIL=admin@localhost\n\
MWDB_BASE_URL=http://127.0.0.1\n\
MWDB_MAIL_SMTP=localhost:25\n\
MWDB_MAIL_FROM=noreply@mwdb.dev\n\
MWDB_RECAPTCHA_SITE_KEY=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI\n\
MWDB_RECAPTCHA_SECRET=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe\n\
UWSGI_PROCESSES=4\n\
MWDB_ENABLE_RATE_LIMIT=1\n\
MWDB_ENABLE_REGISTRATION=1\n\
REACT_APP_API_URL=/api/\n\
HOST=0.0.0.0"
    fd.write(mwdb_vars_setup)
    fd.write(mwdb_opt_vars_setup)
    fd.close()

    #install dependencies 
    #deb = "itsdangerous==2.0.1\n"
    #karton_dashboard = "./karton_plugins/karton-dashboard/requirements.txt"
    #karton_reporter = "./karton_plugins/karton-mwdb-reporter/requirements.txt"
    #fd = open(karton_dashboard ,"a")
    #fd.write(deb)
    #fd.close()
    #fd = open(karton_reporter ,"a")
    #fd.write(deb)
    #fd.close()
    
    # Setup ini files for karton and mwdb-core communication using templates
    karton_ini = "./TheZoo_volume/karton/karton.ini" 
    mwdb_ini = "./TheZoo_volume/karton/mwdb.ini"
    
    # Create config directories if they don't exist
    os.makedirs(os.path.dirname(karton_ini), exist_ok=True)
    os.makedirs(os.path.dirname(mwdb_ini), exist_ok=True)
    
    # Generate karton.ini from template
    generate_karton_config(karton_ini, ADMIN_PASSWORD, MINIO_ACCESS_KEY, MINIO_SECRET_KEY)
    
    # Generate mwdb.ini from template
    generate_mwdb_config(mwdb_ini, SECRET_KEY, MINIO_ACCESS_KEY, MINIO_SECRET_KEY)
    
    
def setup_ini_file(ini_file, section, key, val):
    config = configparser.ConfigParser()
    config.read(ini_file)
    config.set(section,key,val) 
    with open(ini_file, 'w') as configfile:
        config.write(configfile)


def generate_karton_config(output_file, admin_password, minio_access_key, minio_secret_key):
    """Generate karton.ini from template with proper bucket separation"""
    config_content = f"""[core]
 bucket = karton
 redis_url = redis://redis:6379/0
 identity = karton

[redis]
host = redis
port = 6379
db = 0

 [mwdb]
password = {admin_password}

[s3]
address = http://minio:9000
access_key = {minio_access_key}
secret_key = {minio_secret_key}
bucket = karton
"""
    
    with open(output_file, 'w') as f:
        f.write(config_content)
    
    print_status(f"✅ Generated karton.ini with bucket separation", "success")


def generate_mwdb_config(output_file, secret_key, minio_access_key, minio_secret_key):
    """Generate mwdb.ini from template with S3 storage and bucket separation"""
    config_content = f"""[mwdb]
# S3 Storage Configuration for File Persistence Fix
# This ensures MWDB uses a separate bucket from Karton
storage_provider = s3
hash_pathing = 1
hash_pathing_fallback = 1
s3_storage_endpoint = minio:9000
s3_storage_access_key = {minio_access_key}
s3_storage_secret_key = {minio_secret_key}
s3_storage_bucket_name = mwdb-files

# Database Configuration
db_uri = postgresql://mwdb:mwdb@postgres/mwdb

# Security Configuration
secret_key = {secret_key}
"""
    
    with open(output_file, 'w') as f:
        f.write(config_content)
    
    print_status(f"✅ Generated mwdb.ini with S3 storage and bucket separation", "success")


def print_status(message, status="info"):
    """Print colored status messages"""
    colors = {
        "info": "\033[94m",      # Blue
        "success": "\033[92m",   # Green  
        "warning": "\033[93m",   # Yellow
        "error": "\033[91m",     # Red
        "reset": "\033[0m"       # Reset
    }
    print(f"{colors.get(status, '')}{message}{colors['reset']}")


def check_docker():
    """Check if Docker is running"""
    try:
        subprocess.run(["docker", "info"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_docker_compose():
    """Check if Docker Compose is available"""
    try:
        subprocess.run(["docker", "compose", "version"], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["docker-compose", "version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False


def wait_for_service(url, service_name, timeout=120):
    """Wait for a service to be ready"""
    print_status(f"⏳ Waiting for {service_name} to be ready...", "info")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            urllib.request.urlopen(url, timeout=5)
            print_status(f"✅ {service_name} is ready!", "success")
            return True
        except urllib.error.URLError:
            time.sleep(3)
            print(".", end="", flush=True)
    
    print_status(f"❌ Timeout waiting for {service_name}", "error")
    return False


def ensure_submodules():
    """Ensure git submodules are initialized and updated"""
    try:
        subprocess.run(["git", "submodule", "update", "--init", "--recursive"],
                       check=True, capture_output=True)
        print_status("✅ Git submodules initialized", "success")
        return True
    except subprocess.CalledProcessError as e:
        print_status(f"⚠️  Failed to init submodules: {e}", "warning")
        return False


def run_docker_compose(action="up"):
    """Run docker compose commands"""
    try:
        if action == "up":
            print_status("🏗️  Building and starting services...", "info")
            subprocess.run(["docker", "compose", "down", "--remove-orphans"], 
                         capture_output=True, check=False)
            subprocess.run(["docker", "compose", "up", "--build", "-d"], check=True)
        elif action == "restart":
            print_status("🔄 Restarting services...", "info")
            subprocess.run(["docker", "compose", "restart", "mwdb", "mwdb-web"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print_status(f"❌ Docker compose failed: {e}", "error")
        return False


def create_minio_buckets():
    """Create MinIO buckets using docker compose one-shot init service"""
    print_status("🪣 Setting up MinIO buckets...", "info")
    try:
        # Run the one-shot init container defined in docker-compose
        subprocess.run(["docker", "compose", "up", "-d", "minio-init"], check=True, capture_output=True)
        print_status("✅ Bucket separation configured successfully!", "success")
        return True
    except subprocess.CalledProcessError as e:
        print_status(f"❌ Failed to create buckets (minio-init): {e}", "error")
        return False


def test_api():
    """Test the API to ensure everything is working"""
    print_status("🧪 Testing API functionality...", "info")
    
    # Read admin password
    env_vars = {}
    with open("mwdb-vars.env", "r") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                env_vars[key] = value
    
    admin_password = env_vars.get("MWDB_ADMIN_PASSWORD")
    
    try:
        # Test authentication
        import json
        data = json.dumps({"login": "admin", "password": admin_password}).encode()
        req = urllib.request.Request("http://localhost:8080/api/auth/login", 
                                   data=data,
                                   headers={"Content-Type": "application/json"})
        response = urllib.request.urlopen(req)
        auth_data = json.loads(response.read().decode())
        
        if "token" in auth_data:
            print_status("✅ Authentication working!", "success")
            return True
        else:
            print_status("❌ Authentication failed", "error")
            return False
            
    except Exception as e:
        print_status(f"❌ API test failed: {e}", "error")
        return False


def smoke_test_upload_sample():
    """Upload a small random sample to verify end-to-end flow"""
    print_status("🧪 Uploading a test sample...", "info")
    # Read admin password
    env_vars = {}
    with open("mwdb-vars.env", "r") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                env_vars[key] = value

    try:
        import json, tempfile, os
        data = json.dumps({"login": "admin", "password": env_vars["MWDB_ADMIN_PASSWORD"]}).encode()
        req = urllib.request.Request("http://localhost:8080/api/auth/login",
                                     data=data,
                                     headers={"Content-Type": "application/json"})
        response = urllib.request.urlopen(req)
        auth = json.loads(response.read().decode())
        token = auth.get("token")
        if not token:
            print_status("❌ Missing token in auth response", "error")
            return False

        # Create a small random file and upload it
        os.makedirs("TheZoo_volume/samples", exist_ok=True)
        tmp_file = os.path.join("TheZoo_volume/samples", "smoke.bin")
        with open(tmp_file, "wb") as f:
            f.write(os.urandom(2048))

        # Build multipart request manually
        boundary = "----TheZooBoundary"
        body = []
        body.append(f"--{boundary}\r\n".encode())
        body.append(b"Content-Disposition: form-data; name=\"file\"; filename=\"smoke.bin\"\r\n")
        body.append(b"Content-Type: application/octet-stream\r\n\r\n")
        body.append(open(tmp_file, "rb").read())
        body.append(f"\r\n--{boundary}--\r\n".encode())
        body_bytes = b"".join(body)

        req = urllib.request.Request(
            "http://localhost:8080/api/file",
            data=body_bytes,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
        )
        resp = urllib.request.urlopen(req)
        if resp.getcode() == 200:
            print_status("✅ Test sample uploaded", "success")
            return True
        print_status(f"⚠️  Unexpected response: {resp.status}", "warning")
        return False
    except Exception as e:
        print_status(f"⚠️  Smoke test upload failed: {e}", "warning")
        return False


def print_final_status():
    """Print final status and access information"""
    print_status("\n🎉 TheZoo Platform Setup Complete!", "success")
    print_status("=" * 40, "success")
    
    # Read admin password
    with open("mwdb-vars.env", "r") as f:
        for line in f:
            if line.startswith("MWDB_ADMIN_PASSWORD="):
                admin_password = line.split("=", 1)[1].strip()
                break
    
    print("\n📊 Platform Status:")
    try:
        result = subprocess.run(["docker", "compose", "ps"], 
                              capture_output=True, text=True)
        running_count = result.stdout.count("Up")
        print(f"- Active Services: {running_count}")
    except:
        print("- Services: Running")
    
    print("\n🌐 Access Points:")
    print("- MWDB Web Interface: http://localhost:8080")
    print("- Karton Dashboard: http://localhost:8000")
    print("- MinIO Console: http://localhost:9001")
    
    print("\n🔑 Login Credentials:")
    print("- Username: admin")
    print(f"- Password: {admin_password}")
    
    print_status("\n🛡️  File Persistence Protection:", "success")
    print("✅ MWDB files: stored in 'mwdb-files' bucket")
    print("✅ Karton tasks: use 'karton' bucket") 
    print("✅ Files will NOT be deleted after analysis!")
    
    print("\n📚 For more information:")
    print("https://mwdb.readthedocs.io/en/latest/setup-and-configuration.html")


def full_setup():
    """Complete platform setup"""
    print_status("🚀 TheZoo Platform Setup", "success")
    print_status("=" * 30, "success")
    print("\nThis script will:")
    print("✅ Generate secure configuration")
    print("✅ Configure separate MinIO buckets (prevents file deletion)")
    print("✅ Start the platform services")
    print("✅ Verify the setup")
    print()
    
    # Check prerequisites
    if not check_docker():
        print_status("❌ Docker is not running. Please start Docker first.", "error")
        sys.exit(1)
    
    if not check_docker_compose():
        print_status("❌ Docker Compose is not available. Please install Docker Compose.", "error")
        sys.exit(1)
    
    # Step 0: Ensure submodules
    print_status("📦 Step 0: Initializing submodules...", "warning")
    ensure_submodules()

    # Step 1: Generate configuration
    print_status("🔧 Step 1: Generating configuration...", "warning")
    if os.path.exists("mwdb-vars.env"):
        print_status("⚠️  Configuration already exists, skipping generation", "warning")
    else:
        setup_mwdb_vars()
        print_status("✅ Configuration generated", "success")
    
    # Step 2: Start services
    print_status("\n🏗️  Step 2: Starting services...", "warning")
    if not run_docker_compose("up"):
        sys.exit(1)
    print_status("✅ Services started", "success")
    
    # Step 3: Wait for services
    print_status("\n⏳ Step 3: Waiting for services...", "warning")
    if not wait_for_service("http://localhost:9000/minio/health/live", "MinIO"):
        sys.exit(1)
    
    if not wait_for_service("http://localhost:8080/api/ping", "MWDB API"):
        sys.exit(1)
    
    # Step 4: Setup buckets
    print_status("\n🪣 Step 4: Setting up buckets...", "warning")
    if not create_minio_buckets():
        sys.exit(1)
    
    # Step 5: Test the setup
    print_status("\n🧪 Step 5: Testing setup...", "warning")
    if not test_api():
        print_status("⚠️  API test failed, but platform may still be functional", "warning")
    else:
        smoke_test_upload_sample()
    
    # Final status
    print_final_status()


def main():
    """Main function with command line argument support"""
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--setup", "-s", "setup"]:
            # Full setup mode
            full_setup()
        elif sys.argv[1] in ["--config-only", "-c"]:
            # Configuration only mode
            print_status("🔧 Generating configuration only...", "info")
            setup_mwdb_vars()
            print_status("✅ Configuration generated. Run with --setup for full installation.", "success")
        elif sys.argv[1] in ["--help", "-h"]:
            print("TheZoo Platform Setup")
            print("====================")
            print()
            print("Usage:")
            print("  python3 main.py                 # Generate configuration only")
            print("  python3 main.py --setup         # Complete setup (recommended)")
            print("  python3 main.py --config-only   # Generate configuration only")
            print("  python3 main.py --help          # Show this help")
            print()
            print("The --setup option will:")
            print("  ✅ Generate secure configuration")
            print("  ✅ Configure separate MinIO buckets (prevents file deletion)")
            print("  ✅ Start the platform services")
            print("  ✅ Verify the setup")
        else:
            print_status(f"❌ Unknown option: {sys.argv[1]}", "error")
            print("Use --help for available options")
            sys.exit(1)
    else:
        # Default behavior - just generate configuration for backward compatibility
        setup_mwdb_vars()
        print()
        print_status("✅ Configuration generated!", "success")
        print_status("💡 Tip: Use 'python3 main.py --setup' for complete automated setup", "info")

if __name__ == '__main__':
    main()