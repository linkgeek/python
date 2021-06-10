def write_txt():
    f = open("D:/Code/python/data/test.txt", 'r+')
    txt = f.readlines(1)
    f.write('\n11111111111')
    f.close()
    print(txt)


def main():
    write_txt()


if __name__ == '__main__':
    main()
