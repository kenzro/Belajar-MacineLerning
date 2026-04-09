def nasigoreng ():
    bahan= ["nasi", "telur", "bawang merah", "bawang putih", "kecap manis", "garam", "lada"]
    print("bahan bahan untuk membuat nasi goreng adalah ", bahan)

def miegoreng ():
    bahan= ["mie", "telur", "bawang merah", "bawang putih", "kecap manis", "garam", "lada"]
    print("bahan bahan untuk membuat mie goreng adalah ", bahan)

def telurpontianak ():
    bahan= ["telur", "bawang merah", "bawang putih", "kecap manis", "garam", "lada"]        
    print("bahan bahan untuk membuat telur pontianak adalah ", bahan[1])


while True:
    print("RESEP MASAKAN")
    print(" nama nama masakan: ")
    print(" 1. nasi goreng\n 2. mie goreng\n 3. telur pontianak")
    c= int(input(" masukan nama masakan ?"))
    if c != 1 and c != 2 and c != 3:
        print(" nama masakan tidak tersedia")
    elif c == 1:
        nasigoreng()
    elif c == 2:
        miegoreng()
    elif c == 3:
        telurpontianak()