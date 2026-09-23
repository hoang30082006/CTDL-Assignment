BAN = "Đáp án"
from cau_truc import DSLK, NganXep, HangDoiVong, so_nguyen


def dem_gia_tri(L: DSLK, x: int) -> int:
    """Đếm số nút có gt == x bằng cách duyệt các liên kết; không đổi L."""
    x = so_nguyen(x)
    dem, p = 0, L.dau
    while p is not None:
        if p.gt == x:
            dem += 1
        p = p.ke
    return dem


def xoa_tat_ca(L: DSLK, x: int) -> int:
    """Xoá mọi nút có gt == x bằng một lượt duyệt, trả về số nút đã xoá."""
    x = so_nguyen(x)
    dem = 0
    truoc, p = None, L.dau
    while p is not None:
        sau = p.ke
        if p.gt == x:
            if truoc is None:
                L.dau = sau
            else:
                truoc.ke = sau
            L.n -= 1
            dem += 1
            # Giữ nguyên truoc: nút còn lại đứng trước không thay đổi.
        else:
            truoc = p
        p = sau
    return dem


def lay_nhieu(s: NganXep, k: int) -> list[int]:
    """Lấy đúng k giá trị theo thứ tự LIFO; k không hợp lệ thì không sửa s."""
    if type(k) is not int or not 0 <= k <= len(s.a):
        raise ValueError("k phải là số nguyên từ 0 đến số phần tử ngăn xếp.")
    result: list[int] = []
    for _ in range(k):
        result.append(s.lay())
    return result


def xem_k(q: HangDoiVong, k: int) -> list[int]:
    """Trả về k phần tử đầu theo FIFO, không đổi a, dau, so hoặc n."""
    if type(k) is not int or not 0 <= k <= q.so:
        raise ValueError("k phải là số nguyên từ 0 đến số phần tử hàng đợi.")
    result: list[int] = []
    for i in range(k):
        result.append(q.a[(q.dau + i) % q.n])
    return result
