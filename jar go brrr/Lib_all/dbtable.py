# dbtable.py
# OO abstraction of SQL table
# Version 3.07, Aug 15, 2017
 
from sqlite3 import *
from prettytable import printTable, strTable
import os
 
def debug(msg):
    if DbTable.debug:
        print "DEBUG:-->" + msg
 
class SQLExecutionFailure(Exception): pass
class DbTableFailure(Exception): pass

def showDbInfoTJ(database):
    '''
    Prints table names and attributes of all tables in database that is part of the TigerJython distribution."
    '''
    source = "_databases/" + database
    currentdir = getTigerJythonPath("main")
    destination = currentdir + database
    try:
        copyFromJar(source, destination)
    except:
        print "Database", database, "not found in TigerJython distribution"
    else:
        showDbInfo(database)
    
def showDbInfo(database):
    '''
    Prints table names and attributes of all tables in database."
    '''
    if not database.endswith(".db"):
            database += ".db"

    if not os.path.isfile(database):
        print "Database", database, "not found."
        return
    info = getDbInfo(database)
    if info == {}:
        print "No tables found in", database
        return
    for table in info:
        print table, ":", info[table]            
 
   
# -------------------- class DbTable ---------------------------------
class DbTable(object):
    ''' 
    Implementation of a table structure ressembling to a SQL table.
    '''
    tableNames = []
    con = None
    debug = False
     
    def __init__(self, *args):
        '''
        Creates a table with given attributes (names of columns, field names, specified as strings) (may be packed into a tuple). If a table is
        given, a clone is created. The attributes must conform to a legal variable name.
        '''
        debug("DbTable ctor with args: " + str(args))
        self.isEmpty = True
        if len(args) == 0:
            debug("Creating emtpy table")
            return # empty table
        self._setup(*args)

    def _setup(self, *args): 
       # Create table name
        debug("Existing tableNames: "  + str(DbTable.tableNames))
        self.extcon = None
        self.attributeInfo = {}   
        self.tableName = DbTable._getNextTableName()
         
        # Create database if not yet done
        if self.tableName == "tbl$$$0":
            DbTable.con = connect(":memory:")
            debug("RAM database created")
        else:
            debug("Using exiting RAM database")
             
        # Create table
        isCopyCtor = False
        if len(args) == 1:
            if type(args[0]) == tuple or type(args[0]) == list:
                args = args[0]
            elif isinstance(args[0], DbTable):  # copy constructor
                debug("Executing copy constructor")
                isCopyCtor = True
                self.attributeNames = args[0].getAttributes()
    
        if not isCopyCtor:
             self.attributeNames = args
             self.sortAttr = None
             self.ascending = True

        
        for i in range(len(self.attributeNames)):
            setattr(self, self.attributeNames[i], self.attributeNames[i])
        if isCopyCtor:
            for row in args[0]._getRows(self.attributeNames, None, None):
               self.insert(row)
            self.sortAttr = args[0].sortAttr
            self.ascending = args[0].ascending
     
    def _getTableName(self):
        return self.tableName
                    
    def getAttributes(self):
        '''
        Returns attributes (name of columns, field names) as tuple.
        '''
        return tuple(self.attributeNames)
    
    def _getRows(self, columnNames, whereNames, whereValues):
        return self._select(columnNames, whereNames, whereValues).fetchall()
 
    def _select(self, columnNames, whereNames, whereValues):
        cursor = DbTable.con.cursor()
        if columnNames == None:
            cols = "*"
        else:
            cols = ""
            n = len(columnNames)
            for i in range(n):
                if i < n - 1:
                    cols += "[" + columnNames[i] + "], "  # use [] to allow reserved words (like 'alter')
                else:
                    cols += "[" + columnNames[i] + "]"

        if whereNames == None:
            where = ""
        else:
            where = " WHERE "            
            n = len(whereNames)
            for i in range(n):
                if self.attributeInfo[whereNames[i]] in ['int', 'float']:
                    where += "[" + whereNames[i] + "] = " + str(whereValues[i])
                    if i < n - 1:
                       where += " AND "
                else:
                    where += "[" + whereNames[i] + "] = '" + str(whereValues[i]) + "'"
                    if i < n - 1:
                        where += " AND "
        if self.sortAttr == None:
            sort = ""
        else:
            if self.ascending:
                sort = " ORDER BY [" + self.sortAttr + "]"
            else:
                sort = " ORDER BY [" + self.sortAttr + "] DESC"
        
        sql = "SELECT " + cols + " FROM " + self.tableName + where + sort  
        cursor = self._execute(sql, "_select()")        
        return cursor
    
    def __len__(self):
        '''
        Return the number of table rows.
        '''
        columnNames = self.attributeNames
        attributeNames = None
        attributeValues = None
        return len(self._getRows(columnNames, attributeNames, attributeValues))    
    
    def insertMany(self, resultSet):
        '''
        Inserts every entry from the given list or tuple (typically a result set returned by select()).
        '''
        for entry in resultSet:
            self.insert(entry)
                     
    def insert(self, *args):
        '''
        Insert single or multiple records. args is either a parameter list with all attribute values or a tuple. If it is a tuple or a list and
        the first entry is a tuple or a list, multiple record insertion is assumed.
        The parameter types can be: str, int, float or binary and is stored (int is stored as float, but returned as int, if it is a whole number).
        Binaries can be loaded from a file using the getBytes(filename) function.
        All attribute values must be specified.
        '''
        if len(args) == 1 and (type(args[0]) == tuple or type(args[0]) == list):
            args = args[0]
        if  len(self.attributeInfo) ==  0: # types not yet known
            debug("Must get attributeInfo")
            for i in range(len(args)):
                field_value = args[i]
                field_type = type(args[i]).__name__
                self.attributeInfo[self.attributeNames[i]] = field_type
            debug("insert() detected attributeInfo: " + str(self.attributeInfo))        
            DbTable._createDbTable(DbTable.con, self.tableName, self.attributeNames, self.attributeInfo)
            self.isEmpty = False
        
        marks = "("
        for i in range(len(args)):
            marks += '?'
            if i < len(args) - 1:
                marks += ','
            else:
                marks += ')'
        sql = "INSERT INTO  " + self.tableName + " VALUES " + marks
        pstmt = DbTable.con.prepareStatement(sql)
        debug("insert() sql: " + sql)
        for i in range(len(args)):
            if self.attributeInfo[self.attributeNames[i]] == 'int':
                field_value = str(args[i])
                pstmt.setInt(i + 1, int(field_value))
                debug("setInt():  #" + str(i + 1) + ", " + field_value)
            elif self.attributeInfo[self.attributeNames[i]] == 'float':
                field_value = str(args[i])
                pstmt.setDouble(i + 1, float(field_value))
                debug("setDouble(): #" + str(i + 1) + ", " + field_value)
            elif self.attributeInfo[self.attributeNames[i]] in ['str', 'unicode']:
                field_value = str(args[i])
                pstmt.setString(i + 1, field_value)
                debug("setString(): #" + str(i + 1) + ", " + field_value)
            elif self.attributeInfo[self.attributeNames[i]] == 'array':
                field_value = args[i]
                pstmt.setBytes(i + 1, field_value)
                debug("setBytes(): #" + str(i + 1) + ", value")
        try:
            pstmt.execute()
            DbTable.con.commit()
        except Exception, e:
            debug("Failed to execute SQL. Exception: " + str(e))
            raise SQLExecutionFailure("Failed to execute SQL " + sql + " in insert()")

    def sort(self, sortingAttribute, ascending = True):
        '''
        Defines the given attribute as sorting attribute. Table views are then sorted ascendingly with respect to this attribute.
        The sorting attribute is copied to clones.
        '''
        self.sortAttr = sortingAttribute   
        self.ascending = ascending

    def view(self, *args, **kwargs):
        '''
        Shows formatted table values with specified rows that fulfill the conditions in the the attribute/value sequence.
        If an attribute of the table's attributes is not present, all values of this attribute fulfill (wildcard). 
        If a given attribute is not part of the table's attributes, the condition is left out.
        (e.g. view("name", "age", name = "Meyer", firstname = "Bob") shows column 'name' and 'age' of all occurances of Meyer Bob.)
        '''
        if self.isEmpty:
            print "Empty table"
            return
        if len(args) == 0:
            columnNames = self.attributeNames
        else:
            columnNames =  args
        if len(kwargs) == 0:
            attributeNames = None
            attributeValues = None
        else:
            attributeNames = tuple(kwargs.keys())
            attributeValues = tuple(kwargs.values())
        printTable(self._select(columnNames, attributeNames, attributeValues))
    
    def getView(self, *args, **kwargs):
        '''
        Returns string with formatted table values with specified rows that fulfill the conditions in the the attribute/value sequence.
        If an attribute of the table's attributes is not present, all values of this attribute fulfill (wildcard). 
        If a given attribute is not part of the table's attributes, the condition is left out.
        (e.g. view("name", "age", name = "Meyer", firstname = "Bob") shows column 'name' and 'age' of all occurances of Meyer Bob.)
        '''
        if self.isEmpty:
            print "Empty table"
            return
        if len(args) == 0:
            columnNames = self.attributeNames
        else:
            columnNames =  args
        if len(kwargs) == 0:
            attributeNames = None
            attributeValues = None
        else:
            attributeNames = tuple(kwargs.keys())
            attributeValues = tuple(kwargs.values())
        return strTable(self._select(columnNames, attributeNames, attributeValues))
        
    def __str__(self):
        if self.isEmpty:
            return "Empty table"
        return self.getView()
 
    def __repr__(self):
        if self.isEmpty:
            return "Empty table"
        return self.getView()
 
    def __iter__(self):
        self.rows = self._getRows(self.attributeNames, None, None)
        self.pointer = -1
        return self
     
    def next(self):
        if self.pointer == len(self.rows) - 1:
            raise StopIteration
        self.pointer += 1
        return Record(self, self.rows[self.pointer])
         
    def delete(self, **kwargs):
        '''
        Deletes all rows that fulfill the the specified conditions (search pattern, see method search()).
        '''
        if len(kwargs) == 0:
            sql = "DELETE FROM " + self.tableName
        else:
            whereNames = tuple(kwargs.keys())
            whereValues = tuple(kwargs.values())
            sql = "DELETE FROM " + self.tableName + " WHERE "
            for i in range(len(whereNames)):
                if self.attributeInfo[whereNames[i]] in ['int', 'float']:
                    sql += "[" + whereNames[i] + "] = " + str(whereValues[i])
                    if i < len(whereNames) - 1:
                        sql += " AND " 
                else:
                    sql += "[" + whereNames[i] + "] = '" + str(whereValues[i]) + "'"
                    if i < len(whereNames) - 1:
                        sql += " AND "
        self._execute(sql, "delete()")                        
        
    def update(self, **kwargs):
        '''
        Updates all rows that correspond to attribute = value pairs of the first parameter parenthesis with new  
        attribute = value of the second parameter parenthesis. If the first parameter parenthesis is empty, all records are updated.
        Example: update(name = "Mayer")(age = 44, city = "Boston") updates age and city of all rows with name = "Mayer".
        '''
        self.myargs = kwargs
        return self._updateExec
        
    def _updateExec(self, **kwargs):
        searchNames = tuple(self.myargs.keys())
        searchValues = tuple(self.myargs.values())
        dataNames = tuple(kwargs.keys())
        dataValues = tuple(kwargs.values())
        if dataNames == ():
            return
        setstr = " SET "
        for i in range(len(dataNames)):
            if self.attributeInfo[dataNames[i]] in ['int', 'float']:
                setstr += "[" + dataNames[i] + "] = " + str(dataValues[i])
                if i < len(dataNames) - 1:
                    setstr += ", " 
            else:
                setstr += "[" + dataNames[i] + "] = '" + str(dataValues[i]) + "'"
                if i < len(dataNames) - 1:
                    setstr += "', " 

        wherestr = ""            
        if searchNames != ():            
            wherestr = " WHERE "
            for i in range(len(searchNames)):
                if self.attributeInfo[searchNames[i]] in ['int', 'float']:
                    wherestr += "[" + searchNames[i] + "] = " + str(searchValues[i])
                    if i < len(searchNames) - 1:
                        wherestr += " AND "
                else:
                    wherestr += "[" + searchNames[i] + "] = '" + str(searchValues[i]) + "'"
                    if i < len(searchNames) - 1:
                        wherestr += " AND "
        sql = "UPDATE " + self.tableName + setstr + wherestr   
        self._execute(sql, "update()")
  
    def join(self, table, *args):
        '''
        Joins the current table with the given table If no further parameter is given, a full join (cross product) is performed. 
        Two additinal parameters left_attributename and right_attributename selects fields in the joined tables where the condition left = right is fulfilled.
        If a fourth argument showJoinAttr is True, the left and right attributes are included in the
        result, otherwise they are hidden (in the latter case, the attribute names may be identical, default value).
        Example: tbl = person.join(sport, person.pid, sport.sid), or person.join(sport, "pid", "sid") or person.join(sport, "pid", "sid", True)  
        '''
        if len(args) == 0:
            left = None
            right = None
            showJoinAttr = True
        elif len(args) == 2:
            left = args[0]
            right = args[1]
            showJoinAttr = False
        elif len(args) == 3:
            left = args[0]
            right = args[1]
            showJoinAttr = args[2]
        else:
            raise ValueError("Illegal number of arguments")
        debug("join() with left: " + str(left) + " and right: " + str(right))
        leftAttributes = self.getAttributes()
        rightAttributes = table.getAttributes()
        attributeTypes = []
        sql = "SELECT "
        for i in range(len(leftAttributes)):
            if leftAttributes[i] == left and not showJoinAttr:
                continue
            sql += self._getTableName() + "." + leftAttributes[i] + ", "
            attributeTypes.append(self.attributeInfo[leftAttributes[i]])
        for i in range(len(rightAttributes)):
            if rightAttributes[i] == right and not showJoinAttr:
                continue
            if i < len(rightAttributes) - 1:
                sql += table._getTableName() + "." + rightAttributes[i] + ", "
            else:
                sql += table._getTableName() + "." + rightAttributes[i]
            attributeTypes.append(table.attributeInfo[rightAttributes[i]])

            if self.sortAttr == None:
                sort = ""
            else:
                if self.ascending:
                    sort = " ORDER BY [" + self.sortAttr + "]"
                else:
                    sort = " ORDER BY [" + self.sortAttr + "] DESC"
             
        if left == None or right == None:        
            sql +=  " FROM " + self._getTableName() + " JOIN " + table._getTableName() + sort
        else:
            sql +=  " FROM " + self._getTableName() + " JOIN " + table._getTableName() + " ON " + self._getTableName() + "." + left + " = " + table._getTableName() + "." + right + sort
        cursor = self._execute(sql, "join()")
        
        attributes = []
        for i in range(len(leftAttributes)):
            if leftAttributes[i] == left and not showJoinAttr:
                continue
            attributes.append(leftAttributes[i])
        for i in range(len(rightAttributes)):
            if rightAttributes[i] == right and not showJoinAttr:
                continue
            attributes.append(rightAttributes[i])
        aTable = DbTable(attributes)
        for row in cursor.fetchall():
            aTable.insert(row)
        return aTable

    def clone(self):
        '''
        Returns a independent copy of the table.
        '''
        table = DbTable(self.attributeNames)
        for row in self._getRows(self.attributeNames, None, None):
            table.insert(row)
        self.sortAttr = table.sortAttr
        self.ascending = table.ascending
        return table
                     
    def _execute(self, sql, msg):
        try:
            debug("Action " + msg + ". Executing SQL: "  + sql)
            cursor = DbTable.con.cursor()
            cursor.execute(sql)
            DbTable.con.commit()
            return cursor
        except Exception, e:
            debug("Failed to execute SQL. Exception: " + str(e))
            raise SQLExecutionFailure("Failed to execute SQL " + sql + " in " + msg)
            return None
        
    def select(self, *args, **kwargs):
        '''
        Returns a tuple with the specified rows that fulfill the conditions in the the attribute/value sequence.
        If an attribute of the table's attributes is not present, all values of this attribute fulfill (wildcard). 
        If a given attribute is not part of the table's attributes, the condition is left out.
        (e.g. select("name", "age", name = "Meyer", firstname = "Bob") returns column 'name' and 'age' of all occurances of Meyer Bob.)
        '''
        if len(args) == 0:
            columnNames = self.attributeNames
        else:
            columnNames =  args
        if len(kwargs) == 0:
            attributeNames = None
            attributeValues = None
        else:
            attributeNames = tuple(kwargs.keys())
            attributeValues = tuple(kwargs.values())
        return tuple(self._select(columnNames, attributeNames, attributeValues).fetchall())
        
    def _getVarname(self):
        varnamelist = findVariableNamesOfSelf(self)
        debug("varnamelist:" + str(varnamelist))
        for entry in varnamelist:
            if entry != 'self':
                debug("_getVarname() returns " + entry)
                return entry
        return None    
             
    def save(self, databaseName, tableName = None, autocommit = True):
        '''
        Saves the table in external SQLite database with given database name (should end with .db). If given table name is None,  the name of the variable 
        is used as SQL table name. If the database does not exist, it is created. The column names in the SQL table are the table attributes. 
        Each column is accompanied by a column with type information.
        If if the SQL table with given name already exists, it is first deleted. If autocommit = False, the inserts are not committed until commitAndClose() is called (for faster insert
        of many records).
        '''
        if not databaseName.endswith(".db"):
            databaseName += ".db"

        con = connect(databaseName)
        self.extcon = con
        debug("saveTable(): Database connection to " + databaseName + " opened")
        if tableName == None:
            tableName = self._getVarname()
        debug("saveTable(): Using SQL table name: " + tableName)
        try:         
            if tableName in con.showTables():
                DbTable._dropDbTable(con, tableName)
            else:
                debug("No need to drop table " + tableName)
        except Exception, e:
            debug("Failed to execute SQL. Exception: " + str(e))
            con.close()
            debug("saveTable(): Database connection to " + databaseName + " closed")
        try:
            DbTable._createDbTable(con, tableName, self.attributeNames, self.attributeInfo)
            cursor = self._select(None, None, None)
            for row in cursor.fetchall():
                DbTable._insertDbRow(con, tableName, row, autocommit)
            if autocommit:    
                con.close()    
                debug("saveTable(): Database connection to " + databaseName + " closed")
            else:
                debug("saveTable(): Database connection to " + databaseName + " remains open")
        except Exception, e:
            con.close()
            debug("Failed to execute SQL. Exception: " + str(e))
            raise SQLExecutionFailure("Cannot perform table operation in saveTable()")
     
    def restoreFromTJ(self, databaseName, tableName = None):
        '''
        Copies database from the TigerJython JAR distribution to the current folder, retrieves data
        and copies it into the given table.  All pervious table information is lost.
        If the given table name is None, the SQL table name corresponds to the variable name (default: None). 
        Returns False, if database is not found; otherwise returns True
        ''' 
        self.restore(databaseName, tableName, True)

    def restore(self, databaseName, tableName = None, fromJar = False):
        '''
        Retrieves data from SQL table in external SQLite database with given database file path (should end with .db) and copies it into the given table.
        All pervious table information is lost.
        If the given table name is None, the SQL table name corresponds to the variable name (default: None). If fromJar is True, the SQL database
        is read from the TigerJython distribution JAR (default: False)
        '''
        if not databaseName.endswith(".db"):
            databaseName += ".db"

        if tableName == None:
            tableName = self._getVarname()
        debug("restoreTable(): Using SQL table name: " + tableName)
        if not self.isEmpty:
            DbTable._dropDbTable(DbTable.con, self._getTableName())
        if fromJar:
            debug("restoreTable(): Opening database connection from JAR. Database name: " + databaseName)
            extcon = connectTJ(databaseName)
            if extcon == None:
                debug("restoreTable(): Opening database failed")
                raise DbTableFailure("Cannot open database " + databaseName)
        else:
            debug("restoreTable(): Opening database connection from file system. Database name: " + databaseName)
            if not os.path.isfile(databaseName):
                debug("restoreTable(): Opening database failed")
                raise DbTableFailure("Cannot open database " + databaseName)
            extcon = connect(databaseName)
        try:         
            sql = "SELECT * FROM " + tableName
            debug("restoreTable() SQL: "  + sql)
            cursor = extcon.cursor()
            cursor.execute(sql)
            attributeNames = cursor.getColumnNames()
            debug("restoreTable() uses attributeNames: " + str(attributeNames))
            self._setup(attributeNames)
            result = cursor.fetchall()
            for row in result:
                self.insert(row)
            extcon.close()    
            debug("restoreTable(): Database connection to " + databaseName + " closed")
        except Exception, e:
            debug("Failed to execute SQL. Exception: " + str(e))
            raise SQLExecutionFailure("Cannot perform table operation in restoreTable()")
            extcon.close()
            
    def commitAndClose(self):
        '''
        Commit and close the external SQL database after save() with autocommit = False is called.
        '''
        if self.extcon != None:
            self.extcon.commit()
            self.extcon.close()    
            self.extcon = None

    def importFromCSV(self, filename, delimiter):
        '''
        Import table data from a CSV formatted text file. The DbTable instance must have field names (attributes)
        that correspond to the lines in the text file. Empty lines are skipped. The delimiter is used to separate 
        record fields in each line.
        '''
        import csv
        if not filename.endswith(".csv"):
            filename += ".csv"
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter = delimiter)
            for row in reader: # rows is a list with strings
                if row == []:
                    continue
                row1 = []
                for item in row:
                    if item == "":
                        item = "'*'"
                    if DbTable.is_number(item):
                        n = float(item)
                        if n.is_integer():
                            row1.append(int(n))
                        else:
                            row1.append(n)
                    else:
                        row1.append(item)
                self.insert(row1)

    def exportToCSV(self, filename, delimiter, *args, **kwargs):
        '''
        Export table data to a CSV formatted text file.
        Creates a CSV text file  with given name that contains all specified columns that fulfills the conditions 
        in the the attribute/value sequence.  The delimiter is used to separate fields.
        If an attribute of the table's attributes is not present, all values of this attribute fulfill (wildcard). 
        If a given attribute is not part of the table's attributes, the condition is left out.
        (e.g. exportToCSV("myfile.csv", ";", "name", "age", name = "Meyer", firstname = "Bob") exports column 'name' and 'age' 
        of all occurances of Meyer Bob.) 
        '''
        import csv
        if not filename.endswith(".csv"):
            filename += ".csv"
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter = delimiter) 
            data = self.select(*args, **kwargs)
            for row in data:
                writer.writerow(row)
        debug("Successfully saved data to CSV file '" + filename + "'")    


    # ----------------------- static methods ---------------------------------        
    @staticmethod
    def _closeDb():
        if DbTable.con != None:
            DbTable.con.close()
            debug("Connection closed")
 
    @staticmethod
    def _insertDbRow(con, tableName, row, autocommit = True):
        nb = len(row)
        marks = "("
        for i in range(nb):
            marks += '?'
            if i < nb - 1:
                marks += ','
            else:
                marks += ')'
        sql = "INSERT INTO  " + tableName + " VALUES " + marks
        pstmt = con.prepareStatement(sql)
        debug("_insertDbRow() sql: " + sql)
        for i in range(nb):
            if str(type(row[i])) == "<type 'int'>":
                pstmt.setInt(i + 1, row[i])
                debug("pstmt.setInt(): #" + str(i + 1) + ", " + str(row[i]))
            elif str(type(row[i])) == "<type 'float'>":
                pstmt.setDouble(i + 1, row[i])
                debug("pstmt.setDouble(): #" + str(i + 1) + ", " + str(row[i]))
            elif str(type(row[i])) in ["<type 'str'>", "<type 'unicode'>"]:
                field_value = str(row[i])
                pstmt.setString(i + 1, field_value)
                debug("pstmt.setString(): #" + str(i + 1) + ", " + field_value)
            elif str(type(row[i])) == "<type 'array.array'>":
                pstmt.setBytes(i + 1, row[i])
                debug("pstmt.setBytes(): #" + str(i + 1) + ", value")
        try:
            pstmt.execute()
            if autocommit:
                con.commit()
        except Exception, e:
            debug("Failed to execute SQL. Exception: " + str(e))
            raise SQLExecutionFailure("Failed to execute SQL " + sql + " in _insertDbRow()")

    @staticmethod
    def _getNextTableName():
        if len(DbTable.tableNames) == 0:
            next = "tbl$$$0"
        else:
            last = DbTable.tableNames[-1]
            nb = int(last[6:])
            next = "tbl$$$" + str(nb + 1)
        DbTable.tableNames.append(next)
        debug("_getNextTableName() returns: "  + next)
        return next
 
    @staticmethod
    def _dropDbTable(con, tableName):
        try:
            sql = "DROP TABLE " + tableName
            cursor = con.cursor()
            cursor.execute(sql)
            con.commit()
            debug("SQLTable " + tableName + " dropped")
        except Exception, e:
            debug("Failed to drop table")

    @staticmethod
    def _createDbTable(con, tableName, attributeNames, attributeInfo):
        # attributeInfo is a dictionnary with attribute name : type
        try:
            sql = "CREATE TABLE " + tableName + " ("
            for i in range(len(attributeNames)):
                attributeType = attributeInfo[attributeNames[i]]
                if attributeType == 'int':
                    attrType = ' INTEGER '
                elif attributeType == 'float':
                    attrType = ' FLOAT '
                elif attributeType == 'array':
                    attrType = ' BLOB '
                else:
                    attrType = ' TEXT '
                sql += "'" + attributeNames[i] + "'" + attrType # quote attributes to allow reserved words (like 'alter')
                if i < len(attributeNames) - 1:
                    sql += ", "
                else:
                    sql += ")"
            debug("_createDbTable() SQL: "  + sql)
            cursor = con.cursor()
            cursor.execute(sql)
            con.commit()
            debug("SQLTable created")
        except Exception, e:
            debug("Failed to create table. Exception: " + str(e))
            con.close()
            raise SQLExecutionFailure("Cannot perform SQL operation in _createDbTable()")
    
    @staticmethod            
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def setDebug(enable):
        DbTable.debug = enable
        

# -------------------- class Record ---------------------------------
class Record():
    def __init__(self, table, record):
        self.table = table
        self.record = record
        self.attributeNames = table.getAttributes()
        for i in range(len(self.attributeNames)):
            setattr(self, self.attributeNames[i], record[i])
            
    def __str__(self):
        result = ""
        n = len(self.attributeNames)
        for i in range(n):
            result += self.attributeNames[i] + ' = '+ str(getattr(self, self.attributeNames[i]))
            if i < n - 1:
                result += ', '
        return result

    def __repr__(self):
        self.__str__()
           

# ------------------ global functions -----------------------------------
                    

registerFinalizeFunction(DbTable._closeDb)
