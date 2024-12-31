sku_list = [7046538, 8289407, 9056375, 2308597]

# Write your code below:
print(dir(sku_list))

# usando metodo __iter__()
sku_iterator_object_one = sku_list.__iter__()
print(sku_iterator_object_one)

# usando funcion iter()
sku_iterator_object_two = iter(sku_list)
print(sku_iterator_object_two)

#both objects are the same and should print the same memory address result 