a=["kopi","teh","susu","roti","kue"]
b=[10000,5000,15000,2000,3000]
while True:
    print("KASIR TOKO MAKANAN")
    print(" nama nama makanan: ")
    print(" 1. kopi\n 2. teh\n 3. susu\n 4. roti\n 5. kue")
    c= int(input(" masukan nama makanan ?"))
    d= int(input(" masukan jumlah makanan ?"))
    if c != 1 and c != 2 and c != 3 and  c != 4 and c != 5:
        print(" nama makanan tidak tersedia")
    elif c == 1:
        jum=b[0]*d
        if jum< 40000:
            print(" total harga kopi adalah ", jum)
        else:
            diskon=jum*0.1
            total=jum-diskon
            print(" total harga kopi adalah ", total)
    elif c == 2:
        jum=b[1]*d
        if jum< 20000:
            print(" total harga teh adalah ", jum)
        else:
            diskon=jum*0.1
            total=jum-diskon
            print(" total harga teh adalah ", total)
    elif c == 3:
        jum=b[2]*d
        if jum< 50000:
            print(" total harga susu adalah ", jum)
        else:
            diskon=jum*0.1
            total=jum-diskon
            print(" total harga susu adalah ", total)
    elif c == 4:
        jum=b[3]*d
        if jum< 10000:
            print(" total harga roti adalah ", jum)
        else:
            diskon=jum*0.1
            total=jum-diskon
            print(" total harga roti adalah ", total)
    elif c == 5:
        jum=b[4]*d
        if jum< 15000:
            print(" total harga kue adalah ", jum)
        else:
            diskon=jum*0.1
            total=jum-diskon
            print(" total harga kue adalah ", total)