import numpy as np

GRAD = {
    'A': 90,
    'B': 80,
    'C': 70,
    'D': 60,
    'E': 0
}
minimum_score = 75
max_score = 100
iqr_multiplier = 1.5

class AnalisisUjian:
    def __init__(self, name: list, score: list):
        self._validate_input(name, score)
        self.name = np.array(name, dtype=str)
        self.score = np.array(score, dtype=np.float64)
        self.stats = {}

        print(f"Data berhasil dimuat: {len(self.name)} siswa\n")

    @staticmethod
    def _validate_input(name: list, score: list):
        if len(name) != len(score):
            raise ValueError(f"Panjang name ({len(name)}) dan score ({len(score)}) harus sama.")
        score_array = np.array(score, dtype=np.float64)
        if np.any(score_array < 0) or np.any(score_array > max_score):
            raise ValueError("Semua nilai score harus antara 0 dan 100.")
        if len(name) == 0:
            raise ValueError("Data tidak boleh kosong.")

    def compute_stats(self) -> dict:
        s = self.score
        q1, q3 = np.percentile(s, [25, 75])
        iqr = q3 - q1
        pass_score = minimum_score  # Menggunakan minimum_score untuk kelulusan
        self.stats = {
            "mean": np.mean(s),
            "median": np.median(s),
            "std": np.std(s, ddof=1),
            "variance": np.var(s, ddof=1),
            "min": np.min(s),
            "max": np.max(s),
            "range": np.max(s) - np.min(s),
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "total": len(s),
            "passed": int(np.sum(passed_score_mask := s >= pass_score)),
            "failed": int(np.sum(~passed_score_mask)),
            "pass_rate_pct": np.mean(passed_score_mask) * 100,
        }
        return self.stats

    def classify_grades(self) -> np.ndarray:
        s = self.score
        conditions = [
            s >= GRAD["A"],  # ≥ 90 → A
            s >= GRAD["B"],  # ≥ 80 → B
            s >= GRAD["C"],  # ≥ 70 → C
            s >= GRAD["D"],  # ≥ 60 → D
        ]
        choices = ["A", "B", "C", "D"]
        return np.select(conditions, choices, default="E")

    def detect_outliers(self) -> dict:
        if not self.stats:
            self.compute_stats()
        q1, q3, iqr = self.stats["q1"], self.stats["q3"], self.stats["iqr"]
        lower_bound = q1 - iqr * iqr_multiplier
        upper_bound = q3 + iqr * iqr_multiplier
        outliers_mask = (self.score < lower_bound) | (self.score > upper_bound)
        return {
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "outlier_names": self.name[outliers_mask],
            "outlier_scores": self.score[outliers_mask],
            "count": int(np.sum(outliers_mask))
        }

    def rank_students(self, top_n: int = 5) -> dict:
        sorted_indices = np.argsort(self.score)[::-1]
        full_ranking = [
            {"rank": i + 1, "name": self.name[idx], "score": self.score[idx]} for i, idx in enumerate(sorted_indices)
        ]
        return {
            "top": full_ranking[:top_n],
            "bottom": full_ranking[-top_n:],
            "full_ranking": full_ranking
        }

    def grade_distribution(self) -> dict:
        grades = self.classify_grades()
        total = len(grades)
        dist = {}

        for grade in ["A", "B", "C", "D", "E"]:
            count = int(np.sum(grades == grade))
            dist[grade] = {
                "count": count,
                "pct": (count / total * 100) if total > 0 else 0,
            }
        return dist

    def generate_report(self) -> None:
        if not self.stats:
            self.compute_stats()
        grades = self.classify_grades()
        dist = self.grade_distribution()
        rank = self.rank_students()
        outliers = self.detect_outliers()
        st = self.stats

        SEP = "-" * 56
        SEP2 = "=" * 56

        print(f"\n{SEP2}")
        print("   📊  LAPORAN ANALISIS NILAI UJIAN")
        print(f"{SEP2}")
        print(f"\n{'STATISTIK DESKRIPTIF':^56}")
        print(SEP)
        print(f"  {'Jumlah Siswa':<22}: {st['total']}")
        print(f"  {'Rata-rata (Mean)':<22}: {st['mean']:.2f}")
        print(f"  {'Median':<22}: {st['median']:.2f}")
        print(f"  {'Std Deviasi':<22}: {st['std']:.2f}")
        print(f"  {'Varians':<22}: {st['variance']:.2f}")
        print(f"  {'Nilai Minimum':<22}: {st['min']:.2f}")
        print(f"  {'Nilai Maksimum':<22}: {st['max']:.2f}")
        print(f"  {'Range':<22}: {st['range']:.2f}")
        print(f"  {'Q1 (25th percentile)':<22}: {st['q1']:.2f}")
        print(f"  {'Q3 (75th percentile)':<22}: {st['q3']:.2f}")
        print(f"  {'IQR':<22}: {st['iqr']:.2f}")

        # — KELULUSAN
        print(f"\n{'KELULUSAN':^56}")
        print(SEP)
        print(f"  {'Lulus  (≥ ' + str(minimum_score) + ')':<22}: {st['passed']} siswa")
        print(f"  {'Tidak Lulus':<22}: {st['failed']} siswa")
        print(f"  {'Tingkat Kelulusan':<22}: {st['pass_rate_pct']:.1f}%")

        # — DISTRIBUSI NILAI HURUF
        print(f"\n{'DISTRIBUSI NILAI HURUF':^56}")
        print(SEP)
        bar_max = 20
        for grade, info in dist.items():
            bar_len = int((info["pct"] / 100) * bar_max)
            bar = "█" * bar_len + "░" * (bar_max - bar_len)
            print(
                f"  {grade} [{bar}] "
                f"{info['count']:>3} siswa  ({info['pct']:>5.1f}%)"
            )

        # — TOP 5
        print(f"\n{'TOP 5 TERTINGGI':^56}")
        print(SEP)
        for entry in rank["top"]:
            grade = grades[np.where(self.name == entry["name"])[0][0]]
            print(
                f"  #{entry['rank']:<3} {entry['name']:<20}"
                f"  {entry['score']:>6.2f}  [{grade}]"
            )

        # — BOTTOM 5
        print(f"\n{'BOTTOM 5 TERENDAH':^56}")
        print(SEP)
        for entry in reversed(rank["bottom"]):
            grade = grades[np.where(self.name == entry["name"])[0][0]]
            status = "LULUS" if entry["score"] >= minimum_score else "TIDAK LULUS"
            print(
                f"  #{entry['rank']:<3} {entry['name']:<20}"
                f"  {entry['score']:>6.2f}  [{grade}] {status}"
            )

        # — OUTLIER
        print(f"\n{'DETEKSI OUTLIER (Metode IQR)':^56}")
        print(SEP)
        print(f"  Batas Bawah  : {outliers['lower_bound']:.2f}")
        print(f"  Batas Atas   : {outliers['upper_bound']:.2f}")
        if outliers["count"] == 0:
            print("  ✅ Tidak ada outlier terdeteksi.")
        else:
            print(f"  ⚠️  Ditemukan {outliers['count']} outlier:")
            for name, score in zip(outliers["outlier_names"], outliers["outlier_scores"]):
                print(f"      • {name:<20} → {score:.2f}")

        print(f"\n{SEP2}\n")


def load_sample_data() -> tuple[list, list]:
    names = [
        "Andi", "Budi", "Citra", "Dewi", "Eko",
        "Fina", "Gilang", "Hani", "Ivan", "Julia",
        "Kiki", "Lena", "Miko", "Nadia", "Omar",
        "Putri", "Qori", "Rafi", "Sari", "Tomi",
        "Umar", "Vera", "Widi", "Xena", "Yogi",
        "Zahra", "Aldo", "Bella", "Cahyo", "Dini",
    ]
    scores = [
        88, 72, 95, 60, 45, 78, 83, 91, 55, 67,
        70, 48, 85, 92, 63, 77, 58, 74, 89, 40,
        66, 80, 53, 97, 71, 62, 84, 76, 50, 69,
    ]
    return names, scores


def load_from_input() -> tuple[list, list]:
    print("=== INPUT DATA SISWA ===")
    n = int(input("Jumlah siswa: "))
    names, scores = [], []

    for i in range(n):
        name = input(f"  Nama siswa ke-{i+1}: ").strip()
        score = float(input(f"  Nilai {name}: "))
        names.append(name)
        scores.append(score)

    return names, scores


def main():
    print("╔══════════════════════════════════════╗")
    print("║   EXAM ANALYSIS SYSTEM — NumPy       ║")
    print("╚══════════════════════════════════════╝\n")

    # Pilih sumber data: sample atau input manual
    use_sample = input("Gunakan data sampel? (y/n): ").strip().lower()

    if use_sample == "y":
        names, scores = load_sample_data()
    else:
        names, scores = load_from_input()

    # ── Pipeline Analisis ──────────────────────────────
    analyzer = AnalisisUjian(names, scores)  # 1. Inisialisasi
    analyzer.compute_stats()               # 2. Hitung statistik
    analyzer.generate_report()             # 3. Tampilkan laporan
    # ──────────────────────────────────────────────────

    # Akses data mentah (opsional, untuk integrasi lanjut)
    print("📦 Data siap digunakan lebih lanjut:")
    print("   analyzer.stats       → dict statistik" )  
    print("   analyzer.classify_grades() → array nilai huruf" )  
    print("   analyzer.rank_students()   → dict peringkat" )  
    print("   analyzer.detect_outliers() → dict outlier\n")


if __name__ == "__main__":
    main()  
                
                
               
                   
                           