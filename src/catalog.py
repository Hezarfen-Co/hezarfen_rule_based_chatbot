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
    "veli",       # bağlı öğrencilerin salt-okunur gözlemcisi (backend: Parent)
    "ogrenci",
    "ogretmen",
    "yonetici",
    "admin",
)

_ROLE_RANK: Final[dict[str, int]] = {role: rank for rank, role in enumerate(ROLE_HIERARCHY)}

# Oturum açmış sayılan en düşük rol.
MIN_AUTHENTICATED_ROLE: Final[str] = "veli"


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



# Asistanın adı: Hezarfen Ahmed Çelebi'ye saygıyla. Arayüzler (web/cli) ve
# cevap metinleri bu sabiti kullanır; isim değişirse tek yer burası.
ASSISTANT_NAME: Final[str] = "Çelebi"

# Selamlama aynalama: kullanıcı 'günaydın' derse cevap da 'Günaydın!' ile başlar.
# Anahtarlar katlanmış (ascii) formdadır; greeting şablonundaki {selam} yerine
# geçer. Eşleşme yoksa varsayılan kullanılır. Uzun anahtarlar önce denenir.
GREETING_OPENERS: Final[dict[str, str]] = {
    "gunaydin": "Günaydın! ☀️",
    "iyi gunler": "İyi günler! 🌞",
    "iyi aksamlar": "İyi akşamlar! 🌙",
    "selam": "Selam! 👋",
    "hey": "Selam! 👋",
    "merhaba": "Merhaba!",
}
DEFAULT_GREETING_OPENER: Final[str] = "Merhaba!"


INTENTS: Final[list[dict[str, Any]]] = [
    # --- Genel ---------------------------------------------------------------
    {
        "intent": "greeting",
        "category": "general",
        "description": "Kullanıcının selam vermesi / sohbeti başlatması.",
        "response_id": "welcome_message",
        "response_template": (
            "{selam} Ben Çelebi 🪽 — Hezarfen'in kullanım asistanı. Ders, sınav, "
            "karne, yoklama, defter ve mesai gibi konularda 'nasıl yaparım?' "
            "sorularını yanıtlayabilirim. Ne yapmak istiyorsun?"
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": ["Merhaba", "Selam", "Günaydın", "İyi günler", "Hey"],
        "must_not_match": ["help_capabilities", "smalltalk"],
    },
    {
        "intent": "smalltalk",
        "category": "general",
        "description": "Hatır sorma / sohbet ('naber', 'nasılsın') — kısa samimi yanıt.",
        "response_id": "smalltalk_reply",
        "response_template": (
            "İyiyim, sorduğun için sağ ol! 😊 Umarım senin de moralin yerindedir. "
            "Ben Çelebi; asıl işim Hezarfen'de yolunu bulmana yardım etmek. Ders, "
            "sınav, karne, yoklama veya hesap ayarları hakkında 'nasıl yaparım?' "
            "diye sorabilirsin."
        ),
        "response_variants": [
            "Keyfim yerinde, teşekkürler! 🪽 Sen nasılsın bakalım? Hazır buradayken "
            "Hezarfen'le ilgili merak ettiğin bir şey varsa çekinme — ders, sınav, "
            "karne... ne istersen sor.",
            "İyidir iyidir! 😄 Çelebi her zaman görev başında. Söyle bakalım, "
            "Hezarfen'de bugün ne yapmak istiyorsun?",
        ],
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": ["Naber", "Nasılsın", "Ne haber", "Napıyorsun", "İyi misin"],
        "must_not_match": ["greeting"],
    },
    {
        "intent": "thanks",
        "category": "general",
        "description": "Teşekkür etme — kibar kapanış yanıtı.",
        "response_id": "thanks_reply",
        "response_template": (
            "Rica ederim! 😊 Başka bir konuda takıldığında yine sorabilirsin — "
            "ders, sınav, karne, yoklama, defter... hepsi için buradayım."
        ),
        "response_variants": [
            "Ne demek, her zaman! 🪽 Yardımcı olabildiysem ne mutlu. Başka bir "
            "sorun olursa Çelebi burada.",
            "Rica ederim, kolay gelsin! 😊 Takıldığın başka bir yer olursa "
            "sormaktan çekinme.",
        ],
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": ["Teşekkürler", "Sağ ol", "Teşekkür ederim", "Eyvallah", "Çok sağol"],
        "must_not_match": [],
    },
    {
        "intent": "farewell",
        "category": "general",
        "description": "Vedalaşma — sohbeti kapatma yanıtı.",
        "response_id": "farewell_reply",
        "response_template": (
            "Görüşmek üzere! 👋 Hezarfen'de yolun düştüğünde yine buradayım. "
            "İyi çalışmalar!"
        ),
        "response_variants": [
            "Hoşça kal! 🪽 İhtiyacın olduğunda Çelebi bir mesaj uzağında. "
            "Kendine iyi bak!",
            "Görüşürüz, iyi günler! 👋 Derslerin ve sınavların kolay geçsin.",
        ],
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": ["Görüşürüz", "Hoşça kal", "İyi geceler", "Ben kaçtım", "Kendine iyi bak"],
        "must_not_match": ["greeting"],
    },
    {
        "intent": "bot_identity",
        "category": "general",
        "description": "Botun kim/ne olduğunun sorulması ('sen kimsin', 'robot musun').",
        "response_id": "bot_identity_reply",
        "response_template": (
            "Ben Çelebi 🪽 — Hezarfen'in kullanım asistanıyım. Adımı, Galata "
            "Kulesi'nden uçtuğu rivayet edilen Hezarfen Ahmed Çelebi'den alıyorum. "
            "Serbest metin üreten bir yapay zekâ değil, kural tabanlı bir yardımcıyım: "
            "sitedeki gerçek menü ve sayfalara dayanarak 'nasıl yaparım?' sorularını "
            "yanıtlar, seni doğru sayfaya yönlendiririm. Bir şey sormak ister misin?"
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": ["Sen kimsin?", "Adın ne?", "Robot musun?", "Yapay zeka mısın?", "Seni kim yaptı?"],
        "must_not_match": ["smalltalk", "help_capabilities", "platform_info"],
    },
    {
        "intent": "platform_info",
        "category": "general",
        "description": "Hezarfen nedir — platformun ne olduğunun sorulması.",
        "response_id": "platform_overview",
        "response_template": (
            "Hezarfen, bir okulun **ders, sınav, not, yoklama, etkinlik ve personel "
            "mesaisini tek yerde** toplayan bir okul yönetim sitesidir — sloganı: "
            "\"Kampüs çalışma alanın: notlar, etkinlikler ve sınavlar tek yerde.\" "
            "Temel akış **Ders → Sınav → Karne**: öğretmen ders açar, öğrenci sınavlara "
            "girer, notlar **Karnem**'de ağırlıklı ortalamayla toplanır. Ayrıca kişisel "
            "**Defter**, **Etkinlikler**, **Yoklama** ve personel için **Mesai** var. "
            "Ben Çelebi, bu siteyi nasıl kullanacağını adım adım anlatırım — 'ne yapmak "
            "istiyorsun?' diye sorabilirsin."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Hezarfen nedir?",
            "Bu site ne işe yarıyor?",
            "Hezarfen ne demek?",
            "Bu uygulama nedir?",
            "Hezarfen'i kısaca anlatır mısın?",
        ],
        "must_not_match": ["help_capabilities", "bot_identity", "guide_info"],
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
            "Senin yardım menün bulunuyor mu?",
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
            "Kullanıcı adı ve şifre ile giriş nereden yapılır?",
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
            "Öğrenci hesabı oluşturmak istiyorum",
            "Öğrenci hesabı açmak istiyorum",
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
            "Güvenli şekilde çıkış yapmak istiyorum",
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
            "Sistem beni ne zaman otomatik atar?",
            "Ne zaman sistemden atılırım?",
            "Beni oturumdan ne zaman düşürür?",
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
            "Profilime telefon numarası eklemek istiyorum",
            "Numaramı profilime nasıl eklerim?",
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
            "Görünümü koyudan açığa alabilir miyim?",
            "Arayüz görünümünü açık veya koyu yapabilir miyim?",
            "Ekran görünümünü koyu yapabilir miyim?",
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
            "Hezarfen'de roller şöyle sıralanır: **Veli < Öğrenci < Öğretmen < "
            "Yönetici < ADMIN**. Üst rol, alt rolün yaptığı her şeyi yapar; **Veli** "
            "istisnadır — yalnızca kendine bağlanan öğrencileri salt-okunur izler "
            "(sınava giremez, derse kaydolamaz). Kayıt olan herkes Öğrenci başlar; "
            "diğer roller sonradan bir ADMIN tarafından atanır. Rol her istekte "
            "yeniden kontrol edilir; değişince yeniden giriş gerekmez. **Kendi "
            "rolünü** sol menünün altındaki hesap kutusunda, adının yanındaki rol "
            "rozetinden görebilirsin."
        ),
        "auth_required": True,
        "min_role": "veli",
        "example_questions": [
            "Roller nelerdir?",
            "Yetkiler nasıl çalışıyor?",
            "Öğretmen neler yapabilir?",
            "ADMIN ile Yönetici farkı ne?",
            "Kimin hangi yetkisi var?",
            "Rolüm ne benim?",
            "Kendi rolümü nereden görürüm?",
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
            "Sayfalar arası geçiş nasıl yapılır?",
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
            "**Eğitim** sayfası (`/courses`): dersler, **etütler** ve **kulüpler** tek "
            "yerde (üstteki **Tümü / Dersler / Etüt / Kulüp** sekmeleriyle süz). Arama "
            "ve döneme göre filtreleme yapabilirsin; öğrenci yalnızca kayıtlı olduklarını "
            "görür ('Kayıtlı' rozeti). Bir öğeyi açmak için **Görüntüle (View)**'ye bas; "
            "detay `/courses/$id`'de sınavları, oturumları ve (yetkiliysen) katılımcı "
            "listesini gösterir. Öğretmen+ sağ üstten **Yeni** oluşturabilir."
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
            "1) `/courses`'a git, **Yeni ders (New "
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
            "Ön koşul: bu dersi yönetme yetkin olmalı. 1) Ders detayına "
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
            "Sınıfıma öğrenci almak istiyorum",
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
            "Bir öğrencinin kaydını iptal etmek istiyorum",
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
            "düzenlenebilir. Ayrıca ders detayında en az bir **Konu (Subject)** "
            "tanımlı olmalı — her sınav sorusu bir konuya bağlanır. 1) Sınav detayı → "
            "**Sorular (Questions)** → **Soru ekle**. 2) **Soru metni** + **Puan** "
            "(1–100) + **Konu** seç. 3) **Soru türü**: Seçmeli (2–10 şık, doğru şıkkı "
            "işaretle) veya Metin. 4) **Oluştur**. Metin sorular otomatik puanlanmaz, "
            "elle notlanır."
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
        "must_not_match": ["exam_add_question", "student_marks_lookup", "exam_live_monitor", "report_card_view"],
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
            "Kim başlamış canlı görmek istiyorum",
            "Öğrenciler sınava başladı mı anlık görmek istiyorum",
        ],
        "must_not_match": ["exam_grade_student"],
    },
    # --- Ödev (backend/frontend'de bağımsız modül; rehberdeki "Ödev" ise sınav
    # TÜRÜdür — ayrı şey. İçerik frontend'den: /homework, "Ödevler" menüsü) --------
    {
        "intent": "homework_view",
        "category": "homework",
        "description": "Ödevleri/atanan ödevleri görüntüleme.",
        "response_id": "homework_view_info",
        "response_template": (
            "Ödevleri **Akademik** grubundaki **Ödevler** menüsünden (`/homework`) "
            "görürsün. Öğrencide sayfa **Ödevlerim** başlığıyla açılır; her kartta "
            "**Son teslim** tarihi ve durum görünür. Bir ödevin detayına gitmek için "
            "**Aç**'a bas (`/homework/$id`). Öğretmen ve üstü, verdikleri ödevleri ve "
            "**Teslimler**'i aynı sayfadan takip eder."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Ödevlerimi nerede görürüm?",
            "Ödevler sayfası nerede?",
            "Bana verilen ödevler neler?",
            "Ödev son teslim tarihlerini nereden takip ederim?",
            "Ödevlerim listesi nerede?",
        ],
        "must_not_match": ["homework_submit", "course_view", "exam_modes_info"],
    },
    {
        "intent": "homework_submit",
        "category": "homework",
        "description": "Öğrencinin ödevini teslim etmesi.",
        "response_id": "homework_submit_instructions",
        "response_template": (
            "Ön koşul: ödevin verildiği dersin kayıtlı öğrencisisin. 1) **Ödevler** "
            "(`/homework`) → ilgili ödevin detayına (`/homework/$id`) gir. 2) **Ödevi "
            "teslim et** panelinde cevabını yaz ve/veya dosya ekle. 3) Gönder. Teslim "
            "yalnızca Öğrenciye açıktır; **Son teslim** tarihine dikkat et."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Ödevimi nasıl teslim ederim?",
            "Ödev teslimi nereden yapılır?",
            "Verilen ödevi nasıl yüklerim?",
            "Ödev cevabımı nasıl gönderirim?",
            "Ödevimi göndermek istiyorum",
        ],
        "must_not_match": ["homework_view", "homework_grade", "exam_save_answer"],
    },
    {
        "intent": "homework_assign",
        "category": "homework",
        "description": "Ödev oluşturma/atama (Öğretmen+).",
        "response_id": "homework_assign_instructions",
        "response_template": (
            "Ön koşul: yönettiğin bir ders olmalı. 1) **Ödevler** (`/homework`) → "
            "**Ödev ekle**. 2) Dersi seç, başlık ve açıklamayı gir, **Son teslim** "
            "tarihini belirle. 3) Oluştur. Ödev dersin öğrencilerine atanır; gelen "
            "teslimleri ödev detayındaki **Teslimler** bölümünden görürsün."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Ödev nasıl veririm?",
            "Yeni ödev eklemek istiyorum",
            "Öğrencilere ödev atamak istiyorum",
            "Ödev oluşturma nerede?",
            "Sınıfıma ödev vermek istiyorum",
        ],
        "must_not_match": ["homework_grade", "homework_submit", "exam_create"],
    },
    {
        "intent": "homework_grade",
        "category": "homework",
        "description": "Ödev teslimlerini notlandırma (Öğretmen+).",
        "response_id": "homework_grade_instructions",
        "response_template": (
            "Ön koşul: ödevi verdiğin (yönettiğin) ders. 1) **Ödevler** (`/homework`) → "
            "ödevin detayı → **Teslimler**. 2) Bir öğrencinin teslimini aç, **Notlandır** "
            "ile not/geri bildirim ver; gerekirse **Notu kaldır** ile geri al. "
            "Notlandırma Öğretmen ve üstüne açıktır; kendi teslimini notlandıramazsın."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Ödevi nasıl notlandırırım?",
            "Öğrenci ödevine not vermek istiyorum",
            "Ödev teslimlerini nereden değerlendiririm?",
            "Ödev notu girme nerede?",
            "Teslim edilen ödevleri notlandırma",
        ],
        "must_not_match": ["homework_assign", "exam_grade_student", "homework_submit"],
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
            "Notumu nasıl görürüm?",
            "Notumu öğrenmek istiyorum",
            "Kaç aldım?",
            "Sınav sonucumu nerede görürüm?",
            "Kendi notumu görmek istiyorum",
            "Notlarım nerede?",
            "Notlarımı nereden öğrenebilirim?",
            "Sınav sonuçlarım nerede?",
            "Sonuçlarımı merak ediyorum",
            "Sonuçlarım nerede?",
            "Aldığım notlar nerede?",
        ],
        "must_not_match": [
            "weighted_average_info", "student_marks_lookup", "exam_finish_result",
            "exam_grade_student",
        ],
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
            "Ortalamaya girmeyen not olur mu?",
            "Hangi notlar ortalamaya dahil edilmez?",
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
            "Devam oranının formülü ne?",
            "Devam oranı hangi formülle bulunur?",
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
            "Etkinlikte var olarak işaretlenmek istiyorum",
            "Etkinliğe geldim, var demek istiyorum",
            "Etkinlikte kendimi var olarak göstermek istiyorum",
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
            "1) `/events` → **Etkinlik oluştur (Create event)**. "
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
            "Ön koşul: bu sayfa ADMIN hesabında bulunmaz. 1) `/work` "
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
            "Çıkış saatimi kaydetmek istiyorum",
            "Mesai çıkış saatimi nasıl kaydederim?",
            "Giriş çıkış saatimi kaydetmek istiyorum",
        ],
        "must_not_match": ["staff_work_manage", "logout_how"],
    },
    {
        "intent": "staff_work_manage",
        "category": "work",
        "description": "Personel mesai kayıtlarını görme/düzeltme (Yönetici+).",
        "response_id": "staff_work_instructions",
        "response_template": (
            "1) `/management/staff-work` (Personel mesai) → "
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
            "Bir mesai kaydını düzenlemek istiyorum",
            "Mesai kaydını düzeltmek istiyorum",
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
            "1) `/management/terms` (Dönemler) → **Dönem "
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
            "Dönem yönetim ekranına nereden ulaşırım?",
        ],
        "must_not_match": ["school_settings", "course_create"],
    },
    {
        "intent": "school_settings",
        "category": "management",
        "description": "Okul ayarlarını değiştirme (Yönetici+).",
        "response_id": "school_settings_instructions",
        "response_template": (
            "`/management/settings` (Okul ayarları) sayfasında "
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
        "description": "Kullanıcılar sayfası: rol değiştirme + profil düzenleme (ADMIN).",
        "response_id": "user_role_change_instructions",
        "response_template": (
            "**Ne:** **Kullanıcılar** (`/admin/users`, yalnız ADMIN) tüm hesapları "
            "yönettiğin yerdir — burada (a) **rol değiştirir**, (b) **herhangi bir "
            "kullanıcının profilini düzenlersin**.\n"
            "**Nereden / nasıl (rol):** 1) `/admin/users`'ı aç, ada göre **ara**. "
            "2) Satırdaki **rol menüsünden** yeni rolü seç. 3) Beliren **Güncelle "
            "(Update)**'ye basıp onayla. Kendi rolünü değiştiremezsin (kendi satırında "
            "menü pasif); değişiklik sonraki işlemde hemen geçerli olur.\n"
            "**Etkili kullanım:** kalabalık listede önce **arama/filtre** ile daralt; "
            "rolü yanlışlıkla düşürmemek için değişiklikten önce satırdaki adı teyit et. "
            "Profil düzeltmek için kullanıcının satırından profiline geçip alanları güncelle."
        ),
        "auth_required": True,
        "min_role": "admin",
        "example_questions": [
            "Kullanıcılar kısmında ne yapabilirim?",
            "Bir kullanıcının rolünü nasıl değiştiririm?",
            "Öğretmen rolü nasıl atanır?",
            "Kullanıcıyı yönetici yapmak istiyorum",
            "Rol yükseltme nerede?",
            "Kullanıcı profilini düzenleme nerede?",
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
    # --- Pomodoro / Mesajlar / Etüt-Kulüp / Veli (backend v2 özellikleri) -----
    {
        "intent": "pomodoro_use",
        "category": "pomodoro",
        "description": "Pomodoro odak oturumu başlatma/bitirme (tüm roller).",
        "response_id": "pomodoro_instructions",
        "response_template": (
            "Pomodoro, sunucu saatiyle damgalanan kişisel odak kaydıdır; giriş yapan "
            "her kullanıcı kendi oturumunu tutabilir. 1) `/pomodoro` sayfasına git. "
            "2) **Odağı başlat (Start focus)** ile oturumu aç — aynı anda tek açık "
            "oturum olabilir. 3) Çalışman bitince **Odağı bitir (Finish focus)**'a bas. "
            "Sayfada **Toplam odak** süreni ve **Son oturumlar** geçmişini görürsün; "
            "saatler sunucu tarafından damgalanır."
        ),
        "auth_required": True,
        "min_role": "veli",
        "example_questions": [
            "Pomodoro nasıl kullanılır?",
            "Odak oturumu nasıl başlatırım?",
            "Pomodoro sayacı nerede?",
            "Çalışma odağımı nasıl kaydederim?",
            "Odağı bitir düğmesi ne yapıyor?",
            "Toplam odak süremi nereden görürüm?",
            "Odak sürelerimi nerede görüyorum?",
            "Ne kadar odak yaptığımı nereden görürüm?",
        ],
        "must_not_match": ["student_pomodoro_lookup"],
    },
    {
        "intent": "student_pomodoro_lookup",
        "category": "pomodoro",
        "description": "Öğretmenin bir öğrencinin pomodoro geçmişine bakması (Öğretmen+).",
        "response_id": "student_pomodoro_lookup_instructions",
        "response_template": (
            "Bir öğrencinin odak geçmişi için: 1) Yönetim menüsünden **Pomodorolar** "
            "(`/management/pomodoros`) sayfasına git. 2) Arama kutusuna öğrenci adını "
            "yaz ve seç. 3) Panelde o öğrencinin oturumları **Başlangıç / Bitiş / "
            "Süre** sütunlarıyla listelenir. Bu sayfa Öğretmen ve üstüne açıktır."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Öğrencinin pomodoro geçmişini nasıl görürüm?",
            "Bir öğrencinin odak oturumlarına bakmak istiyorum",
            "Öğrenci pomodoroları nerede?",
            "Öğrencimin çalışma sürelerini görebilir miyim?",
        ],
        "must_not_match": ["pomodoro_use"],
    },
    {
        "intent": "messages_use",
        "category": "messages",
        "description": "Mesajlar: kullanıcılar arası bire-bir mesaj gönderme/okuma.",
        "response_id": "messages_instructions",
        "response_template": (
            "**Mesajlar** (`/messages`), kullanıcılar arasında bire-bir, posta tarzı "
            "yazışma içindir. Sol menüden **Mesajlar**'ı aç: **Gelen kutusu**ndaki "
            "mesajları okuyabilir, mesajları **Arşiv**'e veya **Çöp**'e taşıyabilir, "
            "yeni mesaj oluşturup konu + metin yazarak gönderebilirsin. Karşı tarafın "
            "kopyası senin silmenden etkilenmez. (Bu bölüm yeni ekleniyor; arayüzün "
            "son hâli sürüme göre değişebilir.)"
        ),
        "auth_required": True,
        "min_role": "veli",
        "example_questions": [
            "Mesajlarım nerede?",
            "Nasıl mesaj gönderirim?",
            "Gelen kutusunu nasıl açarım?",
            "Öğretmenime mesaj atabilir miyim?",
            "Mesajı arşive nasıl taşırım?",
        ],
        "must_not_match": ["privacy_security"],
    },
    {
        "intent": "study_club_info",
        "category": "courses",
        "description": "Etüt ve Kulüp nedir — ders türleri (course/study/club).",
        "response_id": "study_club_info_message",
        "response_template": (
            "**Etüt** ve **Kulüp**, dersin iki özel türüdür — ders altyapısının "
            "aynısını kullanırlar (kayıt, oturum, yoklama, hatta sınav). Sol menüde "
            "**Etüt** (`/studies`) ve **Kulüp** (`/clubs`) ayrı listeler olarak "
            "görünür; oluştururken tür seçilir. Katılım ve yönetim kuralları dersle "
            "aynıdır: Öğretmen+ oluşturur, öğrenci kaydolur; kontenjan (kapasite) "
            "sınırı konabilir."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Etüt nedir?",
            "Kulüp nasıl çalışıyor?",
            "Etüt ile ders arasındaki fark ne?",
            "Kulübe nasıl katılırım?",
            "Etüt oluşturabilir miyim?",
        ],
        "must_not_match": ["course_create", "course_view"],
    },
    {
        "intent": "parent_info",
        "category": "roles",
        "description": "Veli rolü nedir, veli neler görebilir.",
        "response_id": "parent_role_info",
        "response_template": (
            "**Veli**, kendisine bağlanan öğrencileri **salt-okunur** izleyen roldür: "
            "bağlı öğrencinin notlarını/karnesini ve yoklamasını görüntüleyebilir, "
            "Mesajlar'ı kullanabilir. Veli hesabı sınava giremez, derse kaydolamaz ve "
            "yoklamada işaretlenmez — bu işlemler öğrenciye özeldir. Veli–öğrenci "
            "bağlantısını **ADMIN** kurar; birden çok öğrenci bir veliye bağlanabilir."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Veli rolü nedir?",
            "Veli neler görebilir?",
            "Velimi hesabıma nasıl bağlarım?",
            "Veli çocuğunun notlarını görebilir mi?",
            "Ebeveyn hesabı ne işe yarar?",
        ],
        "must_not_match": ["roles_permissions"],
    },
    # --- Kapsam genişletme: menüdeki sayfa/bölüm açıklama intent'leri -----------
    {
        "intent": "fees_info",
        "category": "school",
        "description": "Okul ücretleri/ödeme bilgisinin nerede görüleceği.",
        "response_id": "fees_info_message",
        "response_template": (
            "Okul **ücretleri** ve ödeme bilgilerini menüdeki **Ücretler** "
            "sayfasından görürsün; borç ve ödeme durumu burada listelenir."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Okul ücretlerini nereden görürüm?",
            "Ödeme bilgilerim nerede?",
            "Ücretler sayfası nerede?",
        ],
        "must_not_match": ["report_card_view", "exam_finish_result"],
    },
    {
        "intent": "branches_info",
        "category": "school",
        "description": "Şubeler (şube/sınıf) sayfası ne işe yarar.",
        "response_id": "branches_info_message",
        "response_template": (
            "**Şubeler** sayfasında okulun şubeleri/sınıfları listelenir; hangi "
            "**şube**de olduğunu ve şubenin ders/öğrenci bilgisini buradan görürsün."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Şubeler sayfası nerede?",
            "Hangi şubedeyim?",
            "Şube listesini nereden görürüm?",
        ],
        "must_not_match": [],
    },
    {
        "intent": "calendar_info",
        "category": "general",
        "description": "Takvim / haftalık ders programı sayfası.",
        "response_id": "calendar_info_message",
        "response_template": (
            "**Takvim** sayfasında etkinlikler, ders oturumları ve haftalık "
            "**program** takvim görünümünde listelenir; günlere göre planı buradan izlersin."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Takvim sayfasını nasıl açarım?",
            "Haftalık ders programım nerede?",
            "Takvimi nereden görürüm?",
        ],
        "must_not_match": ["report_card_view", "exam_schedule_info"],
    },
    {
        "intent": "today_info",
        "category": "general",
        "description": "Bugün / ana panel ne gösterir.",
        "response_id": "today_info_message",
        "response_template": (
            "**Bugün** panelinde günün özeti bir arada görünür: yaklaşan sınavlar, "
            "ödevler ve etkinlikler tek ekranda listelenir."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Bugün panelinde neleri görürüm?",
            "Bugün paneli ne işe yarar?",
            "Ana panelde ne var?",
        ],
        "must_not_match": ["roles_permissions", "help_capabilities"],
    },
    {
        "intent": "question_bank_info",
        "category": "exams",
        "description": "Soru bankası nedir / ne işe yarar.",
        "response_id": "question_bank_info_message",
        "response_template": (
            "**Soru bankası**, öğretmenlerin hazır soru şablonlarını saklayıp "
            "sınavlara eklediği depodur; tekrar kullanılabilir sorular burada tutulur."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Soru bankası ne işe yarar?",
            "Soru bankası nerede?",
            "Hazır sorular nerede saklanır?",
        ],
        "must_not_match": ["exam_add_question", "parent_info"],
    },
    {
        "intent": "notification_settings_info",
        "category": "account",
        "description": "Bildirim ayarlarının nereden değiştirileceği.",
        "response_id": "notification_settings_message",
        "response_template": (
            "**Bildirim** tercihlerini ayarlar bölümünden düzenleyebilirsin; hangi "
            "olaylarda bildirim alacağını buradan seçer veya kapatırsın."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Bildirim ayarlarını nereden değiştiririm?",
            "Bildirimleri nasıl kapatırım?",
            "Bildirim tercihleri nerede?",
        ],
        "must_not_match": ["school_settings", "language_theme"],
    },
    {
        "intent": "nav_overview",
        "category": "general",
        "description": "Menü bölümlerinin genel özeti (hangi bölümde ne var).",
        "response_id": "nav_overview_message",
        "response_template": (
            "Sol menü şu bölümlerden oluşur: **Bugün**; **Eğitim** (Takvim); "
            "**Akademik** (Ödevler, Sınavlar, Soru bankası); **Planlama** "
            "(Etkinlikler, Randevular); **Çalışma alanı** (Defter, Beyaz tahtalar); "
            "**Öğrenci yönetimi** (Şubeler, Öğrenci notları/yoklamaları); **Okul "
            "hizmetleri** (Yemekler); **Topluluk** (Mesajlar, Soru havuzu); **Okul "
            "yönetimi** / Yönetim (Personel mesaisi); **Ayarlar** (Dönemler, "
            "Ücretler, Kullanıcılar). **ADMIN** ek olarak kullanıcı ve rol "
            "yönetimi yapar. Hangi bölümü açmak istediğini yazarsan yolunu veririm."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Menüde hangi bölümler var?",
            "Öğrenci yönetimi bölümü ne işe yarar?",
            "Akademik bölümü altında neler var?",
            "Yönetim menüsünü kısaca anlatır mısın?",
            "ADMIN bölümünde hangi sayfalar var?",
        ],
        "must_not_match": ["help_capabilities", "parent_info", "navigation_help"],
    },
    {
        "intent": "event_view",
        "category": "events",
        "description": "Etkinliklerin nerede görüntüleneceği.",
        "response_id": "event_view_message",
        "response_template": (
            "Okuldaki **etkinlikleri** menüdeki **Etkinlikler** (`/events`) "
            "sayfasından görürsün; yaklaşan ve katılacağın etkinlikler burada listelenir."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Etkinlikleri nerede görürüm?",
            "Etkinlikler sayfası nerede?",
            "Yaklaşan etkinlikler nerede listelenir?",
        ],
        "must_not_match": ["event_create", "homework_view", "event_attendance_mark"],
    },
    {
        "intent": "exam_schedule_info",
        "category": "exams",
        "description": "Sınav takvimi / sınav tarihleri nerede.",
        "response_id": "exam_schedule_message",
        "response_template": (
            "**Sınav** takvimini ve **tarih**lerini **Sınavlar** (`/exams`) "
            "sayfasından görürsün; yaklaşan sınavların tarihleri burada listelenir."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Sınav tarihleri nerede yazıyor?",
            "Sınav takvimimi nereden görürüm?",
            "Sınavlarımın tarihi nerede?",
        ],
        "must_not_match": ["exam_create", "homework_view", "calendar_info"],
    },
    {
        "intent": "course_materials_info",
        "category": "courses",
        "description": "Ders notları / öğretmenin yüklediği dosyalar (course-notes).",
        "response_id": "course_materials_message",
        "response_template": (
            "Öğretmenin yüklediği **ders notları** ve **PDF/dosya**lar ilgili "
            "dersin sayfasındadır: **Dersler** (`/courses`) → ders → Ders notları."
        ),
        "auth_required": False,
        "min_role": "ziyaretci",
        "example_questions": [
            "Ders notları nerede?",
            "Öğretmenin yüklediği PDF nerede?",
            "Ders dosyalarını nereden indiririm?",
        ],
        "must_not_match": ["note_create", "report_card_view"],
    },
    # --- Randevu (T1; frontend /appointments, "Randevular" menüsü) ------------
    {
        "intent": "appointment_book",
        "category": "appointments",
        "description": "Öğrenci/velinin randevu alması.",
        "response_id": "appointment_book_instructions",
        "response_template": (
            "Randevu almak için **Planlama** grubundaki **Randevular** "
            "(`/appointments`) sayfasına git. **Öğretmenlerin açık saatleri** "
            "bölümünden uygun saati seç, **Randevu al**'a bas. Talebin "
            "**Randevularım** altında görünür ve öğretmen onayına düşer. Randevu "
            "alma yalnızca Öğrenci ve Veli'ye açıktır."
        ),
        "auth_required": True,
        "min_role": "veli",
        "example_questions": [
            "Randevu nasıl alırım?",
            "Öğretmenden randevu almak istiyorum",
            "Randevu talebi oluşturmak istiyorum",
            "Görüşme randevusu talep etmek istiyorum",
            "Randevu alma nerede?",
        ],
        "must_not_match": ["appointment_slot_open", "appointment_requests"],
    },
    {
        "intent": "appointment_slot_open",
        "category": "appointments",
        "description": "Öğretmenin müsait randevu saati açması (Öğretmen+).",
        "response_id": "appointment_slot_instructions",
        "response_template": (
            "**Randevular** (`/appointments`) → **Açtığım "
            "saatler** bölümünde **Saat aç** (veya **Yeni saat**) ile müsait "
            "randevu saati yayınla. Öğrenci ve veliler bu saatlerden randevu talep "
            "eder; gelen talepleri **Randevu talepleri**'nden yönetirsin."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Randevu saati nasıl açarım?",
            "Öğrencilere müsait saat yayınlamak istiyorum",
            "Randevu için saat açma nerede?",
            "Müsaitlik saati eklemek istiyorum",
            "Öğrencilere randevu saati açmak istiyorum",
        ],
        "must_not_match": ["appointment_book", "appointment_requests"],
    },
    {
        "intent": "appointment_requests",
        "category": "appointments",
        "description": "Öğretmenin randevu taleplerini onaylaması (Öğretmen+).",
        "response_id": "appointment_requests_instructions",
        "response_template": (
            "**Randevular** (`/appointments`) → **Randevu "
            "talepleri** bölümünde gelen talepleri görürsün; her talepte **Onayla** "
            "ile kabul et (gerekirse reddet). Onaylanan randevu, ilgili öğrenci/"
            "velinin **Randevularım**'ında görünür."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Randevu taleplerini nasıl onaylarım?",
            "Gelen randevu isteklerini nerede görürüm?",
            "Randevu talebini kabul etmek istiyorum",
            "Öğrenci randevu talebini onaylama",
            "Randevu isteklerini yönetmek istiyorum",
        ],
        "must_not_match": ["appointment_book", "appointment_slot_open"],
    },
    # --- Yemek (T1; frontend /meals, "Yemekler" menüsü) -----------------------
    {
        "intent": "meal_view",
        "category": "meals",
        "description": "Yemek menülerini/rezervasyon durumunu görüntüleme.",
        "response_id": "meal_view_info",
        "response_template": (
            "Yemek menülerini **Okul hizmetleri** grubundaki **Yemekler** "
            "(`/meals`) sayfasından görürsün. Günün **Menü** ve **Öğün**lerini, "
            "rezervasyon durumunu (**Rezerve edildi** / **Rezervasyon yok**) "
            "görebilirsin. Detay için menü kartına bas (`/meals/$id`)."
        ),
        "auth_required": True,
        "min_role": "veli",
        "example_questions": [
            "Yemek menüsü nerede?",
            "Yemek menüsünü görmek istiyorum",
            "Yemekler sayfası nerede?",
            "Öğün menüsü nerede?",
            "Yemek listesi nerede?",
        ],
        "must_not_match": ["meal_book", "meal_menu_manage"],
    },
    {
        "intent": "meal_book",
        "category": "meals",
        "description": "Öğün için yer ayırma/iptal (Öğrenci/Veli).",
        "response_id": "meal_book_instructions",
        "response_template": (
            "Yemek için yer ayırmak üzere **Yemekler** (`/meals`) → ilgili menü/"
            "öğüne gir, **Yer ayır**'a bas. Rezervasyonun **Rezerve edildi** olarak "
            "görünür; **Rezervasyonu iptal et** ile geri alabilirsin. Yer ayırma "
            "Öğrenci (kendisi) ve Veli'ye (bağlı çocuğu) açıktır."
        ),
        "auth_required": True,
        "min_role": "veli",
        "example_questions": [
            "Yemek için yer ayırmak istiyorum",
            "Öğün rezervasyonu nasıl yapılır?",
            "Yer ayırma nerede?",
            "Yemek rezervasyonu yapmak istiyorum",
            "Yemek rezervasyonumu iptal etmek istiyorum",
        ],
        "must_not_match": ["meal_view", "meal_menu_manage"],
    },
    {
        "intent": "meal_menu_manage",
        "category": "meals",
        "description": "Menü/öğün/kredi yönetimi (Yönetici+).",
        "response_id": "meal_menu_instructions",
        "response_template": (
            "**Yemekler** (`/meals`) → **Menü yayınla** ile "
            "yeni menü/öğün oluştur, **Yemek ekle** ile öğüne yemek ekle. Öğrenci "
            "**Kredi** yönetimi için **Kredi kaydet** kullanılır. Menü ve kredi "
            "yönetimi yalnızca Yönetici ve ADMIN'e açıktır."
        ),
        "auth_required": True,
        "min_role": "yonetici",
        "example_questions": [
            "Menü nasıl yayınlarım?",
            "Yeni menü oluşturmak istiyorum",
            "Öğüne yemek eklemek istiyorum",
            "Yemek kredisi nasıl kaydedilir?",
            "Kredi kaydetme nerede?",
        ],
        "must_not_match": ["meal_book", "meal_view"],
    },
    # --- Soru havuzu (T1; frontend /questions "Soru havuzu"; sınav "Soru
    # bankası"/question-bank'ten AYRI. Veli havuzdan hariç) --------------------
    {
        "intent": "question_ask",
        "category": "questions",
        "description": "Soru havuzuna soru sorma (Öğrenci+, Veli hariç).",
        "response_id": "question_ask_instructions",
        "response_template": (
            "**Topluluk** grubundaki **Soru havuzu** (`/questions`) sayfasına git. "
            "**Soru sor**'a bas; **Konu**, **Soru detayı** ve isteğe bağlı **Görsel** "
            "ekleyip gönder. Sorun önce **Bekliyor** durumundadır; bir öğretmen "
            "onaylayınca **Onaylandı** olur ve herkese görünür. Soru havuzu Öğrenci "
            "ve üstüne açıktır (Veli hariç)."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Soru havuzuna nasıl soru sorarım?",
            "Soru havuzu nedir?",
            "Havuza yeni soru sormak istiyorum",
            "Soru havuzunda soru sorma nerede?",
            "Soru havuzuna bir soru sormak istiyorum",
        ],
        "must_not_match": ["question_solve", "question_approve", "exam_add_question"],
    },
    {
        "intent": "question_solve",
        "category": "questions",
        "description": "Havuzdaki bir soruya çözüm gönderme (Öğrenci+).",
        "response_id": "question_solve_instructions",
        "response_template": (
            "Bir soruya çözüm göndermek için **Soru havuzu** (`/questions`) → soruyu "
            "aç (`/questions/$id`) → **Çözümler** bölümünde **Çözüm gönder** ile "
            "çözümünü yaz ve paylaş. Çözüm gönderme Öğrenci ve üstüne açıktır."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Bir soruya nasıl çözüm gönderirim?",
            "Çözüm önermek istiyorum",
            "Soruya çözüm yazmak istiyorum",
            "Çözüm paylaşmak istiyorum",
            "Soruyu nasıl çözerim?",
        ],
        "must_not_match": ["question_ask", "question_approve"],
    },
    {
        "intent": "question_approve",
        "category": "questions",
        "description": "Havuzdaki soruları onaylama/reddetme (Öğretmen+).",
        "response_id": "question_approve_instructions",
        "response_template": (
            "**Soru havuzu** (`/questions`) → soru detayında "
            "**Onayla** ile bekleyen soruyu yayınla, gerekirse **Reddet**. Onaylanan "
            "soru **Onaylandı** olur ve herkese görünür. Onaylama Öğretmen ve üstüne açıktır."
        ),
        "auth_required": True,
        "min_role": "ogretmen",
        "example_questions": [
            "Havuzdaki soruları nasıl onaylarım?",
            "Bekleyen soruları onaylamak istiyorum",
            "Öğrenci sorusunu reddetmek istiyorum",
            "Soru onaylama nerede?",
            "Havuzdaki soruları onaylamak istiyorum",
        ],
        "must_not_match": ["question_ask", "question_solve"],
    },
    # --- Beyaz tahta (T1; frontend /whiteboards "Beyaz tahtalar"; Veli hariç) --
    {
        "intent": "board_view",
        "category": "boards",
        "description": "Beyaz tahtaları görüntüleme/açma (Öğrenci+, Veli hariç).",
        "response_id": "board_view_info",
        "response_template": (
            "Beyaz tahtaları **Çalışma alanı** grubundaki **Beyaz tahtalar** "
            "(`/whiteboards`) sayfasından görürsün. Bir tahtayı açmak için kartında "
            "**Aç**'a bas (`/whiteboards/$id`); katılımcılar eşzamanlı çizer. Beyaz "
            "tahtalar Öğrenci ve üstüne açıktır (Veli hariç)."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Beyaz tahtalar nerede?",
            "Var olan bir tahtayı nasıl açarım?",
            "Beyaz tahta sayfası nerede?",
            "Tahtaları nereden görürüm?",
            "Ortak çalışma tahtaları nerede?",
        ],
        "must_not_match": ["board_create"],
    },
    {
        "intent": "board_create",
        "category": "boards",
        "description": "Yeni beyaz tahta oluşturma (Öğrenci+, Veli hariç).",
        "response_id": "board_create_instructions",
        "response_template": (
            "Yeni beyaz tahta için **Beyaz tahtalar** (`/whiteboards`) → **Yeni tahta** "
            "ile **Başlık** gir, isteğe bağlı **Katılımcılar** ekle, oluştur. Tahta "
            "içinde **Kilitle/Kilidi aç**, **Temizle** ve **Tahtayı kapat** kontrolleri "
            "vardır; Öğretmen+ **Toplu davet** ile sınıf/etkinlik katılımcısı çağırabilir."
        ),
        "auth_required": True,
        "min_role": "ogrenci",
        "example_questions": [
            "Yeni beyaz tahta nasıl oluştururum?",
            "Yeni tahta oluşturmak istiyorum",
            "Beyaz tahta eklemek istiyorum",
            "Tahta oluşturma nerede?",
            "Yeni bir tahta oluşturmak istiyorum",
        ],
        "must_not_match": ["board_view"],
    },
]


# Yalnız KURAL ile tetiklenen intent'ler: benzerlik (TF-IDF) havuzuna ALINMAZLAR.
# Ortak kelimeleri (bugün, menü, program, panel...) IDF'i kirletip OOS ayrımını
# bozuyordu; sayfa-arama/bölüm-özeti intent'leri deterministik kuralla kapsanır.
RULE_ONLY_INTENTS: Final[frozenset[str]] = frozenset({
    "fees_info", "branches_info", "calendar_info", "today_info",
    "question_bank_info", "notification_settings_info", "nav_overview",
    "event_view", "exam_schedule_info", "course_materials_info",
    # T1 özellikleri: kural-tetikli; örnek soruları similarity/domain havuzuna
    # ALINMAZ (yeni intent'ler TF-IDF/OOS'u kirletmesin — coverage intent'leri gibi).
    "appointment_book", "appointment_slot_open", "appointment_requests",
    "meal_view", "meal_book", "meal_menu_manage",
    "question_ask", "question_solve", "question_approve",
    "board_view", "board_create",
})


FALLBACK: Final[dict[str, str]] = {
    "response_id": "fallback_clarification",
    "response_template": (
        "Bu isteği tam anlayamadım. Hezarfen'de ders, sınav, karne, yoklama, defter, "
        "mesai veya hesap ayarları hakkında 'nasıl yaparım?' tarzında daha açık bir "
        "soru sorabilir misin?"
    ),
}


# --- Yönlendirme (navigation) ------------------------------------------------
# Her intent'i, kullanıcıyı götürecek gerçek sayfa yoluna eşler. Yollar
# `hezarfen-site-rehberi.md` §4 URL tablosundan birebir alınmıştır (uydurma yok).
# Dinamik yollar ($id gerektirenler) genel liste sayfasına yönlendirilir; asistan
# tekil ID'yi bilmediğinden dürüst davranıp listeye götürür. None = ilgili bir
# sayfa yok (bilgi/açıklama intent'i, ör. selamlama, rol açıklaması).
INTENT_ROUTES: Final[dict[str, str | None]] = {
    "greeting": None,
    "smalltalk": None,
    "thanks": None,
    "farewell": None,
    "bot_identity": None,
    "platform_info": "/guide",
    "help_capabilities": None,
    "guide_info": "/guide",
    "login_how": "/login",
    "register_how": "/register",
    "logout_how": None,
    "session_info": None,
    "account_access_problem": "/login",
    "profile_edit": "/profile",
    "language_theme": None,
    "roles_permissions": None,
    "access_denied_help": None,
    "navigation_help": "/",
    "course_view": "/courses",
    "course_create": "/courses",
    "course_enroll_student": "/courses",
    "course_remove_student": "/courses",
    "lesson_session_add": "/courses",
    "roll_call": "/courses",
    "exam_modes_info": None,
    "exam_create": "/exams",
    "exam_add_question": "/exams",
    "exam_enter_room": "/exams",
    "exam_save_answer": "/exams",
    "exam_finish_result": "/exams",
    "exam_rejoin_retake": "/exams",
    "exam_grade_student": "/exams",
    "exam_live_monitor": "/exams",
    "homework_view": "/homework",
    "homework_submit": "/homework",
    "homework_assign": "/homework",
    "homework_grade": "/homework",
    "report_card_view": "/marks",
    "weighted_average_info": "/marks",
    "student_marks_lookup": "/management/student-marks",
    "attendance_view": "/attendance",
    "attendance_rate_info": "/attendance",
    "event_attendance_mark": "/events",
    "student_attendance_lookup": "/management/student-attendance",
    "event_create": "/events",
    "note_create": "/notes",
    "work_checkin_out": "/work",
    "staff_work_manage": "/management/staff-work",
    "term_manage": "/management/terms",
    "school_settings": "/management/settings",
    "user_role_change": "/admin/users",
    "privacy_security": None,
    "pomodoro_use": "/pomodoro",
    "student_pomodoro_lookup": "/management/pomodoros",
    "messages_use": "/messages",
    "study_club_info": "/studies",
    "parent_info": None,
    # Kapsam genişletme:
    "fees_info": "/payments",
    "branches_info": "/classes",
    "calendar_info": "/calendar",
    "today_info": "/",
    "question_bank_info": "/question-bank",
    "notification_settings_info": None,
    "nav_overview": None,
    "event_view": "/events",
    "exam_schedule_info": "/exams",
    "course_materials_info": "/courses",
    # T1 özellikleri (frontend rotalarıyla birebir)
    "appointment_book": "/appointments",
    "appointment_slot_open": "/appointments",
    "appointment_requests": "/appointments",
    "meal_view": "/meals",
    "meal_book": "/meals",
    "meal_menu_manage": "/meals",
    "question_ask": "/questions",
    "question_solve": "/questions",
    "question_approve": "/questions",
    "board_view": "/whiteboards",
    "board_create": "/whiteboards",
}

# Yol -> arayüzde görünen sayfa adı (buton etiketi için). Rehber §4'teki TR etiketler.
ROUTE_LABELS: Final[dict[str, str]] = {
    "/": "Ana sayfa",
    "/login": "Giriş sayfası",
    "/register": "Kayıt sayfası",
    "/courses": "Dersler",
    "/exams": "Sınavlar",
    "/homework": "Ödevler",
    "/events": "Etkinlikler",
    "/appointments": "Randevular",
    "/meals": "Yemekler",
    "/questions": "Soru havuzu",
    "/whiteboards": "Beyaz tahtalar",
    "/marks": "Karnem",
    "/attendance": "Yoklama",
    "/notes": "Defter",
    "/profile": "Profili düzenle",
    "/guide": "Rehber",
    "/work": "Mesai",
    "/management/student-marks": "Öğrenci notları",
    "/management/student-attendance": "Öğrenci yoklaması",
    "/management/staff-work": "Personel mesai",
    "/pomodoro": "Pomodoro",
    "/management/pomodoros": "Pomodorolar",
    "/messages": "Mesajlar",
    "/studies": "Etüt",
    "/clubs": "Kulüp",
    "/management/settings": "Ayarlar",
    "/management/terms": "Dönemler",
    "/admin/users": "Kullanıcılar",
    "/payments": "Ücretler",
    "/classes": "Şubeler",
    "/calendar": "Takvim",
    "/question-bank": "Soru bankası",
}


def route_for(intent_name: str) -> tuple[str, str] | None:
    """Intent için (yol, sayfa_adı) döndürür; sayfası olmayan intent'lerde None."""

    route = INTENT_ROUTES.get(intent_name)
    if not route:
        return None
    return route, ROUTE_LABELS.get(route, route)


# --- Rol beyanı / role özel yetenek özeti ------------------------------------
# Kullanıcı yalnızca rolünü söylediğinde ("Öğrenci", "ben öğretmenim") o role özel
# ne yapabileceğini özetler. İçerik `hezarfen-site-rehberi.md` §2 yetki matrisinden.
ROLE_CAPABILITIES: Final[dict[str, str]] = {
    "veli": (
        "Veli olarak, sana bağlanan öğrencilerin **salt-okunur gözlemcisisin**: "
        "bağlı öğrencinin notlarını/karnesini ve yoklamasını görüntüleyebilir, "
        "etkinlikleri ve dersleri izleyebilirsin. Veli hesabı sınava giremez, derse "
        "kaydolamaz ve yoklamada işaretlenmez — bunlar öğrenciye özeldir. "
        "Öğrenci bağlantısını ADMIN yapar. Kendi profilini düzenleyebilir ve "
        "Mesajlar'ı kullanabilirsin."
    ),
    "ogrenci": (
        "Öğrenci olarak şunları yapabilirsin: derslere kaydolmak ve sınavlara girmek "
        "(**Sınav odası**), notlarını **Karnem**'de ağırlıklı ortalamayla görmek, "
        "**Yoklama** raporunu takip etmek, kişisel **Defter** tutmak, etkinliklerde "
        "kendi katılımını işaretlemek ve profilini düzenlemek. "
        "Örneğin 'karnemi nerede görürüm' ya da 'sınava nasıl girerim' diye sorabilirsin."
    ),
    "ogretmen": (
        "Öğretmen olarak şunları yapabilirsin: **ders, sınav ve etkinlik oluşturmak**, "
        "derse öğrenci kaydetmek, sınava soru eklemek, **notlandırmak**, ders oturumu "
        "açıp **yoklama almak**, sınavı **canlı izlemek**, öğrenci not/yoklamasını "
        "aramak, **Mesai** kaydı tutmak ve Defter kullanmak. "
        "Örneğin 'sınav nasıl oluşturulur' ya da 'yoklama nasıl alınır' diye sorabilirsin."
    ),
    "yonetici": (
        "Yönetici olarak öğretmenin tüm yetkilerine ek olarak: **her dersi/etkinliği "
        "düzenleyip silmek** (başkasınınki dâhil), **Okul ayarlarını** ve **Dönemleri** "
        "yönetmek, **Personel mesaisini** görüp düzeltmek. "
        "Örneğin 'okul ayarları nerede' ya da 'dönem nasıl oluşturulur' diye sorabilirsin."
    ),
    "admin": (
        "ADMIN olarak yöneticinin tüm yetkilerine ek olarak: **kullanıcı rollerini "
        "değiştirmek** (kendi rolün hariç) ve herhangi bir kullanıcının profilini "
        "düzenlemek. Not: ADMIN'de kişisel mesai kaydı yoktur. "
        "Örneğin 'kullanıcı rolü nasıl değiştirilir' diye sorabilirsin."
    ),
}

# Serbest metindeki rol kelimelerini (ve okul-özel adlarını) kanonik role eşler.
ROLE_ALIASES: Final[dict[str, str]] = {
    "veli": "veli", "ebeveyn": "veli",
    "ogrenci": "ogrenci", "talebe": "ogrenci",
    "ogretmen": "ogretmen", "hoca": "ogretmen",
    "yonetici": "yonetici", "mudur": "yonetici",
    "admin": "admin",
}


def capabilities_for(role: str) -> str | None:
    """Kanonik rol için yetenek özeti (yoksa None)."""

    return ROLE_CAPABILITIES.get(role)


# Role göre başlangıç soru önerileri (frontend "altta tıklanabilir çip" olarak
# gösterir). Her öneri gerçek bir intent'e çözülür — uydurma yönlendirme yok.
ROLE_SUGGESTIONS: Final[dict[str, list[str]]] = {
    "ziyaretci": [
        "Hezarfen nedir?",
        "Nasıl üye olurum?",
        "Nasıl giriş yaparım?",
    ],
    "veli": [
        "Veli neler görebilir?",
        "Roller ve yetkiler nedir?",
        "Mesajlar nerede?",
    ],
    "ogrenci": [
        "Karnemi nerede görürüm?",
        "Sınava nasıl girerim?",
        "Devamsızlığımı nasıl takip ederim?",
        "Deftere not nasıl eklerim?",
    ],
    "ogretmen": [
        "Sınav nasıl oluşturulur?",
        "Yoklama nasıl alınır?",
        "Öğrenci notunu nasıl girerim?",
        "Yeni ders nasıl açılır?",
    ],
    "yonetici": [
        "Okul ayarları nerede?",
        "Dönem nasıl oluşturulur?",
        "Personel mesaisini nasıl görürüm?",
    ],
    "admin": [
        "Kullanıcı rolü nasıl değiştirilir?",
        "Okul ayarları nerede?",
        "Dönem nasıl oluşturulur?",
    ],
}


def suggestions_for(role: str) -> list[str]:
    """Rol için başlangıç soru önerileri (bilinmeyen rolde ziyaretçi listesi)."""

    return ROLE_SUGGESTIONS.get(role, ROLE_SUGGESTIONS["ziyaretci"])


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

        # Opsiyonel cevap varyantları (aynı response_id altında metin çeşitliliği).
        variants = item.get("response_variants")
        if variants is not None:
            if not isinstance(variants, list) or not variants:
                errors.append(f"{name}: response_variants boş olmayan bir liste olmalı.")
            elif any(not isinstance(v, str) or not v.strip() for v in variants):
                errors.append(f"{name}: boş veya metin olmayan response_variant var.")

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

    # Yönlendirme: her intent'in bir route eşlemesi olmalı (None de olabilir ama
    # anahtar bulunmalı) ve tanımlı her yolun bir etiketi olmalı.
    missing_routes = known_intents.difference(INTENT_ROUTES)
    if missing_routes:
        errors.append(f"INTENT_ROUTES eksik intent(ler): {sorted(missing_routes)}")
    unlabeled = {r for r in INTENT_ROUTES.values() if r and r not in ROUTE_LABELS}
    if unlabeled:
        errors.append(f"ROUTE_LABELS'ta etiketi olmayan yol(lar): {sorted(unlabeled)}")

    if errors:
        raise ValueError("Katalog doğrulanamadı:\n- " + "\n- ".join(errors))

    return {
        "intent_count": len(intent_names),
        "response_count": len(response_ids),
        "example_question_count": len(questions),
        "category_count": len(categories),
    }
