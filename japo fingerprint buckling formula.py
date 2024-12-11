import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class AnalisisBuckling:
    def __init__(self, D, E, h, Rx, Ry, dimensi=(100, 100), dx=0.1):
        """
        Inisialisasi parameter analisis buckling

        Parameter:
        D: float - Modulus lentur
        E: float - Modulus Young
        h: float - Ketebalan lapisan
        Rx, Ry: float - Radius kelengkungan utama
        dimensi: tuple - Dimensi grid
        dx: float - Jarak antar grid
        """
        self.D = D  # Modulus lentur
        self.E = E  # Modulus Young
        self.h = h  # Ketebalan lapisan
        self.Rx = Rx  # Radius kelengkungan pada sumbu x
        self.Ry = Ry  # Radius kelengkungan pada sumbu y

        # Parameter grid
        self.nx, self.ny = dimensi
        self.dx = dx
        self.x = np.linspace(0, self.nx*dx, self.nx)
        self.y = np.linspace(0, self.ny*dx, self.ny)
        self.X, self.Y = np.meshgrid(self.x, self.y)

        # Inisialisasi medan defleksi
        self.w = np.zeros((self.nx, self.ny))
        self.F = np.zeros((self.nx, self.ny))  # Fungsi tegangan Airy

    def hitung_energi_elastis(self, w, F):
        """
        Menghitung total energi elastis berdasarkan persamaan (1) dari paper:
        E = ∫[D/2(∇²w)² - 1/(2Eh)(∇²F)² + Fyyw/Rx + Fxxw/Ry - w[F,w] + V(w)]dxdy
        """
        # Menghitung turunan
        w_xx = np.gradient(np.gradient(w, self.dx, axis=1), self.dx, axis=1)
        w_yy = np.gradient(np.gradient(w, self.dx, axis=0), self.dx, axis=0)
        F_xx = np.gradient(np.gradient(F, self.dx, axis=1), self.dx, axis=1)
        F_yy = np.gradient(np.gradient(F, self.dx, axis=0), self.dx, axis=0)

        # Menghitung Laplacian
        del2_w = w_xx + w_yy
        del2_F = F_xx + F_yy

        # Menghitung bracket [F,w]
        F_xy = np.gradient(np.gradient(F, self.dx, axis=0), self.dx, axis=1)
        w_xy = np.gradient(np.gradient(w, self.dx, axis=0), self.dx, axis=1)
        bracket = F_xx * w_yy + F_yy * w_xx - 2 * F_xy * w_xy

        # Potensial sederhana V(w) = cw²/2 + aw³/3 + bw⁴/4
        c, a, b = 1.0, 0.1, 0.01  # Koefisien contoh
        V = c*w**2/2 + a*w**3/3 + b*w**4/4

        # Menghitung densitas energi
        densitas_energi = (
            self.D/2 * del2_w**2
            - 1/(2*self.E*self.h) * del2_F**2
            + F_yy*w/self.Rx
            + F_xx*w/self.Ry
            - w*bracket
            + V
        )

        # Total energi (integrasi numerik)
        total_energi = np.sum(densitas_energi) * self.dx * self.dx
        return total_energi

    def simulasi_buckling(self, langkah=100):
        """
        Mensimulasikan proses buckling dengan memberikan gangguan kecil
        dan meminimalkan energi elastis
        """
        # Gangguan awal (defleksi acak kecil)
        self.w = 0.01 * np.random.randn(self.nx, self.ny)

        energi = []
        dt = 0.01  # Langkah waktu untuk evolusi

        for step in range(langkah):
            # Menghitung energi sebelum update
            energi_sekarang = self.hitung_energi_elastis(self.w, self.F)
            energi.append(energi_sekarang)

            # Update dengan gradient descent sederhana
            dw = 0.01 * np.random.randn(self.nx, self.ny)
            energi_baru = self.hitung_energi_elastis(self.w + dw, self.F)

            if energi_baru < energi_sekarang:
                self.w += dw

        return np.array(energi)

    def plot_hasil(self):
        """Plot pola defleksi akhir dan evolusi energi"""
        fig = plt.figure(figsize=(12, 5))

        # Plot permukaan 3D dari defleksi
        ax1 = fig.add_subplot(121, projection='3d')
        ax1.plot_surface(self.X, self.Y, self.w, cmap='viridis')
        ax1.set_title('Pola Defleksi')
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_zlabel('w')

        # Plot kontur defleksi
        ax2 = fig.add_subplot(122)
        c = ax2.contour(self.X, self.Y, self.w)
        ax2.clabel(c, inline=True, fontsize=8)
        ax2.set_title('Kontur Defleksi')
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')

        plt.tight_layout()
        plt.show()


# Contoh penggunaan
if __name__ == "__main__":
    # Parameter dari paper (dikonversi ke satuan yang konsisten)
    D = 1.3e-7  # Modulus lentur (N⋅mm)
    E = 10e-3   # Modulus Young (N/mm²)
    h = 8.0e-3  # Ketebalan lapisan (mm)
    Rx = Ry = 780  # Radius kelengkungan (mm)

    # Membuat objek analisis
    analisis = AnalisisBuckling(D, E, h, Rx, Ry)

    # Menjalankan simulasi
    hasil_energi = analisis.simulasi_buckling(langkah=100)

    # Plot hasil
    analisis.plot_hasil()

    # Plot evolusi energi
    plt.figure(figsize=(8, 4))
    plt.plot(hasil_energi)
    plt.title('Evolusi Energi')
    plt.xlabel('Langkah')
    plt.ylabel('Total Energi Elastis')
    plt.show()
