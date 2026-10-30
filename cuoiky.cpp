// DT024 - Tim phan tu xuat hien nhieu lan nhat (CTDLGT, INT13185)
// Bien dich: g++ -std=c++17 -O2 -Wall -o cuoiky cuoiky.cpp
// Chay:      ./cuoiky vd1 | vd2 | test | khaosat | nhap
#include <algorithm>
#include <climits>
#include <cstdio>
#include <iostream>
#include <random>
#include <string>
#include <vector>
using namespace std;

struct ModeResult { int gia_tri; int tan_suat; bool hop_le; };
struct Nhom { int gia_tri; int so_luong; };

const int N_MAX = 2000;
const int GIA_TRI_MAX = 1000000;

// Bo dem so sanh khoa theo tung giai doan (Chuong 4.8)
static long long g_dem = 0;   // phep a[j] == a[i] trong mode_dem_truc_tiep
static long long g_sort = 0;  // so sanh khoa trong quick_sort
static long long g_quet = 0;  // phep a[i] == a[i-1] khi quet nhom

// ---------- Kiem tra dau vao ----------
bool validate_input(const vector<int>& a) {
    int n = (int)a.size();
    if (n < 1 || n > N_MAX) return false;
    for (int i = 0; i < n; ++i)
        if (a[i] < -GIA_TRI_MAX || a[i] > GIA_TRI_MAX) return false;
    return true;
}

// ---------- Ban 1: dem truc tiep O(n^2) ----------
ModeResult mode_dem_truc_tiep(const vector<int>& a) {
    if (!validate_input(a)) return {0, 0, false};
    int n = (int)a.size();
    int max_freq = 0;
    int best_val = INT_MAX;
    for (int i = 0; i < n; ++i) {
        int count = 0;
        for (int j = 0; j < n; ++j) {
            ++g_dem;
            if (a[j] == a[i]) ++count;
        }
        if (count > max_freq) {
            max_freq = count;
            best_val = a[i];
        } else if (count == max_freq && a[i] < best_val) {
            best_val = a[i];  // luat hoa: lay gia tri nho hon
        }
    }
    return {best_val, max_freq, true};
}

// ---------- Sort tu cai: quicksort, pivot o giua ----------
static bool nho_hon(int x, int y) { ++g_sort; return x < y; }

void quick_sort(vector<int>& a, int l, int r) {
    if (l >= r) return;
    int pivot = a[l + (r - l) / 2];
    int i = l, j = r;
    while (i <= j) {
        while (nho_hon(a[i], pivot)) ++i;
        while (nho_hon(pivot, a[j])) --j;
        if (i <= j) {
            swap(a[i], a[j]);
            ++i;
            --j;
        }
    }
    quick_sort(a, l, j);
    quick_sort(a, i, r);
}

// ---------- Gom nhom tren mang DA SAP XEP ----------
vector<Nhom> dem_nhom(const vector<int>& a, bool in_nhom = false) {
    vector<Nhom> ds;
    if (a.empty()) return ds;
    int cur = a[0], count = 1;
    for (size_t i = 1; i < a.size(); ++i) {
        ++g_quet;
        if (a[i] == cur) {
            ++count;
        } else {
            ds.push_back({cur, count});
            cur = a[i];
            count = 1;
        }
    }
    ds.push_back({cur, count});  // nhom cuoi: vong lap khong tu dong dong nhom nay
    if (in_nhom) {
        for (const Nhom& g : ds)
            printf("  nhom: gia_tri=%d so_luong=%d\n", g.gia_tri, g.so_luong);
    }
    return ds;
}

// ---------- Ban 2: sap xep + gom nhom ----------
ModeResult mode_sau_sap_xep(vector<int> a, bool in_nhom = true) {  // a: ban sao
    if (!validate_input(a)) return {0, 0, false};
    quick_sort(a, 0, (int)a.size() - 1);
    vector<Nhom> ds = dem_nhom(a, in_nhom);
    int max_freq = 0;
    int best_val = INT_MAX;
    for (const Nhom& g : ds) {
        if (g.so_luong > max_freq) {  // dau > nghiem ngat: hoa thi giu nhom nho hon (da dung truoc)
            max_freq = g.so_luong;
            best_val = g.gia_tri;
        }
    }
    return {best_val, max_freq, true};
}

// ---------- Tien ich in an ----------
string to_str(const vector<int>& a) {
    if (a.size() > 12) {
        return "n=" + to_string(a.size()) + " phan tu, a[0]=" + to_string(a[0]);
    }
    string s = "[";
    for (size_t i = 0; i < a.size(); ++i) {
        if (i) s += ",";
        s += to_string(a[i]);
    }
    return s + "]";
}

void chay_vi_du(const vector<int>& a) {
    printf("Input: %s\n", to_str(a).c_str());
    ModeResult r1 = mode_dem_truc_tiep(a);
    printf("[dem truc tiep] gia_tri=%d; tan_suat=%d\n", r1.gia_tri, r1.tan_suat);
    printf("[sap xep + gom nhom]\n");
    ModeResult r2 = mode_sau_sap_xep(a, true);
    printf("[sap xep + gom nhom] gia_tri=%d; tan_suat=%d\n", r2.gia_tri, r2.tan_suat);
}

// ---------- Bo kiem thu ----------
struct TestCase {
    string ma;
    vector<int> input;
    bool hop_le;
    int gia_tri;
    int tan_suat;
};

static int g_pass = 0, g_total = 0;

void bao_cao(const string& ma, bool ok, const string& chi_tiet) {
    ++g_total;
    if (ok) ++g_pass;
    printf("[%s] %-7s %s\n", ok ? "PASS" : "FAIL", ma.c_str(), chi_tiet.c_str());
}

void chay_ca(const TestCase& t) {
    ModeResult r1 = mode_dem_truc_tiep(t.input);
    ModeResult r2 = mode_sau_sap_xep(t.input, false);
    bool ok;
    char buf[256];
    if (!t.hop_le) {
        ok = !r1.hop_le && !r2.hop_le;
        snprintf(buf, sizeof buf, "%s | expected: tu choi | actual: dem=%s, sort=%s",
                 to_str(t.input).c_str(), r1.hop_le ? "chap nhan" : "tu choi",
                 r2.hop_le ? "chap nhan" : "tu choi");
    } else {
        ok = r1.hop_le && r2.hop_le && r1.gia_tri == t.gia_tri && r1.tan_suat == t.tan_suat &&
             r2.gia_tri == t.gia_tri && r2.tan_suat == t.tan_suat;
        snprintf(buf, sizeof buf, "%s | expected: (%d,%d) | actual: dem=(%d,%d), sort=(%d,%d)",
                 to_str(t.input).c_str(), t.gia_tri, t.tan_suat, r1.gia_tri, r1.tan_suat,
                 r2.gia_tri, r2.tan_suat);
    }
    bao_cao(t.ma, ok, buf);
}

void chay_test() {
    vector<TestCase> ds = {
        {"VD01", {2, 1, 2, 3, 2, 1}, true, 2, 3},
        {"VD02", {4, 1, 4, 1}, true, 1, 2},
        {"TK01", {6, 6, -3, -3, 2}, true, -3, 2},
        {"TK02", {2, 8, 8, 8, 1, 2}, true, 8, 3},
        {"BIEN01", {7}, true, 7, 1},
        {"BIEN02", {-2, -2, -1}, true, -2, 2},
        {"BIEN03", {3, 2, 1}, true, 1, 1},
        {"LOI01", {1000001}, false, 0, 0},
        {"KT09", {5, 5, 5, 5}, true, 5, 4},
        {"KT10", {9, 3, 9, 3, 6, 6}, true, 3, 2},
        {"KT11", {1, 2, 2, 3, 3}, true, 2, 2},
        // Ca bo sung
        {"KT13", vector<int>(2000, GIA_TRI_MAX), true, GIA_TRI_MAX, 2000},
        {"LOI02", {}, false, 0, 0},
        {"LOI03", vector<int>(2001, 1), false, 0, 0},
    };
    for (const TestCase& t : ds) chay_ca(t);

    // KT12: kiem rieng ham dem_nhom
    vector<Nhom> g = dem_nhom({1, 1, 2, 3, 3, 3}, false);
    bool ok = g.size() == 3 && g[0].gia_tri == 1 && g[0].so_luong == 2 && g[1].gia_tri == 2 &&
              g[1].so_luong == 1 && g[2].gia_tri == 3 && g[2].so_luong == 3;
    bao_cao("KT12", ok, "dem_nhom([1,1,2,3,3,3]) | expected: (1,2),(2,1),(3,3)");

    printf("Tong ket: %d/%d PASS, %d FAIL\n", g_pass, g_total, g_total - g_pass);
}

// ---------- Khao sat so phep so sanh khoa ----------
void khao_sat() {
    int cac_n[] = {6, 30, 100, 500};
    mt19937 rng(2026);  // seed co dinh de chay lai duoc
    uniform_int_distribution<int> dist(-50, 50);
    printf("%5s %12s %10s %10s %12s %6s\n", "n", "dem_truc_tiep", "sort", "quet", "sort+quet", "khop");
    for (int n : cac_n) {
        vector<int> a(n);
        for (int& x : a) x = dist(rng);
        g_dem = 0;
        ModeResult r1 = mode_dem_truc_tiep(a);
        long long dem = g_dem;
        g_sort = 0;
        g_quet = 0;
        ModeResult r2 = mode_sau_sap_xep(a, false);
        bool khop = r1.gia_tri == r2.gia_tri && r1.tan_suat == r2.tan_suat;
        printf("%5d %12lld %10lld %10lld %12lld %6s\n", n, dem, g_sort, g_quet, g_sort + g_quet,
               khop ? "dung" : "SAI");
    }
}

// ---------- Nhap tu ban phim ----------
void nhap_ban_phim() {
    int n;
    printf("Nhap n (1..%d): ", N_MAX);
    if (!(cin >> n) || n < 1 || n > N_MAX) {
        printf("Du lieu khong hop le: n phai nam trong [1, %d]\n", N_MAX);
        return;
    }
    vector<int> a(n);
    printf("Nhap %d so nguyen: ", n);
    for (int& x : a) cin >> x;
    if (!validate_input(a)) {
        printf("Du lieu khong hop le: |a[i]| phai <= %d\n", GIA_TRI_MAX);
        return;
    }
    chay_vi_du(a);
}

int main(int argc, char** argv) {
    string lenh = argc > 1 ? argv[1] : "test";
    if (lenh == "vd1") chay_vi_du({2, 1, 2, 3, 2, 1});
    else if (lenh == "vd2") chay_vi_du({4, 1, 4, 1});
    else if (lenh == "test") chay_test();
    else if (lenh == "khaosat") khao_sat();
    else if (lenh == "nhap") nhap_ban_phim();
    else printf("Lenh: vd1 | vd2 | test | khaosat | nhap\n");
    return 0;
}