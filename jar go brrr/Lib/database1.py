# tigerjython/database1.py
#
# (c) 2017, Tobias Kohn
#
# UPDATED: MARCH-17-2018
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

    def __init__(self, table, name, index):
        self._table = table
        self._index = index
        self._name = name
        
    def clone(self):
        return Column(self._table, self._name, self._index)
    
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
        
    def _get_data_(self):
        return [row[self._index] for row in self._table._get_data_()]
    
    def __iter__(self):
        return iter(self._get_data_())
        
    def __repr__(self):
        return repr(self._get_data_())
    
    def __str__(self):
        return str(self._get_data_())

    @property
    def caption(self):
        return self._name

    @property
    def first(self):
        return self[0]
    
    @property
    def last(self):
        return self[-1]
    

class Row(object):
    
    def __init__(self, table, index):
        self._table = table
        self._index = index
        self._data = None
    
    def __getitem__(self, key):
        if self._data is None:
            return self._table.__getitem__((self._index, key))
        else:
            if type(key) is str:
                index = self._table._colname_to_index_(key)
            elif type(key) is int:
                index = key
            else:
                raise KeyError("there is no column: '%s'" % repr(key))
            return self._data[index]
    
    def __len__(self):
        if self._data is None:
            return len(self._table._columns)
        else:
            return len(self._data)
    
    def __setitem__(self, key, value):
        if self._data is None:
            self._table.__setitem__((self._index, key), value)
        else:
            index = self._table._colname_to_index_(key)
            self._data[index] = value

    def _get_data_(self):
        if self._data is None:
            return self._table._get_data_()[self._index]
        else:
            return self._data

    def _get_or_none_(self, col):
        columns = [c.caption for c in self._table._columns]
        columns_l = [c.lower() for c in columns]
        if col in columns:
            i = columns.index(col)
            return self.__getitem__(i)
        elif col.lower() in columns_l:
            i = columns_l.index(col.lower())
            return self.__getitem__(i)
        else:
            return None
        
    def _get_cache_(self):
        if self._data is None:
            self._data = self._get_data_()
            
    def delete(self):
        self._get_cache_()
        del self._table[self._index]
    remove = delete
    drop = delete
    
    def __iter__(self):
        values = self._table._get_data_()[self._index]
        return iter(values)
    
    def __repr__(self):
        return repr(self._get_data_())
    
    def __str__(self):
        return str(self._get_data_())


class BaseTable(object):
    
    def _colname_to_index_(self, name):
        for col in self._columns:
            if col._name == name:
                return col._index
        for col in self._columns:
            if col._name.lower() == name.lower():
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
        return len(self._get_data_())
    
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
            if 0 <= key < len(self):
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
        data = self._get_data_()
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

    def addFromInput(self):
        captions = [col.caption for col in self._columns]
        inp = multiInputAsList(captions)
        if inp is not None:
            return self.add(inp)
    appendFromInput = addFromInput
    
    def remove(self, *args):
        if len(args) > 0:
            if len(args) == 1 and isinstance(args[0], Row):
                args[0].delete()
                return
            else:
                for j in indices(self._data):
                    item = self._data[j]
                    if all([args[i] == item[i] for i in indices(args)]):
                        del self._data[j]
                        return
            raise ValueError("remove(): could not remove '%s'" % repr(args))

    @property
    def first(self):
        return self[0]
    
    @property
    def last(self):
        return self[-1]


class Table(BaseTable):
    
    def __init__(self, *columns):
        self._columns = []
        self._data = []
        self.table_name = ''
        if len(columns) > 0:
            for column in columns:
                self.add_column(column)
    
    def add_column(self, name):
        for col in self._columns:
            if col._name == name:
                return
        index = len(self._columns)
        self._columns.append(Column(self, name, index))
        for item in self._data:
            if len(item) <= index:
                item.append(None)
    addColumn = add_column
            
    def _key_to_col_index_(self, key):
        for col in self._columns:
            if col._name == key:
                return col._index
        for col in self._columns:
            if col._name.lower() == key.lower():
                return col._index
        raise KeyError("there is no column '%s'" % str(key))
        
    def _append_item_(self, item):
        self._data.append(list(item))
        return self.last
        
    def add(self, *data):
        if len(data) == 1 and data[0] is None:
            return None
        
        elif len(data) == 1 and isinstance(data[0], Row):
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
        
        elif len(data) == 1 and type(data[0]) in (list, tuple):
            data = data[0]
            
        col_count = len(self._columns)
        if len(data) > 0:
            def all_of_type(t):
                for item in data:
                    if type(item) != t and not isinstance(item, t):
                        return False
                return True
            
            if all([type(item) is list for item in data]) or all([isinstance(item, Row) for item in data]):
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
            data = self._data
            data.sort(key = lambda x: x[index])
            self._data = data
    
    def _get_data_(self):
        return self._data
    
    def __delitem__(self, key):
        if type(key) is int and 0 <= key < self.__len__():
            del self._data[key]
    
    def __iter__(self):
        rows = [Row(self, i) for i in range(len(self._data))]
        return iter(rows)
    
    def __getstate__(self):
        col_names = [col._name for col in self._columns]
        state = (self.table_name, col_names, self._data)
        return state
    
    def __setstate__(self, state):
        name, col_names, data = state
        self.table_name = name
        self._data = data
        self._columns = []
        for name in col_names:
            self.add_column(name)
        self._data = data
            
        
def createTable(*columns):
    return Table(*columns)
#
# An example table for didactical purposes
#
_MOUNTAINS_DE = [
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
    ["Gerlachovsky stit", "Slowakei", 2655],
    ["Adula", "Schweiz", 3402]
]
_mountains_de = Table("Name", "Land", "Hoehe")
_mountains_de._data = _MOUNTAINS_DE
#
_MOUNTAINS_EN = [
    ["Mount Everest", "Nepal", 8848],
    ["Aconcagua", "Argentinia", 6962],
    ["Kilimanjaro", "Tanzania", 5895],
    ["Elbrus", "Russia", 5642],
    ["Piz Bernina", "Switzerland", 4049],
    ["Saentis", "Switzerland", 2503],
    ["Mont Blanc", "France", 4808],
    ["Mauna Kea", "USA", 4205],
    ["Mount Rainier", "USA", 4393],
    ["K2", "Pakistan", 8611],
    ["Fuji", "Japan", 3776],
    ["Etna", "Italy", 3329],
    ["Piton de Neiges", "France", 3069],
    ["Monte Rosa", "Switzerland", 4634],
    ["Olympos", "Greece", 2919],
    ["Matterhorn", "Switzerland", 4478],
    ["Eiger", "Switzerland", 3970],
    ["Zugspitze", "Germany", 2962],
    ["Finsteraarhorn", "Switzerland", 4274],
    ["Dents du Midi", "Switzerland", 3257],
    ["Toedi", "Switzerland", 3614],
    ["Grossglockner", "Austria", 3798],
    ["Wildspitze", "Austria", 3768],
    ["Monte Viso", "Italy", 3841],
    ["Teide", "Spain", 3718],
    ["Hvannadalshnukur", "Island", 2110],
    ["Gerlachovsky stit", "Slovakia", 2655],
    ["Adula", "Switzerland", 3402]
]
_mountains_en = Table("Name", "Country", "Height")
_mountains_en._data = _MOUNTAINS_EN
#
_MOUNTAINS_FR = [
    ["Mount Everest", "Nepal", 8848],
    ["Aconcagua", "Argentine", 6962],
    ["Kilimanjaro", "Tanzania", 5895],
    ["Elbrus", "Russie", 5642],
    ["Piz Bernina", "Suisse", 4049],
    ["Saentis", "Suisse", 2503],
    ["Mont Blanc", "France", 4808],
    ["Mauna Kea", "USA", 4205],
    ["Mount Rainier", "USA", 4393],
    ["K2", "Pakistan", 8611],
    ["Fuji", "Japon", 3776],
    ["Etna", "Italie", 3329],
    ["Piton de Neiges", "France", 3069],
    ["Monte Rosa", "Suisse", 4634],
    ["Olympos", "Grece", 2919],
    ["Matterhorn", "Suisse", 4478],
    ["Eiger", "Suisse", 3970],
    ["Zugspitze", "Allemagne", 2962],
    ["Finsteraarhorn", "Suisse", 4274],
    ["Dents du Midi", "Suisse", 3257],
    ["Toedi", "Suisse", 3614],
    ["Grossglockner", "Autriche", 3798],
    ["Wildspitze", "Autriche", 3768],
    ["Monte Viso", "Italie", 3841],
    ["Teide", "Espagne", 3718],
    ["Hvannadalshnukur", "Islande", 2110],
    ["Gerlachovsky stit", "Slovaquie", 2655],
    ["Adula", "Suisse", 3402]
]
_mountains_fr = Table("Nom", "Pays", "Altitude")
_mountains_fr._data = _MOUNTAINS_FR
#
#
#
try:
    _lang = getTigerJythonFlag("language")
    if _lang == "de":
        mountains = _mountains_de
    elif _lang == "fr":
        mountains = _mountains_fr
    else:
        mountains = _mountains_en
    del _lang
except:
    pass
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
