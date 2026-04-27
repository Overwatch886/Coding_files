def  change_list_to_string(list) : 
    if len(list) == 0 : 
        print(' ')
    else :
        for i in range(len(list)-1) : 
            print(list[i], end=', ')
        last_term = my_list[len(my_list)-1]
        print ('and ' + str(last_term))
my_list = ['apples', 'bananas', 'oranges', 'mangoes', 5]
#my_list= [ ]
change_list_to_string(my_list)
