import random, string, configparser


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
    
    #setup ini for karton and mwdb-core communitcation
    karton_ini = "./TheZoo_volume/karton/karton.ini" 
    mwdb_ini = "./TheZoo_volume/karton/mwdb.ini"
    setup_ini_file(karton_ini, "mwdb", "password", ADMIN_PASSWORD)
    setup_ini_file(karton_ini, "minio", "access_key", MINIO_ACCESS_KEY)
    setup_ini_file(karton_ini, "minio", "secret_key", MINIO_SECRET_KEY)
    setup_ini_file(mwdb_ini, "mwdb", "secret_key", SECRET_KEY)
    setup_ini_file(mwdb_ini, "mwdb", "s3_storage_access_key", MINIO_ACCESS_KEY)
    setup_ini_file(mwdb_ini, "mwdb", "s3_storage_secret_key", MINIO_SECRET_KEY)
    
    
def setup_ini_file(ini_file, section, key, val):
    config = configparser.ConfigParser()
    config.read(ini_file)
    config.set(section,key,val) 
    with open(ini_file, 'w') as configfile:
        config.write(configfile)


def main():
    setup_mwdb_vars()

if __name__ == '__main__':
    main()


