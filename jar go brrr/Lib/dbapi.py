# dbapi.py
# AP
# Version 1.9, Feb 15, 2017

import os
from com.ziclix.python.sql import zxJDBC

def importJar(jarFile):
    if not os.path.exists(jarFile):
        raise IOError("Can't import " + jarFile)
    from java.net import URL, URLClassLoader
    from java.lang import ClassLoader
    from java.io import File
    m = URLClassLoader.getDeclaredMethod("addURL", [URL])
    m.accessible = 1
    m.invoke(ClassLoader.getSystemClassLoader(), [File(jarFile).toURL()])

__libhome = getTigerJythonPath("lib")
__postgresql_driver = __libhome + "postgresql-9.2-1002.jdbc4.jar"
__mysql_driver = __libhome + "mysql-connector.jar"
__derby_driver = __libhome + "derbyclient.jar"
__embedded_derby_driver = __libhome + "derby.jar"
__sqlite_driver = __libhome + "sqlite-jdbc-3.16.1.jar"

def getDBConnection(*args, **kwargs):
    try:
        if len(args) == 0:
            return zxJDBC.connect(**kwargs)
        if len(args) == 1:
            return zxJDBC.connect(args[0], **kwargs)
        if len(args) == 2:
            return zxJDBC.connect(args[0], args[1], **kwargs)
        if len(args) == 3:
            return zxJDBC.connect(args[0], args[1], args[2], **kwargs)
        if len(args) == 4:
            return zxJDBC.connect(args[0], args[1], args[2], args[3], **kwargs)
        if len(args) == 5:
            return zxJDBC.connect(args[0], args[1], args[2], args[3], args[4], **kwargs)
        if len(args) == 6:
            return zxJDBC.connect(args[0], args[1], args[2], args[3], args[4], args[5], **kwargs)
        return None
    except Exception, e:
        return None

def getDerbyConnection(serverURL, dbname, username, password):
    importJar(__derby_driver)
    con = getDBConnection("jdbc:derby://" + serverURL + "/" + dbname + ";create=true", username, password, "org.apache.derby.jdbc.ClientDriver")
    if con == None:
        raise RuntimeError("Failed to connect to database with arguments (" + 
            serverURL + ", " + dbname + ", " + username + ", " + password + ")")
    return con

def getEmbeddedDerbyConnection(dbname):
    importJar(__embedded_derby_driver)
    con = getDBConnection("jdbc:derby:" + dbname + ";create=true", None, None, "org.apache.derby.jdbc.EmbeddedDriver")
    if con == None:
        raise RuntimeError("Failed to connect to database with argument (" + dbname + ")")
    return con

def getMySQLConnection(serverURL, dbname, username, password):
    importJar(__mysql_driver)
    con = getDBConnection("jdbc:mysql://" + serverURL + "/" + dbname, username, password, "org.gjt.mm.mysql.Driver")
    if con == None:
        raise RuntimeError("Failed to connect to database with arguments (" + 
            serverURL + ", " + dbname + ", " + username + ", " + password + ")")
    return con

def getPostgreSQLConnection(serverURL, dbname, username, password):
    importJar(__postgresql_driver)
    con = getDBConnection("jdbc:postgresql://" + serverURL + "/" + dbname, username, password, "org.postgresql.Driver")
    if con == None:
        raise RuntimeError("Failed to connect to database with arguments (" + 
            serverURL + ", " + dbname + ", " + username + ", " + password + ")")
    return con

def getSQLiteConnection(dbname):
    importJar(__sqlite_driver)
    con = getDBConnection("jdbc:sqlite:" + dbname , None, None, "org.sqlite.JDBC")
    if con == None:
        raise RuntimeError("Failed to connect to database with argument (" + dbname + ")")
    return con

def connect(*args):
    if not (len(args) == 1 or len(args) == 4):
        raise ValueError("Illegal number of arguments")
    url = args[0].strip()
    index = url.find(':')
    if index == -1:
        raise ValueError("No database name given in '" + url + 
        "'.\n    (Use prefix 'sqlite:', 'derby:', 'derbyserver:', 'mysql:', 'postgre:'" )
    database = url[0:index].strip().lower()
    if database not in ['sqlite', 'derby', 'derbyserver', 'mysql', 'postgre']:
        raise ValueError("Illegal database name given in '" + url + 
        "'.\n    (Use prefix 'sqlite:', 'derby:', 'derbyserver:', 'mysql:', 'postgre:'" )
    url = url[index + 1:]    
    if database == 'sqlite':
        if len(args) != 1:
            raise ValueError("Illegal number of arguments")
        return getSQLiteConnection(url)     
    elif database == 'derby':
        if len(args) != 1:
            raise ValueError("Illegal number of arguments")
        return getEmbeddedDerbyConnection(url)     
    elif database == 'derbyserver':
        if len(args) != 4:
            raise ValueError("Illegal number of arguments")
        return getDerbyConnection(url, args[1], args[2], args[3])     
    elif database == 'mysql':
        if len(args) != 4:
            raise ValueError("Illegal number of arguments")
        return getMySQLConnection(url, args[1], args[2], args[3])     
    elif database == 'postgre':
        if len(args) != 4:
            raise ValueError("Illegal number of arguments")
        return getPostgreSQLConnection(url, args[1], args[2], args[3])     

