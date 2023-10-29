# BUKOO

## Daftar Isi

- [Pendahuluan](#Pendahuluan)
- [Cerita aplikasi serta manfaatnya](#Cerita-Aplikasi)
- [Daftar modul yang akan diimplementasikan](#Daftar-Modul)
- [Sumber dataset katalog buku](#Sumber-Dataset)
- [Role pengguna dan deskripsinya](#Role-Pengguna-dan-Deskripsinya)

## Pendahuluan

Proyek ini ditujukan sebagai tugas proyek tengah semester kelompok B03 pada mata kuliah PBP 2023/2024.

Nama Anggota Kelompok B03:
- Muzaki Ahmad Ridho Azizy 		(2206824924)
- Ilham Abdillah Alhamdi 		(2206081194)
- Asadilhaq Elqudsi Prabowo 	(2206083041)
- Wahyu Aji Aruma Sekar Puri 	(2206816115)
- Fayya Salwa Azheva 			(2206826192)




## Cerita Aplikasi 

Aplikasi **Bukoo** merupakan platform yang dirancang untuk pecinta buku yang ingin menjelajahi lebih koleksi-koleksi buku yang ada di dunia. Meskipun pengguna tidak dapat membaca buku secara langsung di aplikasi ini, mereka dapat menemukan informasi rinci tentang berbagai koleksi buku, mencari koleksi buku berdasarkan judul, kategori, dan genre, membuat daftar favorit, dan membuat review mengenai suatu buku, melihat leaderboards buku favorit dan leaderboard user aktif, dan melihat rekomendasi buku berdasarkan preferensi pengguna.

## Daftar Modul
### 1. Modul Koleksi Buku
 Dalam modul koleksi buku, pengguna dapat melihat berbagai data koleksi buku. Selain itu, user juga dapat melihat detail masing-masing buku yang berisi data       seperti judul, author, foto cover buku, sinopsis, dan review. User nantinya juga dapat mencari buku berdasarkan author, tahun buku rilis, judul, dan kategori     seperti genre. Pada modul ini, role author dapat mengajukan buku baru dan mengelola buku yang telah ditambahkan.

### 2. Modul Review
Kami berencana untuk membuat sebuah kolom untuk user memberikan pendapat tentang sebuah buku yang sudah mereka baca dan ditampilkan dalam data bukunya.

### 3. Modul Profile User
  - Profile
      Dalam modul ini, pengguna dapat melihat data dirinya dalam aplikasi ini dan dapat mengubahnya. 
  - Bookmark
      Selain itu, modul ini akan berfungsi untuk user ketika ada sebuah buku yang menarik untuk dibaca atau dibeli dari sumber lain nantinya. User dapat                 menandai buku yang menarik tersebut untuk dapat dilihat nanti jadi tidak perlu untuk mencarinya lagi.

### 4. Modul Leaderboard
Modul leaderboard berkaitan dengan modul review dimana akan menampilkan data buku-buku yang paling banyak di review (Recommended atau Not Recommended)             berdasarkan total akumulasi review yang diberikan oleh user. 

### 5. Modul Dashboard Admin
Pada modul ini Admin dapat melakukan verifikasi terhadap buku yang diajukan oleh Author. Admin dapat menyetujui atau menolak pengajuan buku tersebut.


## Sumber Dataset

1. [Gramedia](https://www.gramedia.com/categories/buku) 
2. [Periplus](https://www.periplus.com/c/1/books)
3. [Goodreads](https://www.goodreads.com/) 

Modul koleksi buku kami datanya diambil dari tiga sumber yang telah dicantumkan di atas dan akan menjadi sebuah perpustakaan digital yang komprehensif. Melalui Gramedia, modul ini mempersembahkan visualisasi yang menggugah, dengan foto-foto menawan dari berbagai buku, disertai sinopsis yang menggoda imajinasi serta ulasan otentik dari pengguna yang mendorong pembaca ke dalam dunia cerita. Periplus menyempurnakan koleksi ini dengan menawarkan jendela ke literatur global, memperluas cakrawala dengan buku-buku impor dan karya-karya monumental dari penulis internasional, sembari menyajikan detail penting seperti nama penulis, tahun penerbitan, dan segmentasi fiksi serta non-fiksi. 

 Sementara itu, Goodreads memperkaya platform dengan insight mendalam, menampilkan ulasan tajam dan peringkat buku yang tercurah langsung dari hati komunitas pembaca global, memfasilitasi pengguna dalam menemukan karya yang resonan dengan jiwa dan selera mereka. Uniknya, ulasan ini bersifat murni dari pengguna, menjamin keaslian dan kejujuran setiap pendapat, sehingga menciptakan ruang dialog yang otentik dan terpercaya dalam website kami. Fitur pencarian yang terintegrasi memungkinkan eksplorasi yang mulus berdasarkan beragam kriteria—judul, penulis, tahun terbit, kategori, genre, dan lebih lagi—menjadikan pencarian buku bukan hanya proses, tetapi sebuah petualangan. Dengan menyatukan kekayaan informasi dari ketiga sumber ini, modul koleksi buku kami tidak hanya berfungsi sebagai repositori informasi, tetapi sebagai kompas personal bagi pembaca untuk menemukan, menggali, dan jatuh cinta pada dunia buku yang luas dan beragam.


  
## Role Pengguna dan Deskripsinya

### Author (Penulis)
 - Mengajukan karya buku
   Penulis mempromosikan karya ke dalam aplikasi Bukoo serta memberikan informasi lengkap mengenai buku, seperti judul, sinopsis, dan genre.
 - Mengelola karya buku
   Penulis dapat memperbarui dan mengelola informasi buku, termasuk sinopsis, sampul buku, atau detail lainnya.
### Readers (Pembaca)
  - Memberikan penilaian 
      Pembaca dapat memberikan penilaian buku tersebut dapat direkomendasikan (Recommended) atau tidak (Not Recommended). 
  - Berpartisipasi dalam memberi ulasan
      Pembaca mampu untuk memberikan ulasan terhadap buku-buku yang mereka baca. Ulasan dapat membantu calon pembaca lainnya memutuskan apakah ingin membaca             buku tersebut atau tidak. Pembaca juga dapat melakukan diskusi terkait buku-buku tertentu dan dapat membahas tentang cerita, karakter, tema, atau aspek           lain dari buku tersebut secara satu arah.
### Guest (Pengguna Umum / _Logout User_)
  - Melihat koleksi buku
      Guest dapat menjelajahi koleksi buku dalam aplikasi Bukoo. Mereka dapat mecari buku berdasarkan judul, penulis, dan genre. Selain itu, mereka dapat               melihat detail buku seperti, sinopsis, penulis, dan tahun rilis. 
  - Melihat ulasan buku
      Guest dapat melihat ulasan yang telah diberikan oleh readers terhadap buku-buku dalam koleksi. Dengan ini, guest mendapatkan wawasan tambahan tentang buku         sebelum memutuskan apakah akan membacanya atau tidak. Namun, pengguna ini tidak dapat mem-bookmarks dan tidak bisa mengulas buku.
### Admin (Pengembang Aplikasi Bukoo)
  - Mengelola pengajuan buku
    Memiliki tanggung jawab untuk meninjau pengajuan buku yang diajukan oleh penulis. Selanjutnya melakukan pengecekan apakah sudah sesuai pedoman aplikasi.
  - Menjaga keamanan aplikasi
      Admin memastikan bahwa aplikasi tetap aman dan terhindar dari potensi masalah keamanan atau pelanggaran data.




