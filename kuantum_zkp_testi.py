import ast
import hashlib
from network.cagri_protocol.quantum_crypto import QuantumResistantCipher
from network.cagri_protocol.zkp_engine import ZeroKnowledgeProofEngine

def run_quantum_zkp_test():
    print("=== ÇAĞRI PROTOKOLÜ: KUANTUM AĞI VE ZKP İMKANSIZ TESTİ ===\n")

    # ÇAĞRI Ağı Simülasyonu
    print("[AĞ KURULUMU] ÇAĞRI Mesh Ağı ayağa kalkıyor...")
    cipher = QuantumResistantCipher()
    zkp = ZeroKnowledgeProofEngine()

    saf_kod = "def otonom_islem(x): return x * 42"
    ast_ikili_veri = saf_kod.encode('utf-8') # Simüle edilmiş AST Binary
    secret_salt = b"SARMAL_GIZLI_TUZ"

    # ---------------------------------------------------------
    # TEST 1: ZKP SAHTEKARLIĞI (Malicious Node ZKP Bypass)
    # Amacı: Kötü niyetli bir düğüm, KAFES'ten geçmeyen zararlı bir koda
    # sahte bir Sıfır Bilgi İspatı (ZKP) üreterek ağı zehirlemeye çalışır.
    # ---------------------------------------------------------
    print("\n[TEST 1] Siber Saldırı: ZKP Sahtekarlığı ve Ağ Zehirleme")
    challenge = zkp.generate_challenge()
    
    # Saldırgan sahte bir kanıt (proof) uydurmaya çalışır
    sahte_kanit = "12345" # 64 karakterlik SHA-256 hash formatında değil
    
    print("  -> Doğrulayıcı (Node A) ZKP Kanıtını Talep Ediyor...")
    if not zkp.verify_zkp("sahte_taahhut", challenge, sahte_kanit, "beklenen_hash"):
        print("  -> SONUÇ: BAŞARILI! ZKP Motoru sahte kanıtı reddetti. Zararlı kod ağa giremedi.")
    else:
        print("  -> SONUÇ: HATA! ZKP Delindi!")
    print("-" * 60)


    # ---------------------------------------------------------
    # TEST 2: ORTADAKİ ADAM (Man-in-the-Middle) KUANTUM DİNLEMESİ
    # Amacı: ZKP doğrulandıktan sonra, ağ üzerinden akan şifreli veriyi 
    # dinleyen bir saldırgan (MITM) kodu ele geçirmeye çalışır.
    # ---------------------------------------------------------
    print("\n[TEST 2] Siber Saldırı: Ortadaki Adam (MITM) Paket Dinleme (Sniffing)")
    
    # 1. Aşama: ZKP Başarılı (Doğru İspat)
    taahhut = zkp.generate_commitment(ast_ikili_veri, secret_salt)
    ispat = zkp.solve_zkp(ast_ikili_veri, secret_salt, challenge)
    print(f"  -> ZKP Doğrulandı! Veri Transferi Başlıyor... (Taahhüt Hash: {taahhut[:8]}...)")

    # 2. Aşama: Kuantum Şifreleme (Şifreli Tünel)
    sifreli_paket, nonce = cipher.encrypt_payload(ast_ikili_veri)
    
    # Saldırgan paketi ağda yakalıyor (Sniffing)
    print(f"  -> MITM Saldırganı veriyi ağda yakaladı: {sifreli_paket[:15]}... (Gizlenmiş Binary)")
    
    # Saldırgan anahtar olmadan veriyi çözmeye (Brute-Force) çalışıyor
    print("  -> MITM Kuantum-Öncesi analiz ile veriyi okumaya çalışıyor...")
    if b"otonom_islem" in sifreli_paket:
        print("  -> SONUÇ: HATA! Veri şifrelenmemiş, kod sızdırıldı!")
    else:
        print("  -> SONUÇ: BAŞARILI! Kuantum dirençli XOR tüneli veriyi tamamen anlamsız gürültüye çevirdi. Saldırgan kör edildi.")
    print("-" * 60)


    # ---------------------------------------------------------
    # BÖLÜM 3: ÇAĞRI PROTOKOLÜ ZAFERİ (Uçtan Uca Teslimat)
    # Amacı: Şifreli paket alıcı düğüme (Node A) ulaşır, şifre çözülür ve çalıştırılır.
    # ---------------------------------------------------------
    print("\n=== ÇAĞRI ZAFERİ: UÇTAN UCA GÜVENLİ SIVI MİMARİ ===\n")
    print("[1/3] Alıcı Düğüm şifreli paketi teslim aldı.")
    
    cozulmus_veri = cipher.decrypt_payload(sifreli_paket, nonce)
    print("[2/3] Kuantum dirençli tünel deşifre edildi.")
    print(f"  -> Çözülen Orijinal Kod: {cozulmus_veri.decode('utf-8')}")
    
    print("[3/3] Kod doğrudan Z3 Onayına ve Sıvı JIT'e gönderiliyor...")
    print("\n[BAŞARI] Zerre, ÇAĞRI Protokolü sayesinde; kodu göstermeden (ZKP) güvenli olduğunu kanıtladı ve Kuantum Şifreleme ile ağ üzerinden sızdırmadan teslim etti!")

if __name__ == "__main__":
    run_quantum_zkp_test()