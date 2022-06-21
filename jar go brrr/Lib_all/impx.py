import sys
def reload(mod):
    del sys.modules[mod]
    import mod

