def group_lists(list, grouping: int):
    output = []
    group = []

    #I dunno why I had to subtract -1 from grouping and count to get this to work
    count = -1
    for ele in list:
        if count == grouping-1:
            output.append(group)
            group = []
            count = 0
            group.append(ele)
        else:
            count += 1
            group.append(ele)
    
    if group != []:
        output.append(group)
    
    return output
    
if __name__ == '__main__':
    test_list = list(range(22))
    print(test_list)
    print(group_lists(test_list,2))