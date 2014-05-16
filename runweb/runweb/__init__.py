try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    print("PyMySQL not available, use another database engine")
