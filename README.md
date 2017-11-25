# IF4072_SpeechASR
Simple ASR using HTK

### Supaya jelas kerjaannya dan anggota yang lain bisa follow up, mending setiap commit tertentu ditulis disini cara pake nya.

---

## MFCC
HTK sudah memberikan command untuk konversi :
> HCopy -A -D -T 1 -C wav_config -S codetrain_gen.scp

File `wav_config` sudah ada pada repo, isinya konfigurasi mfcc atau apalah itu.
Yang harus dibuat itu file `.scp` nya.

Di folder `/All_Code` ada script namanya `generate_scp.py` untuk buat file `.scp` nya secara otomatis.

Caranya tinggal taruh file `generate_scp.py` diluar folder `/Dataset` terus jalanin.

Nanti outputnya bakal ada file `codetrain_gen.scp` dan direktori yang bernama `/Dataset_MFCC`.

Sisanya tinggal jalanin HCopy. Hasil dari HCopy (mfcc nya) bakal ada didalem folder `Dataset_MFCC` yang tadi.


## Script to run all
Untuk run semua process dari awal data kosong hingga training HMM:
```
  python run_all.py
```
untuk merubah urutan proses yang dilakukan, edit run_all.py sesuai keinginan.

Pastikan bahwa:
- Dataset berada pada folder ini juga.

## Script to compile DFA grammar
Untuk bikin grammar bisa liat contohnya di folder grammar.
Buka file upnormal.grammar dan upnormal.voca
Harus dicompile ke bentuk upnormal.dict, upnormal.dfa, dan upnormal.term
Script :
```
  perl mkdfa.pl upnormal
```

Pastikan bahwa:
- Kalian sudah install Julius 4.3.1 dari http://julius.osdn.jp/en_index.php#latest_version
- Kalian sudah set PATH ke bin-nya Julius, misalnya C:\Users\ASUS\Desktop\NLP\Tubes Speech\julius-4.3.1-win32bin
