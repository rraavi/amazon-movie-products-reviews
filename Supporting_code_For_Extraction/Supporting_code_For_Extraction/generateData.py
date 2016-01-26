import operator
import collections
f = open("file_list.txt",'r')			#specify the path containing source files
f3 = open("IronMan_data.txt",'w')		#file opened in write mode to hold specific productID field data
f4 = open("Cars_data.txt",'w')
dict = {}
demo = []
for line in f:
    print line
    if len(line) >2:
        file_name = line[:-1]
        f_temp = open(file_name,'r')
        flag = 0
        for line_nested_file in f_temp:
            if flag ==1:
                if line_nested_file.find('product/productId:') == -1: 
                    f3.writelines(line_nested_file)
                else:
                    flag = 0
            if flag ==2:
                if line_nested_file.find('product/productId:') == -1:
                    f4.writelines(line_nested_file)
                else:
                    flag = 0
            if line_nested_file.find('product/productId:') > -1:
                review = line_nested_file[line_nested_file.find('product/productId:') + 19 : line_nested_file.find('product/productId:') + 29]
                if review == 'B001GAPC1K':
                    f3.writelines(line_nested_file)
                    flag = 1
                if review == 'B005ZMUQCK':
                    f4.writelines(line_nested_file)
                    flag = 2
f.close()
