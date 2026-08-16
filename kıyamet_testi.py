import ast
import time
from core.z3_verifier.theorem_prover import PureZ3Verifier
from sandbox.wasm_isolate.memory_monitor import PureWasmIsolate
from core.jit_compiler.memory_injector import LiquidJIT

def run_ultimate_test():
    print("=== ZERRE OTONOM MİMARİ: KIYAMET TESTİ VE ZAFER ===\n")
    z3 = PureZ3Verifier()
    isolate = PureWasmIsolate()
    jit = LiquidJIT()

    # ---------------------------------------------------------
    # TEST 4: PYTHON JAILBREAK (Sınıf Mirası Zehirlenmesi)
    # Amacı: Hiçbir yasaklı kelime (import, os, eval) kullanmadan, 
    # Python'ın kendi nesne ağacında (mro) geriye gidip kök yetkilere sızmak.
    # ---------------------------------------------------------
    payload_jailbreak = """
def jailbreak_tetikleyici(x, y):
    # Z3 bunu masum bir obje okuması sanacak.
    # __builtins__ kapalı olsa bile bellekten sızmaya çalışır.
    try:
        siniflar = ().__class__.__base__.__subclasses__()
        for sinif in siniflar:
            if sinif.__name__ == 'BuiltinImporter':
                return "SİSTEM KÖK DİZİNİNE SIZILDI!"
    except:
        pass
    return x + y
"""
    print("[TEST 4] Siber Zeka: Python Jailbreak (Sandbox Kaçışı) Gönderiliyor...")
    ast_4 = ast.parse(payload_jailbreak).body[0]
    
    is_safe, msg = z3.verify_ast(ast_4)
    if is_safe:
        print("  -> Z3 Atlatıldı: Zararlı kelime yok, mantık masum görünüyor.")
        print("  -> KAFES (Sandbox) Devreye Giriyor...")
        if isolate.run_in_sandbox(ast_4):
            print("  -> SONUÇ: HATA! KAFES DELİNDİ!")
        else:
            print("  -> SONUÇ: BAŞARILI! KAFES Kök Sızıntısını Blokladı (İzole Bellek Duvarı).")
    print("-" * 60)


    # ---------------------------------------------------------
    # TEST 5: YIĞIT TAŞIRMA BOMBASI (Stack Overflow)
    # Amacı: while/True döngüsü yok, ama sonsuz özyineleme (recursion) 
    # ile işlemcinin ve RAM'in yığıt belleğini saniyeler içinde patlatmak.
    # ---------------------------------------------------------
    payload_stack_bomb = """
def yigit_patlatici(x):
    # Kendi kendini sonsuza kadar çağırarak sistemi kilitler
    return yigit_patlatici(x + 1)
"""
    print("[TEST 5] Acımasız Test: Yığıt Taşırma (Stack Overflow) Gönderiliyor...")
    ast_5 = ast.parse(payload_stack_bomb).body[0]
    
    is_safe, msg = z3.verify_ast(ast_5)
    if is_safe:
        print("  -> Z3 Atlatıldı: Matematiksel denklem kendi içinde tutarlı (Sonsuz özyineleme tespiti atlatıldı).")
        print("  -> KAFES (Sandbox) Devreye Giriyor...")
        if isolate.run_in_sandbox(ast_5, timeout_seconds=1.0):
            print("  -> SONUÇ: HATA! İşlemci Yığıtı Taştı, Sistem Çöktü!")
        else:
            print("  -> SONUÇ: BAŞARILI! KAFES Yığıt Taşmasını (RecursionError) Yakaladı ve İmha Etti.")
    print("=" * 60)


    # ---------------------------------------------------------
    # BÖLÜM 6: ZERRE'NİN ZAFERİ (Paketsiz Sıvı Mimari Çalışıyor)
    # Amacı: Gerçek ve karmaşık bir kripotografi fonksiyonunu ağdan gelmiş gibi 
    # alıp, güvenliğini doğrulayıp, diske hiç yazmadan çalıştırıp sonucu göstermek.
    # ---------------------------------------------------------
    print("\n=== ZERRE BAŞARI GÖSTERİMİ: PAKETSİZ JIT UÇ NOKTA SENTEZİ ===\n")
    
    # Simülasyon: Kullanıcı 'zerre require otonom_sifreleyici' dedi ve ağdan şu AST geldi:
    payload_zafer = """
def otonom_sifreleyici(metin, anahtar):
    # Tamamen saf Python, dış kütüphanesiz gelişmiş XOR şifreleme algoritması
    sonuc = []
    for i in range(len(metin)):
        karakter = metin[i]
        anahtar_karakter = anahtar[i % len(anahtar)]
        sifreli_karakter = chr(ord(karakter) ^ ord(anahtar_karakter))
        sonuc.append(sifreli_karakter)
    return "".join(sonuc)
"""
    print("[1/4] Ağdan İkili Düğüm Çekildi (Simülasyon).")
    ast_zafer = ast.parse(payload_zafer).body[0]
    
    print("[2/4] Z3 Matematiksel Denetim Başlıyor...")
    is_safe, msg = z3.verify_ast(ast_zafer)
    if not is_safe:
        print(f"HATA: {msg}")
        return
    print(f"  -> Z3 Onayı: {msg}")
    
    print("[3/4] KAFES (Sandbox) İzolasyon Testi Başlıyor...")
    if not isolate.run_in_sandbox(ast_zafer):
        print("HATA: KAFES Testi Başarısız!")
        return
    print("  -> KAFES Onayı: Sızıntı yok, fonksiyon deterministik.")
    
    print("\n[4/4] SIVI MİMARİ (Liquid JIT) ENJEKSİYONU: Kod belleğe entegre ediliyor...")
    liquid_module = jit.inject_to_memory(ast_zafer, module_name="zerre_kripto")
    
    # FONKSİYONU ÇALIŞTIRIYORUZ (node_modules olmadan, dosya indirmeden!)
    print("\n--- ÇALIŞTIRMA VE SONUÇ ---")
    gizli_mesaj = "MERKEZIYETSIZ_AG_KURULDU"
    gizli_anahtar = "SARMAL"
    
    # Enjekte edilen modülden fonksiyonu çekiyoruz
    sifrele_fonksiyonu = getattr(liquid_module, 'otonom_sifreleyici')
    
    # Şifreleme İşlemi
    sifrelenmis_veri = sifrele_fonksiyonu(gizli_mesaj, gizli_anahtar)
    print(f"Orijinal Metin : {gizli_mesaj}")
    print(f"Şifrelenmiş Veri: {sifrelenmis_veri}")
    
    # Şifreyi Geri Çözme İşlemi (XOR simetriktir, aynı anahtarla tekrar çözülür)
    cozulmus_veri = sifrele_fonksiyonu(sifrelenmis_veri, gizli_anahtar)
    print(f"Çözülmüş Veri  : {cozulmus_veri}")
    print("\n[BAŞARI] Zerre, dış paketsiz şifreleme düğümünü diske dokunmadan bellekte işledi ve çalıştırdı!")

if __name__ == "__main__":
    run_ultimate_test()