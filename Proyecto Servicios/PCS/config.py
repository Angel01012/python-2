class BasicConfig:
    USER_DB = 'eduardo'
    PASS_DB = 'adm1n123'
    URL_DB = '54.188.55.237'
    PORT_DB = '3306'
    NAME_DB = 'pcs'
    FULL_URL_DB = f"mysql+pymysql://{USER_DB}:{PASS_DB}@{URL_DB}:{PORT_DB}/{NAME_DB}"
    SQLALCHEMY_DATABASE_URI = FULL_URL_DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY="llave_secreta"