class BasicConfig:
    USER_DB = 'postgres'
    PASS_DB = 'Juan%4020'
    URL_DB = '127.0.0.1'
    PORT_DB = '5432'
    NAME_DB = 'flask'
    FULL_URL_DB = f"postgresql://{USER_DB}:{PASS_DB}@{URL_DB}:{PORT_DB}/{NAME_DB}"
    SQLALCHEMY_DATABASE_URI = FULL_URL_DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY="llave_secreta"