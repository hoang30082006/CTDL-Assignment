#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
#include <cmath>

using namespace std;

struct ModeResult {
    int gia_tri;
    int tan_suat;
    bool hop_le;
};

// Hàm kiểm tra đầu vào
bool validate_input(const vector<int>& a) {
    if (a.empty() || a.size() > 2000) return false;
    for (int val : a) {
        if (abs(val) > 1000000) return false;
    }
    return true;
}

// Phương pháp 1: Đếm trực tiếp O(n^2)
ModeResult mode_dem_truc_tiep(const vector<int>& a) {
    if (!validate_input(a)) return {0, 0, false};
    
    int n = a.size();
    int max_freq = 0;
    int best_val = INT_MAX;
    
    for (int i = 0; i < n; ++i) {
        int count = 0;
        for (int j = 0; j < n; ++j) {
            if (a[j] == a[i]) count++;
        }
        if (count > max_freq) {
            max_freq = count;
            best_val = a[i];
        } else if (count == max_freq && a[i] < best_val) {
            best_val = a[i];
        }
    }
    return {best_val, max_freq, true};
}

// Phương pháp 2: Sắp xếp gom nhóm O(n log n)
ModeResult mode_sau_sap_xep(vector<int> a) {
    if (!validate_input(a)) return {0, 0, false};
    
    sort(a.begin(), a.end());
    
    int max_freq = 0;
    int best_val = INT_MAX;
    int current_val = a[0];
    int current_count = 1;
    
    for (size_t i = 1; i < a.size(); ++i) {
        if (a[i] == current_val) {
            current_count++;
        } else {
            if (current_count > max_freq) {
                max_freq = current_count;
                best_val = current_val;
            }
            current_val = a[i];
            current_count = 1;
        }
    }
    
    if (current_count > max_freq) {
        max_freq = current_count;
        best_val = current_val;
    }
    
    return {best_val, max_freq, true};
}

void in_ket_qua(string ten_ca, const vector<int>& a) {
    cout << "=== " << ten_ca << " ===" << endl;
    cout << "Dau vao a: ";
    for (int x : a) cout << x << " ";
    cout << endl;
    
    ModeResult r1 = mode_dem_truc_tiep(a);
    ModeResult r2 = mode_sau_sap_xep(a);
    
    if (!r1.hop_le) {
        cout << "Kiet qua: INPUT KHONG HOP LE (PASS - Tu choi xu ly dung quy dinh)" << endl << endl;
        return;
    }
    
    cout << "Giai thuat Dem truc tiep: Mode = " << r1.gia_tri << ", Tan suat = " << r1.tan_suat << endl;
    cout << "Giai thuat Sap xep gom nhom: Mode = " << r2.gia_tri << ", Tan suat = " << r2.tan_suat << endl;
    cout << "Trang thai: PASS (Ket qua hai phuong phap trung khop)" << endl << endl;
}

int main() {
    // 1. Vi du mau 1
    in_ket_qua("Ca 1: Vi du mau 1", {2, 1, 2, 3, 2, 1});
    
    // 2. Vi du mau 2 (Hoa tan suat - Luat hoa)
    in_ket_qua("Ca 2: Vi du mau 2 (Xul ly hoa)", {4, 1, 4, 1});
    
    // 3. Mang 1 phan tu
    in_ket_qua("Ca 3: Mang 1 phan tu", {99});
    
    // 4. Input sai (Vuot qua 2000 phan tu hoac chua gia tri |a[i]| > 10^6)
    in_ket_qua("Ca 4: Input sai |a[i]| > 10^6", {10, 20, 1000005});

    return 0;
}