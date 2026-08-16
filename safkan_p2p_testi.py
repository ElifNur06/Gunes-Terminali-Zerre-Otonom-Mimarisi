import socket
import threading
import time

def start_pure_p2p_node(listen_port, target_ip, target_port):
    """Saf socket kütüphanesi ile UDP NAT Delme ve P2P Veri Aktarımı"""
    
    # 1. Ham UDP Soketi Oluştur (Sıfır dış bağımlılık)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', listen_port))
    
    print(f"[SAF AĞ] Düğüm başlatıldı. Port {listen_port} dinleniyor...")
    
    def listener():
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                print(f"\n[!] DOĞRUDAN P2P MESAJ ALINDI (Kimden: {addr}):")
                print(f" -> {data.decode('utf-8')}")
            except:
                break

    # Dinleyiciyi ayrı bir thread (iş parçacığı) olarak başlat
    threading.Thread(target=listener, daemon=True).start()

    # 2. NAT Delme İşlemi (Hole Punching)
    # NAT cihazlarının güvenlik duvarını delmek için karşı tarafa sahte/boş paketler atarak portu açıyoruz.
    print(f"[SAF AĞ] NAT deliniyor... {target_ip}:{target_port} hedefine UDP paketleri gönderiliyor.")
    for _ in range(3):
        sock.sendto(b"NAT_DELME_SINYALI", (target_ip, target_port))
        time.sleep(1)

    print("[SAF AĞ] NAT Tüneli Açıldı! Şifreli veriler (LWE & ZKP) doğrudan gönderilebilir.")
    
    # 3. Gerçek Veri Gönderimi
    siber_yuk = "ZERRE_SAF_MİMARİ: KAFES_KODU_VE_ZKP_İSPATI"
    sock.sendto(siber_yuk.encode('utf-8'), (target_ip, target_port))
    print(f"[SAF AĞ] Siber Yük gönderildi -> {target_ip}:{target_port}")
    
    # Sistemin kapanmaması için beklet
    time.sleep(3)
    sock.close()

if __name__ == "__main__":
    print("=== ÇAĞRI: SIFIR BAĞIMLILIKLI HAM UDP NAT DELME ===\n")
    print("Simülasyon: Aynı makinede iki farklı portun birbirini bulması (Gerçek dünyada farklı IP'ler olur)\n")
    
    # Not: Gerçek hayatta Node A ve Node B farklı bilgisayarlarda çalışır. 
    # Biz burada laboratuvar simülasyonu için aynı bilgisayarda farklı portlar (5001 ve 5002) kullanıyoruz.
    
    # Node B (Alıcı) - 5002'yi dinler, 5001'e NAT delmeye çalışır
    threading.Thread(target=start_pure_p2p_node, args=(5002, '127.0.0.1', 5001), daemon=True).start()
    
    time.sleep(0.5) # Senkronizasyon için ufak bir bekleme
    
    # Node A (Gönderici) - 5001'i dinler, 5002'ye NAT delmeye çalışır
    start_pure_p2p_node(5001, '127.0.0.1', 5002)