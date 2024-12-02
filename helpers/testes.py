def float_to_currency(x):
    new = str(x).replace('.',',')
    if new.find(',')>0:
        [main, end] = new.split(',')
    else:
        [main, end] = [new, '']
    new = []
    if len(main)%3 > 0:
        new.append(main[:len(main)%3])
        main = main[len(main)%3:]
    while len(main) > 0:
        new.append(main[:3])
        main = main[3:]
    while len(end)<2:
        end = end+'0'
    return '.'.join(new)+','+end

print(float_to_currency(302080.00))