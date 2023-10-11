# README


## Kelompok F04
1. Fikri Budianto - 2206025306
2. Serafino Theodore Axel Rori - 2206082644
3. Ayundha Sachi Mulia - 2206083275
4. Shanahan Danualif Erwin - 2206817420
5. Muhammad Haekal Kalipaksi - 2206817490

## Deskripsi Aplikasi `README`
Aplikasi `README` adalah aplikasi yang berharap untuk meningkatkan pemahaman tentang bahasa, sastra, dan literasi di Indonesia.  Aplikasi `README` selaras dengan tema Kongres Bahasa Indonesia XII, yaitu "Literasi dalam Kebhinekaan untuk Kemajuan Bangsa." Aplikasi `README` memberikan platform bagi pengguna untuk meminjam buku, membaca buku, memberikan ulasan, dan berdiskusi buku dengan pengguna lain. Selain itu, pengguna juga dapat melihat profil pengguna lain, sehingga dapat melihat buku yang sudah dibaca, ulasan yang ditulis, dan diskusi yang dilakukan oleh pengguna. Berikut adalah manfaat dari aplikasi `README`:
- Meningkatkan literasi, dengan memberikan akses terhadap buku yang disediakan oleh Project Gutenbergs.
- Menciptakan interaksi antar pengguna, dengan memberikan fitur ulasan dan diskusi. Diharapkan pengguna dapat mendapatkan rekomendasi buku dengan membaca ulasan dan diskusi.

## Daftar Modul
### 1. Profil 
*Modul `Profil` akan dikerjakan oleh: **Serafino Theodore Axel Rori***

   Modul Profil adalah bagian dari aplikasi yang memungkinkan pengguna untuk membuat dan mengelola profil pribadi mereka. Di sini, pengguna dapat menambahkan informasi pribadi seperti nama, foto profil, deskripsi singkat, buku yang sedang dibaca, dan genre favorite. Modul ini juga memungkinkan pengguna untuk melihat riwayat aktivitas mereka di aplikasi, seperti buku yang telah mereka beli dan pinjam dan ulasan yang mereka berikan. Selain itu dapat di edit juga profilnya.

### 2. Pinjam Buku
*Modul `Pinjam Buku` akan dikerjakan oleh: **Fikri Budianto***

Modul Pinjam Buku adalah fitur yang memungkinkan pengguna untuk mencari dan meminjam buku dari perpustakaan digital atau fisik. Pengguna dapat mencari buku berdasarkan judul, penulis, atau kategori, lalu meminjam buku tersebut untuk dibaca. Modul ini juga dapat melacak tenggat waktu pengembalian buku dan memberi pengguna akses ke buku yang telah mereka pinjam. Selain itu, modul pinjam buku juga mempertimbangkan stok buku yang dapat dipinjam sehingga stok yang dapat dipinjam habis maka pengguna tidak dapat meminjam buku jenis tersebut. Tentunya selain pengguna dapat meminjam buku, mereka juga bisa mengembalikan buku.

### 3. Review Buku 
*Modul `Review Buku` akan dikerjakan oleh: **Ayundha Sachi Mulia***

Modul Review Buku adalah fitur untuk memberikan bintang atau nilai dan ulasan terhadap buku yang telah dibaca. Pengguna dapat berbagi pendapat mereka mengenai buku yang dibaca dan memberikan rekomendasi ke pengguna lainnya berdasarkan minat mereka. Fitur ini juga me

### 4. Katalog Buku
*Modul `Katalog Buku` akan dikerjakan oleh: **Muhammad Haekal Kalipaksi***

Modul Katalog Buku adalah fitur yang menampilkan daftar lengkap buku yang tersedia. Pengguna dapat menjelajahi katalog tersebut untuk mencari buku sesuai kategori, melihat informasi tentang buku, dan juga membaca sinopsis singkat mengenai buku yang dilihat. Pengguna, dapat mengurutkan buku berdasarkan jumlah pembaca atau jumlah disukai, serta pengguna dapat menerapkan filter buku berdasarkan kategori.Pengguna dapat membuka detail buku, yang berisi informasi detail buku, tombol untuk membaca dan meminjam buku, tombol untuk menyukai buku, ulasan buku, pengguna yang sedang membaca buku, dan banyak diskusi buku. 

### 5. Forum Diskusi Buku
*Modul `Forum Diskusi Buku` akan dikerjakan oleh: **Shanahan Danualif Erwin***

Modul Katalog Buku adalah fitur yang menampilkan daftar lengkap buku yang tersedia. Pengguna dapat menjelajahi katalog tersebut untuk mencari buku sesuai kategori, melihat informasi tentang buku, dan juga membaca sinopsis singkat mengenai buku yang dilihat. Pengguna, dapat mengurutkan buku berdasarkan jumlah pembaca atau jumlah disukai, serta pengguna dapat menerapkan filter buku berdasarkan kategori.Pengguna dapat membuka detail buku, yang berisi informasi detail buku, tombol untuk membaca dan meminjam buku, tombol untuk menyukai buku, ulasan buku, pengguna yang sedang membaca buku, dan banyak diskusi buku. 

### 6. Putar Lagu
*Modul `Putar Lagu` akan dikerjakan secara bersama oleh **Seluruh anggota F04***

memungkinkan pengguna untuk memutar atau mendengarkan musik.

### 7. Autentikasi
*Modul `Autentikasi` akan dikerjakan secara bersama oleh **Seluruh anggota F04***

Sistem autentikasi utama aplikasi `README` untuk register, login, dan logout.


## Sumber dataset katalog buku
Sumber dataset katalog buku yang dipakai adalah Project Gutenberg pada tahun 2023 yang sudah divalidasi dengan kriteria:
Buku yang memiliki tepat satu penulis yang diketahui (Bukan Anonymous).
Buku yang menggunakan bahasa inggris.
Buku yang memiliki tipe teks.

Berikut adalah tautan untuk Dataset katalog buku yang sudah divalidasi:
- CSV	: [pg_catalog_2023_F04.csv](https://drive.google.com/file/d/1cjD7FjjnnaZwMqWoGEQ87otuo28jNluj/view?usp=sharing)
- JSON	: [pg_catalog_2023_F04.json](https://drive.google.com/file/d/11IAON9xykmFxcgPN8nAtMAjqrGROxbJ4/view?usp=sharing)

## Role atau peran pengguna
### Guest
Role Guest adalah pengguna yang belum melakukan login saat masuk aplikasi. Guest hanya dapat mengakses module:
1. Katalog Buku, tapi tidak bisa melihat detail buku, hanya judulnya saja.
2. Authentikasi (Register)

### User
Role User adalah pengguna utama di aplikasi ini, user dapat mengakses module:
1. Profil
2. Pinjam Buku
3. Review Buku
4. Katalog Buku
5. Forum Diskusi Buku
6. Putar Lagu
7. Autentikasi