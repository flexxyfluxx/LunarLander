#
# (c) 2017, Tobias Kohn
#
# LAST UPDATE: MAY-01-2017
#
from java.lang import Thread, Runtime
from java.util.concurrent import ConcurrentLinkedQueue, CyclicBarrier
from java.util.concurrent.atomic import AtomicInteger, AtomicBoolean
from time import sleep

class ReduceFunction:
    def __init__(self, name, f):
        self.name = name
        self.function = f
        
    def __repr__(self):
        return self.name

class REDUCE:
    MAX = ReduceFunction("MAX", lambda x, y: max(x, y))
    MIN = ReduceFunction("MAX", lambda x, y: min(x, y))
    SUM = ReduceFunction("SUM", lambda x, y: x + y)
    PROD = ReduceFunction("PRODUCT", lambda x, y: x*y)
    LAND = ReduceFunction("LOG AND", lambda x, y: x and y)
    LOR = ReduceFunction("LOG OR", lambda x, y: x or y)
    BAND = ReduceFunction("BIN AND", lambda x, y: x & y)
    BOR = ReduceFunction("BIN OR", lambda x, y: x | y)
    XOR = ReduceFunction("BIN XOR", lambda x, y: x ^ y)
    
    GATHER = ReduceFunction("GATHER", lambda x, y: (x, y))
    MERGE = ReduceFunction("MERGE", lambda x, y: _merge(x, y))

    ADD = SUM
    MULTIPLY = PROD
    
    names = {
        'max': MAX,
        'min': MIN,
        'sum': SUM,
        'add': SUM,
        '+': SUM,
        'prod': PROD,
        'mult': PROD,
        'multiply': PROD,
        '*': PROD,
        'and': BAND,
        'or': BOR,
        'gather': GATHER,
        'collect': GATHER,
        'merge': MERGE
    }

_tj_threads = []
_threads_by_id = {}
_threads_by_name = {}
_alive_threads = AtomicInteger(0)
_barrier = None

def _get_current_thread():
    return _threads_by_id[Thread.currentThread().id]

def _get_thread(name):
    if type(name) is int:
        if -1 <= name < len(_tj_threads):
            return _tj_threads[name]
        elif name == len(_tj_threads):
            return _tj_threads[0]
        else:
            raise TypeError("'%d' is not a valid rank for a thread" % name)
    elif type(name) is str and name in _threads_by_name:
        return _tj_threads[_threads_by_name[name]]
    elif name in ["main", "primary", "__main__", "0"]:
        return _tj_threads[0]
    elif type(name) is TJThread:
        return name
    else:
        raise TypeError("'%s' is not a valid identifier for a thread" % str(name))
        
def _get_name_or_null(rank):
    for name in _threads_by_name:
        if _threads_by_name[name] == rank:
            return name
    return None

def getRank():
    return _threads_by_id[Thread.currentThread().id].rank

def getRankCount():
    return len(_tj_threads)

def getName():
    return _threads_by_id[Thread.currentThread().id].name

class TJThread:
    
    def __init__(self, function, _reduce_mode = None):
        global _tj_threads
        self.rank = len(_tj_threads)
        self._function = function
        self._args = []
        self._kwargs = {}
        self._want_name = False
        self._want_rank = False
        self._msg_queue = ConcurrentLinkedQueue()
        self._msg_cache = []
        self._is_running = AtomicBoolean(False)
        self._reduce = _reduce_mode
        self.name = _get_name_or_null(self.rank)
        if self.rank > 0:
            self._thread = Thread(self._run)
            _threads_by_id[self._thread.id] = self
        else:
            _threads_by_id[Thread.currentThread().id] = self
        _tj_threads.append(self)
        try:
            argcount = function.__code__.co_argcount
            self.argcount = argcount
            if argcount > 0:
                first_param = function.__code__.co_varnames[-argcount]
                if "rank" in first_param:
                    self._want_rank = True
                    self.argcount -= 1
                elif "name" in first_param:
                    self._want_name = True
                    self.argcount -= 1
                self.has_varargs = function.__code__.varargs
                if self.has_varargs:
                    self.argcount += 1000000
        except:
            self._argcount = 0
            
    def start(self, args, kwargs):
        self._args = args
        self._kwargs = kwargs
        if self.rank > 0:
            self._thread.start()
        else:
            self._run()
            return self.result
    
    def _run(self):
        _alive_threads.incrementAndGet()
        self._is_running.set(True)
        try:
            if self._want_name and self.name is not None:
                result = self._function(self.name, *self._args, **self._kwargs)
            elif self._want_rank or len(self._args) < self.argcount:
                result = self._function(self.rank, *self._args, **self._kwargs)
            else:
                result = self._function(*self._args, **self._kwargs)
            self.result = result
            if self._reduce is REDUCE.GATHER:
                result = gather(result)
                if result is not None or self.rank == 0:
                    self.result = result
            elif self._reduce is not None:
                result = parallel_reduce(result, self._reduce)
                if result is not None or self.rank == 0:
                    self.result = result
        finally:
            _alive_threads.decrementAndGet()
            self._is_running.set(False)
    
    def _cache_messages(self):
        while not self._msg_queue.isEmpty():
            self._msg_cache.append(self._msg_queue.poll())
        return self._msg_cache
    
    def add_message(self, sender, msg):
        self._msg_queue.add((sender, msg))

    def _get_message(self):
        cache = self._cache_messages()
        if len(cache) > 0:
            return cache.pop(0)
        else:
            return None
                
    def _get_messages_ext(self, source_rank, predicate):
        cache = self._cache_messages()
        if len(cache) > 0 and source_rank is not None:
            result = [x for x in cache if x[0] == source_rank]
        else:
            result = cache
        if len(result) > 0 and predicate is not None:
            return [x for x in result if predicate(x[1])]
        else:
            return result

    def get_message(self, source_rank = None, predicate = None, wait = False):
        if source_rank is None and predicate is None:
            result = self._get_message()
            while wait and result is None:
                Thread.sleep(10)
                result = self._get_message()
            return result
        else:
            result = self._get_messages_ext(source_rank, predicate)
            while wait and len(result) == 0:
                Thread.sleep(10)
                result = self._get_messages_ext(source_rank, predicate)
            if len(result) > 0:
                x = result[0]
                self._msg_cache.remove(x)
                return x
            else:
                return None

    def has_message(self):
        cache = self._cache_messages()
        return len(cache) > 0
    
    @property
    def is_running(self):
        return self._is_running.get()
    
def _clear_threads():
    global _tj_threads, _threads_by_id, _thread_names
    if _alive_threads.get() == 0:
        _tj_threads = []
        _threads_by_id = {}
        _thread_names = {}
    return len(_tj_threads) == 0

def _wait_for_threads():
    Thread.sleep(1)
    while _alive_threads.get() > 0:
        Thread.sleep(1)
    for t in _tj_threads[1:]:
        while t.is_running:
            Thread.sleep(10)
        
def _init_parallels(threadCount):
    _clear_threads()
    _barrier = CyclicBarrier(threadCount)
    _start_parallels(threadCount)
    
def _finalize_parallels():
    _stop_parallels()

def _create_parallel_function(threadCount, reduce_function, function, distribute = False):
    def call_functions(*args, **kwargs):
        _init_parallels(threadCount)
        _threads = []
        for r in range(threadCount):
            _threads.append(TJThread(function, reduce_function))
        total_argcount = sum([t.argcount for t in _threads])
        if len(args) > 0 and total_argcount == len(args):
            arguments = []
            for t in _threads:
                arguments.append(args[:t.argcount])
                args = args[t.argcount:]
            i = len(_threads)-1
            while i >= 0:
                _threads[i].start(arguments[i], kwargs)
                i -= 1
        else:
            for t in reversed(_threads):
                t.start(args, kwargs)
        _wait_for_threads()
        _finalize_parallels()
        return _threads[0].result
    
    def call_functions_dist(*args, **kwargs):
        _init_parallels(threadCount)
        _threads = []
        for r in range(threadCount):
            _threads.append(TJThread(function, reduce_function))
        #total_argcount = sum([t.argcount for t in _threads])
        if len(args) > 0:
            arguments = []
            for arg in args:
                arguments.append(_distribute(threadCount, arg))
            i = len(_threads)-1
            while i >= 0:
                _threads[i].start([arg[i] for arg in arguments], kwargs)
                i -= 1
        else:
            for t in reversed(_threads):
                t.start(args, kwargs)
        _wait_for_threads()
        _finalize_parallels()
        return _threads[0].result

    if distribute:
        return call_functions_dist
    else:
        return call_functions

def _create_parallel_functions(reduce_function, *functions):
    def call_functions(*args, **kwargs):
        _init_parallels(len(functions))
        _threads = []
        for f in functions:
            _threads.append(TJThread(f, reduce_function))
        for t in reversed(_threads):
            t.start(args)
        _wait_for_threads()
        _finalize_parallels()
        return _threads[0].result
    return call_functions

def _all_callable(args):
    """Check if all items in the given sequence are callable."""
    for arg in args:
        if not callable(arg):
            return False
    return True

def _set_names(names, threadCount = 0):
    global _threads_by_name
    if names is not None:
        if threadCount > 0 and len(names) != threadCount:
            raise TypeError("parallel(): is 'names' are given, each thread must have a unique name")
        for i in indices(names):
            name = names[i]
            if name in _threads_by_name:
                raise TypeError("parallel(): two threads cannot share a common name '%s'" % name)
            else:
                _threads_by_name[name] = i
        return True
    else:
        return False

def parallel(*args, **kwargs):
    names = None
    _reduce_mode = None
    _scatter = False
    if len(kwargs) > 0:
        for key in kwargs:
            if key == "names":
                names = kwargs[key]
            elif key in ["reduce", "reduceMode", "reduce_mode", "reduce_function"]:
                if kwargs[key] == True:
                    _reduce_mode = REDUCE.GATHER
                elif kwargs[key] == False:
                    _reduce_mode = None
                else:
                    _reduce_mode = kwargs[key]
            elif key == "scatter":
                if kwargs[key]:
                    _scatter = True
            elif key == "distribute":
                if kwargs[key]:
                    _scatter = True
                    if _reduce_mode is None:
                        _reduce_mode = REDUCE.GATHER
            elif key == "gather":
                if kwargs[key]:
                    _reduce_mode = REDUCE.GATHER
            else:
                raise TypeError("parallel() got an unexpected keyword argument '%s'" % key)
    if len(args) == 0:
        keyargs = kwargs
        if _set_names(names):
            threadCount = len(names)
            del keyargs['names']
        else:
            threadCount = Runtime.getRuntime().availableProcessors()
        return parallel(threadCount, **keyargs)
    elif len(args) == 1 and type(args[0]) is int:
        _set_names(names, args[0])
        def _p(f):
            return _create_parallel_function(args[0], _reduce_mode, f, distribute = _scatter)
        return _p
    elif len(args) == 1 and isinstance(args[0], ReduceFunction):
        if _set_names(names):
            threadCount = len(names)
        else:
            threadCount = Runtime.getRuntime().availableProcessors()
        return parallel(threadCount, reduce = args[0], distribute = _scatter)
    elif len(args) == 1 and callable(args[0]):
        if _set_names(names):
            threadCount = len(names)
        else:
            threadCount = Runtime.getRuntime().availableProcessors()
        return _create_parallel_function(threadCount, _reduce_mode, args[0], distribute = _scatter)
    elif len(args) == 2 and type(args[0]) is int and callable(args[1]):
        _set_names(names, args[0])
        return _create_parallel_function(args[0], _reduce_mode, args[1], distribute = _scatter)
    elif len(args) == 2 and type(args[1]) is int and callable(args[0]):
        _set_names(names, args[1])
        return _create_parallel_function(args[1], _reduce_mode, args[0], distribute = _scatter)
    elif len(args) == 2 and type(args[0]) is int and isinstance(args[1], ReduceFunction):
        return parallel(args[0], reduce = args[1], distribute = _scatter)
    elif _all_callable(args):
        _set_names(names, len(args))
        return _create_parallel_functions(*args)
    else:
        raise TypeError("parallel() got too many arguments")

def send(rank, value):
    if not isinstance(rank, basestring) and hasattr(rank, "__getitem__"):
        for r in rank:
            sendTo(r, value)
    else:
        thread = _get_thread(rank)
        thread.add_message(getRank(), value)
    
def broadcast(value):
    rank = getRank()
    for thread in _tj_threads:
        thread.add_message(rank, value)

def receive(source_rank = None, wait = False):
    thread = _get_current_thread()
    print "Current Thread: %d" % thread.rank
    return thread.get_message(source_rank = source_rank, wait = wait)

_start_parallel_functions = []
_stop_parallel_functions  = []

def registerStartParallel(f):
    _start_parallel_functions.append(f)
    
def registerStopParallel(f):
    _stop_parallel_functions.append(f)

def removeStartParallel(f):
    if f in _start_parallel_functions:
        _start_parallel_functions.remove(f)
    
def removeStopParallel(f):
    if f in _stop_parallel_functions:
        _stop_parallel_functions.remove(f)

def _start_parallels(threadCount):
    for f in _start_parallel_functions:
        f(threadCount)

def _stop_parallels():
    for f in _stop_parallel_functions:
        f()

def barrier():
    if _barrier is not None:
        _barrier.await()
    
_reduce_stack = ConcurrentLinkedQueue()
_reduce_count = AtomicInteger(0)
_reduce_result = None
_reduce_has_result = AtomicBoolean(False)

def parallel_reduce(value, reduce_function, wait = False):
    global _reduce_result
    if reduce_function is None:
        return value
    if reduce_function == sum:
        reduce_function = lambda x, y: x + y
    if type(reduce_function) in [str, unicode]:
        s = reduce_function.lower()
        if s in REDUCE.names:
            reduce_function = REDUCE.names[s]
    if isinstance(reduce_function, ReduceFunction):
        reduce_function = reduce_function.function
    rank = getRank()
    if rank == 0:
        _reduce_result = None
        _reduce_has_result.set(False)
    tos = _reduce_stack.poll()
    while tos is not None:
        value = reduce_function(value, tos)
        tos = _reduce_stack.poll()
    if rank == 0:
        rankCount = getRankCount()-1
        while _reduce_count.get() < rankCount:
            tos = _reduce_stack.poll()
            if tos is not None:
                value = reduce_function(value, tos)
            else:
                Thread.sleep(1)
        while not _reduce_stack.isEmpty():
            value = reduce_function(value, _reduce_stack.poll())
        _reduce_count.set(0)
        _reduce_result = value
        _reduce_has_result.set(True)
        return value
    else:
        _reduce_stack.add(value)
        _reduce_count.incrementAndGet()
        while wait and not _reduce_has_result.get():
            Thread.sleep(10)
        if _reduce_has_result.get():
            return _reduce_result
        else:
            return None

def _distribute(threadCount, arg):
    try:
        result = []
        fullCount = len(arg) % threadCount
        if fullCount == 0:
            fullCount = threadCount
        partLen = (len(arg) + threadCount - 1) // threadCount
        for i in range(fullCount):
            start = i * partLen
            result.append(arg[start:start + partLen])
        start = fullCount * partLen
        partLen -= 1
        while len(result) < threadCount:
            result.append(arg[start:start + partLen])
            start += partLen
        return result
    except:
        return [arg] * threadCount
    
def scatter(data):
    if hasattr(data, '__len__'):
        rank = getRank()
        rankCount = getRankCount()
        if len(data) >= rankCount:
            partLen = (len(data) + rankCount - 1) // rankCount
            start = rank * partLen
            return data[start:start + partLen]
        elif 0 <= rank < len(data):
            return data[rank:rank+1]
        else:
            return []
    else:
        raise ValueError("scatter(): argument must be a list or string")

_gather_stack = ConcurrentLinkedQueue()
_gather_result = None
_gather_has_result = AtomicBoolean(False)

def gather(data, wait = False):
    global _gather_result
    if hasattr(data, '__len__'):
        _gather_has_result.set(False)
        rank = getRank()
        if rank == 0:
            rankCount = getRankCount()
            _gather_stack.add((rank, data))
            while _gather_stack.size() < rankCount:
                Thread.sleep(1)
            result = [[]] * rankCount
            while not _gather_stack.isEmpty():
                (r, value) = _gather_stack.poll()
                result[r] = value
            _gather_result = [x for item in result for x in item]
            _gather_has_result.set(True)
            return _gather_result
        else:
            _gather_stack.add((rank, data))
            while wait and not _gather_has_result.get():
                Thread.sleep(10)
            if _gather_has_result.get():
                return _gather_result
            else:
                return None
    else:
        return gather([data])

def _merge(a, b):
    if type(a) is dict and type(b) is dict:
        result = a.copy()
        result.update(b)
        return result
    elif hasattr(a, '__getitem__') and hasattr(b, '__getitem__'):
        result = [0] * (len(a) + len(b))
        i_a = 0
        i_b = 0
        i_r = 0
        while i_a < len(a) and i_b < len(b):
            if a[i_a] <= b[i_b]:
                result[i_r] = a[i_a]
                i_a += 1
            else:
                result[i_r] = b[i_b]
                i_b += 1
            i_r += 1
        while i_a < len(a):
            result[i_r] = a[i_a]
            i_r += 1; i_a += 1
        while i_b < len(b):
            result[i_r] = b[i_b]
            i_r += 1; i_b += 1
        return result
    else:
        raise TypeError("merge(): arguments must both be dicts or lists of equal length")

if __name__ == "__main__":
    
    @parallel(4, distribute = True)
    def f(rank, L):
        print L
        return [x + 'X' for x in L]
        
    print f(['A', 'B', 'C', 'D', 'E', 'F'])
    print "=" * 40 + "\n\n"
    sleep(.5)

    @parallel(10, reduce = REDUCE.SUM)
    def s(rank):
        print "Hello from %d" % rank
        return rank + 1
#        if rank == 0:
#            value = parallel_reduce(1, REDUCE.SUM)  # lambda x, y: x + y
#            return value
#        else:
#            parallel_reduce(rank+1, REDUCE.SUM)  # lambda x, y: x + y

    @parallel(32)
    def s(rank):
        print "Hello from %d" % rank
        if rank == 0:
            value = parallel_reduce(1, lambda x, y: x + y)
            return value
        else:
            parallel_reduce(rank+1, lambda x, y: x + y)

    @parallel
    def g(rank, numbers):
        data = scatter(numbers)
        data = [x**2 for x in data]
        if rank == 0:
            value = gather(data)
            print value
            print sorted(value)
        else:
            gather(data)

    result = s()
    print "The overall sum is", result
    
    g(list(range(100)))
    print "The entire array has been squared!"
    print "Done"
