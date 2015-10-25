with open('new_pass_names.txt') as f:
    for line in f:
        name = line.split()
        print("insert into users values ('%s', '1111', to_date('24-Oct-2015', 'DD-Mon-YYYY'));" % (name[0]+ " " + name[1])) 
