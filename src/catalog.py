"""Hezarfen kullanım asistanı için intent kataloğu ve rol modeli.

Bu modül YALNIZCA veri + saf yardımcı fonksiyonlar içerir. Metin normalizasyonu,
intent bulma (kural/benzerlik), karar verme ve cevap üretimi ayrı modüllerin
sorumluluğudur.

Kaynak: `hezarfen-site-rehberi.md`. Cevaplar gerçek menü/buton etiketleri ve
sayfa yolları içerir; uydurma yol veya etiket kullanılmaz (rehber §0).

Alan açıklamaları (her intent kaydı):
- intent: Motorun döndüreceği benzersiz sınıf adı.
- category: Gruplama (raporlama/menü için).
- description: İnsan-okunur kısa açıklama.
- response_id: Testlerde metin yerine karşılaştırılan kararlı kimlik.
- response_template: Kullanıcıya gösterilecek adım adım cevap (gerçek yol/etiket).
- auth_required: Oturum gerekip gerekmediği. min_role ile tutarlı olmalıdır.
- min_role: Bu işlemi yapabilen EN DÜŞÜK rol (rol hiyerarşisinden).
- example_questions: Kural/eşik geliştirme örnekleri; benchmark DEĞİLDİR.
- must_not_match: Bu intent ile sık karışabilecek intent adları.

`example_questions` benchmark değildir; gerçek değerlendirme soruları ayrı bir
dosyada tutulur ve bu listeden kopyalanmaz.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Final


# --- Rol modeli (rehber §2) --------------------------------------------------
# Hiyerarşi düşükten yükseğe. Üst rol, alt rolün yaptığı her şeyi yapabilir.
ROLE_HIERARCHY: Final[tuple[str, ...]] = (
    "ziyaretci",  # oturum açmamış kullanıcı
    "ogrenci",
    "ogretmen",
    "yonetici",
    "admin",
)

_ROLE_RANK: Final[dict[str, int]] = {role: rank for rank, role in enumerate(ROLE_HIERARCHY)}

# Oturum açmış sayılan en düşük rol.
MIN_AUTHENTICATED_ROLE: Final[str] = "ogrenci"


REQUIRED_INTENT_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "intent",
        "category",
        "description",
        "response_id",
        "response_template",
        "auth_required",
        "min_role",
        "example_questions",
        "must_not_match",
    }
)


INTENTS: Final[list[dict[str, Any]]] = [
    # --- Genel ---------------------------------------------------------------
    {
        "intent": "greeting",
        "category": "general",
        "description": "Kullanıcının selam vermesi / sohbeti başlatması.",
        "response_id": "welcome_message",
        "response_template": (
            "Merhaba! Ben Hezarfen kullanım asistanıyım. Ders, sınav, karne, "
            "yoklama, defter ve mesai gibi konularda 'nasıl yaparım?' sorularını "
            "yanıtlayabilirim. Ne yapmak istiyorsun?"
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": ["Merhaba", "Selam", "Günaydın", "İyi günler", "Hey"],
        "must_not_match": ["help_capabilities"],
    },
    {
        "intent": "help_capabilities",
        "category": "general",
        "description": "Asistanın neler yapabildiğinin sorulması.",
        "response_id": "capabilities",
        "response_template": (
            "Hezarfen sitesini nasıl kullanacağını anlatabilirim: ders/sınav "
            "oluşturma, sınava girme, karne ve ortalama, yoklama, defter, mesai, "
            "dönem ve okul ayarları, kullanıcı rolleri ve daha fazlası. Rolünü "
            "(Öğrenci/Öğretmen/Yönetici/ADMIN) söylersen sana uygun adımları veririm."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Neler yapabilirsin?",
            "Bana nasıl yardımcı olursun?",
            "Hangi konularda yardım edebilirsin?",
            "Ne işe yarıyorsun?",
            "Özelliklerin neler?",
        ],
        "must_not_match": ["greeting", "guide_info"],
    },
    {
        "intent": "guide_info",
        "category": "general",
        "description": "Uygulama içi Rehber (Guide) sayfasının sorulması.",
        "response_id": "guide_page_info",
        "response_template": (
            "Uygulama içi rehbere hesap (avatar) menüsünden **Rehber (Guide)** ile "
            "veya doğrudan `/guide` adresinden ulaşırsın. 6 adımlık akışı (Ana sayfa, "
            "Defter, Etkinlik/Yoklama, Dersler, Sınavlar, Karnem) ve 'Kim ne yapabilir?' "
            "panelini içerir."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Rehber sayfası nerede?",
            "Kullanım kılavuzu var mı?",
            "Uygulama içi rehbere nasıl ulaşırım?",
            "Guide sayfasını aç",
            "Yardım rehberi nerede?",
        ],
        "must_not_match": ["help_capabilities", "navigation_help"],
    },
    # --- Kimlik / hesap ------------------------------------------------------
    {
        "intent": "login_how",
        "category": "account",
        "description": "Nasıl giriş yapılacağının sorulması.",
        "response_id": "login_instructions",
        "response_template": (
            "Giriş yapmak için `/login` sayfasına git, **Kullanıcı adı (Username)** "
            "(3–32 karakter) ve **Şifre (Password)** (6–128) alanlarını doldur, "
            "**Giriş yap (Log in)** düğmesine bas. Başarılı girişte Ana sayfaya (`/`) "
            "yönlendirilirsin; hatalı bilgide formun üstünde kırmızı hata kutusu çıkar."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Nasıl giriş yaparım?",
            "Giriş sayfası nerede?",
            "Log in nasıl oluyor?",
            "Sisteme nasıl girerim?",
            "Oturum açmak istiyorum",
        ],
        "must_not_match": ["register_how", "account_access_problem"],
    },
    {
        "intent": "register_how",
        "category": "account",
        "description": "Nasıl yeni hesap/kayıt oluşturulacağı.",
        "response_id": "register_instructions",
        "response_template": (
            "Kayıt için `/register` sayfasına git; **Kullanıcı adı** (3–32), **Şifre** "
            "(6–128) ve **Şifreyi onayla (Confirm password)** alanlarını doldurup "
            "**Hesap oluştur (Create account)**'a bas. Yeni hesaplar **Öğrenci** olarak "
            "başlar; kayıt otomatik giriş yapmaz, giriş sayfasına yönlendirilirsin. "
            "'admin/root/support' gibi personel çağrıştıran adlar reddedilir."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Nasıl kayıt olurum?",
            "Yeni hesap nasıl açılır?",
            "Hesap oluşturmak istiyorum",
            "Kayıt sayfası nerede?",
            "Üye olmak istiyorum",
        ],
        "must_not_match": ["login_how"],
    },
    {
        "intent": "logout_how",
        "category": "account",
        "description": "Çıkış yapma yöntemi.",
        "response_id": "logout_instructions",
        "response_template": (
            "Çıkış yapmak için sol menü altındaki hesap kutusunu (ad-soyad) aç ve "
            "**Çıkış yap (Log out)**'a bas. Oturum hemen kapanır."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Nasıl çıkış yaparım?",
            "Oturumu nasıl kapatırım?",
            "Log out nerede?",
            "Hesaptan çıkmak istiyorum",
            "Çıkış yap",
        ],
        "must_not_match": ["session_info"],
    },
    {
        "intent": "session_info",
        "category": "account",
        "description": "Oturum süresi / oturum davranışı.",
        "response_id": "session_duration_info",
        "response_template": (
            "Giriş yapınca **7 gün** geçerli bir oturum açılır. Süre sunucu saatiyle "
            "ölçülür; cihazının saati yanlış olsa bile değişmez. Çıkış yapmak oturumu "
            "hemen kapatır."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Oturumum ne kadar açık kalır?",
            "Ne zaman otomatik çıkış olur?",
            "Oturum süresi kaç gün?",
            "Tekrar giriş yapmam gerekir mi?",
            "Oturum ne kadar sürer?",
        ],
        "must_not_match": ["logout_how"],
    },
    {
        "intent": "account_access_problem",
        "category": "account",
        "description": "Şifre unutma / giriş yapamama gibi erişim sorunları.",
        "response_id": "access_problem_info",
        "response_template": (
            "Hatalı kullanıcı adı/şifrede giriş formunun üstünde kırmızı hata kutusu "
            "çıkar; bilgilerini kontrol edip tekrar dene. Rehberde self-servis bir "
            "'şifremi unuttum' akışı tanımlı değil; kayıtlı bilgilerine erişemiyorsan "
            "okul yönetimine başvurman gerekir."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Şifremi unuttum",
            "Giriş yapamıyorum",
            "Hesabıma giremiyorum",
            "Kullanıcı adımı hatırlamıyorum",
            "Şifremi sıfırlayabilir miyim?",
        ],
        "must_not_match": ["login_how", "privacy_security"],
    },
    {
        "intent": "profile_edit",
        "category": "account",
        "description": "Profil bilgilerini düzenleme.",
        "response_id": "profile_edit_instructions",
        "response_template": (
            "Profilini düzenlemek için hesap menüsünden **Profili düzenle (Edit profile)** "
            "veya `/profile` adresine git; **Ad, Soyad, E-posta, Telefon, Doğum tarihi "
            "(GG/AA/YYYY)** alanlarını güncelleyip **Kaydet**'e bas. Tüm alanlar isteğe "
            "bağlıdır; **kullanıcı adı ve rol buradan değiştirilemez**. Doğum tarihi "
            "gelecekte olamaz."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Profilimi nasıl düzenlerim?",
            "E-posta adresimi değiştirmek istiyorum",
            "Telefon numaramı güncelleyeceğim",
            "Kişisel bilgilerimi nereden değiştiririm?",
            "Doğum tarihimi ekleyebilir miyim?",
        ],
        "must_not_match": ["user_role_change"],
    },
    {
        "intent": "language_theme",
        "category": "account",
        "description": "Dil (TR/EN) veya tema (açık/koyu) değiştirme.",
        "response_id": "language_theme_instructions",
        "response_template": (
            "Giriş yaptıysan sol menü altındaki hesap kutusundan **Dil (Language)** ile "
            "Türkçe/English, **Tema (Toggle theme)** ile Açık/Koyu arasında geçebilirsin. "
            "Ziyaretçiysen bu seçenekler üst bardadır. Seçim tarayıcıda kalıcı saklanır."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Dili nasıl değiştiririm?",
            "İngilizceye nasıl geçerim?",
            "Karanlık moda nasıl geçilir?",
            "Temayı değiştirmek istiyorum",
            "Uygulamayı Türkçe yap",
        ],
        "must_not_match": ["navigation_help"],
    },
    # --- Roller / navigasyon -------------------------------------------------
    {
        "intent": "roles_permissions",
        "category": "roles",
        "description": "Roller ve yetkilerin sorulması.",
        "response_id": "roles_overview",
        "response_template": (
            "Hezarfen'de dört kademeli rol vardır: **Öğrenci < Öğretmen < Yönetici < "
            "ADMIN**. Üst rol, alt rolün yaptığı her şeyi yapar. Kayıt olan herkes "
            "Öğrenci başlar; üst roller sonradan bir ADMIN tarafından atanır. Rol her "
            "istekte yeniden kontrol edilir; değişince yeniden giriş gerekmez."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Roller nelerdir?",
            "Yetkiler nasıl çalışıyor?",
            "Öğretmen neler yapabilir?",
            "ADMIN ile Yönetici farkı ne?",
            "Kimin hangi yetkisi var?",
        ],
        "must_not_match": ["user_role_change", "access_denied_help"],
    },
    {
        "intent": "access_denied_help",
        "category": "roles",
        "description": "'Erişimin yok' / yetkisiz sayfa yönlendirmesi.",
        "response_id": "access_denied_info",
        "response_template": (
            "Yetkisiz erişimde iki davranış olur: bazı sayfalarda sessizce Ana sayfaya "
            "(`/`) yönlendirilirsin (oturum yoksa `/login`'e); bazılarında ise kırmızı "
            "**\"Bu içeriğe erişimin yok.\"** kutusu çıkar. Bu genelde rolünün o işlem "
            "için yetersiz olduğunu ya da ilgili derse kayıtlı olmadığını gösterir."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Bu içeriğe erişimin yok diyor",
            "Neden ana sayfaya atıldım?",
            "Sayfaya giremiyorum neden?",
            "Erişim reddedildi ne demek?",
            "Yetkim yok mu?",
        ],
        "must_not_match": ["roles_permissions", "account_access_problem"],
    },
    {
        "intent": "navigation_help",
        "category": "roles",
        "description": "Menü/sayfa nerede — genel navigasyon.",
        "response_id": "navigation_info",
        "response_template": (
            "Masaüstünde sol dikey menüden gezinilir; gruplar rol bazlıdır ve boş "
            "gruplar gizlenir. Mobilde altta 5 sekme vardır: Ana sayfa, Dersler, "
            "Sınavlar, Defter, Menü. Hangi sayfayı aradığını söylersen tam yolunu "
            "(ör. `/courses`, `/exams`, `/marks`) veririm."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Menüde ne var?",
            "Sayfalar nerede?",
            "Nasıl gezinirim?",
            "İlgili bölümü nasıl bulurum?",
            "Navigasyon nasıl?",
        ],
        "must_not_match": ["guide_info", "language_theme"],
    },
    # --- Dersler -------------------------------------------------------------
    {
        "intent": "course_view",
        "category": "courses",
        "description": "Dersleri listeleme / ders detayına gitme.",
        "response_id": "course_view_info",
        "response_template": (
            "Dersler `/courses` sayfasında listelenir; arama ve döneme göre filtreleme "
            "yapabilirsin. Öğrenci yalnızca kayıtlı olduğu dersleri görür ('Kayıtlı' "
            "rozeti). Bir dersi açmak için satırda **Görüntüle (View)**'ye bas; detay "
            "`/courses/$id`'de sınavları, ders oturumlarını ve (yetkiliysen) sınıf "
            "listesini gösterir."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Derslerimi nerede görürüm?",
            "Ders listesi nerede?",
            "Kayıtlı olduğum dersler neler?",
            "Bir dersin detayına nasıl giderim?",
            "Dersleri nasıl filtrelerim?",
        ],
        "must_not_match": ["course_create", "report_card_view"],
    },
    {
        "intent": "course_create",
        "category": "courses",
        "description": "Yeni ders oluşturma (Öğretmen+).",
        "response_id": "course_create_instructions",
        "response_template": (
            "Ön koşul: Öğretmen ve üstü rol. 1) `/courses`'a git, **Yeni ders (New "
            "course)**'e bas. 2) Sağdan açılan panelde **Başlık** (zorunlu), isteğe "
            "bağlı **Açıklama** ve **Dönem** (varsayılan 'Atanmamış') gir. 3) **Oluştur**. "
            "Öğrencide 'Yeni ders' düğmesi görünmez."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Yeni ders nasıl oluşturulur?",
            "Ders eklemek istiyorum",
            "Nasıl ders açarım?",
            "Yeni bir sınıf oluşturacağım",
            "Ders oluşturma nerede?",
        ],
        "must_not_match": ["course_view", "exam_create", "event_create"],
    },
    {
        "intent": "course_enroll_student",
        "category": "courses",
        "description": "Derse öğrenci kaydetme (Öğretmen+).",
        "response_id": "enroll_student_instructions",
        "response_template": (
            "Ön koşul: dersi oluşturan öğretmen veya Yönetici+ olmak. 1) Ders detayına "
            "(`/courses/$id`) gir, **Sınıf listesi (Roster)** bölümünü aç. 2) **Öğrenci "
            "kaydet (Enroll student)**'e bas, panelde öğrenciyi ara-seç. 3) Onayla. "
            "Zaten kayıtlılar listede çıkmaz; öğrenci seçmezsen 'Önce bir öğrenci "
            "seçmelisin.' uyarısı çıkar. Sınıf listesi yalnızca yönetim yetkilisine görünür."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Derse nasıl öğrenci eklerim?",
            "Öğrenci kaydetmek istiyorum",
            "Sınıfa öğrenci nasıl alınır?",
            "Roster'a öğrenci ekleme",
            "Bir öğrenciyi derse kaydet",
        ],
        "must_not_match": ["course_remove_student", "course_create"],
    },
    {
        "intent": "course_remove_student",
        "category": "courses",
        "description": "Dersten öğrenci çıkarma (Öğretmen+).",
        "response_id": "remove_student_instructions",
        "response_template": (
            "1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci "
            "satırında **Kaldır (Remove)**'a bas ve onayla. Çıkarmak geçmiş notları "
            "silmez; öğrenci daha sonra tekrar kaydedilebilir."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Dersten öğrenci nasıl çıkarılır?",
            "Bir öğrenciyi sınıftan silmek istiyorum",
            "Kaydı nasıl kaldırırım?",
            "Öğrenciyi dersten at",
            "Yanlış kaydettiğim öğrenciyi çıkar",
        ],
        "must_not_match": ["course_enroll_student"],
    },
    {
        "intent": "lesson_session_add",
        "category": "courses",
        "description": "Ders oturumu (ders saati) ekleme (Öğretmen+).",
        "response_id": "lesson_session_instructions",
        "response_template": (
            "Ön koşul: ders yönetim yetkisi. 1) Ders detayı → **Ders oturumları (Lesson "
            "sessions)** → **Oturum ekle (Add session)**. 2) İsteğe bağlı **Konu**, "
            "**Başlangıç** tarih (GG/AA/YYYY) + saat, isteğe bağlı **Bitiş**. 3) **Oturum "
            "ekle**. Başlangıç zorunlu ve gelecekte olmalı; bitiş başlangıçtan önce olamaz."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Ders oturumu nasıl eklerim?",
            "Ders saati eklemek istiyorum",
            "Yeni oturum oluşturma",
            "Derse ders saati ekle",
            "Lesson session nasıl eklenir?",
        ],
        "must_not_match": ["roll_call", "event_create"],
    },
    {
        "intent": "roll_call",
        "category": "courses",
        "description": "Ders oturumunda yoklama alma (Öğretmen+).",
        "response_id": "roll_call_instructions",
        "response_template": (
            "Ön koşul: derste kayıtlı öğrenci ve en az bir oturum olmalı; yönetim "
            "yetkisi. 1) Ders detayı → **Ders oturumları** → oturum kartında **Yoklama "
            "(Roll call)**. 2) Her öğrenci için **Var / Yok / Geç / Mazeretli** seç. "
            "3) Satırda **Kaydet** (daha önce kaydedildiyse **Güncelle**). Öğrenci ders "
            "oturumu yoklamasında kendini işaretleyemez."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Yoklama nasıl alınır?",
            "Ders oturumunda yoklama almak istiyorum",
            "Öğrencileri var/yok nasıl işaretlerim?",
            "Roll call nasıl yapılır?",
            "Devamsızlık işleme",
        ],
        "must_not_match": ["lesson_session_add", "event_attendance_mark", "student_attendance_lookup"],
    },
    # --- Sınavlar ------------------------------------------------------------
    {
        "intent": "exam_modes_info",
        "category": "exams",
        "description": "Sınav modlarının açıklanması.",
        "response_id": "exam_modes_explained",
        "response_template": (
            "Dört sınav modu vardır: **Zamansız** (çevrimdışı notlanır, girilemez), "
            "**Senkron** (herkes tek sabit aralıkta girer), **Asenkron** (aralık içinde "
            "istediğin an başlar, kişisel süre alırsın), **Açık** (her zaman girilebilir, "
            "hep 'Aktif' sayılır). Süre 1 dakika–24 saat arasıdır."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Sınav modları neler?",
            "Senkron ve asenkron farkı ne?",
            "Açık mod ne demek?",
            "Zamansız sınav nedir?",
            "Sınav türleri arasındaki fark ne?",
        ],
        "must_not_match": ["exam_create", "exam_enter_room"],
    },
    {
        "intent": "exam_create",
        "category": "exams",
        "description": "Yeni sınav oluşturma ve mod seçme (Öğretmen+).",
        "response_id": "exam_create_instructions",
        "response_template": (
            "Ön koşul: yönetebileceğin en az bir ders olmalı. 1) `/exams` → **Sınav "
            "oluştur (Create exam)**. 2) **Ders seç**, **Başlık** ve isteğe bağlı "
            "açıklama gir. 3) **Tür** (Ödev/Kısa sınav/Vize/Final/Proje/Sözlü) ve **Mod** "
            "(Senkron/Asenkron/Açık) seç. 4) Gerekirse **Deneme hakkı** ve **Yeniden "
            "girişe izin ver**'i ayarla. 5) Senkron/Asenkron ise Başlangıç/Bitiş gir. "
            "6) **Oluştur**. Sınavlar ders içinden eklenir."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Nasıl sınav oluştururum?",
            "Yeni sınav eklemek istiyorum",
            "Sınav açma nerede?",
            "Vize sınavı oluşturacağım",
            "Sınav nasıl hazırlanır?",
        ],
        "must_not_match": ["exam_add_question", "exam_modes_info", "course_create"],
    },
    {
        "intent": "exam_add_question",
        "category": "exams",
        "description": "Sınava soru ekleme (Öğretmen+).",
        "response_id": "exam_add_question_instructions",
        "response_template": (
            "Ön koşul: yönetim yetkisi; sınav 'Bitti' veya 'Yakında' değilse sorular "
            "düzenlenebilir. 1) Sınav detayı → **Sorular (Questions)** → **Soru ekle**. "
            "2) **Soru metni** + **Puan** (1–100). 3) **Soru türü**: Seçmeli (2–10 şık, "
            "doğru şıkkı işaretle) veya Metin. 4) **Oluştur**. Metin sorular otomatik "
            "puanlanmaz, elle notlanır."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Sınava nasıl soru eklerim?",
            "Soru eklemek istiyorum",
            "Çoktan seçmeli soru nasıl eklenir?",
            "Sınav sorusu oluşturma",
            "Açık uçlu soru ekleyebilir miyim?",
        ],
        "must_not_match": ["exam_create", "exam_grade_student"],
    },
    {
        "intent": "exam_enter_room",
        "category": "exams",
        "description": "Öğrencinin sınava girmesi/başlaması.",
        "response_id": "exam_enter_room_instructions",
        "response_template": (
            "Ön koşul: sınavın dersine kayıtlı olmak; sınav girilebilir modda "
            "(Senkron/Asenkron/Açık) ve **Aktif** olmalı. 1) Sınav detayında "
            "(`/exams/$id`) **Sınav odasını aç (Open exam room)**'a bas. 2) **Sınava "
            "başla (Start exam)**. Sorular ve **Kalan süre** görünür. 'Yakında/Bitti' "
            "sınavda giriş düğmesi çıkmaz; Zamansız sınavda oturum yoktur."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Sınava nasıl girerim?",
            "Sınav odasını nasıl açarım?",
            "Sınava başlamak istiyorum",
            "Online sınava nasıl katılırım?",
            "Sınavı nereden başlatırım?",
        ],
        "must_not_match": ["exam_save_answer", "exam_finish_result", "exam_modes_info"],
    },
    {
        "intent": "exam_save_answer",
        "category": "exams",
        "description": "Sınav odasında cevap kaydetme.",
        "response_id": "exam_save_answer_instructions",
        "response_template": (
            "Ön koşul: durum 'Devam ediyor', süre bitmemiş. 1) Şık seç veya metin "
            "kutusuna yaz. 2) **Cevabı kaydet (Save answer)**. 3) **Kaydedildi** rozeti "
            "çıkar ve ekran otomatik sonraki soruya kayar. Her cevap tek tek kaydedilir; "
            "toplu gönderim yoktur. Süre bitince cevaplar salt okunur olur."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Cevabımı nasıl kaydederim?",
            "Cevabı kaydet düğmesi ne işe yarar?",
            "Sorunun cevabını nasıl işaretlerim?",
            "Cevaplar otomatik kaydediliyor mu?",
            "Bir soruyu nasıl cevaplarım?",
        ],
        "must_not_match": ["exam_enter_room", "exam_finish_result"],
    },
    {
        "intent": "exam_finish_result",
        "category": "exams",
        "description": "Sınavı bitirme ve sonucu görme.",
        "response_id": "exam_finish_instructions",
        "response_template": (
            "1) Yan panelde **Sınavı bitir (Finish exam)**'e bas ve onayla; durum "
            "**Teslim edildi** olur. 2) Sonucu: girilebilir sınavda sınav odasındaki "
            "**Not** alanından, Zamansız sınavda detaydaki **Sonucun (Your result)** "
            "bölümünden görürsün. Notlanmadıysa 'Henüz notlanmadı' yazar. Süre kendiliğinden "
            "biterse durum 'Süresi doldu' olur."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Sınavı nasıl bitiririm?",
            "Sınavı teslim etmek istiyorum",
            "Sonucumu nereden görürüm?",
            "Notumu ne zaman görebilirim?",
            "Sınavı sonlandırma",
        ],
        "must_not_match": ["exam_save_answer", "report_card_view"],
    },
    {
        "intent": "exam_rejoin_retake",
        "category": "exams",
        "description": "Sınavdan çıkıp dönme (rejoin) veya yeni deneme (retake).",
        "response_id": "exam_rejoin_retake_info",
        "response_template": (
            "**Rejoin (aynı denemeye dönüş):** 'Yeniden girişe izin ver' açıksa odadan "
            "çıktıktan sonra tekrar **Sınav odasını aç** → **Sınava devam et**; kalan "
            "süre ve cevapların korunur. **Retake (yeni deneme):** 'Deneme hakkı' açık ve "
            "azami sayı belirlenmişse her yeni giriş bir deneme kullanır. **Süre çıkışta "
            "bile durmaz.**"
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Sınavdan çıkarsam geri girebilir miyim?",
            "Sınava tekrar girebilir miyim?",
            "Kaldığım yerden devam edebilir miyim?",
            "Deneme hakkım var mı?",
            "Rejoin nasıl çalışır?",
        ],
        "must_not_match": ["exam_enter_room", "exam_finish_result"],
    },
    {
        "intent": "exam_grade_student",
        "category": "exams",
        "description": "Öğrenciye not verme / notlandırma (Öğretmen+).",
        "response_id": "exam_grade_instructions",
        "response_template": (
            "Ön koşul: **sınav bitmiş** olmalı (bitene kadar 'Öğrenci notla' düğmesi "
            "pasiftir). 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi "
            "seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik "
            "puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu "
            "elle verirsin. Verilen not sonuç tablosunda **Kaldır** ile silinebilir."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Öğrenciye nasıl not veririm?",
            "Sınavı nasıl notlandırırım?",
            "Not girme nerede?",
            "Öğrenci notla düğmesi neden pasif?",
            "Sınav sonuçlarını nasıl girerim?",
        ],
        "must_not_match": ["exam_add_question", "student_marks_lookup", "exam_live_monitor"],
    },
    {
        "intent": "exam_live_monitor",
        "category": "exams",
        "description": "Sınavı canlı izleme (Öğretmen+).",
        "response_id": "exam_live_monitor_info",
        "response_template": (
            "Ön koşul: sınav başlamış (Yakında değil) ve girilebilir modda; yönetim "
            "yetkisi. Sınav detayı → **Canlı İzleme (Live Monitor)** (`/exams/$id/live`). "
            "Üstteki sayaçlar (Başlamadı/Devam ediyor/Teslim edildi/Süresi doldu/Katılmadı) "
            "ve **Canlı Liste**'de ilerleme, kalan süre, durum görünür. Sınav bitince ekran "
            "'Son Durum'a döner. Öğrenciler bu ekranı göremez."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Sınavı canlı nasıl izlerim?",
            "Öğrencilerin durumunu anlık görmek istiyorum",
            "Canlı izleme nerede?",
            "Live monitor nasıl açılır?",
            "Kim sınavı bitirmiş görebilir miyim?",
        ],
        "must_not_match": ["exam_grade_student"],
    },
    # --- Karne / notlar ------------------------------------------------------
    {
        "intent": "report_card_view",
        "category": "marks",
        "description": "Öğrencinin kendi karnesini/ortalamasını görmesi.",
        "response_id": "report_card_info",
        "response_template": (
            "Karneni görmek için menüden **Karnem (Report card)** veya `/marks`'a git. "
            "Üstte **Genel ortalama** (sayı + harf notu, /100), altında her ders için "
            "**Ders ortalaması** ve sınav bazında **Ağırlık** ve **Not** görünür. Karnem "
            "yalnızca Öğrenci rolüne açıktır; notu girilmemiş sınav '—' gösterir."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Karnemi nerede görürüm?",
            "Notlarımı göster",
            "Ortalamam kaç?",
            "Ders notlarıma nasıl bakarım?",
            "Genel ortalamamı nereden görürüm?",
        ],
        "must_not_match": ["weighted_average_info", "student_marks_lookup", "exam_finish_result"],
    },
    {
        "intent": "weighted_average_info",
        "category": "marks",
        "description": "Ağırlıklı ortalamanın nasıl hesaplandığı.",
        "response_id": "weighted_average_explained",
        "response_template": (
            "Ders ortalaması, notlanmış sınavların **tür ağırlığıyla** ortalamasıdır: "
            "Σ(not×ağırlık)/Σ(ağırlık). Notlanmamış sınavlar atlanır (sıfır sayılmaz). "
            "Genel ortalama, dolu ders ortalamalarının düz aritmetik ortalamasıdır. "
            "Notlar 0–100 tam sayıdır; harf notu okul ayarındaki not bantlarından gelir."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Ortalama nasıl hesaplanıyor?",
            "Ağırlıklı ortalama ne demek?",
            "Notlar nasıl ağırlıklandırılır?",
            "Genel ortalama nasıl çıkıyor?",
            "Sınav ağırlığı ortalamayı nasıl etkiler?",
        ],
        "must_not_match": ["report_card_view"],
    },
    {
        "intent": "student_marks_lookup",
        "category": "marks",
        "description": "Öğretmenin bir öğrencinin notunu araması (Öğretmen+).",
        "response_id": "student_marks_lookup_instructions",
        "response_template": (
            "1) `/management/student-marks` (Öğrenci notları) sayfasını aç. 2) Aramaya "
            "**en az 2 karakter** yaz. 3) Öğrenci satırında **Görüntüle**'ye bas; sağdan "
            "açılan panelde öğrencinin karnesini görürsün. Bu sayfa Öğretmen ve üstüne açıktır."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Bir öğrencinin notunu nasıl görürüm?",
            "Öğrenci karnesini nasıl açarım?",
            "Öğrenci notları sayfası nerede?",
            "Öğrencinin ortalamasına bakmak istiyorum",
            "Student marks nerede?",
        ],
        "must_not_match": ["report_card_view", "student_attendance_lookup", "exam_grade_student"],
    },
    # --- Yoklama / etkinlik --------------------------------------------------
    {
        "intent": "attendance_view",
        "category": "attendance",
        "description": "Öğrencinin kendi yoklama raporunu görmesi.",
        "response_id": "attendance_report_info",
        "response_template": (
            "Kendi yoklamanı görmek için **Yoklama (Attendance)** menüsünden `/attendance`'a "
            "git. **Etkinlikler** ve **Ders oturumları** için ayrı devam oranı (%) kartları "
            "ve **Ders dökümü** tablosu (ders bazında Var/Yok/Geç/Mazeretli) görürsün. Bu "
            "sayfa yalnızca Öğrenci rolüne açıktır."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Devamsızlığımı nerede görürüm?",
            "Yoklama raporum nerede?",
            "Devam oranımı göster",
            "Kaç gün devamsızlığım var?",
            "Kendi yoklamama nasıl bakarım?",
        ],
        "must_not_match": ["attendance_rate_info", "student_attendance_lookup", "event_attendance_mark"],
    },
    {
        "intent": "attendance_rate_info",
        "category": "attendance",
        "description": "Devam oranının nasıl hesaplandığı.",
        "response_id": "attendance_rate_explained",
        "response_template": (
            "Devam oranı = (Var + Geç) / (Var + Yok + Geç). Geç kalmak 'katıldı' sayılır; "
            "**Mazeretli oranın dışındadır** (ne lehte ne aleyhte). Kayıt yoksa veya "
            "tümü mazeretliyse oran boştur. Etkinlik devamı ile ders oturumu devamı ayrı "
            "hesaplanır."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Devam oranı nasıl hesaplanıyor?",
            "Mazeretli sayılınca oranım düşer mi?",
            "Geç kalmak devamsızlık mı?",
            "Oran neden boş görünüyor?",
            "Devam yüzdesi nasıl çıkıyor?",
        ],
        "must_not_match": ["attendance_view"],
    },
    {
        "intent": "event_attendance_mark",
        "category": "attendance",
        "description": "Etkinlikte kendi yoklamasını işaretleme.",
        "response_id": "event_attendance_instructions",
        "response_template": (
            "1) `/events` → ilgili etkinlik kartına tıkla. 2) **Katılım durumum (My "
            "attendance)** bölümünde durumu seç (**Var / Yok / Geç / Mazeretli**). "
            "3) **Yoklamamı kaydet (Save my attendance)**. Etkinlikte herkes kendini "
            "işaretleyebilir; Öğretmen+ başkasını da işaretleyebilir."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Etkinlikte kendimi nasıl işaretlerim?",
            "Etkinlik yoklamasına nasıl katılırım?",
            "Katılım durumumu nasıl kaydederim?",
            "Etkinliğe geldiğimi nasıl belirtirim?",
            "Kendi yoklamamı işaretleme",
        ],
        "must_not_match": ["attendance_view", "roll_call"],
    },
    {
        "intent": "student_attendance_lookup",
        "category": "attendance",
        "description": "Öğretmenin bir öğrencinin yoklamasını araması (Öğretmen+).",
        "response_id": "student_attendance_lookup_instructions",
        "response_template": (
            "1) `/management/student-attendance` (Öğrenci yoklaması) sayfasını aç. "
            "2) Aramaya **en az 2 karakter** yaz. 3) Öğrenci satırında **Görüntüle**; "
            "sağdan açılan panelde öğrencinin yoklama raporunu görürsün. Öğretmen ve üstüne açıktır."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Bir öğrencinin devamsızlığını nasıl görürüm?",
            "Öğrenci yoklaması sayfası nerede?",
            "Öğrencinin devam durumuna bakmak istiyorum",
            "Student attendance nerede?",
            "Öğrenci devam raporunu aç",
        ],
        "must_not_match": ["attendance_view", "student_marks_lookup", "roll_call"],
    },
    {
        "intent": "event_create",
        "category": "events",
        "description": "Etkinlik oluşturma (Öğretmen+).",
        "response_id": "event_create_instructions",
        "response_template": (
            "Ön koşul: Öğretmen+ rolü. 1) `/events` → **Etkinlik oluştur (Create event)**. "
            "2) **Başlık** (zorunlu, ≤200), isteğe bağlı açıklama; isteğe bağlı "
            "**Başlangıç/Bitiş** tarih+saat. 3) **Oluştur**. Başlık boşsa 'Başlık gerekli'; "
            "bitiş başlangıçtan önce olamaz; tarihler gelecekte olmalı."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Etkinlik nasıl oluşturulur?",
            "Yeni etkinlik eklemek istiyorum",
            "Etkinlik oluşturma nerede?",
            "Bir buluşma/oturum planlayacağım",
            "Event oluşturma",
        ],
        "must_not_match": ["course_create", "lesson_session_add"],
    },
    # --- Defter --------------------------------------------------------------
    {
        "intent": "note_create",
        "category": "notebook",
        "description": "Defterde dosya ekli not oluşturma.",
        "response_id": "note_create_instructions",
        "response_template": (
            "1) **Defter (Notebook)** menüsünden `/notes`'a git, **Yeni not (New note)**'a "
            "bas. 2) **Başlık** (zorunlu, ≤200) ve isteğe bağlı **İçerik** (≤10.000) gir. "
            "3) **Ekler** bölümünde **Dosya ekle** ile en fazla 10 dosya ekle. 4) **Oluştur**. "
            "Notlar yalnızca sahibine görünür; dosya boyut sınırı okul ayarındandır (varsayılan ~5 MiB)."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Nasıl not alırım?",
            "Deftere not eklemek istiyorum",
            "Not oluşturma nerede?",
            "Nota dosya ekleyebilir miyim?",
            "Yeni not nasıl yazılır?",
        ],
        "must_not_match": ["report_card_view"],
    },
    # --- Mesai ---------------------------------------------------------------
    {
        "intent": "work_checkin_out",
        "category": "work",
        "description": "Kendi mesai giriş/çıkışı (Öğretmen/Yönetici).",
        "response_id": "work_checkin_instructions",
        "response_template": (
            "Ön koşul: Öğretmen veya Yönetici (ADMIN'de bu sayfa yoktur). 1) `/work` "
            "(Mesai) sayfasını aç. 2) 'Giriş yapılmadı' ise **Giriş yap (Check in)**; iş "
            "bitince **Çıkış yap (Check out)**. 3) **Son kayıtlar**'da giriş/çıkış/süre ve "
            "Açık/Kapalı durumunu görürsün. Saatler sunucu damgalıdır; aynı anda tek açık "
            "mesai olabilir."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Mesaiye nasıl giriş yaparım?",
            "Check in nasıl yapılır?",
            "Mesai çıkışı nerede?",
            "Giriş-çıkış kaydımı nasıl tutarım?",
            "Work log nasıl kullanılır?",
        ],
        "must_not_match": ["staff_work_manage", "logout_how"],
    },
    {
        "intent": "staff_work_manage",
        "category": "work",
        "description": "Personel mesai kayıtlarını görme/düzeltme (Yönetici+).",
        "response_id": "staff_work_instructions",
        "response_template": (
            "Ön koşul: Yönetici veya ADMIN. 1) `/management/staff-work` (Personel mesai) → "
            "aramaya **en az 2 karakter** (öğretmen adı). 2) Öğretmen satırında **Görüntüle**. "
            "3) **Kapalı** bir kaydın **Düzenle**'sini açıp giriş/çıkış tarih+saat düzelt, "
            "**Güncelle**. **Açık mesai düzeltilemez** (önce çıkış yapılmalı veya silinmeli); "
            "çıkış girişten önce olamaz."
        ),
        "auth_required": True,
        "min_role": "yonetici",
        "example_questions": [
            "Personel mesaisini nasıl düzeltirim?",
            "Bir öğretmenin mesai kaydını görmek istiyorum",
            "Staff work nerede?",
            "Kapalı mesaiyi nasıl düzenlerim?",
            "Personel mesai kaydı silme",
        ],
        "must_not_match": ["work_checkin_out"],
    },
    # --- Yönetim -------------------------------------------------------------
    {
        "intent": "term_manage",
        "category": "management",
        "description": "Akademik dönem oluşturma/derse bağlama (Yönetici+).",
        "response_id": "term_manage_instructions",
        "response_template": (
            "Ön koşul: Yönetici veya ADMIN. 1) `/management/terms` (Dönemler) → **Dönem "
            "oluştur (Create term)**. 2) **Ad**, **Başlangıç**, **Bitiş** (GG/AA/YYYY) gir; "
            "bitiş başlangıçtan önce olamaz (tarihler geçmişte olabilir). 3) **Oluştur**. "
            "Dersi döneme bağlamak, ders oluşturma/düzenleme formundaki **Dönem** seçicisinden "
            "yapılır. Dönem silinince bağlı dersler silinmez, 'Atanmamış' olur."
        ),
        "auth_required": True,
        "min_role": "yonetici",
        "example_questions": [
            "Dönem nasıl oluşturulur?",
            "Akademik dönem eklemek istiyorum",
            "Dersi döneme nasıl bağlarım?",
            "Yarıyıl oluşturma nerede?",
            "Terms sayfası nerede?",
        ],
        "must_not_match": ["school_settings", "course_create"],
    },
    {
        "intent": "school_settings",
        "category": "management",
        "description": "Okul ayarlarını değiştirme (Yönetici+).",
        "response_id": "school_settings_instructions",
        "response_template": (
            "Ön koşul: Yönetici veya ADMIN. `/management/settings` (Okul ayarları) sayfasında "
            "**Sınav türleri** (Ad + Ağırlık 1–100), **Yoklama durumları** (Var/Yok/Geç/"
            "Mazeretli kilitlidir, silinemez), **Not bantları** (Alt sınır + Etiket) ve "
            "**Not dosyası boyut sınırı** (0.001–25 MiB) yönetilir. **Satır ekle** ile ekle, "
            "çöp kutusuyla sil, sonra **Kaydet**. Kaydet yalnızca değişiklik varken aktiftir."
        ),
        "auth_required": True,
        "min_role": "yonetici",
        "example_questions": [
            "Okul ayarlarını nasıl değiştiririm?",
            "Sınav türü ağırlığını nereden ayarlarım?",
            "Not bantlarını düzenlemek istiyorum",
            "Yoklama durumu eklemek istiyorum",
            "Settings sayfası nerede?",
        ],
        "must_not_match": ["term_manage", "language_theme"],
    },
    {
        "intent": "user_role_change",
        "category": "management",
        "description": "Kullanıcı rolü değiştirme (ADMIN).",
        "response_id": "user_role_change_instructions",
        "response_template": (
            "Ön koşul: ADMIN. 1) `/admin/users` (Kullanıcılar) sayfasını aç, gerekirse "
            "kullanıcı adına göre ara. 2) Satırdaki rol menüsünden yeni rolü seç. 3) Beliren "
            "**Güncelle (Update)**'ye bas ve onayla. **Kendi rolünü değiştiremezsin** (kendi "
            "satırında menü pasiftir); rol değişmeden 'Güncelle' görünmez. Değişiklik bir "
            "sonraki işlemde hemen geçerli olur."
        ),
        "auth_required": True,
        "min_role": "admin",
        "example_questions": [
            "Bir kullanıcının rolünü nasıl değiştiririm?",
            "Öğretmen rolü nasıl atanır?",
            "Kullanıcıyı yönetici yapmak istiyorum",
            "Rol yükseltme nerede?",
            "Users sayfasından rol değiştirme",
        ],
        "must_not_match": ["roles_permissions", "profile_edit"],
    },
    # --- Güvenlik ------------------------------------------------------------
    {
        "intent": "privacy_security",
        "category": "security",
        "description": "Başkasının verisini isteme / gizlilik-güvenlik.",
        "response_id": "privacy_policy_message",
        "response_template": (
            "Yalnızca kendi yetkili olduğun bilgileri görebilirsin. Başka bir kullanıcının "
            "notu, yoklaması veya kişisel bilgisi paylaşılmaz. Öğretmen ve üstü roller, "
            "yalnızca yetkili oldukları yönetim sayfalarından (Öğrenci notları/yoklaması) "
            "öğrenci verisine erişebilir; kişisel telefon/e-posta paylaşılmaz."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Arkadaşımın notlarını göster",
            "Başka bir öğrencinin devamsızlığı kaç?",
            "Bir öğrencinin telefonunu verir misin?",
            "Sınıftaki herkesin notlarını göster",
            "Verilerim güvende mi?",
        ],
        "must_not_match": ["student_marks_lookup", "student_attendance_lookup", "account_access_problem"],
    },
]


FALLBACK: Final[dict[str, str]] = {
    "response_id": "fallback_clarification",
    "response_template": (
        "Bu isteği tam anlayamadım. Hezarfen'de ders, sınav, karne, yoklama, defter, "
        "mesai veya hesap ayarları hakkında 'nasıl yaparım?' tarzında daha açık bir "
        "soru sorabilir misin?"
    ),
}


# --- Yardımcı fonksiyonlar ---------------------------------------------------
def role_rank(role: str) -> int:
    """Rolün hiyerarşideki sırasını döndürür.

    Raises:
        KeyError: Bilinmeyen rol adı verilirse.
    """

    return _ROLE_RANK[role]


def is_known_role(role: str) -> bool:
    """Verilen rolün hiyerarşide tanımlı olup olmadığını döndürür."""

    return role in _ROLE_RANK


def meets_role(user_role: str, required_role: str) -> bool:
    """user_role, required_role'ün gerektirdiği yetkiye sahip mi?

    Raises:
        KeyError: Rollerden biri bilinmiyorsa.
    """

    return role_rank(user_role) >= role_rank(required_role)


def get_intent(intent_name: str) -> dict[str, Any] | None:
    """Intent adına göre katalog kaydını döndürür (yoksa None)."""

    return next((item for item in INTENTS if item["intent"] == intent_name), None)


def list_intent_names() -> list[str]:
    """Katalogdaki tüm intent adlarını sırasıyla döndürür."""

    return [item["intent"] for item in INTENTS]


def _duplicates(values: list[str]) -> list[str]:
    """Tekrarlanan değerleri deterministik sırayla döndürür."""

    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def validate_catalog() -> dict[str, int]:
    """Kural motorunun gerektirdiği katalog değişmezlerini doğrular.

    Returns:
        Sayımlar: intent_count, response_count, example_question_count, category_count.

    Raises:
        ValueError: Katalog eksik, tutarsız veya belirsizse.
    """

    if not INTENTS:
        raise ValueError("Intent kataloğu boş olamaz.")

    errors: list[str] = []
    intent_names: list[str] = []
    response_ids: list[str] = []
    questions: list[str] = []
    categories: set[str] = set()

    for index, item in enumerate(INTENTS):
        missing_fields = REQUIRED_INTENT_FIELDS.difference(item)
        if missing_fields:
            errors.append(f"INTENTS[{index}] eksik alanlar: {', '.join(sorted(missing_fields))}")
            continue

        name = item["intent"]
        intent_names.append(name)
        response_ids.append(item["response_id"])
        categories.add(item["category"])

        examples = item["example_questions"]
        if not examples:
            errors.append(f"{name}: en az bir örnek soru gerekli.")
        if any(not isinstance(q, str) or not q.strip() for q in examples):
            errors.append(f"{name}: boş veya metin olmayan örnek soru var.")
        questions.extend(examples)

        # Rol geçerliliği.
        min_role = item["min_role"]
        if not is_known_role(min_role):
            errors.append(f"{name}: bilinmeyen min_role '{min_role}'.")
            continue

        # auth_required ile min_role tutarlılığı.
        expected_auth = role_rank(min_role) >= role_rank(MIN_AUTHENTICATED_ROLE)
        if bool(item["auth_required"]) != expected_auth:
            errors.append(
                f"{name}: auth_required={item['auth_required']} ile min_role='{min_role}' "
                f"tutarsız (beklenen auth_required={expected_auth})."
            )

    duplicate_intents = _duplicates(intent_names)
    duplicate_responses = _duplicates(response_ids)
    duplicate_questions = _duplicates(questions)
    known_intents = set(intent_names)

    if duplicate_intents:
        errors.append(f"Tekrarlanan intent: {duplicate_intents}")
    if duplicate_responses:
        errors.append(f"Tekrarlanan response_id: {duplicate_responses}")
    if duplicate_questions:
        errors.append(f"Tekrarlanan örnek soru: {duplicate_questions}")

    for item in INTENTS:
        targets = set(item.get("must_not_match", []))
        unknown_targets = targets.difference(known_intents)
        if unknown_targets:
            errors.append(
                f"{item.get('intent', '<unknown>')}: bilinmeyen must_not_match "
                f"hedefleri: {sorted(unknown_targets)}"
            )
        if item.get("intent") in targets:
            errors.append(f"{item.get('intent')}: must_not_match kendini içeremez.")

    if not FALLBACK.get("response_id") or not FALLBACK.get("response_template"):
        errors.append("Fallback cevabı eksik.")

    if errors:
        raise ValueError("Katalog doğrulanamadı:\n- " + "\n- ".join(errors))

    return {
        "intent_count": len(intent_names),
        "response_count": len(response_ids),
        "example_question_count": len(questions),
        "category_count": len(categories),
    }
