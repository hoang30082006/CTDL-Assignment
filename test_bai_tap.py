"""Kiểm thử công khai bốn hàm. Bản sinh viên sẽ báo lỗi cho tới khi cài đặt.

Được dùng list làm kết quả đối chiếu trong kiểm thử; không dùng nó thay nút liên kết.
"""
import random
import unittest
from cau_truc import DSLK, NganXep, HangDoiVong
from bai_lam import dem_gia_tri, xoa_tat_ca, lay_nhieu, xem_k


def stack(values):
    s = NganXep()
    for x in values: s.day(x)
    return s


def queue_wrap():
    q = HangDoiVong(4)
    for x in [1, 2, 3, 4]: q.them(x)
    q.lay(); q.lay(); q.them(5); q.them(6)
    return q  # a = [5,6,3,4]; FIFO = [3,4,5,6]; dau = 2.


class TestBaiTap(unittest.TestCase):
    def test_dem_rong(self):
        self.assertEqual(dem_gia_tri(DSLK(), 2), 0)

    def test_dem_trung_khong_doi(self):
        L = DSLK([2, 1, 2, 2]); head = L.dau
        self.assertEqual(dem_gia_tri(L, 2), 3)
        self.assertEqual(L.gia_tri(), [2, 1, 2, 2]); self.assertIs(L.dau, head)

    def test_dem_khong_co(self):
        self.assertEqual(dem_gia_tri(DSLK([1, 3]), 2), 0)

    def test_xoa_lien_tiep_va_giu_nut_con_lai(self):
        L = DSLK([2, 2, 1, 2, 3, 2]); p1, p3 = L.tim(1), L.tim(3)
        self.assertEqual(xoa_tat_ca(L, 2), 4)
        self.assertEqual(L.gia_tri(), [1, 3]); self.assertEqual(L.n, 2)
        self.assertIs(L.dau, p1); self.assertIs(p1.ke, p3)

    def test_xoa_het(self):
        L = DSLK([4, 4, 4]); self.assertEqual(xoa_tat_ca(L, 4), 3)
        self.assertIsNone(L.dau); self.assertEqual(L.gia_tri(), [])

    def test_xoa_rong(self):
        self.assertEqual(xoa_tat_ca(DSLK(), 4), 0)

    def test_xoa_khong_co(self):
        L = DSLK([1, 2]); self.assertEqual(xoa_tat_ca(L, 8), 0)
        self.assertEqual(L.gia_tri(), [1, 2])

    def test_lay_nhieu_thu_tu(self):
        s = stack([10, 20, 30]); self.assertEqual(lay_nhieu(s, 2), [30, 20])
        self.assertEqual(s.a, [10])

    def test_lay_nhieu_khong(self):
        s = stack([10]); self.assertEqual(lay_nhieu(s, 0), [])
        self.assertEqual(s.a, [10])

    def test_lay_nhieu_het(self):
        s = stack([0, 1]); self.assertEqual(lay_nhieu(s, 2), [1, 0])
        self.assertTrue(s.rong())

    def test_lay_nhieu_k_sai_khong_doi(self):
        for k in [-1, 4, 1.5, True]:
            s = stack([10, 20, 30]); before = s.a.copy()
            with self.assertRaises(ValueError): lay_nhieu(s, k)
            self.assertEqual(s.a, before)

    def test_lay_nhieu_rong(self):
        self.assertEqual(lay_nhieu(NganXep(), 0), [])
        with self.assertRaises(ValueError): lay_nhieu(NganXep(), 1)

    def test_xem_k_quay_vong(self):
        q = queue_wrap(); before = (q.a.copy(), q.dau, q.so, q.n)
        self.assertEqual(xem_k(q, 3), [3, 4, 5])
        self.assertEqual((q.a, q.dau, q.so, q.n), before)

    def test_xem_k_khong_va_het(self):
        q = queue_wrap(); self.assertEqual(xem_k(q, 0), [])
        self.assertEqual(xem_k(q, 4), [3, 4, 5, 6])

    def test_xem_k_sai_khong_doi(self):
        for k in [-1, 5, 1.5, True]:
            q = queue_wrap(); before = (q.a.copy(), q.dau, q.so, q.n)
            with self.assertRaises(ValueError): xem_k(q, k)
            self.assertEqual((q.a, q.dau, q.so, q.n), before)

    def test_xem_k_rong(self):
        self.assertEqual(xem_k(HangDoiVong(4), 0), [])
        with self.assertRaises(ValueError): xem_k(HangDoiVong(4), 1)

    def test_danh_sach_ngau_nhien_co_seed(self):
        rng = random.Random(20260917)
        for _ in range(200):
            values = [rng.randint(-3, 3) for _ in range(rng.randrange(30))]
            x = rng.randint(-3, 3); L = DSLK(values)
            self.assertEqual(dem_gia_tri(L, x), values.count(x))
            self.assertEqual(xoa_tat_ca(L, x), values.count(x))
            self.assertEqual(L.gia_tri(), [v for v in values if v != x])

if __name__ == "__main__": unittest.main(verbosity=2)
