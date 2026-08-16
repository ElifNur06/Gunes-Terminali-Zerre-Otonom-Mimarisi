from sandbox.wasmtime_isolate import TrueWasmSandbox
import os

def run_hardware_sandbox_test():
    print("=== ZERRE KAFES: GERÇEK DONANIMSAL WASM İZOLASYON TESTİ ===\n")
    
    # Simülasyon: Rust ile derlediğimiz wasm dosyasının byte'larını okuyoruz.
    # (Gerçek senaryoda bu byte'lar ÇAĞRI protokolünden XOR şifresi çözülerek gelecek)
    wasm_dosya_yolu = "zerre_node.wasm"
    
    # Hızlı test için: Eğer .wasm dosyası yoksa, Python'ı durdurma, uyarı ver.
    if not os.path.exists(wasm_dosya_yolu):
        print(f"[UYARI] '{wasm_dosya_yolu}' bulunamadı.")
        print("Bu testi tam çalıştırmak için yukarıdaki Rust kodunu derleyip dizine eklemelisiniz.")
        print("Komut: cargo build --target wasm32-unknown-unknown --release")
        return

    with open(wasm_dosya_yolu, "rb") as f:
        wasm_binary = f.read()

    # KAFES'i Başlat
    sandbox = TrueWasmSandbox()

    # ---------------------------------------------------------
    # TEST 1: ZERRE SIVI MİMARİSİ (Başarılı Çalıştırma)
    # ---------------------------------------------------------
    print("[TEST 1] Ağdan gelen Rust/WASM algoritması KAFES'te çalıştırılıyor...")
    # Ankara (39.9, 32.8) ve Aksaray (38.3, 34.0) koordinatları
    basarili_mi, yanit = sandbox.execute_wasm_payload(wasm_binary, "haversine_mesafe", 39.9, 32.8, 38.3, 34.0)
    
    if basarili_mi:
        print(f"  -> SONUÇ: Başarılı! Hesaplanan Mesafe: {yanit['result']:.2f} km")
        print(f"  -> Harcanan CPU Döngüsü (Yakıt): {yanit['cpu_cycles_used']}")
    else:
        print(f"  -> HATA: {yanit}")
    print("-" * 60)

    # ---------------------------------------------------------
    # TEST 2: DONANIMSAL KESME (Infinite Loop Bombası)
    # ---------------------------------------------------------
    print("\n[TEST 2] Siber Saldırı: WASM içine gizlenmiş Sonsuz Döngü Bombası gönderiliyor...")
    
    # Aynı WASM dosyasındaki zararlı fonksiyonu tetikliyoruz
    basarili_mi, yanit = sandbox.execute_wasm_payload(wasm_binary, "malicious_infinite_loop")
    
    if not basarili_mi:
        print(f"  -> KAFES DEVREYE GİRDİ: {yanit}")
        print("  -> BAŞARI: İşletim sistemi veya ana bellek çökmedi! WASM motoru yakıtı bittiği anda zararlı süreci fiziksel olarak öldürdü.")
    else:
        print("  -> SİSTEM ÇÖKTÜ: Zararlı kod çalıştı.")

if __name__ == "__main__":
    run_hardware_sandbox_test()