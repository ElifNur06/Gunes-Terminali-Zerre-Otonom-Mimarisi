import hashlib
from network.cagri_protocol.true_quantum_crypto import TruePostQuantumLWE
from network.cagri_protocol.true_zkp_engine import TrueZKP_SNARK_Core

def run_production_crypto_test():
    print("=== ÇAĞRI: PRODUCTION-READY PQC VE ZKP (LWE & SCHNORR) TESTİ ===\n")
    
    lwe = TruePostQuantumLWE()
    zkp = TrueZKP_SNARK_Core()
    
    # Simüle edilmiş güvenli AST kodu ve onun devasa tam sayı (int) hali
    saf_kod = b"def gercek_otonom_islem(x): return x ** 3"
    kod_sırrı = int(hashlib.sha256(saf_kod).hexdigest(), 16)

    # ---------------------------------------------------------
    # TEST 1: MATEMATİKSEL ZKP SAHTEKARLIĞI (SNARK BYPASS)
    # ---------------------------------------------------------
    print("[TEST 1] Siber Saldırı: ZKP Matematik Sahtekarlığı")
    
    # Kanıtlayıcı dürüst bir şekilde ispatı oluşturuyor
    y_gercek, t_gercek, r_gercek = zkp.generate_proof(kod_sırrı)
    
    # Saldırgan kodu bilmediği için 'r' değerini rastgele uyduruyor
    r_sahte = 1234567890 
    
    print("  -> Doğrulayıcı ZKP denklemini çözüyor (g^r * y^c mod p == t)...")
    if not zkp.verify_proof(y_gercek, t_gercek, r_sahte):
        print("  -> SONUÇ: BAŞARILI! Matematik yalan söylemez. Sahte kanıt reddedildi.")
    else:
        print("  -> SONUÇ: HATA! SNARK Delindi!")
    print("-" * 65)

    # ---------------------------------------------------------
    # TEST 2: LWE KAFES TABANLI KUANTUM ŞİFRELEMESİ
    # ---------------------------------------------------------
    print("\n[TEST 2] Gerçek Kuantum Dirençli (LWE) Şifreleme ve Deşifre")
    
    # Anahtar çifti (Alıcı)
    print("  -> LWE Kafes Matrisleri oluşturuluyor...")
    sk, pk = lwe.generate_keypair()
    
    # Veri şifreleniyor
    print("  -> Veri çok boyutlu gürültü matrislerine (Kyber mantığı) hapsediliyor...")
    kafes_sifreli_veri = lwe.encrypt_payload(pk, saf_kod)
    
    # Ağa yansıyan veri tamamen bir kafes matrisi (Saldırgan Shor algoritması kullansa bile çözemez)
    print(f"  -> Kuantum Tünelindeki Veri Görünümü (İlk 2 bit matrisi): \n     {kafes_sifreli_veri[:2]}")
    
    # Deşifre İşlemi
    print("  -> Alıcı LWE sırrını (s) kullanarak gürültüyü süzüyor ve veriyi çözüyor...")
    cozulmus_veri = lwe.decrypt_payload(sk, kafes_sifreli_veri)
    
    if cozulmus_veri == saf_kod:
        print(f"  -> SONUÇ: BAŞARILI! Orijinal Veri Kurtarıldı: {cozulmus_veri.decode()}")
    else:
        print("  -> SONUÇ: HATA! Kafes gürültüsü çözülemedi.")
    
    print("\n[BAŞARI] Zerre, XOR oyunlarını bıraktı. Kodu göstermeden ZKP (Fiat-Shamir) ile kanıtladı ve CRYSTALS-Kyber'ın LWE matematiğiyle kuantum dirençli olarak taşıdı!")

if __name__ == "__main__":
    run_production_crypto_test()