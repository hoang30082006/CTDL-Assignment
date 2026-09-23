"""Nối nút bấm với thuật toán. Không chứa mã vẽ giao diện."""
from __future__ import annotations
from copy import deepcopy
import bai_lam
from cau_truc import DSLK, NganXep, HangDoiVong, so_nguyen, can_ngoac_chi_tiet


class UngDung:
    def __init__(self) -> None:
        self.L = DSLK([10, 20, 30])
        self.s = NganXep()
        self.q = HangDoiVong(5)

    def trang_thai(self) -> dict:
        return {
            "language": "Python", "edition": getattr(bai_lam, "BAN", "Đáp án"),
            "list": {"values": self.L.gia_tri(), "n": self.L.n},
            "stack": {"values": self.s.a.copy(), "n": len(self.s.a), "top": self.s.dinh()},
            "queue": {"values": self.q.gia_tri(), "a": self.q.a.copy(), "n": self.q.n,
                      "dau": self.q.dau, "so": self.q.so,
                      "active": [(self.q.dau + i) % self.q.n for i in range(self.q.so)]},
        }

    def thuc_hien(self, data: dict) -> dict:
        if not isinstance(data, dict):
            raise ValueError("Yêu cầu phải là một đối tượng JSON.")
        before = self.trang_thai()
        backup = deepcopy((self.L, self.s, self.q))
        try:
            result, message, steps, trace = self._run(data)
            state = self.trang_thai()  # Kiểm tra n và chu trình sau khi sửa liên kết.
            return {"ok": True, "result": result, "message": message,
                    "steps": steps, "trace": trace, "before": before, "state": state}
        except Exception:
            self.L, self.s, self.q = backup
            raise

    def _run(self, d: dict) -> tuple:
        op = d.get("op")
        x = so_nguyen(d.get("x")) if op in {
            "list.prepend", "list.append", "list.find", "list.insert", "list.delete",
            "list.count", "list.delete_all", "stack.push", "queue.enqueue"} else None
        if op in {"list.prepend", "list.append", "list.insert"} and self.L.n >= 50:
            raise ValueError("Giao diện giới hạn danh sách ở 50 nút.")
        if op == "stack.push" and len(self.s.a) >= 50:
            raise ValueError("Giao diện giới hạn ngăn xếp ở 50 phần tử.")
        k = so_nguyen(d.get("k"), "k") if op in {"stack.pop_many", "queue.peek_k"} else None
        trace = []
        if op == "all.reset":
            self.__init__()
            result, message = None, "Đã khôi phục dữ liệu ban đầu."
            steps = ["Danh sách: 10 → 20 → 30. Ngăn xếp rỗng. Hàng đợi rỗng, sức chứa 5."]
        elif op == "list.reset":
            a = d.get("values")
            if not isinstance(a, list) or len(a) > 50:
                raise ValueError("Nhập một dãy không quá 50 số nguyên.")
            a = [so_nguyen(v) for v in a]  # Kiểm tra hết trước khi thay dữ liệu.
            self.L = DSLK(a)
            result, message = self.L.n, "Đã tạo danh sách mới."
            steps = ["Mỗi giá trị tạo một nút riêng.", "Nút cuối có ke = None; n là số nút."]
        elif op == "list.prepend":
            self.L.them_dau(x)
            result, message = x, f"Đã thêm {x} vào đầu."
            steps = ["Tạo nút m chứa x.", "Cho m.ke giữ đầu cũ, rồi cho dau trỏ tới m.", "Tăng n lên 1."]
        elif op == "list.append":
            self.L.them_cuoi(x)
            result, message = x, f"Đã thêm {x} vào cuối."
            steps = ["Danh sách rỗng: cập nhật dau.", "Danh sách có nút: duyệt đến nút cuối rồi nối m vào sau.", "Tăng n lên 1."]
        elif op == "list.find":
            p, i = self.L.dau, 1
            while p is not None and p.gt != x:
                p, i = p.ke, i + 1
            result = i if p is not None else None
            message = f"Tìm thấy {x} ở vị trí {i}." if p is not None else f"Không có giá trị {x}."
            steps = ["Bắt đầu ở dau và lần theo ke.", "Vị trí hiển thị bắt đầu từ 1; nếu trùng, chọn lần xuất hiện đầu tiên."]
        elif op == "list.insert":
            target = so_nguyen(d.get("target"), "Giá trị cần tìm")
            p = self.L.tim(target)
            if p is None:
                result, message = False, f"Không có nút {target}; danh sách không đổi."
                steps = ["Tìm nút trước khi nối liên kết."]
            else:
                self.L.chen_sau(p, x)
                result, message = True, f"Đã chèn {x} sau nút {target} đầu tiên."
                steps = ["Tìm nút p có giá trị yêu cầu.", "m.ke = p.ke giữ phần đuôi.", "p.ke = m nối nút mới; tăng n."]
        elif op == "list.delete":
            result = self.L.xoa(x)
            message = f"Đã xoá một nút {x}." if result else f"Không có {x}; danh sách không đổi."
            steps = ["Giữ truoc và p khi tìm.", "Xoá đầu: dau = p.ke; xoá giữa/cuối: truoc.ke = p.ke.", "Chỉ giảm n khi thực sự xoá."]
        elif op == "list.reverse":
            self.L.dao()
            result, message = self.L.gia_tri(), "Đã đảo chiều các liên kết."
            steps = ["Lưu sau = p.ke trước khi sửa.", "Đảo p.ke về truoc; dời truoc và p.", "Kết thúc: dau = truoc. Không tạo nút mới."]
        elif op == "list.count":
            result = bai_lam.dem_gia_tri(self.L, x)
            message, steps = f"Số lần xuất hiện của {x}: {result}.", ["Đối chiếu kết quả với số nút có cùng giá trị.", "Danh sách trước và sau phải giống nhau."]
        elif op == "list.delete_all":
            result = bai_lam.xoa_tat_ca(self.L, x)
            message, steps = f"Đã xoá {result} nút mang giá trị {x}.", ["Không được bỏ sót các nút trùng liên tiếp hoặc ở đầu.", "n phải giảm đúng bằng số nút đã xoá."]
        elif op == "stack.reset":
            self.s = NganXep()
            result, message, steps = None, "Đã làm rỗng ngăn xếp.", ["Mảng a rỗng; chưa có đỉnh."]
        elif op == "stack.push":
            self.s.day(x)
            result, message, steps = x, f"Đã đẩy {x} lên đỉnh.", ["Thêm x vào cuối mảng.", "Phần tử cuối mảng là đỉnh ngăn xếp."]
        elif op == "stack.pop":
            result = self.s.lay()
            message = "Ngăn xếp rỗng; không thay đổi." if result is None else f"Đã lấy {result} khỏi đỉnh."
            steps = ["Kiểm tra rỗng trước.", "Nếu có phần tử, lấy và xoá phần tử cuối mảng."]
        elif op == "stack.peek":
            result = self.s.dinh()
            message, steps = "Đã xem đỉnh; không lấy ra.", ["Chỉ đọc phần tử cuối; số phần tử không đổi."]
        elif op == "stack.empty":
            result = self.s.rong()
            message, steps = "Đã kiểm tra ngăn xếp rỗng.", ["Kết quả đúng khi số phần tử bằng 0."]
        elif op == "stack.pop_many":
            result = bai_lam.lay_nhieu(self.s, k)
            message, steps = f"Đã lấy {k} phần tử theo LIFO.", ["Kiểm tra k hợp lệ trước mọi thay đổi.", "Kết quả ghi theo thứ tự lấy ra, không theo thứ tự đáy tới đỉnh."]
        elif op == "queue.reset":
            n = so_nguyen(d.get("capacity"), "Sức chứa")
            if not 1 <= n <= 12:
                raise ValueError("Sức chứa trên giao diện từ 1 đến 12.")
            self.q = HangDoiVong(n)
            result, message, steps = n, "Đã tạo hàng đợi rỗng.", ["Cấp phát mảng cố định; dau = 0 và so = 0."]
        elif op == "queue.enqueue":
            index = (self.q.dau + self.q.so) % self.q.n
            result = self.q.them(x)
            message = f"Đã ghi {x} vào ô logic {index}." if result else "Hàng đầy; từ chối thêm, không ghi đè."
            steps = ["Nếu so = n thì dừng, trả về sai.", "Nếu còn chỗ, ghi tại (dau + so) % n rồi tăng so."]
        elif op == "queue.dequeue":
            result = self.q.lay()
            message = "Hàng rỗng; không thay đổi." if result is None else f"Đã lấy {result} ở đầu hàng."
            steps = ["Nếu so = 0, trả về None.", "Nếu còn phần tử, đọc ô dau; tăng dau theo modulo và giảm so.", "Giá trị cũ có thể còn trong mảng nhưng không còn thuộc hàng đợi."]
        elif op == "queue.peek":
            result = self.q.xem_dau()
            message, steps = "Đã xem đầu hàng; không lấy ra.", ["Chỉ đọc, không sửa dau hoặc so."]
        elif op == "queue.empty":
            result = self.q.rong()
            message, steps = "Đã kiểm tra hàng đợi rỗng.", ["Kiểm tra so = 0, không dựa vào giá trị còn trong mảng."]
        elif op == "queue.peek_k":
            result = bai_lam.xem_k(self.q, k)
            message, steps = f"Đã xem {k} phần tử đầu theo FIFO.", ["Đi theo chỉ số vòng, không đọc thẳng k ô đầu của mảng.", "a, dau, so và n không được thay đổi."]
        elif op == "brackets.check":
            detail = can_ngoac_chi_tiet(d.get("text"))
            result, message, trace = detail["valid"], detail["reason"], detail["trace"]
            steps = ["Ngoặc mở: đẩy vào ngăn xếp.", "Ngoặc đóng: phải khớp loại ở đỉnh.", "Cuối chuỗi: ngăn xếp phải rỗng."]
        else:
            raise ValueError("Không có thao tác này.")
        return result, message, steps, trace
