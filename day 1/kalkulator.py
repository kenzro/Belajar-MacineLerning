while True:
    print("KALKULATOR BAHAN MAKANAN")
    print(" nama nama bahan makanan: ")
    print(" 1. Beras")
    print(" 2. Gula")
    print(" 3. Minyak")
    print(" 4. Garam")
    a= int(input(" masukan nama bahan makanan ?"))
    b= int(input(" masukan jumlah per kilo bahan makanan ?"))
    c=[]
    g=[]
    m=[]
    r=[]
    if a != 1 and a != 2 and a != 3 and  a != 4:
        print(" nama bahan makanan tidak tersedia")
    elif a == 1:
        c.append(b)
        c=c
        print(" total stok beras adalah ", sum(c))
    elif a == 2:
        g.append(b)
        g=g 
        print(" total stok gula adalah ", sum(g))
    elif a == 3:
        m.append(b)
        m=m
        print(" total stok minyak adalah ", sum(m))
    elif a == 4:
        r.append(b)
        r=r
        print(" total stok garam adalah ", sum(r))
    