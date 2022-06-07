nest_li = [[1,2],[3,4],[5,6],[7,8]]

def unzip(zipped):
    return zip(*zipped)

print(unzip(nest_li))