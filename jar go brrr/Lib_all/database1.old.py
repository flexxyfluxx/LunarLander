# tigerjython/database1.py
#
# (c) 2017, Tobias Kohn
#
# UPDATED: JUNE-13-2017
#
import pickle as _pickle
import os.path as _path
import java.awt.Color as _Color
#
# ===== TABLE =====
#
def _conforms(pattern, value):
    if pattern == value:
        return True
    elif value is None:
        return False
    elif type(pattern) is str and type(value) is str:
        pattern = pattern.lower()
        value = value.lower()
        i, j = 0, 0
        while i < len(pattern) and j < len(value):
            if pattern[i] == '*':
                i += 1
                if i == len(pattern):
                    return True
                i2 = i
                while i2 < len(pattern) and pattern[i2] not in ['*', '?']:
                    i2 += 1
                ch = pattern[i:i2]
                if i2 == len(pattern):
                    return (i + len(ch) <= len(value)) and value.endswith(ch)
                while j < len(value)-len(ch) and value[j:j+len(ch)] != ch:
                    j += 1
            elif pattern[i] == value[j] or pattern[i] == '?':
                i += 1
                j += 1
            else:
                return False
        return i == len(pattern) and j == len(value)
    elif type(pattern) is tuple and len(pattern) == 2 and type(value) in [int, long, float]:
        a, b = pattern
        return a <= value <= b
    elif type(pattern) is list:
        return value in pattern
    return False

class Column():
    def __init__(self, table, name, caption, index):
        self._table = table
        self._index = index
        self._name = name
        self.caption = caption
        
    def clone(self):
        return Column(self._table, self._name, self.caption, self._index)
    
    def sort(self):
        self._table._sort_by_(self._index)
        
    def setIndex(self, index):
        self._table._set_index_of_columns_(self, index)
        
    def __getitem__(self, key):
        return self._table.__getitem__((key, self._index))
    
    def __len__(self):
        return self._table.__len__()
    
    def __setitem__(self, key, value):
        self._table.__setitem__((key, self._index), value)
        
    def _has_key_(self, key):
        return key in [self._name, self.caption]
    
    def _get_data_(self):
        return [row[self._index] for row in self._table._get_data_()[1:]]
    
    @property
    def first(self):
        return self[1]
    
    @property
    def last(self):
        return self[-1]

    def __iter__(self):
        return iter(self._get_data_())
        
    def __repr__(self):
        return str(self._get_data_())
    __str__ = __repr__
    
class Row(object):
    def __init__(self, table, index):
        self._table = table
        self._index = index
    
    def __getitem__(self, key):
        return self._table.__getitem__((self._index, key))
    
    def __len__(self):
        return len(self._table._columns)
    
    def __setitem__(self, key, value):
        self._table.__setitem__((self._index, key), value)

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        for col in self._table._columns:
            if col._name == key:
                return self.__getitem__(key)
        raise AttributeError("there is no attribute or column '%s'" % key)
        
    def __setattr__(self, key, value):
        if key in self.__dict__ or key in ["_table", "_index"]:
            self.__dict__[key] = value
            return 
        for col in self._table._columns:
            if col._name == key:
                self.__setitem__(key, value)
                return
        raise AttributeError("there is no attribute or column '%s'" % key)
        
    def keys(self):
        return [col._name for col in self._table._columns]
        
    def _get_data_(self):
        row = self._table._get_data_()[self._index]
        cols = self._table._columns
        result = {}
        for i in indices(cols):
            result[cols[i]._name] = row[i]
        return result
    
    def delete(self):
        del self._table[self._index]
    remove = delete
    drop = delete
    
    def _get_or_none_(self, key):
        return self._get_data_().get(key)

    def __iter__(self):
        values = self._table._get_data_()[self._index]
        return iter(values)
    
    def __repr__(self):
        result = []
        row = self._table._get_data_()[self._index]
        cols = self._table._columns
        for i in indices(cols):
            result.append("%s: %s" % (cols[i]._name, repr(row[i])))
        return "{%s}" % ", ".join(result)
    __str__ = __repr__

class BaseTable(object):
    
    def _colname_to_index_(self, name):
        for col in self._columns:
            if col._name == name:
                return col._index
        for col in self._columns:
            if col.caption == name:
                return col._index
        raise KeyError("there is no column: '%s'" % name)
        
    def _set_index_of_columns_(self, col, index):
        oldIndex = self._columns.index(col)
        if oldIndex != index:
            del self._columns[oldIndex]
            self._columns.insert(index, col)

    def _get_field_(self, row, col):
        data = self._get_data_()
        return data[row][col]
    
    def _set_field_(self, row, col, value):
        data = self._get_data_()
        data[row][col] = value
    
    def _get_data_(self):
        return []

    def _get_row_(self, row):
        return Row(self, row)
    
    def __len__(self):
        return len(self._get_data_())-1
    
    def __getitem__(self, key):
        if type(key) is tuple:
            a, b = key
            if type(a) is int and type(b) is str:
                b = self._colname_to_index_(b)
                return self._get_field_(a, b)
            elif type(a) is str and type(b) is int:
                a = self._colname_to_index_(a)
                return self._get_field_(b, a)
            elif type(a) is int and type(b) is int:
                return self._get_field_(a, b)
            else:
                raise KeyError("there is no field for '%s'" % str(key))
        elif type(key) is int:
            if 0 <= key <= len(self):
                return self._get_row_(key)
            elif -len(self) <= key < 0:
                return self._get_row_(key + len(self) + 1)
            raise KeyError("index out of range: '%d'" % key)
        elif type(key) is str:
            index = self._colname_to_index_(key)
            return self._columns[index]
        else:
            raise KeyError("there is no field for '%s'" % str(key))
    
    def __setitem__(self, key, value):
        if type(key) is tuple:
            a, b = key
            if type(a) is int and type(b) is str:
                b = self._colname_to_index_(b)
                self._set_field_(a, b, value)
            elif type(a) is str and type(b) is int:
                a = self._colname_to_index_(a)
                self._set_field_(b, a, value)
            elif type(a) is int and type(b) is int:
                self._set_field_(a, b, value)
            else:
                raise KeyError("there is no field for '%s'" % str(key))
        else:
            raise KeyError("there is no field for '%s'" % str(key))

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        for col in self._columns:
            if col._name == key:
                return col
        if key.endswith('s'):
            return self.__getattr__(key[:-1])
        else:
            raise AttributeError("there is no attribute or column '%s'" % key)

    def __repr__(self):
        def fill_to(s, l):
            if s is None:
                l1 = l // 2
                return " " * l1 + "-" + (" " * (l - l1 -1))
            elif type(s) in [float, int]:
                return ("%%%dg" % l) % s
            else:
                s = str(s)
                return s + " " * (l - len(s))
        columns = self._columns
        data = self._get_data_()[1:]
        max_lens = [len(col.caption) for col in columns]
        for item in data:
            lens = [len(str(x)) for x in item]
            for i in indices(max_lens):
                max_lens[i] = max(max_lens[i], lens[i])
        if sum(max_lens) < 20:
            for i in indices(max_lens):
                max_lens[i] += 1
        col_names = [fill_to(columns[i].caption, max_lens[i]) for i in indices(max_lens)]
        separator = "+%s+" % "+".join(["-" * m for m in max_lens])
        result = [separator, "|%s|" % "|".join(col_names), separator]
        for item in data:
            d = [fill_to(item[i], max_lens[i]) for i in indices(max_lens)]
            result.append("|%s|" % "|".join(d))
        result.append(separator)
        return "\n".join(result)
    __str__ = __repr__
    
    def sort(self):
        self._sort_by_(0)

    def select(self, **args):
        cols = { col.caption: col._index for col in self._columns }
        cols.update({ col._name: col._index for col in self._columns })
        def has_key(key):
            if key not in cols:
                if key.endswith("_min") or key.endswith("_max"):
                    return key[:-4] in cols
                else:
                    return False
            return True
        for key in args:
            if not has_key(key):
                raise KeyError("there is no column '%s'" % str(key))
        
        rows = [0]
        data = self._get_data_()
        for i in range(1, len(data)):
            row = data[i]
            include = True
            for key in args:
                if key in cols:
                    include = include and _conforms(args[key], row[cols[key]])
                else:
                    value = row[cols[key[:-4]]]
                    if value is None:
                        include = False
                    elif key.endswith("_min"):
                        include = include and args[key] <= value
                    elif key.endswith("_max"):
                        include = include and value <= args[key]
                    else:
                        include = False
            if include:
                rows.append(i)
        return TableView(self, rows)
    
    def find(self, **args):
        cols = { col.caption: col._index for col in self._columns }
        cols.update({ col._name: col._index for col in self._columns })
        for key in args:
            if key not in cols:
                raise KeyError("there is no column '%s'" % str(key))
        result = []
        data = self._get_data_()
        for i in range(1, len(data)):
            row = data[i]
            include = True
            for key in args:
                if key in cols:
                    include = include and _conforms(args[key], row[cols[key]])
                else:
                    include = False
            if include:
                result.append(self[i])
        return result

    def addFromInput(self):
        captions = [col.caption for col in self._columns]
        inp = multiInputAsList(captions)
        if inp is not None:
            return self.add(inp)
    appendFromInput = addFromInput
    
    def remove(self, *args, **kwargs):
        if len(args) > 0 and len(kwargs) == 0:
            for arg in args:
                if type(arg) is Row:
                    arg.delete()
                elif type(arg) is int:
                    del self[arg]
                else:
                    ValueError("remove(): cannot remove '%s'" % str(arg))
        elif len(args) == 0 and len(kwargs) > 0:
            rows = self.find(**kwargs)
            if len(rows) > 0:
                for row in rows:
                    row.delete()
            else:
                ValueError("remove(): no elements found")
        else:
            raise ValueError("remove(): invalid combination of arguments")
            
    @property
    def first(self):
        return self[1]
    
    @property
    def last(self):
        return self[-1]

    def save_as_excel(self, filename):
        import xlwt
        title_style = xlwt.easyxf('font: bold on')
        wb = xlwt.Workbook()
        try:
            name = self.table_name
            if name in ['', None]:
                name = 'Sheet 1'
        except:
            name = 'Sheet 1'
        ws = wb.add_sheet(name)
        data = self._get_data_()
        for i in indices(data[0]):
            ws.write(0, i, data[0][i], title_style)
        for j in range(1, len(data)):
            for i in indices(data[j]):
                value = data[j][i]
                if type(value) in [_Color]:
                    value = str(value)
                elif type(value) in [list]:
                    value = ", ".join([str(v) for v in value])
                ws.write(j, i, value)
        if not filename.endswith(".xls"):
            wb.save(filename + ".xls")
        else:
            wb.save(filename)
    saveAsExcel = save_as_excel

class TableView(BaseTable):
    
    def __init__(self, table, rows = None):
        self.table_name = ''
        self._table = table
        self._columns = [col.clone() for col in table._columns]
        for col in self._columns:
            col._table = self
        self._rows = []
        if rows is None:
            self._rows = range(0, len(table)+1)
        else:
            if 0 not in rows:
                rows.insert(0, 0)
            self._rows = rows
            
    def _add_row(self, row):
        if not row in self._rows:
            self._rows.append(row)
            
    def __len__(self):
        return len(self._rows)-1

    def __delitem__(self, key):
        if type(key) is int and 0 < key <= self.__len__():
            del self._rows[key]
    
    def _get_field_(self, row, col):
        return self._table._get_field_(self._rows[row], col)
    
    def _set_field_(self, row, col, value):
        self._table._set_field_(self._rows[row], col, value)
    
    def _get_data_(self):
        data = self._table._get_data_()
        return [data[row] for row in self._rows]
    
    def _sort_by_(self, index):
        rows = self._rows[1:]
        data = self._table._get_data_()
        rows.sort(key = lambda x: data[x][index])
        self._rows[1:] = rows
    
    def add(self, *data, **xdata):
        self._table.add(*data, **xdata)
    append = add
    
    def __getstate__(self):
        return False

class Table(BaseTable):
    
    def __init__(self, **columns):
        self._columns = []
        self._data = [[]]
        self.table_name = ''
        if len(columns) > 0:
            self.add_column(**columns)
    
    def add_column(self, **names):
        for key in names:
            for col in self._columns:
                if col._name == key:
                    return
            for item in self._data:
                item.append(None)
            index = len(self._columns)
            self._columns.append(Column(self, key, names[key], index))
            self._data[0][index] = names[key]
    addColumn = add_column
            
    def _key_to_col_index_(self, key):
        for col in self._columns:
            if col._name == key:
                return col._index
        for col in self._columns:
            if col.caption == key:
                return col._index
        raise KeyError("there is no column '%s'" % str(key))
        
    def _append_item_(self, item):
        data = self._data
        for i in range(1, len(data)):
            if data[i] == item:
                return self[i]
        data.append(item)
        return self.last
        
    def add(self, *data, **xdata):
        if len(data) == 1 and data[0] is None:
            return
        if len(data) == 1 and isinstance(data[0], Row):
            if len(self._columns) == 0 and len(self) == 0 and data[0]._table is not self:
                for orig_col in data[0]._table._columns:
                    col = orig_col.clone()
                    col._table = self
                    self._columns.append(col)
            data = data[0]
            cols = self._columns
            item = []
            for col in cols:
                item.append(data._get_or_none_(col._name))
            return self._append_item_(item)
        if len(data) == 1 and type(data[0]) in [list, tuple]:
            data = data[0]
        if len(data) == 1 and type(data[0]) is dict and len(xdata) == 0:
            return self.add(**data[0])
            
        col_count = len(self._columns)
        if len(data) == 0 and len(xdata) > 0:
            item = [None] * col_count
            for key in xdata:
                index = self._key_to_col_index_(key)
                item[index] = xdata[key]
            return self._append_item_(item)
        elif len(data) > 0 and len(xdata) == 0:
            def all_of_type(t):
                for item in data:
                    if type(item) != t and not isinstance(item, t):
                        return False
                return True
            if all_of_type(dict):
                result = None
                for item in data:
                    result = self.add(**item)
                return result
            elif all_of_type(list) or all_of_type(Row):
                result = None
                for item in data:
                    result = self.add(item)
                return result
            elif len(data) == col_count:
                return self._append_item_(data)
            elif len(data) < col_count:
                return self.add(list(data) + [None] * (col_count - len(data)))
            elif len(data) % col_count == 0:
                while len(data) > 0:
                    d = data[:col_count]
                    data = data[col_count:]
                    return self.add(d)
        else:
            raise ValueError("cannot add the given values to the table")
            
        return self._data[-1]
    append = add
    
    def _sort_by_(self, index):
        if 0 <= index < len(self._columns):
            data = self._data[1:]
            data.sort(key = lambda x: x[index])
            self._data[1:] = data
    
    def _get_data_(self):
        return self._data
    
    def __delitem__(self, key):
        if type(key) is int and 0 < key <= self.__len__():
            del self._data[key]
    
    def __iter__(self):
        rows = [Row(self, i) for i in range(1, len(self._data))]
        return iter(rows)
    
    def __getstate__(self):
        col_names = [col._name for col in self._columns]
        return (self.table_name, col_names, self._data)
    
    def __setstate__(self, state):
        name, col_names, data = state
        self.table_name = name
        self._data = data
        self._columns = []
        for i in indices(col_names):
            name = col_names[i]
            col = Column(self, name, self._data[0][i], i)
            self._columns.append(col)
        
def createTable(**columns):
    return Table(**columns)
#
# An example table for didactical purposes
#
_MOUNTAINS = [
    ["Name", "Land", "Hoehe"],
    ["Mount Everest", "Nepal", 8848],
    ["Aconcagua", "Argentinien", 6962],
    ["Kilimanjaro", "Tanzania", 5895],
    ["Elbrus", "Russland", 5642],
    ["Piz Bernina", "Schweiz", 4049],
    ["Saentis", "Schweiz", 2503],
    ["Mont Blanc", "Frankreich", 4808],
    ["Mauna Kea", "USA", 4205],
    ["Mount Rainier", "USA", 4393],
    ["K2", "Pakistan", 8611],
    ["Fuji", "Japan", 3776],
    ["Etna", "Italien", 3329],
    ["Piton de Neiges", "Frankreich", 3069],
    ["Monte Rosa", "Schweiz", 4634],
    ["Olympos", "Griechenland", 2919],
    ["Matterhorn", "Schweiz", 4478],
    ["Eiger", "Schweiz", 3970],
    ["Zugspitze", "Deutschland", 2962],
    ["Finsteraarhorn", "Schweiz", 4274],
    ["Dents du Midi", "Schweiz", 3257],
    ["Toedi", "Schweiz", 3614],
    ["Grossglockner", "Oesterreich", 3798],
    ["Wildspitze", "Oesterreich", 3768],
    ["Monte Viso", "Italien", 3841],
    ["Teide", "Spanien", 3718],
    ["Hvannadalshnukur", "Island", 2110],
    ["Gerlachovsky stit", "Slovakei", 2655],
    ["Adula", "Schweiz", 3402]
]
mountains = Table(name = "Name", land = "Land", hoehe = "Hoehe")
mountains.name.setIndex(0)
mountains.land.setIndex(1)
mountains.hoehe.setIndex(2)
mountains._data = _MOUNTAINS
#
# ===== PERSISTENCE INTERFACE =====
#
_databases = []

def _persistent_id(obj):
    if type(obj) is _Color:
        return "java.awt.Color#" + str(obj.getRGB())
    else:
        return None
    
def _persistent_load(obj_id):
    if obj_id.startswith("java.awt.Color#"):
        return _Color(int(obj_id[6:]))
    else:
        raise _pickle.UnpicklingError, "invalid persistent id"
    
class Database(dict):

    def __init__(self, name = None, **kwargs):
        dict.__init__(self)
        _databases.append(self)
        if name is None:
            name = getMainFileName()
        if name.endswith(".py"):
            name += "db"
        else:
            name += ".pydb"
        self._name = name
        self.__load()
        if len(kwargs) > 0:
            self.init(**kwargs)

    def __delattr__(self, key):
        del self[key]
        self._save()

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        return self[key]
    
    def __getitem__(self, key):
        if dict.__contains__(self, key):
            return dict.__getitem__(self, key)
        elif _path.isfile(key):
            return self.__getfile(key)
        else:
            raise KeyError, key
            
    def __getfile(self, filename):
        with open(filename) as f:
            result = f.readlines()
        return "".join(result)

    def __setattr__(self, key, value):
        if key in self.__dict__ or callable(value):
            self.__dict__[key] = value
        elif key in ["_name", "_pickler"]:
            dict.__setattr__(self, key, value)
        elif key not in ["isDefined", "hasVariable", "_save"]:
            self[key] = value

    def __setitem__(self, key, value):
        if key not in ["isDefined", "hasVariable", "_name", "_pickler", "_save"]:
            dict.__setitem__(self, key, value)
            self._save()

    def __load(self):
        name = self._name
        if _path.isfile(name):
            try:
                with open(name) as f:
                    pickler = _pickle.Unpickler(f)
                    pickler.persistent_load = _persistent_load
                    self.update(pickler.load())
            except:
                pass
            
    def isDefined(self, key):
        return key in self
    hasVariable = isDefined
    
    def init(self, **kwargs):
        for key in kwargs:
            if key not in self and key not in ["isDefined", "hasVariable", "_name", "_pickler", "_save"]:
                dict.__setitem__(self, key, kwargs[key])
        self._save()

    def _save(self):
        with open(self._name, "w") as f:
            pickler = _pickle.Pickler(f, _pickle.HIGHEST_PROTOCOL)
            pickler.persistent_id = _persistent_id
            pickler.dump(dict(self))
            
def _saveDataBase():
    for db in _databases:
        db._save()
        
registerFinalizeFunction(_saveDataBase)
#
#EOF