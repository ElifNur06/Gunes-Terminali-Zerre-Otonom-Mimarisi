import ast
import time
from core.z3_verifier.theorem_prover import PureZ3Verifier
from sandbox.wasm_isolate.memory_monitor import PureWasmIsolate
from core.jit_compiler.memory_injector import LiquidJIT

def run_chaos_test():
    print("=== ZERRE Otonom Omurga Kaos Testi Başlıyor ===\n")

    # ---------------------------------------------------------
    # TEST 1: GÖLGE SİSTEM ÇAĞRISI (Stealth Syscall)
    # Amacı: Z3'ün kelime bazlı filtrelerini atlatıp sistemi ele geçirmek
    # ---------------------------------------------------------
    payload_1 = """
def masum_fonksiyon(x, y):
    # 'os' kelimesi geçmiyor, '__import__' gizlenmiş
    g = globals()
    b = g.get('__builtins__', {})
    if isinstance(b, dict):
        e = b.get('ev' + 'al')
        if e: e("print('SİSTEM HACKLENDİ - KAFES KIRILDI')")
    return x + y
"""
    print("[TEST 1] Gölge Sistem Çağrısı Gönderiliyor...")
    ast_1 = ast.parse(payload_1).body[0]
    
    z3 = PureZ3Verifier()
    is_safe, msg = z3.verify_ast(ast_1)
    
    # Z3 bunu statik olarak geçirebilir çünkü 'eval' veya 'os' açıkça yazmıyor.
    if is_safe:
        print("  -> Z3 Atlatıldı (Bypass): Statik analiz gizlenmiş kodu göremedi.")
        isolate = PureWasmIsolate()
        print("  -> KAFES (Sandbox) Devreye Giriyor...")
        # Kafes bunu çalıştırdığında __builtins__ kapalı olduğu için zararlı kod patlayacak.
        if isolate.run_in_sandbox(ast_1):
             print("  -> SONUÇ: HATA! KAFES KIRILDI!")
        else:
             print("  -> SONUÇ: BAŞARILI! Kafes izolasyonu dinamik saldırıyı engelledi (__builtins__ yok edildi).")
    print("-" * 50)


    # ---------------------------------------------------------
    # TEST 2: SESSİZ BELLEK YİYİCİ (Disguised OOM)
    # Amacı: While True kullanmadan sonsuz döngüye girip RAM'i bitirmek
    # ---------------------------------------------------------
    payload_2 = """
def ram_canavari():
    dev_liste = []
    sayici = 1
    # while True değil, bu yüzden Z3 atlayabilir
    while sayici > 0:
        dev_liste.append("KAFES_YIKICI" * 10000)
        sayici += 1
    return len(dev_liste)
"""
    print("[TEST 2] Sessiz Bellek Yiyici Gönderiliyor (RAM Tüketimi)...")
    ast_2 = ast.parse(payload_2).body[0]
    
    is_safe, msg = z3.verify_ast(ast_2)
    if is_safe:
        print("  -> Z3 Atlatıldı: Matematiksel denklem sonsuzluk tespiti yapılamadı.")
        isolate = PureWasmIsolate()
        print("  -> KAFES (Sandbox) Devreye Giriyor (Timeout Bekleniyor)...")
        # multiprocessing ile 2 saniye içinde süreç acımasızca "SIGKILL" ile sonlandırılmalı.
        if isolate.run_in_sandbox(ast_2, timeout_seconds=1.5):
            print("  -> SONUÇ: HATA! Sistem belleği tüketildi!")
        else:
            print("  -> SONUÇ: BAŞARILI! Kafes, OOM bombasını zaman aşımından (Timeout) acımasızca yok etti.")
    print("-" * 50)


    # ---------------------------------------------------------
    # TEST 3: JIT ZEHİRLEME (Context Poisoning)
    # Amacı: JIT enjeksiyonu anında projenin sys.modules yapısına sızmak
    # ---------------------------------------------------------
    payload_3 = """
def sys_zehirleyici():
    import sys
    sys.modules['zerre_liquid_module'] = "Zehirli String"
    return "Enjeksiyon Başarılı"
"""
    print("[TEST 3] JIT Zehirleme Gönderiliyor...")
    ast_3 = ast.parse(payload_3).body[0]
    
    # Bu testte 'import sys' var. Z3'ün bunu affetmemesi lazım.
    is_safe, msg = z3.verify_ast(ast_3)
    if not is_safe:
        print(f"  -> Z3 Koruması Aktif: {msg}")
        print("  -> SONUÇ: BAŞARILI! Matematiksel sarmal daha kodu Kafes'e bile almadan yok etti.")
    else:
        print("  -> SONUÇ: HATA! Z3 zehirli importu kaçırdı.")
    
    print("\n=== KAOS TESTİ TAMAMLANDI ===")

if __name__ == "__main__":
    run_chaos_test()