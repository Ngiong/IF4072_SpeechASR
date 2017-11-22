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
