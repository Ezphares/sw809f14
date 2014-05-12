try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    print("PyMQL not available, use another database engine")