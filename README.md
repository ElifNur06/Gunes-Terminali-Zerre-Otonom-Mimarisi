# ☀️ Güneş Terminali & Zerre Otonom Mimarisi
> **Geliştirici / Marka:** codebygunes  
> **Çekirdek:** Zerre Otonom Mimarisi  
> **Dil Ekosistemi:** Kardelen (Aura)  

---

## 🚀 Proje Vizyonu ve Mimari Özet

**Güneş Terminali**, geleneksel yazılım dünyasının hantal bağımlılıklarından (`PIP`, `NPM`), disk şişiren dosya yapıverinden ve güvenlik açıklarından tamamen arınmış; **sıfır bağımlılıklı, otonom, kuantum dirençli ve kovan zihniyle bağışıklık kazanan** devrimci bir siber ekosistemdir.

Sistemin kalbinde yer alan **Zerre Çekirdeği**, doğal dilden gelen niyetleri okur, P2P ağı üzerinden kodları otonom çeker, diske hiç dokunmadan bellekte (`Liquid JIT`) çalıştırır ve donanımsal izolasyon katmanlarıyla (KAFES / WASM) korur.

---

## 🛠️ Temel Katmanlar ve Özellikler

### 1. 🛡️ KAFES (Donanımsal & Yazılımsal İzolasyon)
* **Pure VM & WASM Düzeyi Koruma:** Kodlar asla işletim sisteminin doğrudan kaynaklarına erişemez. 
* **Yakıt (Fuel) Mekanizması:** Sonsuz döngüye (`While True`) veya bellek şişirme (OOM / Stack Overflow) saldırılarına giren süreçler, yakıtı bittiği an donanımsal olarak durdurulur ve işletim sistemi korunur.
* **Global Kısıtlaması:** `globals` ve `__builtins__` gibi tehlikeli yansıtma (reflection) nesneleri imha edilerek dinamik sızma girişimleri engellenir.

### 2. 🌀 Girdap LLVM (Polimorfik Kod Gizleme)
* **Tersine Mühendislik Direnci:** Ticari sır içeren kritik algoritmalar ve mantık blokları, polimorfik yapıya büründürülerek okunamaz hale getirilir.
* **Bellek Üstü Çözümleme:** Şifreli kodlar yalnızca yetkili alıcının JIT belleğinde orijinal haline dönüştürülür.

### 3. 🧠 SARMAL (Kovan Zihni Küresel Bağışıklık)
* **Dağıtık P2P Ağı:** Düğümler (Aksaray, Kayseri, Ankara vb.) birbiriyle senkronize çalışır.
* **Sıfır Gün Bağışıklığı:** Bir düğüm ilk kez zararlı bir yazılımla (zehirli paket) karşılaştığında yerel KAFES bunu yakalar, anında **Antikor (Hash)** üretir ve Sarmal ağına fısıldar. Diğer tüm düğümler dosyayı açmadan sınırda imha eder.

### 4. 🌐 ÇAĞRI Protokolü (PQC & ZKP)
* **Kuantum Dirençli Şifrevleme (LWE):** CRYSTALS-Kyber mantığıyla çok boyutlu gürültü matrislerine hapsedilen veriler, kuantum bilgisayarların kırıcılığına karşı tamamen güvenlidir.
* **Sıfır Bilgi Kanıtı (ZKP / Schnorr):** Kodun içeriği veya veri açığa çıkmadan, güvenli ve deterministik olduğu matematiksel olarak kanıtlanır.
* **Ham UDP NAT Delme:** Merkezi sunuculara ihtiyaç duymadan, doğrudan soket seviyesinde P2P tünelleri kurar.

### 5. 🎯 Zerre Niyet Motoru & Self-Opt JIT
* **Semantik Router:** Klasik terminal komutları yerine doğal dildeki istekleri (`"İki GPS noktası arasındaki mesafeyi hesapla"`) okur ve ağdan ilgili algoritmayı otonom çeker.
* **Self-Opt JIT Engine:** İşlemci mimarisini analiz ederek kodları donanım seviyesinde optimize eder (Constant Folding) ve saniyeler içinde çalıştırır.

---

## 🧪 Kaos ve Gerçeklik Testleri

Sistem, en sert sızma ve çökertme senaryolarıyla test edilmiş ve başarıyla tescillenmiştir:

1. **Kaos Testi (`chaos_tester.py`):** Statik analizleri atlatan gölge sistem çağrıları, OOM bombaları ve JIT zehirleme girişimleri KAFES ve Sarmal tarafından etkisiz hale getirildi[cite: 1].
2. **Kıyamet Testi (`kiyamet_testi.py`):** Stack Overflow (Yığıt Taşması) saldırıları donanımsal kesmelerle engellendi; kodlar diske hiç yazılmadan tamamen RAM üzerinde (`Liquid JIT`) çalıştırıldı.
3. **Kuantum & ZKP Testi (`kuantum_gerceklik_testi.py`):** Sahte kanıtlar ZKP motoru tarafından reddedildi, LWE matrisleri ile kuantum dirençli veri transferi kanıtlandı.
4. **Kardelen (Aura) Dil Testi (`kardelen_gerceklik_testi.py`):** PIP/NPM bağımlılıklarını tamamen reddeden, dünyadaki ilk otonom paket çeken dil mimarisi test edildi.

---

## 💻 Kullanım Örneği (Güneş Terminali)

Terminal başlatıldığında tüm modüller otomatik olarak devreye girer:

```bash
codebygunes@gunes:~$ Boolean Master oyunundaki karmaşık mantık kapılarını (AND/OR/XOR) inceleyip, Quine-McCluskey algoritması ile en aza indirgeyen otonom bir çözümleyici kur.
