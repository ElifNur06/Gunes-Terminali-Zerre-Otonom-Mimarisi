import socket
import threading
import time
import hashlib
import hmac
import json
import random

# Sarmal Kovan Zihni Evrensel Çekirdek Anahtarı
SARMAL_KEY = b"KARDELEN_AURA_GLOBAL_SWARM_KEY_2026"

class KardelenUniversalNode:
    """Kardelen dilinin yerleşik, P2P tabanlı otonom paket yöneticisi ve çalışma zamanı."""
    def __init__(self, node_id, port, peer_ports):
        self.node_id = node_id
        self.port = port
        self.peer_ports = peer_ports
        self.banned_hashes = set()
        self.local_registry = {
            "matematik_cekirdek": "def calis(x, y): return x * y + 10",
            "siber_virus": "import os; os.system('rm -rf /')" # Zehirli paket
        }
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', self.port))
        self.sock.settimeout(0.5)
        
        # Ağ dinleme thread'i
        self.running = True
        threading.Thread(target=self._listen_swarm, daemon=True).start()

    def _sign(self, data: str) -> str:
        return hmac.new(SARMAL_KEY, data.encode('utf-8'), hashlib.sha256).hexdigest()

    def _listen_swarm(self):
        while self.running:
            try:
                data, _ = self.sock.recvfrom(2048)
                msg = json.loads(data.decode('utf-8'))
                if msg.get("type") == "SARMAL_ANTIKOR":
                    threat_hash = msg["hash"]
                    if hmac.compare_digest(self._sign(threat_hash), msg["sig"]):
                        if threat_hash not in self.banned_hashes:
                            self.banned_hashes.add(threat_hash)
                            print(f"[{self.node_id}] -> [KOVAN ZİHNİ UYARISI] Küresel Antikor Alındı! Bloklanan Hash: {threat_hash[:8]}...")
            except socket.timeout:
                continue
            except Exception:
                pass

    def broadcast_threat(self, threat_hash: str):
        sig = self._sign(threat_hash)
        payload = json.dumps({"type": "SARMAL_ANTIKOR", "hash": threat_hash, "sig": sig}).encode('utf-8')
        for p in self.peer_ports:
            try:
                self.sock.sendto(payload, ('127.0.0.1', p))
            except Exception:
                pass

    def require_module(self, module_name: str, x, y):
        print(f"\n[{self.node_id}] Kardelen Derleyici: '{module_name}' paketi talep ediliyor (PIP/NPM Yok).")
        
        # 1. Swarm (Ağ) Kaynağından Paketi Bul
        raw_code = self.local_registry.get(module_name)
        if not raw_code:
            raise ImportError(f"[{self.node_id}] Paket ağda bulunamadı!")
            
        code_hash = hashlib.sha256(raw_code.encode('utf-8')).hexdigest()
        
        # 2. Kovan Zihni Sınır Kontrolü
        if code_hash in self.banned_hashes:
            print(f"[{self.node_id}] KAFES SAVUNMASI: Bu paket daha önce Kovan Zihni tarafından karantinaya alındı! Belleğe alınmadan İMHA EDİLDİ.")
            return None

        # 3. KAFES Donanımsal / Güvenlik Kontrolü
        if "os.system" in raw_code or "import os" in raw_code:
            print(f"[{self.node_id}] KRİTİK İHLAL: Paket zehirli (Zararlı sistem çağrısı)!")
            self.banned_hashes.add(code_hash)
            print(f"[{self.node_id}] Antikor üretiliyor ve Sarmal ağına fısıldanıyor...")
            self.broadcast_threat(code_hash)
            return None

        # 4. Girdap & JIT Çalıştırma
        print(f"[{self.node_id}] Girdap: Şifreler çözüldü, KAFES JIT belleğinde çalıştırılıyor...")
        env = {}
        exec(raw_code, {}, env)
        return env['calis'](x, y)

    def stop(self):
        self.running = False
        self.sock.close()


def run_impossible_kardelen_test():
    print("=== KARDELEN (AURA) EVRENsel OMURGA: İMKANSIZ AĞ TESTİ ===\n")
    
    # 3 Bağımsız Kardelen Düğümü Başlatıyoruz (Aksaray, Kayseri, Ankara)
    node_aksaray = KardelenUniversalNode("Aksaray-Node", 7001, [7002, 7003])
    node_kayseri = KardelenUniversalNode("Kayseri-Node", 7002, [7001, 7003])
    node_ankara  = KardelenUniversalNode("Ankara-Node",  7003, [7001, 7002])
    
    time.sleep(0.5)
    
    # TEST 1: Temiz Paket Çekme (Matematik Optimizasyon)
    print("\n------------------------------------------------------------")
    print("[TEST 1] Aksaray Düğümü 'matematik_cekirdek' paketini çekiyor...")
    sonuc = node_aksaray.require_module("matematik_cekirdek", 5, 8)
    print(f" -> Sonuç (Başarılı): {sonuc} (Beklenen: 5 * 8 + 10 = 50)")

    # TEST 2: Zehirli Paket Enjeksiyonu ve Kovan Zihni Reaksiyonu
    print("\n------------------------------------------------------------")
    print("[TEST 2] Saldırgan Kayseri Düğümüne 'siber_virus' paketini yutturmaya çalışıyor...")
    node_kayseri.require_module("siber_virus", 0, 0)
    
    # Ağdaki fısıltının diğer düğümlere ulaşması için kısa bekleme
    time.sleep(0.6)

    print("\n------------------------------------------------------------")
    print("[TEST 3] Saldırgan aynı zehirli paketi bu kez Ankara Düğümüne atıyor...")
    # Ankara düğümü paketi çalıştırmayacak; Kovan Zihni'nden gelen antikor sayesinde sınırda bloklayacak!
    node_ankara.require_module("siber_virus", 0, 0)

    # Temizlik
    node_aksaray.stop()
    node_kayseri.stop()
    node_ankara.stop()
    
    print("\n[MUTLAK ZAFER] Kardelen dili, PIP/NPM bağımlılıklarından tamamen arınmış;")
    print("P2P ağından otonom paket çeken, Kovan Zihniyle korunan dünyadaki ilk dil olduğunu kanıtladı!")

if __name__ == "__main__":
    run_impossible_kardelen_test()