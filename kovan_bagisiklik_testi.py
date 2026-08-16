import socket
import threading
import time
import hashlib
import hmac
import json

# Tüm Zerre düğümlerinin birbirini tanıması için ÇAĞRI protokolünün gizli çekirdek anahtarı
SARMAL_SECRET_KEY = b"CODEBYGUNES_HIVE_MIND_CORE_KEY_2026"

class ZerreNode:
    def __init__(self, name, port, peer_ports):
        self.name = name
        self.port = port
        self.peer_ports = peer_ports
        self.banned_hashes = set() # Kovan Zihni Kara Listesi
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', self.port))
        
        # Dinleme işlemini ayrı bir thread'de başlat
        threading.Thread(target=self._listen, daemon=True).start()
        print(f"[{self.name}] Ağa bağlandı (Port: {self.port}). Kovan Zihni ile senkronize.")

    def _hash_code(self, code_str: str) -> str:
        """Kodun AST formunun (veya metninin) değiştirilemez SHA-256 kimliğini çıkarır."""
        return hashlib.sha256(code_str.encode('utf-8')).hexdigest()

    def _sign_payload(self, payload: str) -> str:
        """Kovan Zihnine gönderilecek alarmı HMAC ile imzalar (Sahte alarmları önlemek için)"""
        return hmac.new(SARMAL_SECRET_KEY, payload.encode('utf-8'), hashlib.sha256).hexdigest()

    def _listen(self):
        """Ağdan gelen SARMAL ALARMLARINI (Gossip) dinler."""
        while True:
            try:
                data, _ = self.sock.recvfrom(2048)
                message = json.loads(data.decode('utf-8'))
                
                if message.get("type") == "SARMAL_ALARM":
                    threat_hash = message["hash"]
                    signature = message["signature"]
                    
                    # Alarmın gerçekten Zerre ağından gelip gelmediğini doğrula
                    expected_sig = self._sign_payload(threat_hash)
                    if hmac.compare_digest(expected_sig, signature):
                        if threat_hash not in self.banned_hashes:
                            self.banned_hashes.add(threat_hash)
                            print(f"\n[KOVAN ZİHNİ - {self.name}] Küresel tehdit sinyali alındı! Hash Bloklandı: {threat_hash[:8]}...")
                    else:
                        print(f"\n[!] {self.name}: Sahte/Geçersiz alarm sinyali reddedildi!")
            except Exception:
                pass

    def broadcast_threat(self, threat_hash: str):
        """Tespit edilen zararlı kodun hash'ini tüm Zerre ağına fısıldar (Gossip Protocol)"""
        signature = self._sign_payload(threat_hash)
        payload = json.dumps({
            "type": "SARMAL_ALARM",
            "hash": threat_hash,
            "signature": signature
        }).encode('utf-8')
        
        for p in self.peer_ports:
            self.sock.sendto(payload, ('127.0.0.1', p))

    def evaluate_code(self, code_str: str):
        """Ağdan gelen veya istenen bir kodu değerlendirir."""
        code_hash = self._hash_code(code_str)
        
        # 1. Aşama: KOVAN ZİHNİ (Küresel Bağışıklık Kontrolü)
        if code_hash in self.banned_hashes:
            print(f"[{self.name}] SAVUNMA: Bu kod daha önce Kovan Zihni tarafından mimlendi! KAFES'e sokulmadan sınırda İMHA EDİLDİ.")
            return False

        # 2. Aşama: LOKAL KAFES (Donanımsal İzolasyon Simülasyonu)
        print(f"[{self.name}] Kod Kovan Zihninde temiz görünüyor. Lokal KAFES'e alınıyor...")
        if "os.system" in code_str or "while True" in code_str:
            print(f"[{self.name}] DİKKAT! Lokal KAFES, kodda SİBER SALDIRI (Zehir) tespit etti. Çalıştırma durduruldu!")
            
            # 3. Aşama: ANTİKOR ÜRETİMİ (Kovan Zihnine Bildir)
            self.banned_hashes.add(code_hash)
            print(f"[{self.name}] Kovan Zihni Antikoru Üretildi. Diğer düğümler uyarılıyor...")
            self.broadcast_threat(code_hash)
            return False
            
        print(f"[{self.name}] Kod güvenli. Çalıştırıldı.")
        return True

def run_hive_mind_simulation():
    print("=== SARMAL: KOVAN ZİHNİ KÜRESEL BAĞIŞIKLIK TESTİ ===\n")
    
    # 3 Farklı şehri (Node) simüle ediyoruz
    node_aksaray = ZerreNode("Aksaray (Node A)", 6001, [6002, 6003])
    node_kayseri = ZerreNode("Kayseri (Node B)", 6002, [6001, 6003])
    node_ankara  = ZerreNode("Ankara (Node C)", 6003, [6001, 6002])
    
    time.sleep(1)
    
    siber_saldiri_kodu = "import os; os.system('rm -rf /')"
    
    print("\n------------------------------------------------------------")
    print("[1. SALDIRI DALGASI] Saldırgan hedef olarak Aksaray'ı (Node A) seçti.")
    node_aksaray.evaluate_code(siber_saldiri_kodu)
    
    # Kovan zihninin fısıldaması (UDP) için 1 saniye bekle
    time.sleep(1)
    
    print("\n------------------------------------------------------------")
    print("[2. SALDIRI DALGASI] Saldırgan aynı virüsü Kayseri'ye (Node B) gönderiyor...")
    # Kayseri (Node B) kodu kendisi incelemeyecek, Kovan Zihninden gelen antikor ile anında bloklayacak!
    node_kayseri.evaluate_code(siber_saldiri_kodu)

    print("\n------------------------------------------------------------")
    print("[3. SALDIRI DALGASI] Saldırgan Ankara'yı (Node C) deniyor...")
    node_ankara.evaluate_code(siber_saldiri_kodu)
    
    print("\n[MUTLAK ZAFER] Kovan Zihni (Sarmal) sayesinde 1 fire verilse bile (lokal KAFES tuttu), tüm dünya saniyeler içinde bağışıklık kazandı!")

if __name__ == "__main__":
    run_hive_mind_simulation()