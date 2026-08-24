# Çelebi Benchmark Soru-Cevap Sonuçları

Bu dosya `python benchmark_qa_report.py` komutuyla tek gold kaynak `data/benchmark.jsonl` üzerinden üretilir. Birleşik ve rol bazında filtrelenebilir makine sonucu `data/benchmark_results.json` dosyasındadır. Her soru, kullanıcının gördüğü tam `Engine.handle` akışında çalıştırılır. PASS; intent, rol sonucu, response kimliği ve iki yönlendirme sözleşmesinin tamamını kapsar.

## Özet

- Toplam soru: **601**
- PASS: **601**
- FAIL: **0**
- Kullanıcı-akışı sözleşme başarısı: **100.0%**

| Rol | Toplam | PASS | FAIL |
|---|---:|---:|---:|
| Ziyaretçi | 27 | 27 | 0 |
| Veli | 40 | 40 | 0 |
| Öğrenci | 263 | 263 | 0 |
| Öğretmen | 162 | 162 | 0 |
| Yönetici | 70 | 70 | 0 |
| ADMIN | 39 | 39 | 0 |

## Hatalar

Tüm benchmark soruları beklenen intent ile sonuçlandı.

## Tüm soru ve cevaplar

### 001 · PASS · Ziyaretçi

- Soru: Selamlar
- Beklenen intent: `greeting`
- Gerçek intent: `greeting`
- response_id: `welcome_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Selam! 👋 Ben Çelebi 🪽 — Hezarfen'in kullanım asistanı. Ders, sınav, karne, yoklama, defter ve mesai gibi konularda 'nasıl yaparım?' sorularını yanıtlayabilirim. Ne yapmak istiyorsun?

### 002 · PASS · Ziyaretçi

- Soru: Naber dostum
- Beklenen intent: `smalltalk`
- Gerçek intent: `smalltalk`
- response_id: `smalltalk_reply`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> İyiyim, sorduğun için sağ ol! 😊 Umarım senin de moralin yerindedir. Ben Çelebi; asıl işim Hezarfen'de yolunu bulmana yardım etmek. Ders, sınav, karne, yoklama veya hesap ayarları hakkında 'nasıl yaparım?' diye sorabilirsin.

### 003 · PASS · Öğrenci

- Soru: Sen nasılsın bakalım
- Beklenen intent: `smalltalk`
- Gerçek intent: `smalltalk`
- response_id: `smalltalk_reply`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Keyfim yerinde, teşekkürler! 🪽 Sen nasılsın bakalım? Hazır buradayken Hezarfen'le ilgili merak ettiğin bir şey varsa çekinme — ders, sınav, karne... ne istersen sor.

### 004 · PASS · Öğrenci

- Soru: Ne haber kanka
- Beklenen intent: `smalltalk`
- Gerçek intent: `smalltalk`
- response_id: `smalltalk_reply`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> İyiyim, sorduğun için sağ ol! 😊 Umarım senin de moralin yerindedir. Ben Çelebi; asıl işim Hezarfen'de yolunu bulmana yardım etmek. Ders, sınav, karne, yoklama veya hesap ayarları hakkında 'nasıl yaparım?' diye sorabilirsin.

### 005 · PASS · Ziyaretçi

- Soru: Merhaba asistan
- Beklenen intent: `greeting`
- Gerçek intent: `greeting`
- response_id: `welcome_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Merhaba! Ben Çelebi 🪽 — Hezarfen'in kullanım asistanı. Ders, sınav, karne, yoklama, defter ve mesai gibi konularda 'nasıl yaparım?' sorularını yanıtlayabilirim. Ne yapmak istiyorsun?

### 006 · PASS · Ziyaretçi

- Soru: Sen ne yapabiliyorsun tam olarak?
- Beklenen intent: `help_capabilities`
- Gerçek intent: `help_capabilities`
- response_id: `capabilities`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hezarfen sitesini nasıl kullanacağını anlatabilirim: ders/sınav oluşturma, sınava girme, karne ve ortalama, yoklama, defter, mesai, dönem ve okul ayarları, kullanıcı rolleri ve daha fazlası. Rolünü (Öğrenci/Öğretmen/Yönetici/ADMIN) söylersen sana uygun adımları veririm.

### 007 · PASS · Ziyaretçi

- Soru: Yardım menün var mı?
- Beklenen intent: `help_capabilities`
- Gerçek intent: `help_capabilities`
- response_id: `capabilities`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hezarfen sitesini nasıl kullanacağını anlatabilirim: ders/sınav oluşturma, sınava girme, karne ve ortalama, yoklama, defter, mesai, dönem ve okul ayarları, kullanıcı rolleri ve daha fazlası. Rolünü (Öğrenci/Öğretmen/Yönetici/ADMIN) söylersen sana uygun adımları veririm.

### 008 · PASS · Ziyaretçi

- Soru: Hangi işlerde bana destek olursun?
- Beklenen intent: `help_capabilities`
- Gerçek intent: `help_capabilities`
- response_id: `capabilities`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hezarfen sitesini nasıl kullanacağını anlatabilirim: ders/sınav oluşturma, sınava girme, karne ve ortalama, yoklama, defter, mesai, dönem ve okul ayarları, kullanıcı rolleri ve daha fazlası. Rolünü (Öğrenci/Öğretmen/Yönetici/ADMIN) söylersen sana uygun adımları veririm.

### 009 · PASS · Öğrenci

- Soru: Uygulamanın kendi kılavuzu nerede?
- Beklenen intent: `guide_info`
- Gerçek intent: `guide_info`
- response_id: `guide_page_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Rehber", "route": "/guide"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Uygulama içi rehbere hesap (avatar) menüsünden **Rehber (Guide)** ile veya doğrudan `/guide` adresinden ulaşırsın. Rehber; **Çelebi**, **Defter**, **Soru havuzu**, **Dersler**, **Sınavlar** ve **Karnem** adımlarını, ayrıca rol yetkileri ile kullanım ipuçlarını içerir.

### 010 · PASS · Öğrenci

- Soru: Adım adım tanıtım var mı?
- Beklenen intent: `guide_info`
- Gerçek intent: `guide_info`
- response_id: `guide_page_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Rehber", "route": "/guide"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Uygulama içi rehbere hesap (avatar) menüsünden **Rehber (Guide)** ile veya doğrudan `/guide` adresinden ulaşırsın. Rehber; **Çelebi**, **Defter**, **Soru havuzu**, **Dersler**, **Sınavlar** ve **Karnem** adımlarını, ayrıca rol yetkileri ile kullanım ipuçlarını içerir.

### 011 · PASS · Öğrenci

- Soru: Guide bölümü ne işe yarar?
- Beklenen intent: `guide_info`
- Gerçek intent: `guide_info`
- response_id: `guide_page_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Rehber", "route": "/guide"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Uygulama içi rehbere hesap (avatar) menüsünden **Rehber (Guide)** ile veya doğrudan `/guide` adresinden ulaşırsın. Rehber; **Çelebi**, **Defter**, **Soru havuzu**, **Dersler**, **Sınavlar** ve **Karnem** adımlarını, ayrıca rol yetkileri ile kullanım ipuçlarını içerir.

### 012 · PASS · Ziyaretçi

- Soru: Hesabıma giriş yapmak için ne yapmalıyım?
- Beklenen intent: `login_how`
- Gerçek intent: `login_how`
- response_id: `login_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Giriş sayfası", "route": "/login"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Giriş yapmak için `/login` sayfasına git, **Kullanıcı adı (Username)** (3–32 karakter) ve **Şifre (Password)** (6–128) alanlarını doldur, **Giriş yap (Log in)** düğmesine bas. Başarılı girişte Ana sayfaya (`/`) yönlendirilirsin; hatalı bilgide formun üstünde kırmızı hata kutusu çıkar.

### 013 · PASS · Ziyaretçi

- Soru: Kullanıcı adı ve şifreyle nereden girerim?
- Beklenen intent: `login_how`
- Gerçek intent: `login_how`
- response_id: `login_instructions`
- confidence: `0.6619`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Giriş sayfası", "route": "/login"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Giriş yapmak için `/login` sayfasına git, **Kullanıcı adı (Username)** (3–32 karakter) ve **Şifre (Password)** (6–128) alanlarını doldur, **Giriş yap (Log in)** düğmesine bas. Başarılı girişte Ana sayfaya (`/`) yönlendirilirsin; hatalı bilgide formun üstünde kırmızı hata kutusu çıkar.

### 014 · PASS · Ziyaretçi

- Soru: Log in ekranına nasıl gelirim?
- Beklenen intent: `login_how`
- Gerçek intent: `login_how`
- response_id: `login_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Giriş sayfası", "route": "/login"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Giriş yapmak için `/login` sayfasına git, **Kullanıcı adı (Username)** (3–32 karakter) ve **Şifre (Password)** (6–128) alanlarını doldur, **Giriş yap (Log in)** düğmesine bas. Başarılı girişte Ana sayfaya (`/`) yönlendirilirsin; hatalı bilgide formun üstünde kırmızı hata kutusu çıkar.

### 015 · PASS · Ziyaretçi

- Soru: Sisteme yeni üye olmak istiyorum ne yapmalıyım?
- Beklenen intent: `register_how`
- Gerçek intent: `register_how`
- response_id: `register_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Kayıt sayfası", "route": "/register"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kayıt için `/register` sayfasına git; **Kullanıcı adı** (3–32), **Şifre** (6–128) ve **Şifreyi onayla (Confirm password)** alanlarını doldurup **Hesap oluştur (Create account)**'a bas. Yeni hesaplar **Öğrenci** olarak başlar; kayıt otomatik giriş yapmaz, giriş sayfasına yönlendirilirsin. Kullanıcı adı yalnız küçük ASCII harf, sayı ve `._-` kabul eder; ayraçla başlayıp/bitemez ve iki ayraç art arda gelemez. 'admin/root/support' gibi personel çağrıştıran adlar reddedilir. Aynı kullanıcı adı yeniden gönderildiğinde güvenlik için yine başarılı kayıt görünümü alınabilir ama ikinci hesap oluşturulmaz.

### 016 · PASS · Ziyaretçi

- Soru: Öğrenci hesabı nasıl açarım?
- Beklenen intent: `register_how`
- Gerçek intent: `register_how`
- response_id: `register_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Kayıt sayfası", "route": "/register"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kayıt için `/register` sayfasına git; **Kullanıcı adı** (3–32), **Şifre** (6–128) ve **Şifreyi onayla (Confirm password)** alanlarını doldurup **Hesap oluştur (Create account)**'a bas. Yeni hesaplar **Öğrenci** olarak başlar; kayıt otomatik giriş yapmaz, giriş sayfasına yönlendirilirsin. Kullanıcı adı yalnız küçük ASCII harf, sayı ve `._-` kabul eder; ayraçla başlayıp/bitemez ve iki ayraç art arda gelemez. 'admin/root/support' gibi personel çağrıştıran adlar reddedilir. Aynı kullanıcı adı yeniden gönderildiğinde güvenlik için yine başarılı kayıt görünümü alınabilir ama ikinci hesap oluşturulmaz.

### 017 · PASS · Ziyaretçi

- Soru: Kayıt formu nerede?
- Beklenen intent: `register_how`
- Gerçek intent: `register_how`
- response_id: `register_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Kayıt sayfası", "route": "/register"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kayıt için `/register` sayfasına git; **Kullanıcı adı** (3–32), **Şifre** (6–128) ve **Şifreyi onayla (Confirm password)** alanlarını doldurup **Hesap oluştur (Create account)**'a bas. Yeni hesaplar **Öğrenci** olarak başlar; kayıt otomatik giriş yapmaz, giriş sayfasına yönlendirilirsin. Kullanıcı adı yalnız küçük ASCII harf, sayı ve `._-` kabul eder; ayraçla başlayıp/bitemez ve iki ayraç art arda gelemez. 'admin/root/support' gibi personel çağrıştıran adlar reddedilir. Aynı kullanıcı adı yeniden gönderildiğinde güvenlik için yine başarılı kayıt görünümü alınabilir ama ikinci hesap oluşturulmaz.

### 018 · PASS · Öğrenci

- Soru: Güvenli çıkış nasıl yapılır?
- Beklenen intent: `logout_how`
- Gerçek intent: `logout_how`
- response_id: `logout_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Çıkış yapmak için sol menü altındaki hesap kutusunu (ad-soyad) aç ve **Çıkış yap (Log out)**'a bas. Oturum hemen kapanır.

### 019 · PASS · Öğrenci

- Soru: Oturumu kapatmak istiyorum
- Beklenen intent: `logout_how`
- Gerçek intent: `logout_how`
- response_id: `logout_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Çıkış yapmak için sol menü altındaki hesap kutusunu (ad-soyad) aç ve **Çıkış yap (Log out)**'a bas. Oturum hemen kapanır.

### 020 · PASS · Öğrenci

- Soru: Sistemden nasıl çıkarım?
- Beklenen intent: `logout_how`
- Gerçek intent: `logout_how`
- response_id: `logout_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Çıkış yapmak için sol menü altındaki hesap kutusunu (ad-soyad) aç ve **Çıkış yap (Log out)**'a bas. Oturum hemen kapanır.

### 021 · PASS · Öğrenci

- Soru: Beni ne zaman sistemden atar?
- Beklenen intent: `session_info`
- Gerçek intent: `session_info`
- response_id: `session_duration_info`
- confidence: `0.7528`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Giriş yapınca **7 gün** geçerli bir oturum açılır. Süre sunucu saatiyle ölçülür; cihazının saati yanlış olsa bile değişmez. Çıkış yapmak oturumu hemen kapatır. Süre dolduktan sonra korumalı bir istek **401** dönebilir; bu durumda `/login` üzerinden yeniden giriş yap.

### 022 · PASS · Öğrenci

- Soru: Girişim kaç gün geçerli?
- Beklenen intent: `session_info`
- Gerçek intent: `session_info`
- response_id: `session_duration_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Giriş yapınca **7 gün** geçerli bir oturum açılır. Süre sunucu saatiyle ölçülür; cihazının saati yanlış olsa bile değişmez. Çıkış yapmak oturumu hemen kapatır. Süre dolduktan sonra korumalı bir istek **401** dönebilir; bu durumda `/login` üzerinden yeniden giriş yap.

### 023 · PASS · Öğrenci

- Soru: Oturumum sürekli açık mı kalıyor?
- Beklenen intent: `session_info`
- Gerçek intent: `session_info`
- response_id: `session_duration_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Giriş yapınca **7 gün** geçerli bir oturum açılır. Süre sunucu saatiyle ölçülür; cihazının saati yanlış olsa bile değişmez. Çıkış yapmak oturumu hemen kapatır. Süre dolduktan sonra korumalı bir istek **401** dönebilir; bu durumda `/login` üzerinden yeniden giriş yap.

### 024 · PASS · Ziyaretçi

- Soru: Parolamı hatırlamıyorum ne yapayım?
- Beklenen intent: `account_access_problem`
- Gerçek intent: `account_access_problem`
- response_id: `access_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Giriş sayfası", "route": "/login"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hatalı kullanıcı adı/şifrede giriş formunun üstünde aynı kırmızı **401** hata kutusu çıkar; sistem hangi alanın yanlış olduğunu açıklamaz. Kayıt başarılı göründüğü hâlde yeni bilgilerle giriş olmuyorsa aynı kullanıcı adının daha önce alınmış olabileceğini ve kayıt kurallarını kontrol et. Rehberde self-servis bir 'şifremi unuttum' akışı tanımlı değil; kayıtlı bilgilerine erişemiyorsan okul yönetimine başvurman gerekir.

### 025 · PASS · Ziyaretçi

- Soru: Şifrem yanlış diyor giremiyorum
- Beklenen intent: `account_access_problem`
- Gerçek intent: `account_access_problem`
- response_id: `access_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Giriş sayfası", "route": "/login"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hatalı kullanıcı adı/şifrede giriş formunun üstünde aynı kırmızı **401** hata kutusu çıkar; sistem hangi alanın yanlış olduğunu açıklamaz. Kayıt başarılı göründüğü hâlde yeni bilgilerle giriş olmuyorsa aynı kullanıcı adının daha önce alınmış olabileceğini ve kayıt kurallarını kontrol et. Rehberde self-servis bir 'şifremi unuttum' akışı tanımlı değil; kayıtlı bilgilerine erişemiyorsan okul yönetimine başvurman gerekir.

### 026 · PASS · Ziyaretçi

- Soru: Hesabıma erişemiyorum yardım eder misin?
- Beklenen intent: `account_access_problem`
- Gerçek intent: `account_access_problem`
- response_id: `access_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Giriş sayfası", "route": "/login"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hatalı kullanıcı adı/şifrede giriş formunun üstünde aynı kırmızı **401** hata kutusu çıkar; sistem hangi alanın yanlış olduğunu açıklamaz. Kayıt başarılı göründüğü hâlde yeni bilgilerle giriş olmuyorsa aynı kullanıcı adının daha önce alınmış olabileceğini ve kayıt kurallarını kontrol et. Rehberde self-servis bir 'şifremi unuttum' akışı tanımlı değil; kayıtlı bilgilerine erişemiyorsan okul yönetimine başvurman gerekir.

### 027 · PASS · Öğrenci

- Soru: İletişim bilgilerimi nasıl değiştiririm?
- Beklenen intent: `profile_edit`
- Gerçek intent: `profile_edit`
- response_id: `profile_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Profilini iki yerden güncelleyebilirsin: 1) Sağ üstteki hesap/avatar menüsü → **Ayarlar → Hesap** bölümünde **Ad, Soyad, E-posta, Telefon** ve **Doğum tarihi** alanlarını değiştir. 2) Tam profil ekranı için `/profile/me` adresine git, **Profili düzenle**'ye bas; burada bunlara ek olarak **Görünen ad** ve **Hakkında** alanları da vardır. Profil fotoğrafını da bu sayfadaki avatar üzerinden yükleyebilir, değiştirebilir veya kaldırabilirsin. Sonunda **Kaydet**'e bas. Tüm alanlar isteğe bağlıdır; **kullanıcı adı ve rol buradan değiştirilemez**. E-posta geçerli biçimde, telefon 7–15 hane olmalı; doğum tarihi gelecekte olamaz.

### 028 · PASS · Öğrenci

- Soru: Adımı soyadımı nereden güncellerim?
- Beklenen intent: `profile_edit`
- Gerçek intent: `profile_edit`
- response_id: `profile_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Profilini iki yerden güncelleyebilirsin: 1) Sağ üstteki hesap/avatar menüsü → **Ayarlar → Hesap** bölümünde **Ad, Soyad, E-posta, Telefon** ve **Doğum tarihi** alanlarını değiştir. 2) Tam profil ekranı için `/profile/me` adresine git, **Profili düzenle**'ye bas; burada bunlara ek olarak **Görünen ad** ve **Hakkında** alanları da vardır. Profil fotoğrafını da bu sayfadaki avatar üzerinden yükleyebilir, değiştirebilir veya kaldırabilirsin. Sonunda **Kaydet**'e bas. Tüm alanlar isteğe bağlıdır; **kullanıcı adı ve rol buradan değiştirilemez**. E-posta geçerli biçimde, telefon 7–15 hane olmalı; doğum tarihi gelecekte olamaz.

### 029 · PASS · Öğrenci

- Soru: Kayıtlı telefonumu değiştirmek istiyorum
- Beklenen intent: `profile_edit`
- Gerçek intent: `profile_edit`
- response_id: `profile_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Profilini iki yerden güncelleyebilirsin: 1) Sağ üstteki hesap/avatar menüsü → **Ayarlar → Hesap** bölümünde **Ad, Soyad, E-posta, Telefon** ve **Doğum tarihi** alanlarını değiştir. 2) Tam profil ekranı için `/profile/me` adresine git, **Profili düzenle**'ye bas; burada bunlara ek olarak **Görünen ad** ve **Hakkında** alanları da vardır. Profil fotoğrafını da bu sayfadaki avatar üzerinden yükleyebilir, değiştirebilir veya kaldırabilirsin. Sonunda **Kaydet**'e bas. Tüm alanlar isteğe bağlıdır; **kullanıcı adı ve rol buradan değiştirilemez**. E-posta geçerli biçimde, telefon 7–15 hane olmalı; doğum tarihi gelecekte olamaz.

### 030 · PASS · Ziyaretçi

- Soru: Uygulamayı koyu temaya nasıl alırım?
- Beklenen intent: `language_theme`
- Gerçek intent: `language_theme`
- response_id: `language_theme_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Giriş yaptıysan sağ üstteki hesap/avatar menüsünden **Dil** ile Türkçe/English, **Tema** ile Açık/Koyu arasında hızlıca geçebilirsin. Aynı menüde **Ayarlar → Görünüm** bölümünü açarsan tema ve dile ek olarak vurgu renk paletini de seçebilirsin. Ziyaretçide dil ve tema kontrolleri üst bardadır; görünüm seçimi tarayıcıda saklanır.

### 031 · PASS · Ziyaretçi

- Soru: İngilizce arayüze geçmek istiyorum
- Beklenen intent: `language_theme`
- Gerçek intent: `language_theme`
- response_id: `language_theme_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Giriş yaptıysan sağ üstteki hesap/avatar menüsünden **Dil** ile Türkçe/English, **Tema** ile Açık/Koyu arasında hızlıca geçebilirsin. Aynı menüde **Ayarlar → Görünüm** bölümünü açarsan tema ve dile ek olarak vurgu renk paletini de seçebilirsin. Ziyaretçide dil ve tema kontrolleri üst bardadır; görünüm seçimi tarayıcıda saklanır.

### 032 · PASS · Ziyaretçi

- Soru: Görünümü açık/koyu değiştirebilir miyim?
- Beklenen intent: `language_theme`
- Gerçek intent: `language_theme`
- response_id: `language_theme_instructions`
- confidence: `0.4814`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Giriş yaptıysan sağ üstteki hesap/avatar menüsünden **Dil** ile Türkçe/English, **Tema** ile Açık/Koyu arasında hızlıca geçebilirsin. Aynı menüde **Ayarlar → Görünüm** bölümünü açarsan tema ve dile ek olarak vurgu renk paletini de seçebilirsin. Ziyaretçide dil ve tema kontrolleri üst bardadır; görünüm seçimi tarayıcıda saklanır.

### 033 · PASS · Öğrenci

- Soru: Yönetici ne yapabilir öğretmen ne yapamaz?
- Beklenen intent: `roles_permissions`
- Gerçek intent: `roles_permissions`
- response_id: `roles_overview`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hezarfen'de roller şöyle sıralanır: **Veli < Öğrenci < Öğretmen < Yönetici < ADMIN**; ancak yetki modeli 'üst rol alttaki her şeyi yapar' şeklinde değildir. **Veli** bağlı çocuklarını salt-okunur izler; **Öğrenci** sınava girer, ödev teslim eder ve Pomodoro kullanır; **Öğretmen** yönettiği ders/sınav/yoklama işlemlerini yapar; **Yönetici** okul geneli ayar ve kayıtları yönetir; **ADMIN** kullanıcı/rol yönetir. Örneğin `/pomodoro` ve sınav odası yalnız Öğrenci; `/work` bağlantısı arayüzde yalnız Öğretmen/Yöneticiye gösterilir (backend Teacher+ kontrolü ADMIN isteğini de teknik olarak kabul eder). Yeni hesap Öğrenci başlar; rolü ADMIN atar. Kendi rolünü hesap menüsündeki rozetten görebilirsin.

### 034 · PASS · Öğrenci

- Soru: Rol kademeleri nedir?
- Beklenen intent: `roles_permissions`
- Gerçek intent: `roles_permissions`
- response_id: `roles_overview`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hezarfen'de roller şöyle sıralanır: **Veli < Öğrenci < Öğretmen < Yönetici < ADMIN**; ancak yetki modeli 'üst rol alttaki her şeyi yapar' şeklinde değildir. **Veli** bağlı çocuklarını salt-okunur izler; **Öğrenci** sınava girer, ödev teslim eder ve Pomodoro kullanır; **Öğretmen** yönettiği ders/sınav/yoklama işlemlerini yapar; **Yönetici** okul geneli ayar ve kayıtları yönetir; **ADMIN** kullanıcı/rol yönetir. Örneğin `/pomodoro` ve sınav odası yalnız Öğrenci; `/work` bağlantısı arayüzde yalnız Öğretmen/Yöneticiye gösterilir (backend Teacher+ kontrolü ADMIN isteğini de teknik olarak kabul eder). Yeni hesap Öğrenci başlar; rolü ADMIN atar. Kendi rolünü hesap menüsündeki rozetten görebilirsin.

### 035 · PASS · Öğrenci

- Soru: Yetki seviyeleri nasıl işliyor?
- Beklenen intent: `roles_permissions`
- Gerçek intent: `roles_permissions`
- response_id: `roles_overview`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hezarfen'de roller şöyle sıralanır: **Veli < Öğrenci < Öğretmen < Yönetici < ADMIN**; ancak yetki modeli 'üst rol alttaki her şeyi yapar' şeklinde değildir. **Veli** bağlı çocuklarını salt-okunur izler; **Öğrenci** sınava girer, ödev teslim eder ve Pomodoro kullanır; **Öğretmen** yönettiği ders/sınav/yoklama işlemlerini yapar; **Yönetici** okul geneli ayar ve kayıtları yönetir; **ADMIN** kullanıcı/rol yönetir. Örneğin `/pomodoro` ve sınav odası yalnız Öğrenci; `/work` bağlantısı arayüzde yalnız Öğretmen/Yöneticiye gösterilir (backend Teacher+ kontrolü ADMIN isteğini de teknik olarak kabul eder). Yeni hesap Öğrenci başlar; rolü ADMIN atar. Kendi rolünü hesap menüsündeki rozetten görebilirsin.

### 036 · PASS · Öğrenci

- Soru: Neden sürekli ana sayfaya atılıyorum?
- Beklenen intent: `access_denied_help`
- Gerçek intent: `access_denied_help`
- response_id: `access_denied_info`
- confidence: `0.6710`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Oturumun yoksa korumalı sayfa seni `/login`'e gönderir. Giriş yaptığın halde rolün sayfaya uymuyorsa kırmızı **"Bu içeriğe erişimin yok."** kutusu görünür. Bir işlem çağrısındaki **403** rolünün, ders yönetiminin, kaydının veya hedef öğrenci kapsamının yetersiz olduğunu gösterebilir; **404** bazen var olmayan kaydı, bazen de güvenlik için gizlenen yetkisiz kaydı ifade eder.

### 037 · PASS · Öğrenci

- Soru: Erişimin yok uyarısı alıyorum
- Beklenen intent: `access_denied_help`
- Gerçek intent: `access_denied_help`
- response_id: `access_denied_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Oturumun yoksa korumalı sayfa seni `/login`'e gönderir. Giriş yaptığın halde rolün sayfaya uymuyorsa kırmızı **"Bu içeriğe erişimin yok."** kutusu görünür. Bir işlem çağrısındaki **403** rolünün, ders yönetiminin, kaydının veya hedef öğrenci kapsamının yetersiz olduğunu gösterebilir; **404** bazen var olmayan kaydı, bazen de güvenlik için gizlenen yetkisiz kaydı ifade eder.

### 038 · PASS · Öğrenci

- Soru: Bir sayfayı açamıyorum yetki mi lazım?
- Beklenen intent: `access_denied_help`
- Gerçek intent: `access_denied_help`
- response_id: `access_denied_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Oturumun yoksa korumalı sayfa seni `/login`'e gönderir. Giriş yaptığın halde rolün sayfaya uymuyorsa kırmızı **"Bu içeriğe erişimin yok."** kutusu görünür. Bir işlem çağrısındaki **403** rolünün, ders yönetiminin, kaydının veya hedef öğrenci kapsamının yetersiz olduğunu gösterebilir; **404** bazen var olmayan kaydı, bazen de güvenlik için gizlenen yetkisiz kaydı ifade eder.

### 039 · PASS · Öğrenci

- Soru: Aradığım bölümü menüde bulamıyorum
- Beklenen intent: `navigation_help`
- Gerçek intent: `navigation_help`
- response_id: `navigation_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ana sayfa", "route": "/"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Masaüstünde sol dikey menüden gezinilir; gruplar rol bazlıdır ve yetkin olmayan öğeler gizlenir. Mobil alt çubuk da role göre değişir: Öğrencide **Bugün, Eğitim, Takvim, Karnem, Hesap**; Öğretmen/Yönetici/ADMIN'de **Bugün, Eğitim, Takvim, Hesap**; Velide **Bugün, Çocuklarım, Takvim, Hesap** görünür. Diğer sayfalara **Hesap/Menü** içinden ulaşırsın. Aradığın sayfayı söylersen gerçek yolunu verebilirim.

### 040 · PASS · Öğrenci

- Soru: Sayfalar arasında nasıl geçiş yaparım?
- Beklenen intent: `navigation_help`
- Gerçek intent: `navigation_help`
- response_id: `navigation_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ana sayfa", "route": "/"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Masaüstünde sol dikey menüden gezinilir; gruplar rol bazlıdır ve yetkin olmayan öğeler gizlenir. Mobil alt çubuk da role göre değişir: Öğrencide **Bugün, Eğitim, Takvim, Karnem, Hesap**; Öğretmen/Yönetici/ADMIN'de **Bugün, Eğitim, Takvim, Hesap**; Velide **Bugün, Çocuklarım, Takvim, Hesap** görünür. Diğer sayfalara **Hesap/Menü** içinden ulaşırsın. Aradığın sayfayı söylersen gerçek yolunu verebilirim.

### 041 · PASS · Öğrenci

- Soru: Mobilde menü nerede duruyor?
- Beklenen intent: `navigation_help`
- Gerçek intent: `navigation_help`
- response_id: `navigation_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ana sayfa", "route": "/"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Masaüstünde sol dikey menüden gezinilir; gruplar rol bazlıdır ve yetkin olmayan öğeler gizlenir. Mobil alt çubuk da role göre değişir: Öğrencide **Bugün, Eğitim, Takvim, Karnem, Hesap**; Öğretmen/Yönetici/ADMIN'de **Bugün, Eğitim, Takvim, Hesap**; Velide **Bugün, Çocuklarım, Takvim, Hesap** görünür. Diğer sayfalara **Hesap/Menü** içinden ulaşırsın. Aradığın sayfayı söylersen gerçek yolunu verebilirim.

### 042 · PASS · Öğrenci

- Soru: Hangi derslere kayıtlıyım nereden bakarım?
- Beklenen intent: `course_view`
- Gerçek intent: `course_view`
- response_id: `course_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Eğitim** sayfası (`/courses`): dersler, **etütler** ve **kulüpler** tek yerde (üstteki **Tümü / Dersler / Etüt / Kulüp** sekmeleriyle süz). Arama ve döneme göre filtreleme yapabilirsin; öğrenci yalnızca kayıtlı olduklarını görür ('Kayıtlı' rozeti). Bir öğeyi açmak için **Görüntüle (View)**'ye bas; detay `/courses/$id`'de sınavları, oturumları ve (yetkiliysen) katılımcı listesini gösterir. Öğretmen+ sağ üstten **Yeni** oluşturabilir.

### 043 · PASS · Öğrenci

- Soru: Ders detay sayfasına nasıl giderim?
- Beklenen intent: `course_view`
- Gerçek intent: `course_view`
- response_id: `course_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Eğitim** sayfası (`/courses`): dersler, **etütler** ve **kulüpler** tek yerde (üstteki **Tümü / Dersler / Etüt / Kulüp** sekmeleriyle süz). Arama ve döneme göre filtreleme yapabilirsin; öğrenci yalnızca kayıtlı olduklarını görür ('Kayıtlı' rozeti). Bir öğeyi açmak için **Görüntüle (View)**'ye bas; detay `/courses/$id`'de sınavları, oturumları ve (yetkiliysen) katılımcı listesini gösterir. Öğretmen+ sağ üstten **Yeni** oluşturabilir.

### 044 · PASS · Öğrenci

- Soru: Dersleri döneme göre süzebilir miyim?
- Beklenen intent: `course_view`
- Gerçek intent: `course_view`
- response_id: `course_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Eğitim** sayfası (`/courses`): dersler, **etütler** ve **kulüpler** tek yerde (üstteki **Tümü / Dersler / Etüt / Kulüp** sekmeleriyle süz). Arama ve döneme göre filtreleme yapabilirsin; öğrenci yalnızca kayıtlı olduklarını görür ('Kayıtlı' rozeti). Bir öğeyi açmak için **Görüntüle (View)**'ye bas; detay `/courses/$id`'de sınavları, oturumları ve (yetkiliysen) katılımcı listesini gösterir. Öğretmen+ sağ üstten **Yeni** oluşturabilir.

### 045 · PASS · Öğretmen

- Soru: Öğretmen olarak yeni bir ders açmak istiyorum
- Beklenen intent: `course_create`
- Gerçek intent: `course_create`
- response_id: `course_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/courses`'a git, **Yeni ders (New course)**'e bas. 2) Sağdan açılan panelde **Başlık** (zorunlu), isteğe bağlı **Açıklama** ve **Dönem** (varsayılan 'Atanmamış') gir. 3) **Oluştur**. Öğrencide 'Yeni ders' düğmesi görünmez.

### 046 · PASS · Öğretmen

- Soru: Ders ekleme düğmesi nerede?
- Beklenen intent: `course_create`
- Gerçek intent: `course_create`
- response_id: `course_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/courses`'a git, **Yeni ders (New course)**'e bas. 2) Sağdan açılan panelde **Başlık** (zorunlu), isteğe bağlı **Açıklama** ve **Dönem** (varsayılan 'Atanmamış') gir. 3) **Oluştur**. Öğrencide 'Yeni ders' düğmesi görünmez.

### 047 · PASS · Öğretmen

- Soru: Bir sınıf oluşturmak istiyorum nasıl yaparım?
- Beklenen intent: `class_section_manage`
- Gerçek intent: `class_section_manage`
- response_id: `class_section_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 048 · PASS · Öğretmen

- Soru: Bir öğrenciyi dersime nasıl eklerim?
- Beklenen intent: `course_enroll_student`
- Gerçek intent: `course_enroll_student`
- response_id: `enroll_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: bu dersi yönetme yetkin olmalı. 1) Ders detayına (`/courses/$id`) gir, **Sınıf listesi (Roster)** bölümünü aç. 2) **Öğrenci kaydet (Enroll student)**'e bas, panelde öğrenciyi ara-seç. 3) Onayla. Zaten kayıtlılar listede çıkmaz; öğrenci seçmezsen 'Önce bir öğrenci seçmelisin.' uyarısı çıkar. Yalnız **Öğrenci** rolündeki hesaplar derse kaydedilebilir; sınıf doluysa işlem 409 ile reddedilir. Sınıf listesi yalnızca dersi yönetebilen hesaba görünür.

### 049 · PASS · Öğretmen

- Soru: Sınıf listeme öğrenci almak istiyorum
- Beklenen intent: `course_enroll_student`
- Gerçek intent: `course_enroll_student`
- response_id: `enroll_student_instructions`
- confidence: `0.6473`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: bu dersi yönetme yetkin olmalı. 1) Ders detayına (`/courses/$id`) gir, **Sınıf listesi (Roster)** bölümünü aç. 2) **Öğrenci kaydet (Enroll student)**'e bas, panelde öğrenciyi ara-seç. 3) Onayla. Zaten kayıtlılar listede çıkmaz; öğrenci seçmezsen 'Önce bir öğrenci seçmelisin.' uyarısı çıkar. Yalnız **Öğrenci** rolündeki hesaplar derse kaydedilebilir; sınıf doluysa işlem 409 ile reddedilir. Sınıf listesi yalnızca dersi yönetebilen hesaba görünür.

### 050 · PASS · Öğretmen

- Soru: Derse kayıt yapma işlemi nasıl?
- Beklenen intent: `course_enroll_student`
- Gerçek intent: `course_enroll_student`
- response_id: `enroll_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: bu dersi yönetme yetkin olmalı. 1) Ders detayına (`/courses/$id`) gir, **Sınıf listesi (Roster)** bölümünü aç. 2) **Öğrenci kaydet (Enroll student)**'e bas, panelde öğrenciyi ara-seç. 3) Onayla. Zaten kayıtlılar listede çıkmaz; öğrenci seçmezsen 'Önce bir öğrenci seçmelisin.' uyarısı çıkar. Yalnız **Öğrenci** rolündeki hesaplar derse kaydedilebilir; sınıf doluysa işlem 409 ile reddedilir. Sınıf listesi yalnızca dersi yönetebilen hesaba görünür.

### 051 · PASS · Öğretmen

- Soru: Yanlışlıkla eklediğim öğrenciyi dersten çıkarayım
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 052 · PASS · Öğretmen

- Soru: Sınıf listesinden birini silmek istiyorum
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 053 · PASS · Öğretmen

- Soru: Öğrenci kaydını iptal etmek istiyorum
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `0.8211`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 054 · PASS · Öğretmen

- Soru: Derse yeni bir ders saati eklemek istiyorum
- Beklenen intent: `lesson_session_add`
- Gerçek intent: `lesson_session_add`
- response_id: `lesson_session_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ders yönetim yetkisi. 1) Ders detayı → **Ders oturumları (Lesson sessions)** → **Oturum ekle (Add session)**. 2) İsteğe bağlı **Konu**, **Başlangıç** tarih (GG/AA/YYYY) + saat, isteğe bağlı **Bitiş**. 3) **Oturum ekle**. Başlangıç zorunlu ve gelecekte olmalı; bitiş başlangıçtan önce olamaz. 'Derse yeni oturum ekleyemiyorum' gibi bir durumda önce ders yönetim yetkini ve tarih sırasını kontrol et.

### 055 · PASS · Öğretmen

- Soru: Oturum oluşturmak nasıl yapılır?
- Beklenen intent: `lesson_session_add`
- Gerçek intent: `lesson_session_add`
- response_id: `lesson_session_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ders yönetim yetkisi. 1) Ders detayı → **Ders oturumları (Lesson sessions)** → **Oturum ekle (Add session)**. 2) İsteğe bağlı **Konu**, **Başlangıç** tarih (GG/AA/YYYY) + saat, isteğe bağlı **Bitiş**. 3) **Oturum ekle**. Başlangıç zorunlu ve gelecekte olmalı; bitiş başlangıçtan önce olamaz. 'Derse yeni oturum ekleyemiyorum' gibi bir durumda önce ders yönetim yetkini ve tarih sırasını kontrol et.

### 056 · PASS · Öğretmen

- Soru: Ders için bir saat planlamak istiyorum
- Beklenen intent: `lesson_session_add`
- Gerçek intent: `lesson_session_add`
- response_id: `lesson_session_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ders yönetim yetkisi. 1) Ders detayı → **Ders oturumları (Lesson sessions)** → **Oturum ekle (Add session)**. 2) İsteğe bağlı **Konu**, **Başlangıç** tarih (GG/AA/YYYY) + saat, isteğe bağlı **Bitiş**. 3) **Oturum ekle**. Başlangıç zorunlu ve gelecekte olmalı; bitiş başlangıçtan önce olamaz. 'Derse yeni oturum ekleyemiyorum' gibi bir durumda önce ders yönetim yetkini ve tarih sırasını kontrol et.

### 057 · PASS · Öğretmen

- Soru: Ders saatinde öğrencileri nasıl var yok yaparım?
- Beklenen intent: `roll_call`
- Gerçek intent: `roll_call`
- response_id: `roll_call_instructions`
- confidence: `0.4512`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: derste kayıtlı öğrenci ve en az bir oturum olmalı; yönetim yetkisi. 1) Ders detayı → **Ders oturumları** → oturum kartında **Yoklama (Roll call)**. 2) Her öğrenci için **Var / Yok / Geç / Mazeretli** seç. 3) Satırda **Kaydet** (daha önce kaydedildiyse **Güncelle**). Öğrenci ders oturumu yoklamasında kendini işaretleyemez.

### 058 · PASS · Öğretmen

- Soru: Oturumda yoklama almak istiyorum
- Beklenen intent: `roll_call`
- Gerçek intent: `roll_call`
- response_id: `roll_call_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: derste kayıtlı öğrenci ve en az bir oturum olmalı; yönetim yetkisi. 1) Ders detayı → **Ders oturumları** → oturum kartında **Yoklama (Roll call)**. 2) Her öğrenci için **Var / Yok / Geç / Mazeretli** seç. 3) Satırda **Kaydet** (daha önce kaydedildiyse **Güncelle**). Öğrenci ders oturumu yoklamasında kendini işaretleyemez.

### 059 · PASS · Öğretmen

- Soru: Devam kontrolü nasıl kaydedilir?
- Beklenen intent: `roll_call`
- Gerçek intent: `roll_call`
- response_id: `roll_call_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: derste kayıtlı öğrenci ve en az bir oturum olmalı; yönetim yetkisi. 1) Ders detayı → **Ders oturumları** → oturum kartında **Yoklama (Roll call)**. 2) Her öğrenci için **Var / Yok / Geç / Mazeretli** seç. 3) Satırda **Kaydet** (daha önce kaydedildiyse **Güncelle**). Öğrenci ders oturumu yoklamasında kendini işaretleyemez.

### 060 · PASS · Öğrenci

- Soru: Asenkron sınav ne anlama geliyor?
- Beklenen intent: `exam_modes_info`
- Gerçek intent: `exam_modes_info`
- response_id: `exam_modes_explained`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Dört sınav modu vardır: **Zamansız** (çevrimdışı notlanır, girilemez), **Senkron** (herkes tek sabit aralıkta girer), **Asenkron** (aralık içinde istediğin an başlar, kişisel süre alırsın), **Açık** (her zaman girilebilir, hep 'Aktif' sayılır). Süre 1 dakika–24 saat arasıdır.

### 061 · PASS · Öğrenci

- Soru: Sınav modları arasında ne fark var?
- Beklenen intent: `exam_modes_info`
- Gerçek intent: `exam_modes_info`
- response_id: `exam_modes_explained`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Dört sınav modu vardır: **Zamansız** (çevrimdışı notlanır, girilemez), **Senkron** (herkes tek sabit aralıkta girer), **Asenkron** (aralık içinde istediğin an başlar, kişisel süre alırsın), **Açık** (her zaman girilebilir, hep 'Aktif' sayılır). Süre 1 dakika–24 saat arasıdır.

### 062 · PASS · Öğrenci

- Soru: Açık mod sürekli mi açık kalıyor?
- Beklenen intent: `exam_modes_info`
- Gerçek intent: `exam_modes_info`
- response_id: `exam_modes_explained`
- confidence: `0.4620`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Dört sınav modu vardır: **Zamansız** (çevrimdışı notlanır, girilemez), **Senkron** (herkes tek sabit aralıkta girer), **Asenkron** (aralık içinde istediğin an başlar, kişisel süre alırsın), **Açık** (her zaman girilebilir, hep 'Aktif' sayılır). Süre 1 dakika–24 saat arasıdır.

### 063 · PASS · Öğretmen

- Soru: Dersime sınav eklemek istiyorum
- Beklenen intent: `exam_create`
- Gerçek intent: `exam_create`
- response_id: `exam_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: yönetebileceğin en az bir ders olmalı. 1) `/exams` → **Sınav oluştur (Create exam)**. 2) **Ders seç**, **Başlık** ve isteğe bağlı açıklama gir. 3) **Tür** (Ödev/Kısa sınav/Vize/Final/Proje/Sözlü) ve **Mod** (Senkron/Asenkron/Açık) seç. 4) Gerekirse **Deneme hakkı** ve **Yeniden girişe izin ver**'i ayarla. 5) Senkron/Asenkron ise Başlangıç/Bitiş gir. Asenkron modda süre zorunludur; Senkron mod süre kabul etmez. Süre 1 dakika–24 saat arasında ve sınav penceresine sığmalıdır; Açık mod başlangıç/bitiş taşımaz. 6) **Oluştur**. Sınavlar ders içinden eklenir.

### 064 · PASS · Öğretmen

- Soru: Yeni bir yazılı oluşturacağım
- Beklenen intent: `exam_create`
- Gerçek intent: `exam_create`
- response_id: `exam_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: yönetebileceğin en az bir ders olmalı. 1) `/exams` → **Sınav oluştur (Create exam)**. 2) **Ders seç**, **Başlık** ve isteğe bağlı açıklama gir. 3) **Tür** (Ödev/Kısa sınav/Vize/Final/Proje/Sözlü) ve **Mod** (Senkron/Asenkron/Açık) seç. 4) Gerekirse **Deneme hakkı** ve **Yeniden girişe izin ver**'i ayarla. 5) Senkron/Asenkron ise Başlangıç/Bitiş gir. Asenkron modda süre zorunludur; Senkron mod süre kabul etmez. Süre 1 dakika–24 saat arasında ve sınav penceresine sığmalıdır; Açık mod başlangıç/bitiş taşımaz. 6) **Oluştur**. Sınavlar ders içinden eklenir.

### 065 · PASS · Öğretmen

- Soru: Sınav hazırlama adımları neler?
- Beklenen intent: `exam_create`
- Gerçek intent: `exam_create`
- response_id: `exam_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: yönetebileceğin en az bir ders olmalı. 1) `/exams` → **Sınav oluştur (Create exam)**. 2) **Ders seç**, **Başlık** ve isteğe bağlı açıklama gir. 3) **Tür** (Ödev/Kısa sınav/Vize/Final/Proje/Sözlü) ve **Mod** (Senkron/Asenkron/Açık) seç. 4) Gerekirse **Deneme hakkı** ve **Yeniden girişe izin ver**'i ayarla. 5) Senkron/Asenkron ise Başlangıç/Bitiş gir. Asenkron modda süre zorunludur; Senkron mod süre kabul etmez. Süre 1 dakika–24 saat arasında ve sınav penceresine sığmalıdır; Açık mod başlangıç/bitiş taşımaz. 6) **Oluştur**. Sınavlar ders içinden eklenir.

### 066 · PASS · Öğretmen

- Soru: Sınavıma çoktan seçmeli soru koymak istiyorum
- Beklenen intent: `exam_add_question`
- Gerçek intent: `exam_add_question`
- response_id: `exam_add_question_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: yönetim yetkisi ve sınavda henüz başlamış bir öğrenci denemesi olmaması. Ayrıca ders detayında en az bir **Konu (Subject)** tanımlı olmalı — her sınav sorusu bir konuya bağlanır. 1) Sınav detayı → **Sorular (Questions)** → **Soru ekle**. 2) **Soru metni** + **Puan** (1–100) + **Konu** seç. 3) **Soru türü**: Seçmeli (2–10 şık, doğru şıkkı işaretle) veya Metin. 4) **Oluştur**. Metin sorular otomatik puanlanmaz, elle notlanır. Herhangi bir öğrenci sınav denemesine başladıktan sonra soru ekleme/değiştirme 409 ile engellenir.

### 067 · PASS · Öğretmen

- Soru: Soru ekleme nasıl yapılır?
- Beklenen intent: `exam_add_question`
- Gerçek intent: `exam_add_question`
- response_id: `exam_add_question_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: yönetim yetkisi ve sınavda henüz başlamış bir öğrenci denemesi olmaması. Ayrıca ders detayında en az bir **Konu (Subject)** tanımlı olmalı — her sınav sorusu bir konuya bağlanır. 1) Sınav detayı → **Sorular (Questions)** → **Soru ekle**. 2) **Soru metni** + **Puan** (1–100) + **Konu** seç. 3) **Soru türü**: Seçmeli (2–10 şık, doğru şıkkı işaretle) veya Metin. 4) **Oluştur**. Metin sorular otomatik puanlanmaz, elle notlanır. Herhangi bir öğrenci sınav denemesine başladıktan sonra soru ekleme/değiştirme 409 ile engellenir.

### 068 · PASS · Öğretmen

- Soru: Sınava açık uçlu soru nasıl eklerim?
- Beklenen intent: `exam_add_question`
- Gerçek intent: `exam_add_question`
- response_id: `exam_add_question_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: yönetim yetkisi ve sınavda henüz başlamış bir öğrenci denemesi olmaması. Ayrıca ders detayında en az bir **Konu (Subject)** tanımlı olmalı — her sınav sorusu bir konuya bağlanır. 1) Sınav detayı → **Sorular (Questions)** → **Soru ekle**. 2) **Soru metni** + **Puan** (1–100) + **Konu** seç. 3) **Soru türü**: Seçmeli (2–10 şık, doğru şıkkı işaretle) veya Metin. 4) **Oluştur**. Metin sorular otomatik puanlanmaz, elle notlanır. Herhangi bir öğrenci sınav denemesine başladıktan sonra soru ekleme/değiştirme 409 ile engellenir.

### 069 · PASS · Öğrenci

- Soru: Öğrenci olarak sınava nasıl başlarım?
- Beklenen intent: `exam_enter_room`
- Gerçek intent: `exam_enter_room`
- response_id: `exam_enter_room_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: sınavın dersine kayıtlı olmak; sınav girilebilir modda (Senkron/Asenkron/Açık) ve **Aktif** olmalı. 1) Sınav detayında (`/exams/$id`) **Sınav odasını aç (Open exam room)**'a bas. 2) **Sınava başla (Start exam)**. Sorular ve **Kalan süre** görünür. Giremiyorsan en sık nedenler: sınav henüz başlamadı veya bitti, **Zamansız** modda, derse kayıtlı değilsin, önceki deneme zaten teslim edildi, süre doldu ya da deneme hakkın kalmadı.

### 070 · PASS · Öğrenci

- Soru: Online sınav odasına nasıl girerim?
- Beklenen intent: `exam_enter_room`
- Gerçek intent: `exam_enter_room`
- response_id: `exam_enter_room_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: sınavın dersine kayıtlı olmak; sınav girilebilir modda (Senkron/Asenkron/Açık) ve **Aktif** olmalı. 1) Sınav detayında (`/exams/$id`) **Sınav odasını aç (Open exam room)**'a bas. 2) **Sınava başla (Start exam)**. Sorular ve **Kalan süre** görünür. Giremiyorsan en sık nedenler: sınav henüz başlamadı veya bitti, **Zamansız** modda, derse kayıtlı değilsin, önceki deneme zaten teslim edildi, süre doldu ya da deneme hakkın kalmadı.

### 071 · PASS · Öğrenci

- Soru: Sınavımı nereden başlatabilirim?
- Beklenen intent: `exam_enter_room`
- Gerçek intent: `exam_enter_room`
- response_id: `exam_enter_room_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: sınavın dersine kayıtlı olmak; sınav girilebilir modda (Senkron/Asenkron/Açık) ve **Aktif** olmalı. 1) Sınav detayında (`/exams/$id`) **Sınav odasını aç (Open exam room)**'a bas. 2) **Sınava başla (Start exam)**. Sorular ve **Kalan süre** görünür. Giremiyorsan en sık nedenler: sınav henüz başlamadı veya bitti, **Zamansız** modda, derse kayıtlı değilsin, önceki deneme zaten teslim edildi, süre doldu ya da deneme hakkın kalmadı.

### 072 · PASS · Öğrenci

- Soru: Verdiğim cevabı nasıl kaydederim?
- Beklenen intent: `exam_save_answer`
- Gerçek intent: `exam_save_answer`
- response_id: `exam_save_answer_instructions`
- confidence: `0.7009`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: durum 'Devam ediyor', süre bitmemiş. 1) Şık seç veya metin kutusuna yaz. 2) **Cevabı kaydet (Save answer)**. 3) **Kaydedildi** rozeti çıkar ve ekran otomatik sonraki soruya kayar. Her cevap tek tek kaydedilir; toplu gönderim yoktur. Süre bitince cevaplar salt okunur olur.

### 073 · PASS · Öğrenci

- Soru: Cevaplar tek tek mi kaydediliyor?
- Beklenen intent: `exam_save_answer`
- Gerçek intent: `exam_save_answer`
- response_id: `exam_save_answer_instructions`
- confidence: `0.5904`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: durum 'Devam ediyor', süre bitmemiş. 1) Şık seç veya metin kutusuna yaz. 2) **Cevabı kaydet (Save answer)**. 3) **Kaydedildi** rozeti çıkar ve ekran otomatik sonraki soruya kayar. Her cevap tek tek kaydedilir; toplu gönderim yoktur. Süre bitince cevaplar salt okunur olur.

### 074 · PASS · Öğrenci

- Soru: Bir soruyu işaretledim sonra ne yapmalıyım?
- Beklenen intent: `exam_save_answer`
- Gerçek intent: `exam_save_answer`
- response_id: `exam_save_answer_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: durum 'Devam ediyor', süre bitmemiş. 1) Şık seç veya metin kutusuna yaz. 2) **Cevabı kaydet (Save answer)**. 3) **Kaydedildi** rozeti çıkar ve ekran otomatik sonraki soruya kayar. Her cevap tek tek kaydedilir; toplu gönderim yoktur. Süre bitince cevaplar salt okunur olur.

### 075 · PASS · Öğrenci

- Soru: Sınavı tamamlayıp teslim etmek istiyorum
- Beklenen intent: `exam_finish_result`
- Gerçek intent: `exam_finish_result`
- response_id: `exam_finish_instructions`
- confidence: `0.8673`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Yan panelde **Sınavı bitir (Finish exam)**'e bas ve onayla; durum **Teslim edildi** olur. 2) Sonucu: girilebilir sınavda sınav odasındaki **Not** alanından, Zamansız sınavda detaydaki **Sonucun (Your result)** bölümünden görürsün. Notlanmadıysa 'Henüz notlanmadı' yazar. Süre kendiliğinden biterse durum 'Süresi doldu' olur.

### 076 · PASS · Öğrenci

- Soru: Notumu sınavdan sonra nereden görürüm?
- Beklenen intent: `exam_finish_result`
- Gerçek intent: `exam_finish_result`
- response_id: `exam_finish_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Yan panelde **Sınavı bitir (Finish exam)**'e bas ve onayla; durum **Teslim edildi** olur. 2) Sonucu: girilebilir sınavda sınav odasındaki **Not** alanından, Zamansız sınavda detaydaki **Sonucun (Your result)** bölümünden görürsün. Notlanmadıysa 'Henüz notlanmadı' yazar. Süre kendiliğinden biterse durum 'Süresi doldu' olur.

### 077 · PASS · Öğrenci

- Soru: Sınavı bitirince ne oluyor?
- Beklenen intent: `exam_finish_result`
- Gerçek intent: `exam_finish_result`
- response_id: `exam_finish_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Yan panelde **Sınavı bitir (Finish exam)**'e bas ve onayla; durum **Teslim edildi** olur. 2) Sonucu: girilebilir sınavda sınav odasındaki **Not** alanından, Zamansız sınavda detaydaki **Sonucun (Your result)** bölümünden görürsün. Notlanmadıysa 'Henüz notlanmadı' yazar. Süre kendiliğinden biterse durum 'Süresi doldu' olur.

### 078 · PASS · Öğrenci

- Soru: Yanlışlıkla sınavdan çıktım geri girebilir miyim?
- Beklenen intent: `exam_rejoin_retake`
- Gerçek intent: `exam_rejoin_retake`
- response_id: `exam_rejoin_retake_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Rejoin (aynı denemeye dönüş):** 'Yeniden girişe izin ver' açıksa odadan çıktıktan sonra tekrar **Sınav odasını aç** → **Sınava devam et**; kalan süre ve cevapların korunur. **Retake (yeni deneme):** 'Deneme hakkı' açık ve azami sayı belirlenmişse her yeni giriş bir deneme kullanır. **Süre çıkışta bile durmaz.** 'Yeniden giriş kapalı', 'deneme hakkı kalmadı', 'süre doldu' veya 'deneme zaten teslim edildi' durumunda aynı denemeye dönemezsin.

### 079 · PASS · Öğrenci

- Soru: Sınava ikinci kez girme hakkım var mı?
- Beklenen intent: `exam_rejoin_retake`
- Gerçek intent: `exam_rejoin_retake`
- response_id: `exam_rejoin_retake_info`
- confidence: `0.6445`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Rejoin (aynı denemeye dönüş):** 'Yeniden girişe izin ver' açıksa odadan çıktıktan sonra tekrar **Sınav odasını aç** → **Sınava devam et**; kalan süre ve cevapların korunur. **Retake (yeni deneme):** 'Deneme hakkı' açık ve azami sayı belirlenmişse her yeni giriş bir deneme kullanır. **Süre çıkışta bile durmaz.** 'Yeniden giriş kapalı', 'deneme hakkı kalmadı', 'süre doldu' veya 'deneme zaten teslim edildi' durumunda aynı denemeye dönemezsin.

### 080 · PASS · Öğrenci

- Soru: Kaldığım sorudan devam edebilir miyim?
- Beklenen intent: `exam_rejoin_retake`
- Gerçek intent: `exam_rejoin_retake`
- response_id: `exam_rejoin_retake_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Rejoin (aynı denemeye dönüş):** 'Yeniden girişe izin ver' açıksa odadan çıktıktan sonra tekrar **Sınav odasını aç** → **Sınava devam et**; kalan süre ve cevapların korunur. **Retake (yeni deneme):** 'Deneme hakkı' açık ve azami sayı belirlenmişse her yeni giriş bir deneme kullanır. **Süre çıkışta bile durmaz.** 'Yeniden giriş kapalı', 'deneme hakkı kalmadı', 'süre doldu' veya 'deneme zaten teslim edildi' durumunda aynı denemeye dönemezsin.

### 081 · PASS · Öğretmen

- Soru: Öğretmen olarak sınavı nasıl puanlarım?
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 082 · PASS · Öğretmen

- Soru: Öğrenci notlarını girmek istiyorum
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 083 · PASS · Öğretmen

- Soru: Notlandırma neden şu an kapalı?
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 084 · PASS · Öğretmen

- Soru: Sınav sırasında öğrencileri anlık takip edebilir miyim?
- Beklenen intent: `exam_live_monitor`
- Gerçek intent: `exam_live_monitor`
- response_id: `exam_live_monitor_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: sınavın dersinde yönetim yetkisi. Backend canlı görüntü için ayrıca 'başlamış olmalı' veya belirli bir mod şartı aramaz. Sınav detayı → **Canlı İzleme (Live Monitor)** (`/exams/$id/live`). Üstteki sayaçlar (Başlamadı/Devam ediyor/Teslim edildi/Süresi doldu/Katılmadı) ve **Canlı Liste**'de ilerleme, kalan süre, durum görünür. Sınav bitince ekran 'Son Durum'a döner. Öğrenciler bu ekranı göremez.

### 085 · PASS · Öğretmen

- Soru: Kimin başladığını canlı görmek istiyorum
- Beklenen intent: `exam_live_monitor`
- Gerçek intent: `exam_live_monitor`
- response_id: `exam_live_monitor_info`
- confidence: `0.5891`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: sınavın dersinde yönetim yetkisi. Backend canlı görüntü için ayrıca 'başlamış olmalı' veya belirli bir mod şartı aramaz. Sınav detayı → **Canlı İzleme (Live Monitor)** (`/exams/$id/live`). Üstteki sayaçlar (Başlamadı/Devam ediyor/Teslim edildi/Süresi doldu/Katılmadı) ve **Canlı Liste**'de ilerleme, kalan süre, durum görünür. Sınav bitince ekran 'Son Durum'a döner. Öğrenciler bu ekranı göremez.

### 086 · PASS · Öğretmen

- Soru: Canlı izleme ekranı nerede?
- Beklenen intent: `exam_live_monitor`
- Gerçek intent: `exam_live_monitor`
- response_id: `exam_live_monitor_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: sınavın dersinde yönetim yetkisi. Backend canlı görüntü için ayrıca 'başlamış olmalı' veya belirli bir mod şartı aramaz. Sınav detayı → **Canlı İzleme (Live Monitor)** (`/exams/$id/live`). Üstteki sayaçlar (Başlamadı/Devam ediyor/Teslim edildi/Süresi doldu/Katılmadı) ve **Canlı Liste**'de ilerleme, kalan süre, durum görünür. Sınav bitince ekran 'Son Durum'a döner. Öğrenciler bu ekranı göremez.

### 087 · PASS · Öğrenci

- Soru: Karnemi ve harf notlarımı görmek istiyorum
- Beklenen intent: `report_card_view`
- Gerçek intent: `report_card_view`
- response_id: `report_card_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Karnem", "route": "/marks"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Karneni görmek için menüden **Karnem (Report card)** veya `/marks`'a git. Üstte **Genel ortalama** (sayı + harf notu, /100), altında her ders için **Ders ortalaması** ve sınav bazında **Ağırlık** ve **Not** görünür. Karnem yalnızca Öğrenci rolüne açıktır; notu henüz girilmemiş sınav rapor listesine eklenmez.

### 088 · PASS · Öğrenci

- Soru: Bütün ders notlarım nerede listeleniyor?
- Beklenen intent: `report_card_view`
- Gerçek intent: `report_card_view`
- response_id: `report_card_info`
- confidence: `0.5655`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Karnem", "route": "/marks"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Karneni görmek için menüden **Karnem (Report card)** veya `/marks`'a git. Üstte **Genel ortalama** (sayı + harf notu, /100), altında her ders için **Ders ortalaması** ve sınav bazında **Ağırlık** ve **Not** görünür. Karnem yalnızca Öğrenci rolüne açıktır; notu henüz girilmemiş sınav rapor listesine eklenmez.

### 089 · PASS · Öğrenci

- Soru: Genel ortalamama nereden bakarım?
- Beklenen intent: `report_card_view`
- Gerçek intent: `report_card_view`
- response_id: `report_card_info`
- confidence: `0.6125`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Karnem", "route": "/marks"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Karneni görmek için menüden **Karnem (Report card)** veya `/marks`'a git. Üstte **Genel ortalama** (sayı + harf notu, /100), altında her ders için **Ders ortalaması** ve sınav bazında **Ağırlık** ve **Not** görünür. Karnem yalnızca Öğrenci rolüne açıktır; notu henüz girilmemiş sınav rapor listesine eklenmez.

### 090 · PASS · Öğrenci

- Soru: Ders ortalamam nasıl hesaplanıyor?
- Beklenen intent: `weighted_average_info`
- Gerçek intent: `weighted_average_info`
- response_id: `weighted_average_explained`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Karnem", "route": "/marks"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ders ortalaması, notlanmış sınavların **tür ağırlığıyla** ortalamasıdır: Σ(not×ağırlık)/Σ(ağırlık). Notlanmamış sınavlar atlanır (sıfır sayılmaz). Genel ortalama, dolu ders ortalamalarının düz aritmetik ortalamasıdır. Notlar 0–100 tam sayıdır; harf notu okul ayarındaki not bantlarından gelir.

### 091 · PASS · Öğrenci

- Soru: Sınav ağırlıkları nota nasıl yansıyor?
- Beklenen intent: `weighted_average_info`
- Gerçek intent: `weighted_average_info`
- response_id: `weighted_average_explained`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Karnem", "route": "/marks"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ders ortalaması, notlanmış sınavların **tür ağırlığıyla** ortalamasıdır: Σ(not×ağırlık)/Σ(ağırlık). Notlanmamış sınavlar atlanır (sıfır sayılmaz). Genel ortalama, dolu ders ortalamalarının düz aritmetik ortalamasıdır. Notlar 0–100 tam sayıdır; harf notu okul ayarındaki not bantlarından gelir.

### 092 · PASS · Öğrenci

- Soru: Ortalamaya girmeyen notlar oluyor mu?
- Beklenen intent: `weighted_average_info`
- Gerçek intent: `weighted_average_info`
- response_id: `weighted_average_explained`
- confidence: `0.7373`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Karnem", "route": "/marks"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ders ortalaması, notlanmış sınavların **tür ağırlığıyla** ortalamasıdır: Σ(not×ağırlık)/Σ(ağırlık). Notlanmamış sınavlar atlanır (sıfır sayılmaz). Genel ortalama, dolu ders ortalamalarının düz aritmetik ortalamasıdır. Notlar 0–100 tam sayıdır; harf notu okul ayarındaki not bantlarından gelir.

### 093 · PASS · Öğretmen

- Soru: Öğretmen olarak bir öğrencinin karnesini görmek istiyorum
- Beklenen intent: `student_marks_lookup`
- Gerçek intent: `student_marks_lookup`
- response_id: `student_marks_lookup_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Öğrenci notları", "route": "/management/student-marks"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/management/student-marks` (Öğrenci notları) sayfasını aç. 2) Aramaya **en az 2 karakter** yaz. 3) Öğrenci satırında **Görüntüle**'ye bas; sağdan açılan panelde öğrencinin karnesini görürsün. Bu sayfa Öğretmen ve üstüne açıktır.

### 094 · PASS · Öğretmen

- Soru: Öğrenci notu sorgulama sayfası nerede?
- Beklenen intent: `student_marks_lookup`
- Gerçek intent: `student_marks_lookup`
- response_id: `student_marks_lookup_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Öğrenci notları", "route": "/management/student-marks"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/management/student-marks` (Öğrenci notları) sayfasını aç. 2) Aramaya **en az 2 karakter** yaz. 3) Öğrenci satırında **Görüntüle**'ye bas; sağdan açılan panelde öğrencinin karnesini görürsün. Bu sayfa Öğretmen ve üstüne açıktır.

### 095 · PASS · Öğretmen

- Soru: Belirli bir öğrencinin notlarına bakmak istiyorum
- Beklenen intent: `student_marks_lookup`
- Gerçek intent: `student_marks_lookup`
- response_id: `student_marks_lookup_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Öğrenci notları", "route": "/management/student-marks"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/management/student-marks` (Öğrenci notları) sayfasını aç. 2) Aramaya **en az 2 karakter** yaz. 3) Öğrenci satırında **Görüntüle**'ye bas; sağdan açılan panelde öğrencinin karnesini görürsün. Bu sayfa Öğretmen ve üstüne açıktır.

### 096 · PASS · Öğrenci

- Soru: Kendi devamsızlık durumumu görmek istiyorum
- Beklenen intent: `attendance_view`
- Gerçek intent: `attendance_view`
- response_id: `attendance_report_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yoklama", "route": "/attendance"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kendi yoklamanı görmek için **Yoklama (Attendance)** menüsünden `/attendance`'a git. **Etkinlikler** ve **Ders oturumları** için ayrı devam oranı (%) kartları ve **Ders dökümü** tablosu (ders bazında Var/Yok/Geç/Mazeretli) görürsün. Bu sayfa yalnızca Öğrenci rolüne açıktır.

### 097 · PASS · Öğrenci

- Soru: Devam yüzdemi nereden görürüm?
- Beklenen intent: `attendance_view`
- Gerçek intent: `attendance_view`
- response_id: `attendance_report_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yoklama", "route": "/attendance"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kendi yoklamanı görmek için **Yoklama (Attendance)** menüsünden `/attendance`'a git. **Etkinlikler** ve **Ders oturumları** için ayrı devam oranı (%) kartları ve **Ders dökümü** tablosu (ders bazında Var/Yok/Geç/Mazeretli) görürsün. Bu sayfa yalnızca Öğrenci rolüne açıktır.

### 098 · PASS · Öğrenci

- Soru: Yoklama geçmişime bakmak istiyorum
- Beklenen intent: `attendance_view`
- Gerçek intent: `attendance_view`
- response_id: `attendance_report_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yoklama", "route": "/attendance"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kendi yoklamanı görmek için **Yoklama (Attendance)** menüsünden `/attendance`'a git. **Etkinlikler** ve **Ders oturumları** için ayrı devam oranı (%) kartları ve **Ders dökümü** tablosu (ders bazında Var/Yok/Geç/Mazeretli) görürsün. Bu sayfa yalnızca Öğrenci rolüne açıktır.

### 099 · PASS · Öğrenci

- Soru: Mazeretli sayılırsam oranım etkilenir mi?
- Beklenen intent: `attendance_rate_info`
- Gerçek intent: `attendance_rate_info`
- response_id: `attendance_rate_explained`
- confidence: `0.5852`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yoklama", "route": "/attendance"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Devam oranı = (Var + Geç) / (Var + Yok + Geç). Geç kalmak 'katıldı' sayılır; **Mazeretli oranın dışındadır** (ne lehte ne aleyhte). Kayıt yoksa veya tümü mazeretliyse oran boştur. Etkinlik devamı ile ders oturumu devamı ayrı hesaplanır.

### 100 · PASS · Öğrenci

- Soru: Devam oranı formülü nedir?
- Beklenen intent: `attendance_rate_info`
- Gerçek intent: `attendance_rate_info`
- response_id: `attendance_rate_explained`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yoklama", "route": "/attendance"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Devam oranı = (Var + Geç) / (Var + Yok + Geç). Geç kalmak 'katıldı' sayılır; **Mazeretli oranın dışındadır** (ne lehte ne aleyhte). Kayıt yoksa veya tümü mazeretliyse oran boştur. Etkinlik devamı ile ders oturumu devamı ayrı hesaplanır.

### 101 · PASS · Öğrenci

- Soru: Geç kalma devamsızlığa mı yazılır?
- Beklenen intent: `attendance_rate_info`
- Gerçek intent: `attendance_rate_info`
- response_id: `attendance_rate_explained`
- confidence: `0.6048`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yoklama", "route": "/attendance"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Devam oranı = (Var + Geç) / (Var + Yok + Geç). Geç kalmak 'katıldı' sayılır; **Mazeretli oranın dışındadır** (ne lehte ne aleyhte). Kayıt yoksa veya tümü mazeretliyse oran boştur. Etkinlik devamı ile ders oturumu devamı ayrı hesaplanır.

### 102 · PASS · Öğrenci

- Soru: Etkinliğe katıldığımı nasıl bildiririm?
- Beklenen intent: `event_attendance_mark`
- Gerçek intent: `event_attendance_mark`
- response_id: `event_attendance_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 103 · PASS · Öğrenci

- Soru: Kendi etkinlik yoklamamı işaretlemek istiyorum
- Beklenen intent: `event_attendance_mark`
- Gerçek intent: `event_attendance_mark`
- response_id: `event_attendance_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 104 · PASS · Öğrenci

- Soru: Bir etkinlikte var demek istiyorum
- Beklenen intent: `event_attendance_mark`
- Gerçek intent: `event_attendance_mark`
- response_id: `event_attendance_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 105 · PASS · Öğretmen

- Soru: Öğretmen olarak öğrencinin devamsızlığını sorgulamak istiyorum
- Beklenen intent: `student_attendance_lookup`
- Gerçek intent: `student_attendance_lookup`
- response_id: `student_attendance_lookup_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Öğrenci yoklaması", "route": "/management/student-attendance"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/management/student-attendance` (Öğrenci yoklaması) sayfasını aç. 2) Aramaya **en az 2 karakter** yaz. 3) Öğrenci satırında **Görüntüle**; sağdan açılan panelde öğrencinin yoklama raporunu görürsün. Öğretmen ve üstüne açıktır.

### 106 · PASS · Öğretmen

- Soru: Bir öğrencinin yoklama raporu nerede?
- Beklenen intent: `student_attendance_lookup`
- Gerçek intent: `student_attendance_lookup`
- response_id: `student_attendance_lookup_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Öğrenci yoklaması", "route": "/management/student-attendance"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/management/student-attendance` (Öğrenci yoklaması) sayfasını aç. 2) Aramaya **en az 2 karakter** yaz. 3) Öğrenci satırında **Görüntüle**; sağdan açılan panelde öğrencinin yoklama raporunu görürsün. Öğretmen ve üstüne açıktır.

### 107 · PASS · Öğretmen

- Soru: Öğrenci devam durumu görüntüleme sayfası
- Beklenen intent: `student_attendance_lookup`
- Gerçek intent: `student_attendance_lookup`
- response_id: `student_attendance_lookup_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Öğrenci yoklaması", "route": "/management/student-attendance"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/management/student-attendance` (Öğrenci yoklaması) sayfasını aç. 2) Aramaya **en az 2 karakter** yaz. 3) Öğrenci satırında **Görüntüle**; sağdan açılan panelde öğrencinin yoklama raporunu görürsün. Öğretmen ve üstüne açıktır.

### 108 · PASS · Öğretmen

- Soru: Yeni bir etkinlik planlamak istiyorum
- Beklenen intent: `event_create`
- Gerçek intent: `event_create`
- response_id: `event_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Etkinlikler", "route": "/events"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/events` → **Etkinlik oluştur (Create event)**. 2) **Başlık** (zorunlu, ≤200), isteğe bağlı açıklama; isteğe bağlı **Başlangıç/Bitiş** tarih+saat. 3) **Oluştur**. Başlık boşsa 'Başlık gerekli'; bitiş başlangıçtan önce olamaz; tarihler gelecekte olmalı.

### 109 · PASS · Öğretmen

- Soru: Etkinlik ekleme nasıl yapılır?
- Beklenen intent: `event_create`
- Gerçek intent: `event_create`
- response_id: `event_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Etkinlikler", "route": "/events"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/events` → **Etkinlik oluştur (Create event)**. 2) **Başlık** (zorunlu, ≤200), isteğe bağlı açıklama; isteğe bağlı **Başlangıç/Bitiş** tarih+saat. 3) **Oluştur**. Başlık boşsa 'Başlık gerekli'; bitiş başlangıçtan önce olamaz; tarihler gelecekte olmalı.

### 110 · PASS · Öğretmen

- Soru: Bir toplantı etkinliği oluşturacağım
- Beklenen intent: `event_create`
- Gerçek intent: `event_create`
- response_id: `event_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Etkinlikler", "route": "/events"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/events` → **Etkinlik oluştur (Create event)**. 2) **Başlık** (zorunlu, ≤200), isteğe bağlı açıklama; isteğe bağlı **Başlangıç/Bitiş** tarih+saat. 3) **Oluştur**. Başlık boşsa 'Başlık gerekli'; bitiş başlangıçtan önce olamaz; tarihler gelecekte olmalı.

### 111 · PASS · Öğrenci

- Soru: Kişisel not almak istiyorum nasıl?
- Beklenen intent: `note_create`
- Gerçek intent: `note_create`
- response_id: `note_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) **Defter (Notebook)** menüsünden `/notes`'a git, **Yeni not (New note)**'a bas. 2) **Başlık** (zorunlu, ≤200) ve isteğe bağlı **İçerik** (≤10.000) gir. 3) **Ekler** bölümünde **Dosya ekle** ile en fazla 10 dosya ekle. 4) **Oluştur**. Notlar yalnızca sahibine görünür. 10 dosyaya ulaştığında önce bir eki silmelisin; dosya boyut sınırı okul ayarındandır (varsayılan ~5 MiB) ve aşılırsa 413 hatası alınır.

### 112 · PASS · Öğrenci

- Soru: Deftere dosya ekli not eklemek istiyorum
- Beklenen intent: `note_create`
- Gerçek intent: `note_create`
- response_id: `note_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) **Defter (Notebook)** menüsünden `/notes`'a git, **Yeni not (New note)**'a bas. 2) **Başlık** (zorunlu, ≤200) ve isteğe bağlı **İçerik** (≤10.000) gir. 3) **Ekler** bölümünde **Dosya ekle** ile en fazla 10 dosya ekle. 4) **Oluştur**. Notlar yalnızca sahibine görünür. 10 dosyaya ulaştığında önce bir eki silmelisin; dosya boyut sınırı okul ayarındandır (varsayılan ~5 MiB) ve aşılırsa 413 hatası alınır.

### 113 · PASS · Öğrenci

- Soru: Yeni not oluşturma nerede?
- Beklenen intent: `note_create`
- Gerçek intent: `note_create`
- response_id: `note_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) **Defter (Notebook)** menüsünden `/notes`'a git, **Yeni not (New note)**'a bas. 2) **Başlık** (zorunlu, ≤200) ve isteğe bağlı **İçerik** (≤10.000) gir. 3) **Ekler** bölümünde **Dosya ekle** ile en fazla 10 dosya ekle. 4) **Oluştur**. Notlar yalnızca sahibine görünür. 10 dosyaya ulaştığında önce bir eki silmelisin; dosya boyut sınırı okul ayarındandır (varsayılan ~5 MiB) ve aşılırsa 413 hatası alınır.

### 114 · PASS · Öğrenci

- Soru: not değiştirmek
- Beklenen intent: `note_edit`
- Gerçek intent: `note_edit`
- response_id: `note_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu değiştirmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Düzenle**'yi seç. 3) Başlığı veya içeriği değiştirip **Güncelle**'ye bas ve onayla. Yalnızca kendi Defter notlarını düzenleyebilirsin.

### 115 · PASS · Öğretmen

- Soru: notumu düzenlemek istiyorum
- Beklenen intent: `note_edit`
- Gerçek intent: `note_edit`
- response_id: `note_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu değiştirmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Düzenle**'yi seç. 3) Başlığı veya içeriği değiştirip **Güncelle**'ye bas ve onayla. Yalnızca kendi Defter notlarını düzenleyebilirsin.

### 116 · PASS · Veli

- Soru: Defterimdeki kaydın başlığını güncellemek istiyorum
- Beklenen intent: `note_edit`
- Gerçek intent: `note_edit`
- response_id: `note_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu değiştirmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Düzenle**'yi seç. 3) Başlığı veya içeriği değiştirip **Güncelle**'ye bas ve onayla. Yalnızca kendi Defter notlarını düzenleyebilirsin.

### 117 · PASS · ADMIN

- Soru: Bu notun içeriğini düzeltmek istiyorum
- Beklenen intent: `note_edit`
- Gerçek intent: `note_edit`
- response_id: `note_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu değiştirmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Düzenle**'yi seç. 3) Başlığı veya içeriği değiştirip **Güncelle**'ye bas ve onayla. Yalnızca kendi Defter notlarını düzenleyebilirsin.

### 118 · PASS · Öğrenci

- Soru: not silmek
- Beklenen intent: `note_delete`
- Gerçek intent: `note_delete`
- response_id: `note_delete_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu silmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Sil**'i seç. 3) Açılan onay penceresinde silme işlemini onayla. Yalnızca kendi Defter notlarını silebilirsin.

### 119 · PASS · Yönetici

- Soru: ben not silmek
- Beklenen intent: `note_delete`
- Gerçek intent: `note_delete`
- response_id: `note_delete_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu silmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Sil**'i seç. 3) Açılan onay penceresinde silme işlemini onayla. Yalnızca kendi Defter notlarını silebilirsin.

### 120 · PASS · Veli

- Soru: Defterimdeki eski yazıyı kaldırmak istiyorum
- Beklenen intent: `note_delete`
- Gerçek intent: `note_delete`
- response_id: `note_delete_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu silmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Sil**'i seç. 3) Açılan onay penceresinde silme işlemini onayla. Yalnızca kendi Defter notlarını silebilirsin.

### 121 · PASS · ADMIN

- Soru: notumu silmek istiyorum
- Beklenen intent: `note_delete`
- Gerçek intent: `note_delete`
- response_id: `note_delete_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu silmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Sil**'i seç. 3) Açılan onay penceresinde silme işlemini onayla. Yalnızca kendi Defter notlarını silebilirsin.

### 122 · PASS · Öğretmen

- Soru: Mesaiye giriş kaydı nasıl açarım?
- Beklenen intent: `work_checkin_out`
- Gerçek intent: `work_checkin_out`
- response_id: `work_checkin_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Mesai", "route": "/work"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Arayüzde `/work` bağlantısı Öğretmen/Yönetici hesabında görünür; ADMIN navigasyonunda gösterilmez (backend Teacher+ kontrolü ADMIN çağrısını da kabul eder). 1) `/work` (Mesai) sayfasını aç. 2) 'Giriş yapılmadı' ise **Giriş yap (Check in)**; iş bitince **Çıkış yap (Check out)**. 3) **Son kayıtlar**'da giriş/çıkış/süre ve Açık/Kapalı durumunu görürsün. Saatler sunucu damgalıdır; aynı anda tek açık mesai olabilir. 'Zaten giriş yaptın' hatasında önce açık kaydı **Çıkış yap** ile kapat; 'giriş yapılmadı' hatasında çıkıştan önce **Giriş yap**.

### 123 · PASS · Öğretmen

- Soru: İşe geldiğimi nasıl damgalarım?
- Beklenen intent: `work_checkin_out`
- Gerçek intent: `work_checkin_out`
- response_id: `work_checkin_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Mesai", "route": "/work"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Arayüzde `/work` bağlantısı Öğretmen/Yönetici hesabında görünür; ADMIN navigasyonunda gösterilmez (backend Teacher+ kontrolü ADMIN çağrısını da kabul eder). 1) `/work` (Mesai) sayfasını aç. 2) 'Giriş yapılmadı' ise **Giriş yap (Check in)**; iş bitince **Çıkış yap (Check out)**. 3) **Son kayıtlar**'da giriş/çıkış/süre ve Açık/Kapalı durumunu görürsün. Saatler sunucu damgalıdır; aynı anda tek açık mesai olabilir. 'Zaten giriş yaptın' hatasında önce açık kaydı **Çıkış yap** ile kapat; 'giriş yapılmadı' hatasında çıkıştan önce **Giriş yap**.

### 124 · PASS · Öğretmen

- Soru: Çıkış saatimi nasıl kaydederim?
- Beklenen intent: `work_checkin_out`
- Gerçek intent: `work_checkin_out`
- response_id: `work_checkin_instructions`
- confidence: `0.8844`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Mesai", "route": "/work"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Arayüzde `/work` bağlantısı Öğretmen/Yönetici hesabında görünür; ADMIN navigasyonunda gösterilmez (backend Teacher+ kontrolü ADMIN çağrısını da kabul eder). 1) `/work` (Mesai) sayfasını aç. 2) 'Giriş yapılmadı' ise **Giriş yap (Check in)**; iş bitince **Çıkış yap (Check out)**. 3) **Son kayıtlar**'da giriş/çıkış/süre ve Açık/Kapalı durumunu görürsün. Saatler sunucu damgalıdır; aynı anda tek açık mesai olabilir. 'Zaten giriş yaptın' hatasında önce açık kaydı **Çıkış yap** ile kapat; 'giriş yapılmadı' hatasında çıkıştan önce **Giriş yap**.

### 125 · PASS · Yönetici

- Soru: Yönetici olarak bir öğretmenin mesaisini düzeltmek istiyorum
- Beklenen intent: `staff_work_manage`
- Gerçek intent: `staff_work_manage`
- response_id: `staff_work_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Personel mesai", "route": "/management/staff-work"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/management/staff-work` (Personel mesai) → aramaya **en az 2 karakter** (öğretmen adı). 2) Öğretmen satırında **Görüntüle**. 3) **Kapalı** bir kaydın **Düzenle**'sini açıp giriş/çıkış tarih+saat düzelt, **Güncelle**. **Açık mesai düzeltilemez** (önce çıkış yapılmalı veya silinmeli); çıkış girişten önce olamaz.

### 126 · PASS · Yönetici

- Soru: Personel mesai kayıtlarını nereden yönetirim?
- Beklenen intent: `staff_work_manage`
- Gerçek intent: `staff_work_manage`
- response_id: `staff_work_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Personel mesai", "route": "/management/staff-work"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/management/staff-work` (Personel mesai) → aramaya **en az 2 karakter** (öğretmen adı). 2) Öğretmen satırında **Görüntüle**. 3) **Kapalı** bir kaydın **Düzenle**'sini açıp giriş/çıkış tarih+saat düzelt, **Güncelle**. **Açık mesai düzeltilemez** (önce çıkış yapılmalı veya silinmeli); çıkış girişten önce olamaz.

### 127 · PASS · Yönetici

- Soru: Kapalı bir mesai kaydını düzenlemek istiyorum
- Beklenen intent: `staff_work_manage`
- Gerçek intent: `staff_work_manage`
- response_id: `staff_work_instructions`
- confidence: `0.8764`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Personel mesai", "route": "/management/staff-work"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/management/staff-work` (Personel mesai) → aramaya **en az 2 karakter** (öğretmen adı). 2) Öğretmen satırında **Görüntüle**. 3) **Kapalı** bir kaydın **Düzenle**'sini açıp giriş/çıkış tarih+saat düzelt, **Güncelle**. **Açık mesai düzeltilemez** (önce çıkış yapılmalı veya silinmeli); çıkış girişten önce olamaz.

### 128 · PASS · Yönetici

- Soru: Yeni akademik dönem eklemek istiyorum
- Beklenen intent: `term_manage`
- Gerçek intent: `term_manage`
- response_id: `term_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dönemler", "route": "/management/terms"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/management/terms` (Dönemler) → **Dönem oluştur (Create term)**. 2) **Ad**, **Başlangıç**, **Bitiş** (GG/AA/YYYY) gir; bitiş başlangıçtan önce olamaz (tarihler geçmişte olabilir). 3) **Oluştur**. Dersi döneme bağlamak, ders oluşturma/düzenleme formundaki **Dönem** seçicisinden yapılır. Bir dönem herhangi bir ders veya şubeye bağlıysa silme işlemi 409 ile reddedilir; önce bu bağlantıları kaldırmalısın.

### 129 · PASS · Yönetici

- Soru: Dersi bir yarıyıla nasıl bağlarım?
- Beklenen intent: `term_manage`
- Gerçek intent: `term_manage`
- response_id: `term_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dönemler", "route": "/management/terms"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/management/terms` (Dönemler) → **Dönem oluştur (Create term)**. 2) **Ad**, **Başlangıç**, **Bitiş** (GG/AA/YYYY) gir; bitiş başlangıçtan önce olamaz (tarihler geçmişte olabilir). 3) **Oluştur**. Dersi döneme bağlamak, ders oluşturma/düzenleme formundaki **Dönem** seçicisinden yapılır. Bir dönem herhangi bir ders veya şubeye bağlıysa silme işlemi 409 ile reddedilir; önce bu bağlantıları kaldırmalısın.

### 130 · PASS · Yönetici

- Soru: Dönem yönetimi sayfası nerede?
- Beklenen intent: `term_manage`
- Gerçek intent: `term_manage`
- response_id: `term_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dönemler", "route": "/management/terms"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/management/terms` (Dönemler) → **Dönem oluştur (Create term)**. 2) **Ad**, **Başlangıç**, **Bitiş** (GG/AA/YYYY) gir; bitiş başlangıçtan önce olamaz (tarihler geçmişte olabilir). 3) **Oluştur**. Dersi döneme bağlamak, ders oluşturma/düzenleme formundaki **Dönem** seçicisinden yapılır. Bir dönem herhangi bir ders veya şubeye bağlıysa silme işlemi 409 ile reddedilir; önce bu bağlantıları kaldırmalısın.

### 131 · PASS · Yönetici

- Soru: Sınav türü ağırlıklarını değiştirmek istiyorum
- Beklenen intent: `school_settings`
- Gerçek intent: `school_settings`
- response_id: `school_settings_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ayarlar", "route": "/management/settings"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> `/management/settings` (Okul ayarları) sayfasında **Değerlendirme** sekmesinde sınav türü/ağırlığı, yoklama durumları ve not bantları; **Yemekhane** sekmesinde rezervasyon kapanış süresi, öğün saatleri ve beslenme etiketleri; **Sistem** sekmesinde not/dosya yükleme limiti ile Çelebi sohbet geçmişi, konu ve mesaj limitleri yönetilir. **Satır ekle** ile ekle, çöp kutusuyla sil, sonra **Kaydet**. Bu okul geneli sayfa kişisel hesap/avatar **Ayarlar** penceresinden farklıdır.

### 132 · PASS · Yönetici

- Soru: Not bantlarını nereden düzenlerim?
- Beklenen intent: `school_settings`
- Gerçek intent: `school_settings`
- response_id: `school_settings_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ayarlar", "route": "/management/settings"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> `/management/settings` (Okul ayarları) sayfasında **Değerlendirme** sekmesinde sınav türü/ağırlığı, yoklama durumları ve not bantları; **Yemekhane** sekmesinde rezervasyon kapanış süresi, öğün saatleri ve beslenme etiketleri; **Sistem** sekmesinde not/dosya yükleme limiti ile Çelebi sohbet geçmişi, konu ve mesaj limitleri yönetilir. **Satır ekle** ile ekle, çöp kutusuyla sil, sonra **Kaydet**. Bu okul geneli sayfa kişisel hesap/avatar **Ayarlar** penceresinden farklıdır.

### 133 · PASS · Yönetici

- Soru: Okul geneli ayarlar nerede?
- Beklenen intent: `school_settings`
- Gerçek intent: `school_settings`
- response_id: `school_settings_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ayarlar", "route": "/management/settings"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> `/management/settings` (Okul ayarları) sayfasında **Değerlendirme** sekmesinde sınav türü/ağırlığı, yoklama durumları ve not bantları; **Yemekhane** sekmesinde rezervasyon kapanış süresi, öğün saatleri ve beslenme etiketleri; **Sistem** sekmesinde not/dosya yükleme limiti ile Çelebi sohbet geçmişi, konu ve mesaj limitleri yönetilir. **Satır ekle** ile ekle, çöp kutusuyla sil, sonra **Kaydet**. Bu okul geneli sayfa kişisel hesap/avatar **Ayarlar** penceresinden farklıdır.

### 134 · PASS · ADMIN

- Soru: Bir kullanıcıyı öğretmen yapmak istiyorum
- Beklenen intent: `user_role_change`
- Gerçek intent: `user_role_change`
- response_id: `user_role_change_instructions`
- confidence: `0.5754`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Kullanıcılar", "route": "/admin/users"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Ne:** **Kullanıcılar** (`/admin/users`, yalnız ADMIN) tüm hesapları yönettiğin yerdir — burada (a) **rol değiştirir**, (b) **herhangi bir kullanıcının profilini düzenlersin**.
> **Nereden / nasıl (rol):** 1) `/admin/users`'ı aç, ada göre **ara**. 2) Satırdaki **rol menüsünden** yeni rolü seç. 3) Beliren **Güncelle (Update)**'ye basıp onayla. Kendi rolünü değiştiremezsin (kendi satırında menü pasif); değişiklik sonraki işlemde hemen geçerli olur.
> **Etkili kullanım:** kalabalık listede önce **arama/filtre** ile daralt; rolü yanlışlıkla düşürmemek için değişiklikten önce satırdaki adı teyit et. Kendi rolünü ve sistemdeki son ADMIN'in rolünü değiştiremezsin. Rol değişimi ders kaydı/öğretmen ataması, randevu slotu, etkinlik kaydı ve beyaz tahta üyelikleri gibi role bağlı ilişkileri etkileyebilir. Profil düzeltmek için kullanıcının satırından profiline geçip alanları güncelle.

### 135 · PASS · ADMIN

- Soru: Admin olarak rol atama nasıl yapılır?
- Beklenen intent: `user_role_change`
- Gerçek intent: `user_role_change`
- response_id: `user_role_change_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Kullanıcılar", "route": "/admin/users"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Ne:** **Kullanıcılar** (`/admin/users`, yalnız ADMIN) tüm hesapları yönettiğin yerdir — burada (a) **rol değiştirir**, (b) **herhangi bir kullanıcının profilini düzenlersin**.
> **Nereden / nasıl (rol):** 1) `/admin/users`'ı aç, ada göre **ara**. 2) Satırdaki **rol menüsünden** yeni rolü seç. 3) Beliren **Güncelle (Update)**'ye basıp onayla. Kendi rolünü değiştiremezsin (kendi satırında menü pasif); değişiklik sonraki işlemde hemen geçerli olur.
> **Etkili kullanım:** kalabalık listede önce **arama/filtre** ile daralt; rolü yanlışlıkla düşürmemek için değişiklikten önce satırdaki adı teyit et. Kendi rolünü ve sistemdeki son ADMIN'in rolünü değiştiremezsin. Rol değişimi ders kaydı/öğretmen ataması, randevu slotu, etkinlik kaydı ve beyaz tahta üyelikleri gibi role bağlı ilişkileri etkileyebilir. Profil düzeltmek için kullanıcının satırından profiline geçip alanları güncelle.

### 136 · PASS · ADMIN

- Soru: Kullanıcının yetkisini yükseltmek istiyorum
- Beklenen intent: `user_role_change`
- Gerçek intent: `user_role_change`
- response_id: `user_role_change_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Kullanıcılar", "route": "/admin/users"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Ne:** **Kullanıcılar** (`/admin/users`, yalnız ADMIN) tüm hesapları yönettiğin yerdir — burada (a) **rol değiştirir**, (b) **herhangi bir kullanıcının profilini düzenlersin**.
> **Nereden / nasıl (rol):** 1) `/admin/users`'ı aç, ada göre **ara**. 2) Satırdaki **rol menüsünden** yeni rolü seç. 3) Beliren **Güncelle (Update)**'ye basıp onayla. Kendi rolünü değiştiremezsin (kendi satırında menü pasif); değişiklik sonraki işlemde hemen geçerli olur.
> **Etkili kullanım:** kalabalık listede önce **arama/filtre** ile daralt; rolü yanlışlıkla düşürmemek için değişiklikten önce satırdaki adı teyit et. Kendi rolünü ve sistemdeki son ADMIN'in rolünü değiştiremezsin. Rol değişimi ders kaydı/öğretmen ataması, randevu slotu, etkinlik kaydı ve beyaz tahta üyelikleri gibi role bağlı ilişkileri etkileyebilir. Profil düzeltmek için kullanıcının satırından profiline geçip alanları güncelle.

### 137 · PASS · Öğrenci

- Soru: Başka birinin karnesini öğrenebilir miyim?
- Beklenen intent: `privacy_security`
- Gerçek intent: `privacy_security`
- response_id: `privacy_policy_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yalnızca kendi yetkili olduğun bilgileri görebilirsin. Başka bir kullanıcının notu, yoklaması veya kişisel bilgisi paylaşılmaz. Öğretmen ve üstü roller, yalnızca yetkili oldukları yönetim sayfalarından (Öğrenci notları/yoklaması) öğrenci verisine erişebilir; kişisel telefon/e-posta paylaşılmaz.

### 138 · PASS · Öğrenci

- Soru: Sınıf arkadaşımın devamsızlığını söyle
- Beklenen intent: `privacy_security`
- Gerçek intent: `privacy_security`
- response_id: `privacy_policy_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yalnızca kendi yetkili olduğun bilgileri görebilirsin. Başka bir kullanıcının notu, yoklaması veya kişisel bilgisi paylaşılmaz. Öğretmen ve üstü roller, yalnızca yetkili oldukları yönetim sayfalarından (Öğrenci notları/yoklaması) öğrenci verisine erişebilir; kişisel telefon/e-posta paylaşılmaz.

### 139 · PASS · Öğrenci

- Soru: Bir öğretmenin telefon numarasını verir misin?
- Beklenen intent: `privacy_security`
- Gerçek intent: `privacy_security`
- response_id: `privacy_policy_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yalnızca kendi yetkili olduğun bilgileri görebilirsin. Başka bir kullanıcının notu, yoklaması veya kişisel bilgisi paylaşılmaz. Öğretmen ve üstü roller, yalnızca yetkili oldukları yönetim sayfalarından (Öğrenci notları/yoklaması) öğrenci verisine erişebilir; kişisel telefon/e-posta paylaşılmaz.

### 140 · PASS · Öğrenci

- Soru: Bugün hava nasıl olacak?
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 141 · PASS · Öğrenci

- Soru: Bana bir şiir yazar mısın?
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 142 · PASS · Öğrenci

- Soru: Matematik ödevimi çözer misin?
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 143 · PASS · Öğrenci

- Soru: En yakın pizzacı nerede?
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 144 · PASS · Öğrenci

- Soru: Türkiye'nin başkenti neresi?
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 145 · PASS · Öğrenci

- Soru: Bitcoin fiyatı bugün kaç?
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 146 · PASS · Öğrenci

- Soru: Nasıl kilo veririm?
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 147 · PASS · Öğrenci

- Soru: Bana bir fıkra anlat
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 148 · PASS · Öğrenci

- Soru: Kaç yaşındasın?
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 149 · PASS · Öğrenci

- Soru: Yarın maç var mı?
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 150 · PASS · Öğrenci

- Soru: İyi bir film önerir misin?
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 151 · PASS · Öğrenci

- Soru: 2 artı 2 kaç eder?
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 152 · PASS · Öğrenci

- Soru: Bu akşam ne pişirsem?
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 153 · PASS · Öğrenci

- Soru: Python'da nasıl döngü yazılır?
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 154 · PASS · Öğrenci

- Soru: Arabamın lastiği patladı ne yapmalıyım?
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 155 · PASS · Öğrenci

- Soru: Bana motivasyon sözü söyle
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 156 · PASS · Öğrenci

- Soru: İstanbul'a nasıl giderim?
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 157 · PASS · Öğrenci

- Soru: Kahve mi çay mı daha sağlıklı?
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 158 · PASS · Öğrenci

- Soru: Pythonda for döngüsü nasıl yazılır
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 159 · PASS · Öğrenci

- Soru: Bana pizza tarifi ver
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 160 · PASS · Öğrenci

- Soru: Sevgilimden ayrıldım çok üzgünüm
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 161 · PASS · Öğrenci

- Soru: Bugünkü maç kaçta başlıyor
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 162 · PASS · Öğrenci

- Soru: Kilo vermek için ne önerirsin
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 163 · PASS · Öğrenci

- Soru: En sevdiğin film hangisi
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 164 · PASS · Öğrenci

- Soru: Telefonumun şarjı çabuk bitiyor
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 165 · PASS · Öğrenci

- Soru: Yarın hava yağmurlu mu
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `fallback_clarification`
- confidence: `0.0000`
- fallback: `true`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `fallback` / `out_of_scope`
- Sözleşme: `PASS`

> Bu isteği tam anlayamadım. Hezarfen'de profil/ayarlar, ders/şube, sınav, ödev, karne/yoklama, Defter, randevu, yemek/ödeme, Mesajlar veya dosya ve hata sorunları hakkında daha açık yazabilir misin? Örneğin sayfayı, bastığın düğmeyi ve varsa hata metnini söyle: 'Ödev dosyam 413 veriyor' gibi.

### 166 · PASS · Öğretmen

- Soru: Gerçek öğrenci listesini buraya getir
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `out_of_scope_action`
- confidence: `0.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `deny` / `scope_boundary_data`
- Sözleşme: `PASS`

> Ben gerçek veriyi getiremem, gösteremem ya da göremem; sistemdeki canlı kayıtları bilemiyorum 🙂 Yalnızca nasıl yapılacağını adım adım anlatabilirim. Örneğin "öğrenci listesini nereden görürüm?" diye sorarsan, ilgili sayfayı ve adımları söyleyeyim.

### 167 · PASS · ADMIN

- Soru: Sistemde toplam kaç kullanıcı var
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `out_of_scope_action`
- confidence: `0.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `deny` / `scope_boundary_data`
- Sözleşme: `PASS`

> Ben gerçek veriyi getiremem, gösteremem ya da göremem; sistemdeki canlı kayıtları bilemiyorum 🙂 Yalnızca nasıl yapılacağını adım adım anlatabilirim. Örneğin "öğrenci listesini nereden görürüm?" diye sorarsan, ilgili sayfayı ve adımları söyleyeyim.

### 168 · PASS · Yönetici

- Soru: Kayıtlı öğretmenlerin sayısını bana söyle
- Beklenen intent: `oos`
- Gerçek intent: `oos`
- response_id: `out_of_scope_action`
- confidence: `0.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `deny` / `scope_boundary_data`
- Sözleşme: `PASS`

> Ben gerçek veriyi getiremem, gösteremem ya da göremem; sistemdeki canlı kayıtları bilemiyorum 🙂 Yalnızca nasıl yapılacağını adım adım anlatabilirim. Örneğin "öğrenci listesini nereden görürüm?" diye sorarsan, ilgili sayfayı ve adımları söyleyeyim.

### 169 · PASS · Öğrenci

- Soru: Çok teşekkür ederim ya
- Beklenen intent: `thanks`
- Gerçek intent: `thanks`
- response_id: `thanks_reply`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Rica ederim, kolay gelsin! 😊 Takıldığın başka bir yer olursa sormaktan çekinme.

### 170 · PASS · Öğrenci

- Soru: sağ olasın
- Beklenen intent: `thanks`
- Gerçek intent: `thanks`
- response_id: `thanks_reply`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Rica ederim, kolay gelsin! 😊 Takıldığın başka bir yer olursa sormaktan çekinme.

### 171 · PASS · Öğrenci

- Soru: eyvallah hocam
- Beklenen intent: `thanks`
- Gerçek intent: `thanks`
- response_id: `thanks_reply`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Rica ederim, kolay gelsin! 😊 Takıldığın başka bir yer olursa sormaktan çekinme.

### 172 · PASS · Öğrenci

- Soru: hadi görüşürüz
- Beklenen intent: `farewell`
- Gerçek intent: `farewell`
- response_id: `farewell_reply`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hoşça kal! 🪽 İhtiyacın olduğunda Çelebi bir mesaj uzağında. Kendine iyi bak!

### 173 · PASS · Öğrenci

- Soru: hoşçakal
- Beklenen intent: `farewell`
- Gerçek intent: `farewell`
- response_id: `farewell_reply`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hoşça kal! 🪽 İhtiyacın olduğunda Çelebi bir mesaj uzağında. Kendine iyi bak!

### 174 · PASS · Öğrenci

- Soru: iyi geceler sana
- Beklenen intent: `farewell`
- Gerçek intent: `farewell`
- response_id: `farewell_reply`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Görüşürüz, iyi günler! 👋 Derslerin ve sınavların kolay geçsin.

### 175 · PASS · Öğrenci

- Soru: sen bir robot musun
- Beklenen intent: `bot_identity`
- Gerçek intent: `bot_identity`
- response_id: `bot_identity_reply`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ben Çelebi 🪽 — Hezarfen'in kullanım asistanıyım. Adımı, Galata Kulesi'nden uçtuğu rivayet edilen Hezarfen Ahmed Çelebi'den alıyorum. Serbest metin üreten bir yapay zekâ değil, kural tabanlı bir yardımcıyım: sitedeki gerçek menü ve sayfalara dayanarak 'nasıl yaparım?' sorularını yanıtlar, seni doğru sayfaya yönlendiririm. Bir şey sormak ister misin?

### 176 · PASS · Öğrenci

- Soru: kimsin sen ya
- Beklenen intent: `bot_identity`
- Gerçek intent: `bot_identity`
- response_id: `bot_identity_reply`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ben Çelebi 🪽 — Hezarfen'in kullanım asistanıyım. Adımı, Galata Kulesi'nden uçtuğu rivayet edilen Hezarfen Ahmed Çelebi'den alıyorum. Serbest metin üreten bir yapay zekâ değil, kural tabanlı bir yardımcıyım: sitedeki gerçek menü ve sayfalara dayanarak 'nasıl yaparım?' sorularını yanıtlar, seni doğru sayfaya yönlendiririm. Bir şey sormak ister misin?

### 177 · PASS · Öğrenci

- Soru: senin adın ne
- Beklenen intent: `bot_identity`
- Gerçek intent: `bot_identity`
- response_id: `bot_identity_reply`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ben Çelebi 🪽 — Hezarfen'in kullanım asistanıyım. Adımı, Galata Kulesi'nden uçtuğu rivayet edilen Hezarfen Ahmed Çelebi'den alıyorum. Serbest metin üreten bir yapay zekâ değil, kural tabanlı bir yardımcıyım: sitedeki gerçek menü ve sayfalara dayanarak 'nasıl yaparım?' sorularını yanıtlar, seni doğru sayfaya yönlendiririm. Bir şey sormak ister misin?

### 178 · PASS · Öğrenci

- Soru: Pomodoro oturumu açmak istiyorum
- Beklenen intent: `pomodoro_use`
- Gerçek intent: `pomodoro_use`
- response_id: `pomodoro_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Pomodoro", "route": "/pomodoro"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Pomodoro, sunucu saatiyle damgalanan ve yalnız **Öğrenci** hesabının başlatabildiği kişisel odak kaydıdır. 1) `/pomodoro` sayfasına git. 2) **Odağı başlat (Start focus)** ile oturumu aç — aynı anda tek açık oturum olabilir. 3) Çalışman bitince **Odağı bitir (Finish focus)**'a bas. Sayfada **Toplam odak** süreni ve **Son oturumlar** geçmişini görürsün; saatler sunucu tarafından damgalanır.

### 179 · PASS · Öğrenci

- Soru: Odağı nasıl başlatırım?
- Beklenen intent: `pomodoro_use`
- Gerçek intent: `pomodoro_use`
- response_id: `pomodoro_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Pomodoro", "route": "/pomodoro"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Pomodoro, sunucu saatiyle damgalanan ve yalnız **Öğrenci** hesabının başlatabildiği kişisel odak kaydıdır. 1) `/pomodoro` sayfasına git. 2) **Odağı başlat (Start focus)** ile oturumu aç — aynı anda tek açık oturum olabilir. 3) Çalışman bitince **Odağı bitir (Finish focus)**'a bas. Sayfada **Toplam odak** süreni ve **Son oturumlar** geçmişini görürsün; saatler sunucu tarafından damgalanır.

### 180 · PASS · Öğrenci

- Soru: Toplam odak sürem nerede görünür?
- Beklenen intent: `pomodoro_use`
- Gerçek intent: `pomodoro_use`
- response_id: `pomodoro_instructions`
- confidence: `0.7110`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Pomodoro", "route": "/pomodoro"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Pomodoro, sunucu saatiyle damgalanan ve yalnız **Öğrenci** hesabının başlatabildiği kişisel odak kaydıdır. 1) `/pomodoro` sayfasına git. 2) **Odağı başlat (Start focus)** ile oturumu aç — aynı anda tek açık oturum olabilir. 3) Çalışman bitince **Odağı bitir (Finish focus)**'a bas. Sayfada **Toplam odak** süreni ve **Son oturumlar** geçmişini görürsün; saatler sunucu tarafından damgalanır.

### 181 · PASS · Öğretmen

- Soru: Öğrencinin pomodorolarına bakmak istiyorum
- Beklenen intent: `student_pomodoro_lookup`
- Gerçek intent: `student_pomodoro_lookup`
- response_id: `student_pomodoro_lookup_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Pomodorolar", "route": "/management/pomodoros"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Bir öğrencinin odak geçmişi için: 1) Yönetim menüsünden **Pomodorolar** (`/management/pomodoros`) sayfasına git. 2) Arama kutusuna öğrenci adını yaz ve seç. 3) Panelde o öğrencinin oturumları **Başlangıç / Bitiş / Süre** sütunlarıyla listelenir. Bu sayfa Öğretmen ve üstüne açıktır.

### 182 · PASS · Öğretmen

- Soru: Bir öğrencinin odak geçmişini nasıl açarım?
- Beklenen intent: `student_pomodoro_lookup`
- Gerçek intent: `student_pomodoro_lookup`
- response_id: `student_pomodoro_lookup_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Pomodorolar", "route": "/management/pomodoros"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Bir öğrencinin odak geçmişi için: 1) Yönetim menüsünden **Pomodorolar** (`/management/pomodoros`) sayfasına git. 2) Arama kutusuna öğrenci adını yaz ve seç. 3) Panelde o öğrencinin oturumları **Başlangıç / Bitiş / Süre** sütunlarıyla listelenir. Bu sayfa Öğretmen ve üstüne açıktır.

### 183 · PASS · Öğrenci

- Soru: Mesaj kutum nerede?
- Beklenen intent: `messages_use`
- Gerçek intent: `messages_use`
- response_id: `messages_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Mesajlar", "route": "/messages"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Mesajlar** (`/messages`), kullanıcılar arasında bire-bir, posta tarzı yazışma içindir. Sol menüden **Mesajlar**'ı aç: **Gelen kutusu**ndaki mesajları okuyabilir, mesajları **Arşiv**'e veya **Çöp**'e taşıyabilir, yeni mesaj oluşturup konu + metin yazarak gönderebilirsin. Bir iletiyi kalıcı silmek için önce **Çöp** klasörüne taşıyıp oradan sil; karşı tarafın kopyası senin arşivleme/silme işlemlerinden etkilenmez. Kendine mesaj gönderemezsin.

### 184 · PASS · Öğrenci

- Soru: Birine mesaj yollamak istiyorum
- Beklenen intent: `messages_use`
- Gerçek intent: `messages_use`
- response_id: `messages_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Mesajlar", "route": "/messages"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Mesajlar** (`/messages`), kullanıcılar arasında bire-bir, posta tarzı yazışma içindir. Sol menüden **Mesajlar**'ı aç: **Gelen kutusu**ndaki mesajları okuyabilir, mesajları **Arşiv**'e veya **Çöp**'e taşıyabilir, yeni mesaj oluşturup konu + metin yazarak gönderebilirsin. Bir iletiyi kalıcı silmek için önce **Çöp** klasörüne taşıyıp oradan sil; karşı tarafın kopyası senin arşivleme/silme işlemlerinden etkilenmez. Kendine mesaj gönderemezsin.

### 185 · PASS · Veli

- Soru: Gelen kutusuna nereden bakarım?
- Beklenen intent: `messages_use`
- Gerçek intent: `messages_use`
- response_id: `messages_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Mesajlar", "route": "/messages"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Mesajlar** (`/messages`), kullanıcılar arasında bire-bir, posta tarzı yazışma içindir. Sol menüden **Mesajlar**'ı aç: **Gelen kutusu**ndaki mesajları okuyabilir, mesajları **Arşiv**'e veya **Çöp**'e taşıyabilir, yeni mesaj oluşturup konu + metin yazarak gönderebilirsin. Bir iletiyi kalıcı silmek için önce **Çöp** klasörüne taşıyıp oradan sil; karşı tarafın kopyası senin arşivleme/silme işlemlerinden etkilenmez. Kendine mesaj gönderemezsin.

### 186 · PASS · Öğrenci

- Soru: Etüt ne demek?
- Beklenen intent: `study_club_info`
- Gerçek intent: `study_club_info`
- response_id: `study_club_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Etüt", "route": "/studies"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Etüt** ve **Kulüp**, dersin iki özel türüdür — ders altyapısının aynısını kullanırlar (kayıt, oturum, yoklama, sınav). Ayrı sol menü öğeleri değillerdir: **Eğitim/Dersler** (`/courses`) sayfasındaki **Etüt** ve **Kulüp** filtrelerinden açılırlar; `/studies` ve `/clubs` adresleri de bu filtreli listeye yönlendirir. Öğretmen+ oluşturur; öğrenciyi ders yöneticisi roster üzerinden kaydeder, öğrenci kendi kendine kaydolmaz. Kontenjan sınırı konabilir.

### 187 · PASS · Öğrenci

- Soru: Kulüp dersten farklı mı?
- Beklenen intent: `study_club_info`
- Gerçek intent: `study_club_info`
- response_id: `study_club_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Etüt", "route": "/studies"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Etüt** ve **Kulüp**, dersin iki özel türüdür — ders altyapısının aynısını kullanırlar (kayıt, oturum, yoklama, sınav). Ayrı sol menü öğeleri değillerdir: **Eğitim/Dersler** (`/courses`) sayfasındaki **Etüt** ve **Kulüp** filtrelerinden açılırlar; `/studies` ve `/clubs` adresleri de bu filtreli listeye yönlendirir. Öğretmen+ oluşturur; öğrenciyi ders yöneticisi roster üzerinden kaydeder, öğrenci kendi kendine kaydolmaz. Kontenjan sınırı konabilir.

### 188 · PASS · Öğrenci

- Soru: Etüde nasıl katılırım?
- Beklenen intent: `study_club_info`
- Gerçek intent: `study_club_info`
- response_id: `study_club_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Etüt", "route": "/studies"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Etüt** ve **Kulüp**, dersin iki özel türüdür — ders altyapısının aynısını kullanırlar (kayıt, oturum, yoklama, sınav). Ayrı sol menü öğeleri değillerdir: **Eğitim/Dersler** (`/courses`) sayfasındaki **Etüt** ve **Kulüp** filtrelerinden açılırlar; `/studies` ve `/clubs` adresleri de bu filtreli listeye yönlendirir. Öğretmen+ oluşturur; öğrenciyi ders yöneticisi roster üzerinden kaydeder, öğrenci kendi kendine kaydolmaz. Kontenjan sınırı konabilir.

### 189 · PASS · Öğrenci

- Soru: Veli hesabı nedir?
- Beklenen intent: `parent_info`
- Gerçek intent: `parent_info`
- response_id: `parent_role_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Çocuklarım", "route": "/students"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Ne:** **Veli**, kendisine bağlanan öğrencileri **salt-okunur** izleyen roldür: bağlı öğrencinin not/karnesini, yoklamasını, ödev raporunu, şube üyeliklerini ve Pomodoro geçmişini görüntüleyebilir; Mesajlar'ı kullanabilir. Veli ayrıca uygun randevuyu ve çocuğu için yemeği ayırabilir. Veli hesabı sınava giremez, derse kaydolamaz ve yoklamada işaretlenmez — bu işlemler öğrenciye özeldir.
> **Nereden/nasıl:** Bağlı öğrencilerini **Çocuklarım** sayfasından (`/students`) görürsün; bir çocuğu seçip notlarına/karnesine ve yoklamasına oradan geçersin.
> **Etkili kullanım:** Birden çok öğrenci tek veliye bağlanabilir — Çocuklarım'dan aralarında geçiş yaparsın. Veli–öğrenci bağlantısını **ADMIN** kurar; bağlantı görünmüyorsa okuldan bağlanmasını iste.

### 190 · PASS · Öğrenci

- Soru: Velim notlarımı görebilir mi?
- Beklenen intent: `parent_info`
- Gerçek intent: `parent_info`
- response_id: `parent_role_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Çocuklarım", "route": "/students"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Ne:** **Veli**, kendisine bağlanan öğrencileri **salt-okunur** izleyen roldür: bağlı öğrencinin not/karnesini, yoklamasını, ödev raporunu, şube üyeliklerini ve Pomodoro geçmişini görüntüleyebilir; Mesajlar'ı kullanabilir. Veli ayrıca uygun randevuyu ve çocuğu için yemeği ayırabilir. Veli hesabı sınava giremez, derse kaydolamaz ve yoklamada işaretlenmez — bu işlemler öğrenciye özeldir.
> **Nereden/nasıl:** Bağlı öğrencilerini **Çocuklarım** sayfasından (`/students`) görürsün; bir çocuğu seçip notlarına/karnesine ve yoklamasına oradan geçersin.
> **Etkili kullanım:** Birden çok öğrenci tek veliye bağlanabilir — Çocuklarım'dan aralarında geçiş yaparsın. Veli–öğrenci bağlantısını **ADMIN** kurar; bağlantı görünmüyorsa okuldan bağlanmasını iste.

### 191 · PASS · Veli

- Soru: Ebeveyn rolü ne işe yarıyor?
- Beklenen intent: `parent_info`
- Gerçek intent: `parent_info`
- response_id: `parent_role_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Çocuklarım", "route": "/students"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Ne:** **Veli**, kendisine bağlanan öğrencileri **salt-okunur** izleyen roldür: bağlı öğrencinin not/karnesini, yoklamasını, ödev raporunu, şube üyeliklerini ve Pomodoro geçmişini görüntüleyebilir; Mesajlar'ı kullanabilir. Veli ayrıca uygun randevuyu ve çocuğu için yemeği ayırabilir. Veli hesabı sınava giremez, derse kaydolamaz ve yoklamada işaretlenmez — bu işlemler öğrenciye özeldir.
> **Nereden/nasıl:** Bağlı öğrencilerini **Çocuklarım** sayfasından (`/students`) görürsün; bir çocuğu seçip notlarına/karnesine ve yoklamasına oradan geçersin.
> **Etkili kullanım:** Birden çok öğrenci tek veliye bağlanabilir — Çocuklarım'dan aralarında geçiş yaparsın. Veli–öğrenci bağlantısını **ADMIN** kurar; bağlantı görünmüyorsa okuldan bağlanmasını iste.

### 192 · PASS · Ziyaretçi

- Soru: Hazerfen tam olarak ne?
- Beklenen intent: `platform_info`
- Gerçek intent: `platform_info`
- response_id: `platform_overview`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Rehber", "route": "/guide"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hezarfen, bir okulun **ders, sınav, not, yoklama, etkinlik ve personel mesaisini tek yerde** toplayan bir okul yönetim sitesidir — sloganı: "Kampüs çalışma alanın: notlar, etkinlikler ve sınavlar tek yerde." Temel akış **Ders → Sınav → Karne**: öğretmen ders açar, öğrenci sınavlara girer, notlar **Karnem**'de ağırlıklı ortalamayla toplanır. Ayrıca kişisel **Defter**, **Etkinlikler**, **Yoklama** ve personel için **Mesai** var. Ben Çelebi, bu siteyi nasıl kullanacağını adım adım anlatırım — 'ne yapmak istiyorsun?' diye sorabilirsin.

### 193 · PASS · Öğrenci

- Soru: Bu platform ne için var?
- Beklenen intent: `platform_info`
- Gerçek intent: `platform_info`
- response_id: `platform_overview`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Rehber", "route": "/guide"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hezarfen, bir okulun **ders, sınav, not, yoklama, etkinlik ve personel mesaisini tek yerde** toplayan bir okul yönetim sitesidir — sloganı: "Kampüs çalışma alanın: notlar, etkinlikler ve sınavlar tek yerde." Temel akış **Ders → Sınav → Karne**: öğretmen ders açar, öğrenci sınavlara girer, notlar **Karnem**'de ağırlıklı ortalamayla toplanır. Ayrıca kişisel **Defter**, **Etkinlikler**, **Yoklama** ve personel için **Mesai** var. Ben Çelebi, bu siteyi nasıl kullanacağını adım adım anlatırım — 'ne yapmak istiyorsun?' diye sorabilirsin.

### 194 · PASS · Ziyaretçi

- Soru: Hezarfeni kısaca tanıtır mısın
- Beklenen intent: `platform_info`
- Gerçek intent: `platform_info`
- response_id: `platform_overview`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Rehber", "route": "/guide"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hezarfen, bir okulun **ders, sınav, not, yoklama, etkinlik ve personel mesaisini tek yerde** toplayan bir okul yönetim sitesidir — sloganı: "Kampüs çalışma alanın: notlar, etkinlikler ve sınavlar tek yerde." Temel akış **Ders → Sınav → Karne**: öğretmen ders açar, öğrenci sınavlara girer, notlar **Karnem**'de ağırlıklı ortalamayla toplanır. Ayrıca kişisel **Defter**, **Etkinlikler**, **Yoklama** ve personel için **Mesai** var. Ben Çelebi, bu siteyi nasıl kullanacağını adım adım anlatırım — 'ne yapmak istiyorsun?' diye sorabilirsin.

### 195 · PASS · Öğrenci

- Soru: Bana atanan ödevler nerede
- Beklenen intent: `homework_view`
- Gerçek intent: `homework_view`
- response_id: `homework_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ödevleri **Akademik** grubundaki **Ödevler** menüsünden (`/homework`) görürsün. Öğrencide sayfa **Ödevlerim** başlığıyla açılır; her kartta **Son teslim** tarihi ve durum görünür. Bir ödevin detayına gitmek için **Aç**'a bas (`/homework/$id`). Öğretmen ve üstü, verdikleri ödevleri ve **Teslimler**'i aynı sayfadan takip eder.

### 196 · PASS · Öğrenci

- Soru: Ödev listemi görmek istiyorum
- Beklenen intent: `homework_view`
- Gerçek intent: `homework_view`
- response_id: `homework_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ödevleri **Akademik** grubundaki **Ödevler** menüsünden (`/homework`) görürsün. Öğrencide sayfa **Ödevlerim** başlığıyla açılır; her kartta **Son teslim** tarihi ve durum görünür. Bir ödevin detayına gitmek için **Aç**'a bas (`/homework/$id`). Öğretmen ve üstü, verdikleri ödevleri ve **Teslimler**'i aynı sayfadan takip eder.

### 197 · PASS · Öğrenci

- Soru: Ödevlerim hangi sayfada
- Beklenen intent: `homework_view`
- Gerçek intent: `homework_view`
- response_id: `homework_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ödevleri **Akademik** grubundaki **Ödevler** menüsünden (`/homework`) görürsün. Öğrencide sayfa **Ödevlerim** başlığıyla açılır; her kartta **Son teslim** tarihi ve durum görünür. Bir ödevin detayına gitmek için **Aç**'a bas (`/homework/$id`). Öğretmen ve üstü, verdikleri ödevleri ve **Teslimler**'i aynı sayfadan takip eder.

### 198 · PASS · Öğrenci

- Soru: Ödevi nasıl gönderirim
- Beklenen intent: `homework_submit`
- Gerçek intent: `homework_submit`
- response_id: `homework_submit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ödevin verildiği dersin kayıtlı öğrencisisin. 1) **Ödevler** (`/homework`) → ilgili ödevin detayına (`/homework/$id`) gir. 2) **Ödevi teslim et** panelinde cevabını yaz ve/veya dosya ekle. 3) Gönder. Teslim yalnızca Öğrenciye açıktır; **Son teslim** tarihine dikkat et. Teslim notlandırıldıktan sonra öğrenci metni veya dosyayı değiştiremez/silemez; dosya okulun yükleme sınırını aşarsa 413 hatası alınır.

### 199 · PASS · Öğrenci

- Soru: Ödev teslimini nereden yaparım
- Beklenen intent: `homework_submit`
- Gerçek intent: `homework_submit`
- response_id: `homework_submit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ödevin verildiği dersin kayıtlı öğrencisisin. 1) **Ödevler** (`/homework`) → ilgili ödevin detayına (`/homework/$id`) gir. 2) **Ödevi teslim et** panelinde cevabını yaz ve/veya dosya ekle. 3) Gönder. Teslim yalnızca Öğrenciye açıktır; **Son teslim** tarihine dikkat et. Teslim notlandırıldıktan sonra öğrenci metni veya dosyayı değiştiremez/silemez; dosya okulun yükleme sınırını aşarsa 413 hatası alınır.

### 200 · PASS · Öğrenci

- Soru: Yaptığım ödevi yüklemek istiyorum
- Beklenen intent: `homework_submit`
- Gerçek intent: `homework_submit`
- response_id: `homework_submit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ödevin verildiği dersin kayıtlı öğrencisisin. 1) **Ödevler** (`/homework`) → ilgili ödevin detayına (`/homework/$id`) gir. 2) **Ödevi teslim et** panelinde cevabını yaz ve/veya dosya ekle. 3) Gönder. Teslim yalnızca Öğrenciye açıktır; **Son teslim** tarihine dikkat et. Teslim notlandırıldıktan sonra öğrenci metni veya dosyayı değiştiremez/silemez; dosya okulun yükleme sınırını aşarsa 413 hatası alınır.

### 201 · PASS · Öğretmen

- Soru: Sınıfa ödev atamak istiyorum
- Beklenen intent: `homework_assign`
- Gerçek intent: `homework_assign`
- response_id: `homework_assign_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: yönettiğin bir ders olmalı. 1) **Ödevler** (`/homework`) → **Ödev ekle**. 2) Dersi seç, başlık ve açıklamayı gir, **Son teslim** tarihini belirle. 3) Oluştur. Ödev dersin öğrencilerine atanır; gelen teslimleri ödev detayındaki **Teslimler** bölümünden görürsün.

### 202 · PASS · Öğretmen

- Soru: Öğrencilerime nasıl ödev veririm
- Beklenen intent: `homework_assign`
- Gerçek intent: `homework_assign`
- response_id: `homework_assign_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: yönettiğin bir ders olmalı. 1) **Ödevler** (`/homework`) → **Ödev ekle**. 2) Dersi seç, başlık ve açıklamayı gir, **Son teslim** tarihini belirle. 3) Oluştur. Ödev dersin öğrencilerine atanır; gelen teslimleri ödev detayındaki **Teslimler** bölümünden görürsün.

### 203 · PASS · Öğretmen

- Soru: Yeni bir ödev oluşturmak istiyorum
- Beklenen intent: `homework_assign`
- Gerçek intent: `homework_assign`
- response_id: `homework_assign_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: yönettiğin bir ders olmalı. 1) **Ödevler** (`/homework`) → **Ödev ekle**. 2) Dersi seç, başlık ve açıklamayı gir, **Son teslim** tarihini belirle. 3) Oluştur. Ödev dersin öğrencilerine atanır; gelen teslimleri ödev detayındaki **Teslimler** bölümünden görürsün.

### 204 · PASS · Öğretmen

- Soru: Öğrencinin ödevine nasıl not veririm
- Beklenen intent: `homework_grade`
- Gerçek intent: `homework_grade`
- response_id: `homework_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ödevi verdiğin (yönettiğin) ders. 1) **Ödevler** (`/homework`) → ödevin detayı → **Teslimler**. 2) Bir öğrencinin teslimini aç, **Notlandır** ile not/geri bildirim ver; gerekirse **Notu kaldır** ile geri al. Notlandırma Öğretmen ve üstüne açıktır; kendi teslimini notlandıramazsın.

### 205 · PASS · Öğretmen

- Soru: Ödev teslimini değerlendirmek istiyorum
- Beklenen intent: `homework_grade`
- Gerçek intent: `homework_grade`
- response_id: `homework_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ödevi verdiğin (yönettiğin) ders. 1) **Ödevler** (`/homework`) → ödevin detayı → **Teslimler**. 2) Bir öğrencinin teslimini aç, **Notlandır** ile not/geri bildirim ver; gerekirse **Notu kaldır** ile geri al. Notlandırma Öğretmen ve üstüne açıktır; kendi teslimini notlandıramazsın.

### 206 · PASS · Öğretmen

- Soru: Teslim edilen ödeve puan vermek istiyorum
- Beklenen intent: `homework_grade`
- Gerçek intent: `homework_grade`
- response_id: `homework_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ödevi verdiğin (yönettiğin) ders. 1) **Ödevler** (`/homework`) → ödevin detayı → **Teslimler**. 2) Bir öğrencinin teslimini aç, **Notlandır** ile not/geri bildirim ver; gerekirse **Notu kaldır** ile geri al. Notlandırma Öğretmen ve üstüne açıktır; kendi teslimini notlandıramazsın.

### 207 · PASS · Öğrenci

- Soru: Ücret ödemelerimi nerede takip ederim?
- Beklenen intent: `fees_info`
- Gerçek intent: `fees_info`
- response_id: `fees_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ücretler", "route": "/payments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kendi okul ücret ve ödeme ekstreni **Ücretlerim** (`/payments`) sayfasından görürsün. Öğrencide kendi borç/ödeme durumu, Velide bağlı çocuğu seçerek salt-okunur ekstre görünür. Okulun tahsilat yönetimi ise ayrı `/management/payments` sayfasıdır.

### 208 · PASS · Öğrenci

- Soru: Okul ücreti hangi sayfada?
- Beklenen intent: `fees_info`
- Gerçek intent: `fees_info`
- response_id: `fees_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ücretler", "route": "/payments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kendi okul ücret ve ödeme ekstreni **Ücretlerim** (`/payments`) sayfasından görürsün. Öğrencide kendi borç/ödeme durumu, Velide bağlı çocuğu seçerek salt-okunur ekstre görünür. Okulun tahsilat yönetimi ise ayrı `/management/payments` sayfasıdır.

### 209 · PASS · Öğrenci

- Soru: Ödeme durumumu nereden görürüm?
- Beklenen intent: `fees_info`
- Gerçek intent: `fees_info`
- response_id: `fees_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ücretler", "route": "/payments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kendi okul ücret ve ödeme ekstreni **Ücretlerim** (`/payments`) sayfasından görürsün. Öğrencide kendi borç/ödeme durumu, Velide bağlı çocuğu seçerek salt-okunur ekstre görünür. Okulun tahsilat yönetimi ise ayrı `/management/payments` sayfasıdır.

### 210 · PASS · Öğrenci

- Soru: Şube bilgimi nereden öğrenirim?
- Beklenen intent: `profile_view`
- Gerçek intent: `profile_view`
- response_id: `profile_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kendi profilini `/profile/me` adresinden veya hesap menüsündeki **Profilim** seçeneğinden açabilirsin. Burada profil fotoğrafın, görünen adın/Hakkında alanın, rolün, şube ve ders üyeliklerin, rozetlerin ile odak saati, odak oturumu, teslim edilen/zamanında ödev ve girilen sınav istatistiklerin görünür. Kendi sayfanda **Profili düzenle** düğmesi vardır. Başka bir kişinin profili `/profile/$userId` ile açılır; erişim kapsamını backend denetler ve Veli yalnız kendisini veya bağlı çocuklarını görebilir.

### 211 · PASS · Öğrenci

- Soru: Okulun şubeleri hangi sayfada?
- Beklenen intent: `branches_info`
- Gerçek intent: `branches_info`
- response_id: `branches_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 212 · PASS · Öğrenci

- Soru: Şube listesi nerede?
- Beklenen intent: `branches_info`
- Gerçek intent: `branches_info`
- response_id: `branches_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 213 · PASS · Öğrenci

- Soru: Takvimi nereden açarım?
- Beklenen intent: `calendar_info`
- Gerçek intent: `calendar_info`
- response_id: `calendar_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Takvim", "route": "/calendar"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Takvim** (`/calendar`) aylık görünümde sınav, ödev, etkinlik, randevu ve ders oturumlarını birleştirir. **Bugün** düğmesiyle geçerli aya/güne dönebilir, bir günü seçerek o günün ayrıntılarını görebilirsin.

### 214 · PASS · Öğrenci

- Soru: Haftalık programım nerede görünür?
- Beklenen intent: `calendar_info`
- Gerçek intent: `calendar_info`
- response_id: `calendar_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Takvim", "route": "/calendar"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Takvim** (`/calendar`) aylık görünümde sınav, ödev, etkinlik, randevu ve ders oturumlarını birleştirir. **Bugün** düğmesiyle geçerli aya/güne dönebilir, bir günü seçerek o günün ayrıntılarını görebilirsin.

### 215 · PASS · Öğrenci

- Soru: Ders programını nasıl görürüm?
- Beklenen intent: `calendar_info`
- Gerçek intent: `calendar_info`
- response_id: `calendar_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Takvim", "route": "/calendar"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Takvim** (`/calendar`) aylık görünümde sınav, ödev, etkinlik, randevu ve ders oturumlarını birleştirir. **Bugün** düğmesiyle geçerli aya/güne dönebilir, bir günü seçerek o günün ayrıntılarını görebilirsin.

### 216 · PASS · Öğrenci

- Soru: Ana panel neyi gösterir?
- Beklenen intent: `today_info`
- Gerçek intent: `today_info`
- response_id: `today_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ana sayfa", "route": "/"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Bugün** panelinde günün özeti bir arada görünür: yaklaşan sınavlar, ödevler ve etkinlikler tek ekranda listelenir.

### 217 · PASS · Öğrenci

- Soru: Bugün paneli neleri listeler?
- Beklenen intent: `today_info`
- Gerçek intent: `today_info`
- response_id: `today_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ana sayfa", "route": "/"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Bugün** panelinde günün özeti bir arada görünür: yaklaşan sınavlar, ödevler ve etkinlikler tek ekranda listelenir.

### 218 · PASS · Öğrenci

- Soru: Ana paneldeki özet nedir?
- Beklenen intent: `today_info`
- Gerçek intent: `today_info`
- response_id: `today_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ana sayfa", "route": "/"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Bugün** panelinde günün özeti bir arada görünür: yaklaşan sınavlar, ödevler ve etkinlikler tek ekranda listelenir.

### 219 · PASS · Öğretmen

- Soru: Soru bankasına nasıl ulaşırım?
- Beklenen intent: `question_bank_info`
- Gerçek intent: `question_bank_info`
- response_id: `question_bank_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru bankası", "route": "/question-bank"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Soru bankası**, öğretmenlerin hazır soru şablonlarını saklayıp sınavlara eklediği depodur; tekrar kullanılabilir sorular burada tutulur.

### 220 · PASS · Öğretmen

- Soru: Soru bankası ne demek?
- Beklenen intent: `question_bank_info`
- Gerçek intent: `question_bank_info`
- response_id: `question_bank_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru bankası", "route": "/question-bank"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Soru bankası**, öğretmenlerin hazır soru şablonlarını saklayıp sınavlara eklediği depodur; tekrar kullanılabilir sorular burada tutulur.

### 221 · PASS · Öğretmen

- Soru: Soru bankası hangi sayfada?
- Beklenen intent: `question_bank_info`
- Gerçek intent: `question_bank_info`
- response_id: `question_bank_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru bankası", "route": "/question-bank"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Soru bankası**, öğretmenlerin hazır soru şablonlarını saklayıp sınavlara eklediği depodur; tekrar kullanılabilir sorular burada tutulur.

### 222 · PASS · Öğrenci

- Soru: Bildirimleri nereden yönetirim?
- Beklenen intent: `notification_settings_info`
- Gerçek intent: `notification_settings_info`
- response_id: `notification_settings_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Şu an bildirimleri olay türüne göre açıp kapatan veya ses/e-posta tercihi sunan ayrı bir ayar ekranı yok. Üst bardaki **zil** simgesi Bildirim Merkezi'ni açar; mesaj, etkinlik, sınav ve ödev bildirimlerini burada görürsün. Bir bildirimi **× / Sil** ile kapatabilir ya da **Tümünü sil** ile listeyi temizleyebilirsin. Bildirime basmak ilgili sayfayı açar; mesaj bildirimi ayrıca okundu olarak işaretlenir.

### 223 · PASS · Öğrenci

- Soru: Bildirim tercihlerimi değiştirmek istiyorum
- Beklenen intent: `notification_settings_info`
- Gerçek intent: `notification_settings_info`
- response_id: `notification_settings_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Şu an bildirimleri olay türüne göre açıp kapatan veya ses/e-posta tercihi sunan ayrı bir ayar ekranı yok. Üst bardaki **zil** simgesi Bildirim Merkezi'ni açar; mesaj, etkinlik, sınav ve ödev bildirimlerini burada görürsün. Bir bildirimi **× / Sil** ile kapatabilir ya da **Tümünü sil** ile listeyi temizleyebilirsin. Bildirime basmak ilgili sayfayı açar; mesaj bildirimi ayrıca okundu olarak işaretlenir.

### 224 · PASS · Öğrenci

- Soru: Bildirim sesini nasıl kapatırım?
- Beklenen intent: `notification_settings_info`
- Gerçek intent: `notification_settings_info`
- response_id: `notification_settings_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Şu an bildirimleri olay türüne göre açıp kapatan veya ses/e-posta tercihi sunan ayrı bir ayar ekranı yok. Üst bardaki **zil** simgesi Bildirim Merkezi'ni açar; mesaj, etkinlik, sınav ve ödev bildirimlerini burada görürsün. Bir bildirimi **× / Sil** ile kapatabilir ya da **Tümünü sil** ile listeyi temizleyebilirsin. Bildirime basmak ilgili sayfayı açar; mesaj bildirimi ayrıca okundu olarak işaretlenir.

### 225 · PASS · Yönetici

- Soru: Yönetim menüsünde ne var?
- Beklenen intent: `nav_overview`
- Gerçek intent: `nav_overview`
- response_id: `nav_overview_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Sol menüde rolüne göre şu gruplar görünür: **Dersler** (Dersler, Ödevler, Sınavlar, Soru bankası, öğrencide Karnem); **Planlama** (Etkinlikler, Takvim, Randevular); **Çalışma alanı** (Defter, Beyaz tahtalar, öğrencide Pomodoro, personelde Mesai); **Öğrenciler** (Çocuklarım veya Şubeler, Öğrenci notları/yoklaması/pomodoroları); **Hizmetler** (Yemekler, uygun rolde Ücretler); **Topluluk** (Mesajlar, Soru havuzu); **Okul** (Personel mesai, okul ayarları, dönemler, ödemeler ve ADMIN'de Kullanıcılar). **Profilim**, kişisel **Ayarlar** ve **Rehber** hesap menüsündedir; yetkin olmayan öğeler gizlenir.

### 226 · PASS · Yönetici

- Soru: Akademik altında hangi sayfalar var?
- Beklenen intent: `nav_overview`
- Gerçek intent: `nav_overview`
- response_id: `section_overview`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Akademik** bölümünde şunlar var:
> - **Eğitim (dersler/etüt/kulüp)** (`/courses`)
> - **Ödevler** (`/homework`)
> - **Sınavlar** (`/exams`)
> - **Soru bankası** (`/question-bank`) _öğretmen+_
> - **Karnem** (`/marks`) _öğrenci_
>
> Rolüne göre bazı öğeler menüde görünmeyebilir. Hangisini merak ediyorsan 'nasıl yaparım?' diye sorabilirsin.

### 227 · PASS · Yönetici

- Soru: ADMIN bölümünde neler var?
- Beklenen intent: `nav_overview`
- Gerçek intent: `nav_overview`
- response_id: `nav_overview_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Sol menüde rolüne göre şu gruplar görünür: **Dersler** (Dersler, Ödevler, Sınavlar, Soru bankası, öğrencide Karnem); **Planlama** (Etkinlikler, Takvim, Randevular); **Çalışma alanı** (Defter, Beyaz tahtalar, öğrencide Pomodoro, personelde Mesai); **Öğrenciler** (Çocuklarım veya Şubeler, Öğrenci notları/yoklaması/pomodoroları); **Hizmetler** (Yemekler, uygun rolde Ücretler); **Topluluk** (Mesajlar, Soru havuzu); **Okul** (Personel mesai, okul ayarları, dönemler, ödemeler ve ADMIN'de Kullanıcılar). **Profilim**, kişisel **Ayarlar** ve **Rehber** hesap menüsündedir; yetkin olmayan öğeler gizlenir.

### 228 · PASS · Öğrenci

- Soru: Etkinlik listesi nerede?
- Beklenen intent: `event_view`
- Gerçek intent: `event_view`
- response_id: `event_view_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Etkinlikler", "route": "/events"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Okuldaki **etkinlikleri** menüdeki **Etkinlikler** (`/events`) sayfasından görürsün. Backend oturumlu kullanıcıya yalnız kendi katılacağı etkinlikleri değil, okulun etkinlik listesini döndürür; audience alanı beklenen katılımcıyı belirtir, görünürlük filtresi değildir.

### 229 · PASS · Öğrenci

- Soru: Yaklaşan etkinlikleri nereden görürüm?
- Beklenen intent: `event_view`
- Gerçek intent: `event_view`
- response_id: `event_view_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Etkinlikler", "route": "/events"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Okuldaki **etkinlikleri** menüdeki **Etkinlikler** (`/events`) sayfasından görürsün. Backend oturumlu kullanıcıya yalnız kendi katılacağı etkinlikleri değil, okulun etkinlik listesini döndürür; audience alanı beklenen katılımcıyı belirtir, görünürlük filtresi değildir.

### 230 · PASS · Öğrenci

- Soru: Etkinlik listemi görmek istiyorum
- Beklenen intent: `event_view`
- Gerçek intent: `event_view`
- response_id: `event_view_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Etkinlikler", "route": "/events"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Okuldaki **etkinlikleri** menüdeki **Etkinlikler** (`/events`) sayfasından görürsün. Backend oturumlu kullanıcıya yalnız kendi katılacağı etkinlikleri değil, okulun etkinlik listesini döndürür; audience alanı beklenen katılımcıyı belirtir, görünürlük filtresi değildir.

### 231 · PASS · Öğrenci

- Soru: Sınav takvimi hangi sayfada?
- Beklenen intent: `exam_schedule_info`
- Gerçek intent: `exam_schedule_info`
- response_id: `exam_schedule_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Sınav** takvimini ve **tarih**lerini **Sınavlar** (`/exams`) sayfasından görürsün; yaklaşan sınavların tarihleri burada listelenir.

### 232 · PASS · Öğrenci

- Soru: Sınav tarihlerini nereden görürüm?
- Beklenen intent: `exam_schedule_info`
- Gerçek intent: `exam_schedule_info`
- response_id: `exam_schedule_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Sınav** takvimini ve **tarih**lerini **Sınavlar** (`/exams`) sayfasından görürsün; yaklaşan sınavların tarihleri burada listelenir.

### 233 · PASS · Öğrenci

- Soru: Yaklaşan sınavların tarihi nerede?
- Beklenen intent: `exam_schedule_info`
- Gerçek intent: `exam_schedule_info`
- response_id: `exam_schedule_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Sınav** takvimini ve **tarih**lerini **Sınavlar** (`/exams`) sayfasından görürsün; yaklaşan sınavların tarihleri burada listelenir.

### 234 · PASS · Öğrenci

- Soru: Ders dosyaları hangi sayfada?
- Beklenen intent: `course_materials_info`
- Gerçek intent: `course_materials_info`
- response_id: `course_materials_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Öğretmenin yüklediği **ders notları** ve **PDF/dosya**lar ilgili dersin sayfasındadır: **Dersler** (`/courses`) → ders → Ders notları.

### 235 · PASS · Öğrenci

- Soru: Öğretmenin PDF dosyaları nerede?
- Beklenen intent: `course_materials_info`
- Gerçek intent: `course_materials_info`
- response_id: `course_materials_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Öğretmenin yüklediği **ders notları** ve **PDF/dosya**lar ilgili dersin sayfasındadır: **Dersler** (`/courses`) → ders → Ders notları.

### 236 · PASS · Öğrenci

- Soru: Ders notu dosyalarını nereden indiririm?
- Beklenen intent: `course_materials_info`
- Gerçek intent: `course_materials_info`
- response_id: `course_materials_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Öğretmenin yüklediği **ders notları** ve **PDF/dosya**lar ilgili dersin sayfasındadır: **Dersler** (`/courses`) → ders → Ders notları.

### 237 · PASS · Öğrenci

- Soru: Nasıl randevu alabilirim
- Beklenen intent: `appointment_book`
- Gerçek intent: `appointment_book`
- response_id: `appointment_book_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Randevu almak için **Planlama** grubundaki **Randevular** (`/appointments`) sayfasına git. **Öğretmenlerin açık saatleri** bölümünden uygun saati seç, **Randevu al**'a bas. Talebin **Randevularım** altında görünür ve öğretmen onayına düşer. Randevu alma yalnızca Öğrenci ve Veli'ye açıktır. Veli randevuyu çocuğu adına değil kendi requester hesabıyla alır. Slot başlamış/doluysa, aynı saatte başka randevun varsa veya öğretmen artık uygun rolde değilse 409 alırsın. İptali yalnız talebi açan kullanıcı yapar; öğretmenin önerdiği yeni saati **Kabul et/Reddet** ile yanıtlayabilirsin.

### 238 · PASS · Veli

- Soru: Randevu almak için ne yapmalıyım
- Beklenen intent: `appointment_book`
- Gerçek intent: `appointment_book`
- response_id: `appointment_book_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Randevu almak için **Planlama** grubundaki **Randevular** (`/appointments`) sayfasına git. **Öğretmenlerin açık saatleri** bölümünden uygun saati seç, **Randevu al**'a bas. Talebin **Randevularım** altında görünür ve öğretmen onayına düşer. Randevu alma yalnızca Öğrenci ve Veli'ye açıktır. Veli randevuyu çocuğu adına değil kendi requester hesabıyla alır. Slot başlamış/doluysa, aynı saatte başka randevun varsa veya öğretmen artık uygun rolde değilse 409 alırsın. İptali yalnız talebi açan kullanıcı yapar; öğretmenin önerdiği yeni saati **Kabul et/Reddet** ile yanıtlayabilirsin.

### 239 · PASS · Öğrenci

- Soru: Yeni bir randevu talebi oluşturayım
- Beklenen intent: `appointment_book`
- Gerçek intent: `appointment_book`
- response_id: `appointment_book_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Randevu almak için **Planlama** grubundaki **Randevular** (`/appointments`) sayfasına git. **Öğretmenlerin açık saatleri** bölümünden uygun saati seç, **Randevu al**'a bas. Talebin **Randevularım** altında görünür ve öğretmen onayına düşer. Randevu alma yalnızca Öğrenci ve Veli'ye açıktır. Veli randevuyu çocuğu adına değil kendi requester hesabıyla alır. Slot başlamış/doluysa, aynı saatte başka randevun varsa veya öğretmen artık uygun rolde değilse 409 alırsın. İptali yalnız talebi açan kullanıcı yapar; öğretmenin önerdiği yeni saati **Kabul et/Reddet** ile yanıtlayabilirsin.

### 240 · PASS · Öğretmen

- Soru: Öğrencilere randevu saatleri açmak istiyorum
- Beklenen intent: `appointment_slot_open`
- Gerçek intent: `appointment_slot_open`
- response_id: `appointment_slot_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Randevular** (`/appointments`) → **Açtığım saatler** bölümünde **Saat aç** (veya **Yeni saat**) ile müsait randevu saati yayınla. Öğrenci ve veliler bu saatlerden randevu talep eder; gelen talepleri **Randevu talepleri**'nden yönetirsin. Pending veya onaylı randevusu bulunan tekil saat/tekrarlı seri silinemez; önce talebin durumunu çözmelisin.

### 241 · PASS · Öğretmen

- Soru: Müsait saatlerimi nasıl yayınlarım
- Beklenen intent: `appointment_slot_open`
- Gerçek intent: `appointment_slot_open`
- response_id: `appointment_slot_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Randevular** (`/appointments`) → **Açtığım saatler** bölümünde **Saat aç** (veya **Yeni saat**) ile müsait randevu saati yayınla. Öğrenci ve veliler bu saatlerden randevu talep eder; gelen talepleri **Randevu talepleri**'nden yönetirsin. Pending veya onaylı randevusu bulunan tekil saat/tekrarlı seri silinemez; önce talebin durumunu çözmelisin.

### 242 · PASS · Öğretmen

- Soru: Randevu için boş saat eklemek istiyorum
- Beklenen intent: `appointment_slot_open`
- Gerçek intent: `appointment_slot_open`
- response_id: `appointment_slot_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Randevular** (`/appointments`) → **Açtığım saatler** bölümünde **Saat aç** (veya **Yeni saat**) ile müsait randevu saati yayınla. Öğrenci ve veliler bu saatlerden randevu talep eder; gelen talepleri **Randevu talepleri**'nden yönetirsin. Pending veya onaylı randevusu bulunan tekil saat/tekrarlı seri silinemez; önce talebin durumunu çözmelisin.

### 243 · PASS · Öğretmen

- Soru: Gelen randevu taleplerini nasıl onaylarım
- Beklenen intent: `appointment_requests`
- Gerçek intent: `appointment_requests`
- response_id: `appointment_requests_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Randevular** (`/appointments`) → **Randevu talepleri** bölümünde gelen talepleri görürsün; her talepte **Onayla** ile kabul et (gerekirse reddet) veya **Başka saat öner**. Onaylanan randevu, ilgili öğrenci/velinin **Randevularım**'ında görünür. Karşı saati requester kabul/reddeder; eski ya da artık geçerli olmayan teklife basmak 409 verir. Öğretmen/Yönetici randevuyu requester adına iptal edemez.

### 244 · PASS · Öğretmen

- Soru: Randevu isteklerini nereden yönetirim
- Beklenen intent: `appointment_requests`
- Gerçek intent: `appointment_requests`
- response_id: `appointment_requests_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Randevular** (`/appointments`) → **Randevu talepleri** bölümünde gelen talepleri görürsün; her talepte **Onayla** ile kabul et (gerekirse reddet) veya **Başka saat öner**. Onaylanan randevu, ilgili öğrenci/velinin **Randevularım**'ında görünür. Karşı saati requester kabul/reddeder; eski ya da artık geçerli olmayan teklife basmak 409 verir. Öğretmen/Yönetici randevuyu requester adına iptal edemez.

### 245 · PASS · Öğretmen

- Soru: Bir randevu talebini kabul etmek istiyorum
- Beklenen intent: `appointment_requests`
- Gerçek intent: `appointment_requests`
- response_id: `appointment_requests_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Randevular** (`/appointments`) → **Randevu talepleri** bölümünde gelen talepleri görürsün; her talepte **Onayla** ile kabul et (gerekirse reddet) veya **Başka saat öner**. Onaylanan randevu, ilgili öğrenci/velinin **Randevularım**'ında görünür. Karşı saati requester kabul/reddeder; eski ya da artık geçerli olmayan teklife basmak 409 verir. Öğretmen/Yönetici randevuyu requester adına iptal edemez.

### 246 · PASS · Öğrenci

- Soru: Yemek menüsünü nereden görebilirim
- Beklenen intent: `meal_view`
- Gerçek intent: `meal_view`
- response_id: `meal_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yemek menülerini **Okul hizmetleri** grubundaki **Yemekler** (`/meals`) sayfasından görürsün. Günün **Menü** ve **Öğün**lerini, rezervasyon durumunu (**Rezerve edildi** / **Rezervasyon yok**) görebilirsin. Detay için menü kartına bas (`/meals/$id`).

### 247 · PASS · Veli

- Soru: Öğün menüsünü görmek istiyorum
- Beklenen intent: `meal_view`
- Gerçek intent: `meal_view`
- response_id: `meal_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yemek menülerini **Okul hizmetleri** grubundaki **Yemekler** (`/meals`) sayfasından görürsün. Günün **Menü** ve **Öğün**lerini, rezervasyon durumunu (**Rezerve edildi** / **Rezervasyon yok**) görebilirsin. Detay için menü kartına bas (`/meals/$id`).

### 248 · PASS · Öğrenci

- Soru: Haftalık yemek listesi nerede
- Beklenen intent: `meal_view`
- Gerçek intent: `meal_view`
- response_id: `meal_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yemek menülerini **Okul hizmetleri** grubundaki **Yemekler** (`/meals`) sayfasından görürsün. Günün **Menü** ve **Öğün**lerini, rezervasyon durumunu (**Rezerve edildi** / **Rezervasyon yok**) görebilirsin. Detay için menü kartına bas (`/meals/$id`).

### 249 · PASS · Öğrenci

- Soru: Öğle yemeği için yer ayırmak istiyorum
- Beklenen intent: `meal_book`
- Gerçek intent: `meal_book`
- response_id: `meal_book_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yemek için yer ayırmak üzere **Yemekler** (`/meals`) → ilgili menü/öğüne gir, **Yer ayır**'a bas. Rezervasyonun **Rezerve edildi** olarak görünür; **Rezervasyonu iptal et** ile geri alabilirsin. Yer ayırma Öğrenci (kendisi) ve Veli'ye (bağlı çocuğu) açıktır. Geçmiş tarih, iptal eşiği, doluluk, yeniden-rezervasyon tavanı veya eşzamanlı değişiklik 409 üretebilir; sayfayı yenileyip güncel kapasite ve son saati kontrol et.

### 250 · PASS · Veli

- Soru: Menüden yemek rezerve etmek istiyorum
- Beklenen intent: `meal_book`
- Gerçek intent: `meal_book`
- response_id: `meal_book_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yemek için yer ayırmak üzere **Yemekler** (`/meals`) → ilgili menü/öğüne gir, **Yer ayır**'a bas. Rezervasyonun **Rezerve edildi** olarak görünür; **Rezervasyonu iptal et** ile geri alabilirsin. Yer ayırma Öğrenci (kendisi) ve Veli'ye (bağlı çocuğu) açıktır. Geçmiş tarih, iptal eşiği, doluluk, yeniden-rezervasyon tavanı veya eşzamanlı değişiklik 409 üretebilir; sayfayı yenileyip güncel kapasite ve son saati kontrol et.

### 251 · PASS · Öğrenci

- Soru: Öğün için yer ayırtmak istiyorum
- Beklenen intent: `meal_book`
- Gerçek intent: `meal_book`
- response_id: `meal_book_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yemek için yer ayırmak üzere **Yemekler** (`/meals`) → ilgili menü/öğüne gir, **Yer ayır**'a bas. Rezervasyonun **Rezerve edildi** olarak görünür; **Rezervasyonu iptal et** ile geri alabilirsin. Yer ayırma Öğrenci (kendisi) ve Veli'ye (bağlı çocuğu) açıktır. Geçmiş tarih, iptal eşiği, doluluk, yeniden-rezervasyon tavanı veya eşzamanlı değişiklik 409 üretebilir; sayfayı yenileyip güncel kapasite ve son saati kontrol et.

### 252 · PASS · Yönetici

- Soru: Yeni yemek menüsü yayınlamak istiyorum
- Beklenen intent: `meal_menu_manage`
- Gerçek intent: `meal_menu_manage`
- response_id: `meal_menu_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Yemekler** (`/meals`) → **Menü yayınla** ile yeni menü/öğün oluştur, **Yemek ekle** ile öğüne yemek ekle; menü ve yemek içeriği yönetimi Yönetici+ içindir. Öğrencinin güvenlik kaydı olan **Beslenme profili** ayrı bir işlemdir; **Kredi kaydetme** ise yalnız ADMIN hesabında görünür.

### 253 · PASS · Yönetici

- Soru: Öğüne yeni yemek eklemek istiyorum
- Beklenen intent: `meal_menu_manage`
- Gerçek intent: `meal_menu_manage`
- response_id: `meal_menu_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Yemekler** (`/meals`) → **Menü yayınla** ile yeni menü/öğün oluştur, **Yemek ekle** ile öğüne yemek ekle; menü ve yemek içeriği yönetimi Yönetici+ içindir. Öğrencinin güvenlik kaydı olan **Beslenme profili** ayrı bir işlemdir; **Kredi kaydetme** ise yalnız ADMIN hesabında görünür.

### 254 · PASS · Yönetici

- Soru: Öğrenci yemek kredisi girmek istiyorum
- Beklenen intent: `meal_credit_manage`
- Gerçek intent: `meal_credit_manage`
- response_id: `meal_credit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 255 · PASS · Öğrenci

- Soru: Soru havuzunda soru sormak istiyorum
- Beklenen intent: `question_ask`
- Gerçek intent: `question_ask`
- response_id: `question_ask_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru havuzu", "route": "/questions"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Topluluk** grubundaki **Soru havuzu** (`/questions`) sayfasına git. **Soru sor**'a bas; **Konu**, **Soru detayı** ve isteğe bağlı **Görsel** ekleyip gönder. Sorun önce **Bekliyor** durumundadır; bir öğretmen onaylayınca **Onaylandı** olur ve havuza erişebilen Öğrenci/Öğretmen/Yönetici/ADMIN hesaplarına görünür. Yeni soru sorma yalnız exact **Öğrenci** rolündedir; personel soru çözebilir/modere edebilir ama öğrenci adına yeni soru soramaz. Veli soru havuzuna erişemez.

### 256 · PASS · Öğrenci

- Soru: Takıldığım soruyu havuza nasıl sorarım
- Beklenen intent: `question_ask`
- Gerçek intent: `question_ask`
- response_id: `question_ask_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru havuzu", "route": "/questions"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Topluluk** grubundaki **Soru havuzu** (`/questions`) sayfasına git. **Soru sor**'a bas; **Konu**, **Soru detayı** ve isteğe bağlı **Görsel** ekleyip gönder. Sorun önce **Bekliyor** durumundadır; bir öğretmen onaylayınca **Onaylandı** olur ve havuza erişebilen Öğrenci/Öğretmen/Yönetici/ADMIN hesaplarına görünür. Yeni soru sorma yalnız exact **Öğrenci** rolündedir; personel soru çözebilir/modere edebilir ama öğrenci adına yeni soru soramaz. Veli soru havuzuna erişemez.

### 257 · PASS · Öğrenci

- Soru: Soru havuzuna soru göndermek istiyorum
- Beklenen intent: `question_ask`
- Gerçek intent: `question_ask`
- response_id: `question_ask_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru havuzu", "route": "/questions"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Topluluk** grubundaki **Soru havuzu** (`/questions`) sayfasına git. **Soru sor**'a bas; **Konu**, **Soru detayı** ve isteğe bağlı **Görsel** ekleyip gönder. Sorun önce **Bekliyor** durumundadır; bir öğretmen onaylayınca **Onaylandı** olur ve havuza erişebilen Öğrenci/Öğretmen/Yönetici/ADMIN hesaplarına görünür. Yeni soru sorma yalnız exact **Öğrenci** rolündedir; personel soru çözebilir/modere edebilir ama öğrenci adına yeni soru soramaz. Veli soru havuzuna erişemez.

### 258 · PASS · Öğrenci

- Soru: Zor bir soruya çözüm göndermek istiyorum
- Beklenen intent: `question_solve`
- Gerçek intent: `question_solve`
- response_id: `question_solve_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru havuzu", "route": "/questions"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Bir soruya çözüm göndermek için **Soru havuzu** (`/questions`) → soruyu aç (`/questions/$id`) → **Çözümler** bölümünde **Çözüm gönder** ile çözümünü yaz ve paylaş. Çözüm gönderme Öğrenci ve üstüne açıktır.

### 259 · PASS · Öğrenci

- Soru: Bir soruya çözüm önerisi yapmak istiyorum
- Beklenen intent: `question_solve`
- Gerçek intent: `question_solve`
- response_id: `question_solve_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru havuzu", "route": "/questions"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Bir soruya çözüm göndermek için **Soru havuzu** (`/questions`) → soruyu aç (`/questions/$id`) → **Çözümler** bölümünde **Çözüm gönder** ile çözümünü yaz ve paylaş. Çözüm gönderme Öğrenci ve üstüne açıktır.

### 260 · PASS · Öğrenci

- Soru: Havuzdaki soruyu çözmek istiyorum
- Beklenen intent: `question_solve`
- Gerçek intent: `question_solve`
- response_id: `question_solve_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru havuzu", "route": "/questions"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Bir soruya çözüm göndermek için **Soru havuzu** (`/questions`) → soruyu aç (`/questions/$id`) → **Çözümler** bölümünde **Çözüm gönder** ile çözümünü yaz ve paylaş. Çözüm gönderme Öğrenci ve üstüne açıktır.

### 261 · PASS · Öğretmen

- Soru: Bekleyen havuz sorularını onaylayayım
- Beklenen intent: `question_approve`
- Gerçek intent: `question_approve`
- response_id: `question_approve_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru havuzu", "route": "/questions"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Soru havuzu** (`/questions`) → soru detayında **Onayla** ile bekleyen soruyu yayınla, gerekirse **Reddet**. Onaylanan soru **Onaylandı** olur ve havuza erişen rollere görünür. **Reddet**, soru kaydıyla birlikte çözümleri ve görselleri kalıcı olarak siler; onaylamadan önce içeriği kontrol et. Moderasyon Öğretmen ve üstüne açıktır.

### 262 · PASS · Öğretmen

- Soru: Öğrenci sorularını nasıl onaylarım
- Beklenen intent: `question_approve`
- Gerçek intent: `question_approve`
- response_id: `question_approve_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru havuzu", "route": "/questions"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Soru havuzu** (`/questions`) → soru detayında **Onayla** ile bekleyen soruyu yayınla, gerekirse **Reddet**. Onaylanan soru **Onaylandı** olur ve havuza erişen rollere görünür. **Reddet**, soru kaydıyla birlikte çözümleri ve görselleri kalıcı olarak siler; onaylamadan önce içeriği kontrol et. Moderasyon Öğretmen ve üstüne açıktır.

### 263 · PASS · Öğretmen

- Soru: Havuzdaki bir soruyu reddetmek istiyorum
- Beklenen intent: `question_approve`
- Gerçek intent: `question_approve`
- response_id: `question_approve_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru havuzu", "route": "/questions"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Soru havuzu** (`/questions`) → soru detayında **Onayla** ile bekleyen soruyu yayınla, gerekirse **Reddet**. Onaylanan soru **Onaylandı** olur ve havuza erişen rollere görünür. **Reddet**, soru kaydıyla birlikte çözümleri ve görselleri kalıcı olarak siler; onaylamadan önce içeriği kontrol et. Moderasyon Öğretmen ve üstüne açıktır.

### 264 · PASS · Öğrenci

- Soru: Beyaz tahta listesini nereden görürüm
- Beklenen intent: `board_view`
- Gerçek intent: `board_view`
- response_id: `board_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Beyaz tahtalar", "route": "/whiteboards"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Beyaz tahtaları **Çalışma alanı** grubundaki **Beyaz tahtalar** (`/whiteboards`) sayfasından görürsün. Bir tahtayı açmak için kartında **Aç**'a bas (`/whiteboards/$id`); katılımcılar eşzamanlı çizer. Beyaz tahtalar Öğrenci ve üstüne açıktır (Veli hariç).

### 265 · PASS · Öğrenci

- Soru: Bir tahtayı nasıl açarım
- Beklenen intent: `board_view`
- Gerçek intent: `board_view`
- response_id: `board_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Beyaz tahtalar", "route": "/whiteboards"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Beyaz tahtaları **Çalışma alanı** grubundaki **Beyaz tahtalar** (`/whiteboards`) sayfasından görürsün. Bir tahtayı açmak için kartında **Aç**'a bas (`/whiteboards/$id`); katılımcılar eşzamanlı çizer. Beyaz tahtalar Öğrenci ve üstüne açıktır (Veli hariç).

### 266 · PASS · Öğretmen

- Soru: Var olan tahtaları nasıl görürüm
- Beklenen intent: `board_view`
- Gerçek intent: `board_view`
- response_id: `board_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Beyaz tahtalar", "route": "/whiteboards"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Beyaz tahtaları **Çalışma alanı** grubundaki **Beyaz tahtalar** (`/whiteboards`) sayfasından görürsün. Bir tahtayı açmak için kartında **Aç**'a bas (`/whiteboards/$id`); katılımcılar eşzamanlı çizer. Beyaz tahtalar Öğrenci ve üstüne açıktır (Veli hariç).

### 267 · PASS · Öğrenci

- Soru: Beyaz tahta oluşturmak istiyorum
- Beklenen intent: `board_create`
- Gerçek intent: `board_create`
- response_id: `board_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Beyaz tahtalar", "route": "/whiteboards"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yeni beyaz tahta için **Beyaz tahtalar** (`/whiteboards`) → **Yeni tahta** ile **Başlık** gir, isteğe bağlı **Katılımcılar** ekle, oluştur. Tahta içinde **Kilitle/Kilidi aç**, **Temizle**, **Tahtayı kapat** ve silme kontrolleri yalnız oluşturucudadır; kapatma kalıcı salt-okunur durumdur ve yeniden açma yoktur. Boş/kilitli/kapalı tahtayı temizleme 409 verebilir. Öğretmen+ **Toplu davet** ile sınıf, ders veya etkinlik katılımcısı çağırabilir; kapasite aşılırsa toplu ekleme bütünüyle reddedilir. Tahtayı silmek çizim geçmişini de kalıcı siler.

### 268 · PASS · Öğrenci

- Soru: Yeni bir çizim tahtası oluşturayım
- Beklenen intent: `board_create`
- Gerçek intent: `board_create`
- response_id: `board_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Beyaz tahtalar", "route": "/whiteboards"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yeni beyaz tahta için **Beyaz tahtalar** (`/whiteboards`) → **Yeni tahta** ile **Başlık** gir, isteğe bağlı **Katılımcılar** ekle, oluştur. Tahta içinde **Kilitle/Kilidi aç**, **Temizle**, **Tahtayı kapat** ve silme kontrolleri yalnız oluşturucudadır; kapatma kalıcı salt-okunur durumdur ve yeniden açma yoktur. Boş/kilitli/kapalı tahtayı temizleme 409 verebilir. Öğretmen+ **Toplu davet** ile sınıf, ders veya etkinlik katılımcısı çağırabilir; kapasite aşılırsa toplu ekleme bütünüyle reddedilir. Tahtayı silmek çizim geçmişini de kalıcı siler.

### 269 · PASS · Öğretmen

- Soru: Yeni beyaz tahta eklemek istiyorum
- Beklenen intent: `board_create`
- Gerçek intent: `board_create`
- response_id: `board_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Beyaz tahtalar", "route": "/whiteboards"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yeni beyaz tahta için **Beyaz tahtalar** (`/whiteboards`) → **Yeni tahta** ile **Başlık** gir, isteğe bağlı **Katılımcılar** ekle, oluştur. Tahta içinde **Kilitle/Kilidi aç**, **Temizle**, **Tahtayı kapat** ve silme kontrolleri yalnız oluşturucudadır; kapatma kalıcı salt-okunur durumdur ve yeniden açma yoktur. Boş/kilitli/kapalı tahtayı temizleme 409 verebilir. Öğretmen+ **Toplu davet** ile sınıf, ders veya etkinlik katılımcısı çağırabilir; kapasite aşılırsa toplu ekleme bütünüyle reddedilir. Tahtayı silmek çizim geçmişini de kalıcı siler.

### 270 · PASS · Yönetici

- Soru: Ödeme yönetimi nerede
- Beklenen intent: `fees_manage`
- Gerçek intent: `fees_manage`
- response_id: `fees_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödemeler", "route": "/management/payments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Ne:** **Ödemeler** (`/management/payments`, Yönetici+) okulun ücret ve ödeme kayıtlarını yönettiğin sayfadır (öğrencilerin borç/tahsilat durumu).
> **Nereden/nasıl:** `/management/payments`'ı aç; öğrenci/döneme göre süz, ödeme kaydını gör; tahsilat, iade veya ters kayıt işlemini ilgili satırdan yap. Defter satırları sonradan düzenlenip silinmez: düzeltmeler yeni refund/reversal satırı ekleyerek append-only tutulur.
> **Not:** Bu yönetim sayfasıdır; öğrenci/velinin kendi **Ödeme ekstresi** ayrı sayfadır (`/payments`).

### 271 · PASS · Yönetici

- Soru: Öğrenci ödemelerini nereden yönetirim
- Beklenen intent: `fees_manage`
- Gerçek intent: `fees_manage`
- response_id: `fees_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödemeler", "route": "/management/payments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Ne:** **Ödemeler** (`/management/payments`, Yönetici+) okulun ücret ve ödeme kayıtlarını yönettiğin sayfadır (öğrencilerin borç/tahsilat durumu).
> **Nereden/nasıl:** `/management/payments`'ı aç; öğrenci/döneme göre süz, ödeme kaydını gör; tahsilat, iade veya ters kayıt işlemini ilgili satırdan yap. Defter satırları sonradan düzenlenip silinmez: düzeltmeler yeni refund/reversal satırı ekleyerek append-only tutulur.
> **Not:** Bu yönetim sayfasıdır; öğrenci/velinin kendi **Ödeme ekstresi** ayrı sayfadır (`/payments`).

### 272 · PASS · ADMIN

- Soru: Ücret tahsilatını nereden takip ederim
- Beklenen intent: `fees_manage`
- Gerçek intent: `fees_manage`
- response_id: `fees_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödemeler", "route": "/management/payments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Ne:** **Ödemeler** (`/management/payments`, Yönetici+) okulun ücret ve ödeme kayıtlarını yönettiğin sayfadır (öğrencilerin borç/tahsilat durumu).
> **Nereden/nasıl:** `/management/payments`'ı aç; öğrenci/döneme göre süz, ödeme kaydını gör; tahsilat, iade veya ters kayıt işlemini ilgili satırdan yap. Defter satırları sonradan düzenlenip silinmez: düzeltmeler yeni refund/reversal satırı ekleyerek append-only tutulur.
> **Not:** Bu yönetim sayfasıdır; öğrenci/velinin kendi **Ödeme ekstresi** ayrı sayfadır (`/payments`).

### 273 · PASS · Öğrenci

- Soru: notu silmek istiyorum
- Beklenen intent: `note_delete`
- Gerçek intent: `note_delete`
- response_id: `note_delete_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu silmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Sil**'i seç. 3) Açılan onay penceresinde silme işlemini onayla. Yalnızca kendi Defter notlarını silebilirsin.

### 274 · PASS · Veli

- Soru: Not kartındaki kaydı kaldırabilir miyim?
- Beklenen intent: `note_delete`
- Gerçek intent: `note_delete`
- response_id: `note_delete_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu silmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Sil**'i seç. 3) Açılan onay penceresinde silme işlemini onayla. Yalnızca kendi Defter notlarını silebilirsin.

### 275 · PASS · Öğretmen

- Soru: Defterimdeki notlardan birini sileceğim
- Beklenen intent: `note_delete`
- Gerçek intent: `note_delete`
- response_id: `note_delete_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu silmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Sil**'i seç. 3) Açılan onay penceresinde silme işlemini onayla. Yalnızca kendi Defter notlarını silebilirsin.

### 276 · PASS · ADMIN

- Soru: Yanlış yazdığım notu kaldır
- Beklenen intent: `note_delete`
- Gerçek intent: `note_delete`
- response_id: `note_delete_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu silmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Sil**'i seç. 3) Açılan onay penceresinde silme işlemini onayla. Yalnızca kendi Defter notlarını silebilirsin.

### 277 · PASS · Öğrenci

- Soru: notu silebilirmiyim
- Beklenen intent: `note_delete`
- Gerçek intent: `note_delete`
- response_id: `note_delete_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu silmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Sil**'i seç. 3) Açılan onay penceresinde silme işlemini onayla. Yalnızca kendi Defter notlarını silebilirsin.

### 278 · PASS · Öğrenci

- Soru: not slmek istiyorum
- Beklenen intent: `note_delete`
- Gerçek intent: `note_delete`
- response_id: `note_delete_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu silmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Sil**'i seç. 3) Açılan onay penceresinde silme işlemini onayla. Yalnızca kendi Defter notlarını silebilirsin.

### 279 · PASS · Öğrenci

- Soru: defterdeki notu slemek
- Beklenen intent: `note_delete`
- Gerçek intent: `note_delete`
- response_id: `note_delete_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu silmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Sil**'i seç. 3) Açılan onay penceresinde silme işlemini onayla. Yalnızca kendi Defter notlarını silebilirsin.

### 280 · PASS · Öğrenci

- Soru: notu kaldır
- Beklenen intent: `note_delete`
- Gerçek intent: `note_delete`
- response_id: `note_delete_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu silmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Sil**'i seç. 3) Açılan onay penceresinde silme işlemini onayla. Yalnızca kendi Defter notlarını silebilirsin.

### 281 · PASS · Öğrenci

- Soru: eski defter notunu temizlemek istiyorum
- Beklenen intent: `note_delete`
- Gerçek intent: `note_delete`
- response_id: `note_delete_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu silmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Sil**'i seç. 3) Açılan onay penceresinde silme işlemini onayla. Yalnızca kendi Defter notlarını silebilirsin.

### 282 · PASS · Öğrenci

- Soru: ben not değiştirmek
- Beklenen intent: `note_edit`
- Gerçek intent: `note_edit`
- response_id: `note_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu değiştirmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Düzenle**'yi seç. 3) Başlığı veya içeriği değiştirip **Güncelle**'ye bas ve onayla. Yalnızca kendi Defter notlarını düzenleyebilirsin.

### 283 · PASS · Öğrenci

- Soru: notu güncelle
- Beklenen intent: `note_edit`
- Gerçek intent: `note_edit`
- response_id: `note_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu değiştirmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Düzenle**'yi seç. 3) Başlığı veya içeriği değiştirip **Güncelle**'ye bas ve onayla. Yalnızca kendi Defter notlarını düzenleyebilirsin.

### 284 · PASS · Veli

- Soru: not başlığını değiştir
- Beklenen intent: `note_edit`
- Gerçek intent: `note_edit`
- response_id: `note_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu değiştirmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Düzenle**'yi seç. 3) Başlığı veya içeriği değiştirip **Güncelle**'ye bas ve onayla. Yalnızca kendi Defter notlarını düzenleyebilirsin.

### 285 · PASS · Öğrenci

- Soru: nota yazdığım içeriği güncelleyebilir miyim
- Beklenen intent: `note_edit`
- Gerçek intent: `note_edit`
- response_id: `note_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu değiştirmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Düzenle**'yi seç. 3) Başlığı veya içeriği değiştirip **Güncelle**'ye bas ve onayla. Yalnızca kendi Defter notlarını düzenleyebilirsin.

### 286 · PASS · Öğretmen

- Soru: defterde yazdığımı düzeltmek istiyorum
- Beklenen intent: `note_edit`
- Gerçek intent: `note_edit`
- response_id: `note_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu değiştirmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Düzenle**'yi seç. 3) Başlığı veya içeriği değiştirip **Güncelle**'ye bas ve onayla. Yalnızca kendi Defter notlarını düzenleyebilirsin.

### 287 · PASS · Öğrenci

- Soru: defterdeki notu güncellicem
- Beklenen intent: `note_edit`
- Gerçek intent: `note_edit`
- response_id: `note_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu değiştirmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Düzenle**'yi seç. 3) Başlığı veya içeriği değiştirip **Güncelle**'ye bas ve onayla. Yalnızca kendi Defter notlarını düzenleyebilirsin.

### 288 · PASS · Veli

- Soru: kişisel notta değişiklik yapacağım
- Beklenen intent: `note_edit`
- Gerçek intent: `note_edit`
- response_id: `note_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu değiştirmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Düzenle**'yi seç. 3) Başlığı veya içeriği değiştirip **Güncelle**'ye bas ve onayla. Yalnızca kendi Defter notlarını düzenleyebilirsin.

### 289 · PASS · Öğrenci

- Soru: not eklemek
- Beklenen intent: `note_create`
- Gerçek intent: `note_create`
- response_id: `note_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) **Defter (Notebook)** menüsünden `/notes`'a git, **Yeni not (New note)**'a bas. 2) **Başlık** (zorunlu, ≤200) ve isteğe bağlı **İçerik** (≤10.000) gir. 3) **Ekler** bölümünde **Dosya ekle** ile en fazla 10 dosya ekle. 4) **Oluştur**. Notlar yalnızca sahibine görünür. 10 dosyaya ulaştığında önce bir eki silmelisin; dosya boyut sınırı okul ayarındandır (varsayılan ~5 MiB) ve aşılırsa 413 hatası alınır.

### 290 · PASS · Veli

- Soru: defterime hatırlatma yazmak istiyorum
- Beklenen intent: `note_create`
- Gerçek intent: `note_create`
- response_id: `note_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) **Defter (Notebook)** menüsünden `/notes`'a git, **Yeni not (New note)**'a bas. 2) **Başlık** (zorunlu, ≤200) ve isteğe bağlı **İçerik** (≤10.000) gir. 3) **Ekler** bölümünde **Dosya ekle** ile en fazla 10 dosya ekle. 4) **Oluştur**. Notlar yalnızca sahibine görünür. 10 dosyaya ulaştığında önce bir eki silmelisin; dosya boyut sınırı okul ayarındandır (varsayılan ~5 MiB) ve aşılırsa 413 hatası alınır.

### 291 · PASS · Öğretmen

- Soru: yeni bir not yazacağım
- Beklenen intent: `note_create`
- Gerçek intent: `note_create`
- response_id: `note_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) **Defter (Notebook)** menüsünden `/notes`'a git, **Yeni not (New note)**'a bas. 2) **Başlık** (zorunlu, ≤200) ve isteğe bağlı **İçerik** (≤10.000) gir. 3) **Ekler** bölümünde **Dosya ekle** ile en fazla 10 dosya ekle. 4) **Oluştur**. Notlar yalnızca sahibine görünür. 10 dosyaya ulaştığında önce bir eki silmelisin; dosya boyut sınırı okul ayarındandır (varsayılan ~5 MiB) ve aşılırsa 413 hatası alınır.

### 292 · PASS · Öğrenci

- Soru: not almak istiyorum
- Beklenen intent: `note_create`
- Gerçek intent: `note_create`
- response_id: `note_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) **Defter (Notebook)** menüsünden `/notes`'a git, **Yeni not (New note)**'a bas. 2) **Başlık** (zorunlu, ≤200) ve isteğe bağlı **İçerik** (≤10.000) gir. 3) **Ekler** bölümünde **Dosya ekle** ile en fazla 10 dosya ekle. 4) **Oluştur**. Notlar yalnızca sahibine görünür. 10 dosyaya ulaştığında önce bir eki silmelisin; dosya boyut sınırı okul ayarındandır (varsayılan ~5 MiB) ve aşılırsa 413 hatası alınır.

### 293 · PASS · Öğretmen

- Soru: sınav notunu silmek
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 294 · PASS · Öğretmen

- Soru: öğrenci notunu değiştirmek
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 295 · PASS · Öğretmen

- Soru: Ayşe'nin sınav notunu düzeltmek istiyorum
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 296 · PASS · Öğretmen

- Soru: sınav puanını değiştirmek istiyorum
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 297 · PASS · Yönetici

- Soru: öğrencinin notunu kaldırmak istiyorum
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 298 · PASS · Öğretmen

- Soru: ödev notunu silmek
- Beklenen intent: `homework_grade`
- Gerçek intent: `homework_grade`
- response_id: `homework_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ödevi verdiğin (yönettiğin) ders. 1) **Ödevler** (`/homework`) → ödevin detayı → **Teslimler**. 2) Bir öğrencinin teslimini aç, **Notlandır** ile not/geri bildirim ver; gerekirse **Notu kaldır** ile geri al. Notlandırma Öğretmen ve üstüne açıktır; kendi teslimini notlandıramazsın.

### 299 · PASS · Öğretmen

- Soru: ödev puanını değiştirmek
- Beklenen intent: `homework_grade`
- Gerçek intent: `homework_grade`
- response_id: `homework_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ödevi verdiğin (yönettiğin) ders. 1) **Ödevler** (`/homework`) → ödevin detayı → **Teslimler**. 2) Bir öğrencinin teslimini aç, **Notlandır** ile not/geri bildirim ver; gerekirse **Notu kaldır** ile geri al. Notlandırma Öğretmen ve üstüne açıktır; kendi teslimini notlandıramazsın.

### 300 · PASS · Öğretmen

- Soru: teslim notunu düzeltmek
- Beklenen intent: `homework_grade`
- Gerçek intent: `homework_grade`
- response_id: `homework_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ödevi verdiğin (yönettiğin) ders. 1) **Ödevler** (`/homework`) → ödevin detayı → **Teslimler**. 2) Bir öğrencinin teslimini aç, **Notlandır** ile not/geri bildirim ver; gerekirse **Notu kaldır** ile geri al. Notlandırma Öğretmen ve üstüne açıktır; kendi teslimini notlandıramazsın.

### 301 · PASS · Yönetici

- Soru: öğrencinin ödev puanını kaldırmak
- Beklenen intent: `homework_grade`
- Gerçek intent: `homework_grade`
- response_id: `homework_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ödevi verdiğin (yönettiğin) ders. 1) **Ödevler** (`/homework`) → ödevin detayı → **Teslimler**. 2) Bir öğrencinin teslimini aç, **Notlandır** ile not/geri bildirim ver; gerekirse **Notu kaldır** ile geri al. Notlandırma Öğretmen ve üstüne açıktır; kendi teslimini notlandıramazsın.

### 302 · PASS · Yönetici

- Soru: not bandını silmek
- Beklenen intent: `school_settings`
- Gerçek intent: `school_settings`
- response_id: `school_settings_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ayarlar", "route": "/management/settings"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> `/management/settings` (Okul ayarları) sayfasında **Değerlendirme** sekmesinde sınav türü/ağırlığı, yoklama durumları ve not bantları; **Yemekhane** sekmesinde rezervasyon kapanış süresi, öğün saatleri ve beslenme etiketleri; **Sistem** sekmesinde not/dosya yükleme limiti ile Çelebi sohbet geçmişi, konu ve mesaj limitleri yönetilir. **Satır ekle** ile ekle, çöp kutusuyla sil, sonra **Kaydet**. Bu okul geneli sayfa kişisel hesap/avatar **Ayarlar** penceresinden farklıdır.

### 303 · PASS · Yönetici

- Soru: okuldaki not bandını değiştirmek
- Beklenen intent: `school_settings`
- Gerçek intent: `school_settings`
- response_id: `school_settings_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ayarlar", "route": "/management/settings"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> `/management/settings` (Okul ayarları) sayfasında **Değerlendirme** sekmesinde sınav türü/ağırlığı, yoklama durumları ve not bantları; **Yemekhane** sekmesinde rezervasyon kapanış süresi, öğün saatleri ve beslenme etiketleri; **Sistem** sekmesinde not/dosya yükleme limiti ile Çelebi sohbet geçmişi, konu ve mesaj limitleri yönetilir. **Satır ekle** ile ekle, çöp kutusuyla sil, sonra **Kaydet**. Bu okul geneli sayfa kişisel hesap/avatar **Ayarlar** penceresinden farklıdır.

### 304 · PASS · ADMIN

- Soru: not aralıklarını güncellemek
- Beklenen intent: `school_settings`
- Gerçek intent: `school_settings`
- response_id: `school_settings_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ayarlar", "route": "/management/settings"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> `/management/settings` (Okul ayarları) sayfasında **Değerlendirme** sekmesinde sınav türü/ağırlığı, yoklama durumları ve not bantları; **Yemekhane** sekmesinde rezervasyon kapanış süresi, öğün saatleri ve beslenme etiketleri; **Sistem** sekmesinde not/dosya yükleme limiti ile Çelebi sohbet geçmişi, konu ve mesaj limitleri yönetilir. **Satır ekle** ile ekle, çöp kutusuyla sil, sonra **Kaydet**. Bu okul geneli sayfa kişisel hesap/avatar **Ayarlar** penceresinden farklıdır.

### 305 · PASS · Öğretmen

- Soru: öğrenci kaydını kaldırmak
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 306 · PASS · Öğretmen

- Soru: ders kaydını silmek
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 307 · PASS · Yönetici

- Soru: sınıftan öğrencinin kaydını kaldır
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 308 · PASS · Yönetici

- Soru: mesai kaydını silmek
- Beklenen intent: `staff_work_manage`
- Gerçek intent: `staff_work_manage`
- response_id: `staff_work_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Personel mesai", "route": "/management/staff-work"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/management/staff-work` (Personel mesai) → aramaya **en az 2 karakter** (öğretmen adı). 2) Öğretmen satırında **Görüntüle**. 3) **Kapalı** bir kaydın **Düzenle**'sini açıp giriş/çıkış tarih+saat düzelt, **Güncelle**. **Açık mesai düzeltilemez** (önce çıkış yapılmalı veya silinmeli); çıkış girişten önce olamaz.

### 309 · PASS · ADMIN

- Soru: kapalı mesaiyi kaldırmak
- Beklenen intent: `staff_work_manage`
- Gerçek intent: `staff_work_manage`
- response_id: `staff_work_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Personel mesai", "route": "/management/staff-work"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/management/staff-work` (Personel mesai) → aramaya **en az 2 karakter** (öğretmen adı). 2) Öğretmen satırında **Görüntüle**. 3) **Kapalı** bir kaydın **Düzenle**'sini açıp giriş/çıkış tarih+saat düzelt, **Güncelle**. **Açık mesai düzeltilemez** (önce çıkış yapılmalı veya silinmeli); çıkış girişten önce olamaz.

### 310 · PASS · Öğrenci

- Soru: randevuyu iptal etmek
- Beklenen intent: `appointment_book`
- Gerçek intent: `appointment_book`
- response_id: `appointment_book_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Randevu almak için **Planlama** grubundaki **Randevular** (`/appointments`) sayfasına git. **Öğretmenlerin açık saatleri** bölümünden uygun saati seç, **Randevu al**'a bas. Talebin **Randevularım** altında görünür ve öğretmen onayına düşer. Randevu alma yalnızca Öğrenci ve Veli'ye açıktır. Veli randevuyu çocuğu adına değil kendi requester hesabıyla alır. Slot başlamış/doluysa, aynı saatte başka randevun varsa veya öğretmen artık uygun rolde değilse 409 alırsın. İptali yalnız talebi açan kullanıcı yapar; öğretmenin önerdiği yeni saati **Kabul et/Reddet** ile yanıtlayabilirsin.

### 311 · PASS · Veli

- Soru: randevu talebimi geri çekmek istiyorum
- Beklenen intent: `appointment_book`
- Gerçek intent: `appointment_book`
- response_id: `appointment_book_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Randevu almak için **Planlama** grubundaki **Randevular** (`/appointments`) sayfasına git. **Öğretmenlerin açık saatleri** bölümünden uygun saati seç, **Randevu al**'a bas. Talebin **Randevularım** altında görünür ve öğretmen onayına düşer. Randevu alma yalnızca Öğrenci ve Veli'ye açıktır. Veli randevuyu çocuğu adına değil kendi requester hesabıyla alır. Slot başlamış/doluysa, aynı saatte başka randevun varsa veya öğretmen artık uygun rolde değilse 409 alırsın. İptali yalnız talebi açan kullanıcı yapar; öğretmenin önerdiği yeni saati **Kabul et/Reddet** ile yanıtlayabilirsin.

### 312 · PASS · Öğrenci

- Soru: yemek rezervasyonumu silmek
- Beklenen intent: `meal_book`
- Gerçek intent: `meal_book`
- response_id: `meal_book_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yemek için yer ayırmak üzere **Yemekler** (`/meals`) → ilgili menü/öğüne gir, **Yer ayır**'a bas. Rezervasyonun **Rezerve edildi** olarak görünür; **Rezervasyonu iptal et** ile geri alabilirsin. Yer ayırma Öğrenci (kendisi) ve Veli'ye (bağlı çocuğu) açıktır. Geçmiş tarih, iptal eşiği, doluluk, yeniden-rezervasyon tavanı veya eşzamanlı değişiklik 409 üretebilir; sayfayı yenileyip güncel kapasite ve son saati kontrol et.

### 313 · PASS · Öğrenci

- Soru: başkasının notunu sil
- Beklenen intent: `privacy_security`
- Gerçek intent: `privacy_security`
- response_id: `privacy_policy_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yalnızca kendi yetkili olduğun bilgileri görebilirsin. Başka bir kullanıcının notu, yoklaması veya kişisel bilgisi paylaşılmaz. Öğretmen ve üstü roller, yalnızca yetkili oldukları yönetim sayfalarından (Öğrenci notları/yoklaması) öğrenci verisine erişebilir; kişisel telefon/e-posta paylaşılmaz.

### 314 · PASS · Öğrenci

- Soru: arkadaşımın notunu değiştirmek istiyorum
- Beklenen intent: `privacy_security`
- Gerçek intent: `privacy_security`
- response_id: `privacy_policy_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yalnızca kendi yetkili olduğun bilgileri görebilirsin. Başka bir kullanıcının notu, yoklaması veya kişisel bilgisi paylaşılmaz. Öğretmen ve üstü roller, yalnızca yetkili oldukları yönetim sayfalarından (Öğrenci notları/yoklaması) öğrenci verisine erişebilir; kişisel telefon/e-posta paylaşılmaz.

### 315 · PASS · Öğrenci

- Soru: başka birinin notuna müdahale edebilir miyim
- Beklenen intent: `privacy_security`
- Gerçek intent: `privacy_security`
- response_id: `privacy_policy_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yalnızca kendi yetkili olduğun bilgileri görebilirsin. Başka bir kullanıcının notu, yoklaması veya kişisel bilgisi paylaşılmaz. Öğretmen ve üstü roller, yalnızca yetkili oldukları yönetim sayfalarından (Öğrenci notları/yoklaması) öğrenci verisine erişebilir; kişisel telefon/e-posta paylaşılmaz.

### 316 · PASS · Öğrenci

- Soru: öğretmenin telefonunu öğrenmek istiyorum
- Beklenen intent: `privacy_security`
- Gerçek intent: `privacy_security`
- response_id: `privacy_policy_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yalnızca kendi yetkili olduğun bilgileri görebilirsin. Başka bir kullanıcının notu, yoklaması veya kişisel bilgisi paylaşılmaz. Öğretmen ve üstü roller, yalnızca yetkili oldukları yönetim sayfalarından (Öğrenci notları/yoklaması) öğrenci verisine erişebilir; kişisel telefon/e-posta paylaşılmaz.

### 317 · PASS · Öğrenci

- Soru: saol
- Beklenen intent: `thanks`
- Gerçek intent: `thanks`
- response_id: `thanks_reply`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Rica ederim! 😊 Başka bir konuda takıldığında yine sorabilirsin — ders, sınav, karne, yoklama, defter... hepsi için buradayım.

### 318 · PASS · Öğrenci

- Soru: sınava geri döncem
- Beklenen intent: `exam_rejoin_retake`
- Gerçek intent: `exam_rejoin_retake`
- response_id: `exam_rejoin_retake_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Rejoin (aynı denemeye dönüş):** 'Yeniden girişe izin ver' açıksa odadan çıktıktan sonra tekrar **Sınav odasını aç** → **Sınava devam et**; kalan süre ve cevapların korunur. **Retake (yeni deneme):** 'Deneme hakkı' açık ve azami sayı belirlenmişse her yeni giriş bir deneme kullanır. **Süre çıkışta bile durmaz.** 'Yeniden giriş kapalı', 'deneme hakkı kalmadı', 'süre doldu' veya 'deneme zaten teslim edildi' durumunda aynı denemeye dönemezsin.

### 319 · PASS · Öğretmen

- Soru: öğrenciyi puanlıcam
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 320 · PASS · ADMIN

- Soru: öğrenciyi öğretmen yapcam
- Beklenen intent: `user_role_change`
- Gerçek intent: `user_role_change`
- response_id: `user_role_change_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Kullanıcılar", "route": "/admin/users"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Ne:** **Kullanıcılar** (`/admin/users`, yalnız ADMIN) tüm hesapları yönettiğin yerdir — burada (a) **rol değiştirir**, (b) **herhangi bir kullanıcının profilini düzenlersin**.
> **Nereden / nasıl (rol):** 1) `/admin/users`'ı aç, ada göre **ara**. 2) Satırdaki **rol menüsünden** yeni rolü seç. 3) Beliren **Güncelle (Update)**'ye basıp onayla. Kendi rolünü değiştiremezsin (kendi satırında menü pasif); değişiklik sonraki işlemde hemen geçerli olur.
> **Etkili kullanım:** kalabalık listede önce **arama/filtre** ile daralt; rolü yanlışlıkla düşürmemek için değişiklikten önce satırdaki adı teyit et. Kendi rolünü ve sistemdeki son ADMIN'in rolünü değiştiremezsin. Rol değişimi ders kaydı/öğretmen ataması, randevu slotu, etkinlik kaydı ve beyaz tahta üyelikleri gibi role bağlı ilişkileri etkileyebilir. Profil düzeltmek için kullanıcının satırından profiline geçip alanları güncelle.

### 321 · PASS · Öğrenci

- Soru: etkinlikler nerde
- Beklenen intent: `event_view`
- Gerçek intent: `event_view`
- response_id: `event_view_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Etkinlikler", "route": "/events"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Okuldaki **etkinlikleri** menüdeki **Etkinlikler** (`/events`) sayfasından görürsün. Backend oturumlu kullanıcıya yalnız kendi katılacağı etkinlikleri değil, okulun etkinlik listesini döndürür; audience alanı beklenen katılımcıyı belirtir, görünürlük filtresi değildir.

### 322 · PASS · Öğrenci

- Soru: ders pdfi nerde
- Beklenen intent: `course_materials_info`
- Gerçek intent: `course_materials_info`
- response_id: `course_materials_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Öğretmenin yüklediği **ders notları** ve **PDF/dosya**lar ilgili dersin sayfasındadır: **Dersler** (`/courses`) → ders → Ders notları.

### 323 · PASS · Öğretmen

- Soru: randevuyu onaylıcam
- Beklenen intent: `appointment_requests`
- Gerçek intent: `appointment_requests`
- response_id: `appointment_requests_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Randevular** (`/appointments`) → **Randevu talepleri** bölümünde gelen talepleri görürsün; her talepte **Onayla** ile kabul et (gerekirse reddet) veya **Başka saat öner**. Onaylanan randevu, ilgili öğrenci/velinin **Randevularım**'ında görünür. Karşı saati requester kabul/reddeder; eski ya da artık geçerli olmayan teklife basmak 409 verir. Öğretmen/Yönetici randevuyu requester adına iptal edemez.

### 324 · PASS · Öğrenci

- Soru: yemek ayırtcam
- Beklenen intent: `meal_book`
- Gerçek intent: `meal_book`
- response_id: `meal_book_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yemek için yer ayırmak üzere **Yemekler** (`/meals`) → ilgili menü/öğüne gir, **Yer ayır**'a bas. Rezervasyonun **Rezerve edildi** olarak görünür; **Rezervasyonu iptal et** ile geri alabilirsin. Yer ayırma Öğrenci (kendisi) ve Veli'ye (bağlı çocuğu) açıktır. Geçmiş tarih, iptal eşiği, doluluk, yeniden-rezervasyon tavanı veya eşzamanlı değişiklik 409 üretebilir; sayfayı yenileyip güncel kapasite ve son saati kontrol et.

### 325 · PASS · Yönetici

- Soru: menü yayınlıcam
- Beklenen intent: `meal_menu_manage`
- Gerçek intent: `meal_menu_manage`
- response_id: `meal_menu_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Yemekler** (`/meals`) → **Menü yayınla** ile yeni menü/öğün oluştur, **Yemek ekle** ile öğüne yemek ekle; menü ve yemek içeriği yönetimi Yönetici+ içindir. Öğrencinin güvenlik kaydı olan **Beslenme profili** ayrı bir işlemdir; **Kredi kaydetme** ise yalnız ADMIN hesabında görünür.

### 326 · PASS · Öğretmen

- Soru: soruyu onaylıcam
- Beklenen intent: `question_approve`
- Gerçek intent: `question_approve`
- response_id: `question_approve_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru havuzu", "route": "/questions"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Soru havuzu** (`/questions`) → soru detayında **Onayla** ile bekleyen soruyu yayınla, gerekirse **Reddet**. Onaylanan soru **Onaylandı** olur ve havuza erişen rollere görünür. **Reddet**, soru kaydıyla birlikte çözümleri ve görselleri kalıcı olarak siler; onaylamadan önce içeriği kontrol et. Moderasyon Öğretmen ve üstüne açıktır.

### 327 · PASS · Öğrenci

- Soru: sınava gircem
- Beklenen intent: `exam_enter_room`
- Gerçek intent: `exam_enter_room`
- response_id: `exam_enter_room_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: sınavın dersine kayıtlı olmak; sınav girilebilir modda (Senkron/Asenkron/Açık) ve **Aktif** olmalı. 1) Sınav detayında (`/exams/$id`) **Sınav odasını aç (Open exam room)**'a bas. 2) **Sınava başla (Start exam)**. Sorular ve **Kalan süre** görünür. Giremiyorsan en sık nedenler: sınav henüz başlamadı veya bitti, **Zamansız** modda, derse kayıtlı değilsin, önceki deneme zaten teslim edildi, süre doldu ya da deneme hakkın kalmadı.

### 328 · PASS · Öğrenci

- Soru: ödevi yüklicem
- Beklenen intent: `homework_submit`
- Gerçek intent: `homework_submit`
- response_id: `homework_submit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ödevin verildiği dersin kayıtlı öğrencisisin. 1) **Ödevler** (`/homework`) → ilgili ödevin detayına (`/homework/$id`) gir. 2) **Ödevi teslim et** panelinde cevabını yaz ve/veya dosya ekle. 3) Gönder. Teslim yalnızca Öğrenciye açıktır; **Son teslim** tarihine dikkat et. Teslim notlandırıldıktan sonra öğrenci metni veya dosyayı değiştiremez/silemez; dosya okulun yükleme sınırını aşarsa 413 hatası alınır.

### 329 · PASS · Öğrenci

- Soru: profilimi degistircem
- Beklenen intent: `profile_edit`
- Gerçek intent: `profile_edit`
- response_id: `profile_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Profilini iki yerden güncelleyebilirsin: 1) Sağ üstteki hesap/avatar menüsü → **Ayarlar → Hesap** bölümünde **Ad, Soyad, E-posta, Telefon** ve **Doğum tarihi** alanlarını değiştir. 2) Tam profil ekranı için `/profile/me` adresine git, **Profili düzenle**'ye bas; burada bunlara ek olarak **Görünen ad** ve **Hakkında** alanları da vardır. Profil fotoğrafını da bu sayfadaki avatar üzerinden yükleyebilir, değiştirebilir veya kaldırabilirsin. Sonunda **Kaydet**'e bas. Tüm alanlar isteğe bağlıdır; **kullanıcı adı ve rol buradan değiştirilemez**. E-posta geçerli biçimde, telefon 7–15 hane olmalı; doğum tarihi gelecekte olamaz.

### 330 · PASS · Öğrenci

- Soru: baskasinin notu
- Beklenen intent: `privacy_security`
- Gerçek intent: `privacy_security`
- response_id: `privacy_policy_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yalnızca kendi yetkili olduğun bilgileri görebilirsin. Başka bir kullanıcının notu, yoklaması veya kişisel bilgisi paylaşılmaz. Öğretmen ve üstü roller, yalnızca yetkili oldukları yönetim sayfalarından (Öğrenci notları/yoklaması) öğrenci verisine erişebilir; kişisel telefon/e-posta paylaşılmaz.

### 331 · PASS · Öğretmen

- Soru: Ali'nin notunu düzelt
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 332 · PASS · Öğretmen

- Soru: sınav notunu güncelle
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 333 · PASS · Öğretmen

- Soru: öğrencinin notunu değil kaydını sil
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 334 · PASS · Öğretmen

- Soru: öğrenciyi değil notunu sil
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 335 · PASS · Öğretmen

- Soru: hocam yanlış puan girdim nasıl geri alırım
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 336 · PASS · Öğretmen

- Soru: teslimin puanını geri al
- Beklenen intent: `homework_grade`
- Gerçek intent: `homework_grade`
- response_id: `homework_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ödevi verdiğin (yönettiğin) ders. 1) **Ödevler** (`/homework`) → ödevin detayı → **Teslimler**. 2) Bir öğrencinin teslimini aç, **Notlandır** ile not/geri bildirim ver; gerekirse **Notu kaldır** ile geri al. Notlandırma Öğretmen ve üstüne açıktır; kendi teslimini notlandıramazsın.

### 337 · PASS · Öğretmen

- Soru: rosterdan çıkar
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 338 · PASS · Öğrenci

- Soru: mailimi duzelt
- Beklenen intent: `profile_edit`
- Gerçek intent: `profile_edit`
- response_id: `profile_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Profilini iki yerden güncelleyebilirsin: 1) Sağ üstteki hesap/avatar menüsü → **Ayarlar → Hesap** bölümünde **Ad, Soyad, E-posta, Telefon** ve **Doğum tarihi** alanlarını değiştir. 2) Tam profil ekranı için `/profile/me` adresine git, **Profili düzenle**'ye bas; burada bunlara ek olarak **Görünen ad** ve **Hakkında** alanları da vardır. Profil fotoğrafını da bu sayfadaki avatar üzerinden yükleyebilir, değiştirebilir veya kaldırabilirsin. Sonunda **Kaydet**'e bas. Tüm alanlar isteğe bağlıdır; **kullanıcı adı ve rol buradan değiştirilemez**. E-posta geçerli biçimde, telefon 7–15 hane olmalı; doğum tarihi gelecekte olamaz.

### 339 · PASS · Öğretmen

- Soru: snv olustur
- Beklenen intent: `exam_create`
- Gerçek intent: `exam_create`
- response_id: `exam_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: yönetebileceğin en az bir ders olmalı. 1) `/exams` → **Sınav oluştur (Create exam)**. 2) **Ders seç**, **Başlık** ve isteğe bağlı açıklama gir. 3) **Tür** (Ödev/Kısa sınav/Vize/Final/Proje/Sözlü) ve **Mod** (Senkron/Asenkron/Açık) seç. 4) Gerekirse **Deneme hakkı** ve **Yeniden girişe izin ver**'i ayarla. 5) Senkron/Asenkron ise Başlangıç/Bitiş gir. Asenkron modda süre zorunludur; Senkron mod süre kabul etmez. Süre 1 dakika–24 saat arasında ve sınav penceresine sığmalıdır; Açık mod başlangıç/bitiş taşımaz. 6) **Oluştur**. Sınavlar ders içinden eklenir.

### 340 · PASS · Öğrenci

- Soru: snava gircem
- Beklenen intent: `exam_enter_room`
- Gerçek intent: `exam_enter_room`
- response_id: `exam_enter_room_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: sınavın dersine kayıtlı olmak; sınav girilebilir modda (Senkron/Asenkron/Açık) ve **Aktif** olmalı. 1) Sınav detayında (`/exams/$id`) **Sınav odasını aç (Open exam room)**'a bas. 2) **Sınava başla (Start exam)**. Sorular ve **Kalan süre** görünür. Giremiyorsan en sık nedenler: sınav henüz başlamadı veya bitti, **Zamansız** modda, derse kayıtlı değilsin, önceki deneme zaten teslim edildi, süre doldu ya da deneme hakkın kalmadı.

### 341 · PASS · Öğretmen

- Soru: drs açcam
- Beklenen intent: `course_create`
- Gerçek intent: `course_create`
- response_id: `course_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/courses`'a git, **Yeni ders (New course)**'e bas. 2) Sağdan açılan panelde **Başlık** (zorunlu), isteğe bağlı **Açıklama** ve **Dönem** (varsayılan 'Atanmamış') gir. 3) **Oluştur**. Öğrencide 'Yeni ders' düğmesi görünmez.

### 342 · PASS · Öğretmen

- Soru: yoklma al
- Beklenen intent: `roll_call`
- Gerçek intent: `roll_call`
- response_id: `roll_call_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: derste kayıtlı öğrenci ve en az bir oturum olmalı; yönetim yetkisi. 1) Ders detayı → **Ders oturumları** → oturum kartında **Yoklama (Roll call)**. 2) Her öğrenci için **Var / Yok / Geç / Mazeretli** seç. 3) Satırda **Kaydet** (daha önce kaydedildiyse **Güncelle**). Öğrenci ders oturumu yoklamasında kendini işaretleyemez.

### 343 · PASS · Öğrenci

- Soru: karnme bak
- Beklenen intent: `report_card_view`
- Gerçek intent: `report_card_view`
- response_id: `report_card_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Karnem", "route": "/marks"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Karneni görmek için menüden **Karnem (Report card)** veya `/marks`'a git. Üstte **Genel ortalama** (sayı + harf notu, /100), altında her ders için **Ders ortalaması** ve sınav bazında **Ağırlık** ve **Not** görünür. Karnem yalnızca Öğrenci rolüne açıktır; notu henüz girilmemiş sınav rapor listesine eklenmez.

### 344 · PASS · Öğretmen

- Soru: ogrnci notunu degstr
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 345 · PASS · Öğretmen

- Soru: öğrenci puanını düzelt
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 346 · PASS · Öğretmen

- Soru: öğrenci puanını sil
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 347 · PASS · Öğretmen

- Soru: sınav puanını kaldır
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 348 · PASS · Öğretmen

- Soru: öğrenci kaydını sil
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 349 · PASS · Öğretmen

- Soru: rosterdan öğrenciyi çıkar
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 350 · PASS · Öğretmen

- Soru: öğrencinin notunu değil kaydını kaldır
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 351 · PASS · Öğrenci

- Soru: başkasının notunu değiştirmek
- Beklenen intent: `privacy_security`
- Gerçek intent: `privacy_security`
- response_id: `privacy_policy_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yalnızca kendi yetkili olduğun bilgileri görebilirsin. Başka bir kullanıcının notu, yoklaması veya kişisel bilgisi paylaşılmaz. Öğretmen ve üstü roller, yalnızca yetkili oldukları yönetim sayfalarından (Öğrenci notları/yoklaması) öğrenci verisine erişebilir; kişisel telefon/e-posta paylaşılmaz.

### 352 · PASS · Öğrenci

- Soru: benim notumu sil
- Beklenen intent: `note_delete`
- Gerçek intent: `note_delete`
- response_id: `note_delete_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu silmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Sil**'i seç. 3) Açılan onay penceresinde silme işlemini onayla. Yalnızca kendi Defter notlarını silebilirsin.

### 353 · PASS · Öğretmen

- Soru: ödev teslim puanını düzelt
- Beklenen intent: `homework_grade`
- Gerçek intent: `homework_grade`
- response_id: `homework_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ödevi verdiğin (yönettiğin) ders. 1) **Ödevler** (`/homework`) → ödevin detayı → **Teslimler**. 2) Bir öğrencinin teslimini aç, **Notlandır** ile not/geri bildirim ver; gerekirse **Notu kaldır** ile geri al. Notlandırma Öğretmen ve üstüne açıktır; kendi teslimini notlandıramazsın.

### 354 · PASS · Yönetici

- Soru: not bandını güncelle
- Beklenen intent: `school_settings`
- Gerçek intent: `school_settings`
- response_id: `school_settings_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ayarlar", "route": "/management/settings"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> `/management/settings` (Okul ayarları) sayfasında **Değerlendirme** sekmesinde sınav türü/ağırlığı, yoklama durumları ve not bantları; **Yemekhane** sekmesinde rezervasyon kapanış süresi, öğün saatleri ve beslenme etiketleri; **Sistem** sekmesinde not/dosya yükleme limiti ile Çelebi sohbet geçmişi, konu ve mesaj limitleri yönetilir. **Satır ekle** ile ekle, çöp kutusuyla sil, sonra **Kaydet**. Bu okul geneli sayfa kişisel hesap/avatar **Ayarlar** penceresinden farklıdır.

### 355 · PASS · Öğretmen

- Soru: sınav oluştur ve yoklama al
- Beklenen intent: `exam_create`
- Gerçek intent: `exam_create`
- response_id: `exam_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Birkaç şey sormuşsun, sırayla cevaplayayım:
>
> **1) Yeni sınav oluşturma ve mod seçme**
> Ön koşul: yönetebileceğin en az bir ders olmalı. 1) `/exams` → **Sınav oluştur (Create exam)**. 2) **Ders seç**, **Başlık** ve isteğe bağlı açıklama gir. 3) **Tür** (Ödev/Kısa sınav/Vize/Final/Proje/Sözlü) ve **Mod** (Senkron/Asenkron/Açık) seç. 4) Gerekirse **Deneme hakkı** ve **Yeniden girişe izin ver**'i ayarla. 5) Senkron/Asenkron ise Başlangıç/Bitiş gir. Asenkron modda süre zorunludur; Senkron mod süre kabul etmez. Süre 1 dakika–24 saat arasında ve sınav penceresine sığmalıdır; Açık mod başlangıç/bitiş taşımaz. 6) **Oluştur**. Sınavlar ders içinden eklenir.
>
> **2) Ders oturumunda yoklama alma**
> Ön koşul: derste kayıtlı öğrenci ve en az bir oturum olmalı; yönetim yetkisi. 1) Ders detayı → **Ders oturumları** → oturum kartında **Yoklama (Roll call)**. 2) Her öğrenci için **Var / Yok / Geç / Mazeretli** seç. 3) Satırda **Kaydet** (daha önce kaydedildiyse **Güncelle**). Öğrenci ders oturumu yoklamasında kendini işaretleyemez.

### 356 · PASS · Öğrenci

- Soru: profil sayfamı görmek istiyorum
- Beklenen intent: `profile_view`
- Gerçek intent: `profile_view`
- response_id: `profile_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kendi profilini `/profile/me` adresinden veya hesap menüsündeki **Profilim** seçeneğinden açabilirsin. Burada profil fotoğrafın, görünen adın/Hakkında alanın, rolün, şube ve ders üyeliklerin, rozetlerin ile odak saati, odak oturumu, teslim edilen/zamanında ödev ve girilen sınav istatistiklerin görünür. Kendi sayfanda **Profili düzenle** düğmesi vardır. Başka bir kişinin profili `/profile/$userId` ile açılır; erişim kapsamını backend denetler ve Veli yalnız kendisini veya bağlı çocuklarını görebilir.

### 357 · PASS · Öğrenci

- Soru: kazandığım rozetleri hangi ekranda bulurum
- Beklenen intent: `profile_view`
- Gerçek intent: `profile_view`
- response_id: `profile_view_info`
- confidence: `0.3877`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kendi profilini `/profile/me` adresinden veya hesap menüsündeki **Profilim** seçeneğinden açabilirsin. Burada profil fotoğrafın, görünen adın/Hakkında alanın, rolün, şube ve ders üyeliklerin, rozetlerin ile odak saati, odak oturumu, teslim edilen/zamanında ödev ve girilen sınav istatistiklerin görünür. Kendi sayfanda **Profili düzenle** düğmesi vardır. Başka bir kişinin profili `/profile/$userId` ile açılır; erişim kapsamını backend denetler ve Veli yalnız kendisini veya bağlı çocuklarını görebilir.

### 358 · PASS · Öğretmen

- Soru: odak ve ödev istatistiklerim profilimde nerede
- Beklenen intent: `profile_view`
- Gerçek intent: `profile_view`
- response_id: `profile_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kendi profilini `/profile/me` adresinden veya hesap menüsündeki **Profilim** seçeneğinden açabilirsin. Burada profil fotoğrafın, görünen adın/Hakkında alanın, rolün, şube ve ders üyeliklerin, rozetlerin ile odak saati, odak oturumu, teslim edilen/zamanında ödev ve girilen sınav istatistiklerin görünür. Kendi sayfanda **Profili düzenle** düğmesi vardır. Başka bir kişinin profili `/profile/$userId` ile açılır; erişim kapsamını backend denetler ve Veli yalnız kendisini veya bağlı çocuklarını görebilir.

### 359 · PASS · Öğrenci

- Soru: avatar fotoğrafımı yenilemek istiyorum
- Beklenen intent: `profile_edit`
- Gerçek intent: `profile_edit`
- response_id: `profile_edit_instructions`
- confidence: `0.4833`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Profilini iki yerden güncelleyebilirsin: 1) Sağ üstteki hesap/avatar menüsü → **Ayarlar → Hesap** bölümünde **Ad, Soyad, E-posta, Telefon** ve **Doğum tarihi** alanlarını değiştir. 2) Tam profil ekranı için `/profile/me` adresine git, **Profili düzenle**'ye bas; burada bunlara ek olarak **Görünen ad** ve **Hakkında** alanları da vardır. Profil fotoğrafını da bu sayfadaki avatar üzerinden yükleyebilir, değiştirebilir veya kaldırabilirsin. Sonunda **Kaydet**'e bas. Tüm alanlar isteğe bağlıdır; **kullanıcı adı ve rol buradan değiştirilemez**. E-posta geçerli biçimde, telefon 7–15 hane olmalı; doğum tarihi gelecekte olamaz.

### 360 · PASS · Öğretmen

- Soru: biyografi alanını temizlemek istiyorum
- Beklenen intent: `profile_edit`
- Gerçek intent: `profile_edit`
- response_id: `profile_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Profilini iki yerden güncelleyebilirsin: 1) Sağ üstteki hesap/avatar menüsü → **Ayarlar → Hesap** bölümünde **Ad, Soyad, E-posta, Telefon** ve **Doğum tarihi** alanlarını değiştir. 2) Tam profil ekranı için `/profile/me` adresine git, **Profili düzenle**'ye bas; burada bunlara ek olarak **Görünen ad** ve **Hakkında** alanları da vardır. Profil fotoğrafını da bu sayfadaki avatar üzerinden yükleyebilir, değiştirebilir veya kaldırabilirsin. Sonunda **Kaydet**'e bas. Tüm alanlar isteğe bağlıdır; **kullanıcı adı ve rol buradan değiştirilemez**. E-posta geçerli biçimde, telefon 7–15 hane olmalı; doğum tarihi gelecekte olamaz.

### 361 · PASS · Veli

- Soru: görünen ismim yanlış, nereden düzeltirim
- Beklenen intent: `profile_edit`
- Gerçek intent: `profile_edit`
- response_id: `profile_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Profilini iki yerden güncelleyebilirsin: 1) Sağ üstteki hesap/avatar menüsü → **Ayarlar → Hesap** bölümünde **Ad, Soyad, E-posta, Telefon** ve **Doğum tarihi** alanlarını değiştir. 2) Tam profil ekranı için `/profile/me` adresine git, **Profili düzenle**'ye bas; burada bunlara ek olarak **Görünen ad** ve **Hakkında** alanları da vardır. Profil fotoğrafını da bu sayfadaki avatar üzerinden yükleyebilir, değiştirebilir veya kaldırabilirsin. Sonunda **Kaydet**'e bas. Tüm alanlar isteğe bağlıdır; **kullanıcı adı ve rol buradan değiştirilemez**. E-posta geçerli biçimde, telefon 7–15 hane olmalı; doğum tarihi gelecekte olamaz.

### 362 · PASS · Öğrenci

- Soru: hesap menüsündeki kişisel ayar penceresini arıyorum
- Beklenen intent: `personal_settings`
- Gerçek intent: `personal_settings`
- response_id: `personal_settings_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel **Ayarlar** bir sayfa değil, sağ üstteki hesap/avatar menüsünden açılan penceredir. **Hesap** bölümünde Ad, Soyad, E-posta, Telefon ve Doğum tarihini; **Görünüm** bölümünde Açık/Koyu tema, Türkçe/English dil ve vurgu renk paletini değiştirebilirsin. Görünen ad, Hakkında ve profil fotoğrafı gibi tam profil seçenekleri için `/profile/me` → **Profili düzenle** yolunu kullan. Okul geneli ayarlar ise bundan ayrıdır ve `/management/settings` altında yalnız yetkili hesaplara görünür.

### 363 · PASS · Öğretmen

- Soru: vurgu rengini varsayılana nasıl döndürürüm
- Beklenen intent: `personal_settings`
- Gerçek intent: `personal_settings`
- response_id: `personal_settings_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel **Ayarlar** bir sayfa değil, sağ üstteki hesap/avatar menüsünden açılan penceredir. **Hesap** bölümünde Ad, Soyad, E-posta, Telefon ve Doğum tarihini; **Görünüm** bölümünde Açık/Koyu tema, Türkçe/English dil ve vurgu renk paletini değiştirebilirsin. Görünen ad, Hakkında ve profil fotoğrafı gibi tam profil seçenekleri için `/profile/me` → **Profili düzenle** yolunu kullan. Okul geneli ayarlar ise bundan ayrıdır ve `/management/settings` altında yalnız yetkili hesaplara görünür.

### 364 · PASS · Veli

- Soru: ayarlar penceresinde hangi kişisel seçenekler var
- Beklenen intent: `personal_settings`
- Gerçek intent: `personal_settings`
- response_id: `personal_settings_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel **Ayarlar** bir sayfa değil, sağ üstteki hesap/avatar menüsünden açılan penceredir. **Hesap** bölümünde Ad, Soyad, E-posta, Telefon ve Doğum tarihini; **Görünüm** bölümünde Açık/Koyu tema, Türkçe/English dil ve vurgu renk paletini değiştirebilirsin. Görünen ad, Hakkında ve profil fotoğrafı gibi tam profil seçenekleri için `/profile/me` → **Profili düzenle** yolunu kullan. Okul geneli ayarlar ise bundan ayrıdır ve `/management/settings` altında yalnız yetkili hesaplara görünür.

### 365 · PASS · Öğrenci

- Soru: tema dil ve renk seçimlerini aynı yerde yapabilir miyim
- Beklenen intent: `language_theme`
- Gerçek intent: `language_theme`
- response_id: `language_theme_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Giriş yaptıysan sağ üstteki hesap/avatar menüsünden **Dil** ile Türkçe/English, **Tema** ile Açık/Koyu arasında hızlıca geçebilirsin. Aynı menüde **Ayarlar → Görünüm** bölümünü açarsan tema ve dile ek olarak vurgu renk paletini de seçebilirsin. Ziyaretçide dil ve tema kontrolleri üst bardadır; görünüm seçimi tarayıcıda saklanır.

### 366 · PASS · Öğrenci

- Soru: zil menüsündeki tüm uyarıları temizlemek istiyorum
- Beklenen intent: `notification_settings_info`
- Gerçek intent: `notification_settings_info`
- response_id: `notification_settings_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Şu an bildirimleri olay türüne göre açıp kapatan veya ses/e-posta tercihi sunan ayrı bir ayar ekranı yok. Üst bardaki **zil** simgesi Bildirim Merkezi'ni açar; mesaj, etkinlik, sınav ve ödev bildirimlerini burada görürsün. Bir bildirimi **× / Sil** ile kapatabilir ya da **Tümünü sil** ile listeyi temizleyebilirsin. Bildirime basmak ilgili sayfayı açar; mesaj bildirimi ayrıca okundu olarak işaretlenir.

### 367 · PASS · Öğretmen

- Soru: bir bildirimi listeden nasıl kaldırırım
- Beklenen intent: `notification_settings_info`
- Gerçek intent: `notification_settings_info`
- response_id: `notification_settings_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Şu an bildirimleri olay türüne göre açıp kapatan veya ses/e-posta tercihi sunan ayrı bir ayar ekranı yok. Üst bardaki **zil** simgesi Bildirim Merkezi'ni açar; mesaj, etkinlik, sınav ve ödev bildirimlerini burada görürsün. Bir bildirimi **× / Sil** ile kapatabilir ya da **Tümünü sil** ile listeyi temizleyebilirsin. Bildirime basmak ilgili sayfayı açar; mesaj bildirimi ayrıca okundu olarak işaretlenir.

### 368 · PASS · Yönetici

- Soru: yalnız e-posta bildirimi açma seçeneği var mı
- Beklenen intent: `notification_settings_info`
- Gerçek intent: `notification_settings_info`
- response_id: `notification_settings_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Şu an bildirimleri olay türüne göre açıp kapatan veya ses/e-posta tercihi sunan ayrı bir ayar ekranı yok. Üst bardaki **zil** simgesi Bildirim Merkezi'ni açar; mesaj, etkinlik, sınav ve ödev bildirimlerini burada görürsün. Bir bildirimi **× / Sil** ile kapatabilir ya da **Tümünü sil** ile listeyi temizleyebilirsin. Bildirime basmak ilgili sayfayı açar; mesaj bildirimi ayrıca okundu olarak işaretlenir.

### 369 · PASS · Veli

- Soru: mesaj bildirimine basınca ne oluyor
- Beklenen intent: `notification_settings_info`
- Gerçek intent: `notification_settings_info`
- response_id: `notification_settings_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Şu an bildirimleri olay türüne göre açıp kapatan veya ses/e-posta tercihi sunan ayrı bir ayar ekranı yok. Üst bardaki **zil** simgesi Bildirim Merkezi'ni açar; mesaj, etkinlik, sınav ve ödev bildirimlerini burada görürsün. Bir bildirimi **× / Sil** ile kapatabilir ya da **Tümünü sil** ile listeyi temizleyebilirsin. Bildirime basmak ilgili sayfayı açar; mesaj bildirimi ayrıca okundu olarak işaretlenir.

### 370 · PASS · Öğrenci

- Soru: 409 çakışma hatası aldım neyi kontrol etmeliyim
- Beklenen intent: `technical_error_help`
- Gerçek intent: `technical_error_help`
- response_id: `technical_error_triage`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hatanın nedenini ayırabilmem için **hangi sayfada hangi düğmeye bastığını** ve ekrandaki hata metnini aynen yaz. Genel anlamı şöyledir: **400** alan/değer iş kuralına uymuyor, **401** oturum yok/süresi dolmuş, **403** rol veya ders/öğrenci kapsamı yetersiz, **404** kayıt yok ya da güvenlik için gizlenmiş, **409** işlem mevcut durumla çakışıyor, **413** dosya okul sınırını aşıyor, **422** istek gövdesinde zorunlu alan/tip/biçim yanlış, **429** çok sık istek gönderildiği, **503** hizmet/veritabanı geçici olarak ulaşılamadığı anlamına gelir. 401'de yeniden giriş yap; 429/503'te kısa süre bekleyip bir kez daha dene. Yazma isteği zaman aşımına uğradıysa işlemi tekrarlamadan önce kaydın oluşup oluşmadığını kontrol et.

### 371 · PASS · Öğretmen

- Soru: dosya yüklerken 413 döndü
- Beklenen intent: `upload_problem`
- Gerçek intent: `upload_problem`
- response_id: `upload_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Dosya yüklemede önce alanı ayır: **400**; multipart içindeki `file` alanı eksik, dosya boş veya gövde bozuk olabilir. **413**, dosyanın sunucu/okul boyut sınırını aştığını gösterir; güncel sınır okulun Sistem ayarındadır (varsayılan yaklaşık 5 MiB). Defter, ders notu ve ödev tesliminde kayıt başına en fazla **10 dosya** vardır; önce bir eki sil. Satır içinde gösterilecek görseller yalnız PNG/JPEG/WebP/GIF'tir; SVG desteklenmez. Hata sürerse hangi sayfada yüklediğini, dosya türü/boyutunu ve tam hata metnini yaz; kişisel dosya içeriğini sohbete kopyalama.

### 372 · PASS · Öğrenci

- Soru: 429 çok fazla istek uyarısı ne demek
- Beklenen intent: `technical_error_help`
- Gerçek intent: `technical_error_help`
- response_id: `technical_error_triage`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hatanın nedenini ayırabilmem için **hangi sayfada hangi düğmeye bastığını** ve ekrandaki hata metnini aynen yaz. Genel anlamı şöyledir: **400** alan/değer iş kuralına uymuyor, **401** oturum yok/süresi dolmuş, **403** rol veya ders/öğrenci kapsamı yetersiz, **404** kayıt yok ya da güvenlik için gizlenmiş, **409** işlem mevcut durumla çakışıyor, **413** dosya okul sınırını aşıyor, **422** istek gövdesinde zorunlu alan/tip/biçim yanlış, **429** çok sık istek gönderildiği, **503** hizmet/veritabanı geçici olarak ulaşılamadığı anlamına gelir. 401'de yeniden giriş yap; 429/503'te kısa süre bekleyip bir kez daha dene. Yazma isteği zaman aşımına uğradıysa işlemi tekrarlamadan önce kaydın oluşup oluşmadığını kontrol et.

### 373 · PASS · Yönetici

- Soru: veritabanı 503 döndürdü tekrar deneyeyim mi
- Beklenen intent: `technical_error_help`
- Gerçek intent: `technical_error_help`
- response_id: `technical_error_triage`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hatanın nedenini ayırabilmem için **hangi sayfada hangi düğmeye bastığını** ve ekrandaki hata metnini aynen yaz. Genel anlamı şöyledir: **400** alan/değer iş kuralına uymuyor, **401** oturum yok/süresi dolmuş, **403** rol veya ders/öğrenci kapsamı yetersiz, **404** kayıt yok ya da güvenlik için gizlenmiş, **409** işlem mevcut durumla çakışıyor, **413** dosya okul sınırını aşıyor, **422** istek gövdesinde zorunlu alan/tip/biçim yanlış, **429** çok sık istek gönderildiği, **503** hizmet/veritabanı geçici olarak ulaşılamadığı anlamına gelir. 401'de yeniden giriş yap; 429/503'te kısa süre bekleyip bir kez daha dene. Yazma isteği zaman aşımına uğradıysa işlemi tekrarlamadan önce kaydın oluşup oluşmadığını kontrol et.

### 374 · PASS · Öğrenci

- Soru: kaydet düğmesine bastım ama çalışmıyor
- Beklenen intent: `technical_error_help`
- Gerçek intent: `technical_error_help`
- response_id: `technical_error_triage`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hatanın nedenini ayırabilmem için **hangi sayfada hangi düğmeye bastığını** ve ekrandaki hata metnini aynen yaz. Genel anlamı şöyledir: **400** alan/değer iş kuralına uymuyor, **401** oturum yok/süresi dolmuş, **403** rol veya ders/öğrenci kapsamı yetersiz, **404** kayıt yok ya da güvenlik için gizlenmiş, **409** işlem mevcut durumla çakışıyor, **413** dosya okul sınırını aşıyor, **422** istek gövdesinde zorunlu alan/tip/biçim yanlış, **429** çok sık istek gönderildiği, **503** hizmet/veritabanı geçici olarak ulaşılamadığı anlamına gelir. 401'de yeniden giriş yap; 429/503'te kısa süre bekleyip bir kez daha dene. Yazma isteği zaman aşımına uğradıysa işlemi tekrarlamadan önce kaydın oluşup oluşmadığını kontrol et.

### 375 · PASS · Veli

- Soru: isteğim başarısız oldu hata metnini nereye yazayım
- Beklenen intent: `technical_error_help`
- Gerçek intent: `technical_error_help`
- response_id: `technical_error_triage`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hatanın nedenini ayırabilmem için **hangi sayfada hangi düğmeye bastığını** ve ekrandaki hata metnini aynen yaz. Genel anlamı şöyledir: **400** alan/değer iş kuralına uymuyor, **401** oturum yok/süresi dolmuş, **403** rol veya ders/öğrenci kapsamı yetersiz, **404** kayıt yok ya da güvenlik için gizlenmiş, **409** işlem mevcut durumla çakışıyor, **413** dosya okul sınırını aşıyor, **422** istek gövdesinde zorunlu alan/tip/biçim yanlış, **429** çok sık istek gönderildiği, **503** hizmet/veritabanı geçici olarak ulaşılamadığı anlamına gelir. 401'de yeniden giriş yap; 429/503'te kısa süre bekleyip bir kez daha dene. Yazma isteği zaman aşımına uğradıysa işlemi tekrarlamadan önce kaydın oluşup oluşmadığını kontrol et.

### 376 · PASS · ADMIN

- Soru: yazma isteği zaman aşımına uğradı yeniden göndereyim mi
- Beklenen intent: `technical_error_help`
- Gerçek intent: `technical_error_help`
- response_id: `technical_error_triage`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hatanın nedenini ayırabilmem için **hangi sayfada hangi düğmeye bastığını** ve ekrandaki hata metnini aynen yaz. Genel anlamı şöyledir: **400** alan/değer iş kuralına uymuyor, **401** oturum yok/süresi dolmuş, **403** rol veya ders/öğrenci kapsamı yetersiz, **404** kayıt yok ya da güvenlik için gizlenmiş, **409** işlem mevcut durumla çakışıyor, **413** dosya okul sınırını aşıyor, **422** istek gövdesinde zorunlu alan/tip/biçim yanlış, **429** çok sık istek gönderildiği, **503** hizmet/veritabanı geçici olarak ulaşılamadığı anlamına gelir. 401'de yeniden giriş yap; 429/503'te kısa süre bekleyip bir kez daha dene. Yazma isteği zaman aşımına uğradıysa işlemi tekrarlamadan önce kaydın oluşup oluşmadığını kontrol et.

### 377 · PASS · Öğrenci

- Soru: oturum süresi dolduğu için 401 alıyorum
- Beklenen intent: `session_info`
- Gerçek intent: `session_info`
- response_id: `session_duration_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Giriş yapınca **7 gün** geçerli bir oturum açılır. Süre sunucu saatiyle ölçülür; cihazının saati yanlış olsa bile değişmez. Çıkış yapmak oturumu hemen kapatır. Süre dolduktan sonra korumalı bir istek **401** dönebilir; bu durumda `/login` üzerinden yeniden giriş yap.

### 378 · PASS · Öğretmen

- Soru: 403 rol mü ders yetkisi mi demek
- Beklenen intent: `access_denied_help`
- Gerçek intent: `access_denied_help`
- response_id: `access_denied_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Oturumun yoksa korumalı sayfa seni `/login`'e gönderir. Giriş yaptığın halde rolün sayfaya uymuyorsa kırmızı **"Bu içeriğe erişimin yok."** kutusu görünür. Bir işlem çağrısındaki **403** rolünün, ders yönetiminin, kaydının veya hedef öğrenci kapsamının yetersiz olduğunu gösterebilir; **404** bazen var olmayan kaydı, bazen de güvenlik için gizlenen yetkisiz kaydı ifade eder.

### 379 · PASS · Yönetici

- Soru: yetkisiz kayıt neden 404 gibi görünüyor
- Beklenen intent: `access_denied_help`
- Gerçek intent: `access_denied_help`
- response_id: `access_denied_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Oturumun yoksa korumalı sayfa seni `/login`'e gönderir. Giriş yaptığın halde rolün sayfaya uymuyorsa kırmızı **"Bu içeriğe erişimin yok."** kutusu görünür. Bir işlem çağrısındaki **403** rolünün, ders yönetiminin, kaydının veya hedef öğrenci kapsamının yetersiz olduğunu gösterebilir; **404** bazen var olmayan kaydı, bazen de güvenlik için gizlenen yetkisiz kaydı ifade eder.

### 380 · PASS · ADMIN

- Soru: admin neden pomodoro başlatamıyor
- Beklenen intent: `pomodoro_use`
- Gerçek intent: `pomodoro_use`
- response_id: `pomodoro_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 381 · PASS · ADMIN

- Soru: admin kendi mesai girişini yapabilir mi
- Beklenen intent: `work_checkin_out`
- Gerçek intent: `work_checkin_out`
- response_id: `work_checkin_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 382 · PASS · Öğretmen

- Soru: öğretmen öğrenci gibi sınav odasına girebilir mi
- Beklenen intent: `exam_enter_room`
- Gerçek intent: `exam_enter_room`
- response_id: `exam_enter_room_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 383 · PASS · Yönetici

- Soru: üst rol her öğrenci işlemini yapabilir mi
- Beklenen intent: `roles_permissions`
- Gerçek intent: `roles_permissions`
- response_id: `roles_overview`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hezarfen'de roller şöyle sıralanır: **Veli < Öğrenci < Öğretmen < Yönetici < ADMIN**; ancak yetki modeli 'üst rol alttaki her şeyi yapar' şeklinde değildir. **Veli** bağlı çocuklarını salt-okunur izler; **Öğrenci** sınava girer, ödev teslim eder ve Pomodoro kullanır; **Öğretmen** yönettiği ders/sınav/yoklama işlemlerini yapar; **Yönetici** okul geneli ayar ve kayıtları yönetir; **ADMIN** kullanıcı/rol yönetir. Örneğin `/pomodoro` ve sınav odası yalnız Öğrenci; `/work` bağlantısı arayüzde yalnız Öğretmen/Yöneticiye gösterilir (backend Teacher+ kontrolü ADMIN isteğini de teknik olarak kabul eder). Yeni hesap Öğrenci başlar; rolü ADMIN atar. Kendi rolünü hesap menüsündeki rozetten görebilirsin.

### 384 · PASS · Öğretmen

- Soru: telefonda sınavlar sekmesini göremiyorum
- Beklenen intent: `navigation_help`
- Gerçek intent: `navigation_help`
- response_id: `navigation_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ana sayfa", "route": "/"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Masaüstünde sol dikey menüden gezinilir; gruplar rol bazlıdır ve yetkin olmayan öğeler gizlenir. Mobil alt çubuk da role göre değişir: Öğrencide **Bugün, Eğitim, Takvim, Karnem, Hesap**; Öğretmen/Yönetici/ADMIN'de **Bugün, Eğitim, Takvim, Hesap**; Velide **Bugün, Çocuklarım, Takvim, Hesap** görünür. Diğer sayfalara **Hesap/Menü** içinden ulaşırsın. Aradığın sayfayı söylersen gerçek yolunu verebilirim.

### 385 · PASS · Veli

- Soru: veli mobil menüsünde neden dersler yok
- Beklenen intent: `navigation_help`
- Gerçek intent: `navigation_help`
- response_id: `navigation_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ana sayfa", "route": "/"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Masaüstünde sol dikey menüden gezinilir; gruplar rol bazlıdır ve yetkin olmayan öğeler gizlenir. Mobil alt çubuk da role göre değişir: Öğrencide **Bugün, Eğitim, Takvim, Karnem, Hesap**; Öğretmen/Yönetici/ADMIN'de **Bugün, Eğitim, Takvim, Hesap**; Velide **Bugün, Çocuklarım, Takvim, Hesap** görünür. Diğer sayfalara **Hesap/Menü** içinden ulaşırsın. Aradığın sayfayı söylersen gerçek yolunu verebilirim.

### 386 · PASS · Öğrenci

- Soru: öğrencinin mobil alt menüsünde hangi sekmeler var
- Beklenen intent: `navigation_help`
- Gerçek intent: `navigation_help`
- response_id: `navigation_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ana sayfa", "route": "/"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Masaüstünde sol dikey menüden gezinilir; gruplar rol bazlıdır ve yetkin olmayan öğeler gizlenir. Mobil alt çubuk da role göre değişir: Öğrencide **Bugün, Eğitim, Takvim, Karnem, Hesap**; Öğretmen/Yönetici/ADMIN'de **Bugün, Eğitim, Takvim, Hesap**; Velide **Bugün, Çocuklarım, Takvim, Hesap** görünür. Diğer sayfalara **Hesap/Menü** içinden ulaşırsın. Aradığın sayfayı söylersen gerçek yolunu verebilirim.

### 387 · PASS · Yönetici

- Soru: okul ayarlarında chatbot mesaj sınırı nerede
- Beklenen intent: `school_settings`
- Gerçek intent: `school_settings`
- response_id: `school_settings_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ayarlar", "route": "/management/settings"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> `/management/settings` (Okul ayarları) sayfasında **Değerlendirme** sekmesinde sınav türü/ağırlığı, yoklama durumları ve not bantları; **Yemekhane** sekmesinde rezervasyon kapanış süresi, öğün saatleri ve beslenme etiketleri; **Sistem** sekmesinde not/dosya yükleme limiti ile Çelebi sohbet geçmişi, konu ve mesaj limitleri yönetilir. **Satır ekle** ile ekle, çöp kutusuyla sil, sonra **Kaydet**. Bu okul geneli sayfa kişisel hesap/avatar **Ayarlar** penceresinden farklıdır.

### 388 · PASS · ADMIN

- Soru: öğün saatlerini okul genelinde ayarlamak istiyorum
- Beklenen intent: `school_settings`
- Gerçek intent: `school_settings`
- response_id: `school_settings_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ayarlar", "route": "/management/settings"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> `/management/settings` (Okul ayarları) sayfasında **Değerlendirme** sekmesinde sınav türü/ağırlığı, yoklama durumları ve not bantları; **Yemekhane** sekmesinde rezervasyon kapanış süresi, öğün saatleri ve beslenme etiketleri; **Sistem** sekmesinde not/dosya yükleme limiti ile Çelebi sohbet geçmişi, konu ve mesaj limitleri yönetilir. **Satır ekle** ile ekle, çöp kutusuyla sil, sonra **Kaydet**. Bu okul geneli sayfa kişisel hesap/avatar **Ayarlar** penceresinden farklıdır.

### 389 · PASS · Yönetici

- Soru: beslenme etiketleri hangi ayarlar sekmesinde
- Beklenen intent: `school_settings`
- Gerçek intent: `school_settings`
- response_id: `school_settings_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ayarlar", "route": "/management/settings"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> `/management/settings` (Okul ayarları) sayfasında **Değerlendirme** sekmesinde sınav türü/ağırlığı, yoklama durumları ve not bantları; **Yemekhane** sekmesinde rezervasyon kapanış süresi, öğün saatleri ve beslenme etiketleri; **Sistem** sekmesinde not/dosya yükleme limiti ile Çelebi sohbet geçmişi, konu ve mesaj limitleri yönetilir. **Satır ekle** ile ekle, çöp kutusuyla sil, sonra **Kaydet**. Bu okul geneli sayfa kişisel hesap/avatar **Ayarlar** penceresinden farklıdır.

### 390 · PASS · Öğretmen

- Soru: sınıf dolu olduğu için öğrenci ekleyemiyorum
- Beklenen intent: `course_enroll_student`
- Gerçek intent: `course_enroll_student`
- response_id: `enroll_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: bu dersi yönetme yetkin olmalı. 1) Ders detayına (`/courses/$id`) gir, **Sınıf listesi (Roster)** bölümünü aç. 2) **Öğrenci kaydet (Enroll student)**'e bas, panelde öğrenciyi ara-seç. 3) Onayla. Zaten kayıtlılar listede çıkmaz; öğrenci seçmezsen 'Önce bir öğrenci seçmelisin.' uyarısı çıkar. Yalnız **Öğrenci** rolündeki hesaplar derse kaydedilebilir; sınıf doluysa işlem 409 ile reddedilir. Sınıf listesi yalnızca dersi yönetebilen hesaba görünür.

### 391 · PASS · Yönetici

- Soru: öğretmen hesabını öğrenci diye derse kaydedebilir miyim
- Beklenen intent: `course_enroll_student`
- Gerçek intent: `course_enroll_student`
- response_id: `enroll_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: bu dersi yönetme yetkin olmalı. 1) Ders detayına (`/courses/$id`) gir, **Sınıf listesi (Roster)** bölümünü aç. 2) **Öğrenci kaydet (Enroll student)**'e bas, panelde öğrenciyi ara-seç. 3) Onayla. Zaten kayıtlılar listede çıkmaz; öğrenci seçmezsen 'Önce bir öğrenci seçmelisin.' uyarısı çıkar. Yalnız **Öğrenci** rolündeki hesaplar derse kaydedilebilir; sınıf doluysa işlem 409 ile reddedilir. Sınıf listesi yalnızca dersi yönetebilen hesaba görünür.

### 392 · PASS · Öğretmen

- Soru: dersten çıkardığım öğrencinin eski sınav sonuçları silinir mi
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 393 · PASS · Öğretmen

- Soru: öğrenciyi roster listesinden kaldıramadım
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 394 · PASS · Öğretmen

- Soru: derse yeni bir oturum eklemem gerekiyor
- Beklenen intent: `lesson_session_add`
- Gerçek intent: `lesson_session_add`
- response_id: `lesson_session_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ders yönetim yetkisi. 1) Ders detayı → **Ders oturumları (Lesson sessions)** → **Oturum ekle (Add session)**. 2) İsteğe bağlı **Konu**, **Başlangıç** tarih (GG/AA/YYYY) + saat, isteğe bağlı **Bitiş**. 3) **Oturum ekle**. Başlangıç zorunlu ve gelecekte olmalı; bitiş başlangıçtan önce olamaz. 'Derse yeni oturum ekleyemiyorum' gibi bir durumda önce ders yönetim yetkini ve tarih sırasını kontrol et.

### 395 · PASS · Öğretmen

- Soru: ders oturumunun bitişi başlangıçtan önce hatası veriyor
- Beklenen intent: `lesson_session_add`
- Gerçek intent: `lesson_session_add`
- response_id: `lesson_session_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ders yönetim yetkisi. 1) Ders detayı → **Ders oturumları (Lesson sessions)** → **Oturum ekle (Add session)**. 2) İsteğe bağlı **Konu**, **Başlangıç** tarih (GG/AA/YYYY) + saat, isteğe bağlı **Bitiş**. 3) **Oturum ekle**. Başlangıç zorunlu ve gelecekte olmalı; bitiş başlangıçtan önce olamaz. 'Derse yeni oturum ekleyemiyorum' gibi bir durumda önce ders yönetim yetkini ve tarih sırasını kontrol et.

### 396 · PASS · Öğrenci

- Soru: sınav oluşturma sadece sınav modlarını açıkla
- Beklenen intent: `exam_modes_info`
- Gerçek intent: `exam_modes_info`
- response_id: `exam_modes_explained`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Dört sınav modu vardır: **Zamansız** (çevrimdışı notlanır, girilemez), **Senkron** (herkes tek sabit aralıkta girer), **Asenkron** (aralık içinde istediğin an başlar, kişisel süre alırsın), **Açık** (her zaman girilebilir, hep 'Aktif' sayılır). Süre 1 dakika–24 saat arasıdır.

### 397 · PASS · Öğrenci

- Soru: sınav başlamadı uyarısı yüzünden odaya giremiyorum
- Beklenen intent: `exam_enter_room`
- Gerçek intent: `exam_enter_room`
- response_id: `exam_enter_room_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: sınavın dersine kayıtlı olmak; sınav girilebilir modda (Senkron/Asenkron/Açık) ve **Aktif** olmalı. 1) Sınav detayında (`/exams/$id`) **Sınav odasını aç (Open exam room)**'a bas. 2) **Sınava başla (Start exam)**. Sorular ve **Kalan süre** görünür. Giremiyorsan en sık nedenler: sınav henüz başlamadı veya bitti, **Zamansız** modda, derse kayıtlı değilsin, önceki deneme zaten teslim edildi, süre doldu ya da deneme hakkın kalmadı.

### 398 · PASS · Öğrenci

- Soru: deneme hakkım kalmadığı için sınav açılmıyor
- Beklenen intent: `exam_rejoin_retake`
- Gerçek intent: `exam_rejoin_retake`
- response_id: `exam_rejoin_retake_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Rejoin (aynı denemeye dönüş):** 'Yeniden girişe izin ver' açıksa odadan çıktıktan sonra tekrar **Sınav odasını aç** → **Sınava devam et**; kalan süre ve cevapların korunur. **Retake (yeni deneme):** 'Deneme hakkı' açık ve azami sayı belirlenmişse her yeni giriş bir deneme kullanır. **Süre çıkışta bile durmaz.** 'Yeniden giriş kapalı', 'deneme hakkı kalmadı', 'süre doldu' veya 'deneme zaten teslim edildi' durumunda aynı denemeye dönemezsin.

### 399 · PASS · Öğrenci

- Soru: zamansız sınavın odasına neden girilmiyor
- Beklenen intent: `exam_enter_room`
- Gerçek intent: `exam_enter_room`
- response_id: `exam_enter_room_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: sınavın dersine kayıtlı olmak; sınav girilebilir modda (Senkron/Asenkron/Açık) ve **Aktif** olmalı. 1) Sınav detayında (`/exams/$id`) **Sınav odasını aç (Open exam room)**'a bas. 2) **Sınava başla (Start exam)**. Sorular ve **Kalan süre** görünür. Giremiyorsan en sık nedenler: sınav henüz başlamadı veya bitti, **Zamansız** modda, derse kayıtlı değilsin, önceki deneme zaten teslim edildi, süre doldu ya da deneme hakkın kalmadı.

### 400 · PASS · Öğretmen

- Soru: ilk öğrenci başladıktan sonra sınav sorusunu değiştirebilir miyim
- Beklenen intent: `exam_add_question`
- Gerçek intent: `exam_add_question`
- response_id: `exam_add_question_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: yönetim yetkisi ve sınavda henüz başlamış bir öğrenci denemesi olmaması. Ayrıca ders detayında en az bir **Konu (Subject)** tanımlı olmalı — her sınav sorusu bir konuya bağlanır. 1) Sınav detayı → **Sorular (Questions)** → **Soru ekle**. 2) **Soru metni** + **Puan** (1–100) + **Konu** seç. 3) **Soru türü**: Seçmeli (2–10 şık, doğru şıkkı işaretle) veya Metin. 4) **Oluştur**. Metin sorular otomatik puanlanmaz, elle notlanır. Herhangi bir öğrenci sınav denemesine başladıktan sonra soru ekleme/değiştirme 409 ile engellenir.

### 401 · PASS · Öğretmen

- Soru: sınav sorusu değiştirirken attempts started hatası aldım
- Beklenen intent: `exam_add_question`
- Gerçek intent: `exam_add_question`
- response_id: `exam_add_question_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: yönetim yetkisi ve sınavda henüz başlamış bir öğrenci denemesi olmaması. Ayrıca ders detayında en az bir **Konu (Subject)** tanımlı olmalı — her sınav sorusu bir konuya bağlanır. 1) Sınav detayı → **Sorular (Questions)** → **Soru ekle**. 2) **Soru metni** + **Puan** (1–100) + **Konu** seç. 3) **Soru türü**: Seçmeli (2–10 şık, doğru şıkkı işaretle) veya Metin. 4) **Oluştur**. Metin sorular otomatik puanlanmaz, elle notlanır. Herhangi bir öğrenci sınav denemesine başladıktan sonra soru ekleme/değiştirme 409 ile engellenir.

### 402 · PASS · Öğretmen

- Soru: kendi hesabıma sınav notu veremiyorum
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 403 · PASS · Yönetici

- Soru: ayar listesinden silinen sınav türüne not girerken 409 aldım
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 404 · PASS · Öğrenci

- Soru: yeniden giriş kapalı olduğu için sınava dönemiyorum
- Beklenen intent: `exam_rejoin_retake`
- Gerçek intent: `exam_rejoin_retake`
- response_id: `exam_rejoin_retake_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Rejoin (aynı denemeye dönüş):** 'Yeniden girişe izin ver' açıksa odadan çıktıktan sonra tekrar **Sınav odasını aç** → **Sınava devam et**; kalan süre ve cevapların korunur. **Retake (yeni deneme):** 'Deneme hakkı' açık ve azami sayı belirlenmişse her yeni giriş bir deneme kullanır. **Süre çıkışta bile durmaz.** 'Yeniden giriş kapalı', 'deneme hakkı kalmadı', 'süre doldu' veya 'deneme zaten teslim edildi' durumunda aynı denemeye dönemezsin.

### 405 · PASS · Öğrenci

- Soru: teslim edilmiş denemeye tekrar bağlanabilir miyim
- Beklenen intent: `exam_rejoin_retake`
- Gerçek intent: `exam_rejoin_retake`
- response_id: `exam_rejoin_retake_info`
- confidence: `0.3727`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Rejoin (aynı denemeye dönüş):** 'Yeniden girişe izin ver' açıksa odadan çıktıktan sonra tekrar **Sınav odasını aç** → **Sınava devam et**; kalan süre ve cevapların korunur. **Retake (yeni deneme):** 'Deneme hakkı' açık ve azami sayı belirlenmişse her yeni giriş bir deneme kullanır. **Süre çıkışta bile durmaz.** 'Yeniden giriş kapalı', 'deneme hakkı kalmadı', 'süre doldu' veya 'deneme zaten teslim edildi' durumunda aynı denemeye dönemezsin.

### 406 · PASS · Öğrenci

- Soru: notlandırılan ödev teslimimi artık değiştiremiyorum
- Beklenen intent: `homework_submit`
- Gerçek intent: `homework_submit`
- response_id: `homework_submit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ödevin verildiği dersin kayıtlı öğrencisisin. 1) **Ödevler** (`/homework`) → ilgili ödevin detayına (`/homework/$id`) gir. 2) **Ödevi teslim et** panelinde cevabını yaz ve/veya dosya ekle. 3) Gönder. Teslim yalnızca Öğrenciye açıktır; **Son teslim** tarihine dikkat et. Teslim notlandırıldıktan sonra öğrenci metni veya dosyayı değiştiremez/silemez; dosya okulun yükleme sınırını aşarsa 413 hatası alınır.

### 407 · PASS · Öğrenci

- Soru: ödev dosyam okul limitini aşıp 413 veriyor
- Beklenen intent: `homework_submit`
- Gerçek intent: `homework_submit`
- response_id: `homework_submit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ödevin verildiği dersin kayıtlı öğrencisisin. 1) **Ödevler** (`/homework`) → ilgili ödevin detayına (`/homework/$id`) gir. 2) **Ödevi teslim et** panelinde cevabını yaz ve/veya dosya ekle. 3) Gönder. Teslim yalnızca Öğrenciye açıktır; **Son teslim** tarihine dikkat et. Teslim notlandırıldıktan sonra öğrenci metni veya dosyayı değiştiremez/silemez; dosya okulun yükleme sınırını aşarsa 413 hatası alınır.

### 408 · PASS · Öğrenci

- Soru: defter notuna on birinci dosyayı ekleyemiyorum
- Beklenen intent: `note_file_manage`
- Gerçek intent: `note_file_manage`
- response_id: `note_file_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel not eklerini yönetmek için **Defter** (`/notes`) sayfasında not kartını aç ve okuyucu içindeki **Ekler** bölümüne git. **Dosya ekle** ile yükleyebilir, dosya kartından **Görüntüle** veya **İndir** diyebilir, **Sil** ile yalnız o eki onaylayarak kaldırabilirsin; çizimler için **Çizim** seçeneği de vardır. Her not en fazla **10 dosya** taşır ve dosya başına okulun `max_file_bytes` sınırı uygulanır (varsayılan yaklaşık 5 MiB): tavan doluysa önce bir eki sil, fazla boyutta 413 alınır. Boş veya bozuk multipart dosya 400'dür. Bazı türler uygulama içinde önizlenmez; bu, dosyanın kaybolduğu anlamına gelmez, **İndir** ile açabilirsin. Kişisel not ve ekleri yalnız sahibine aittir; başka kullanıcının notu 404 ile gizlenir.

### 409 · PASS · Öğrenci

- Soru: başkasına ait defter notu neden bulunamadı görünüyor
- Beklenen intent: `privacy_security`
- Gerçek intent: `privacy_security`
- response_id: `privacy_policy_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yalnızca kendi yetkili olduğun bilgileri görebilirsin. Başka bir kullanıcının notu, yoklaması veya kişisel bilgisi paylaşılmaz. Öğretmen ve üstü roller, yalnızca yetkili oldukları yönetim sayfalarından (Öğrenci notları/yoklaması) öğrenci verisine erişebilir; kişisel telefon/e-posta paylaşılmaz.

### 410 · PASS · Öğretmen

- Soru: zaten mesai girişi yaptın uyarısında ne yapmalıyım
- Beklenen intent: `work_checkin_out`
- Gerçek intent: `work_checkin_out`
- response_id: `work_checkin_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Mesai", "route": "/work"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Arayüzde `/work` bağlantısı Öğretmen/Yönetici hesabında görünür; ADMIN navigasyonunda gösterilmez (backend Teacher+ kontrolü ADMIN çağrısını da kabul eder). 1) `/work` (Mesai) sayfasını aç. 2) 'Giriş yapılmadı' ise **Giriş yap (Check in)**; iş bitince **Çıkış yap (Check out)**. 3) **Son kayıtlar**'da giriş/çıkış/süre ve Açık/Kapalı durumunu görürsün. Saatler sunucu damgalıdır; aynı anda tek açık mesai olabilir. 'Zaten giriş yaptın' hatasında önce açık kaydı **Çıkış yap** ile kapat; 'giriş yapılmadı' hatasında çıkıştan önce **Giriş yap**.

### 411 · PASS · Yönetici

- Soru: giriş yapmadan mesai çıkışı veremiyorum
- Beklenen intent: `work_checkin_out`
- Gerçek intent: `work_checkin_out`
- response_id: `work_checkin_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Mesai", "route": "/work"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Arayüzde `/work` bağlantısı Öğretmen/Yönetici hesabında görünür; ADMIN navigasyonunda gösterilmez (backend Teacher+ kontrolü ADMIN çağrısını da kabul eder). 1) `/work` (Mesai) sayfasını aç. 2) 'Giriş yapılmadı' ise **Giriş yap (Check in)**; iş bitince **Çıkış yap (Check out)**. 3) **Son kayıtlar**'da giriş/çıkış/süre ve Açık/Kapalı durumunu görürsün. Saatler sunucu damgalıdır; aynı anda tek açık mesai olabilir. 'Zaten giriş yaptın' hatasında önce açık kaydı **Çıkış yap** ile kapat; 'giriş yapılmadı' hatasında çıkıştan önce **Giriş yap**.

### 412 · PASS · Yönetici

- Soru: ders bağlı olduğu için akademik dönemi silemiyorum
- Beklenen intent: `term_manage`
- Gerçek intent: `term_manage`
- response_id: `term_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dönemler", "route": "/management/terms"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/management/terms` (Dönemler) → **Dönem oluştur (Create term)**. 2) **Ad**, **Başlangıç**, **Bitiş** (GG/AA/YYYY) gir; bitiş başlangıçtan önce olamaz (tarihler geçmişte olabilir). 3) **Oluştur**. Dersi döneme bağlamak, ders oluşturma/düzenleme formundaki **Dönem** seçicisinden yapılır. Bir dönem herhangi bir ders veya şubeye bağlıysa silme işlemi 409 ile reddedilir; önce bu bağlantıları kaldırmalısın.

### 413 · PASS · ADMIN

- Soru: şubeye bağlı dönem silinir mi
- Beklenen intent: `term_manage`
- Gerçek intent: `term_manage`
- response_id: `term_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dönemler", "route": "/management/terms"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/management/terms` (Dönemler) → **Dönem oluştur (Create term)**. 2) **Ad**, **Başlangıç**, **Bitiş** (GG/AA/YYYY) gir; bitiş başlangıçtan önce olamaz (tarihler geçmişte olabilir). 3) **Oluştur**. Dersi döneme bağlamak, ders oluşturma/düzenleme formundaki **Dönem** seçicisinden yapılır. Bir dönem herhangi bir ders veya şubeye bağlıysa silme işlemi 409 ile reddedilir; önce bu bağlantıları kaldırmalısın.

### 414 · PASS · Öğretmen

- Soru: öğrenciyi etkinlikte var olarak işaretlemek istiyorum
- Beklenen intent: `event_attendance_mark`
- Gerçek intent: `event_attendance_mark`
- response_id: `event_attendance_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Etkinlikler", "route": "/events"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) `/events` → ilgili etkinlik kartına tıkla. 2) Etkinliğin katılımcı listesinde öğrenci için **Var / Yok / Geç / Mazeretli** durumunu seç. 3) Kaydet. Etkinlik yoklamasını yalnız Öğretmen ve üstü işaretleyebilir; hedef öğrenci etkinliğin katılımcı kitlesinde olmalı. Öğrenci veya Veli kendi katılımını işaretleyemez.

### 415 · PASS · Öğrenci

- Soru: öğrenci kendi etkinlik katılımını kaydedebilir mi
- Beklenen intent: `event_attendance_mark`
- Gerçek intent: `event_attendance_mark`
- response_id: `event_attendance_instructions`
- confidence: `0.5231`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 416 · PASS · Öğretmen

- Soru: öğretmen hesabıyla soru havuzuna yeni soru sorabilir miyim
- Beklenen intent: `question_ask`
- Gerçek intent: `question_ask`
- response_id: `question_ask_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 417 · PASS · ADMIN

- Soru: öğrenciye yemek kredisi yüklemek istiyorum
- Beklenen intent: `meal_credit_manage`
- Gerçek intent: `meal_credit_manage`
- response_id: `meal_credit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Öğrenci yemek kredisi yalnız **ADMIN** tarafından kaydedilebilir. `/meals` sayfasından bir öğün detayını aç, öğrenci hesabını seç ve **Hizmet** sekmesindeki **Kredi kaydet** bölümünde tutar (isteğe bağlı yöntem/not) girip onayla. Kredi kaydı seçili öğüne bağlı değildir; öğrencinin append-only yemek hesabına işlenir. Yönetici menü ve beslenme profillerini düzenleyebilir ancak kredi kaydetme kontrolü onda görünmez.

### 418 · PASS · Yönetici

- Soru: yönetici hesabında kredi kaydet düğmesi niye yok
- Beklenen intent: `meal_credit_manage`
- Gerçek intent: `meal_credit_manage`
- response_id: `meal_credit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 419 · PASS · ADMIN

- Soru: yemek bakiyesine tutar ekleme işlemi nerede
- Beklenen intent: `meal_credit_manage`
- Gerçek intent: `meal_credit_manage`
- response_id: `meal_credit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Öğrenci yemek kredisi yalnız **ADMIN** tarafından kaydedilebilir. `/meals` sayfasından bir öğün detayını aç, öğrenci hesabını seç ve **Hizmet** sekmesindeki **Kredi kaydet** bölümünde tutar (isteğe bağlı yöntem/not) girip onayla. Kredi kaydı seçili öğüne bağlı değildir; öğrencinin append-only yemek hesabına işlenir. Yönetici menü ve beslenme profillerini düzenleyebilir ancak kredi kaydetme kontrolü onda görünmez.

### 420 · PASS · Öğrenci

- Soru: etütleri dersler ekranında nasıl filtrelerim
- Beklenen intent: `study_club_info`
- Gerçek intent: `study_club_info`
- response_id: `study_club_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Etüt", "route": "/studies"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Etüt** ve **Kulüp**, dersin iki özel türüdür — ders altyapısının aynısını kullanırlar (kayıt, oturum, yoklama, sınav). Ayrı sol menü öğeleri değillerdir: **Eğitim/Dersler** (`/courses`) sayfasındaki **Etüt** ve **Kulüp** filtrelerinden açılırlar; `/studies` ve `/clubs` adresleri de bu filtreli listeye yönlendirir. Öğretmen+ oluşturur; öğrenciyi ders yöneticisi roster üzerinden kaydeder, öğrenci kendi kendine kaydolmaz. Kontenjan sınırı konabilir.

### 421 · PASS · Öğrenci

- Soru: kulübe kendi kendime kayıt olabilir miyim
- Beklenen intent: `study_club_info`
- Gerçek intent: `study_club_info`
- response_id: `study_club_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Etüt", "route": "/studies"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Etüt** ve **Kulüp**, dersin iki özel türüdür — ders altyapısının aynısını kullanırlar (kayıt, oturum, yoklama, sınav). Ayrı sol menü öğeleri değillerdir: **Eğitim/Dersler** (`/courses`) sayfasındaki **Etüt** ve **Kulüp** filtrelerinden açılırlar; `/studies` ve `/clubs` adresleri de bu filtreli listeye yönlendirir. Öğretmen+ oluşturur; öğrenciyi ders yöneticisi roster üzerinden kaydeder, öğrenci kendi kendine kaydolmaz. Kontenjan sınırı konabilir.

### 422 · PASS · Veli

- Soru: takvim haftalık değil aylık mı çalışıyor
- Beklenen intent: `calendar_info`
- Gerçek intent: `calendar_info`
- response_id: `calendar_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Takvim", "route": "/calendar"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Takvim** (`/calendar`) aylık görünümde sınav, ödev, etkinlik, randevu ve ders oturumlarını birleştirir. **Bugün** düğmesiyle geçerli aya/güne dönebilir, bir günü seçerek o günün ayrıntılarını görebilirsin.

### 423 · PASS · Öğrenci

- Soru: randevular takvim ekranında gösteriliyor mu
- Beklenen intent: `calendar_info`
- Gerçek intent: `calendar_info`
- response_id: `calendar_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Takvim", "route": "/calendar"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Takvim** (`/calendar`) aylık görünümde sınav, ödev, etkinlik, randevu ve ders oturumlarını birleştirir. **Bugün** düğmesiyle geçerli aya/güne dönebilir, bir günü seçerek o günün ayrıntılarını görebilirsin.

### 424 · PASS · Öğrenci

- Soru: ücretlerim sayfasından borç dökümüne bakmak istiyorum
- Beklenen intent: `fees_info`
- Gerçek intent: `fees_info`
- response_id: `fees_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ücretler", "route": "/payments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kendi okul ücret ve ödeme ekstreni **Ücretlerim** (`/payments`) sayfasından görürsün. Öğrencide kendi borç/ödeme durumu, Velide bağlı çocuğu seçerek salt-okunur ekstre görünür. Okulun tahsilat yönetimi ise ayrı `/management/payments` sayfasıdır.

### 425 · PASS · Veli

- Soru: veliyim çocuğumun ödeme ekstresini nereden açarım
- Beklenen intent: `fees_info`
- Gerçek intent: `fees_info`
- response_id: `fees_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ücretler", "route": "/payments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kendi okul ücret ve ödeme ekstreni **Ücretlerim** (`/payments`) sayfasından görürsün. Öğrencide kendi borç/ödeme durumu, Velide bağlı çocuğu seçerek salt-okunur ekstre görünür. Okulun tahsilat yönetimi ise ayrı `/management/payments` sayfasıdır.

### 426 · PASS · Öğrenci

- Soru: soru bankası öğrenci hesabında neden görünmüyor
- Beklenen intent: `question_bank_info`
- Gerçek intent: `question_bank_info`
- response_id: `question_bank_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 427 · PASS · Öğrenci

- Soru: öğretmenin yüklediği ders dosyasını indiremedim
- Beklenen intent: `course_materials_info`
- Gerçek intent: `course_materials_info`
- response_id: `course_materials_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Öğretmenin yüklediği **ders notları** ve **PDF/dosya**lar ilgili dersin sayfasındadır: **Dersler** (`/courses`) → ders → Ders notları.

### 428 · PASS · Öğrenci

- Soru: profilime giden doğru adres profile me mi
- Beklenen intent: `profile_view`
- Gerçek intent: `profile_view`
- response_id: `profile_view_info`
- confidence: `0.3616`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kendi profilini `/profile/me` adresinden veya hesap menüsündeki **Profilim** seçeneğinden açabilirsin. Burada profil fotoğrafın, görünen adın/Hakkında alanın, rolün, şube ve ders üyeliklerin, rozetlerin ile odak saati, odak oturumu, teslim edilen/zamanında ödev ve girilen sınav istatistiklerin görünür. Kendi sayfanda **Profili düzenle** düğmesi vardır. Başka bir kişinin profili `/profile/$userId` ile açılır; erişim kapsamını backend denetler ve Veli yalnız kendisini veya bağlı çocuklarını görebilir.

### 429 · PASS · Öğrenci

- Soru: hangi ders ve şube üyeliklerim var
- Beklenen intent: `profile_view`
- Gerçek intent: `profile_view`
- response_id: `profile_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kendi profilini `/profile/me` adresinden veya hesap menüsündeki **Profilim** seçeneğinden açabilirsin. Burada profil fotoğrafın, görünen adın/Hakkında alanın, rolün, şube ve ders üyeliklerin, rozetlerin ile odak saati, odak oturumu, teslim edilen/zamanında ödev ve girilen sınav istatistiklerin görünür. Kendi sayfanda **Profili düzenle** düğmesi vardır. Başka bir kişinin profili `/profile/$userId` ile açılır; erişim kapsamını backend denetler ve Veli yalnız kendisini veya bağlı çocuklarını görebilir.

### 430 · PASS · Veli

- Soru: hakkında alanımı tamamen boşaltmak istiyorum
- Beklenen intent: `profile_edit`
- Gerçek intent: `profile_edit`
- response_id: `profile_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Profilini iki yerden güncelleyebilirsin: 1) Sağ üstteki hesap/avatar menüsü → **Ayarlar → Hesap** bölümünde **Ad, Soyad, E-posta, Telefon** ve **Doğum tarihi** alanlarını değiştir. 2) Tam profil ekranı için `/profile/me` adresine git, **Profili düzenle**'ye bas; burada bunlara ek olarak **Görünen ad** ve **Hakkında** alanları da vardır. Profil fotoğrafını da bu sayfadaki avatar üzerinden yükleyebilir, değiştirebilir veya kaldırabilirsin. Sonunda **Kaydet**'e bas. Tüm alanlar isteğe bağlıdır; **kullanıcı adı ve rol buradan değiştirilemez**. E-posta geçerli biçimde, telefon 7–15 hane olmalı; doğum tarihi gelecekte olamaz.

### 431 · PASS · Öğretmen

- Soru: doğum tarihini gelecekte seçince neden kaydetmiyor
- Beklenen intent: `profile_edit`
- Gerçek intent: `profile_edit`
- response_id: `profile_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Profilini iki yerden güncelleyebilirsin: 1) Sağ üstteki hesap/avatar menüsü → **Ayarlar → Hesap** bölümünde **Ad, Soyad, E-posta, Telefon** ve **Doğum tarihi** alanlarını değiştir. 2) Tam profil ekranı için `/profile/me` adresine git, **Profili düzenle**'ye bas; burada bunlara ek olarak **Görünen ad** ve **Hakkında** alanları da vardır. Profil fotoğrafını da bu sayfadaki avatar üzerinden yükleyebilir, değiştirebilir veya kaldırabilirsin. Sonunda **Kaydet**'e bas. Tüm alanlar isteğe bağlıdır; **kullanıcı adı ve rol buradan değiştirilemez**. E-posta geçerli biçimde, telefon 7–15 hane olmalı; doğum tarihi gelecekte olamaz.

### 432 · PASS · Öğrenci

- Soru: ayarlar ayrı sayfa mı yoksa pencere mi
- Beklenen intent: `personal_settings`
- Gerçek intent: `personal_settings`
- response_id: `personal_settings_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel **Ayarlar** bir sayfa değil, sağ üstteki hesap/avatar menüsünden açılan penceredir. **Hesap** bölümünde Ad, Soyad, E-posta, Telefon ve Doğum tarihini; **Görünüm** bölümünde Açık/Koyu tema, Türkçe/English dil ve vurgu renk paletini değiştirebilirsin. Görünen ad, Hakkında ve profil fotoğrafı gibi tam profil seçenekleri için `/profile/me` → **Profili düzenle** yolunu kullan. Okul geneli ayarlar ise bundan ayrıdır ve `/management/settings` altında yalnız yetkili hesaplara görünür.

### 433 · PASS · Veli

- Soru: hesap görünüm bölümünde hangi seçenekler değişir
- Beklenen intent: `personal_settings`
- Gerçek intent: `personal_settings`
- response_id: `personal_settings_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel **Ayarlar** bir sayfa değil, sağ üstteki hesap/avatar menüsünden açılan penceredir. **Hesap** bölümünde Ad, Soyad, E-posta, Telefon ve Doğum tarihini; **Görünüm** bölümünde Açık/Koyu tema, Türkçe/English dil ve vurgu renk paletini değiştirebilirsin. Görünen ad, Hakkında ve profil fotoğrafı gibi tam profil seçenekleri için `/profile/me` → **Profili düzenle** yolunu kullan. Okul geneli ayarlar ise bundan ayrıdır ve `/management/settings` altında yalnız yetkili hesaplara görünür.

### 434 · PASS · Öğrenci

- Soru: profil avatarına svg yükleyemiyorum
- Beklenen intent: `upload_problem`
- Gerçek intent: `upload_problem`
- response_id: `upload_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Dosya yüklemede önce alanı ayır: **400**; multipart içindeki `file` alanı eksik, dosya boş veya gövde bozuk olabilir. **413**, dosyanın sunucu/okul boyut sınırını aştığını gösterir; güncel sınır okulun Sistem ayarındadır (varsayılan yaklaşık 5 MiB). Defter, ders notu ve ödev tesliminde kayıt başına en fazla **10 dosya** vardır; önce bir eki sil. Satır içinde gösterilecek görseller yalnız PNG/JPEG/WebP/GIF'tir; SVG desteklenmez. Hata sürerse hangi sayfada yüklediğini, dosya türü/boyutunu ve tam hata metnini yaz; kişisel dosya içeriğini sohbete kopyalama.

### 435 · PASS · Yönetici

- Soru: kendi profilimde üyelik ve istatistikleri arıyorum
- Beklenen intent: `profile_view`
- Gerçek intent: `profile_view`
- response_id: `profile_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kendi profilini `/profile/me` adresinden veya hesap menüsündeki **Profilim** seçeneğinden açabilirsin. Burada profil fotoğrafın, görünen adın/Hakkında alanın, rolün, şube ve ders üyeliklerin, rozetlerin ile odak saati, odak oturumu, teslim edilen/zamanında ödev ve girilen sınav istatistiklerin görünür. Kendi sayfanda **Profili düzenle** düğmesi vardır. Başka bir kişinin profili `/profile/$userId` ile açılır; erişim kapsamını backend denetler ve Veli yalnız kendisini veya bağlı çocuklarını görebilir.

### 436 · PASS · Öğrenci

- Soru: profil fotoğrafını kaldırınca varsayılan avatar gelir mi
- Beklenen intent: `profile_edit`
- Gerçek intent: `profile_edit`
- response_id: `profile_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Profilini iki yerden güncelleyebilirsin: 1) Sağ üstteki hesap/avatar menüsü → **Ayarlar → Hesap** bölümünde **Ad, Soyad, E-posta, Telefon** ve **Doğum tarihi** alanlarını değiştir. 2) Tam profil ekranı için `/profile/me` adresine git, **Profili düzenle**'ye bas; burada bunlara ek olarak **Görünen ad** ve **Hakkında** alanları da vardır. Profil fotoğrafını da bu sayfadaki avatar üzerinden yükleyebilir, değiştirebilir veya kaldırabilirsin. Sonunda **Kaydet**'e bas. Tüm alanlar isteğe bağlıdır; **kullanıcı adı ve rol buradan değiştirilemez**. E-posta geçerli biçimde, telefon 7–15 hane olmalı; doğum tarihi gelecekte olamaz.

### 437 · PASS · Ziyaretçi

- Soru: kayıt başarılı yazdı ama yeni bilgilerle giriş yapamıyorum
- Beklenen intent: `account_access_problem`
- Gerçek intent: `account_access_problem`
- response_id: `access_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Giriş sayfası", "route": "/login"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hatalı kullanıcı adı/şifrede giriş formunun üstünde aynı kırmızı **401** hata kutusu çıkar; sistem hangi alanın yanlış olduğunu açıklamaz. Kayıt başarılı göründüğü hâlde yeni bilgilerle giriş olmuyorsa aynı kullanıcı adının daha önce alınmış olabileceğini ve kayıt kurallarını kontrol et. Rehberde self-servis bir 'şifremi unuttum' akışı tanımlı değil; kayıtlı bilgilerine erişemiyorsan okul yönetimine başvurman gerekir.

### 438 · PASS · Ziyaretçi

- Soru: kullanıcı adı neden nokta ile başlayamıyor
- Beklenen intent: `register_how`
- Gerçek intent: `register_how`
- response_id: `register_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Kayıt sayfası", "route": "/register"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kayıt için `/register` sayfasına git; **Kullanıcı adı** (3–32), **Şifre** (6–128) ve **Şifreyi onayla (Confirm password)** alanlarını doldurup **Hesap oluştur (Create account)**'a bas. Yeni hesaplar **Öğrenci** olarak başlar; kayıt otomatik giriş yapmaz, giriş sayfasına yönlendirilirsin. Kullanıcı adı yalnız küçük ASCII harf, sayı ve `._-` kabul eder; ayraçla başlayıp/bitemez ve iki ayraç art arda gelemez. 'admin/root/support' gibi personel çağrıştıran adlar reddedilir. Aynı kullanıcı adı yeniden gönderildiğinde güvenlik için yine başarılı kayıt görünümü alınabilir ama ikinci hesap oluşturulmaz.

### 439 · PASS · Ziyaretçi

- Soru: aynı kullanıcı adıyla ikinci hesap açılır mı
- Beklenen intent: `register_how`
- Gerçek intent: `register_how`
- response_id: `register_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Kayıt sayfası", "route": "/register"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kayıt için `/register` sayfasına git; **Kullanıcı adı** (3–32), **Şifre** (6–128) ve **Şifreyi onayla (Confirm password)** alanlarını doldurup **Hesap oluştur (Create account)**'a bas. Yeni hesaplar **Öğrenci** olarak başlar; kayıt otomatik giriş yapmaz, giriş sayfasına yönlendirilirsin. Kullanıcı adı yalnız küçük ASCII harf, sayı ve `._-` kabul eder; ayraçla başlayıp/bitemez ve iki ayraç art arda gelemez. 'admin/root/support' gibi personel çağrıştıran adlar reddedilir. Aynı kullanıcı adı yeniden gönderildiğinde güvenlik için yine başarılı kayıt görünümü alınabilir ama ikinci hesap oluşturulmaz.

### 440 · PASS · Ziyaretçi

- Soru: kullanıcı adı hangi karakterleri kabul ediyor
- Beklenen intent: `register_how`
- Gerçek intent: `register_how`
- response_id: `register_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Kayıt sayfası", "route": "/register"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kayıt için `/register` sayfasına git; **Kullanıcı adı** (3–32), **Şifre** (6–128) ve **Şifreyi onayla (Confirm password)** alanlarını doldurup **Hesap oluştur (Create account)**'a bas. Yeni hesaplar **Öğrenci** olarak başlar; kayıt otomatik giriş yapmaz, giriş sayfasına yönlendirilirsin. Kullanıcı adı yalnız küçük ASCII harf, sayı ve `._-` kabul eder; ayraçla başlayıp/bitemez ve iki ayraç art arda gelemez. 'admin/root/support' gibi personel çağrıştıran adlar reddedilir. Aynı kullanıcı adı yeniden gönderildiğinde güvenlik için yine başarılı kayıt görünümü alınabilir ama ikinci hesap oluşturulmaz.

### 441 · PASS · Ziyaretçi

- Soru: yanlış kullanıcı ile yanlış şifre neden aynı 401 mesajını veriyor
- Beklenen intent: `account_access_problem`
- Gerçek intent: `account_access_problem`
- response_id: `access_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Giriş sayfası", "route": "/login"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hatalı kullanıcı adı/şifrede giriş formunun üstünde aynı kırmızı **401** hata kutusu çıkar; sistem hangi alanın yanlış olduğunu açıklamaz. Kayıt başarılı göründüğü hâlde yeni bilgilerle giriş olmuyorsa aynı kullanıcı adının daha önce alınmış olabileceğini ve kayıt kurallarını kontrol et. Rehberde self-servis bir 'şifremi unuttum' akışı tanımlı değil; kayıtlı bilgilerine erişemiyorsan okul yönetimine başvurman gerekir.

### 442 · PASS · Öğretmen

- Soru: öğrenci silmek istiyorum
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 443 · PASS · Öğretmen

- Soru: öğrenciyi silmek istiyorum
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 444 · PASS · Yönetici

- Soru: ders listesinden öğrenciyi kaldıracağım
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 445 · PASS · Yönetici

- Soru: yeni şube oluştururken kapasiteyi nerede giriyorum
- Beklenen intent: `class_section_manage`
- Gerçek intent: `class_section_manage`
- response_id: `class_section_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Şubeler", "route": "/management/classes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Şube yönetimi için **Şubeler** (`/management/classes`, Yönetici+) sayfasını aç. **Şube oluştur** ile zorunlu sınıf adını; isteğe bağlı sınıf düzeyi, dönem ve sınıf öğretmenini gir. Mevcut şubenin detayında düzenleme/silme, öğrenci ekleme-çıkarma ve ders bağlama-ayırma işlemleri vardır. Oluşturma formunda ayrı bir **kapasite** alanı yoktur. Şubeye öğrenci eklemek bağlı derslere kayıtları tek işlemde kurar; öğrenci zaten üyeyse, şube/ders kapasitesi dolmuşsa veya bağlı ders bulunamazsa işlem 409 ile bütünüyle reddedilir. Üyesi ya da bağlı dersi olan şube silinemez; önce ilişkileri kaldır. Buradaki **şube/sınıf grubu**, `/courses` üzerindeki **ders oluşturma** işleminden farklıdır.

### 446 · PASS · Yönetici

- Soru: sınıf grubu açmak ders açmakla aynı mı
- Beklenen intent: `class_section_manage`
- Gerçek intent: `class_section_manage`
- response_id: `class_section_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Şubeler", "route": "/management/classes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Şube yönetimi için **Şubeler** (`/management/classes`, Yönetici+) sayfasını aç. **Şube oluştur** ile zorunlu sınıf adını; isteğe bağlı sınıf düzeyi, dönem ve sınıf öğretmenini gir. Mevcut şubenin detayında düzenleme/silme, öğrenci ekleme-çıkarma ve ders bağlama-ayırma işlemleri vardır. Oluşturma formunda ayrı bir **kapasite** alanı yoktur. Şubeye öğrenci eklemek bağlı derslere kayıtları tek işlemde kurar; öğrenci zaten üyeyse, şube/ders kapasitesi dolmuşsa veya bağlı ders bulunamazsa işlem 409 ile bütünüyle reddedilir. Üyesi ya da bağlı dersi olan şube silinemez; önce ilişkileri kaldır. Buradaki **şube/sınıf grubu**, `/courses` üzerindeki **ders oluşturma** işleminden farklıdır.

### 447 · PASS · Yönetici

- Soru: şubeye öğrenci eklerken bağlı ders dolu hatası aldım
- Beklenen intent: `class_section_manage`
- Gerçek intent: `class_section_manage`
- response_id: `class_section_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Şubeler", "route": "/management/classes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Şube yönetimi için **Şubeler** (`/management/classes`, Yönetici+) sayfasını aç. **Şube oluştur** ile zorunlu sınıf adını; isteğe bağlı sınıf düzeyi, dönem ve sınıf öğretmenini gir. Mevcut şubenin detayında düzenleme/silme, öğrenci ekleme-çıkarma ve ders bağlama-ayırma işlemleri vardır. Oluşturma formunda ayrı bir **kapasite** alanı yoktur. Şubeye öğrenci eklemek bağlı derslere kayıtları tek işlemde kurar; öğrenci zaten üyeyse, şube/ders kapasitesi dolmuşsa veya bağlı ders bulunamazsa işlem 409 ile bütünüyle reddedilir. Üyesi ya da bağlı dersi olan şube silinemez; önce ilişkileri kaldır. Buradaki **şube/sınıf grubu**, `/courses` üzerindeki **ders oluşturma** işleminden farklıdır.

### 448 · PASS · ADMIN

- Soru: şubeden öğrenciyi çıkarınca ders kayıtları ne olur
- Beklenen intent: `class_section_manage`
- Gerçek intent: `class_section_manage`
- response_id: `class_section_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Şubeler", "route": "/management/classes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Şube yönetimi için **Şubeler** (`/management/classes`, Yönetici+) sayfasını aç. **Şube oluştur** ile zorunlu sınıf adını; isteğe bağlı sınıf düzeyi, dönem ve sınıf öğretmenini gir. Mevcut şubenin detayında düzenleme/silme, öğrenci ekleme-çıkarma ve ders bağlama-ayırma işlemleri vardır. Oluşturma formunda ayrı bir **kapasite** alanı yoktur. Şubeye öğrenci eklemek bağlı derslere kayıtları tek işlemde kurar; öğrenci zaten üyeyse, şube/ders kapasitesi dolmuşsa veya bağlı ders bulunamazsa işlem 409 ile bütünüyle reddedilir. Üyesi ya da bağlı dersi olan şube silinemez; önce ilişkileri kaldır. Buradaki **şube/sınıf grubu**, `/courses` üzerindeki **ders oluşturma** işleminden farklıdır.

### 449 · PASS · Yönetici

- Soru: dersi şubeye bağlamak istiyorum
- Beklenen intent: `class_section_manage`
- Gerçek intent: `class_section_manage`
- response_id: `class_section_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Şubeler", "route": "/management/classes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Şube yönetimi için **Şubeler** (`/management/classes`, Yönetici+) sayfasını aç. **Şube oluştur** ile zorunlu sınıf adını; isteğe bağlı sınıf düzeyi, dönem ve sınıf öğretmenini gir. Mevcut şubenin detayında düzenleme/silme, öğrenci ekleme-çıkarma ve ders bağlama-ayırma işlemleri vardır. Oluşturma formunda ayrı bir **kapasite** alanı yoktur. Şubeye öğrenci eklemek bağlı derslere kayıtları tek işlemde kurar; öğrenci zaten üyeyse, şube/ders kapasitesi dolmuşsa veya bağlı ders bulunamazsa işlem 409 ile bütünüyle reddedilir. Üyesi ya da bağlı dersi olan şube silinemez; önce ilişkileri kaldır. Buradaki **şube/sınıf grubu**, `/courses` üzerindeki **ders oluşturma** işleminden farklıdır.

### 450 · PASS · ADMIN

- Soru: şubedeki ders bağlantısını ayırmam lazım
- Beklenen intent: `class_section_manage`
- Gerçek intent: `class_section_manage`
- response_id: `class_section_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Şubeler", "route": "/management/classes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Şube yönetimi için **Şubeler** (`/management/classes`, Yönetici+) sayfasını aç. **Şube oluştur** ile zorunlu sınıf adını; isteğe bağlı sınıf düzeyi, dönem ve sınıf öğretmenini gir. Mevcut şubenin detayında düzenleme/silme, öğrenci ekleme-çıkarma ve ders bağlama-ayırma işlemleri vardır. Oluşturma formunda ayrı bir **kapasite** alanı yoktur. Şubeye öğrenci eklemek bağlı derslere kayıtları tek işlemde kurar; öğrenci zaten üyeyse, şube/ders kapasitesi dolmuşsa veya bağlı ders bulunamazsa işlem 409 ile bütünüyle reddedilir. Üyesi ya da bağlı dersi olan şube silinemez; önce ilişkileri kaldır. Buradaki **şube/sınıf grubu**, `/courses` üzerindeki **ders oluşturma** işleminden farklıdır.

### 451 · PASS · Yönetici

- Soru: üyeleri olan şubeyi silmeye çalışınca 409 geliyor
- Beklenen intent: `class_section_manage`
- Gerçek intent: `class_section_manage`
- response_id: `class_section_manage_instructions`
- confidence: `0.3685`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Şubeler", "route": "/management/classes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Şube yönetimi için **Şubeler** (`/management/classes`, Yönetici+) sayfasını aç. **Şube oluştur** ile zorunlu sınıf adını; isteğe bağlı sınıf düzeyi, dönem ve sınıf öğretmenini gir. Mevcut şubenin detayında düzenleme/silme, öğrenci ekleme-çıkarma ve ders bağlama-ayırma işlemleri vardır. Oluşturma formunda ayrı bir **kapasite** alanı yoktur. Şubeye öğrenci eklemek bağlı derslere kayıtları tek işlemde kurar; öğrenci zaten üyeyse, şube/ders kapasitesi dolmuşsa veya bağlı ders bulunamazsa işlem 409 ile bütünüyle reddedilir. Üyesi ya da bağlı dersi olan şube silinemez; önce ilişkileri kaldır. Buradaki **şube/sınıf grubu**, `/courses` üzerindeki **ders oluşturma** işleminden farklıdır.

### 452 · PASS · Öğretmen

- Soru: öğretmen olarak yeni sınıf grubu oluşturabilir miyim
- Beklenen intent: `class_section_manage`
- Gerçek intent: `class_section_manage`
- response_id: `class_section_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 453 · PASS · Öğrenci

- Soru: multipart içinde file alanı yok diyor
- Beklenen intent: `upload_problem`
- Gerçek intent: `upload_problem`
- response_id: `upload_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Dosya yüklemede önce alanı ayır: **400**; multipart içindeki `file` alanı eksik, dosya boş veya gövde bozuk olabilir. **413**, dosyanın sunucu/okul boyut sınırını aştığını gösterir; güncel sınır okulun Sistem ayarındadır (varsayılan yaklaşık 5 MiB). Defter, ders notu ve ödev tesliminde kayıt başına en fazla **10 dosya** vardır; önce bir eki sil. Satır içinde gösterilecek görseller yalnız PNG/JPEG/WebP/GIF'tir; SVG desteklenmez. Hata sürerse hangi sayfada yüklediğini, dosya türü/boyutunu ve tam hata metnini yaz; kişisel dosya içeriğini sohbete kopyalama.

### 454 · PASS · Veli

- Soru: boş dosyayı ek olarak kabul etmiyor
- Beklenen intent: `upload_problem`
- Gerçek intent: `upload_problem`
- response_id: `upload_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Dosya yüklemede önce alanı ayır: **400**; multipart içindeki `file` alanı eksik, dosya boş veya gövde bozuk olabilir. **413**, dosyanın sunucu/okul boyut sınırını aştığını gösterir; güncel sınır okulun Sistem ayarındadır (varsayılan yaklaşık 5 MiB). Defter, ders notu ve ödev tesliminde kayıt başına en fazla **10 dosya** vardır; önce bir eki sil. Satır içinde gösterilecek görseller yalnız PNG/JPEG/WebP/GIF'tir; SVG desteklenmez. Hata sürerse hangi sayfada yüklediğini, dosya türü/boyutunu ve tam hata metnini yaz; kişisel dosya içeriğini sohbete kopyalama.

### 455 · PASS · Öğretmen

- Soru: okulun dosya boyut sınırını aştım
- Beklenen intent: `upload_problem`
- Gerçek intent: `upload_problem`
- response_id: `upload_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Dosya yüklemede önce alanı ayır: **400**; multipart içindeki `file` alanı eksik, dosya boş veya gövde bozuk olabilir. **413**, dosyanın sunucu/okul boyut sınırını aştığını gösterir; güncel sınır okulun Sistem ayarındadır (varsayılan yaklaşık 5 MiB). Defter, ders notu ve ödev tesliminde kayıt başına en fazla **10 dosya** vardır; önce bir eki sil. Satır içinde gösterilecek görseller yalnız PNG/JPEG/WebP/GIF'tir; SVG desteklenmez. Hata sürerse hangi sayfada yüklediğini, dosya türü/boyutunu ve tam hata metnini yaz; kişisel dosya içeriğini sohbete kopyalama.

### 456 · PASS · Öğrenci

- Soru: desteklenmeyen dosya türü uyarısı neden çıkar
- Beklenen intent: `upload_problem`
- Gerçek intent: `upload_problem`
- response_id: `upload_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Dosya yüklemede önce alanı ayır: **400**; multipart içindeki `file` alanı eksik, dosya boş veya gövde bozuk olabilir. **413**, dosyanın sunucu/okul boyut sınırını aştığını gösterir; güncel sınır okulun Sistem ayarındadır (varsayılan yaklaşık 5 MiB). Defter, ders notu ve ödev tesliminde kayıt başına en fazla **10 dosya** vardır; önce bir eki sil. Satır içinde gösterilecek görseller yalnız PNG/JPEG/WebP/GIF'tir; SVG desteklenmez. Hata sürerse hangi sayfada yüklediğini, dosya türü/boyutunu ve tam hata metnini yaz; kişisel dosya içeriğini sohbete kopyalama.

### 457 · PASS · Öğrenci

- Soru: ek limitim dolu olduğu için yeni dosya yüklenmiyor
- Beklenen intent: `upload_problem`
- Gerçek intent: `upload_problem`
- response_id: `upload_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Dosya yüklemede önce alanı ayır: **400**; multipart içindeki `file` alanı eksik, dosya boş veya gövde bozuk olabilir. **413**, dosyanın sunucu/okul boyut sınırını aştığını gösterir; güncel sınır okulun Sistem ayarındadır (varsayılan yaklaşık 5 MiB). Defter, ders notu ve ödev tesliminde kayıt başına en fazla **10 dosya** vardır; önce bir eki sil. Satır içinde gösterilecek görseller yalnız PNG/JPEG/WebP/GIF'tir; SVG desteklenmez. Hata sürerse hangi sayfada yüklediğini, dosya türü/boyutunu ve tam hata metnini yaz; kişisel dosya içeriğini sohbete kopyalama.

### 458 · PASS · Öğretmen

- Soru: ders notuna onuncudan sonra dosya eklenir mi
- Beklenen intent: `course_note_manage`
- Gerçek intent: `course_note_manage`
- response_id: `course_note_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ders detayında (`/courses/$id`) **Ders notları** sekmesini aç. Dersin oluşturucusu/atanmış öğretmeni veya Yönetici/ADMIN burada **Yeni ders notu** ile başlık, içerik ve en fazla 10 dosya ekleyebilir; not kartından düzenleyebilir, silebilir ve **Ekler** bölümünü yönetebilir. Derse kayıtlı öğrenci notları ve dosyaları okuyup indirebilir ama ekleme, düzenleme veya silme yapamaz. Dosya başına okul boyut sınırı vardır; 11. ek 409, fazla boyut 413, boş/bozuk dosya 400 verir. Oluşturma sırasında bazı ekler yüklenemezse not yine kaydedilmiş olabilir ve arayüz başarısız ek sayısını gösterir; sayfayı yenileyip eksik ekleri yeniden yükle. Ders notunu silmek bütün eklerini de kalıcı siler. Yönetmediğin ders 403, görünmeyen ders/not 404 ile sonuçlanır. Bu alan kişisel **Defter** notundan ayrıdır.

### 459 · PASS · Öğretmen

- Soru: görsel olarak svg neden desteklenmiyor
- Beklenen intent: `upload_problem`
- Gerçek intent: `upload_problem`
- response_id: `upload_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Dosya yüklemede önce alanı ayır: **400**; multipart içindeki `file` alanı eksik, dosya boş veya gövde bozuk olabilir. **413**, dosyanın sunucu/okul boyut sınırını aştığını gösterir; güncel sınır okulun Sistem ayarındadır (varsayılan yaklaşık 5 MiB). Defter, ders notu ve ödev tesliminde kayıt başına en fazla **10 dosya** vardır; önce bir eki sil. Satır içinde gösterilecek görseller yalnız PNG/JPEG/WebP/GIF'tir; SVG desteklenmez. Hata sürerse hangi sayfada yüklediğini, dosya türü/boyutunu ve tam hata metnini yaz; kişisel dosya içeriğini sohbete kopyalama.

### 460 · PASS · ADMIN

- Soru: dosya yükleme isteği bozuk multipart dönüyor
- Beklenen intent: `upload_problem`
- Gerçek intent: `upload_problem`
- response_id: `upload_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Dosya yüklemede önce alanı ayır: **400**; multipart içindeki `file` alanı eksik, dosya boş veya gövde bozuk olabilir. **413**, dosyanın sunucu/okul boyut sınırını aştığını gösterir; güncel sınır okulun Sistem ayarındadır (varsayılan yaklaşık 5 MiB). Defter, ders notu ve ödev tesliminde kayıt başına en fazla **10 dosya** vardır; önce bir eki sil. Satır içinde gösterilecek görseller yalnız PNG/JPEG/WebP/GIF'tir; SVG desteklenmez. Hata sürerse hangi sayfada yüklediğini, dosya türü/boyutunu ve tam hata metnini yaz; kişisel dosya içeriğini sohbete kopyalama.

### 461 · PASS · Öğrenci

- Soru: çelebi yanıt vermiyor servis mi kapalı
- Beklenen intent: `chatbot_service_problem`
- Gerçek intent: `chatbot_service_problem`
- response_id: `chatbot_service_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Çelebi yanıt vermiyorsa hata metnini ayır: **AI service is not enabled**, backend'de köprü özelliğinin kapalı; **no AI service is connected**, çalışan chatbot bridge'in backend'e bağlı olmadığını gösterir. Bu durumlarda istek **503** olur ve mesaj kaydı oluşturulmaz. **429** mesaj hız sınırıdır; `Retry-After` kadar bekle. Kabul edilen mesaj önce **202/pending** olabilir; uzun süre tamamlanmazsa `unavailable`, `busy`, `timed_out`, `transport`, `protocol`, `bad_reply`, `empty_reply`, `interrupted` ya da köprünün döndürdüğü başka bir servis koduyla başarısız görünür. Uzak servis boş bir kod döndürürse backend bunu `service_error` olarak kaydeder. Thread limiti dolduysa kullanılmayan bir sohbeti sil; thread silmek içindeki bütün mesajları da kalıcı siler. Yabancı thread kimliği güvenlik için 404 döner.

### 462 · PASS · Yönetici

- Soru: ai service is not enabled mesajı ne anlatıyor
- Beklenen intent: `chatbot_service_problem`
- Gerçek intent: `chatbot_service_problem`
- response_id: `chatbot_service_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Çelebi yanıt vermiyorsa hata metnini ayır: **AI service is not enabled**, backend'de köprü özelliğinin kapalı; **no AI service is connected**, çalışan chatbot bridge'in backend'e bağlı olmadığını gösterir. Bu durumlarda istek **503** olur ve mesaj kaydı oluşturulmaz. **429** mesaj hız sınırıdır; `Retry-After` kadar bekle. Kabul edilen mesaj önce **202/pending** olabilir; uzun süre tamamlanmazsa `unavailable`, `busy`, `timed_out`, `transport`, `protocol`, `bad_reply`, `empty_reply`, `interrupted` ya da köprünün döndürdüğü başka bir servis koduyla başarısız görünür. Uzak servis boş bir kod döndürürse backend bunu `service_error` olarak kaydeder. Thread limiti dolduysa kullanılmayan bir sohbeti sil; thread silmek içindeki bütün mesajları da kalıcı siler. Yabancı thread kimliği güvenlik için 404 döner.

### 463 · PASS · ADMIN

- Soru: no ai service is connected right now hatası aldım
- Beklenen intent: `chatbot_service_problem`
- Gerçek intent: `chatbot_service_problem`
- response_id: `chatbot_service_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Çelebi yanıt vermiyorsa hata metnini ayır: **AI service is not enabled**, backend'de köprü özelliğinin kapalı; **no AI service is connected**, çalışan chatbot bridge'in backend'e bağlı olmadığını gösterir. Bu durumlarda istek **503** olur ve mesaj kaydı oluşturulmaz. **429** mesaj hız sınırıdır; `Retry-After` kadar bekle. Kabul edilen mesaj önce **202/pending** olabilir; uzun süre tamamlanmazsa `unavailable`, `busy`, `timed_out`, `transport`, `protocol`, `bad_reply`, `empty_reply`, `interrupted` ya da köprünün döndürdüğü başka bir servis koduyla başarısız görünür. Uzak servis boş bir kod döndürürse backend bunu `service_error` olarak kaydeder. Thread limiti dolduysa kullanılmayan bir sohbeti sil; thread silmek içindeki bütün mesajları da kalıcı siler. Yabancı thread kimliği güvenlik için 404 döner.

### 464 · PASS · ADMIN

- Soru: chatbot bridge çalışıyor ama bağlı görünmüyor
- Beklenen intent: `chatbot_service_problem`
- Gerçek intent: `chatbot_service_problem`
- response_id: `chatbot_service_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Çelebi yanıt vermiyorsa hata metnini ayır: **AI service is not enabled**, backend'de köprü özelliğinin kapalı; **no AI service is connected**, çalışan chatbot bridge'in backend'e bağlı olmadığını gösterir. Bu durumlarda istek **503** olur ve mesaj kaydı oluşturulmaz. **429** mesaj hız sınırıdır; `Retry-After` kadar bekle. Kabul edilen mesaj önce **202/pending** olabilir; uzun süre tamamlanmazsa `unavailable`, `busy`, `timed_out`, `transport`, `protocol`, `bad_reply`, `empty_reply`, `interrupted` ya da köprünün döndürdüğü başka bir servis koduyla başarısız görünür. Uzak servis boş bir kod döndürürse backend bunu `service_error` olarak kaydeder. Thread limiti dolduysa kullanılmayan bir sohbeti sil; thread silmek içindeki bütün mesajları da kalıcı siler. Yabancı thread kimliği güvenlik için 404 döner.

### 465 · PASS · Öğrenci

- Soru: sohbet mesajı uzun zamandır pending
- Beklenen intent: `chatbot_service_problem`
- Gerçek intent: `chatbot_service_problem`
- response_id: `chatbot_service_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Çelebi yanıt vermiyorsa hata metnini ayır: **AI service is not enabled**, backend'de köprü özelliğinin kapalı; **no AI service is connected**, çalışan chatbot bridge'in backend'e bağlı olmadığını gösterir. Bu durumlarda istek **503** olur ve mesaj kaydı oluşturulmaz. **429** mesaj hız sınırıdır; `Retry-After` kadar bekle. Kabul edilen mesaj önce **202/pending** olabilir; uzun süre tamamlanmazsa `unavailable`, `busy`, `timed_out`, `transport`, `protocol`, `bad_reply`, `empty_reply`, `interrupted` ya da köprünün döndürdüğü başka bir servis koduyla başarısız görünür. Uzak servis boş bir kod döndürürse backend bunu `service_error` olarak kaydeder. Thread limiti dolduysa kullanılmayan bir sohbeti sil; thread silmek içindeki bütün mesajları da kalıcı siler. Yabancı thread kimliği güvenlik için 404 döner.

### 466 · PASS · Öğretmen

- Soru: çelebi timed_out durumuna düştü
- Beklenen intent: `chatbot_service_problem`
- Gerçek intent: `chatbot_service_problem`
- response_id: `chatbot_service_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Çelebi yanıt vermiyorsa hata metnini ayır: **AI service is not enabled**, backend'de köprü özelliğinin kapalı; **no AI service is connected**, çalışan chatbot bridge'in backend'e bağlı olmadığını gösterir. Bu durumlarda istek **503** olur ve mesaj kaydı oluşturulmaz. **429** mesaj hız sınırıdır; `Retry-After` kadar bekle. Kabul edilen mesaj önce **202/pending** olabilir; uzun süre tamamlanmazsa `unavailable`, `busy`, `timed_out`, `transport`, `protocol`, `bad_reply`, `empty_reply`, `interrupted` ya da köprünün döndürdüğü başka bir servis koduyla başarısız görünür. Uzak servis boş bir kod döndürürse backend bunu `service_error` olarak kaydeder. Thread limiti dolduysa kullanılmayan bir sohbeti sil; thread silmek içindeki bütün mesajları da kalıcı siler. Yabancı thread kimliği güvenlik için 404 döner.

### 467 · PASS · Yönetici

- Soru: çelebi transport hatasıyla cevaplamadı
- Beklenen intent: `chatbot_service_problem`
- Gerçek intent: `chatbot_service_problem`
- response_id: `chatbot_service_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Çelebi yanıt vermiyorsa hata metnini ayır: **AI service is not enabled**, backend'de köprü özelliğinin kapalı; **no AI service is connected**, çalışan chatbot bridge'in backend'e bağlı olmadığını gösterir. Bu durumlarda istek **503** olur ve mesaj kaydı oluşturulmaz. **429** mesaj hız sınırıdır; `Retry-After` kadar bekle. Kabul edilen mesaj önce **202/pending** olabilir; uzun süre tamamlanmazsa `unavailable`, `busy`, `timed_out`, `transport`, `protocol`, `bad_reply`, `empty_reply`, `interrupted` ya da köprünün döndürdüğü başka bir servis koduyla başarısız görünür. Uzak servis boş bir kod döndürürse backend bunu `service_error` olarak kaydeder. Thread limiti dolduysa kullanılmayan bir sohbeti sil; thread silmek içindeki bütün mesajları da kalıcı siler. Yabancı thread kimliği güvenlik için 404 döner.

### 468 · PASS · Öğrenci

- Soru: chatbotta thread limiti doldu ne silmeliyim
- Beklenen intent: `chatbot_service_problem`
- Gerçek intent: `chatbot_service_problem`
- response_id: `chatbot_service_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Çelebi yanıt vermiyorsa hata metnini ayır: **AI service is not enabled**, backend'de köprü özelliğinin kapalı; **no AI service is connected**, çalışan chatbot bridge'in backend'e bağlı olmadığını gösterir. Bu durumlarda istek **503** olur ve mesaj kaydı oluşturulmaz. **429** mesaj hız sınırıdır; `Retry-After` kadar bekle. Kabul edilen mesaj önce **202/pending** olabilir; uzun süre tamamlanmazsa `unavailable`, `busy`, `timed_out`, `transport`, `protocol`, `bad_reply`, `empty_reply`, `interrupted` ya da köprünün döndürdüğü başka bir servis koduyla başarısız görünür. Uzak servis boş bir kod döndürürse backend bunu `service_error` olarak kaydeder. Thread limiti dolduysa kullanılmayan bir sohbeti sil; thread silmek içindeki bütün mesajları da kalıcı siler. Yabancı thread kimliği güvenlik için 404 döner.

### 469 · PASS · Veli

- Soru: chatbot threadini silersem mesajları da gider mi
- Beklenen intent: `chatbot_service_problem`
- Gerçek intent: `chatbot_service_problem`
- response_id: `chatbot_service_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Çelebi yanıt vermiyorsa hata metnini ayır: **AI service is not enabled**, backend'de köprü özelliğinin kapalı; **no AI service is connected**, çalışan chatbot bridge'in backend'e bağlı olmadığını gösterir. Bu durumlarda istek **503** olur ve mesaj kaydı oluşturulmaz. **429** mesaj hız sınırıdır; `Retry-After` kadar bekle. Kabul edilen mesaj önce **202/pending** olabilir; uzun süre tamamlanmazsa `unavailable`, `busy`, `timed_out`, `transport`, `protocol`, `bad_reply`, `empty_reply`, `interrupted` ya da köprünün döndürdüğü başka bir servis koduyla başarısız görünür. Uzak servis boş bir kod döndürürse backend bunu `service_error` olarak kaydeder. Thread limiti dolduysa kullanılmayan bir sohbeti sil; thread silmek içindeki bütün mesajları da kalıcı siler. Yabancı thread kimliği güvenlik için 404 döner.

### 470 · PASS · Öğrenci

- Soru: chatbot 429 için ne kadar beklemeliyim
- Beklenen intent: `chatbot_service_problem`
- Gerçek intent: `chatbot_service_problem`
- response_id: `chatbot_service_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Çelebi yanıt vermiyorsa hata metnini ayır: **AI service is not enabled**, backend'de köprü özelliğinin kapalı; **no AI service is connected**, çalışan chatbot bridge'in backend'e bağlı olmadığını gösterir. Bu durumlarda istek **503** olur ve mesaj kaydı oluşturulmaz. **429** mesaj hız sınırıdır; `Retry-After` kadar bekle. Kabul edilen mesaj önce **202/pending** olabilir; uzun süre tamamlanmazsa `unavailable`, `busy`, `timed_out`, `transport`, `protocol`, `bad_reply`, `empty_reply`, `interrupted` ya da köprünün döndürdüğü başka bir servis koduyla başarısız görünür. Uzak servis boş bir kod döndürürse backend bunu `service_error` olarak kaydeder. Thread limiti dolduysa kullanılmayan bir sohbeti sil; thread silmek içindeki bütün mesajları da kalıcı siler. Yabancı thread kimliği güvenlik için 404 döner.

### 471 · PASS · Öğretmen

- Soru: asenkron sınavda süre zorunlu hatası alıyorum
- Beklenen intent: `exam_create`
- Gerçek intent: `exam_create`
- response_id: `exam_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: yönetebileceğin en az bir ders olmalı. 1) `/exams` → **Sınav oluştur (Create exam)**. 2) **Ders seç**, **Başlık** ve isteğe bağlı açıklama gir. 3) **Tür** (Ödev/Kısa sınav/Vize/Final/Proje/Sözlü) ve **Mod** (Senkron/Asenkron/Açık) seç. 4) Gerekirse **Deneme hakkı** ve **Yeniden girişe izin ver**'i ayarla. 5) Senkron/Asenkron ise Başlangıç/Bitiş gir. Asenkron modda süre zorunludur; Senkron mod süre kabul etmez. Süre 1 dakika–24 saat arasında ve sınav penceresine sığmalıdır; Açık mod başlangıç/bitiş taşımaz. 6) **Oluştur**. Sınavlar ders içinden eklenir.

### 472 · PASS · Öğretmen

- Soru: senkron sınav süre alanını neden kabul etmiyor
- Beklenen intent: `exam_create`
- Gerçek intent: `exam_create`
- response_id: `exam_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: yönetebileceğin en az bir ders olmalı. 1) `/exams` → **Sınav oluştur (Create exam)**. 2) **Ders seç**, **Başlık** ve isteğe bağlı açıklama gir. 3) **Tür** (Ödev/Kısa sınav/Vize/Final/Proje/Sözlü) ve **Mod** (Senkron/Asenkron/Açık) seç. 4) Gerekirse **Deneme hakkı** ve **Yeniden girişe izin ver**'i ayarla. 5) Senkron/Asenkron ise Başlangıç/Bitiş gir. Asenkron modda süre zorunludur; Senkron mod süre kabul etmez. Süre 1 dakika–24 saat arasında ve sınav penceresine sığmalıdır; Açık mod başlangıç/bitiş taşımaz. 6) **Oluştur**. Sınavlar ders içinden eklenir.

### 473 · PASS · Yönetici

- Soru: açık mod sınava başlangıç tarihi yazabilir miyim
- Beklenen intent: `exam_create`
- Gerçek intent: `exam_create`
- response_id: `exam_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: yönetebileceğin en az bir ders olmalı. 1) `/exams` → **Sınav oluştur (Create exam)**. 2) **Ders seç**, **Başlık** ve isteğe bağlı açıklama gir. 3) **Tür** (Ödev/Kısa sınav/Vize/Final/Proje/Sözlü) ve **Mod** (Senkron/Asenkron/Açık) seç. 4) Gerekirse **Deneme hakkı** ve **Yeniden girişe izin ver**'i ayarla. 5) Senkron/Asenkron ise Başlangıç/Bitiş gir. Asenkron modda süre zorunludur; Senkron mod süre kabul etmez. Süre 1 dakika–24 saat arasında ve sınav penceresine sığmalıdır; Açık mod başlangıç/bitiş taşımaz. 6) **Oluştur**. Sınavlar ders içinden eklenir.

### 474 · PASS · Öğretmen

- Soru: sınav süresi zaman penceresine sığmıyor
- Beklenen intent: `exam_create`
- Gerçek intent: `exam_create`
- response_id: `exam_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: yönetebileceğin en az bir ders olmalı. 1) `/exams` → **Sınav oluştur (Create exam)**. 2) **Ders seç**, **Başlık** ve isteğe bağlı açıklama gir. 3) **Tür** (Ödev/Kısa sınav/Vize/Final/Proje/Sözlü) ve **Mod** (Senkron/Asenkron/Açık) seç. 4) Gerekirse **Deneme hakkı** ve **Yeniden girişe izin ver**'i ayarla. 5) Senkron/Asenkron ise Başlangıç/Bitiş gir. Asenkron modda süre zorunludur; Senkron mod süre kabul etmez. Süre 1 dakika–24 saat arasında ve sınav penceresine sığmalıdır; Açık mod başlangıç/bitiş taşımaz. 6) **Oluştur**. Sınavlar ders içinden eklenir.

### 475 · PASS · Öğretmen

- Soru: sınav duration en fazla kaç saat olabilir
- Beklenen intent: `exam_create`
- Gerçek intent: `exam_create`
- response_id: `exam_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: yönetebileceğin en az bir ders olmalı. 1) `/exams` → **Sınav oluştur (Create exam)**. 2) **Ders seç**, **Başlık** ve isteğe bağlı açıklama gir. 3) **Tür** (Ödev/Kısa sınav/Vize/Final/Proje/Sözlü) ve **Mod** (Senkron/Asenkron/Açık) seç. 4) Gerekirse **Deneme hakkı** ve **Yeniden girişe izin ver**'i ayarla. 5) Senkron/Asenkron ise Başlangıç/Bitiş gir. Asenkron modda süre zorunludur; Senkron mod süre kabul etmez. Süre 1 dakika–24 saat arasında ve sınav penceresine sığmalıdır; Açık mod başlangıç/bitiş taşımaz. 6) **Oluştur**. Sınavlar ders içinden eklenir.

### 476 · PASS · Öğretmen

- Soru: canlı izleme için sınavın başlaması şart mı
- Beklenen intent: `exam_live_monitor`
- Gerçek intent: `exam_live_monitor`
- response_id: `exam_live_monitor_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: sınavın dersinde yönetim yetkisi. Backend canlı görüntü için ayrıca 'başlamış olmalı' veya belirli bir mod şartı aramaz. Sınav detayı → **Canlı İzleme (Live Monitor)** (`/exams/$id/live`). Üstteki sayaçlar (Başlamadı/Devam ediyor/Teslim edildi/Süresi doldu/Katılmadı) ve **Canlı Liste**'de ilerleme, kalan süre, durum görünür. Sınav bitince ekran 'Son Durum'a döner. Öğrenciler bu ekranı göremez.

### 477 · PASS · Öğretmen

- Soru: sınav bitmeden öğrencinin notunu girebilir miyim
- Beklenen intent: `exam_grade_student`
- Gerçek intent: `exam_grade_student`
- response_id: `exam_grade_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Sınav detayı → **Öğrenci notla (Grade a student)**. 2) Öğrenciyi seç, **Not** (0–100 tam sayı) gir, kaydet ve onayla. Metin cevaplar otomatik puanlanmaz; **Cevap Kâğıdı**'ndaki otomatik puanı referans alıp nihai notu elle verirsin. Hedef hesap Öğrenci olmalı, sınavın dersine kayıtlı olmalı ve kendi hesabını notlandıramazsın. Okul ayarından kaldırılmış bir sınav türünde not kaydetmek 409 ile reddedilir. Verilen not sonuç tablosunda **Kaldır** ile silinebilir.

### 478 · PASS · Öğrenci

- Soru: not verilmemiş sınav neden karnede hiç görünmüyor
- Beklenen intent: `report_card_view`
- Gerçek intent: `report_card_view`
- response_id: `report_card_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Karnem", "route": "/marks"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Karneni görmek için menüden **Karnem (Report card)** veya `/marks`'a git. Üstte **Genel ortalama** (sayı + harf notu, /100), altında her ders için **Ders ortalaması** ve sınav bazında **Ağırlık** ve **Not** görünür. Karnem yalnızca Öğrenci rolüne açıktır; notu henüz girilmemiş sınav rapor listesine eklenmez.

### 479 · PASS · Öğrenci

- Soru: sınav denemesi teslim edildiği için cevap değişmiyor
- Beklenen intent: `exam_rejoin_retake`
- Gerçek intent: `exam_rejoin_retake`
- response_id: `exam_rejoin_retake_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Rejoin (aynı denemeye dönüş):** 'Yeniden girişe izin ver' açıksa odadan çıktıktan sonra tekrar **Sınav odasını aç** → **Sınava devam et**; kalan süre ve cevapların korunur. **Retake (yeni deneme):** 'Deneme hakkı' açık ve azami sayı belirlenmişse her yeni giriş bir deneme kullanır. **Süre çıkışta bile durmaz.** 'Yeniden giriş kapalı', 'deneme hakkı kalmadı', 'süre doldu' veya 'deneme zaten teslim edildi' durumunda aynı denemeye dönemezsin.

### 480 · PASS · Öğrenci

- Soru: sınavın süresi dolduktan sonra yeniden bağlanabilir miyim
- Beklenen intent: `exam_rejoin_retake`
- Gerçek intent: `exam_rejoin_retake`
- response_id: `exam_rejoin_retake_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Sınavlar", "route": "/exams"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Rejoin (aynı denemeye dönüş):** 'Yeniden girişe izin ver' açıksa odadan çıktıktan sonra tekrar **Sınav odasını aç** → **Sınava devam et**; kalan süre ve cevapların korunur. **Retake (yeni deneme):** 'Deneme hakkı' açık ve azami sayı belirlenmişse her yeni giriş bir deneme kullanır. **Süre çıkışta bile durmaz.** 'Yeniden giriş kapalı', 'deneme hakkı kalmadı', 'süre doldu' veya 'deneme zaten teslim edildi' durumunda aynı denemeye dönemezsin.

### 481 · PASS · Öğrenci

- Soru: notlandırılmış ödev dosyasını neden silemiyorum
- Beklenen intent: `homework_submit`
- Gerçek intent: `homework_submit`
- response_id: `homework_submit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: ödevin verildiği dersin kayıtlı öğrencisisin. 1) **Ödevler** (`/homework`) → ilgili ödevin detayına (`/homework/$id`) gir. 2) **Ödevi teslim et** panelinde cevabını yaz ve/veya dosya ekle. 3) Gönder. Teslim yalnızca Öğrenciye açıktır; **Son teslim** tarihine dikkat et. Teslim notlandırıldıktan sonra öğrenci metni veya dosyayı değiştiremez/silemez; dosya okulun yükleme sınırını aşarsa 413 hatası alınır.

### 482 · PASS · Öğretmen

- Soru: ödev hedef kitlesini daraltırken 409 aldım
- Beklenen intent: `homework_manage`
- Gerçek intent: `homework_manage`
- response_id: `homework_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yönettiğin dersin detayında (`/courses/$id`) **Ödevler** sekmesine geç. Ödev satırının **İşlemler** menüsünde **Düzenle** ile başlık, açıklama, aynı dersin konusu ve gelecekteki son teslim tarihini değiştir; **Sil** ile ödevi onaylayarak kaldır. Ders oluşturucusu/atanmış öğretmen yalnız yönettiği derste, Yönetici/ADMIN okul kapsamında işlem yapabilir. Yeni son tarih geçmişteyse veya konu başka derse aitse 400 alınır. Backend'de hedef kitleyi daraltan bir değişiklik, kapsam dışına çıkacak öğrencinin teslimi ya da sonucu varsa 409 ile bütünüyle reddedilir; eşzamanlı konu değişiminde de kaydı yeniden okuyup denemek gerekebilir. **Ödevi silmek**, öğrencilerin teslim metinlerini, ek dosyalarını ve not/sonuçlarını da kalıcı siler; yalnız bir öğrencinin kendi teslimini kaldırması farklı olan **Teslimi geri çek** işlemidir.

### 483 · PASS · Öğretmen

- Soru: ödev yalnız seçilen öğrencilere nasıl atanır
- Beklenen intent: `homework_assign`
- Gerçek intent: `homework_assign`
- response_id: `homework_assign_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ön koşul: yönettiğin bir ders olmalı. 1) **Ödevler** (`/homework`) → **Ödev ekle**. 2) Dersi seç, başlık ve açıklamayı gir, **Son teslim** tarihini belirle. 3) Oluştur. Ödev dersin öğrencilerine atanır; gelen teslimleri ödev detayındaki **Teslimler** bölümünden görürsün.

### 484 · PASS · Öğrenci

- Soru: ödeve not verildikten sonra teslim geri çekilir mi
- Beklenen intent: `homework_withdraw_submission`
- Gerçek intent: `homework_withdraw_submission`
- response_id: `homework_withdraw_submission_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yalnız exact **Öğrenci** rolü kendi teslimini geri çekebilir. **Ödevler** (`/homework`) → ödev detayı (`/homework/$id`) → **Ödevi teslim et** panelinde **Teslimi geri çek**'e basıp uyarıyı onayla. Bu işlem teslim metnini ve eklenen **bütün dosyaları kalıcı siler**; ödevin kendisini veya öğretmenin başka öğrencilere verdiği kaydı silmez. Düğme yalnız bir teslim varken ve sonuç/not yokken görünür. Notlandırılmış teslim donmuştur: geri çekme 409 verir; önce öğretmenin notu kaldırması gerekir. Teslim yoksa 404, dersten çıkarıldıysan 403, ödevin hedef kitlesinde değilsen güvenlik için 404 alınır. Son teslim tarihi geçmiş olması tek başına geri çekmeyi engellemez; daha sonra yeniden gönderirsen yeni teslim geç olarak işaretlenir.

### 485 · PASS · Öğrenci

- Soru: randevu slotu dolu olduğu için talep açamıyorum
- Beklenen intent: `appointment_book`
- Gerçek intent: `appointment_book`
- response_id: `appointment_book_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Randevu almak için **Planlama** grubundaki **Randevular** (`/appointments`) sayfasına git. **Öğretmenlerin açık saatleri** bölümünden uygun saati seç, **Randevu al**'a bas. Talebin **Randevularım** altında görünür ve öğretmen onayına düşer. Randevu alma yalnızca Öğrenci ve Veli'ye açıktır. Veli randevuyu çocuğu adına değil kendi requester hesabıyla alır. Slot başlamış/doluysa, aynı saatte başka randevun varsa veya öğretmen artık uygun rolde değilse 409 alırsın. İptali yalnız talebi açan kullanıcı yapar; öğretmenin önerdiği yeni saati **Kabul et/Reddet** ile yanıtlayabilirsin.

### 486 · PASS · Veli

- Soru: randevu saatim başka görüşmeyle çakışıyor
- Beklenen intent: `appointment_book`
- Gerçek intent: `appointment_book`
- response_id: `appointment_book_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Randevu almak için **Planlama** grubundaki **Randevular** (`/appointments`) sayfasına git. **Öğretmenlerin açık saatleri** bölümünden uygun saati seç, **Randevu al**'a bas. Talebin **Randevularım** altında görünür ve öğretmen onayına düşer. Randevu alma yalnızca Öğrenci ve Veli'ye açıktır. Veli randevuyu çocuğu adına değil kendi requester hesabıyla alır. Slot başlamış/doluysa, aynı saatte başka randevun varsa veya öğretmen artık uygun rolde değilse 409 alırsın. İptali yalnız talebi açan kullanıcı yapar; öğretmenin önerdiği yeni saati **Kabul et/Reddet** ile yanıtlayabilirsin.

### 487 · PASS · Öğrenci

- Soru: başlamış randevu için 409 geldi
- Beklenen intent: `appointment_book`
- Gerçek intent: `appointment_book`
- response_id: `appointment_book_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Randevu almak için **Planlama** grubundaki **Randevular** (`/appointments`) sayfasına git. **Öğretmenlerin açık saatleri** bölümünden uygun saati seç, **Randevu al**'a bas. Talebin **Randevularım** altında görünür ve öğretmen onayına düşer. Randevu alma yalnızca Öğrenci ve Veli'ye açıktır. Veli randevuyu çocuğu adına değil kendi requester hesabıyla alır. Slot başlamış/doluysa, aynı saatte başka randevun varsa veya öğretmen artık uygun rolde değilse 409 alırsın. İptali yalnız talebi açan kullanıcı yapar; öğretmenin önerdiği yeni saati **Kabul et/Reddet** ile yanıtlayabilirsin.

### 488 · PASS · Veli

- Soru: öğretmenin önerdiği yeni randevu saatini kabul edeceğim
- Beklenen intent: `appointment_book`
- Gerçek intent: `appointment_book`
- response_id: `appointment_book_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Randevu almak için **Planlama** grubundaki **Randevular** (`/appointments`) sayfasına git. **Öğretmenlerin açık saatleri** bölümünden uygun saati seç, **Randevu al**'a bas. Talebin **Randevularım** altında görünür ve öğretmen onayına düşer. Randevu alma yalnızca Öğrenci ve Veli'ye açıktır. Veli randevuyu çocuğu adına değil kendi requester hesabıyla alır. Slot başlamış/doluysa, aynı saatte başka randevun varsa veya öğretmen artık uygun rolde değilse 409 alırsın. İptali yalnız talebi açan kullanıcı yapar; öğretmenin önerdiği yeni saati **Kabul et/Reddet** ile yanıtlayabilirsin.

### 489 · PASS · Öğretmen

- Soru: onaylı talep bulunan randevu saatini silemiyorum
- Beklenen intent: `appointment_slot_open`
- Gerçek intent: `appointment_slot_open`
- response_id: `appointment_slot_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Randevular** (`/appointments`) → **Açtığım saatler** bölümünde **Saat aç** (veya **Yeni saat**) ile müsait randevu saati yayınla. Öğrenci ve veliler bu saatlerden randevu talep eder; gelen talepleri **Randevu talepleri**'nden yönetirsin. Pending veya onaylı randevusu bulunan tekil saat/tekrarlı seri silinemez; önce talebin durumunu çözmelisin.

### 490 · PASS · Yönetici

- Soru: randevu serisini silmek neden reddediliyor
- Beklenen intent: `appointment_slot_open`
- Gerçek intent: `appointment_slot_open`
- response_id: `appointment_slot_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Randevular** (`/appointments`) → **Açtığım saatler** bölümünde **Saat aç** (veya **Yeni saat**) ile müsait randevu saati yayınla. Öğrenci ve veliler bu saatlerden randevu talep eder; gelen talepleri **Randevu talepleri**'nden yönetirsin. Pending veya onaylı randevusu bulunan tekil saat/tekrarlı seri silinemez; önce talebin durumunu çözmelisin.

### 491 · PASS · Öğretmen

- Soru: randevu için başka saat önermek istiyorum
- Beklenen intent: `appointment_requests`
- Gerçek intent: `appointment_requests`
- response_id: `appointment_requests_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Randevular** (`/appointments`) → **Randevu talepleri** bölümünde gelen talepleri görürsün; her talepte **Onayla** ile kabul et (gerekirse reddet) veya **Başka saat öner**. Onaylanan randevu, ilgili öğrenci/velinin **Randevularım**'ında görünür. Karşı saati requester kabul/reddeder; eski ya da artık geçerli olmayan teklife basmak 409 verir. Öğretmen/Yönetici randevuyu requester adına iptal edemez.

### 492 · PASS · Öğrenci

- Soru: eski randevu teklifine basınca 409 oluyor
- Beklenen intent: `appointment_requests`
- Gerçek intent: `appointment_requests`
- response_id: `appointment_requests_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 493 · PASS · Öğretmen

- Soru: öğretmen olarak öğrencinin randevusunu iptal edebilir miyim
- Beklenen intent: `appointment_requests`
- Gerçek intent: `appointment_requests`
- response_id: `appointment_requests_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Randevular", "route": "/appointments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Randevular** (`/appointments`) → **Randevu talepleri** bölümünde gelen talepleri görürsün; her talepte **Onayla** ile kabul et (gerekirse reddet) veya **Başka saat öner**. Onaylanan randevu, ilgili öğrenci/velinin **Randevularım**'ında görünür. Karşı saati requester kabul/reddeder; eski ya da artık geçerli olmayan teklife basmak 409 verir. Öğretmen/Yönetici randevuyu requester adına iptal edemez.

### 494 · PASS · Öğrenci

- Soru: yemek rezervasyonu doluluk yüzünden 409 verdi
- Beklenen intent: `meal_book`
- Gerçek intent: `meal_book`
- response_id: `meal_book_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yemek için yer ayırmak üzere **Yemekler** (`/meals`) → ilgili menü/öğüne gir, **Yer ayır**'a bas. Rezervasyonun **Rezerve edildi** olarak görünür; **Rezervasyonu iptal et** ile geri alabilirsin. Yer ayırma Öğrenci (kendisi) ve Veli'ye (bağlı çocuğu) açıktır. Geçmiş tarih, iptal eşiği, doluluk, yeniden-rezervasyon tavanı veya eşzamanlı değişiklik 409 üretebilir; sayfayı yenileyip güncel kapasite ve son saati kontrol et.

### 495 · PASS · Veli

- Soru: öğün kapasitesi tamamen dolu
- Beklenen intent: `meal_book`
- Gerçek intent: `meal_book`
- response_id: `meal_book_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yemek için yer ayırmak üzere **Yemekler** (`/meals`) → ilgili menü/öğüne gir, **Yer ayır**'a bas. Rezervasyonun **Rezerve edildi** olarak görünür; **Rezervasyonu iptal et** ile geri alabilirsin. Yer ayırma Öğrenci (kendisi) ve Veli'ye (bağlı çocuğu) açıktır. Geçmiş tarih, iptal eşiği, doluluk, yeniden-rezervasyon tavanı veya eşzamanlı değişiklik 409 üretebilir; sayfayı yenileyip güncel kapasite ve son saati kontrol et.

### 496 · PASS · Öğrenci

- Soru: yemek için son rezervasyon saatini kaçırdım
- Beklenen intent: `meal_book`
- Gerçek intent: `meal_book`
- response_id: `meal_book_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yemek için yer ayırmak üzere **Yemekler** (`/meals`) → ilgili menü/öğüne gir, **Yer ayır**'a bas. Rezervasyonun **Rezerve edildi** olarak görünür; **Rezervasyonu iptal et** ile geri alabilirsin. Yer ayırma Öğrenci (kendisi) ve Veli'ye (bağlı çocuğu) açıktır. Geçmiş tarih, iptal eşiği, doluluk, yeniden-rezervasyon tavanı veya eşzamanlı değişiklik 409 üretebilir; sayfayı yenileyip güncel kapasite ve son saati kontrol et.

### 497 · PASS · Veli

- Soru: aynı öğüne yeniden rezervasyon tavanına ulaştım
- Beklenen intent: `meal_book`
- Gerçek intent: `meal_book`
- response_id: `meal_book_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yemek için yer ayırmak üzere **Yemekler** (`/meals`) → ilgili menü/öğüne gir, **Yer ayır**'a bas. Rezervasyonun **Rezerve edildi** olarak görünür; **Rezervasyonu iptal et** ile geri alabilirsin. Yer ayırma Öğrenci (kendisi) ve Veli'ye (bağlı çocuğu) açıktır. Geçmiş tarih, iptal eşiği, doluluk, yeniden-rezervasyon tavanı veya eşzamanlı değişiklik 409 üretebilir; sayfayı yenileyip güncel kapasite ve son saati kontrol et.

### 498 · PASS · ADMIN

- Soru: yemek kredisi seçtiğim öğüne mi yazılıyor
- Beklenen intent: `meal_credit_manage`
- Gerçek intent: `meal_credit_manage`
- response_id: `meal_credit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Öğrenci yemek kredisi yalnız **ADMIN** tarafından kaydedilebilir. `/meals` sayfasından bir öğün detayını aç, öğrenci hesabını seç ve **Hizmet** sekmesindeki **Kredi kaydet** bölümünde tutar (isteğe bağlı yöntem/not) girip onayla. Kredi kaydı seçili öğüne bağlı değildir; öğrencinin append-only yemek hesabına işlenir. Yönetici menü ve beslenme profillerini düzenleyebilir ancak kredi kaydetme kontrolü onda görünmez.

### 499 · PASS · Yönetici

- Soru: ödeme kaydını silmek yerine ters kayıt mı açmalıyım
- Beklenen intent: `fees_manage`
- Gerçek intent: `fees_manage`
- response_id: `fees_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödemeler", "route": "/management/payments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Ne:** **Ödemeler** (`/management/payments`, Yönetici+) okulun ücret ve ödeme kayıtlarını yönettiğin sayfadır (öğrencilerin borç/tahsilat durumu).
> **Nereden/nasıl:** `/management/payments`'ı aç; öğrenci/döneme göre süz, ödeme kaydını gör; tahsilat, iade veya ters kayıt işlemini ilgili satırdan yap. Defter satırları sonradan düzenlenip silinmez: düzeltmeler yeni refund/reversal satırı ekleyerek append-only tutulur.
> **Not:** Bu yönetim sayfasıdır; öğrenci/velinin kendi **Ödeme ekstresi** ayrı sayfadır (`/payments`).

### 500 · PASS · ADMIN

- Soru: yanlış tahsilatı iade etmek istiyorum
- Beklenen intent: `fees_manage`
- Gerçek intent: `fees_manage`
- response_id: `fees_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödemeler", "route": "/management/payments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Ne:** **Ödemeler** (`/management/payments`, Yönetici+) okulun ücret ve ödeme kayıtlarını yönettiğin sayfadır (öğrencilerin borç/tahsilat durumu).
> **Nereden/nasıl:** `/management/payments`'ı aç; öğrenci/döneme göre süz, ödeme kaydını gör; tahsilat, iade veya ters kayıt işlemini ilgili satırdan yap. Defter satırları sonradan düzenlenip silinmez: düzeltmeler yeni refund/reversal satırı ekleyerek append-only tutulur.
> **Not:** Bu yönetim sayfasıdır; öğrenci/velinin kendi **Ödeme ekstresi** ayrı sayfadır (`/payments`).

### 501 · PASS · Yönetici

- Soru: ödeme ledger satırı neden düzenlenmiyor
- Beklenen intent: `fees_manage`
- Gerçek intent: `fees_manage`
- response_id: `fees_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödemeler", "route": "/management/payments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Ne:** **Ödemeler** (`/management/payments`, Yönetici+) okulun ücret ve ödeme kayıtlarını yönettiğin sayfadır (öğrencilerin borç/tahsilat durumu).
> **Nereden/nasıl:** `/management/payments`'ı aç; öğrenci/döneme göre süz, ödeme kaydını gör; tahsilat, iade veya ters kayıt işlemini ilgili satırdan yap. Defter satırları sonradan düzenlenip silinmez: düzeltmeler yeni refund/reversal satırı ekleyerek append-only tutulur.
> **Not:** Bu yönetim sayfasıdır; öğrenci/velinin kendi **Ödeme ekstresi** ayrı sayfadır (`/payments`).

### 502 · PASS · ADMIN

- Soru: aynı request key farklı ödeme tutarında neden reddediliyor
- Beklenen intent: `fees_manage`
- Gerçek intent: `fees_manage`
- response_id: `fees_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödemeler", "route": "/management/payments"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Ne:** **Ödemeler** (`/management/payments`, Yönetici+) okulun ücret ve ödeme kayıtlarını yönettiğin sayfadır (öğrencilerin borç/tahsilat durumu).
> **Nereden/nasıl:** `/management/payments`'ı aç; öğrenci/döneme göre süz, ödeme kaydını gör; tahsilat, iade veya ters kayıt işlemini ilgili satırdan yap. Defter satırları sonradan düzenlenip silinmez: düzeltmeler yeni refund/reversal satırı ekleyerek append-only tutulur.
> **Not:** Bu yönetim sayfasıdır; öğrenci/velinin kendi **Ödeme ekstresi** ayrı sayfadır (`/payments`).

### 503 · PASS · Öğrenci

- Soru: mesajı kalıcı silmek için önce çöpe mi taşımalıyım
- Beklenen intent: `messages_use`
- Gerçek intent: `messages_use`
- response_id: `messages_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Mesajlar", "route": "/messages"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Mesajlar** (`/messages`), kullanıcılar arasında bire-bir, posta tarzı yazışma içindir. Sol menüden **Mesajlar**'ı aç: **Gelen kutusu**ndaki mesajları okuyabilir, mesajları **Arşiv**'e veya **Çöp**'e taşıyabilir, yeni mesaj oluşturup konu + metin yazarak gönderebilirsin. Bir iletiyi kalıcı silmek için önce **Çöp** klasörüne taşıyıp oradan sil; karşı tarafın kopyası senin arşivleme/silme işlemlerinden etkilenmez. Kendine mesaj gönderemezsin.

### 504 · PASS · Veli

- Soru: mesajımı silince alıcının kopyası da silinir mi
- Beklenen intent: `messages_use`
- Gerçek intent: `messages_use`
- response_id: `messages_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Mesajlar", "route": "/messages"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Mesajlar** (`/messages`), kullanıcılar arasında bire-bir, posta tarzı yazışma içindir. Sol menüden **Mesajlar**'ı aç: **Gelen kutusu**ndaki mesajları okuyabilir, mesajları **Arşiv**'e veya **Çöp**'e taşıyabilir, yeni mesaj oluşturup konu + metin yazarak gönderebilirsin. Bir iletiyi kalıcı silmek için önce **Çöp** klasörüne taşıyıp oradan sil; karşı tarafın kopyası senin arşivleme/silme işlemlerinden etkilenmez. Kendine mesaj gönderemezsin.

### 505 · PASS · Öğretmen

- Soru: kendime mesaj gönderemiyorum neden
- Beklenen intent: `messages_use`
- Gerçek intent: `messages_use`
- response_id: `messages_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Mesajlar", "route": "/messages"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Mesajlar** (`/messages`), kullanıcılar arasında bire-bir, posta tarzı yazışma içindir. Sol menüden **Mesajlar**'ı aç: **Gelen kutusu**ndaki mesajları okuyabilir, mesajları **Arşiv**'e veya **Çöp**'e taşıyabilir, yeni mesaj oluşturup konu + metin yazarak gönderebilirsin. Bir iletiyi kalıcı silmek için önce **Çöp** klasörüne taşıyıp oradan sil; karşı tarafın kopyası senin arşivleme/silme işlemlerinden etkilenmez. Kendine mesaj gönderemezsin.

### 506 · PASS · Öğretmen

- Soru: havuz sorusunu reddetmek çözümleri de kalıcı siler mi
- Beklenen intent: `question_approve`
- Gerçek intent: `question_approve`
- response_id: `question_approve_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru havuzu", "route": "/questions"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Soru havuzu** (`/questions`) → soru detayında **Onayla** ile bekleyen soruyu yayınla, gerekirse **Reddet**. Onaylanan soru **Onaylandı** olur ve havuza erişen rollere görünür. **Reddet**, soru kaydıyla birlikte çözümleri ve görselleri kalıcı olarak siler; onaylamadan önce içeriği kontrol et. Moderasyon Öğretmen ve üstüne açıktır.

### 507 · PASS · Öğretmen

- Soru: soru havuzunda pending soruyu kim görebilir
- Beklenen intent: `question_approve`
- Gerçek intent: `question_approve`
- response_id: `question_approve_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru havuzu", "route": "/questions"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Soru havuzu** (`/questions`) → soru detayında **Onayla** ile bekleyen soruyu yayınla, gerekirse **Reddet**. Onaylanan soru **Onaylandı** olur ve havuza erişen rollere görünür. **Reddet**, soru kaydıyla birlikte çözümleri ve görselleri kalıcı olarak siler; onaylamadan önce içeriği kontrol et. Moderasyon Öğretmen ve üstüne açıktır.

### 508 · PASS · Öğrenci

- Soru: tahtayı kapatırsam yeniden açabilir miyim
- Beklenen intent: `board_create`
- Gerçek intent: `board_create`
- response_id: `board_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Beyaz tahtalar", "route": "/whiteboards"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yeni beyaz tahta için **Beyaz tahtalar** (`/whiteboards`) → **Yeni tahta** ile **Başlık** gir, isteğe bağlı **Katılımcılar** ekle, oluştur. Tahta içinde **Kilitle/Kilidi aç**, **Temizle**, **Tahtayı kapat** ve silme kontrolleri yalnız oluşturucudadır; kapatma kalıcı salt-okunur durumdur ve yeniden açma yoktur. Boş/kilitli/kapalı tahtayı temizleme 409 verebilir. Öğretmen+ **Toplu davet** ile sınıf, ders veya etkinlik katılımcısı çağırabilir; kapasite aşılırsa toplu ekleme bütünüyle reddedilir. Tahtayı silmek çizim geçmişini de kalıcı siler.

### 509 · PASS · Öğretmen

- Soru: kilitli tahtayı temizlerken 409 alıyorum
- Beklenen intent: `board_create`
- Gerçek intent: `board_create`
- response_id: `board_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Beyaz tahtalar", "route": "/whiteboards"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yeni beyaz tahta için **Beyaz tahtalar** (`/whiteboards`) → **Yeni tahta** ile **Başlık** gir, isteğe bağlı **Katılımcılar** ekle, oluştur. Tahta içinde **Kilitle/Kilidi aç**, **Temizle**, **Tahtayı kapat** ve silme kontrolleri yalnız oluşturucudadır; kapatma kalıcı salt-okunur durumdur ve yeniden açma yoktur. Boş/kilitli/kapalı tahtayı temizleme 409 verebilir. Öğretmen+ **Toplu davet** ile sınıf, ders veya etkinlik katılımcısı çağırabilir; kapasite aşılırsa toplu ekleme bütünüyle reddedilir. Tahtayı silmek çizim geçmişini de kalıcı siler.

### 510 · PASS · Öğretmen

- Soru: tahtaya ders katılımcılarını toplu davet edeceğim
- Beklenen intent: `board_create`
- Gerçek intent: `board_create`
- response_id: `board_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Beyaz tahtalar", "route": "/whiteboards"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yeni beyaz tahta için **Beyaz tahtalar** (`/whiteboards`) → **Yeni tahta** ile **Başlık** gir, isteğe bağlı **Katılımcılar** ekle, oluştur. Tahta içinde **Kilitle/Kilidi aç**, **Temizle**, **Tahtayı kapat** ve silme kontrolleri yalnız oluşturucudadır; kapatma kalıcı salt-okunur durumdur ve yeniden açma yoktur. Boş/kilitli/kapalı tahtayı temizleme 409 verebilir. Öğretmen+ **Toplu davet** ile sınıf, ders veya etkinlik katılımcısı çağırabilir; kapasite aşılırsa toplu ekleme bütünüyle reddedilir. Tahtayı silmek çizim geçmişini de kalıcı siler.

### 511 · PASS · Öğrenci

- Soru: tahtayı silmek çizim geçmişini de yok eder mi
- Beklenen intent: `board_create`
- Gerçek intent: `board_create`
- response_id: `board_create_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Beyaz tahtalar", "route": "/whiteboards"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yeni beyaz tahta için **Beyaz tahtalar** (`/whiteboards`) → **Yeni tahta** ile **Başlık** gir, isteğe bağlı **Katılımcılar** ekle, oluştur. Tahta içinde **Kilitle/Kilidi aç**, **Temizle**, **Tahtayı kapat** ve silme kontrolleri yalnız oluşturucudadır; kapatma kalıcı salt-okunur durumdur ve yeniden açma yoktur. Boş/kilitli/kapalı tahtayı temizleme 409 verebilir. Öğretmen+ **Toplu davet** ile sınıf, ders veya etkinlik katılımcısı çağırabilir; kapasite aşılırsa toplu ekleme bütünüyle reddedilir. Tahtayı silmek çizim geçmişini de kalıcı siler.

### 512 · PASS · Öğrenci

- Soru: öğrenci kendi etkinlik yoklamasını neden işaretleyemiyor
- Beklenen intent: `event_attendance_mark`
- Gerçek intent: `event_attendance_mark`
- response_id: `event_attendance_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 513 · PASS · Veli

- Soru: veli bağlı çocuğun pomodoro geçmişini görebilir mi
- Beklenen intent: `parent_info`
- Gerçek intent: `parent_info`
- response_id: `parent_role_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Çocuklarım", "route": "/students"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Ne:** **Veli**, kendisine bağlanan öğrencileri **salt-okunur** izleyen roldür: bağlı öğrencinin not/karnesini, yoklamasını, ödev raporunu, şube üyeliklerini ve Pomodoro geçmişini görüntüleyebilir; Mesajlar'ı kullanabilir. Veli ayrıca uygun randevuyu ve çocuğu için yemeği ayırabilir. Veli hesabı sınava giremez, derse kaydolamaz ve yoklamada işaretlenmez — bu işlemler öğrenciye özeldir.
> **Nereden/nasıl:** Bağlı öğrencilerini **Çocuklarım** sayfasından (`/students`) görürsün; bir çocuğu seçip notlarına/karnesine ve yoklamasına oradan geçersin.
> **Etkili kullanım:** Birden çok öğrenci tek veliye bağlanabilir — Çocuklarım'dan aralarında geçiş yaparsın. Veli–öğrenci bağlantısını **ADMIN** kurar; bağlantı görünmüyorsa okuldan bağlanmasını iste.

### 514 · PASS · Veli

- Soru: veli çocuğu adına öğretmenden randevu mu alır
- Beklenen intent: `parent_info`
- Gerçek intent: `parent_info`
- response_id: `parent_role_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Çocuklarım", "route": "/students"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Ne:** **Veli**, kendisine bağlanan öğrencileri **salt-okunur** izleyen roldür: bağlı öğrencinin not/karnesini, yoklamasını, ödev raporunu, şube üyeliklerini ve Pomodoro geçmişini görüntüleyebilir; Mesajlar'ı kullanabilir. Veli ayrıca uygun randevuyu ve çocuğu için yemeği ayırabilir. Veli hesabı sınava giremez, derse kaydolamaz ve yoklamada işaretlenmez — bu işlemler öğrenciye özeldir.
> **Nereden/nasıl:** Bağlı öğrencilerini **Çocuklarım** sayfasından (`/students`) görürsün; bir çocuğu seçip notlarına/karnesine ve yoklamasına oradan geçersin.
> **Etkili kullanım:** Birden çok öğrenci tek veliye bağlanabilir — Çocuklarım'dan aralarında geçiş yaparsın. Veli–öğrenci bağlantısını **ADMIN** kurar; bağlantı görünmüyorsa okuldan bağlanmasını iste.

### 515 · PASS · Öğrenci

- Soru: mobil hesap sekmesinden profilime ulaşabilir miyim
- Beklenen intent: `navigation_help`
- Gerçek intent: `navigation_help`
- response_id: `navigation_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ana sayfa", "route": "/"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Masaüstünde sol dikey menüden gezinilir; gruplar rol bazlıdır ve yetkin olmayan öğeler gizlenir. Mobil alt çubuk da role göre değişir: Öğrencide **Bugün, Eğitim, Takvim, Karnem, Hesap**; Öğretmen/Yönetici/ADMIN'de **Bugün, Eğitim, Takvim, Hesap**; Velide **Bugün, Çocuklarım, Takvim, Hesap** görünür. Diğer sayfalara **Hesap/Menü** içinden ulaşırsın. Aradığın sayfayı söylersen gerçek yolunu verebilirim.

### 516 · PASS · Yönetici

- Soru: 400 ile 422 hatasının farkı nedir
- Beklenen intent: `technical_error_help`
- Gerçek intent: `technical_error_help`
- response_id: `technical_error_triage`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Hatanın nedenini ayırabilmem için **hangi sayfada hangi düğmeye bastığını** ve ekrandaki hata metnini aynen yaz. Genel anlamı şöyledir: **400** alan/değer iş kuralına uymuyor, **401** oturum yok/süresi dolmuş, **403** rol veya ders/öğrenci kapsamı yetersiz, **404** kayıt yok ya da güvenlik için gizlenmiş, **409** işlem mevcut durumla çakışıyor, **413** dosya okul sınırını aşıyor, **422** istek gövdesinde zorunlu alan/tip/biçim yanlış, **429** çok sık istek gönderildiği, **503** hizmet/veritabanı geçici olarak ulaşılamadığı anlamına gelir. 401'de yeniden giriş yap; 429/503'te kısa süre bekleyip bir kez daha dene. Yazma isteği zaman aşımına uğradıysa işlemi tekrarlamadan önce kaydın oluşup oluşmadığını kontrol et.

### 517 · PASS · Öğretmen

- Soru: bu öğrenciyi dersten çıkaracağım
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 518 · PASS · Öğretmen

- Soru: sınıf listesinden öğrenciyi nasıl kaldırırım
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 519 · PASS · Yönetici

- Soru: öğrencinin ders kaydını sonlandırmam lazım
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 520 · PASS · Öğretmen

- Soru: rosterdaki remove düğmesini bulamadım
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 521 · PASS · ADMIN

- Soru: öğrenciyi course roster içinden remove etmek istiyorum
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 522 · PASS · Yönetici

- Soru: öğrenci hesabını değil yalnız ders kaydını kaldıracağım
- Beklenen intent: `course_remove_student`
- Gerçek intent: `course_remove_student`
- response_id: `remove_student_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> 1) Ders detayı → **Sınıf listesi (Roster)** bölümünü aç. 2) İlgili öğrenci satırında **Kaldır (Remove)**'a bas ve onayla. Bunun için dersi yönetme yetkin olmalı. Çıkarmak geçmiş sınav sonuçlarını **silmez**; raporlarda öğrenci yeniden kaydedilene kadar gizlenir ve öğrenci daha sonra tekrar derse kaydedilebilir.

### 523 · PASS · Veli

- Soru: defterdeki kişisel notumu kaldıracağım
- Beklenen intent: `note_delete`
- Gerçek intent: `note_delete`
- response_id: `note_delete_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu silmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Sil**'i seç. 3) Açılan onay penceresinde silme işlemini onayla. Yalnızca kendi Defter notlarını silebilirsin.

### 524 · PASS · Öğrenci

- Soru: yazdığım notu silmek istiyorum
- Beklenen intent: `note_delete`
- Gerçek intent: `note_delete`
- response_id: `note_delete_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu silmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Sil**'i seç. 3) Açılan onay penceresinde silme işlemini onayla. Yalnızca kendi Defter notlarını silebilirsin.

### 525 · PASS · Öğretmen

- Soru: kişisel notta değişiklik yapmam lazım
- Beklenen intent: `note_edit`
- Gerçek intent: `note_edit`
- response_id: `note_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu değiştirmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Düzenle**'yi seç. 3) Başlığı veya içeriği değiştirip **Güncelle**'ye bas ve onayla. Yalnızca kendi Defter notlarını düzenleyebilirsin.

### 526 · PASS · Veli

- Soru: defter kaydını yeniden düzenleyeceğim
- Beklenen intent: `note_edit`
- Gerçek intent: `note_edit`
- response_id: `note_edit_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel notunu değiştirmek için: 1) **Defter (Notebook)** menüsünden `/notes` sayfasını aç. 2) İlgili not kartındaki **İşlem** menüsünden **Düzenle**'yi seç. 3) Başlığı veya içeriği değiştirip **Güncelle**'ye bas ve onayla. Yalnızca kendi Defter notlarını düzenleyebilirsin.

### 527 · PASS · Öğrenci

- Soru: profile me sayfasını nereden açarım
- Beklenen intent: `profile_view`
- Gerçek intent: `profile_view`
- response_id: `profile_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kendi profilini `/profile/me` adresinden veya hesap menüsündeki **Profilim** seçeneğinden açabilirsin. Burada profil fotoğrafın, görünen adın/Hakkında alanın, rolün, şube ve ders üyeliklerin, rozetlerin ile odak saati, odak oturumu, teslim edilen/zamanında ödev ve girilen sınav istatistiklerin görünür. Kendi sayfanda **Profili düzenle** düğmesi vardır. Başka bir kişinin profili `/profile/$userId` ile açılır; erişim kapsamını backend denetler ve Veli yalnız kendisini veya bağlı çocuklarını görebilir.

### 528 · PASS · Veli

- Soru: profilim ekranındaki rozet ve istatistikler nerede
- Beklenen intent: `profile_view`
- Gerçek intent: `profile_view`
- response_id: `profile_view_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Profilim", "route": "/profile/me"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kendi profilini `/profile/me` adresinden veya hesap menüsündeki **Profilim** seçeneğinden açabilirsin. Burada profil fotoğrafın, görünen adın/Hakkında alanın, rolün, şube ve ders üyeliklerin, rozetlerin ile odak saati, odak oturumu, teslim edilen/zamanında ödev ve girilen sınav istatistiklerin görünür. Kendi sayfanda **Profili düzenle** düğmesi vardır. Başka bir kişinin profili `/profile/$userId` ile açılır; erişim kapsamını backend denetler ve Veli yalnız kendisini veya bağlı çocuklarını görebilir.

### 529 · PASS · Öğrenci

- Soru: ayarlar penceresinde hesabımı düzenlemek istiyorum
- Beklenen intent: `personal_settings`
- Gerçek intent: `personal_settings`
- response_id: `personal_settings_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel **Ayarlar** bir sayfa değil, sağ üstteki hesap/avatar menüsünden açılan penceredir. **Hesap** bölümünde Ad, Soyad, E-posta, Telefon ve Doğum tarihini; **Görünüm** bölümünde Açık/Koyu tema, Türkçe/English dil ve vurgu renk paletini değiştirebilirsin. Görünen ad, Hakkında ve profil fotoğrafı gibi tam profil seçenekleri için `/profile/me` → **Profili düzenle** yolunu kullan. Okul geneli ayarlar ise bundan ayrıdır ve `/management/settings` altında yalnız yetkili hesaplara görünür.

### 530 · PASS · Öğretmen

- Soru: hesap menüsündeki settings ayrı bir sayfa mı
- Beklenen intent: `personal_settings`
- Gerçek intent: `personal_settings`
- response_id: `personal_settings_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel **Ayarlar** bir sayfa değil, sağ üstteki hesap/avatar menüsünden açılan penceredir. **Hesap** bölümünde Ad, Soyad, E-posta, Telefon ve Doğum tarihini; **Görünüm** bölümünde Açık/Koyu tema, Türkçe/English dil ve vurgu renk paletini değiştirebilirsin. Görünen ad, Hakkında ve profil fotoğrafı gibi tam profil seçenekleri için `/profile/me` → **Profili düzenle** yolunu kullan. Okul geneli ayarlar ise bundan ayrıdır ve `/management/settings` altında yalnız yetkili hesaplara görünür.

### 531 · PASS · Veli

- Soru: ayarlar görünüm kısmında vurgu rengini değiştireceğim
- Beklenen intent: `personal_settings`
- Gerçek intent: `personal_settings`
- response_id: `personal_settings_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel **Ayarlar** bir sayfa değil, sağ üstteki hesap/avatar menüsünden açılan penceredir. **Hesap** bölümünde Ad, Soyad, E-posta, Telefon ve Doğum tarihini; **Görünüm** bölümünde Açık/Koyu tema, Türkçe/English dil ve vurgu renk paletini değiştirebilirsin. Görünen ad, Hakkında ve profil fotoğrafı gibi tam profil seçenekleri için `/profile/me` → **Profili düzenle** yolunu kullan. Okul geneli ayarlar ise bundan ayrıdır ve `/management/settings` altında yalnız yetkili hesaplara görünür.

### 532 · PASS · Öğrenci

- Soru: dosya yükleyemiyorum neden
- Beklenen intent: `upload_problem`
- Gerçek intent: `upload_problem`
- response_id: `upload_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Dosya yüklemede önce alanı ayır: **400**; multipart içindeki `file` alanı eksik, dosya boş veya gövde bozuk olabilir. **413**, dosyanın sunucu/okul boyut sınırını aştığını gösterir; güncel sınır okulun Sistem ayarındadır (varsayılan yaklaşık 5 MiB). Defter, ders notu ve ödev tesliminde kayıt başına en fazla **10 dosya** vardır; önce bir eki sil. Satır içinde gösterilecek görseller yalnız PNG/JPEG/WebP/GIF'tir; SVG desteklenmez. Hata sürerse hangi sayfada yüklediğini, dosya türü/boyutunu ve tam hata metnini yaz; kişisel dosya içeriğini sohbete kopyalama.

### 533 · PASS · Öğretmen

- Soru: on birinci eki ekleyemiyorum
- Beklenen intent: `upload_problem`
- Gerçek intent: `upload_problem`
- response_id: `upload_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Dosya yüklemede önce alanı ayır: **400**; multipart içindeki `file` alanı eksik, dosya boş veya gövde bozuk olabilir. **413**, dosyanın sunucu/okul boyut sınırını aştığını gösterir; güncel sınır okulun Sistem ayarındadır (varsayılan yaklaşık 5 MiB). Defter, ders notu ve ödev tesliminde kayıt başına en fazla **10 dosya** vardır; önce bir eki sil. Satır içinde gösterilecek görseller yalnız PNG/JPEG/WebP/GIF'tir; SVG desteklenmez. Hata sürerse hangi sayfada yüklediğini, dosya türü/boyutunu ve tam hata metnini yaz; kişisel dosya içeriğini sohbete kopyalama.

### 534 · PASS · Öğrenci

- Soru: çelebi çalışmıyor neden
- Beklenen intent: `chatbot_service_problem`
- Gerçek intent: `chatbot_service_problem`
- response_id: `chatbot_service_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Çelebi yanıt vermiyorsa hata metnini ayır: **AI service is not enabled**, backend'de köprü özelliğinin kapalı; **no AI service is connected**, çalışan chatbot bridge'in backend'e bağlı olmadığını gösterir. Bu durumlarda istek **503** olur ve mesaj kaydı oluşturulmaz. **429** mesaj hız sınırıdır; `Retry-After` kadar bekle. Kabul edilen mesaj önce **202/pending** olabilir; uzun süre tamamlanmazsa `unavailable`, `busy`, `timed_out`, `transport`, `protocol`, `bad_reply`, `empty_reply`, `interrupted` ya da köprünün döndürdüğü başka bir servis koduyla başarısız görünür. Uzak servis boş bir kod döndürürse backend bunu `service_error` olarak kaydeder. Thread limiti dolduysa kullanılmayan bir sohbeti sil; thread silmek içindeki bütün mesajları da kalıcı siler. Yabancı thread kimliği güvenlik için 404 döner.

### 535 · PASS · ADMIN

- Soru: chatbot backend servisine bağlanamıyor
- Beklenen intent: `chatbot_service_problem`
- Gerçek intent: `chatbot_service_problem`
- response_id: `chatbot_service_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Çelebi yanıt vermiyorsa hata metnini ayır: **AI service is not enabled**, backend'de köprü özelliğinin kapalı; **no AI service is connected**, çalışan chatbot bridge'in backend'e bağlı olmadığını gösterir. Bu durumlarda istek **503** olur ve mesaj kaydı oluşturulmaz. **429** mesaj hız sınırıdır; `Retry-After` kadar bekle. Kabul edilen mesaj önce **202/pending** olabilir; uzun süre tamamlanmazsa `unavailable`, `busy`, `timed_out`, `transport`, `protocol`, `bad_reply`, `empty_reply`, `interrupted` ya da köprünün döndürdüğü başka bir servis koduyla başarısız görünür. Uzak servis boş bir kod döndürürse backend bunu `service_error` olarak kaydeder. Thread limiti dolduysa kullanılmayan bir sohbeti sil; thread silmek içindeki bütün mesajları da kalıcı siler. Yabancı thread kimliği güvenlik için 404 döner.

### 536 · PASS · Yönetici

- Soru: çelebi bad_reply durumuna düştü
- Beklenen intent: `chatbot_service_problem`
- Gerçek intent: `chatbot_service_problem`
- response_id: `chatbot_service_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Çelebi yanıt vermiyorsa hata metnini ayır: **AI service is not enabled**, backend'de köprü özelliğinin kapalı; **no AI service is connected**, çalışan chatbot bridge'in backend'e bağlı olmadığını gösterir. Bu durumlarda istek **503** olur ve mesaj kaydı oluşturulmaz. **429** mesaj hız sınırıdır; `Retry-After` kadar bekle. Kabul edilen mesaj önce **202/pending** olabilir; uzun süre tamamlanmazsa `unavailable`, `busy`, `timed_out`, `transport`, `protocol`, `bad_reply`, `empty_reply`, `interrupted` ya da köprünün döndürdüğü başka bir servis koduyla başarısız görünür. Uzak servis boş bir kod döndürürse backend bunu `service_error` olarak kaydeder. Thread limiti dolduysa kullanılmayan bir sohbeti sil; thread silmek içindeki bütün mesajları da kalıcı siler. Yabancı thread kimliği güvenlik için 404 döner.

### 537 · PASS · Öğretmen

- Soru: çelebi empty_reply koduyla başarısız oldu
- Beklenen intent: `chatbot_service_problem`
- Gerçek intent: `chatbot_service_problem`
- response_id: `chatbot_service_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Çelebi yanıt vermiyorsa hata metnini ayır: **AI service is not enabled**, backend'de köprü özelliğinin kapalı; **no AI service is connected**, çalışan chatbot bridge'in backend'e bağlı olmadığını gösterir. Bu durumlarda istek **503** olur ve mesaj kaydı oluşturulmaz. **429** mesaj hız sınırıdır; `Retry-After` kadar bekle. Kabul edilen mesaj önce **202/pending** olabilir; uzun süre tamamlanmazsa `unavailable`, `busy`, `timed_out`, `transport`, `protocol`, `bad_reply`, `empty_reply`, `interrupted` ya da köprünün döndürdüğü başka bir servis koduyla başarısız görünür. Uzak servis boş bir kod döndürürse backend bunu `service_error` olarak kaydeder. Thread limiti dolduysa kullanılmayan bir sohbeti sil; thread silmek içindeki bütün mesajları da kalıcı siler. Yabancı thread kimliği güvenlik için 404 döner.

### 538 · PASS · Öğrenci

- Soru: chatbot mesajı interrupted görünüyor
- Beklenen intent: `chatbot_service_problem`
- Gerçek intent: `chatbot_service_problem`
- response_id: `chatbot_service_problem_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Çelebi yanıt vermiyorsa hata metnini ayır: **AI service is not enabled**, backend'de köprü özelliğinin kapalı; **no AI service is connected**, çalışan chatbot bridge'in backend'e bağlı olmadığını gösterir. Bu durumlarda istek **503** olur ve mesaj kaydı oluşturulmaz. **429** mesaj hız sınırıdır; `Retry-After` kadar bekle. Kabul edilen mesaj önce **202/pending** olabilir; uzun süre tamamlanmazsa `unavailable`, `busy`, `timed_out`, `transport`, `protocol`, `bad_reply`, `empty_reply`, `interrupted` ya da köprünün döndürdüğü başka bir servis koduyla başarısız görünür. Uzak servis boş bir kod döndürürse backend bunu `service_error` olarak kaydeder. Thread limiti dolduysa kullanılmayan bir sohbeti sil; thread silmek içindeki bütün mesajları da kalıcı siler. Yabancı thread kimliği güvenlik için 404 döner.

### 539 · PASS · Yönetici

- Soru: şube oluşturma formunda kapasite alanı neden yok
- Beklenen intent: `class_section_manage`
- Gerçek intent: `class_section_manage`
- response_id: `class_section_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Şubeler", "route": "/management/classes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Şube yönetimi için **Şubeler** (`/management/classes`, Yönetici+) sayfasını aç. **Şube oluştur** ile zorunlu sınıf adını; isteğe bağlı sınıf düzeyi, dönem ve sınıf öğretmenini gir. Mevcut şubenin detayında düzenleme/silme, öğrenci ekleme-çıkarma ve ders bağlama-ayırma işlemleri vardır. Oluşturma formunda ayrı bir **kapasite** alanı yoktur. Şubeye öğrenci eklemek bağlı derslere kayıtları tek işlemde kurar; öğrenci zaten üyeyse, şube/ders kapasitesi dolmuşsa veya bağlı ders bulunamazsa işlem 409 ile bütünüyle reddedilir. Üyesi ya da bağlı dersi olan şube silinemez; önce ilişkileri kaldır. Buradaki **şube/sınıf grubu**, `/courses` üzerindeki **ders oluşturma** işleminden farklıdır.

### 540 · PASS · Veli

- Soru: takvim görünümü haftalık mı aylık mı
- Beklenen intent: `calendar_info`
- Gerçek intent: `calendar_info`
- response_id: `calendar_info_message`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Takvim", "route": "/calendar"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Takvim** (`/calendar`) aylık görünümde sınav, ödev, etkinlik, randevu ve ders oturumlarını birleştirir. **Bugün** düğmesiyle geçerli aya/güne dönebilir, bir günü seçerek o günün ayrıntılarını görebilirsin.

### 541 · PASS · Veli

- Soru: oturumum bitince gelen 401 için yeniden mi giriş yapmalıyım
- Beklenen intent: `session_info`
- Gerçek intent: `session_info`
- response_id: `session_duration_info`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `None`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Giriş yapınca **7 gün** geçerli bir oturum açılır. Süre sunucu saatiyle ölçülür; cihazının saati yanlış olsa bile değişmez. Çıkış yapmak oturumu hemen kapatır. Süre dolduktan sonra korumalı bir istek **401** dönebilir; bu durumda `/login` üzerinden yeniden giriş yap.

### 542 · PASS · Öğrenci

- Soru: PDF ders notlarımı Deftere içe aktarmak istiyorum
- Beklenen intent: `note_import_ocr`
- Gerçek intent: `note_import_ocr`
- response_id: `note_import_ocr_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Defter** (`/notes`) sayfasında **İçe aktar**'a basıp PDF, TXT veya Markdown dosyanı seç. Hezarfen dosyadaki mevcut metni tarayıcıda çıkarır; satır sonu, sayfa numarası ve gürültüyü temizleyerek düzenlenebilir bir **Başlık** ve Markdown **İçerik** önizlemesi hazırlar. Kontrol edip **Oluştur**'a basınca yalnız sana ait yeni bir Defter notu kaydedilir. Bu araç görüntü tabanlı/taranmış PDF'ye kendi başına OCR uygulamaz: 'metin çıkarılamadı' uyarısında dosyayı önce bir OCR aracıyla aranabilir PDF/TXT'ye dönüştürüp yeniden seç. Bozuk karakter uyarısı çıkarsa metni oluşturmadan önce elle düzelt. İçe aktarma özgün dosyayı ek olarak saklamaz; dosyayı da tutmak istiyorsan notu açıp **Ekler → Dosya ekle** kullan.

### 543 · PASS · Veli

- Soru: taranmış PDF dosyasında OCR yapılıyor mu
- Beklenen intent: `note_import_ocr`
- Gerçek intent: `note_import_ocr`
- response_id: `note_import_ocr_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Defter** (`/notes`) sayfasında **İçe aktar**'a basıp PDF, TXT veya Markdown dosyanı seç. Hezarfen dosyadaki mevcut metni tarayıcıda çıkarır; satır sonu, sayfa numarası ve gürültüyü temizleyerek düzenlenebilir bir **Başlık** ve Markdown **İçerik** önizlemesi hazırlar. Kontrol edip **Oluştur**'a basınca yalnız sana ait yeni bir Defter notu kaydedilir. Bu araç görüntü tabanlı/taranmış PDF'ye kendi başına OCR uygulamaz: 'metin çıkarılamadı' uyarısında dosyayı önce bir OCR aracıyla aranabilir PDF/TXT'ye dönüştürüp yeniden seç. Bozuk karakter uyarısı çıkarsa metni oluşturmadan önce elle düzelt. İçe aktarma özgün dosyayı ek olarak saklamaz; dosyayı da tutmak istiyorsan notu açıp **Ekler → Dosya ekle** kullan.

### 544 · PASS · Öğretmen

- Soru: Markdown dosyamı Deftere aktarabilir miyim
- Beklenen intent: `note_import_ocr`
- Gerçek intent: `note_import_ocr`
- response_id: `note_import_ocr_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Defter** (`/notes`) sayfasında **İçe aktar**'a basıp PDF, TXT veya Markdown dosyanı seç. Hezarfen dosyadaki mevcut metni tarayıcıda çıkarır; satır sonu, sayfa numarası ve gürültüyü temizleyerek düzenlenebilir bir **Başlık** ve Markdown **İçerik** önizlemesi hazırlar. Kontrol edip **Oluştur**'a basınca yalnız sana ait yeni bir Defter notu kaydedilir. Bu araç görüntü tabanlı/taranmış PDF'ye kendi başına OCR uygulamaz: 'metin çıkarılamadı' uyarısında dosyayı önce bir OCR aracıyla aranabilir PDF/TXT'ye dönüştürüp yeniden seç. Bozuk karakter uyarısı çıkarsa metni oluşturmadan önce elle düzelt. İçe aktarma özgün dosyayı ek olarak saklamaz; dosyayı da tutmak istiyorsan notu açıp **Ekler → Dosya ekle** kullan.

### 545 · PASS · ADMIN

- Soru: not içe aktarırken metin çıkarılamadı
- Beklenen intent: `note_import_ocr`
- Gerçek intent: `note_import_ocr`
- response_id: `note_import_ocr_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Defter** (`/notes`) sayfasında **İçe aktar**'a basıp PDF, TXT veya Markdown dosyanı seç. Hezarfen dosyadaki mevcut metni tarayıcıda çıkarır; satır sonu, sayfa numarası ve gürültüyü temizleyerek düzenlenebilir bir **Başlık** ve Markdown **İçerik** önizlemesi hazırlar. Kontrol edip **Oluştur**'a basınca yalnız sana ait yeni bir Defter notu kaydedilir. Bu araç görüntü tabanlı/taranmış PDF'ye kendi başına OCR uygulamaz: 'metin çıkarılamadı' uyarısında dosyayı önce bir OCR aracıyla aranabilir PDF/TXT'ye dönüştürüp yeniden seç. Bozuk karakter uyarısı çıkarsa metni oluşturmadan önce elle düzelt. İçe aktarma özgün dosyayı ek olarak saklamaz; dosyayı da tutmak istiyorsan notu açıp **Ekler → Dosya ekle** kullan.

### 546 · PASS · Yönetici

- Soru: Defter notu aktarımındaki bozuk karakterleri nasıl düzeltirim
- Beklenen intent: `note_import_ocr`
- Gerçek intent: `note_import_ocr`
- response_id: `note_import_ocr_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Defter** (`/notes`) sayfasında **İçe aktar**'a basıp PDF, TXT veya Markdown dosyanı seç. Hezarfen dosyadaki mevcut metni tarayıcıda çıkarır; satır sonu, sayfa numarası ve gürültüyü temizleyerek düzenlenebilir bir **Başlık** ve Markdown **İçerik** önizlemesi hazırlar. Kontrol edip **Oluştur**'a basınca yalnız sana ait yeni bir Defter notu kaydedilir. Bu araç görüntü tabanlı/taranmış PDF'ye kendi başına OCR uygulamaz: 'metin çıkarılamadı' uyarısında dosyayı önce bir OCR aracıyla aranabilir PDF/TXT'ye dönüştürüp yeniden seç. Bozuk karakter uyarısı çıkarsa metni oluşturmadan önce elle düzelt. İçe aktarma özgün dosyayı ek olarak saklamaz; dosyayı da tutmak istiyorsan notu açıp **Ekler → Dosya ekle** kullan.

### 547 · PASS · Ziyaretçi

- Soru: ziyaretçiyim PDF'yi Deftere içe aktarabilir miyim
- Beklenen intent: `note_import_ocr`
- Gerçek intent: `note_import_ocr`
- response_id: `note_import_ocr_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `login_required`
- navigation: `None`
- assistant outcome/reason: `deny` / `authentication_required`
- Sözleşme: `PASS`

> Bu konu için önce giriş yapman gerekiyor. `/login` sayfasından güvenli biçimde giriş yapabilirsin.

### 548 · PASS · Öğrenci

- Soru: Defter notuma dosya eklemek istiyorum
- Beklenen intent: `note_file_manage`
- Gerçek intent: `note_file_manage`
- response_id: `note_file_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel not eklerini yönetmek için **Defter** (`/notes`) sayfasında not kartını aç ve okuyucu içindeki **Ekler** bölümüne git. **Dosya ekle** ile yükleyebilir, dosya kartından **Görüntüle** veya **İndir** diyebilir, **Sil** ile yalnız o eki onaylayarak kaldırabilirsin; çizimler için **Çizim** seçeneği de vardır. Her not en fazla **10 dosya** taşır ve dosya başına okulun `max_file_bytes` sınırı uygulanır (varsayılan yaklaşık 5 MiB): tavan doluysa önce bir eki sil, fazla boyutta 413 alınır. Boş veya bozuk multipart dosya 400'dür. Bazı türler uygulama içinde önizlenmez; bu, dosyanın kaybolduğu anlamına gelmez, **İndir** ile açabilirsin. Kişisel not ve ekleri yalnız sahibine aittir; başka kullanıcının notu 404 ile gizlenir.

### 549 · PASS · Veli

- Soru: kişisel not ekini nasıl silerim
- Beklenen intent: `note_file_manage`
- Gerçek intent: `note_file_manage`
- response_id: `note_file_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel not eklerini yönetmek için **Defter** (`/notes`) sayfasında not kartını aç ve okuyucu içindeki **Ekler** bölümüne git. **Dosya ekle** ile yükleyebilir, dosya kartından **Görüntüle** veya **İndir** diyebilir, **Sil** ile yalnız o eki onaylayarak kaldırabilirsin; çizimler için **Çizim** seçeneği de vardır. Her not en fazla **10 dosya** taşır ve dosya başına okulun `max_file_bytes` sınırı uygulanır (varsayılan yaklaşık 5 MiB): tavan doluysa önce bir eki sil, fazla boyutta 413 alınır. Boş veya bozuk multipart dosya 400'dür. Bazı türler uygulama içinde önizlenmez; bu, dosyanın kaybolduğu anlamına gelmez, **İndir** ile açabilirsin. Kişisel not ve ekleri yalnız sahibine aittir; başka kullanıcının notu 404 ile gizlenir.

### 550 · PASS · Öğretmen

- Soru: Defterdeki eki nereden indiririm
- Beklenen intent: `note_file_manage`
- Gerçek intent: `note_file_manage`
- response_id: `note_file_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel not eklerini yönetmek için **Defter** (`/notes`) sayfasında not kartını aç ve okuyucu içindeki **Ekler** bölümüne git. **Dosya ekle** ile yükleyebilir, dosya kartından **Görüntüle** veya **İndir** diyebilir, **Sil** ile yalnız o eki onaylayarak kaldırabilirsin; çizimler için **Çizim** seçeneği de vardır. Her not en fazla **10 dosya** taşır ve dosya başına okulun `max_file_bytes` sınırı uygulanır (varsayılan yaklaşık 5 MiB): tavan doluysa önce bir eki sil, fazla boyutta 413 alınır. Boş veya bozuk multipart dosya 400'dür. Bazı türler uygulama içinde önizlenmez; bu, dosyanın kaybolduğu anlamına gelmez, **İndir** ile açabilirsin. Kişisel not ve ekleri yalnız sahibine aittir; başka kullanıcının notu 404 ile gizlenir.

### 551 · PASS · ADMIN

- Soru: Defterde on birinci dosyayı neden ekleyemiyorum
- Beklenen intent: `note_file_manage`
- Gerçek intent: `note_file_manage`
- response_id: `note_file_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel not eklerini yönetmek için **Defter** (`/notes`) sayfasında not kartını aç ve okuyucu içindeki **Ekler** bölümüne git. **Dosya ekle** ile yükleyebilir, dosya kartından **Görüntüle** veya **İndir** diyebilir, **Sil** ile yalnız o eki onaylayarak kaldırabilirsin; çizimler için **Çizim** seçeneği de vardır. Her not en fazla **10 dosya** taşır ve dosya başına okulun `max_file_bytes` sınırı uygulanır (varsayılan yaklaşık 5 MiB): tavan doluysa önce bir eki sil, fazla boyutta 413 alınır. Boş veya bozuk multipart dosya 400'dür. Bazı türler uygulama içinde önizlenmez; bu, dosyanın kaybolduğu anlamına gelmez, **İndir** ile açabilirsin. Kişisel not ve ekleri yalnız sahibine aittir; başka kullanıcının notu 404 ile gizlenir.

### 552 · PASS · Yönetici

- Soru: Defterdeki kişisel not dosyalarına bir çizim ekleyebilir miyim
- Beklenen intent: `note_file_manage`
- Gerçek intent: `note_file_manage`
- response_id: `note_file_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Defter", "route": "/notes"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Kişisel not eklerini yönetmek için **Defter** (`/notes`) sayfasında not kartını aç ve okuyucu içindeki **Ekler** bölümüne git. **Dosya ekle** ile yükleyebilir, dosya kartından **Görüntüle** veya **İndir** diyebilir, **Sil** ile yalnız o eki onaylayarak kaldırabilirsin; çizimler için **Çizim** seçeneği de vardır. Her not en fazla **10 dosya** taşır ve dosya başına okulun `max_file_bytes` sınırı uygulanır (varsayılan yaklaşık 5 MiB): tavan doluysa önce bir eki sil, fazla boyutta 413 alınır. Boş veya bozuk multipart dosya 400'dür. Bazı türler uygulama içinde önizlenmez; bu, dosyanın kaybolduğu anlamına gelmez, **İndir** ile açabilirsin. Kişisel not ve ekleri yalnız sahibine aittir; başka kullanıcının notu 404 ile gizlenir.

### 553 · PASS · Ziyaretçi

- Soru: giriş yapmadan kişisel notuma dosya ekleyebilir miyim
- Beklenen intent: `note_file_manage`
- Gerçek intent: `note_file_manage`
- response_id: `note_file_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `login_required`
- navigation: `None`
- assistant outcome/reason: `deny` / `authentication_required`
- Sözleşme: `PASS`

> Bu konu için önce giriş yapman gerekiyor. `/login` sayfasından güvenli biçimde giriş yapabilirsin.

### 554 · PASS · Öğretmen

- Soru: dersime yeni bir müfredat konusu eklemek istiyorum
- Beklenen intent: `course_subject_manage`
- Gerçek intent: `course_subject_manage`
- response_id: `course_subject_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yönettiğin dersin detayını (`/courses/$id`) açıp **Konular** sekmesine geç. **Konu ekle** ile zorunlu **Konu adı** (en fazla 200) ve isteğe bağlı açıklamayı (en fazla 2.000) kaydet; satırın **İşlemler** menüsünden **Düzenle** veya **Kaldır** kullan. Ders oluşturucusu ve atanmış öğretmen yalnız yönettiği derste, Yönetici/ADMIN okul kapsamında yazabilir; öğrenci konuları okuyabilse de değiştiremez. Her sınav sorusu ve ödev aynı dersin bir konusuna bağlıdır. Bu yüzden sınav sorusu veya ödev hâlâ konuyu kullanıyorsa silme **409** olur; önce bunları başka konuya taşı ya da sil. Soru bankası şablonu tek başına silmeyi engellemez; konu silinince şablondaki isteğe bağlı köken bilgisi temizlenir. Yabancı ders konusu seçmek 400, yönetmediğin ders 403'tür.

### 555 · PASS · Yönetici

- Soru: ders konusunun adını değiştirmem lazım
- Beklenen intent: `course_subject_manage`
- Gerçek intent: `course_subject_manage`
- response_id: `course_subject_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yönettiğin dersin detayını (`/courses/$id`) açıp **Konular** sekmesine geç. **Konu ekle** ile zorunlu **Konu adı** (en fazla 200) ve isteğe bağlı açıklamayı (en fazla 2.000) kaydet; satırın **İşlemler** menüsünden **Düzenle** veya **Kaldır** kullan. Ders oluşturucusu ve atanmış öğretmen yalnız yönettiği derste, Yönetici/ADMIN okul kapsamında yazabilir; öğrenci konuları okuyabilse de değiştiremez. Her sınav sorusu ve ödev aynı dersin bir konusuna bağlıdır. Bu yüzden sınav sorusu veya ödev hâlâ konuyu kullanıyorsa silme **409** olur; önce bunları başka konuya taşı ya da sil. Soru bankası şablonu tek başına silmeyi engellemez; konu silinince şablondaki isteğe bağlı köken bilgisi temizlenir. Yabancı ders konusu seçmek 400, yönetmediğin ders 403'tür.

### 556 · PASS · ADMIN

- Soru: ders konusunu silerken 409 alıyorum
- Beklenen intent: `course_subject_manage`
- Gerçek intent: `course_subject_manage`
- response_id: `course_subject_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yönettiğin dersin detayını (`/courses/$id`) açıp **Konular** sekmesine geç. **Konu ekle** ile zorunlu **Konu adı** (en fazla 200) ve isteğe bağlı açıklamayı (en fazla 2.000) kaydet; satırın **İşlemler** menüsünden **Düzenle** veya **Kaldır** kullan. Ders oluşturucusu ve atanmış öğretmen yalnız yönettiği derste, Yönetici/ADMIN okul kapsamında yazabilir; öğrenci konuları okuyabilse de değiştiremez. Her sınav sorusu ve ödev aynı dersin bir konusuna bağlıdır. Bu yüzden sınav sorusu veya ödev hâlâ konuyu kullanıyorsa silme **409** olur; önce bunları başka konuya taşı ya da sil. Soru bankası şablonu tek başına silmeyi engellemez; konu silinince şablondaki isteğe bağlı köken bilgisi temizlenir. Yabancı ders konusu seçmek 400, yönetmediğin ders 403'tür.

### 557 · PASS · Öğretmen

- Soru: ödeve bağlı ders konusunu neden silemiyorum
- Beklenen intent: `course_subject_manage`
- Gerçek intent: `course_subject_manage`
- response_id: `course_subject_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yönettiğin dersin detayını (`/courses/$id`) açıp **Konular** sekmesine geç. **Konu ekle** ile zorunlu **Konu adı** (en fazla 200) ve isteğe bağlı açıklamayı (en fazla 2.000) kaydet; satırın **İşlemler** menüsünden **Düzenle** veya **Kaldır** kullan. Ders oluşturucusu ve atanmış öğretmen yalnız yönettiği derste, Yönetici/ADMIN okul kapsamında yazabilir; öğrenci konuları okuyabilse de değiştiremez. Her sınav sorusu ve ödev aynı dersin bir konusuna bağlıdır. Bu yüzden sınav sorusu veya ödev hâlâ konuyu kullanıyorsa silme **409** olur; önce bunları başka konuya taşı ya da sil. Soru bankası şablonu tek başına silmeyi engellemez; konu silinince şablondaki isteğe bağlı köken bilgisi temizlenir. Yabancı ders konusu seçmek 400, yönetmediğin ders 403'tür.

### 558 · PASS · Öğrenci

- Soru: öğrenci olarak ders konusunu düzenleyebilir miyim
- Beklenen intent: `course_subject_manage`
- Gerçek intent: `course_subject_manage`
- response_id: `course_subject_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 559 · PASS · Veli

- Soru: veli ders için müfredat konusu oluşturabilir mi
- Beklenen intent: `course_subject_manage`
- Gerçek intent: `course_subject_manage`
- response_id: `course_subject_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 560 · PASS · Öğretmen

- Soru: sınıfla paylaşılacak bir ders notu oluşturmak istiyorum
- Beklenen intent: `course_note_manage`
- Gerçek intent: `course_note_manage`
- response_id: `course_note_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ders detayında (`/courses/$id`) **Ders notları** sekmesini aç. Dersin oluşturucusu/atanmış öğretmeni veya Yönetici/ADMIN burada **Yeni ders notu** ile başlık, içerik ve en fazla 10 dosya ekleyebilir; not kartından düzenleyebilir, silebilir ve **Ekler** bölümünü yönetebilir. Derse kayıtlı öğrenci notları ve dosyaları okuyup indirebilir ama ekleme, düzenleme veya silme yapamaz. Dosya başına okul boyut sınırı vardır; 11. ek 409, fazla boyut 413, boş/bozuk dosya 400 verir. Oluşturma sırasında bazı ekler yüklenemezse not yine kaydedilmiş olabilir ve arayüz başarısız ek sayısını gösterir; sayfayı yenileyip eksik ekleri yeniden yükle. Ders notunu silmek bütün eklerini de kalıcı siler. Yönetmediğin ders 403, görünmeyen ders/not 404 ile sonuçlanır. Bu alan kişisel **Defter** notundan ayrıdır.

### 561 · PASS · Yönetici

- Soru: ders notundaki PDF dosyasını değiştirmek istiyorum
- Beklenen intent: `course_note_manage`
- Gerçek intent: `course_note_manage`
- response_id: `course_note_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ders detayında (`/courses/$id`) **Ders notları** sekmesini aç. Dersin oluşturucusu/atanmış öğretmeni veya Yönetici/ADMIN burada **Yeni ders notu** ile başlık, içerik ve en fazla 10 dosya ekleyebilir; not kartından düzenleyebilir, silebilir ve **Ekler** bölümünü yönetebilir. Derse kayıtlı öğrenci notları ve dosyaları okuyup indirebilir ama ekleme, düzenleme veya silme yapamaz. Dosya başına okul boyut sınırı vardır; 11. ek 409, fazla boyut 413, boş/bozuk dosya 400 verir. Oluşturma sırasında bazı ekler yüklenemezse not yine kaydedilmiş olabilir ve arayüz başarısız ek sayısını gösterir; sayfayı yenileyip eksik ekleri yeniden yükle. Ders notunu silmek bütün eklerini de kalıcı siler. Yönetmediğin ders 403, görünmeyen ders/not 404 ile sonuçlanır. Bu alan kişisel **Defter** notundan ayrıdır.

### 562 · PASS · ADMIN

- Soru: ders notu dosyalarından bazıları yüklenmedi
- Beklenen intent: `course_note_manage`
- Gerçek intent: `course_note_manage`
- response_id: `course_note_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ders detayında (`/courses/$id`) **Ders notları** sekmesini aç. Dersin oluşturucusu/atanmış öğretmeni veya Yönetici/ADMIN burada **Yeni ders notu** ile başlık, içerik ve en fazla 10 dosya ekleyebilir; not kartından düzenleyebilir, silebilir ve **Ekler** bölümünü yönetebilir. Derse kayıtlı öğrenci notları ve dosyaları okuyup indirebilir ama ekleme, düzenleme veya silme yapamaz. Dosya başına okul boyut sınırı vardır; 11. ek 409, fazla boyut 413, boş/bozuk dosya 400 verir. Oluşturma sırasında bazı ekler yüklenemezse not yine kaydedilmiş olabilir ve arayüz başarısız ek sayısını gösterir; sayfayı yenileyip eksik ekleri yeniden yükle. Ders notunu silmek bütün eklerini de kalıcı siler. Yönetmediğin ders 403, görünmeyen ders/not 404 ile sonuçlanır. Bu alan kişisel **Defter** notundan ayrıdır.

### 563 · PASS · Öğretmen

- Soru: ders notuna on birinci eki neden koyamıyorum
- Beklenen intent: `course_note_manage`
- Gerçek intent: `course_note_manage`
- response_id: `course_note_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ders detayında (`/courses/$id`) **Ders notları** sekmesini aç. Dersin oluşturucusu/atanmış öğretmeni veya Yönetici/ADMIN burada **Yeni ders notu** ile başlık, içerik ve en fazla 10 dosya ekleyebilir; not kartından düzenleyebilir, silebilir ve **Ekler** bölümünü yönetebilir. Derse kayıtlı öğrenci notları ve dosyaları okuyup indirebilir ama ekleme, düzenleme veya silme yapamaz. Dosya başına okul boyut sınırı vardır; 11. ek 409, fazla boyut 413, boş/bozuk dosya 400 verir. Oluşturma sırasında bazı ekler yüklenemezse not yine kaydedilmiş olabilir ve arayüz başarısız ek sayısını gösterir; sayfayı yenileyip eksik ekleri yeniden yükle. Ders notunu silmek bütün eklerini de kalıcı siler. Yönetmediğin ders 403, görünmeyen ders/not 404 ile sonuçlanır. Bu alan kişisel **Defter** notundan ayrıdır.

### 564 · PASS · Öğrenci

- Soru: öğrenci öğretmenin ders notunu silebilir mi
- Beklenen intent: `course_note_manage`
- Gerçek intent: `course_note_manage`
- response_id: `course_note_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 565 · PASS · Veli

- Soru: veli olarak derse not ekleyebilir miyim
- Beklenen intent: `course_note_manage`
- Gerçek intent: `course_note_manage`
- response_id: `course_note_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 566 · PASS · Yönetici

- Soru: derse başka bir öğretmen atamak istiyorum
- Beklenen intent: `course_teacher_manage`
- Gerçek intent: `course_teacher_manage`
- response_id: `course_teacher_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ders detayında (`/courses/$id`) **Öğretmenler** sekmesine git. Yalnız **Yönetici** veya **ADMIN**, **Öğretmen ata** ile Öğretmen ya da daha üst roldeki hesabı seçebilir; atanmış satırda **Öğretmeni çıkar** ile ilişkiyi kaldırabilir. Dersin kendi öğretmen oluşturucusu bu kadroyu değiştiremez. Atama idempotenttir; zaten atanmış kişi yeniden seçilirse çoğaltılmaz. Atanan kişi sınav, oturum, konu, sınıf listesi ve notlandırma dahil dersi yönetir; fakat yalnız bu atamayla dersi silemez veya öğretmen listesini değiştiremez. Hedef hesap yoksa/Öğretmen altındaysa 400, atama sırasında rolü düşürülürse işlem geri alınıp 409, atanmış olmayan kişiyi çıkarma 404 olur. Çıkarmak ders, sınav, oturum ve öğrenci kayıtlarını silmez; yalnız öğretmenin yönetim hakkını geri alır.

### 567 · PASS · ADMIN

- Soru: atanmış öğretmeni dersten çıkarmam lazım
- Beklenen intent: `course_teacher_manage`
- Gerçek intent: `course_teacher_manage`
- response_id: `course_teacher_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ders detayında (`/courses/$id`) **Öğretmenler** sekmesine git. Yalnız **Yönetici** veya **ADMIN**, **Öğretmen ata** ile Öğretmen ya da daha üst roldeki hesabı seçebilir; atanmış satırda **Öğretmeni çıkar** ile ilişkiyi kaldırabilir. Dersin kendi öğretmen oluşturucusu bu kadroyu değiştiremez. Atama idempotenttir; zaten atanmış kişi yeniden seçilirse çoğaltılmaz. Atanan kişi sınav, oturum, konu, sınıf listesi ve notlandırma dahil dersi yönetir; fakat yalnız bu atamayla dersi silemez veya öğretmen listesini değiştiremez. Hedef hesap yoksa/Öğretmen altındaysa 400, atama sırasında rolü düşürülürse işlem geri alınıp 409, atanmış olmayan kişiyi çıkarma 404 olur. Çıkarmak ders, sınav, oturum ve öğrenci kayıtlarını silmez; yalnız öğretmenin yönetim hakkını geri alır.

### 568 · PASS · Öğretmen

- Soru: öğretmen olarak dersin öğretmen listesini değiştirebilir miyim
- Beklenen intent: `course_teacher_manage`
- Gerçek intent: `course_teacher_manage`
- response_id: `course_teacher_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 569 · PASS · Yönetici

- Soru: öğretmen atarken hedef rolü uygun değil diyor
- Beklenen intent: `course_teacher_manage`
- Gerçek intent: `course_teacher_manage`
- response_id: `course_teacher_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ders detayında (`/courses/$id`) **Öğretmenler** sekmesine git. Yalnız **Yönetici** veya **ADMIN**, **Öğretmen ata** ile Öğretmen ya da daha üst roldeki hesabı seçebilir; atanmış satırda **Öğretmeni çıkar** ile ilişkiyi kaldırabilir. Dersin kendi öğretmen oluşturucusu bu kadroyu değiştiremez. Atama idempotenttir; zaten atanmış kişi yeniden seçilirse çoğaltılmaz. Atanan kişi sınav, oturum, konu, sınıf listesi ve notlandırma dahil dersi yönetir; fakat yalnız bu atamayla dersi silemez veya öğretmen listesini değiştiremez. Hedef hesap yoksa/Öğretmen altındaysa 400, atama sırasında rolü düşürülürse işlem geri alınıp 409, atanmış olmayan kişiyi çıkarma 404 olur. Çıkarmak ders, sınav, oturum ve öğrenci kayıtlarını silmez; yalnız öğretmenin yönetim hakkını geri alır.

### 570 · PASS · ADMIN

- Soru: atanmamış öğretmeni çıkarınca 404 aldım
- Beklenen intent: `course_teacher_manage`
- Gerçek intent: `course_teacher_manage`
- response_id: `course_teacher_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Ders detayında (`/courses/$id`) **Öğretmenler** sekmesine git. Yalnız **Yönetici** veya **ADMIN**, **Öğretmen ata** ile Öğretmen ya da daha üst roldeki hesabı seçebilir; atanmış satırda **Öğretmeni çıkar** ile ilişkiyi kaldırabilir. Dersin kendi öğretmen oluşturucusu bu kadroyu değiştiremez. Atama idempotenttir; zaten atanmış kişi yeniden seçilirse çoğaltılmaz. Atanan kişi sınav, oturum, konu, sınıf listesi ve notlandırma dahil dersi yönetir; fakat yalnız bu atamayla dersi silemez veya öğretmen listesini değiştiremez. Hedef hesap yoksa/Öğretmen altındaysa 400, atama sırasında rolü düşürülürse işlem geri alınıp 409, atanmış olmayan kişiyi çıkarma 404 olur. Çıkarmak ders, sınav, oturum ve öğrenci kayıtlarını silmez; yalnız öğretmenin yönetim hakkını geri alır.

### 571 · PASS · Öğrenci

- Soru: öğretmeni dersten çıkarınca sınavlar silinir mi
- Beklenen intent: `course_teacher_manage`
- Gerçek intent: `course_teacher_manage`
- response_id: `course_teacher_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 572 · PASS · Öğrenci

- Soru: ödev teslimimi geri çekmek istiyorum
- Beklenen intent: `homework_withdraw_submission`
- Gerçek intent: `homework_withdraw_submission`
- response_id: `homework_withdraw_submission_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yalnız exact **Öğrenci** rolü kendi teslimini geri çekebilir. **Ödevler** (`/homework`) → ödev detayı (`/homework/$id`) → **Ödevi teslim et** panelinde **Teslimi geri çek**'e basıp uyarıyı onayla. Bu işlem teslim metnini ve eklenen **bütün dosyaları kalıcı siler**; ödevin kendisini veya öğretmenin başka öğrencilere verdiği kaydı silmez. Düğme yalnız bir teslim varken ve sonuç/not yokken görünür. Notlandırılmış teslim donmuştur: geri çekme 409 verir; önce öğretmenin notu kaldırması gerekir. Teslim yoksa 404, dersten çıkarıldıysan 403, ödevin hedef kitlesinde değilsen güvenlik için 404 alınır. Son teslim tarihi geçmiş olması tek başına geri çekmeyi engellemez; daha sonra yeniden gönderirsen yeni teslim geç olarak işaretlenir.

### 573 · PASS · Öğrenci

- Soru: ödev teslimimi geri çekip gönderdiğim her şeyi kaldırmak istiyorum
- Beklenen intent: `homework_withdraw_submission`
- Gerçek intent: `homework_withdraw_submission`
- response_id: `homework_withdraw_submission_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yalnız exact **Öğrenci** rolü kendi teslimini geri çekebilir. **Ödevler** (`/homework`) → ödev detayı (`/homework/$id`) → **Ödevi teslim et** panelinde **Teslimi geri çek**'e basıp uyarıyı onayla. Bu işlem teslim metnini ve eklenen **bütün dosyaları kalıcı siler**; ödevin kendisini veya öğretmenin başka öğrencilere verdiği kaydı silmez. Düğme yalnız bir teslim varken ve sonuç/not yokken görünür. Notlandırılmış teslim donmuştur: geri çekme 409 verir; önce öğretmenin notu kaldırması gerekir. Teslim yoksa 404, dersten çıkarıldıysan 403, ödevin hedef kitlesinde değilsen güvenlik için 404 alınır. Son teslim tarihi geçmiş olması tek başına geri çekmeyi engellemez; daha sonra yeniden gönderirsen yeni teslim geç olarak işaretlenir.

### 574 · PASS · Öğrenci

- Soru: teslimi geri çek düğmesi neden görünmüyor
- Beklenen intent: `homework_withdraw_submission`
- Gerçek intent: `homework_withdraw_submission`
- response_id: `homework_withdraw_submission_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yalnız exact **Öğrenci** rolü kendi teslimini geri çekebilir. **Ödevler** (`/homework`) → ödev detayı (`/homework/$id`) → **Ödevi teslim et** panelinde **Teslimi geri çek**'e basıp uyarıyı onayla. Bu işlem teslim metnini ve eklenen **bütün dosyaları kalıcı siler**; ödevin kendisini veya öğretmenin başka öğrencilere verdiği kaydı silmez. Düğme yalnız bir teslim varken ve sonuç/not yokken görünür. Notlandırılmış teslim donmuştur: geri çekme 409 verir; önce öğretmenin notu kaldırması gerekir. Teslim yoksa 404, dersten çıkarıldıysan 403, ödevin hedef kitlesinde değilsen güvenlik için 404 alınır. Son teslim tarihi geçmiş olması tek başına geri çekmeyi engellemez; daha sonra yeniden gönderirsen yeni teslim geç olarak işaretlenir.

### 575 · PASS · Öğrenci

- Soru: ödev teslimini geri çekmeye çalışınca notlandırıldığı için 409 dönüyor
- Beklenen intent: `homework_withdraw_submission`
- Gerçek intent: `homework_withdraw_submission`
- response_id: `homework_withdraw_submission_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yalnız exact **Öğrenci** rolü kendi teslimini geri çekebilir. **Ödevler** (`/homework`) → ödev detayı (`/homework/$id`) → **Ödevi teslim et** panelinde **Teslimi geri çek**'e basıp uyarıyı onayla. Bu işlem teslim metnini ve eklenen **bütün dosyaları kalıcı siler**; ödevin kendisini veya öğretmenin başka öğrencilere verdiği kaydı silmez. Düğme yalnız bir teslim varken ve sonuç/not yokken görünür. Notlandırılmış teslim donmuştur: geri çekme 409 verir; önce öğretmenin notu kaldırması gerekir. Teslim yoksa 404, dersten çıkarıldıysan 403, ödevin hedef kitlesinde değilsen güvenlik için 404 alınır. Son teslim tarihi geçmiş olması tek başına geri çekmeyi engellemez; daha sonra yeniden gönderirsen yeni teslim geç olarak işaretlenir.

### 576 · PASS · Öğrenci

- Soru: ödev teslimini silince dosyalar da gider mi
- Beklenen intent: `homework_withdraw_submission`
- Gerçek intent: `homework_withdraw_submission`
- response_id: `homework_withdraw_submission_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Ödevler", "route": "/homework"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yalnız exact **Öğrenci** rolü kendi teslimini geri çekebilir. **Ödevler** (`/homework`) → ödev detayı (`/homework/$id`) → **Ödevi teslim et** panelinde **Teslimi geri çek**'e basıp uyarıyı onayla. Bu işlem teslim metnini ve eklenen **bütün dosyaları kalıcı siler**; ödevin kendisini veya öğretmenin başka öğrencilere verdiği kaydı silmez. Düğme yalnız bir teslim varken ve sonuç/not yokken görünür. Notlandırılmış teslim donmuştur: geri çekme 409 verir; önce öğretmenin notu kaldırması gerekir. Teslim yoksa 404, dersten çıkarıldıysan 403, ödevin hedef kitlesinde değilsen güvenlik için 404 alınır. Son teslim tarihi geçmiş olması tek başına geri çekmeyi engellemez; daha sonra yeniden gönderirsen yeni teslim geç olarak işaretlenir.

### 577 · PASS · Öğretmen

- Soru: öğretmen öğrencinin teslimini geri çekebilir mi
- Beklenen intent: `homework_withdraw_submission`
- Gerçek intent: `homework_withdraw_submission`
- response_id: `homework_withdraw_submission_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 578 · PASS · Öğretmen

- Soru: var olan ödevi düzenlemek istiyorum
- Beklenen intent: `homework_manage`
- Gerçek intent: `homework_manage`
- response_id: `homework_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yönettiğin dersin detayında (`/courses/$id`) **Ödevler** sekmesine geç. Ödev satırının **İşlemler** menüsünde **Düzenle** ile başlık, açıklama, aynı dersin konusu ve gelecekteki son teslim tarihini değiştir; **Sil** ile ödevi onaylayarak kaldır. Ders oluşturucusu/atanmış öğretmen yalnız yönettiği derste, Yönetici/ADMIN okul kapsamında işlem yapabilir. Yeni son tarih geçmişteyse veya konu başka derse aitse 400 alınır. Backend'de hedef kitleyi daraltan bir değişiklik, kapsam dışına çıkacak öğrencinin teslimi ya da sonucu varsa 409 ile bütünüyle reddedilir; eşzamanlı konu değişiminde de kaydı yeniden okuyup denemek gerekebilir. **Ödevi silmek**, öğrencilerin teslim metinlerini, ek dosyalarını ve not/sonuçlarını da kalıcı siler; yalnız bir öğrencinin kendi teslimini kaldırması farklı olan **Teslimi geri çek** işlemidir.

### 579 · PASS · Yönetici

- Soru: ödevin son teslim tarihini değiştirmem lazım
- Beklenen intent: `homework_manage`
- Gerçek intent: `homework_manage`
- response_id: `homework_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yönettiğin dersin detayında (`/courses/$id`) **Ödevler** sekmesine geç. Ödev satırının **İşlemler** menüsünde **Düzenle** ile başlık, açıklama, aynı dersin konusu ve gelecekteki son teslim tarihini değiştir; **Sil** ile ödevi onaylayarak kaldır. Ders oluşturucusu/atanmış öğretmen yalnız yönettiği derste, Yönetici/ADMIN okul kapsamında işlem yapabilir. Yeni son tarih geçmişteyse veya konu başka derse aitse 400 alınır. Backend'de hedef kitleyi daraltan bir değişiklik, kapsam dışına çıkacak öğrencinin teslimi ya da sonucu varsa 409 ile bütünüyle reddedilir; eşzamanlı konu değişiminde de kaydı yeniden okuyup denemek gerekebilir. **Ödevi silmek**, öğrencilerin teslim metinlerini, ek dosyalarını ve not/sonuçlarını da kalıcı siler; yalnız bir öğrencinin kendi teslimini kaldırması farklı olan **Teslimi geri çek** işlemidir.

### 580 · PASS · ADMIN

- Soru: ödev kaydını tamamen silersem teslimler ne olur
- Beklenen intent: `homework_manage`
- Gerçek intent: `homework_manage`
- response_id: `homework_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yönettiğin dersin detayında (`/courses/$id`) **Ödevler** sekmesine geç. Ödev satırının **İşlemler** menüsünde **Düzenle** ile başlık, açıklama, aynı dersin konusu ve gelecekteki son teslim tarihini değiştir; **Sil** ile ödevi onaylayarak kaldır. Ders oluşturucusu/atanmış öğretmen yalnız yönettiği derste, Yönetici/ADMIN okul kapsamında işlem yapabilir. Yeni son tarih geçmişteyse veya konu başka derse aitse 400 alınır. Backend'de hedef kitleyi daraltan bir değişiklik, kapsam dışına çıkacak öğrencinin teslimi ya da sonucu varsa 409 ile bütünüyle reddedilir; eşzamanlı konu değişiminde de kaydı yeniden okuyup denemek gerekebilir. **Ödevi silmek**, öğrencilerin teslim metinlerini, ek dosyalarını ve not/sonuçlarını da kalıcı siler; yalnız bir öğrencinin kendi teslimini kaldırması farklı olan **Teslimi geri çek** işlemidir.

### 581 · PASS · Öğretmen

- Soru: ödevin bağlı olduğu ders konusunu başka bir konuyla değiştiremiyorum
- Beklenen intent: `homework_manage`
- Gerçek intent: `homework_manage`
- response_id: `homework_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yönettiğin dersin detayında (`/courses/$id`) **Ödevler** sekmesine geç. Ödev satırının **İşlemler** menüsünde **Düzenle** ile başlık, açıklama, aynı dersin konusu ve gelecekteki son teslim tarihini değiştir; **Sil** ile ödevi onaylayarak kaldır. Ders oluşturucusu/atanmış öğretmen yalnız yönettiği derste, Yönetici/ADMIN okul kapsamında işlem yapabilir. Yeni son tarih geçmişteyse veya konu başka derse aitse 400 alınır. Backend'de hedef kitleyi daraltan bir değişiklik, kapsam dışına çıkacak öğrencinin teslimi ya da sonucu varsa 409 ile bütünüyle reddedilir; eşzamanlı konu değişiminde de kaydı yeniden okuyup denemek gerekebilir. **Ödevi silmek**, öğrencilerin teslim metinlerini, ek dosyalarını ve not/sonuçlarını da kalıcı siler; yalnız bir öğrencinin kendi teslimini kaldırması farklı olan **Teslimi geri çek** işlemidir.

### 582 · PASS · Yönetici

- Soru: ödev hedef kitlesini daraltırken 409 alıyorum
- Beklenen intent: `homework_manage`
- Gerçek intent: `homework_manage`
- response_id: `homework_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Dersler", "route": "/courses"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Yönettiğin dersin detayında (`/courses/$id`) **Ödevler** sekmesine geç. Ödev satırının **İşlemler** menüsünde **Düzenle** ile başlık, açıklama, aynı dersin konusu ve gelecekteki son teslim tarihini değiştir; **Sil** ile ödevi onaylayarak kaldır. Ders oluşturucusu/atanmış öğretmen yalnız yönettiği derste, Yönetici/ADMIN okul kapsamında işlem yapabilir. Yeni son tarih geçmişteyse veya konu başka derse aitse 400 alınır. Backend'de hedef kitleyi daraltan bir değişiklik, kapsam dışına çıkacak öğrencinin teslimi ya da sonucu varsa 409 ile bütünüyle reddedilir; eşzamanlı konu değişiminde de kaydı yeniden okuyup denemek gerekebilir. **Ödevi silmek**, öğrencilerin teslim metinlerini, ek dosyalarını ve not/sonuçlarını da kalıcı siler; yalnız bir öğrencinin kendi teslimini kaldırması farklı olan **Teslimi geri çek** işlemidir.

### 583 · PASS · Öğrenci

- Soru: öğrenci ödevin kendisini silebilir mi
- Beklenen intent: `homework_manage`
- Gerçek intent: `homework_manage`
- response_id: `homework_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 584 · PASS · Öğretmen

- Soru: yemekte öğrenciyi servis edildi işaretlemek istiyorum
- Beklenen intent: `meal_service_mark`
- Gerçek intent: `meal_service_mark`
- response_id: `meal_service_mark_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Yemekler** (`/meals`) → ilgili menü detayı (`/meals/$id`) → **Servis kaydı** sekmesine git. Öğrenci/personel satırında **Servis edildi** veya **Gelmedi** seç; rezervasyonsuz gelen biri için arama alanından hesabı seçip **Servis edildi** de. Bu kayıt Öğretmen, Yönetici ve ADMIN'e açıktır; öğrenci kendi kaydını işaretleyemez. Aynı menü+kişi için tek satır vardır, yeniden işaretlemek mevcut durumu düzeltir. Rezervasyon zorunlu değildir ve hedef mevcut herhangi bir kullanıcı olabilir; geçersiz durum veya kullanıcı 400, olmayan menü 404 verir. Servis kaydı **parayı değiştirmez**: rezerve olup gelmeyen kişi yine ücretlendirilir, rezervasyonsuz servis edilen kişiye sırf bu işaretle ücret yazılmaz. Öğretmen yalnız kaydedilmiş servis satırlarını görür; Yönetici/ADMIN rezervasyon denetimini de birleşik listede görür.

### 585 · PASS · Yönetici

- Soru: öğünde gelmedi kaydını nasıl tutarım
- Beklenen intent: `meal_service_mark`
- Gerçek intent: `meal_service_mark`
- response_id: `meal_service_mark_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Yemekler** (`/meals`) → ilgili menü detayı (`/meals/$id`) → **Servis kaydı** sekmesine git. Öğrenci/personel satırında **Servis edildi** veya **Gelmedi** seç; rezervasyonsuz gelen biri için arama alanından hesabı seçip **Servis edildi** de. Bu kayıt Öğretmen, Yönetici ve ADMIN'e açıktır; öğrenci kendi kaydını işaretleyemez. Aynı menü+kişi için tek satır vardır, yeniden işaretlemek mevcut durumu düzeltir. Rezervasyon zorunlu değildir ve hedef mevcut herhangi bir kullanıcı olabilir; geçersiz durum veya kullanıcı 400, olmayan menü 404 verir. Servis kaydı **parayı değiştirmez**: rezerve olup gelmeyen kişi yine ücretlendirilir, rezervasyonsuz servis edilen kişiye sırf bu işaretle ücret yazılmaz. Öğretmen yalnız kaydedilmiş servis satırlarını görür; Yönetici/ADMIN rezervasyon denetimini de birleşik listede görür.

### 586 · PASS · ADMIN

- Soru: rezervasyonsuz gelen kişiyi servis listesine eklemek istiyorum
- Beklenen intent: `meal_service_mark`
- Gerçek intent: `meal_service_mark`
- response_id: `meal_service_mark_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Yemekler** (`/meals`) → ilgili menü detayı (`/meals/$id`) → **Servis kaydı** sekmesine git. Öğrenci/personel satırında **Servis edildi** veya **Gelmedi** seç; rezervasyonsuz gelen biri için arama alanından hesabı seçip **Servis edildi** de. Bu kayıt Öğretmen, Yönetici ve ADMIN'e açıktır; öğrenci kendi kaydını işaretleyemez. Aynı menü+kişi için tek satır vardır, yeniden işaretlemek mevcut durumu düzeltir. Rezervasyon zorunlu değildir ve hedef mevcut herhangi bir kullanıcı olabilir; geçersiz durum veya kullanıcı 400, olmayan menü 404 verir. Servis kaydı **parayı değiştirmez**: rezerve olup gelmeyen kişi yine ücretlendirilir, rezervasyonsuz servis edilen kişiye sırf bu işaretle ücret yazılmaz. Öğretmen yalnız kaydedilmiş servis satırlarını görür; Yönetici/ADMIN rezervasyon denetimini de birleşik listede görür.

### 587 · PASS · Öğretmen

- Soru: servis kaydını yanlış girdim nasıl düzeltirim
- Beklenen intent: `meal_service_mark`
- Gerçek intent: `meal_service_mark`
- response_id: `meal_service_mark_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Yemekler** (`/meals`) → ilgili menü detayı (`/meals/$id`) → **Servis kaydı** sekmesine git. Öğrenci/personel satırında **Servis edildi** veya **Gelmedi** seç; rezervasyonsuz gelen biri için arama alanından hesabı seçip **Servis edildi** de. Bu kayıt Öğretmen, Yönetici ve ADMIN'e açıktır; öğrenci kendi kaydını işaretleyemez. Aynı menü+kişi için tek satır vardır, yeniden işaretlemek mevcut durumu düzeltir. Rezervasyon zorunlu değildir ve hedef mevcut herhangi bir kullanıcı olabilir; geçersiz durum veya kullanıcı 400, olmayan menü 404 verir. Servis kaydı **parayı değiştirmez**: rezerve olup gelmeyen kişi yine ücretlendirilir, rezervasyonsuz servis edilen kişiye sırf bu işaretle ücret yazılmaz. Öğretmen yalnız kaydedilmiş servis satırlarını görür; Yönetici/ADMIN rezervasyon denetimini de birleşik listede görür.

### 588 · PASS · Yönetici

- Soru: gelmedi işareti yemek ücretini geri verir mi
- Beklenen intent: `meal_service_mark`
- Gerçek intent: `meal_service_mark`
- response_id: `meal_service_mark_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Yemekler** (`/meals`) → ilgili menü detayı (`/meals/$id`) → **Servis kaydı** sekmesine git. Öğrenci/personel satırında **Servis edildi** veya **Gelmedi** seç; rezervasyonsuz gelen biri için arama alanından hesabı seçip **Servis edildi** de. Bu kayıt Öğretmen, Yönetici ve ADMIN'e açıktır; öğrenci kendi kaydını işaretleyemez. Aynı menü+kişi için tek satır vardır, yeniden işaretlemek mevcut durumu düzeltir. Rezervasyon zorunlu değildir ve hedef mevcut herhangi bir kullanıcı olabilir; geçersiz durum veya kullanıcı 400, olmayan menü 404 verir. Servis kaydı **parayı değiştirmez**: rezerve olup gelmeyen kişi yine ücretlendirilir, rezervasyonsuz servis edilen kişiye sırf bu işaretle ücret yazılmaz. Öğretmen yalnız kaydedilmiş servis satırlarını görür; Yönetici/ADMIN rezervasyon denetimini de birleşik listede görür.

### 589 · PASS · Öğrenci

- Soru: öğrenci kendi yemek yoklamasını işaretleyebilir mi
- Beklenen intent: `meal_service_mark`
- Gerçek intent: `meal_service_mark`
- response_id: `meal_service_mark_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 590 · PASS · Yönetici

- Soru: öğrencinin beslenme profilini güncellemek istiyorum
- Beklenen intent: `meal_dietary_profile_manage`
- Gerçek intent: `meal_dietary_profile_manage`
- response_id: `meal_dietary_profile_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Öğrencinin okul tarafından tutulan beslenme kaydını değiştirmek için **Yemekler** (`/meals`) → bir menü detayı → **Yönet** → **Öğrenci kaydı** bölümünde öğrenciyi seç. Okul ayarlarındaki sözlükten alerji/beslenme etiketlerini işaretle, gerekirse en fazla 500 karakterlik **Mutfak notu** yaz ve **Kaydet**. Bu güvenlik kaydına yalnız Yönetici ve ADMIN yazabilir; Öğretmen okuyabilir, Öğrenci kendi ve Veli bağlı çocuğunun profilini görebilir fakat hiçbiri değiştiremez. Etiket listesi en fazla 10 öğedir ve tamamı okulun `dietary_tags` sözlüğünde bulunmalıdır; bilinmeyen/fazla etiket, uzun not veya öğrenci olmayan hedef 400, olmayan kullanıcı 404 verir. Boş etiket listesi 'bilinen kısıt yok' demektir; boş/null mutfak notu mevcut notu temizler. Menüdeki çakışma uyarıları bu profil ile yemek etiketlerinin kesişiminden hesaplanır.

### 591 · PASS · ADMIN

- Soru: alerji etiketini öğrenciye nasıl eklerim
- Beklenen intent: `meal_dietary_profile_manage`
- Gerçek intent: `meal_dietary_profile_manage`
- response_id: `meal_dietary_profile_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Öğrencinin okul tarafından tutulan beslenme kaydını değiştirmek için **Yemekler** (`/meals`) → bir menü detayı → **Yönet** → **Öğrenci kaydı** bölümünde öğrenciyi seç. Okul ayarlarındaki sözlükten alerji/beslenme etiketlerini işaretle, gerekirse en fazla 500 karakterlik **Mutfak notu** yaz ve **Kaydet**. Bu güvenlik kaydına yalnız Yönetici ve ADMIN yazabilir; Öğretmen okuyabilir, Öğrenci kendi ve Veli bağlı çocuğunun profilini görebilir fakat hiçbiri değiştiremez. Etiket listesi en fazla 10 öğedir ve tamamı okulun `dietary_tags` sözlüğünde bulunmalıdır; bilinmeyen/fazla etiket, uzun not veya öğrenci olmayan hedef 400, olmayan kullanıcı 404 verir. Boş etiket listesi 'bilinen kısıt yok' demektir; boş/null mutfak notu mevcut notu temizler. Menüdeki çakışma uyarıları bu profil ile yemek etiketlerinin kesişiminden hesaplanır.

### 592 · PASS · Yönetici

- Soru: mutfak notunu temizlemem gerekiyor
- Beklenen intent: `meal_dietary_profile_manage`
- Gerçek intent: `meal_dietary_profile_manage`
- response_id: `meal_dietary_profile_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Öğrencinin okul tarafından tutulan beslenme kaydını değiştirmek için **Yemekler** (`/meals`) → bir menü detayı → **Yönet** → **Öğrenci kaydı** bölümünde öğrenciyi seç. Okul ayarlarındaki sözlükten alerji/beslenme etiketlerini işaretle, gerekirse en fazla 500 karakterlik **Mutfak notu** yaz ve **Kaydet**. Bu güvenlik kaydına yalnız Yönetici ve ADMIN yazabilir; Öğretmen okuyabilir, Öğrenci kendi ve Veli bağlı çocuğunun profilini görebilir fakat hiçbiri değiştiremez. Etiket listesi en fazla 10 öğedir ve tamamı okulun `dietary_tags` sözlüğünde bulunmalıdır; bilinmeyen/fazla etiket, uzun not veya öğrenci olmayan hedef 400, olmayan kullanıcı 404 verir. Boş etiket listesi 'bilinen kısıt yok' demektir; boş/null mutfak notu mevcut notu temizler. Menüdeki çakışma uyarıları bu profil ile yemek etiketlerinin kesişiminden hesaplanır.

### 593 · PASS · Öğretmen

- Soru: öğretmen beslenme profilini değiştirebilir mi
- Beklenen intent: `meal_dietary_profile_manage`
- Gerçek intent: `meal_dietary_profile_manage`
- response_id: `meal_dietary_profile_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 594 · PASS · ADMIN

- Soru: bilinmeyen dietary tag hatası alıyorum
- Beklenen intent: `meal_dietary_profile_manage`
- Gerçek intent: `meal_dietary_profile_manage`
- response_id: `meal_dietary_profile_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Yemekler", "route": "/meals"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> Öğrencinin okul tarafından tutulan beslenme kaydını değiştirmek için **Yemekler** (`/meals`) → bir menü detayı → **Yönet** → **Öğrenci kaydı** bölümünde öğrenciyi seç. Okul ayarlarındaki sözlükten alerji/beslenme etiketlerini işaretle, gerekirse en fazla 500 karakterlik **Mutfak notu** yaz ve **Kaydet**. Bu güvenlik kaydına yalnız Yönetici ve ADMIN yazabilir; Öğretmen okuyabilir, Öğrenci kendi ve Veli bağlı çocuğunun profilini görebilir fakat hiçbiri değiştiremez. Etiket listesi en fazla 10 öğedir ve tamamı okulun `dietary_tags` sözlüğünde bulunmalıdır; bilinmeyen/fazla etiket, uzun not veya öğrenci olmayan hedef 400, olmayan kullanıcı 404 verir. Boş etiket listesi 'bilinen kısıt yok' demektir; boş/null mutfak notu mevcut notu temizler. Menüdeki çakışma uyarıları bu profil ile yemek etiketlerinin kesişiminden hesaplanır.

### 595 · PASS · Öğrenci

- Soru: öğrenci kendi alerji kaydını düzenleyebilir mi
- Beklenen intent: `meal_dietary_profile_manage`
- Gerçek intent: `meal_dietary_profile_manage`
- response_id: `meal_dietary_profile_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.

### 596 · PASS · Öğretmen

- Soru: soru bankasına yeni bir şablon eklemek istiyorum
- Beklenen intent: `question_bank_manage`
- Gerçek intent: `question_bank_manage`
- response_id: `question_bank_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru bankası", "route": "/question-bank"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Soru bankası** (`/question-bank`) Öğretmen+ içindir. **Soru oluştur** ile yönetebildiğin dersi ve o dersin konusunu seç; soru türü, metin, puan, seçenek/doğru cevap ve isteğe bağlı görselleri kaydet. Yeni şablon daima **Yalnız ben** (private) doğar; **Okulla paylaşılan** görünürlüğüne geçişte onay istenir. Paylaşımı sonradan private'a alsan bile daha önce sınavlara kopyalanmış sorular geri silinmez. Listeyi sahip, konu, görünürlük ve metinle süzebilirsin. Öğretmen ve Yönetici kendi şablonunu düzenleyip siler; ADMIN okul kapsamındaki bütün şablonları yönetebilir. Başka bir öğretmenin private şablonu 404 ile gizlenir; okulla paylaşılan şablonu görebilsen de sahibi/ADMIN değilsen değiştirme 403'tür. Konu köken bilgisidir: silinirse şablonda boşalır; şablonu sınava eklerken hedef sınavın dersinden bir konu seçmek gerekir. Şablonu silmek, ondan daha önce üretilmiş bağımsız sınav sorularını silmez. Eşzamanlı güncelleme sürekli çakışırsa 409 ile yeniden okuma/deneme istenir.

### 597 · PASS · Yönetici

- Soru: bankadaki kendi sorumu düzenlemem lazım
- Beklenen intent: `question_bank_manage`
- Gerçek intent: `question_bank_manage`
- response_id: `question_bank_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru bankası", "route": "/question-bank"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Soru bankası** (`/question-bank`) Öğretmen+ içindir. **Soru oluştur** ile yönetebildiğin dersi ve o dersin konusunu seç; soru türü, metin, puan, seçenek/doğru cevap ve isteğe bağlı görselleri kaydet. Yeni şablon daima **Yalnız ben** (private) doğar; **Okulla paylaşılan** görünürlüğüne geçişte onay istenir. Paylaşımı sonradan private'a alsan bile daha önce sınavlara kopyalanmış sorular geri silinmez. Listeyi sahip, konu, görünürlük ve metinle süzebilirsin. Öğretmen ve Yönetici kendi şablonunu düzenleyip siler; ADMIN okul kapsamındaki bütün şablonları yönetebilir. Başka bir öğretmenin private şablonu 404 ile gizlenir; okulla paylaşılan şablonu görebilsen de sahibi/ADMIN değilsen değiştirme 403'tür. Konu köken bilgisidir: silinirse şablonda boşalır; şablonu sınava eklerken hedef sınavın dersinden bir konu seçmek gerekir. Şablonu silmek, ondan daha önce üretilmiş bağımsız sınav sorularını silmez. Eşzamanlı güncelleme sürekli çakışırsa 409 ile yeniden okuma/deneme istenir.

### 598 · PASS · Öğretmen

- Soru: soru bankasındaki şablonu okul görünürlüğüne açmak istiyorum
- Beklenen intent: `question_bank_manage`
- Gerçek intent: `question_bank_manage`
- response_id: `question_bank_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru bankası", "route": "/question-bank"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Soru bankası** (`/question-bank`) Öğretmen+ içindir. **Soru oluştur** ile yönetebildiğin dersi ve o dersin konusunu seç; soru türü, metin, puan, seçenek/doğru cevap ve isteğe bağlı görselleri kaydet. Yeni şablon daima **Yalnız ben** (private) doğar; **Okulla paylaşılan** görünürlüğüne geçişte onay istenir. Paylaşımı sonradan private'a alsan bile daha önce sınavlara kopyalanmış sorular geri silinmez. Listeyi sahip, konu, görünürlük ve metinle süzebilirsin. Öğretmen ve Yönetici kendi şablonunu düzenleyip siler; ADMIN okul kapsamındaki bütün şablonları yönetebilir. Başka bir öğretmenin private şablonu 404 ile gizlenir; okulla paylaşılan şablonu görebilsen de sahibi/ADMIN değilsen değiştirme 403'tür. Konu köken bilgisidir: silinirse şablonda boşalır; şablonu sınava eklerken hedef sınavın dersinden bir konu seçmek gerekir. Şablonu silmek, ondan daha önce üretilmiş bağımsız sınav sorularını silmez. Eşzamanlı güncelleme sürekli çakışırsa 409 ile yeniden okuma/deneme istenir.

### 599 · PASS · Yönetici

- Soru: başka öğretmenin banka sorusunu silebilir miyim
- Beklenen intent: `question_bank_manage`
- Gerçek intent: `question_bank_manage`
- response_id: `question_bank_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru bankası", "route": "/question-bank"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Soru bankası** (`/question-bank`) Öğretmen+ içindir. **Soru oluştur** ile yönetebildiğin dersi ve o dersin konusunu seç; soru türü, metin, puan, seçenek/doğru cevap ve isteğe bağlı görselleri kaydet. Yeni şablon daima **Yalnız ben** (private) doğar; **Okulla paylaşılan** görünürlüğüne geçişte onay istenir. Paylaşımı sonradan private'a alsan bile daha önce sınavlara kopyalanmış sorular geri silinmez. Listeyi sahip, konu, görünürlük ve metinle süzebilirsin. Öğretmen ve Yönetici kendi şablonunu düzenleyip siler; ADMIN okul kapsamındaki bütün şablonları yönetebilir. Başka bir öğretmenin private şablonu 404 ile gizlenir; okulla paylaşılan şablonu görebilsen de sahibi/ADMIN değilsen değiştirme 403'tür. Konu köken bilgisidir: silinirse şablonda boşalır; şablonu sınava eklerken hedef sınavın dersinden bir konu seçmek gerekir. Şablonu silmek, ondan daha önce üretilmiş bağımsız sınav sorularını silmez. Eşzamanlı güncelleme sürekli çakışırsa 409 ile yeniden okuma/deneme istenir.

### 600 · PASS · ADMIN

- Soru: şablonun konusu silinirse ne olur
- Beklenen intent: `question_bank_manage`
- Gerçek intent: `question_bank_manage`
- response_id: `question_bank_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `None`
- navigation: `{"available": true, "label": "Soru bankası", "route": "/question-bank"}`
- assistant outcome/reason: `allow` / `allowed`
- Sözleşme: `PASS`

> **Soru bankası** (`/question-bank`) Öğretmen+ içindir. **Soru oluştur** ile yönetebildiğin dersi ve o dersin konusunu seç; soru türü, metin, puan, seçenek/doğru cevap ve isteğe bağlı görselleri kaydet. Yeni şablon daima **Yalnız ben** (private) doğar; **Okulla paylaşılan** görünürlüğüne geçişte onay istenir. Paylaşımı sonradan private'a alsan bile daha önce sınavlara kopyalanmış sorular geri silinmez. Listeyi sahip, konu, görünürlük ve metinle süzebilirsin. Öğretmen ve Yönetici kendi şablonunu düzenleyip siler; ADMIN okul kapsamındaki bütün şablonları yönetebilir. Başka bir öğretmenin private şablonu 404 ile gizlenir; okulla paylaşılan şablonu görebilsen de sahibi/ADMIN değilsen değiştirme 403'tür. Konu köken bilgisidir: silinirse şablonda boşalır; şablonu sınava eklerken hedef sınavın dersinden bir konu seçmek gerekir. Şablonu silmek, ondan daha önce üretilmiş bağımsız sınav sorularını silmez. Eşzamanlı güncelleme sürekli çakışırsa 409 ile yeniden okuma/deneme istenir.

### 601 · PASS · Öğrenci

- Soru: banka sorusunu silince sınavdaki kopyası da silinir mi
- Beklenen intent: `question_bank_manage`
- Gerçek intent: `question_bank_manage`
- response_id: `question_bank_manage_instructions`
- confidence: `1.0000`
- fallback: `false`
- auth_action: `role_insufficient`
- navigation: `None`
- assistant outcome/reason: `deny` / `role_not_permitted`
- Sözleşme: `PASS`

> Bu işlem rolünün kapsamı dışında görünüyor 🙂 O yüzden adımları ve yönlendirmeyi paylaşmıyorum. Yetkin dahilindeki bir konuda yardımcı olayım.
