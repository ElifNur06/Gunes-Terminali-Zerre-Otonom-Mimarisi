import ast
import random

class GirdapKnotter(ast.NodeTransformer):
    """Girdap LLVM: Ağacın dallarını matematiksel olarak kördüğüm yapar (Obfuscation)"""
    def __init__(self, key: int):
        self.key = key % 255  # Saf XOR anahtarı
        random.seed(key)

    def visit_Constant(self, node):
        if isinstance(node.value, int):
            # Tam sayıları XOR ile şifrele (Örn: 5 -> 5 ^ 42)
            return ast.Constant(value=node.value ^ self.key)
        return node

    def visit_Name(self, node):
        # Korumalı kelimeleri atla
        if node.id in ['True', 'False', 'None']:
            return node
            
        # Değişken ve fonksiyon isimlerini kriptografik Hex-XOR formatına çevir
        # Örn: 'sqrt' -> '_5b6f6068' (Geçerli ama anlamsız bir değişken adı)
        encrypted_name = "_" + "".join([hex(ord(c) ^ self.key)[2:].zfill(2) for c in node.id])
        return ast.Name(id=encrypted_name, ctx=node.ctx)

    def visit_Module(self, node):
        self.generic_visit(node)
        # Opaque Predicate (Sahte Mantık) Ekleme: 
        # Tersine mühendisleri yanıltmak için çalışmayan ama gerçek gibi duran sahte düğümler ekleriz.
        bogus_code = ast.parse(f"_{random.randint(1000, 9999)} = 0 ^ {self.key}\n").body
        node.body = bogus_code + node.body
        return node


class GirdapUnknotter(ast.NodeTransformer):
    """Girdap LLVM: Hedef JIT belleğinde düğümleri çözer (De-obfuscation)"""
    def __init__(self, key: int):
        self.key = key % 255

    def visit_Constant(self, node):
        if isinstance(node.value, int):
            # Sayıları XOR ile geri çöz
            return ast.Constant(value=node.value ^ self.key)
        return node

    def visit_Name(self, node):
        # İsimleri Hex-XOR formatından orijinal karakterlerine döndür
        if node.id.startswith("_"):
            hex_str = node.id[1:]
            try:
                decrypted_name = "".join([chr(int(hex_str[i:i+2], 16) ^ self.key) for i in range(0, len(hex_str), 2)])
                return ast.Name(id=decrypted_name, ctx=node.ctx)
            except Exception:
                return node
        return node

def run_girdap_simulation():
    print("=== GİRDAP LLVM: DİNAMİK AST GİZLEME VE TERSİNE MÜHENDİSLİK TESTİ ===\n")
    
    # 1. ORİJİNAL KOD (Ticari Sır / Siber Güvenlik Algoritması)
    # Bu kod, basit bir algoritma gibi görünse de bir şirketin veya sistemin kalbi olabilir.
    orijinal_kod = """
gizli_carpan = 5
hedef_deger = 10
sonuc = (hedef_deger * gizli_carpan) + 2
"""
    print("[1] Gönderici: Orijinal AST oluşturuldu (Ticari sır içeriyor).")
    ham_ast = ast.parse(orijinal_kod)

    # 2. GİRDAP MUTASYONU (Obfuscation)
    secret_key = 187 # ÇAĞRI protokolünden gelen dinamik anahtar
    knotter = GirdapKnotter(key=secret_key)
    
    obfuscated_ast = knotter.visit(ham_ast)
    ast.fix_missing_locations(obfuscated_ast)
    
    # Kodu terminalde görebilmek için (ast.unparse Python 3.9+ gerektirir)
    print("\n[2] Girdap Motoru Kodu Düğümledi. Ağa yansıyan polimorfik kod:")
    print("-" * 60)
    girdapli_kod_metni = ast.unparse(obfuscated_ast)
    print(girdapli_kod_metni)
    print("-" * 60)

    # 3. SİBER SALDIRGAN (Tersine Mühendislik Girişimi)
    print("\n[3] Siber Saldırgan: Ağdaki kodu yakaladı ve izinsiz çalıştırmayı deniyor...")
    try:
        # Saldırgan kendi Python yorumlayıcısında çalıştırmayı dener
        exec(compile(obfuscated_ast, filename="<ast>", mode="exec"))
        print("  -> SALDIRGAN BAŞARILI: Kod çalıştı!")
    except Exception as e:
        print(f"  -> GİRDAP SAVUNMASI DEVREDE: Saldırganın sistemi çöktü! Hata: {type(e).__name__} ({e})")
        print("  -> İsimler ve mantık şifreli olduğu için standart derleyiciler bu kodu anlayamaz.")

    # 4. HEDEF ZERRE JIT BELLEĞİ (De-Obfuscation)
    print("\n[4] Alıcı (ZerreVM): Kod belleğe alındı. Çözülüyor...")
    unknotter = GirdapUnknotter(key=secret_key)
    
    temiz_ast = unknotter.visit(obfuscated_ast)
    ast.fix_missing_locations(temiz_ast)
    
    # ZerreVM (Simülasyon için lokal exec) temiz AST'yi çalıştırır
    sandbox_bellek = {}
    exec(compile(temiz_ast, filename="<ast>", mode="exec"), {}, sandbox_bellek)
    
    print("\n[5] MUTLAK BAŞARI: Kod JIT belleğinde orijinal haline dönüp başarıyla hesaplandı!")
    print(f"  -> Orijinal Sonuc: {sandbox_bellek['sonuc']}")
    print(f"  -> Çözülen Gizli Değişken (gizli_carpan): {sandbox_bellek['gizli_carpan']}")

if __name__ == "__main__":
    run_girdap_simulation()