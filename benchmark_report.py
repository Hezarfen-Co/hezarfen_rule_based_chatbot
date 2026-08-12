"""Rol-bazlı kapsamlı benchmark -> test_sonuclari.txt.

Her rol için 50 soru; her biri o rolle motora sorulur ve tam soru+cevap yazılır.
Yeniden üretmek için: python benchmark_report.py
"""
import io
import sys
from collections import Counter
from datetime import datetime, timezone

from src.engine import get_default_engine

e = get_default_engine()

ROLE_ORDER = ["ziyaretci", "veli", "ogrenci", "ogretmen", "yonetici", "admin"]
ROLE_LABEL = {
    "ziyaretci": "ZIYARETCI (Visitor)", "veli": "VELI (Parent)",
    "ogrenci": "OGRENCI (Student)", "ogretmen": "OGRETMEN (Teacher)",
    "yonetici": "YONETICI (Manager)", "admin": "ADMIN",
}

ROLE_QUESTIONS = {
    "ziyaretci": [
        "Hezarfen nedir?", "Bu site ne işe yarar?", "Nasıl üye olurum?",
        "Kayıt nasıl yapılır?", "Giriş nasıl yaparım?", "Şifremi unuttum ne yapmalıyım?",
        "Hesap nasıl açılır?", "Sen kimsin?", "Merhaba", "Roller nelerdir?",
        "Öğretmen ne yapabilir?", "Veli ne yapabilir?", "Karnemi görebilir miyim?",
        "Sınava nasıl girerim?", "Notlarımı göster", "Ders nasıl oluşturulur?",
        "Yoklama nasıl alınır?", "Rehber sayfası nerede?", "Uygulama ücretsiz mi?",
        "Kayıt olurken hangi bilgiler gerekli?", "Giriş yapamıyorum",
        "Öğrenci olarak neler yapabilirim?", "Profilimi düzenleyebilir miyim?",
        "Mesaj gönderebilir miyim?", "Etkinlikleri görebilir miyim?",
        "Bugün hava durumu nasıl?", "Pomodoro nedir?", "Etüt kulübü ne?",
        "Görüşürüz", "Teşekkürler", "Hazerfen nedir?", "Oturum ne kadar sürüyor?",
        "Kullanıcı adımı unuttum", "Sınav sonuçlarımı görebilir miyim?",
        "Nasıl çıkış yaparım?", "Bu platform kimler için?", "Ödev sistemi var mı?",
        "Naber", "Kaydolmadan kullanabilir miyim?", "Ortalamam nasıl hesaplanır?",
        "Yeni ders açmak istiyorum", "Öğrenci kaydetmek istiyorum",
        "Sınav oluşturmak istiyorum", "ben kimim",
        "Okul yönetimiyle nasıl iletişim kurarım?", "Devamsızlığımı nereden görürüm?",
        "Karne ne zaman açıklanır?", "Şifre değiştirme nasıl yapılır?", "Rolüm ne?",
        "Uygulamayı telefondan kullanabilir miyim?",
    ],
    "veli": [
        "Veli olarak neler yapabilirim?", "Çocuğumun notlarını nasıl görürüm?",
        "Çocuğumun karnesini görebilir miyim?", "Çocuğumun devamsızlığını nereden takip ederim?",
        "Bağlı öğrencilerimi nerede görürüm?", "Çocuğumun sınav sonuçları nerede?",
        "Çocuğumun odak/pomodoro kaydını görebilir miyim?", "Çocuğumun ödevlerini görebilir miyim?",
        "Öğretmenle nasıl mesajlaşırım?", "Mesaj kutuma nasıl bakarım?",
        "Çocuğumu nasıl hesabıma bağlarım?", "Birden fazla çocuğumu bağlayabilir miyim?",
        "Çocuğumun sınavına onun yerine girebilir miyim?", "Çocuğumun yerine yoklama işaretleyebilir miyim?",
        "Çocuğumu derse kaydedebilir miyim?", "Çocuğumun notunu değiştirebilir miyim?",
        "Profilimi nasıl düzenlerim?", "Şifremi nasıl değiştiririm?", "Merhaba", "Sen kimsin?",
        "Veli ne demek?", "Çocuğumun ortalaması kaç?", "Çocuğum hangi derslere kayıtlı?",
        "Çocuğumun öğretmenleri kimler?", "Çocuğumun yoklama oranı nedir?",
        "Etkinlikleri görebilir miyim?", "Çocuğumun etkinlik katılımını görebilir miyim?",
        "Kendi sınavlarım nerede?", "Ders oluşturabilir miyim?", "Teşekkürler",
        "Görüşürüz", "Naber", "Rolüm ne?", "Hezarfen nedir?", "Çıkış nasıl yapılır?",
        "Çocuğumun notunu öğretmeni girmemiş, ne yapmalıyım?", "Bugün hava durumu nasıl?",
        "Çocuğumun karnesini indirebilir miyim?", "Çocuğumla ilgili öğretmene mesaj atmak istiyorum",
        "Bildirim ayarları nerede?", "Çocuğumun sınav takvimini görebilir miyim?",
        "Hazerfen'de veli girişi nasıl?", "Çocuğumun devamsızlık raporunu göster", "ben kimim",
        "Çocuğumun ödev notlarını görebilir miyim?", "Veli hesabı sınava girebilir mi?",
        "Öğrenci ekleyebilir miyim?", "Mesaj nasıl gönderilir?",
        "Çocuğumun genel ortalamasını nereden görürüm?", "Kullanıcı rolü değiştirebilir miyim?",
    ],
    "ogrenci": [
        "Karnemi nerede görürüm?", "Notlarım nerede?", "Notlarımı nereden öğrenebilirim?",
        "Ortalamam kaç?", "Sınav sonuçlarım nerede?", "Kaç aldım?", "Sınava nasıl girerim?",
        "Sınav odası nerede?", "Sınavı nasıl bitiririm?", "Sınavdan çıkarsam geri girebilir miyim?",
        "Cevabımı nasıl kaydederim?", "Cevap kağıdıma resim ekleyebilir miyim?",
        "Devamsızlığımı nereden görürüm?", "Yoklama oranım nedir?", "Deftere nasıl not eklerim?",
        "Deftere dosya yükleyebilir miyim?", "Pomodoro nasıl kullanılır?",
        "Odak süremi nereden görürüm?", "Etkinliklere nasıl katılırım?",
        "Etkinlikte kendimi nasıl işaretlerim?", "Mesaj kutuma nasıl bakarım?",
        "Nasıl mesaj gönderirim?", "Profilimi nasıl düzenlerim?", "Şifremi nasıl değiştiririm?",
        "Derslerime nereden bakarım?", "Hangi derslere kayıtlıyım?", "Ödevlerimi nereden görürüm?",
        "Ödevimi nasıl teslim ederim?", "Ödev notumu nereden görürüm?",
        "Sınav oluşturabilir miyim?", "Öğrenci kaydedebilir miyim?", "Yoklama alabilir miyim?",
        "Başka bir öğrencinin notunu görebilir miyim?", "Not verebilir miyim?",
        "Ders oluşturabilir miyim?", "Merhaba", "Sen kimsin?", "Teşekkürler", "Görüşürüz",
        "Naber", "ben kimim", "Rolüm ne?", "Ortalama nasıl hesaplanıyor?",
        "Harf notları neye göre veriliyor?", "Sınav modları neler?", "Karnemi indirebilir miyim?",
        "Bugün hava durumu nasıl?", "Python'da liste nasıl sıralanır?",
        "Hazerfen nasıl kullanılır?", "Kendi notumu görmek istiyorum",
    ],
    "ogretmen": [
        "Sınav nasıl oluşturulur?", "Yeni sınav eklemek istiyorum", "Sınava soru nasıl eklerim?",
        "Seçmeli soru nasıl eklenir?", "Soruya resim ekleyebilir miyim?",
        "Öğrenciye nasıl not veririm?", "Sınavı nasıl notlandırırım?", "Ders nasıl oluşturulur?",
        "Yeni ders açmak istiyorum", "Derse öğrenci nasıl kaydederim?",
        "Sınıf listesini nereden görürüm?", "Ders oturumu nasıl eklenir?", "Yoklama nasıl alınır?",
        "Yoklamayı nasıl güncellerim?", "Öğrencinin notunu nasıl görürüm?",
        "Öğrenci notları sayfası nerede?", "Öğrencinin devamsızlığını nasıl görürüm?",
        "Öğrencinin odak kaydını görebilir miyim?", "Ödev nasıl verilir?",
        "Ödevi nasıl notlandırırım?", "Ödev teslimlerini nereden görürüm?",
        "Mesai girişimi nasıl yaparım?", "Mesai çıkışı nasıl yapılır?",
        "Mesai kaydımı nereden görürüm?", "Sınavı nasıl yayınlarım?",
        "Sınavı taslak olarak kaydedebilir miyim?", "Canlı sınav takibi nerede?",
        "Öğrenciyi sınavdan çıkarabilir miyim?", "Dersi nasıl silerim?",
        "Derse konu/müfredat nasıl eklenir?", "Etkinlik nasıl oluşturulur?",
        "Etkinlik yoklaması nasıl alınır?", "Öğrenciyi etkinliğe nasıl kaydederim?",
        "Sınav sonuçlarını nereden görürüm?", "Sınav istatistiklerine nasıl bakarım?",
        "Kullanıcı rolü değiştirebilir miyim?", "Okul ayarlarını değiştirebilir miyim?",
        "Dönem oluşturabilir miyim?", "Derse öğretmen atayabilir miyim?", "Merhaba",
        "Sen kimsin?", "Teşekkürler", "Rolüm ne?", "Ödev için son teslim tarihi nasıl belirlenir?",
        "Bir öğrencinin karnesini nasıl açarım?", "Sınava kaç deneme hakkı verebilirim?",
        "Yeniden girişe nasıl izin veririm?", "ben kimim", "Hazerfen'de ders nasıl açılır?",
        "Kendi mesai kaydımı başlatırım",
    ],
    "yonetici": [
        "Okul ayarlarını nasıl değiştiririm?", "Sınav türü ağırlıklarını nereden ayarlarım?",
        "Not bantlarını nasıl düzenlerim?", "Yoklama durumlarını değiştirebilir miyim?",
        "Dosya boyut sınırını nasıl ayarlarım?", "Dönem nasıl oluşturulur?",
        "Akademik dönem eklemek istiyorum", "Derse öğretmen nasıl atarım?",
        "Öğretmen atamasını nasıl kaldırırım?", "Sınav nasıl oluşturulur?",
        "Ders nasıl oluşturulur?", "Derse öğrenci nasıl kaydederim?", "Yoklama nasıl alınır?",
        "Öğrenciye not nasıl verilir?", "Öğrencinin notunu nasıl görürüm?", "Ödev nasıl verilir?",
        "Mesai kayıtlarını nasıl düzeltirim?", "Bir personelin mesaisini düzenleyebilir miyim?",
        "Ders oturumunda öğretmeni işaretleyebilir miyim?", "Etkinlik nasıl oluşturulur?",
        "Kullanıcı rolü değiştirebilir miyim?", "Bir kullanıcıyı admin yapabilir miyim?",
        "Kullanıcının profilini düzenleyebilir miyim?", "Veli-öğrenci bağlantısını kurabilir miyim?",
        "Dersi nasıl silerim?", "Dönem silebilir miyim?", "Sınav istatistikleri nerede?",
        "Canlı sınav takibi nasıl yapılır?", "Soru havuzunu nasıl yönetirim?",
        "Öğrenci sorusunu nasıl onaylarım?", "Merhaba", "Sen kimsin?", "Teşekkürler",
        "Rolüm ne?", "Yönetici neler yapabilir?", "Ortalama nasıl hesaplanıyor?",
        "Not bandı nedir?", "Kulüp nasıl oluşturulur?", "Etüt nasıl açılır?",
        "Sınav ağırlığı ortalamayı nasıl etkiler?", "Öğrenci notları sayfası nerede?",
        "Devamsızlık raporlarını nereden görürüm?", "Mesai kaydımı başlatırım", "ben kimim",
        "Bugün hava durumu nasıl?", "Hazarfen ayarları nerede?",
        "Bir öğretmeni yönetici yapabilir miyim?", "Kullanıcıları nasıl listelerim?",
        "Sınav modları neler?", "Yeni kullanıcı ekleyebilir miyim?",
    ],
    "admin": [
        "Kullanıcı rolü nasıl değiştirilir?", "Bir kullanıcıyı öğretmen yapmak istiyorum",
        "Bir kullanıcıyı admin yapabilir miyim?", "Kendi rolümü değiştirebilir miyim?",
        "Bir kullanıcının profilini nasıl düzenlerim?", "Kullanıcıları nasıl listelerim?",
        "Veli-öğrenci bağlantısını nasıl kurarım?", "Bir veliye öğrenci nasıl bağlarım?",
        "Bağlantıyı nasıl kaldırırım?", "Okul ayarlarını nasıl değiştiririm?",
        "Dönem nasıl oluşturulur?", "Derse öğretmen atama nasıl yapılır?",
        "Sınav nasıl oluşturulur?", "Ders nasıl oluşturulur?", "Yoklama nasıl alınır?",
        "Öğrenciye not nasıl verilir?", "Kendi mesai kaydımı nereden başlatırım?",
        "Mesai giriş çıkış nasıl yapılır?", "Not bantlarını nasıl ayarlarım?",
        "Sınav türü ağırlıkları nerede?", "Kullanıcı rollerini kim değiştirebilir?",
        "Bir öğrenciyi veliye bağlayabilir miyim?", "Soru havuzunu yönetebilir miyim?",
        "Öğrenci sorusunu nasıl onaylarım?", "Merhaba", "Sen kimsin?", "Teşekkürler",
        "Rolüm ne?", "ADMIN neler yapabilir?", "ben kimim", "Kendi rolümü ADMIN yapabilir miyim?",
        "Kullanıcı silebilir miyim?", "Ortalama nasıl hesaplanıyor?",
        "Öğrencinin notunu görebilir miyim?", "Öğrencinin karnesini nasıl açarım?",
        "Devamsızlık raporları nerede?", "Bugün hava durumu nasıl?", "Python nasıl öğrenilir?",
        "Hazerfen yönetimi nerede?", "Bir kullanıcının şifresini sıfırlayabilir miyim?",
        "Görüşürüz", "Naber", "Etkinlik oluşturabilir miyim?", "Dönem silebilir miyim?",
        "Kulüp nasıl açılır?", "Kullanıcı adı değiştirilebilir mi?", "Yeni dönem eklemek istiyorum",
        "Sistemdeki tüm kullanıcıları görebilir miyim?", "Öğretmen atamasını kaldırabilir miyim?",
        "Bir kullanıcıyı yönetici yapmak istiyorum",
    ],
}


def run_one(role, q):
    auth = role != "ziyaretci"
    return e.handle({"query": q, "session": {"role": role, "authenticated": auth}})


buf = io.StringIO()
w = buf.write
w("=" * 80 + "\n")
w("CELEBI ASISTAN - ROL BAZLI KAPSAMLI TEST SONUCLARI (her rol icin 50 soru)\n")
w(f"Uretim: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n")
w("Yeniden uretmek icin: python benchmark_report.py\n")
w("=" * 80 + "\n")

for role in ROLE_ORDER:
    qs = ROLE_QUESTIONS[role]
    stats = Counter()
    w("\n\n" + "#" * 80 + "\n")
    w(f"# ROL: {ROLE_LABEL[role]}  ({len(qs)} soru)\n")
    w("#" * 80 + "\n")
    for i, q in enumerate(qs, 1):
        r = run_one(role, q)
        saf = r.get("safety") or {}
        if r.get("fallback"):
            stats["fallback"] += 1
        elif r.get("auth_action"):
            stats["gated"] += 1
        else:
            stats["answered"] += 1
        meta = [f"intent={r.get('intent')}", f"resp_id={r.get('response_id')}",
                f"conf={r.get('confidence'):.2f}"]
        if r.get("auth_action"):
            meta.append(f"auth={r['auth_action']}(gerekli:{r.get('required_role')})")
        if r.get("fallback"):
            meta.append("FALLBACK")
        if saf.get("category") and saf["category"] != "CLEAN":
            meta.append(f"safety={saf['category']}/{saf.get('decision')}")
        if r.get("answers"):
            meta.append(f"answers={len(r['answers'])}")
        w(f"\n{i:2d}. SORU: {q}\n")
        w("    (" + ", ".join(meta) + ")\n")
        w("    CEVAP:\n")
        for line in (r.get("text") or "").split("\n"):
            w("      " + line + "\n")
    w(f"\n--- {ROLE_LABEL[role]} OZET: cevaplandi={stats['answered']}, "
      f"gating={stats['gated']}, fallback/clarify={stats['fallback']} ---\n")

out = buf.getvalue()
with open("test_sonuclari.txt", "w", encoding="utf-8") as fh:
    fh.write(out)
sys.stdout.reconfigure(encoding="utf-8")
total = sum(len(v) for v in ROLE_QUESTIONS.values())
print(f"{total} soru soruldu, {len(out)} karakter -> test_sonuclari.txt")
