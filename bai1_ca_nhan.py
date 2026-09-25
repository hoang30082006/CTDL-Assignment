# Luy thua nhanh (chia de tri): tinh A^n mod M, in lan vet tung loi goi.
A = 10        # co so
M = 1009      # modulo
so_goi = 0    # so loi goi de quy (khong ke loi goi ngoai cung)
so_le = 0     # so buoc gap n le
so_nhan = 0   # so phep nhan da thuc hien

def luy_thua(n: int) -> int:
    global so_goi, so_le, so_nhan
    if n == 0:
        print("n = 0: co so, tra ve 1")
        return 1 % M
    
    so_goi += 1
    nua = luy_thua(n // 2)      # chi goi de quy MOT lan
    kq = nua * nua % M
    so_nhan += 1               # dem phep nhan nua * nua
    
    if n % 2 == 1: 
        so_le += 1
    if n % 2 == 1: 
        kq = kq * A % M
        so_nhan += 1           # dem phep nhan voi A khi n le
        
    print(f"n = {n} ({'le' if n % 2 == 1 else 'chan'}): nua = {nua}, "
          f"binh phuong mod M = {nua * nua % M}, tra ve {kq}")
    return kq

def main():
    print("MSSV: N24DCDT027 | Ma ca: 1")
    print("Nhap n (0..60):")
    try:
        n = int(input().strip())
    except (ValueError, EOFError):
        print("Du lieu khong hop le.")
        return
    if not 0 <= n <= 60:
        print("Du lieu khong hop le.")
        return
        
    kq = luy_thua(n)
    print(f"Ket qua: {A}^{n} mod {M} = {kq}")
    print("So loi goi de quy:", so_goi)
    print("So buoc n le:", so_le)
    print("So phep nhan:", so_nhan)

if __name__ == "__main__":
    main()