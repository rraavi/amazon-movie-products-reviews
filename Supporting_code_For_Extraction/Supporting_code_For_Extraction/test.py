import operator
import collections
f = open("file_list.txt",'r')		#specify the path containing the source files
dict = {}
demo = []
for line in f:
    print line
    if len(line) >2:
        file_name = line[:-1]
        f_temp = open(file_name,'r')
        for line_nested_file in f_temp:
            if line_nested_file.find('product/productId:') > -1:
                review = line_nested_file[line_nested_file.find('product/productId:') + 19 : line_nested_file.find('product/productId:') + 29]
                if review in dict:
                    dict[review] += 1
                else:
                    dict[review] = 1
print collections.Counter(dict).most_common(20)			#prints 20 most common items from the collection
f.close()
