"""Kiểm thử thuật toán mẫu; không yêu cầu hoàn thành bốn hàm bài tập."""
import random
import unittest
from cau_truc import DSLK, NganXep, HangDoiVong, so_nguyen, can_ngoac_chi_tiet
from dich_vu import UngDung


class TestDanhSach(unittest.TestCase):
    def test_rong(self):
        L = DSLK()
        self.assertEqual(L.gia_tri(), [])
        self.assertIsNone(L.tim(1))
        self.assertFalse(L.xoa(1))

    def test_them_dau_cuoi(self):
        L = DSLK()
        L.them_cuoi(20); L.them_dau(10); L.them_cuoi(30)
        self.assertEqual(L.gia_tri(), [10, 20, 30])
        self.assertEqual(L.n, 3)

    def test_chen_sau(self):
        L = DSLK([10, 20, 30])
        p = L.tim(20); tail = p.ke
        m = L.chen_sau(p, 25)
        self.assertIs(m.ke, tail)
        self.assertEqual(L.gia_tri(), [10, 20, 25, 30])

    def test_xoa_dau_cuoi_giua(self):
        L = DSLK([1, 2, 3, 4])
        for x in [1, 4, 2, 3]:
            self.assertTrue(L.xoa(x))
        self.assertEqual(L.gia_tri(), [])

    def test_xoa_chi_mot_gia_tri_trung(self):
        L = DSLK([2, 2, 3])
        self.assertTrue(L.xoa(2))
        self.assertEqual(L.gia_tri(), [2, 3])
        self.assertFalse(L.xoa(99))

    def test_dao_giu_nguyen_doi_tuong_nut(self):
        L = DSLK([1, 2, 3]); old = [L.tim(i) for i in [1, 2, 3]]
        L.dao()
        self.assertEqual(L.gia_tri(), [3, 2, 1])
        self.assertIs(L.dau, old[2]); self.assertIs(old[2].ke, old[1])
        L.dao(); self.assertEqual(L.gia_tri(), [1, 2, 3])

    def test_dao_rong_mot_nut(self):
        for values in [[], [8]]:
            L = DSLK(values); L.dao(); self.assertEqual(L.gia_tri(), values)

    def test_phat_hien_chu_trinh(self):
        L = DSLK([1]); L.dau.ke = L.dau
        with self.assertRaises(ValueError): L.gia_tri()

    def test_phat_hien_n_sai(self):
        L = DSLK([1]); L.n = 9
        with self.assertRaises(ValueError): L.gia_tri()

    def test_ngau_nhien_co_seed(self):
        rng = random.Random(20260917)
        L, ref = DSLK(), []
        for _ in range(1000):
            x, op = rng.randint(-10, 10), rng.randrange(4)
            if op == 0: L.them_dau(x); ref.insert(0, x)
            elif op == 1: L.them_cuoi(x); ref.append(x)
            elif op == 2:
                found = x in ref
                self.assertEqual(L.xoa(x), found)
                if found: ref.remove(x)
            else: L.dao(); ref.reverse()
            self.assertEqual(L.gia_tri(), ref)


class TestNganXep(unittest.TestCase):
    def test_rong(self):
        s = NganXep(); self.assertTrue(s.rong())
        self.assertIsNone(s.lay()); self.assertIsNone(s.dinh())

    def test_lifo(self):
        s = NganXep()
        for x in [10, 20, 30]: s.day(x)
        self.assertEqual([s.lay(), s.lay(), s.lay()], [30, 20, 10])

    def test_xem_dinh_khong_xoa(self):
        s = NganXep(); s.day(0)
        self.assertEqual(s.dinh(), 0); self.assertEqual(s.a, [0])


class TestHangDoi(unittest.TestCase):
    def test_suc_chua_sai(self):
        for n in [0, -1, True, 2.5]:
            with self.assertRaises(ValueError): HangDoiVong(n)

    def test_rong(self):
        q = HangDoiVong(4)
        self.assertTrue(q.rong()); self.assertIsNone(q.lay())
        self.assertIsNone(q.xem_dau()); self.assertEqual(q.gia_tri(), [])

    def test_day_khong_ghi_de(self):
        q = HangDoiVong(2); q.them(1); q.them(2)
        before = (q.a.copy(), q.dau, q.so)
        self.assertFalse(q.them(3))
        self.assertEqual((q.a, q.dau, q.so), before)

    def test_quay_vong_va_o_cu(self):
        q = HangDoiVong(4)
        for x in [1, 2, 3, 4]: q.them(x)
        self.assertEqual(q.lay(), 1)
        self.assertEqual(q.a, [1, 2, 3, 4])
        self.assertEqual(q.gia_tri(), [2, 3, 4])
        q.them(5)
        self.assertEqual(q.a, [5, 2, 3, 4])
        self.assertEqual(q.gia_tri(), [2, 3, 4, 5])

    def test_suc_chua_mot(self):
        q = HangDoiVong(1); self.assertTrue(q.them(0))
        self.assertFalse(q.them(1)); self.assertEqual(q.lay(), 0)
        self.assertTrue(q.them(2)); self.assertEqual(q.lay(), 2)

    def test_ngau_nhien_co_seed(self):
        rng = random.Random(20260917); q = HangDoiVong(7); ref = []
        for _ in range(1000):
            if rng.random() < 0.6:
                x = rng.randint(-10, 10); allowed = len(ref) < 7
                self.assertEqual(q.them(x), allowed)
                if allowed: ref.append(x)
            else:
                expected = ref.pop(0) if ref else None
                self.assertEqual(q.lay(), expected)
            self.assertEqual(q.gia_tri(), ref)


class TestNgoacVaDauVao(unittest.TestCase):
    def test_ngoac_dung(self):
        for s in ["", "a+b", "(a+[b*c])-{d/e}", "((()))", "{[(a+b)*c]}"]:
            self.assertTrue(can_ngoac_chi_tiet(s)["valid"])

    def test_ngoac_sai(self):
        for s in [")(", "([)]", "(()", "(a+[b)*c]"]:
            self.assertFalse(can_ngoac_chi_tiet(s)["valid"])

    def test_vi_tri_unicode(self):
        trace = can_ngoac_chi_tiet("á[)]")["trace"]
        self.assertEqual(trace[-1]["pos"], 3)
        self.assertFalse(trace[-1]["ok"])

    def test_kiem_tra_gia_tri(self):
        for x in [True, 2.5, "2", None, 1000001]:
            with self.assertRaises(ValueError): so_nguyen(x)
        self.assertEqual(so_nguyen(0), 0)

    def test_service_rollback_input(self):
        app = UngDung(); before = app.trang_thai()
        with self.assertRaises(ValueError): app.thuc_hien({"op":"list.reset", "values":[1, "sai"]})
        self.assertEqual(app.trang_thai(), before)

    def test_service_cau_lenh(self):
        app = UngDung()
        a = app.thuc_hien({"op":"list.insert","x":25,"target":20})
        self.assertEqual(a["before"]["list"]["values"], [10, 20, 30])
        self.assertEqual(a["state"]["list"]["values"], [10, 20, 25, 30])

if __name__ == "__main__": unittest.main(verbosity=2)
