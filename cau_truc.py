"""Chương 5: thuật toán cơ bản, độc lập với giao diện.

Đầu vào: số nguyên trong [-1_000_000, 1_000_000].
Danh sách dùng nút thật (gt, ke), không dùng list để thay thế các liên kết.
Ngăn xếp dùng mảng động; hàng đợi dùng mảng cố định và chỉ số vòng.
Tên biến theo mục 5.3, 5.4 và 5.5 của tài liệu học phần.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable


def so_nguyen(x: object, ten: str = "Giá trị") -> int:
    if type(x) is not int or not -1_000_000 <= x <= 1_000_000:
        raise ValueError(f"{ten} phải là số nguyên từ -1000000 đến 1000000.")
    return x


@dataclass(eq=False, slots=True)
class Nut:
    gt: int
    ke: Nut | None = None


class DSLK:
    def __init__(self, values: Iterable[int] = ()) -> None:
        self.dau: Nut | None = None
        self.n = 0
        for x in values:
            self.them_cuoi(x)

    def them_dau(self, gt: int) -> None:
        gt = so_nguyen(gt)
        self.dau = Nut(gt, self.dau)
        self.n += 1

    def them_cuoi(self, gt: int) -> None:
        m = Nut(so_nguyen(gt))
        if self.dau is None:
            self.dau = m
        else:
            p = self.dau
            while p.ke is not None:
                p = p.ke
            p.ke = m
        self.n += 1

    def tim(self, gt: int) -> Nut | None:
        """Trả về nút đầu tiên có giá trị gt; không thấy thì trả về None."""
        gt = so_nguyen(gt)
        p = self.dau
        while p is not None and p.gt != gt:
            p = p.ke
        return p

    def chen_sau(self, p: Nut, gt: int) -> Nut:
        """Điều kiện: p là một nút của danh sách, thường lấy bằng tim()."""
        if p is None:
            raise ValueError("Cần một nút hợp lệ để chèn sau.")
        m = Nut(so_nguyen(gt), p.ke)  # Giữ phần đuôi trước khi đổi p.ke.
        p.ke = m
        self.n += 1
        return m

    def xoa(self, gt: int) -> bool:
        """Chỉ xoá lần xuất hiện đầu tiên; trả về có xoá được hay không."""
        gt = so_nguyen(gt)
        truoc, p = None, self.dau
        while p is not None and p.gt != gt:
            truoc, p = p, p.ke
        if p is None:
            return False
        if truoc is None:
            self.dau = p.ke
        else:
            truoc.ke = p.ke
        self.n -= 1
        return True

    def dao(self) -> None:
        truoc, p = None, self.dau
        while p is not None:
            sau = p.ke              # Giữ lối đi tới phần chưa đảo.
            p.ke = truoc
            truoc, p = p, sau
        self.dau = truoc

    def gia_tri(self) -> list[int]:
        """Tạo bản sao để hiển thị/kiểm thử; không phải cách lưu danh sách."""
        result: list[int] = []
        seen: set[int] = set()
        p = self.dau
        while p is not None:
            if id(p) in seen:
                raise ValueError("Danh sách có chu trình. Kiểm tra thứ tự sửa ke.")
            seen.add(id(p))
            result.append(p.gt)
            p = p.ke
        if len(result) != self.n:
            raise ValueError("Biến n không bằng số nút thực tế.")
        return result


class NganXep:
    """self.a lưu từ đáy tới đỉnh; phần tử cuối mảng là đỉnh."""
    def __init__(self) -> None:
        self.a: list[int] = []

    def day(self, x: int) -> None:
        self.a.append(so_nguyen(x))

    def lay(self) -> int | None:
        return self.a.pop() if self.a else None

    def dinh(self) -> int | None:
        return self.a[-1] if self.a else None

    def rong(self) -> bool:
        return len(self.a) == 0


class HangDoiVong:
    """dau là chỉ số logic từ 0; n là sức chứa; so là số phần tử hợp lệ."""
    def __init__(self, n: int = 5) -> None:
        if type(n) is not int or n <= 0:
            raise ValueError("Sức chứa phải là số nguyên dương.")
        self.a: list[int | None] = [None] * n
        self.n, self.dau, self.so = n, 0, 0

    def them(self, x: int) -> bool:
        x = so_nguyen(x)
        if self.so == self.n:
            return False
        self.a[(self.dau + self.so) % self.n] = x
        self.so += 1
        return True

    def lay(self) -> int | None:
        if self.so == 0:
            return None
        x = self.a[self.dau]
        # Không xoá ô vật lý: giá trị cũ không còn thuộc hàng đợi logic.
        self.dau = (self.dau + 1) % self.n
        self.so -= 1
        return x

    def xem_dau(self) -> int | None:
        return self.a[self.dau] if self.so else None

    def rong(self) -> bool:
        return self.so == 0

    def gia_tri(self) -> list[int]:
        return [self.a[(self.dau + i) % self.n] for i in range(self.so)]


def can_ngoac_chi_tiet(text: str) -> dict:
    """Kiểm tra (), [], {}; bỏ qua ký tự khác. Vị trí tính từ 1 theo ký tự.

    Đây là kiểm tra cấu trúc ngoặc, không phải trình phân tích cú pháp mã nguồn.
    Dấu ngoặc trong dấu nháy vẫn được xem là ngoặc của chuỗi đầu vào.
    """
    if not isinstance(text, str) or len(text) > 200:
        raise ValueError("Chuỗi kiểm tra tối đa 200 ký tự.")
    cap = {")": "(", "]": "[", "}": "{"}
    st: list[str] = []
    trace = []
    for i, c in enumerate(text, 1):
        good = True
        if c in "([{":
            st.append(c)
            note = "Đưa ngoặc mở vào đỉnh."
        elif c in ")]}":
            if not st:
                note, good = "Ngoặc đóng không có ngoặc mở tương ứng.", False
            elif st[-1] != cap[c]:
                note, good = "Ngoặc đóng khác loại với ngoặc mở ở đỉnh.", False
            else:
                st.pop()
                note = "Khớp loại: lấy ngoặc mở khỏi đỉnh."
        else:
            note = "Không phải dấu ngoặc: bỏ qua."
        trace.append({"pos": i, "char": c, "stack": st.copy(), "note": note, "ok": good})
        if not good:
            return {"valid": False, "reason": note, "trace": trace}
    good = not st
    note = "Các dấu ngoặc khớp nhau." if good else "Còn ngoặc mở chưa được đóng."
    trace.append({"pos": len(text) + 1, "char": "", "stack": st.copy(), "note": note, "ok": good})
    return {"valid": good, "reason": note, "trace": trace}
