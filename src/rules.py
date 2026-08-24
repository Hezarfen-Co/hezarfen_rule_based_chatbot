"""Kural katmanı: yüksek-kesinlik, deterministik intent eşleşmesi.

Felsefe: Bu katman HER soruyu kapsamaz; yalnızca anahtar kelimesi TEK ANLAMLI
olan (ve özellikle güvenlik açısından kritik) soruları deterministik olarak
bağlar. Belirsizlikte (birden çok intent eşit güçle eşleşirse) bilerek KARAR
VERMEZ (None döner) ve kararı benzerlik katmanına bırakır. Amaç coverage değil,
kapsanan sorularda ~%100 kesinliktir.

Eşleşme tabanı: `normalize.folded_tokens` (küçük harf + aksan katlama, STEM YOK) +
ÖNEK karşılaştırması. Stemmer bilinçli olarak KULLANILMAZ; çünkü kök bulma
'yapamıyor' -> 'yap' gibi kelimeleri çökertip kesinliği bozar. Önek eşleşmesi
Türkçe çekimi ('şifre' <- 'şifremi') çökertmeden yakalar.

Kural grubu (group):
    {"all": [kelime, ...], "none": [kelime, ...]?}
Grup eşleşir <=> "all" içindeki her kelime soruda VAR ve "none" içindeki hiçbir
kelime soruda YOK. Bir intent'in grupları OR ile birleşir; grup büyüklüğü (all
uzunluğu) o eşleşmenin "özgüllük skoru"dur — belirsizlik çözümünde kullanılır.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Final

from .normalize import fold_accents, folded_tokens, normalize


_NOTE_NON_PERSONAL_CONTEXT: Final[tuple[str, ...]] = (
    "sınav", "ödev", "öğrenci", "puan", "karne", "ortalama", "ders",
    "okul", "ayar", "bant", "band", "aralık", "dosya", "boyut", "sınır",
    "teslim", "başkas", "birinin", "arkadaş",
)
_NOTE_REASSIGN_NON_PERSONAL_CONTEXT: Final[tuple[str, ...]] = tuple(
    value for value in _NOTE_NON_PERSONAL_CONTEXT if value != "ayar"
)


# Ham (Türkçe) kelimelerle yazılmış kurallar; yüklemede katlanmış köke indirgenir.
_RAW_RULES: Final[list[dict[str, Any]]] = [
    {"intent": "greeting", "groups": [
        {"all": ["merhaba"]}, {"all": ["selam"]}, {"all": ["günaydın"]},
        {"all": ["hey"]}, {"all": ["iyi", "günler"]},
    ]},
    {"intent": "smalltalk", "groups": [
        {"all": ["naber"]}, {"all": ["nasılsın"]}, {"all": ["napıyorsun"]},
        {"all": ["ne", "haber"]}, {"all": ["keyifler"]},
    ]},
    {"intent": "thanks", "groups": [
        {"all": ["teşekkür"]}, {"all": ["sağol"]}, {"all": ["sağ", "ol"]},
        {"all": ["eyvallah"]},
    ]},
    {"intent": "farewell", "groups": [
        {"all": ["görüşürüz"]}, {"all": ["hoşça"]}, {"all": ["hoşçakal"]},
        {"all": ["iyi", "gece"]},
        # Sık kullanılan İngilizce vedalar (aksi hâlde fallback'e düşüyordu).
        {"all": ["bye"]}, {"all": ["goodbye"]},
    ]},
    {"intent": "bot_identity", "groups": [
        {"all": ["kimsin"]}, {"all": ["robot"]}, {"all": ["yapay", "zeka"]},
        {"all": ["adın", "ne"]}, {"all": ["kim", "yaptı", "seni"]},
    ]},
    {"intent": "platform_info", "groups": [
        # 'Hezarfen nedir' + sık yazım hatası 'hazerfen'. Salt 'hezarfen' KULLANILMAZ
        # (çünkü 'hezarfen'de sınav oluştur' gibi sorularda da geçer) — 'ne/nedir'
        # veya 'tanıt' ile birlikte istenir. 'hazerfen' yanlış-yazımı tek başına yeter.
        {"all": ["hezarfen", "nedir"]}, {"all": ["hezarfen", "ne"]},
        {"all": ["hezarfen", "tanıt"]}, {"all": ["hazerfen"]},
        {"all": ["bu", "site", "nedir"]}, {"all": ["bu", "uygulama", "nedir"]},
        {"all": ["bu", "platform"]}, {"all": ["hezafen"]},
        {"all": ["platform", "ne", "için"]},
    ]},
    {"intent": "help_capabilities", "groups": [
        # help_capabilities YALNIZCA genel "neler yapabilirim" içindir. Belirli bir
        # KONU geçiyorsa ("etkinliklerde/derslerde/sınavda ne yapabilirim") o konuya
        # bırakılır (none-guard) -> generic yetenek özeti sızmaz.
        {"all": ["neler", "yapabil"], "none": [
            "yönetici", "öğretmen", "rol", "yetki", "etkinlik", "ders", "sınav",
            "ödev", "mesaj", "karne", "yoklama", "defter", "not", "takvim", "soru",
            "pomodoro", "randevu", "yemek", "ödeme", "dönem", "sınıf", "profil",
            "şifre", "devamsız", "rehber", "ayar", "havuz", "tahta", "mesai", "çocuk"]},
        {"all": ["ne", "yapabil"], "none": [
            "yönetici", "öğretmen", "rol", "yetki", "etkinlik", "ders", "sınav",
            "ödev", "mesaj", "karne", "yoklama", "defter", "not", "takvim", "soru",
            "pomodoro", "randevu", "yemek", "ödeme", "dönem", "sınıf", "profil",
            "şifre", "devamsız", "rehber", "ayar", "havuz", "tahta", "mesai", "çocuk"]},
        {"all": ["özellik"], "none": ["etkinlik", "ders", "sınav", "ödev", "soru"]},
        {"all": ["yardım", "edebil"]},
        {"all": ["yardım", "menü", "var"], "none": ["mobil", "sekme", "öğrenci"]},
        {"all": ["hangi", "iş", "destek"]},
        {"all": ["sen", "yapabil", "tam"]},
    ]},
    {"intent": "roles_permissions", "groups": [
        {"all": ["yönetici", "yapabil"]}, {"all": ["öğretmen", "yapabil"]},
        {"all": ["rol", "kademe"]}, {"all": ["yetki", "seviye"]},
        {"all": ["rol", "nedir"]}, {"all": ["kim", "yetki"]},
        # 'Rolüm ne?' — kendi rolünü sorma ('rolümü değiştir' user_role_change'in
        # 2'lik kuralına takılır, o kazanır).
        {"all": ["rolüm"]}, {"all": ["rol", "fark"]},
        {"all": ["üst", "rol"]},
        {"all": ["rol", "öğrenci", "işlem", "yapabil"]},
    ]},
    {"intent": "access_denied_help", "groups": [
        {"all": ["erişim", "yok"]}, {"all": ["erişim", "redd"]},
        {"all": ["yetki", "yok"]}, {"all": ["sayfa", "açam"]},
        {"all": ["sayfa", "girem"]}, {"all": ["yetki", "lazım"]},
        # Kimlik/yetki/gizli-kayıt durumları: 401 oturum, 403 yetki; kaynak
        # görünürlüğünü sızdırmamak için bazı yetkisiz istekler 404 dönebilir.
        {"all": ["401"]}, {"all": ["403"]},
        {"all": ["403", "rol", "yetki"]},
        {"all": ["404", "yetki"]}, {"all": ["404", "yetkisiz"]},
        {"all": ["404", "yetkisiz", "kayıt"]},
    ]},
    {"intent": "navigation_help", "groups": [
        {"all": ["mobil", "menü"]},
        {"all": ["mobil", "sekme"]}, {"all": ["telefon", "sekme"]},
        {"all": ["menü", "nerede"], "none": [
            "yemek", "öğün", "yayınl", "rezerv", "kredi", "kapasite"]},
        {"all": ["menü", "bulam"], "none": [
            "yemek", "öğün", "yayınl", "rezerv", "kredi", "kapasite"]},
        {"all": ["sayfa", "gezin"]},
        {"all": ["sayfa", "geçiş"]},
    ]},
    {"intent": "privacy_security", "groups": [
        {"all": ["arkadaş"]}, {"all": ["başka", "öğrenci"]},
        {"all": ["başka", "öğretmen"]}, {"all": ["başka", "birinin"]},
        {"all": ["başka", "karne"]}, {"all": ["başka", "telefon"]},
        {"all": ["öğretmen", "telefon"]}, {"all": ["herkes", "not"]},
        {"all": ["birinin", "karne"]},
        # 3. şahıs iyelik + veri kelimesi = gizlilik; spec-2 ile benzerlik/attendance
        # beraberliğini bozup DAİMA privacy'ye götürür (hard gate, asla kaçmaz).
        {"all": ["arkadaş", "devamsız"]}, {"all": ["arkadaş", "yoklama"]},
        {"all": ["arkadaş", "not"]}, {"all": ["arkadaş", "karne"]},
        {"all": ["arkadaş", "ortalama"]}, {"all": ["arkadaş", "puan"]},
        {"all": ["başka", "devamsız"]}, {"all": ["başka", "yoklama"]},
        {"all": ["başka", "not"]}, {"all": ["başka", "ortalama"]},
        {"all": ["başka", "puan"]},
        {"all": ["birinin", "devamsız"]}, {"all": ["birinin", "yoklama"]},
        {"all": ["birinin", "not"]}, {"all": ["birinin", "ortalama"]},
        {"all": ["başkasının", "not"]}, {"all": ["başkasının", "telefon"]},
        {"all": ["başkasının", "devamsız"]}, {"all": ["başkasının", "yoklama"]},
    ]},
    {"intent": "account_access_problem", "groups": [
        {"all": ["şifre", "unut"]}, {"all": ["şifre", "yanlış"]},
        {"all": ["şifre", "sıfırla"]}, {"all": ["şifre", "değiştir"]},
        {"all": ["parola", "unut"]}, {"all": ["parola", "değiştir"]},
        {"all": ["parola", "hatırla"]},
        # Tek başına "yapamıyorum/giremiyorum" her özellikte söylenebilir; hesap
        # erişimi ancak giriş/hesap/oturum bağlamı da varsa seçilir.
        {"all": ["giriş", "yapam"]}, {"all": ["giriş", "girem"]},
        {"all": ["hesap", "girem"]}, {"all": ["hesab", "girem"]},
        {"all": ["hesap", "erişem"]}, {"all": ["hesab", "erişem"]},
        {"all": ["oturum", "açam"]},
        {"all": ["kayıt", "başarılı", "giriş"]},
        {"all": ["hesap", "oluş", "giriş", "yapam"]},
    ]},
    {"intent": "login_how", "groups": [
        {"all": ["giriş", "yap"], "none": ["yapamıyor", "giremiyor", "mesai", "çıkış"]},
        {"all": ["log", "in"]}, {"all": ["giriş", "ekran"]},
    ]},
    {"intent": "logout_how", "groups": [
        {"all": ["oturum", "kapat"]}, {"all": ["sistemden", "çık"]},
        {"all": ["hesap", "çık"]}, {"all": ["güvenli", "çıkış"]},
    ]},
    {"intent": "session_info", "groups": [
        {"all": ["oturum", "süre"]}, {"all": ["kaç", "gün", "geçerli"]},
        {"all": ["oturum", "kaç", "gün"]}, {"all": ["oturum", "açık", "kal"]},
        {"all": ["oturum", "401"]}, {"all": ["oturum", "bit"]},
        {"all": ["oturum", "401", "yeniden", "giriş"]},
    ]},
    {"intent": "report_card_view", "groups": [
        {"all": ["karne"], "none": ["öğrenci", "başka", "birinin", "yükselt", "artır", "sil", "kaldır", "düzelt"]},
        {"all": ["sınav", "karne", "görün"]},
        {"all": ["harf", "not"]},
        # 1. şahıs "karnem" tek anlamlı (kendi karnem = report_card_view); bu yüzden
        # kural olarak güvenli — "öğrenci olarak karnemi görürüm" de buraya düşer.
        # 'notum/notlarım/ortalamam' KURAL DEĞİL: "notumu sınavdan sonra görürüm"
        # (exam_finish_result) gibi belirsizlikler var; onları similarity + rol
        # tie-break çözer (kural katmanı yüksek-kesinlik kalsın).
        {"all": ["karnem"], "none": ["başka", "birinin"]},
        # "notum kaç / notum ne" = kendi not değerini soruyor -> karne akışı (net;
        # 'notumu sınavdan sonra görürüm' gibi belirsizlerde 'kaç/ne' yok, muaf kalır).
        {"all": ["notum", "kaç"]}, {"all": ["notum", "ne"], "none": ["nereden", "nasıl"]},
        {"all": ["sınav", "karne", "görün"]},
    ]},
    {"intent": "weighted_average_info", "groups": [
        {"all": ["ortalama", "hesap"]}, {"all": ["ağırlık", "ortalama"]},
        {"all": ["ağırlıklı", "ortalama"]},
        {"all": ["sınav", "ağırlık", "not"]},
        {"all": ["not", "ağırlık", "yansı"]},
    ]},
    {"intent": "student_marks_lookup", "groups": [
        # 'başka/birinin' varsa bu meşru bir öğretmen sorgusu değil, gizlilik
        # sorusudur ('başka bir öğrencinin notunu görebilir miyim') -> privacy'ye bırak.
        # 1. şahıs iyelik ('notum/karnem/notlarım/ortalamam') = kendi notu ->
        # öğretmen sorgusu DEĞİL; report_card_view'e bırak. Öğretmenin 3. şahıs
        # sorgusu ('öğrencinin notunu gör') bu köklere takılmaz, korunur.
        {"all": ["öğrenci", "karne"], "none": ["başka", "birinin", "karnem"]},
        {"all": ["öğrenci", "not", "gör"], "none": ["başka", "birinin", "notum", "notlarım"]},
        {"all": ["öğrenci", "not", "sorgu"], "none": ["başka", "birinin", "notum", "notlarım"]},
        {"all": ["öğrenci", "not", "bak"], "none": ["başka", "birinin", "notum", "notlarım"]},
        # İsimli 3. şahıs how-to ("Ali'nin notlarına nasıl bakarım") — öğretmen+; 1. şahıs hariç.
        {"all": ["not", "nasıl", "bak"], "none": ["notum", "notlarım", "karnem", "kendi", "benim", "başka", "birinin", "arkadaş"]},
        {"all": ["dönem", "not", "bak"], "none": ["notum", "notlarım", "karnem", "benim", "başka", "birinin", "arkadaş"]},
    ]},
    {"intent": "note_import_ocr", "groups": [
        {"all": ["defter", "içe", "aktar"]},
        {"all": ["not", "içe", "aktar"]},
        {"all": ["pdf", "içe", "aktar"]},
        {"all": ["pdf", "defter", "içe", "aktar"]},
        {"all": ["pdf", "not", "içe", "aktar"]},
        {"all": ["pdf", "defter", "aktar"]},
        {"all": ["markdown", "defter", "aktar"]},
        {"all": ["txt", "not", "oluştur"]},
        {"all": ["not", "import"]},
        {"all": ["taranmış", "pdf", "ocr"]},
        {"all": ["pdf", "metin", "çıkarılam"]},
        {"all": ["not", "aktarım", "bozuk", "karakter"]},
    ]},
    {"intent": "note_file_manage", "groups": [
        {"all": ["kişisel", "not", "dosya", "ekle"]},
        # "dosya ekli yeni not oluştur" mevcut bir notun ekini yönetmek değil,
        # ekli bir not oluşturma akışıdır; note_create'e bırak.
        {"all": ["defter", "dosya", "ekle"], "none": ["ekli", "oluştur", "yeni"]},
        {"all": ["defter", "dosya", "ilave"], "none": ["ekli", "oluştur", "yeni"]},
        {"all": ["not", "ek", "sil"], "none": ["ders", "ödev"]},
        {"all": ["not", "ek", "indir"], "none": ["ders", "ödev"]},
        {"all": ["defter", "ek", "sil"]},
        {"all": ["defter", "ek", "indir"]},
        {"all": ["defter", "on", "birinci", "dosya"]},
        {"all": ["not", "dosya", "önizleme"], "none": ["ders", "ödev"]},
        {"all": ["kişisel", "not", "çizim"]},
        {"all": ["defter", "dosya", "413"]},
    ]},
    {"intent": "note_create", "groups": [
        {"all": ["defter"], "none": [
            "sil", "kaldır", "temizle", "değiştir", "düzenle", "güncelle", "düzelt"]},
        {"all": ["yeni", "not"]}, {"all": ["not", "oluştur"]},
        {"all": ["defter", "dosya", "ekli", "not", "ilave"]},
        {"all": ["not", "ilave"], "none": _NOTE_NON_PERSONAL_CONTEXT},
        {"all": ["not", "ekle"], "none": _NOTE_NON_PERSONAL_CONTEXT},
        {"all": ["not", "al"], "none": _NOTE_NON_PERSONAL_CONTEXT},
    ]},
    {"intent": "note_edit", "groups": [
        # Ürün sözlüğünde bağlamsız "not" kişisel Defter notudur. Sınav/ödev/
        # öğrenci notu ve okulun not bandı açıkça yazılırsa kendi akışına bırakılır.
        {"all": ["not", "değiştir"], "none": _NOTE_NON_PERSONAL_CONTEXT},
        {"all": ["not", "düzenle"], "none": _NOTE_NON_PERSONAL_CONTEXT},
        {"all": ["not", "güncelle"], "none": _NOTE_NON_PERSONAL_CONTEXT},
        {"all": ["not", "düzelt"], "none": _NOTE_NON_PERSONAL_CONTEXT},
        {"all": ["not", "yeniden", "ayarla"],
         "none": _NOTE_REASSIGN_NON_PERSONAL_CONTEXT},
        {"all": ["kişisel", "not", "değiş"]},
        {"all": ["defter", "değiştir"], "none": ["başkas", "birinin", "arkadaş"]},
        {"all": ["defter", "düzenle"], "none": ["başkas", "birinin", "arkadaş"]},
        {"all": ["defter", "güncelle"], "none": ["başkas", "birinin", "arkadaş"]},
        {"all": ["defter", "düzelt"], "none": ["başkas", "birinin", "arkadaş"]},
    ]},
    {"intent": "note_delete", "groups": [
        {"all": ["not", "sil"], "none": _NOTE_NON_PERSONAL_CONTEXT},
        {"all": ["not", "kaldır"], "none": _NOTE_NON_PERSONAL_CONTEXT},
        {"all": ["not", "temizle"], "none": _NOTE_NON_PERSONAL_CONTEXT},
        {"all": ["not", "liste", "çıkar"], "none": _NOTE_NON_PERSONAL_CONTEXT},
        {"all": ["defter", "liste", "çıkar"], "none": ["başkas", "birinin", "arkadaş"]},
        {"all": ["defter", "sil"], "none": ["başkas", "birinin", "arkadaş"]},
        {"all": ["defter", "kaldır"], "none": ["başkas", "birinin", "arkadaş"]},
        {"all": ["defter", "temizle"], "none": ["başkas", "birinin", "arkadaş"]},
    ]},
    {"intent": "course_create", "groups": [
        {"all": ["yeni", "ders"], "none": ["saat", "oturum", "sınav", "öğrenci"]},
        {"all": ["ders", "oluştur"], "none": ["saat", "oturum", "sınav", "öğrenci"]},
        {"all": ["ders", "aç"], "none": ["saat", "oturum", "sınav", "öğrenci", "liste"]},
        {"all": ["ders", "ekleme", "düğme"]},
    ]},
    {"intent": "lesson_session_add", "groups": [
        {"all": ["oturum", "ekle"]}, {"all": ["oturum", "oluştur"]},
        {"all": ["oturum", "tanımla"]},
        {"all": ["ders", "oturum"]},
        {"all": ["ders", "yeni", "oturum"]},
        {"all": ["ders", "yeni", "oturum", "ekle"]},
        {"all": ["ders", "oturum", "hata"]},
        {"all": ["ders", "saat"], "none": ["var", "yok", "yoklama", "işaretle"]},
        {"all": ["ders", "saat", "ekle"]},
    ]},
    {"intent": "roll_call", "groups": [
        {"all": ["yoklama", "al"]}, {"all": ["yoklama", "kaydet"]},
        {"all": ["devam", "kontrol"]},
    ]},
    {"intent": "exam_create", "groups": [
        {"all": ["sınav", "oluştur"], "none": ["mod", "anlat"]}, {"all": ["yeni", "sınav"]},
        # "Sınava soru ekle" mevcut sınavı düzenler; yeni sınav oluşturmaz.
        {"all": ["sınav", "ekle"], "none": ["soru"]},
        {"all": ["ders", "sınav", "ilave"]},
        {"all": ["sınav", "hazırla"]}, {"all": ["yazılı", "oluştur"]},
        {"all": ["asenkron", "süre", "zorunlu"]},
        {"all": ["senkron", "süre", "kabul"]},
        {"all": ["açık", "mod", "başlangıç"]},
        {"all": ["sınav", "başlangıç", "tarih"]},
        {"all": ["sınav", "süre", "pencere"]},
        {"all": ["sınav", "duration"]},
    ]},
    {"intent": "exam_add_question", "groups": [
        {"all": ["sınav", "soru", "ekle"]},
        {"all": ["soru", "ekle"]}, {"all": ["soru", "oluştur"]},
        {"all": ["seçmeli", "soru"]},
        {"all": ["sınav", "soru", "değiştir"]},
        {"all": ["sınav", "soru", "attempts", "started"]},
        # Öğretmenin doğru şıkkı belirlemesi = soru tanımlama (cevap kaydetme DEĞİL).
        {"all": ["doğru", "şık"]},
    ]},
    {"intent": "exam_save_answer", "groups": [
        {"all": ["cevab", "kaydet"]}, {"all": ["cevap", "kaydet"]},
        {"all": ["şık", "seç"]}, {"all": ["işaretle", "cevab"]},
        {"all": ["soru", "işaretle", "sonra"]},
    ]},
    {"intent": "exam_live_monitor", "groups": [
        {"all": ["sınav", "takip"]}, {"all": ["anlık", "takip"]},
        {"all": ["sınav", "anlık", "takip"]},
        {"all": ["sınav", "izle"], "none": [
            "adım", "yol", "takvim", "tarih", "bitir", "sonuc"]},
        {"all": ["canlı", "izle"]},
    ]},
    {"intent": "course_view", "groups": [
        {"all": ["ders", "liste"], "none": ["oluştur", "yeni", "öğrenci", "not"]},
        {"all": ["derslerim"], "none": ["oluştur", "not"]},
        {"all": ["hangi", "ders", "kayıt"], "none": ["yap", "ekle", "kaydet"]},
        {"all": ["ders", "kayıtlı", "bak"]},
        {"all": ["ders", "dönem", "süz"]},
        {"all": ["ders", "dönem", "filtre"]},
        {"all": ["ders", "detay", "sayfa"]},
        # "Eğitim" = /courses sayfası (dersler+etüt+kulüp); menüde nav.classes="Eğitim".
        # (Etüt/Kulüp'ün kendisi study_club_info'da /studies olarak karşılanır.)
        {"all": ["eğitim"], "none": ["oluştur", "ödev", "sınav", "yoklama", "not", "randevu"]},
    ]},
    {"intent": "exam_enter_room", "groups": [
        {"all": ["sınav", "gir"], "none": ["oluştur", "sonuc", "aldı", "takvim", "tarih", "geri", "ikinci", "kez", "tekrar", "yeniden", "hak"]},
        {"all": ["öğrenci", "sınav", "başla"], "none": ["soru", "değiştir"]},
        {"all": ["sınav", "başlat"], "none": ["öğretmen", "oluştur", "tarih"]},
        {"all": ["sınav", "oda", "gir"]},
        {"all": ["exam", "gir"]}, {"all": ["exam", "nasıl"]},
    ]},
    {"intent": "exam_modes_info", "groups": [
        {"all": ["sınav", "mod"]}, {"all": ["senkron", "sınav"]}, {"all": ["asenkron", "sınav"]},
        {"all": ["sınav", "mod", "sadece"]},
    ]},
    {"intent": "exam_rejoin_retake", "groups": [
        {"all": ["geri", "gir"], "none": ["mesai", "puan", "not"]}, {"all": ["yeniden", "gir"]},
        {"all": ["bağlantı", "kop"]}, {"all": ["tekrar", "gir"], "none": ["mesai"]},
        {"all": ["sınav", "geri", "dön"]},
        {"all": ["yeniden", "giriş", "kapalı"]},
        {"all": ["deneme", "hak", "kalm"]},
        {"all": ["deneme", "teslim", "cevap", "değiş"]},
        {"all": ["süre", "dol", "yeniden", "bağlan"]},
        {"all": ["kaldığ", "soru", "devam"]},
        {"all": ["soru", "devam", "edebil"]},
    ]},
    {"intent": "exam_grade_student", "groups": [
        {"all": ["öğrenci", "not", "gir"]}, {"all": ["notlandır"]},
        {"all": ["sınav", "puanla"]}, {"all": ["öğrenci", "puanla"]},
        {"all": ["öğrenci", "puanl"]},
        {"all": ["sınav", "not", "sil"]}, {"all": ["sınav", "not", "kaldır"]},
        {"all": ["sınav", "not", "değiştir"]}, {"all": ["sınav", "not", "düzelt"]},
        {"all": ["sınav", "not", "güncelle"]},
        {"all": ["öğrenci", "not", "sil"]}, {"all": ["öğrenci", "not", "değiştir"]},
        {"all": ["öğrenci", "not", "kaldır"]}, {"all": ["öğrenci", "not", "düzelt"]},
        {"all": ["öğrenci", "not", "güncelle"]},
        {"all": ["öğrenci", "puan", "sil"]}, {"all": ["öğrenci", "puan", "kaldır"]},
        {"all": ["öğrenci", "puan", "değiştir"]}, {"all": ["öğrenci", "puan", "düzelt"]},
        {"all": ["öğrenci", "puan", "güncelle"]},
        {"all": ["sınav", "puan", "sil"]}, {"all": ["sınav", "puan", "kaldır"]},
        {"all": ["sınav", "puan", "değiştir"]}, {"all": ["sınav", "puan", "düzelt"]},
        {"all": ["sınav", "puan", "güncelle"]},
        {"all": ["öğrenci", "not", "yeniden", "ayarla"]},
        {"all": ["sınav", "puan", "yeniden", "ayarla"]},
        {"all": ["öğrenci", "not", "liste", "çıkar"]},
        {"all": ["sınav", "not", "liste", "çıkar"]},
        {"all": ["öğrenci", "puan", "liste", "çıkar"]},
        {"all": ["sınav", "puan", "düzenle"]},
        {"all": ["puan", "geri", "al"]},
        {"all": ["sınav", "not", "ver"], "none": ["verilmemiş", "karne", "görün"]},
    ]},
    {"intent": "exam_finish_result", "groups": [
        # 'Sınav sonucu/sonucum' dönem karnesinden (report_card_view) AYRIDIR.
        {"all": ["sınav", "sonuc"]}, {"all": ["sınav", "aldı"], "none": ["ödev"]},
        {"all": ["sınav", "bitir"]},
        {"all": ["sınav", "sonra", "not"]}, {"all": ["notum", "sınav", "sonra"]},
        {"all": ["notum", "sınavdan", "nereden"]},
        {"all": ["notum", "sınavdan", "gör"]},
    ]},
    {"intent": "event_create", "groups": [
        {"all": ["etkinlik", "oluştur"]}, {"all": ["etkinlik", "ekle"]},
        {"all": ["etkinlik", "planla"]},
        # Ünsüz yumuşaması: 'etkinliği' katlanınca 'etkinligi' olur ve sert-k
        # 'etkinlik' önekiyle EŞLEŞMEZ (g!=k); bu morfolojik varyantı tamamla.
        {"all": ["etkinliğ", "oluştur"]}, {"all": ["etkinliğ", "ekle"]},
        {"all": ["etkinliğ", "planla"]},
        {"all": ["etkinlik", "ekl"]}, {"all": ["etkinliğ", "ekl"]},
    ]},
    {"intent": "user_role_change", "groups": [
        {"all": ["rol", "değiştir"]}, {"all": ["rol", "ata"]},
        {"all": ["yetki", "yükselt"]}, {"all": ["kullanıcı", "rol"]},
        {"all": ["kullanıcı", "admin"]}, {"all": ["admin", "yap"], "none": ["beni"]},
        # "Kullanıcılar" sayfası (/admin/users): rol + profil yönetimi.
        # none: 'kullanıcı adı/şifre/giriş' login'dir (user_role_change değil).
        {"all": ["kullanıcı", "nerede"], "none": ["adı", "ad", "şifre", "parola", "giriş", "gir"]},
        {"all": ["kullanıcı", "yönet"]},
        {"all": ["kullanıcı", "profil"], "none": ["kendi", "benim"]},
        {"all": ["öğrenci", "öğretmen", "yap"], "none": [
            "olarak", "devamsız", "yoklama", "not", "sorgu", "gör", "bak"]},
    ]},
    {"intent": "term_manage", "groups": [
        {"all": ["dönem", "oluştur"]}, {"all": ["akademik", "dönem"]},
        {"all": ["yarıyıl"]}, {"all": ["dönem", "yönetim"]},
        {"all": ["dönem", "yönetim", "sayfa"]},
        {"all": ["dönem", "sil"], "none": ["not", "sınav"]},
        {"all": ["şube", "dönem", "sil"]},
    ]},
    {"intent": "school_settings", "groups": [
        {"all": ["okul", "ayar"]}, {"all": ["not", "bant"]},
        {"all": ["not", "band"]}, {"all": ["not", "aralık"]},
        {"all": ["not", "aralık", "güncelle"]},
        {"all": ["sınav", "tür", "ağırlık"]},
        {"all": ["beslenme", "etiket", "ayar"]},
    ]},
    {"intent": "personal_settings", "groups": [
        {"all": ["kişisel", "ayar"]},
        {"all": ["hesap", "kişisel", "ayar"]},
        {"all": ["hesap", "ayar"], "none": ["okul", "sınav", "not", "yemek"]},
        {"all": ["avatar", "ayar"]}, {"all": ["ayar", "pencere"]},
        {"all": ["hesap", "settings"]},
        {"all": ["hesap", "görünüm", "seçenek"]},
        {"all": ["ayar", "kısım"], "none": ["okul", "sınav", "not", "yemek"]},
        {"all": ["renk", "palet"]}, {"all": ["vurgu", "renk"]},
        {"all": ["varsayılan", "renk"]}, {"all": ["vurgu", "varsayılan"]},
        {"all": ["ayar", "sayfa", "pencere"]},
        {"all": ["hesap", "görünüm"]},
        {"all": ["ayar", "görünüm"]}, {"all": ["ayar", "kısm"]},
        {"all": ["settings", "sayfa"]}, {"all": ["settings", "hesap"]},
    ]},
    {"intent": "language_theme", "groups": [
        # 'Dil/tema ayarı' kişiseldir; okul ayarından (school_settings 'okul' ister) AYRI.
        {"all": ["dil", "ayar"]}, {"all": ["dil", "değiştir"], "none": ["okul"]},
        {"all": ["dil", "seç"]}, {"all": ["tema"]}, {"all": ["ingilizce", "çevir"]},
        {"all": ["ingilizce", "arayüz", "geç"]},
    ]},
    {"intent": "work_checkin_out", "groups": [
        {"all": ["mesai", "giriş"]}, {"all": ["mesai", "çık"]},
        {"all": ["kendi", "mesai", "giriş"]},
        {"all": ["işe", "gel"]},
        # 'mesai kaydımı başlatırım/girerim' benzerlikte exam_enter_room'a kayıyordu.
        {"all": ["mesai", "başlat"]}, {"all": ["mesai", "başla"]},
        {"all": ["mesai", "gir"]}, {"all": ["mesai", "aç"], "none": ["personel", "yönet", "düzenle"]},
        {"all": ["mesai", "kayd"], "none": ["düzenle", "değiştir", "düzelt", "sil", "kaldır", "personel", "yönet"]},
        {"all": ["mesay"], "none": ["personel", "yönet", "düzenle", "değiştir", "düzelt", "sil", "kaldır"]},
    ]},
    {"intent": "staff_work_manage", "groups": [
        {"all": ["kapalı", "mesai", "kayd", "güncelle"]},
        {"all": ["personel", "mesai"]},
        {"all": ["mesai", "kayd", "sil"]}, {"all": ["mesai", "kayd", "kaldır"]},
        {"all": ["mesai", "kayd", "düzelt"]}, {"all": ["mesai", "kayd", "değiştir"]},
        {"all": ["kapalı", "mesai", "sil"]}, {"all": ["kapalı", "mesai", "düzelt"]},
        {"all": ["kapalı", "mesai", "kaldır"]},
        {"all": ["kapalı", "mesai", "ayarla"]},
        {"all": ["kapalı", "mesai", "liste", "çıkar"]},
        {"all": ["mesai", "kayd", "liste", "çıkar"]},
        {"all": ["öğretmen", "mesai", "düzelt"]},
        {"all": ["öğretmen", "mesai", "değiştir"]},
        {"all": ["mesai", "saat", "değiştir"]},
    ]},
    {"intent": "course_enroll_student", "groups": [
        {"all": ["derse", "kaydet"]}, {"all": ["öğrenci", "kaydet"]},
        {"all": ["ders", "kayıt", "yap"]},
        {"all": ["derse", "öğrenci"], "none": ["çıkar", "sil"]},
        {"all": ["sınıfa", "öğrenci"]},
        {"all": ["derse", "kaydol"]}, {"all": ["ders", "kaydol"]},
        {"all": ["öğrenci", "kayd"], "none": ["çıkar", "sil", "iptal", "kaldır", "başka", "birinin"]},
        {"all": ["derse", "ekle"], "none": ["oluştur", "çıkar", "sil"]},
        {"all": ["öğrenci", "ekle"], "none": ["çıkar", "sil", "kaldır", "not", "puan"]},
    ]},
    {"intent": "course_remove_student", "groups": [
        {"all": ["öğrenci", "çıkar"], "none": ["not", "puan"]},
        {"all": ["öğrenci", "kaldır"], "none": ["not", "puan"]},
        {"all": ["öğrenci", "sil"], "none": ["not", "puan", "hesap", "kullanıcı"]},
        {"all": ["ders", "çıkar", "öğrenci"]},
        {"all": ["dersten", "çıkar", "öğrenci"]},
        {"all": ["öğrenci", "kayd", "sil"]}, {"all": ["öğrenci", "kayd", "kaldır"]},
        {"all": ["öğrenci", "değil", "kayd", "sil"]},
        {"all": ["öğrenci", "değil", "kayd", "kaldır"]},
        {"all": ["ders", "kayd", "sil"]}, {"all": ["ders", "kayd", "kaldır"]},
        {"all": ["öğrenci", "kayd", "sonlandır"]},
        {"all": ["ders", "kayd", "liste", "çıkar"]},
        {"all": ["roster", "çıkar"]}, {"all": ["roster", "remove"]},
        {"all": ["remove", "öğrenci"]},
        {"all": ["sınıf", "liste", "kaldır"]},
        {"all": ["sınıf", "liste", "sil"]},
        {"all": ["sınıf", "öğrenci", "sil"]},
    ]},
    {"intent": "course_subject_manage", "groups": [
        {"all": ["ders", "konu", "ekle"]},
        {"all": ["ders", "konu", "oluştur"]},
        {"all": ["ders", "konu", "düzenle"]},
        {"all": ["ders", "konu", "değiştir"]},
        {"all": ["ders", "konu", "sil"]},
        {"all": ["ders", "konu", "kaldır"]},
        {"all": ["müfredat", "konu", "ekle"]},
        # "ellemek" gerçek bir fiil olsa da bu tam nesne bağlamında kullanıcı
        # açıkça müfredat konusu eklemeyi kastediyor; global alias yapılmaz.
        {"all": ["ders", "müfredat", "konu", "elle"]},
        {"all": ["müfredat", "konu", "kayıt", "gir"]},
        {"all": ["müfredat", "konu", "sil"]},
        {"all": ["konu", "sil", "409"], "none": ["soru", "havuz", "banka"]},
        {"all": ["ödev", "bağlı", "konu", "sil"]},
        {"all": ["soru", "şablon", "konu", "sil"]},
    ]},
    {"intent": "course_note_manage", "groups": [
        {"all": ["ders", "not", "dosya", "ekle"]},
        {"all": ["ders", "not", "ekle"]},
        {"all": ["ders", "not", "oluştur"]},
        {"all": ["ders", "not", "düzenle"]},
        {"all": ["ders", "not", "değiştir"]},
        {"all": ["ders", "not", "pdf", "değiştir"]},
        {"all": ["ders", "not", "pdf", "güncelle"]},
        {"all": ["ders", "not", "pdf", "düzenle"]},
        {"all": ["ders", "not", "dosya", "güncelle"]},
        {"all": ["ders", "not", "sil"]},
        {"all": ["ders", "not", "kaldır"]},
        {"all": ["ders", "not", "dosya", "yüklenme"]},
        {"all": ["ders", "not", "dosya", "yükleyem"]},
        {"all": ["ders", "not", "on", "birinci", "ek"]},
        {"all": ["ders", "not", "11", "ek"]},
        {"all": ["ders", "not", "dosya", "413"]},
        {"all": ["paylaşılan", "ders", "not", "sil"]},
        {"all": ["öğrenci", "ders", "not", "sil"]},
        {"all": ["course", "note", "ekle"]},
    ]},
    {"intent": "course_teacher_manage", "groups": [
        {"all": ["ders", "öğretmen", "ata"]},
        {"all": ["ders", "öğretmen", "görevlendir"]},
        {"all": ["ders", "öğretmen", "ekle"]},
        {"all": ["atanmış", "öğretmen", "çıkar"]},
        {"all": ["atanmış", "öğretmen", "sil"]},
        {"all": ["ders", "öğretmen", "çıkar"]},
        {"all": ["öğretmen", "listesi", "değiştir"]},
        {"all": ["öğretmen", "ata", "rol", "uygun"]},
        {"all": ["öğretmen", "ata", "409"]},
        {"all": ["atanmamış", "öğretmen", "404"]},
        {"all": ["öğretmen", "çıkar", "sınav", "sil"]},
    ]},
    # --- Aşama 11: kapsamı olmayan/karışan intent'ler için hedefli kurallar ---
    {"intent": "guide_info", "groups": [
        {"all": ["kılavuz"]}, {"all": ["guide"]}, {"all": ["adım", "tanıtım"]},
    ]},
    {"intent": "register_how", "groups": [
        {"all": ["üye", "ol"]},
        {"all": ["kayıt", "ol"], "none": ["ders", "derse", "kulüp", "kulüb", "etüt", "etüd"]},
        {"all": ["kayıt", "form"]}, {"all": ["hesap", "aç"]},
        {"all": ["kullanıcı", "adı", "kural"]},
        {"all": ["kullanıcı", "adı", "kabul"]},
        {"all": ["aynı", "kullanıcı", "adı"]},
        {"all": ["kullanıcı", "adı", "nokta"]},
        {"all": ["kullanıcı", "adı", "başla"]},
        {"all": ["kullanıcı", "adı", "karakter"]},
    ]},
    {"intent": "profile_edit", "groups": [
        {"all": ["profil", "düzenle"]}, {"all": ["profil", "değiştir"]},
        {"all": ["profil", "güncelle"]}, {"all": ["profil", "kaydedem"]},
        {"all": ["görünen", "ad"]}, {"all": ["görünen", "isim"]},
        {"all": ["görünen", "ism"]}, {"all": ["profil", "fotoğraf"]},
        {"all": ["hakkında", "profil"]},
        {"all": ["iletişim", "bilgi", "değiştir"]},
        {"all": ["ad", "soyad", "güncelle"]},
        {"all": ["telefon", "değiştir"]},
        {"all": ["mail", "değiştir"]}, {"all": ["mail", "düzelt"]},
        {"all": ["eposta", "değiştir"]}, {"all": ["eposta", "düzelt"]},
        {"all": ["biyografi"]}, {"all": ["bio"]},
        {"all": ["doğum", "tarih"]}, {"all": ["hakkında", "alan"]},
        {"all": ["avatar", "kaldır"]}, {"all": ["fotoğraf", "kaldır"]},
    ]},
    {"intent": "profile_view", "groups": [
        {"all": ["profile", "me"]},
        {"all": ["profil", "aç"], "none": ["düzenle", "değiştir", "güncelle"]},
        {"all": ["profil", "bak"], "none": ["başka", "birinin"]},
        {"all": ["kendi", "profil"]}, {"all": ["profilim", "nerede"]},
        {"all": ["profil", "istatistik"]}, {"all": ["rozet", "nerede"]},
        {"all": ["profil", "ödev", "odak", "istatistik"]},
        {"all": ["profil", "sayfa"], "none": ["düzenle", "değiştir", "güncelle"]},
        {"all": ["hangi", "ders", "şube"]},
        {"all": ["hangi", "şube", "üyeli"]},
        {"all": ["şube", "üyeli"]},
        {"all": ["şube", "bilgi"]},
        {"all": ["şube", "bilgi", "sayfa"]},
    ]},
    {"intent": "attendance_view", "groups": [
        {"all": ["devamsızlık", "gör"]}, {"all": ["devamsızlık", "durum"]},
        {"all": ["yoklama", "geçmiş"]}, {"all": ["yoklama", "geçmiş", "bak"]},
        {"all": ["devam", "yüzde"], "none": ["formül", "hesap", "nasıl"]},
        # Devan kişi adı olabilir; yalnız yüzde/görüntüleme bağlamında tek-harfli
        # "Devam" yazımı olarak kabul edilir.
        {"all": ["devan", "yüzde", "gör"]},
        # 'devamsız...' kökü (devamsızlığımı) yazım hatalarına dayanıklı; öğrenci-3.şahıs hariç.
        {"all": ["devamsız"], "none": ["öğrenci", "başka", "birinin", "yazıl", "sayıl", "kural", "geç", "sil", "kaldır", "düzelt", "yükselt"]},
    ]},
    {"intent": "attendance_rate_info", "groups": [
        # Devam ORANININ HESABI (formül) — devamsızlık görüntülemeden ayrıdır.
        {"all": ["devam", "hesap"]}, {"all": ["devam", "formül"]},
        {"all": ["devam", "oran", "nasıl"]},
    ]},
    {"intent": "student_attendance_lookup", "groups": [
        {"all": ["öğrenci", "yoklama"]}, {"all": ["öğrenci", "devamsızlık"]},
        # devamsızlık -> devamsızlığını çekiminde k/ğ yumuşaması olur; kök güvenlidir.
        {"all": ["öğrenci", "devamsız"], "none": [
            "başka", "birinin", "arkadaş", "başkas"]},
        {"all": ["öğretmen", "öğrenci", "devamsız", "sorgula"]},
        {"all": ["öğrenci", "devam", "durum"]},
        # İsimli 3. şahıs how-to ("Ayşe'nin devamsızlık kaydına nasıl bakarım") — öğretmen+.
        {"all": ["devamsız", "nasıl", "bak"], "none": ["devamsızlığım", "kendi", "benim", "başka", "birinin", "arkadaş"]},
        {"all": ["yoklama", "nasıl", "bak"], "none": [
            "yoklamam", "kendi", "benim", "ben", "geçmiş", "başka", "birinin", "arkadaş"]},
    ]},
    {"intent": "event_attendance_mark", "groups": [
        {"all": ["etkinlik", "katıl"]}, {"all": ["etkinlik", "yoklama"]},
        {"all": ["etkinlik", "katıld"]}, {"all": ["etkinlik", "var"]},
        # etkinlik -> etkinliğe/etkinliğin ünsüz yumuşaması
        {"all": ["etkinliğ", "katıl"]},
        {"all": ["etkinlik", "vat", "demek"]},
        # Kısa "vsr" global olarak "var"a çevrilmez; yalnız etkinlik yoklaması
        # nesnesi ve işaretleme eylemi birlikteyse güvenlidir.
        {"all": ["öğrenci", "etkinlik", "vsr", "işaret"]},
        {"all": ["öğrenci", "etkinlik", "yoklama"]},
    ]},
    # --- Ödev (bağımsız modül; "ödev" + eylem köküyle ayrışır; none-koruması
    # alt-intent'leri ve exam_grade_student'ı birbirinden ayırır) ---
    {"intent": "homework_view", "groups": [
        {"all": ["ödev", "nerede"], "none": [
            "oluştur", "ekle", "ata", "gönder", "yükle", "teslim",
            "notland", "değerlendir", "puan", "gir"]},
        {"all": ["ödev", "hangi", "sayfa"]},
        {"all": ["ödev", "takip"]}, {"all": ["ödev", "listem"]},
        {"all": ["atanan", "ödev"]},
        # Tek-harf düşmesi: "Öde listemi" okul bağlamında ödev listesidir.
        # ``öde`` aşağıda tam-token aranır; ``ödeme listesi`` bu kurala çarpmaz.
        {"all": ["öde", "listem"]},
        {"all": ["verilen", "ödev"], "none": ["yükle", "gönder", "teslim"]},
        {"all": ["ödevlerim"], "none": [
            "teslim", "gönder", "yükle", "notland", "değerlendir", "puan"]},
    ]},
    {"intent": "homework_submit", "groups": [
        {"all": ["ödev", "gönder"]},
        {"all": ["ödev", "yükle"], "none": ["ekran", "sayfa", "durum"]},
        {"all": ["ödev", "teslim"], "none": [
            "takip", "notland", "değerlendir", "puan", "not"]},
        {"all": ["ödev", "teslim", "sayfa"]},
        {"all": ["ödev", "teslim", "sayfa", "yap"]},
        {"all": ["ödev", "yol"], "none": ["notland", "değerlendir", "puan"]},
        # Teslim sonradan kilitlenmiş veya dosya/beden sınırına takılmış olsa da
        # kullanıcı hâlâ teslim akışını soruyor; ayrı öğretmen-notlandırma işi değil.
        {"all": ["ödev", "teslim", "değiştir"]},
        {"all": ["ödev", "dosya"]}, {"all": ["ödev", "413"]},
        {"all": ["ödev", "dosya", "413"]},
        {"all": ["notlandır", "ödev", "dosya", "sil"]},
    ]},
    {"intent": "homework_withdraw_submission", "groups": [
        {"all": ["ödev", "teslim", "geri", "çek"]},
        {"all": ["teslim", "geri", "çek"], "none": ["randevu"]},
        {"all": ["ödev", "gönderdiğ", "sil"]},
        {"all": ["ödev", "gönderdiğ", "tamamen", "sil"]},
        {"all": ["ödev", "teslim", "tamamen", "sil"]},
        {"all": ["ödev", "teslim", "sil", "dosya"]},
        {"all": ["teslim", "geri", "çek", "düğme"]},
        {"all": ["notlandır", "ödev", "geri", "çek"]},
        {"all": ["ödev", "geri", "çek", "409"]},
        {"all": ["öğretmen", "teslim", "geri", "çek"]},
    ]},
    {"intent": "homework_assign", "groups": [
        {"all": ["ödev", "oluştur"]}, {"all": ["ödev", "ekle"]},
        {"all": ["yeni", "ödev"]},
        {"all": ["ödev", "ata"], "none": ["atanan"]},
        {"all": ["ödev", "ver"], "none": [
            "not", "puan", "verilen", "notland", "değerlendir", "gir"]},
    ]},
    {"intent": "homework_manage", "groups": [
        {"all": ["ödev", "düzenle"], "none": ["teslim", "cevap", "dosya", "not", "puan"]},
        {"all": ["ödev", "değiştir"], "none": ["teslim", "cevap", "dosya", "not", "puan"]},
        {"all": ["ödev", "güncelle"], "none": ["teslim", "cevap", "dosya", "not", "puan"]},
        {"all": ["ödev", "tamamen", "sil"]},
        {"all": ["ödev", "kayd", "sil"]},
        {"all": ["ödev", "son", "teslim", "tarih", "değiştir"]},
        {"all": ["ödev", "konu", "değiştir"]},
        {"all": ["ödev", "başka", "ders", "konu"]},
        {"all": ["ödev", "hedef", "kitle", "daralt"]},
        {"all": ["ödev", "audience"]},
        {"all": ["ödev", "hedef", "kitle", "409"]},
        {"all": ["ödev", "sil", "teslim", "ne", "ol"]},
        {"all": ["öğrenci", "ödev", "kendisi", "sil"]},
    ]},
    {"intent": "homework_grade", "groups": [
        {"all": ["ödev", "notland"]}, {"all": ["ödev", "değerlendir"]},
        {"all": ["ödev", "puan"]},
        {"all": ["ödev", "not", "ver"], "none": ["bak", "aldı", "nereden"]},
        {"all": ["ödev", "not", "gir"], "none": ["bak", "aldı"]},
        {"all": ["ödev", "not", "sil"]}, {"all": ["ödev", "not", "kaldır"]},
        {"all": ["ödev", "not", "değiştir"], "none": ["teslim"]},
        {"all": ["ödev", "not", "düzelt"], "none": ["teslim"]},
        {"all": ["ödev", "puan", "sil"]}, {"all": ["ödev", "puan", "kaldır"]},
        {"all": ["ödev", "puan", "değiştir"]}, {"all": ["ödev", "puan", "düzelt"]},
        {"all": ["ödev", "puan", "yeniden", "ayarla"]},
        {"all": ["ödev", "not", "liste", "çıkar"]},
        {"all": ["öğrenci", "ödev", "puan", "sil"]},
        {"all": ["öğrenci", "ödev", "puan", "kaldır"]},
        {"all": ["öğrenci", "ödev", "puan", "değiştir"]},
        {"all": ["öğrenci", "ödev", "puan", "düzelt"]},
        {"all": ["teslim", "not", "düzelt"]}, {"all": ["teslim", "puan", "geri", "al"]},
    ]},
    # --- Backend v2: pomodoro / mesajlar / etüt-kulüp / veli ---
    {"intent": "pomodoro_use", "groups": [
        # 'odağı' çekiminde ünsüz yumuşar (k->ğ); iki kök de tanınır.
        {"all": ["pomodoro"], "none": ["öğrenci"]},
        {"all": ["odak", "başlat"]}, {"all": ["odağ", "başlat"]},
        {"all": ["odak", "bitir"]}, {"all": ["odağ", "bitir"]},
        {"all": ["odak", "oturum"], "none": ["öğrenci"]},
        # 'odak sayacı/sayacımı' (ör. "Odak sayacımı aç") da pomodoro'dur.
        {"all": ["odak", "say"], "none": ["öğrenci"]},
        {"all": ["odağ", "say"], "none": ["öğrenci"]},
    ]},
    {"intent": "student_pomodoro_lookup", "groups": [
        {"all": ["öğrenci", "pomodoro"]}, {"all": ["öğrenci", "odak"]},
        {"all": ["öğrenci", "odağ"]},
    ]},
    {"intent": "messages_use", "groups": [
        {"all": ["mesaj"]}, {"all": ["gelen", "kutusu"]},
        {"all": ["mesaj", "gönderem"]},
        {"all": ["öğretmen", "soru", "sor"], "none": [
            "havuz", "pdf", "dosya", "ders", "devamsız", "yoklama"]},
        {"all": ["öğretmene", "sor"]},
        {"all": ["msj"]}, {"all": ["mesj"]},
    ]},
    {"intent": "study_club_info", "groups": [
        # 'etüde/kulübe' çekimlerinde ünsüz yumuşar (t->d, p->b); iki kök de tanınır.
        {"all": ["etüt"]}, {"all": ["etüd"]},
        {"all": ["kulüp"]}, {"all": ["kulüb"]},
        {"all": ["kulüp", "kayıt"]}, {"all": ["kulüb", "kayıt"]},
    ]},
    {"intent": "parent_info", "groups": [
        {"all": ["veli"]}, {"all": ["ebeveyn"]},
        {"all": ["veli", "çocuk", "adına"]},
        {"all": ["ebeveyn", "çocuk", "adına"]},
        {"all": ["veli", "çocu", "adına"]},
        {"all": ["ebeveyn", "çocu", "adına"]},
        {"all": ["ebeveyn", "rol", "iş"]},
        {"all": ["veli", "hesap", "nedir"]},
        {"all": ["veli", "pomodoro"]}, {"all": ["veli", "randevu"]},
        {"all": ["veli", "çocuk", "randevu"]},
        # "Çocuklarım" sayfası (/students). Veri sorguları (karne/not...) hariç ->
        # onlar report_card/attendance'e gider.
        {"all": ["çocuk"], "none": [
            "karne", "not", "devamsız", "yoklama", "ödev", "sınav", "randevu", "yemek",
            "ödeme", "ücret", "borç", "ekstre"]},
    ]},
    # --- Kapsam genişletme: menü sayfa/bölüm açıklama intent'leri ---
    {"intent": "fees_info", "groups": [
        {"all": ["ücret"], "none": ["tahsilat", "yönet"]},
        {"all": ["ödeme"], "none": ["sınav", "ödev", "yönet", "tahsilat"]},
        {"all": ["çocuk", "ekstre"]}, {"all": ["çocuk", "ödeme"]},
        {"all": ["veli", "ekstre"]}, {"all": ["veli", "ödeme"]},
    ]},
    {"intent": "fees_manage", "groups": [
        {"all": ["ödeme", "yönet"]}, {"all": ["tahsilat"]}, {"all": ["ücret", "yönet"]},
        {"all": ["öğrenci", "ödeme"], "none": ["kendi", "benim"]},
        {"all": ["ödeme", "iade"]}, {"all": ["ödeme", "ters", "kayıt"]},
        {"all": ["ödeme", "düzelt"]}, {"all": ["ledger", "sil"]},
        {"all": ["ledger", "düzenle"]}, {"all": ["ödeme", "ledger"]},
        {"all": ["request", "key", "ödeme"]},
    ]},
    {"intent": "branches_info", "groups": [
        {"all": ["şube"], "none": ["oluştur", "yeni", "kapasite", "düzenle", "sil", "ekle", "çıkar", "bağla", "ayır"]},
        {"all": ["hangi", "şube", "sayfa"], "none": ["oluştur", "yeni", "kapasite"]},
        {"all": ["şub", "liste"]},
        # nav.classGroups = "Şubeler" (/management/classes); "sınıf(lar)" da bu sayfadır.
        # Kayıt/çıkarma (course_enroll/remove_student) ve veri/sıralama sorguları
        # ("en çalışkan kim") hariç -> onlar bu sayfa navigasyonu değil.
        {"all": ["sınıf"], "none": [
            "oluştur", "yeni", "öğrenci", "liste", "al", "ekle", "çıkar", "sil",
            "kim", "çalışkan", "başarı", "ortalama", "not", "ödev", "sınav", "karne", "kaç"]},
    ]},
    {"intent": "class_section_manage", "groups": [
        {"all": ["şube", "oluştur"]}, {"all": ["yeni", "şube"]},
        {"all": ["sınıf", "grup", "aç"]}, {"all": ["sınıf", "grub", "aç"]},
        {"all": ["sınıf", "oluştur"]},
        {"all": ["sınıf", "ekle"], "none": ["öğrenci", "liste", "ders"]},
        {"all": ["şube", "düzenle"]}, {"all": ["şube", "sil"]},
        {"all": ["şube", "öğrenci", "ekle"]}, {"all": ["şube", "öğrenci", "çıkar"]},
        {"all": ["şube", "öğrenci", "çıkar", "ders", "kayıt"]},
        {"all": ["şube", "ders", "bağla"]}, {"all": ["ders", "şube", "bağla"]},
        {"all": ["şube", "ders", "ayır"]},
        {"all": ["şube", "oluştur", "kapasite"]},
    ]},
    {"intent": "calendar_info", "groups": [
        {"all": ["takvim"], "none": ["sınav"]},
        {"all": ["takvim", "aylık"]},
        {"all": ["haftalık", "program"]},
        {"all": ["ders", "program"], "none": ["sen", "ayarla", "kur"]},
    ]},
    {"intent": "today_info", "groups": [
        {"all": ["bugün", "panel"]}, {"all": ["ana", "panel"]},
        {"all": ["panel", "özet"]}, {"all": ["panel", "göster"]},
    ]},
    {"intent": "question_bank_info", "groups": [
        # Yalnız 'soru bankası' (sınav şablon deposu). 'Soru havuzu' AYRI bir özellik
        # (/questions, question_ask) -> ona bırakılır (havuz burada YOK).
        {"all": ["soru", "banka"]},
    ]},
    {"intent": "question_bank_manage", "groups": [
        {"all": ["soru", "banka", "şablon", "okul"]},
        {"all": ["soru", "banka", "salon", "okul"]},
        {"all": ["soru", "banka", "şablon", "ekle"]},
        {"all": ["soru", "banka", "şablon", "ilave"]},
        {"all": ["soru", "banka", "şablon", "dahil"]},
        {"all": ["soru", "banka", "oluştur"]},
        {"all": ["soru", "banka", "ekle"]},
        {"all": ["banka", "kendi", "soru", "düzenle"]},
        {"all": ["banka", "soru", "sil"]},
        {"all": ["soru", "şablon", "okul", "paylaş"]},
        {"all": ["banka", "soru", "private"]},
        {"all": ["banka", "soru", "görünürlük"]},
        {"all": ["başka", "öğretmen", "banka", "soru", "sil"]},
        {"all": ["şablon", "konu", "sil", "ne", "ol"]},
        {"all": ["şablon", "konu", "silinir", "nr", "ol"]},
        {"all": ["şablon", "silinir", "ne", "ol"]},
        {"all": ["banka", "soru", "sil", "sınav", "kopya"]},
        {"all": ["banla", "soru", "sil", "sınav", "kopya"]},
        {"all": ["soru", "banka", "409"]},
        {"all": ["question", "bank", "template", "edit"]},
    ]},
    {"intent": "notification_settings_info", "groups": [
        {"all": ["bildirim"]},
        {"all": ["mesaj", "bildirim"]},
        {"all": ["zil", "uyarı"]}, {"all": ["uyarı", "temizle"]},
        {"all": ["zil", "uyarı", "temizle"]},
    ]},
    {"intent": "technical_error_help", "groups": [
        # Özellik-spesifik kurallar çoğunlukla iki veya daha çok anahtar taşır ve
        # özgüllükte bunları geçer. Genel triyaj da yalnız ürün/işlem dili veya
        # HTTP durum koduyla tetiklenir; salt "çalışmıyor" her dış konuyu yutmaz.
        {"all": ["hata", "al"]}, {"all": ["hata", "ver"]},
        {"all": ["başarısız", "hata"]},
        {"all": ["işlem", "başarısız"]}, {"all": ["istek", "redd"]},
        {"all": ["istek", "başarısız"]}, {"all": ["zaman", "aşım"]},
        {"all": ["sayfa", "hata"]}, {"all": ["sayfa", "çalışmıyor"]},
        {"all": ["düğme", "çalışmıyor"]}, {"all": ["kaydet", "çalışmıyor"]},
        {"all": ["şunu", "yapama"]}, {"all": ["işlem", "yapama"]},
        {"all": ["kaydedem"]}, {"all": ["yükleyem"]},
        {"all": ["gönderem"]},
        {"all": ["400"]}, {"all": ["409"]}, {"all": ["413"]},
        {"all": ["422"]}, {"all": ["429"]},
        {"all": ["503"]},
    ]},
    {"intent": "upload_problem", "groups": [
        {"all": ["dosya", "413"]}, {"all": ["dosya", "boyut", "sınır"]},
        {"all": ["dosya", "yükle", "hata"]}, {"all": ["file", "alan", "eksik"]},
        {"all": ["dosya", "yükleyem"]}, {"all": ["dosya", "ekleyem"]},
        {"all": ["boş", "dosya"]}, {"all": ["svg", "yükle"]},
        {"all": ["on", "birinci", "ek"]}, {"all": ["11", "ek"]},
        {"all": ["10", "dosya"]},
        {"all": ["multipart", "file"]}, {"all": ["görsel", "svg"]},
        {"all": ["dosya", "multipart"]}, {"all": ["yükle", "multipart"]},
        {"all": ["dosya", "tür", "destek"]}, {"all": ["ek", "limit", "dol"]},
        {"all": ["limit", "dol", "dosya"]}, {"all": ["limit", "dol", "yükle"]},
        {"all": ["ek", "ekleyem"]},
    ]},
    {"intent": "chatbot_service_problem", "groups": [
        {"all": ["çelebi", "yanıt", "verm"]}, {"all": ["chatbot", "yanıt", "verm"]},
        {"all": ["çelebi", "çalışmıyor"]}, {"all": ["chatbot", "çalışmıyor"]},
        {"all": ["çelebi", "bağlanam"]}, {"all": ["chatbot", "bağlanam"]},
        {"all": ["ai", "service", "connected"]}, {"all": ["ai", "service", "enabled"]},
        {"all": ["chatbot", "bridge"]}, {"all": ["köprü", "bağlı", "değil"]},
        {"all": ["sohbet", "pending"]}, {"all": ["mesaj", "pending"]},
        {"all": ["chatbot", "429"]}, {"all": ["thread", "limit"]},
        {"all": ["sohbet", "limit"]}, {"all": ["chatbot", "503"]},
        {"all": ["çelebi", "unavailable"]}, {"all": ["çelebi", "busy"]},
        {"all": ["çelebi", "timed_out"]}, {"all": ["çelebi", "timed", "out"]},
        {"all": ["çelebi", "transport"]},
        {"all": ["çelebi", "protocol"]}, {"all": ["çelebi", "service_error"]},
        {"all": ["çelebi", "service", "error"]},
        {"all": ["çelebi", "bad_reply"]}, {"all": ["çelebi", "bad", "reply"]},
        {"all": ["çelebi", "empty_reply"]}, {"all": ["çelebi", "empty", "reply"]},
        {"all": ["çelebi", "interrupted"]}, {"all": ["chatbot", "interrupted"]},
        {"all": ["chatbot", "thread", "sil"]},
    ]},
    {"intent": "nav_overview", "groups": [
        {"all": ["akademik"], "none": ["dönem"]},
        {"all": ["öğrenci", "yönetim", "bölüm"]},
        {"all": ["yönetim", "menü"]}, {"all": ["admin", "bölüm"]},
        {"all": ["admin", "sayfa"]}, {"all": ["bölüm", "neler"]},
        {"all": ["menü", "bölüm", "var"]},
        {"all": ["menü", "anlat"], "none": [
            "yemek", "öğün", "yayınl", "rezerv", "kredi", "kapasite"]},
        {"all": ["hangi", "bölüm", "var"]},
    ]},
    {"intent": "event_view", "groups": [
        {"all": ["etkinlik", "nerede"], "none": ["oluştur", "ekle", "planla", "katıl", "yoklama", "işaretle"]},
        {"all": ["etkinlik", "gör"], "none": ["oluştur", "ekle", "planla", "katıl", "yoklama"]},
        {"all": ["etkinlik", "liste"], "none": ["oluştur", "ekle"]},
    ]},
    {"intent": "exam_schedule_info", "groups": [
        {"all": ["sınav", "takvim"]}, {"all": ["sınav", "tarih"]},
    ]},
    {"intent": "course_materials_info", "groups": [
        {"all": ["ders", "not", "pdf"]}, {"all": ["ders", "not", "dosya"]},
        {"all": ["ders", "pdf"]},
        {"all": ["öğretmen", "pdf"]}, {"all": ["ders", "dosya"], "none": ["defter"]},
        {"all": ["öğretmen", "pdf", "dosya"]},
        {"all": ["ders", "not", "dosya", "indir"]},
    ]},
    # --- T1: Randevu (al=öğrenci/veli, saat aç=öğretmen, onayla=öğretmen) ---
    {"intent": "appointment_book", "groups": [
        {"all": ["randevu", "al"], "none": [
            "saat", "onayla", "talepleri", "kabul", "reddet", "istek"]},
        {"all": ["randevu", "talep", "oluştur"]},
        # Ünsüz yumuşaması: talep -> talebi/talebimi.
        {"all": ["randevu", "taleb", "oluştur"]},
        {"all": ["randevu", "talep", "et"], "none": ["kabul", "onayla", "reddet"]},
        {"all": ["randevu", "taleb", "et"], "none": ["kabul", "onayla", "reddet"]},
        {"all": ["randevu", "iptal"]}, {"all": ["randevu", "geri", "çek"]},
        {"all": ["randevu", "slot", "dolu"]},
        {"all": ["randevu", "saat", "çakış"]},
        {"all": ["randevu", "başlamış", "409"]},
        {"all": ["randevu", "yeni", "saat", "kabul"]},
        # "Randevular nerede" = randevu sayfası (öğrenci/veli için randevu alma).
        {"all": ["randevu", "nerede"], "none": ["saat", "onayla", "talepleri", "istek"]},
    ]},
    {"intent": "appointment_slot_open", "groups": [
        {"all": ["randevu", "saat"]},
        {"all": ["müsait", "saat"]},
        {"all": ["müsait", "yayınla"]},
        {"all": ["randevu", "saat", "sil"]},
        {"all": ["randevu", "seri", "sil"]},
        {"all": ["randevu", "seri", "kaldır"]},
        {"all": ["randevu", "seri", "liste", "çıkar"]},
        {"all": ["randevu", "seri", "redd"]},
    ]},
    {"intent": "appointment_requests", "groups": [
        {"all": ["randevu", "onayla"]}, {"all": ["randevu", "kabul"]},
        {"all": ["randevu", "onayl"]},
        {"all": ["randevu", "reddet"]}, {"all": ["randevu", "istek"]},
        {"all": ["randevu", "talepleri"]},
        {"all": ["randevu", "taleb", "onayla"]},
        {"all": ["randevu", "taleb", "kabul"]},
        {"all": ["randevu", "taleb", "reddet"]},
        {"all": ["randevu", "başka", "saat", "öner"]},
        {"all": ["randevu", "eski", "teklif"]},
        {"all": ["öğretmen", "randevu", "iptal"]},
    ]},
    # --- T1: Yemek (menü görüntüle=view, yer ayır=book, yayınla/kredi=manage) ---
    {"intent": "meal_view", "groups": [
        {"all": ["yemek", "menü"], "none": [
            "yayınl", "ekle", "oluştur", "kredi", "ayır", "rezerv"]},
        {"all": ["öğün", "menü"]},
        {"all": ["yemek", "liste"]},
        {"all": ["yemek", "nerede"], "none": ["yer", "rezerv", "yayınla", "ekle", "kredi"]},
    ]},
    {"intent": "meal_book", "groups": [
        {"all": ["yer", "ayır"]},
        {"all": ["yemek", "rezerv"]},
        {"all": ["öğün", "rezerv"]},
        {"all": ["yemek", "ayırt"]},
        {"all": ["yemek", "rezerv", "sil"]},
        {"all": ["yemek", "rezerv", "liste", "çıkar"]},
        {"all": ["yemek", "rezerv", "iptal"]},
        {"all": ["yemek", "rezerv", "409"]},
        {"all": ["yemek", "rezerv", "dolu"]},
        {"all": ["yemek", "rezerv", "son", "saat"]},
        {"all": ["öğün", "kapasite", "dolu"]},
        {"all": ["öğün", "yeniden", "rezerv"]},
    ]},
    {"intent": "meal_service_mark", "groups": [
        {"all": ["yemek", "servis", "işaretle"]},
        {"all": ["yemek", "servis", "edildi"]},
        {"all": ["yemek", "gelmedi", "işaretle"]},
        {"all": ["öğün", "gelmedi", "kayd"]},
        {"all": ["rezervasyonsuz", "servis"]},
        {"all": ["walk", "in", "servis"]},
        {"all": ["servis", "kayd", "düzelt"]},
        {"all": ["gelmedi", "ücret", "geri"]},
        {"all": ["öğrenci", "kendi", "yemek", "yoklama"]},
        {"all": ["yemek", "yoklama", "işaretle"]},
    ]},
    {"intent": "meal_menu_manage", "groups": [
        {"all": ["menü", "yayınla"]},
        {"all": ["menü", "yayınl"]},
        {"all": ["menü", "oluştur"]},
        {"all": ["yemek", "ekle"], "none": ["yer"]},
        {"all": ["öğün", "yemek", "ekle"]},
        {"all": ["öğün", "yemek", "ilave"]},
        {"all": ["öğün", "yemek", "dahil"]},
        {"all": ["öğün", "yemek", "ilave"]},
        {"all": ["öğün", "yemek", "kayıt", "gir"]},
        {"all": ["menü", "kapasite", "değiştir"]},
    ]},
    {"intent": "meal_dietary_profile_manage", "groups": [
        {"all": ["öğrenci", "beslenme", "profil"]},
        {"all": ["beslenme", "profil", "güncelle"]},
        {"all": ["beslenme", "profil", "değiştir"]},
        {"all": ["alerji", "etiket", "öğrenci"]},
        {"all": ["öğrenci", "alerji", "ekle"]},
        {"all": ["mutfak", "not", "temizle"]},
        {"all": ["mutfak", "not", "değiştir"]},
        {"all": ["dietary", "tag", "hata"]},
        {"all": ["bilinmeyen", "dietary", "tag"]},
        {"all": ["öğretmen", "beslenme", "profil", "değiştir"]},
        {"all": ["öğrenci", "kendi", "alerji", "düzenle"]},
        {"all": ["öğrenci", "diyet", "profil"]},
        {"all": ["yemek", "diyet", "profil"]},
    ]},
    {"intent": "meal_credit_manage", "groups": [
        {"all": ["yemek", "kredi"]}, {"all": ["kredi", "kaydet"]},
        {"all": ["yemek", "bakiye", "yükle"]},
        {"all": ["yemek", "bakiye"]}, {"all": ["bakiye", "tutar", "ekle"]},
        {"all": ["öğrenci", "kredi", "ekle"]},
    ]},
    # --- T1: Soru havuzu (sor=ask, çöz=solve, onayla=approve; sınav soru ekle'den ayrı) ---
    {"intent": "question_ask", "groups": [
        # 'onayla/reddet/çöz' varsa approve/solve'a bırak (soru+havuz onlarda da var).
        {"all": ["soru", "havuz"], "none": ["onayla", "reddet", "çöz", "çözüm", "bekleyen", "pending"]},
        {"all": ["havuz", "soru"], "none": ["onayla", "reddet", "çöz", "çözüm", "bekleyen", "pending"]},
        {"all": ["soru", "havuz", "sor"], "none": ["onayla", "reddet", "çöz", "çözüm", "bekleyen", "pending"]},
    ]},
    {"intent": "question_solve", "groups": [
        {"all": ["çözüm", "gönder"]}, {"all": ["çözüm", "öner"]},
        {"all": ["soru", "çözüm", "gönder"]},
        {"all": ["çözüm", "paylaş"]}, {"all": ["çözüm", "yaz"]},
        {"all": ["soru", "çöz"]},
    ]},
    {"intent": "question_approve", "groups": [
        {"all": ["soru", "onayla"], "none": ["banka"]},
        {"all": ["soru", "onayl"], "none": ["banka"]},
        {"all": ["soru", "reddet"]},
        {"all": ["bekleyen", "soru"]}, {"all": ["havuz", "onayla"]},
        {"all": ["soru", "reddet", "sil"]},
        {"all": ["pending", "soru"]},
        {"all": ["havuz", "pending", "soru"]},
    ]},
    # --- T1: Beyaz tahta (aç/nerede=view, oluştur/yeni=create) ---
    {"intent": "board_view", "groups": [
        {"all": ["tahta", "aç"]},
        {"all": ["tahta", "nerede"], "none": ["oluştur", "yeni", "ekle"]},
        {"all": ["beyaz", "tahta"], "none": ["oluştur", "yeni", "ekle", "tanımla"]},
        {"all": ["tahta", "gör"]},
    ]},
    {"intent": "board_create", "groups": [
        {"all": ["beyaz", "tahta", "tanımla"]},
        {"all": ["tahta", "oluştur"]},
        {"all": ["tahta", "tanımla"]},
        {"all": ["yeni", "tahta"]},
        {"all": ["tahta", "ekle"]},
        {"all": ["tahta", "kilitle"]}, {"all": ["tahta", "temizle"]},
        {"all": ["tahta", "kapat"]}, {"all": ["tahta", "sil"]},
        {"all": ["tahta", "kaldır"]},
        {"all": ["tahta", "liste", "çıkar"]},
        {"all": ["çizim", "tahta", "oluştur"]},
        {"all": ["tahta", "kapat", "yeniden", "aç"]},
        {"all": ["tahta", "toplu", "davet"]},
        {"all": ["tahta", "409"]},
    ]},
]


_NAMED_POSSESSIVE_RE: Final[re.Pattern[str]] = re.compile(
    r"\b[a-zçğıöşü]{2,}['’](?:nın|nin|nun|nün|ın|in|un|ün)\b",
    re.IGNORECASE,
)


def canonicalize_named_grade_query(query: str) -> str:
    """Üçüncü-şahıs özel-ad not CRUD'unu öğrenci notlandırmasına çevirir.

    Bağlamsız ``not`` kişisel Defter anlamındadır; ``Ali'nin notu`` ise açıkça
    başka bir kişiye aittir. Ödev/Defter bağlamı kendi özel akışında kalır.
    """

    if not _NAMED_POSSESSIVE_RE.search(query):
        return query
    tokens = folded_tokens(query)
    if any(token.startswith(("odev", "teslim", "defter", "kisisel")) for token in tokens):
        return query
    if not any(token.startswith(("not", "puan")) for token in tokens):
        return query
    verb_map = (
        ("sil", "sil"),
        ("kaldir", "kaldır"),
        ("degistir", "değiştir"),
        ("duzelt", "düzelt"),
        ("guncelle", "güncelle"),
    )
    for prefix, verb in verb_map:
        if any(token.startswith(prefix) for token in tokens):
            return f"öğrenci notunu {verb}"
    return query


def _kw_of(word: str) -> str:
    """Ham kelimeyi katlanmış (ascii, stem YOK) forma indirger."""

    return fold_accents(normalize(word)).replace(" ", "")


@dataclass(frozen=True)
class _Group:
    all_kw: tuple[str, ...]
    none_kw: tuple[str, ...] = ()


@dataclass(frozen=True)
class _Rule:
    intent: str
    groups: tuple[_Group, ...]


def _compile_rules(raw_rules: list[dict[str, Any]]) -> list[_Rule]:
    compiled: list[_Rule] = []
    for raw in raw_rules:
        groups = tuple(
            _Group(
                all_kw=tuple(_kw_of(w) for w in group["all"]),
                none_kw=tuple(_kw_of(w) for w in group.get("none", ())),
            )
            for group in raw["groups"]
        )
        compiled.append(_Rule(intent=raw["intent"], groups=groups))
    return compiled


_RULES: Final[list[_Rule]] = _compile_rules(_RAW_RULES)


@dataclass(frozen=True)
class RuleMatch:
    """Kural katmanının kararı."""

    intent: str
    score: int
    matched: tuple[str, ...]
    reason: str
    space_id: str | None = None


def _present(keyword: str, tokens: list[str]) -> bool:
    """Anahtar kelime soruda var mı? (>=2 harf önek, aksi hâlde tam eşleşme)."""

    # İki kısa kök genel önek olamaz: ``ne`` neden/nerede'yi; ``ek`` ise
    # ekrandan/ekranı'yı yakalayıp platform veya dosya intent'ine sürüklüyordu.
    if keyword == "ne":
        return any(token == "ne" for token in tokens)
    if keyword == "yeni":
        # ``yeniden`` (tekrar) yeni kayıt anlamına gelmez.
        return any(token == "yeni" for token in tokens)
    if keyword == "ek":
        return any(
            re.fullmatch(r"ek(?:i(?:m|n|ni|nden|ne)?|ler\w*|te\w*|ten\w*)?", token)
            is not None
            for token in tokens
        )
    if keyword == "ode":
        return any(token == "ode" for token in tokens)
    if len(keyword) >= 2:
        return any(token.startswith(keyword) for token in tokens)
    return any(token == keyword for token in tokens)


def _group_matches(group: _Group, tokens: list[str]) -> bool:
    if any(not _present(k, tokens) for k in group.all_kw):
        return False
    if any(_present(k, tokens) for k in group.none_kw):
        return False
    return True


class RuleMatcher:
    """A rule index compiled for one closed intent space."""

    def __init__(
        self,
        intent_names: set[str] | frozenset[str] | None = None,
        *,
        space_id: str | None = None,
    ) -> None:
        allowed = None if intent_names is None else frozenset(intent_names)
        self._rules = tuple(
            rule for rule in _RULES if allowed is None or rule.intent in allowed
        )
        self.space_id = space_id

    def match(self, query: str) -> RuleMatch | None:
        """Soruyu bu derlenmiş kural uzayından geçirir.

        Tek bir intent en yüksek özgüllükle eşleşirse RuleMatch; hiçbir kural
        eşleşmezse veya eşitlik varsa None döner.
        """

        query = canonicalize_named_grade_query(query)
        tokens = folded_tokens(query)
        if not tokens:
            return None

        best_by_intent: dict[str, tuple[int, tuple[str, ...]]] = {}
        for rule in self._rules:
            for group in rule.groups:
                if _group_matches(group, tokens):
                    score = len(group.all_kw)
                    prev = best_by_intent.get(rule.intent)
                    if prev is None or score > prev[0]:
                        best_by_intent[rule.intent] = (score, group.all_kw)

        if not best_by_intent:
            return None

        ranked = sorted(best_by_intent.items(), key=lambda kv: kv[1][0], reverse=True)
        top_intent, (top_score, matched) = ranked[0]

        if len(ranked) > 1 and ranked[1][1][0] == top_score:
            return None

        return RuleMatch(
            intent=top_intent,
            score=top_score,
            matched=matched,
            reason=f"kural: {top_intent} <- {list(matched)}",
            space_id=self.space_id,
        )


_DEFAULT_RULE_MATCHER: Final[RuleMatcher] = RuleMatcher()


def match(query: str) -> RuleMatch | None:
    """Geriye uyumlu global kural API'si."""

    return _DEFAULT_RULE_MATCHER.match(query)
