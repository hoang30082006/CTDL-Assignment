# Day con tang dai nhat (Quy hoach dong) - Tep thu loi (Da khoi phuc)
A = [3, 10, 7, 20, 12, 4, 21, 1, 2]

def day_con_tang(a):
    n = len(a)
    f = [1] * n
    vet = [-1] * n
    
    print("Day xet:", " ".join(map(str, a)))
    for i in range(n):
        for j in range(i):
            if a[j] < a[i] and f[j] + 1 > f[i]:
                f[i] = f[j] + 1
                vet[i] = j  # DA KHOI PHUC DONG NAY (XOA DAU #)
        tu_str = f"{vet[i] + 1}" if vet[i] != -1 else "khong"
        print(f"i = {i + 1}: a = {a[i]}, f = {f[i]}, tu = {tu_str}")
                
    max_len = max(f)
    idx = f.index(max_len)
    
    day = []
    while idx != -1:
        day.append(a[idx])
        idx = vet[idx]
    day.reverse()
    
    return max_len, day

def main():
    print("MSSV: N24DCDT027 | Ma ca: 1")
    print("Nhap n (1..9), so phan tu dau tien cua day duoc xet:")
    try:
        n = int(input().strip())
    except (ValueError, EOFError):
        print("Du lieu khong hop le.")
        return
    if not 1 <= n <= 9:
        print("Du lieu khong hop le.")
        return
        
    sub_A = A[:n]
    do_dai, day = day_con_tang(sub_A)
    print("Do dai day con tang dai nhat:", do_dai)
    print("Mot day con tang dai nhat:", " ".join(map(str, day)))

if __name__ == "__main__":
    main()