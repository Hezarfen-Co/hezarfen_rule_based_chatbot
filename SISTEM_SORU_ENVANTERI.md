# Hezarfen Sistem Soru Envanteri

Bu belge, Hezarfen arayüzünde gerçekten bulunan sayfa ve işlemleri chatbot benchmarkına dönüştürmek için hazırlanmış inceleme envanteridir. Kaynak kodun 24 Ağustos 2026 tarihli çalışma ağacı esas alınmıştır. Frontend ve backend yalnız salt-okunur kaynak olarak incelenmiş; uygulama değişiklikleri yalnız `Hezarfen-Rule-Based-Chatbot` reposunda yapılmıştır.

## Bu turda kapatılan yüksek öncelikli boşluklar

- `/profile/me`, hesap menüsündeki kişisel Ayarlar penceresi ve okul Ayarları birbirinden ayrıldı.
- `class_section_manage`, şube/sınıf grubu CRUD'u ile öğrenci/ders bağlantılarını ders CRUD'undan ayırdı.
- `upload_problem`, 400/413, boş/bozuk multipart, 10 dosya tavanı ve görsel türlerini kapsıyor.
- `chatbot_service_problem`, bridge disabled/disconnected, 429, pending/failure ve thread tavanını kapsıyor.
- Sınav zamanlama, notlandırılmış ödev kilidi, randevu durumları, append-only ödeme düzeltmesi, yemek rezervasyonu ve beyaz tahta durumları mevcut yanıtlara işlendi.
- Defter içe aktarma/OCR/ek, ders konusu/notu/öğretmeni, ödev yönetimi/teslim geri çekme, soru bankası CRUD, şube CRUD ve yemek servis/diyet akışları özel intentlerle kapatıldı.
- Katalog **98 intent** içeriyor. Elle etiketli gold küme **601 soru ve 601/601 PASS**; `stress-v3.5.0` koşusu 9.000 uygulama-içi + 1.000 OOS vakada **9.984 PASS / 16 FAIL (%99,84)** verdi (4 soft, 12 hard).

Tablolardaki **Kısmi/Eksik/Çelişki** değerleri kaynak taraması anındaki boşlukları gösterir; yukarıdaki maddeler uygulama sonrasındaki farkı kaydeder.
Tablodaki `CB src/catalog.py:<satır>` numaraları da bu ilk tarama anının kanıtıdır;
sonraki intent eklemeleri satırları kaydırdığı için güncel kodda intent adını aramak
satır numarasından daha güvenilirdir. Frontend/backend kanıt satırları salt-okunur
kaynak snapshotına aittir.

## Nasıl okunmalı?

Rol kısaltmaları:

- V: Veli
- Ö: Öğrenci
- T: Öğretmen
- Y: Yönetici
- A: ADMIN
- Z: Oturum açmamış ziyaretçi

Chatbot kapsamı:

- **Tam:** Sayfanın ana kullanıcı akışı, doğru rol ve doğru yönlendirme mevcut intent ile anlatılıyor.
- **Kısmi:** Sayfa tanınıyor ancak görünür işlemlerden veya önemli hata durumlarından en az biri ayrı bir soru olarak karşılanmıyor.
- **Eksik:** Sayfa/işlem için güvenilir, özel bir intent yok.
- **Çelişki:** Chatbot metni, intent metadatası, frontend veya backend arasında doğrulanmış bir uyuşmazlık var.

Bu sınıflandırma “sayfa için herhangi bir cevap var mı?” değil, kullanıcının görünür düğme ve hata metinleri hakkında sorabileceği gerçek soru yüzeyini ölçer.

## Yetkiyi doğru yorumlama

Frontend rol sırası V < Ö < T < Y < A olarak tanımlanır; fakat ürün saf bir hiyerarşi değildir. Exact role, max role ve kaynak sahipliği kontrolleri vardır. Frontend route guard oturum, minimum/maksimum/tam rol kontrolü yapar; oturumsuz kullanıcıyı /login sayfasına gönderir, rol uyuşmazlığında sayfa içinde “Bu içeriğe erişimin yok.” uyarısı gösterir. Kanıt: ../hezarfen_frontend/src/lib/roles.ts:3-9 ve ../hezarfen_frontend/src/components/layout/route-guard.tsx:12-49.

Frontend’de bir route’un açılması, backend işleminin yetkili olduğu anlamına gelmez. Backend’in temel extractor seviyeleri ../hezarfen_backend/src/web/extractor.rs:81-82,101-102,121-122,141-142 satırlarında; kaynak kapsamı kontrolleri ise ilgili endpointlerde uygulanır. Örneğin Pomodoro yalnız tam Öğrenci rolüdür, sınav odası yalnız kayıtlı Öğrencidir, /work yalnız Öğretmen ve Yönetici içindir, yemek kredisi yalnız ADMIN tarafından yazılır. Bu nedenle benchmarkta yalnız frontend route guard’a bakılarak “üst rol de yapar” beklentisi üretilmemelidir.

## 48 route ve soru yüzeyi

### Route 1-24

| # | Route | Rol ve gerçek erişim | Görünür özellikler ve olası soru aileleri | Hata / boş / doğrulama yüzeyi | Chatbot kapsamı | Kanıt |
|---:|---|---|---|---|---|---|
| 1 | **/** | V/Ö/T/Y/A | Role özel özet, yaklaşan sınav/ödev/etkinlik, istatistik ve grafikler. “Bugün ne var?”, “Ana panelde ne görüyorum?” | Yükleniyor, role göre boş kartlar ve veri hatası | **Kısmi:** today_info yalnız genel özeti anlatıyor; role özel kart ve istatistik soruları eksik | FE ../hezarfen_frontend/src/routes/router.tsx:93-97; ../hezarfen_frontend/src/pages/dashboard-page.tsx:95-96,439-535. CB src/catalog.py:1681-1696 |
| 2 | **/login** | Yalnız Z; giriş yapan kullanıcı GuestGuard ile ana sayfaya gider | Kullanıcı adı/şifre ile giriş, kayıt sayfasına geçiş, erişim sorunu. “Nasıl giriş yaparım?”, “Şifremi unuttum” | Zorunlu kullanıcı adı/şifre, başarısız kimlik doğrulama, bekleyen gönderim | **Tam:** login_how ve account_access_problem ana akışı ayırıyor | FE ../hezarfen_frontend/src/routes/router.tsx:99-103; ../hezarfen_frontend/src/pages/login-page.tsx:14-18,39-43,63-123; ../hezarfen_frontend/src/components/layout/guest-guard.tsx:6-13. CB src/catalog.py:251-271,344-364 |
| 3 | **/register** | Yalnız Z | Hesap oluşturma, girişe dönme. “Nasıl kayıt olurum?”, “Şifreler neden uyuşmuyor?” | Kullanıcı adı/şifre zorunlu, şifre tekrarı uyuşmazlığı, sunucu hatası | **Tam:** register_how doğru route ve temel alanları kapsıyor | FE ../hezarfen_frontend/src/routes/router.tsx:105-109; ../hezarfen_frontend/src/pages/register-page.tsx:13-17,39-47,66-140. CB src/catalog.py:274-296 |
| 4 | **/notes** | V/Ö/T/Y/A; kişisel kayıt | Yeni not, düzenle, sil, dosyadan içe aktar, OCR, ek ve çizim. “Not al”, “Ben not silmek”, “PDF’den nota aktar” | “Henüz not yok”; başlık zorunlu ve en çok 200, içerik en çok 10.000; en çok 10 dosya; OCR/format ve kısmi yükleme hataları | **Tam:** note_create/edit/delete yanında note_import_ocr ve note_file_manage içe aktarma, OCR, ek ve çizimi ayırıyor | FE ../hezarfen_frontend/src/routes/router.tsx:111-115; ../hezarfen_frontend/src/pages/notes-page.tsx:27-31,78-170; ../hezarfen_frontend/src/components/notes/note-form.tsx:59-73; ../hezarfen_frontend/src/components/notes/note-import-panel.tsx:37,63. CB src/catalog.py:1236-1307 |
| 5 | **/events** | V/Ö/T/Y/A görüntüleme; T+ oluşturma | Liste, filtre, detay açma ve etkinlik oluşturma. “Etkinlikler nerede?”, “Etkinlik oluşturacağım” | “Etkinlik bulunamadı”, yükleme/yeniden dene, tarih aralığı hataları | **Kısmi:** event_view ve event_create var; filtre, düzenleme, silme ve kayıt türü soruları eksik | FE ../hezarfen_frontend/src/routes/router.tsx:117-121; ../hezarfen_frontend/src/pages/events-page.tsx:29-33,53,193-212. BE ../hezarfen_backend/src/web/events.rs:275-279,365-389,460-475. CB src/catalog.py:1213-1233,1770-1785 |
| 6 | **/events/$id** | V/Ö/T/Y/A görüntüler; oluşturucu veya Y+ yönetir; T+ roster/yoklama | Detay, düzenle/sil, katılımcı listesi, öğrenci ekle/çıkar, yoklama işaretle. “Öğrenciyi etkinliğe ekle”, “Katılımını işaretle” | Öğrenci seçilmeden işlem uyarısı; roster/yoklama boş; hedef kitle dışında 400/403/404 | **Kısmi:** event_attendance_mark doğru biçimde T+; edit/delete ve kayıt/çıkarma için özel intent yok | FE ../hezarfen_frontend/src/routes/router.tsx:123-127; ../hezarfen_frontend/src/pages/event-detail-page.tsx:49-53,79-95,169-195,271-360. BE ../hezarfen_backend/src/web/events.rs:481-505,544-565,743-746,818-821. CB src/catalog.py:1168-1188 |
| 7 | **/exams** | V/Ö/T/Y/A route; yönetilebilir sınavlarda T+ işlem | Sınav listesi, takvim, oluşturma, yayınlama, düzenleme. “Sınav ne zaman?”, “Sınav oluştur/yayınla” | “Sınav bulunamadı”, zaman/tür/süre ve yayınlama hataları | **Kısmi:** exam_schedule_info, exam_modes_info ve exam_create var; yayınla/düzenle/sil ayrı değil | FE ../hezarfen_frontend/src/routes/router.tsx:129-133; ../hezarfen_frontend/src/pages/exams-page.tsx:39-43,81-88,185-208,273-293. BE ../hezarfen_backend/src/web/exams/mod.rs:586-587,669-670. CB src/catalog.py:730-773,1788-1803 |
| 8 | **/homework** | V/Ö/T/Y/A route; Ö kendi ödevini, T+ yönettiği dersi görür/yönetir | Ödevlerim, filtre, detay, ödev oluşturma. “Ödevlerim nerede?”, “Ödev ver” | “Ödev bulunamadı”; teslim tarihi geçmiş/başlangıçtan önce; ders yönetimi yoksa 403 | **Kısmi:** homework_view, homework_assign ve homework_manage görüntüleme/oluşturma/edit/silmeyi kapsıyor; ayrıntılı liste filtreleri tek intent altında | FE ../hezarfen_frontend/src/routes/router.tsx:135-139; ../hezarfen_frontend/src/pages/homework-page.tsx:42-46,78-93,118-121,230-250. BE ../hezarfen_backend/src/web/homework.rs:503-508,1119-1120. CB src/catalog.py:948-1014 |
| 9 | **/homework/$id** | V/Ö/T/Y/A route; yalnız Ö teslim; ders yöneticisi notlandırır | Metin/dosya teslimi, teslimi geri çekme, not verme, dosya görüntüleme. “Ödevi yükle”, “Teslimi geri al”, “Puan ver” | Notlandıktan sonra geri çekilemez; dosya ve teslim hataları; boş/henüz teslim yok | **Tam:** homework_submit, homework_withdraw_submission ve homework_grade temel teslim yaşam döngüsünü ve notlandırma kilidini ayırıyor | FE ../hezarfen_frontend/src/routes/router.tsx:141-145; ../hezarfen_frontend/src/pages/homework-detail-page.tsx:33-42,50-88; ../hezarfen_frontend/src/i18n/messages.ts:2653-2659. BE ../hezarfen_backend/src/web/homework.rs:503-508,1217-1218. CB src/catalog.py:971-1037 |
| 10 | **/exams/$id** | V/Ö/T/Y/A route; Ö kayıtlı sınava girer; oluşturucu/Y+ yönetir | Detay, sınava gir/devam et, soru ekle, canlı izle, sonuç/cevap kâğıdı, notlandır, edit/delete | Sınav başlamadı/bitti, kayıt yok, deneme hakkı, boş sonuç; seçili öğrenci yok; 403/404 | **Kısmi:** giriş, yeniden katılma, soru ekleme, bitirme/sonuç, notlandırma ve canlı izleme var; yayın/edit/delete/cevap inceleme görselleri eksik | FE ../hezarfen_frontend/src/routes/router.tsx:147-151; ../hezarfen_frontend/src/pages/exam-detail-page.tsx:101-107,230-242,394-445,723-760. BE ../hezarfen_backend/src/web/exams/attempts.rs:713-744. CB src/catalog.py:752-944 |
| 11 | **/exam-room/$id** | Tam Ö ve sınava kayıtlı | Sınava başla, cevabı kaydet, bağlantı sonrası devam et, bitir. “Cevabım kaydoldu mu?”, “Sınava geri dönebilir miyim?” | Oda yükleniyor; yetkisiz/kayıtsız; süre/deneme hakkı; kayıt ve gönderim hatası | **Tam:** exam_enter_room, exam_save_answer, exam_finish_result, exam_rejoin_retake ana yaşam döngüsünü kapsıyor | FE ../hezarfen_frontend/src/routes/router.tsx:153-157; ../hezarfen_frontend/src/pages/exam-room-page.tsx:16-20,35-45,59-80. BE ../hezarfen_backend/src/web/exams/attempts.rs:713-744. CB src/catalog.py:802-893 |
| 12 | **/question-bank** | T/Y/A | Soru şablonu listele/filtrele/oluştur; sahibi veya A düzenler | “Soru bulunamadı”, form doğrulaması, sahiplik 403 | **Tam:** question_bank_info kavramı; question_bank_manage oluşturma, düzenleme, silme, görünürlük ve kopya davranışını anlatıyor | FE ../hezarfen_frontend/src/routes/router.tsx:159-163; ../hezarfen_frontend/src/pages/question-bank-page.tsx:27-31,90-105,206-228. BE ../hezarfen_backend/src/web/bank_questions.rs:357-376. CB src/catalog.py:1699-1714 |
| 13 | **/question-bank/$id** | T/Y/A; sahibi veya A düzenler/siler | Şablon detayı, düzenle, sil, görsel yükle/kaldır. “Soru şablonunu değiştir”, “Görsel ekle” | Bulunamadı/gizli 404; sahiplik 403; görsel yükleme hatası | **Kısmi:** question_bank_manage detay CRUD ve sahiplik/görünürlüğü kapsıyor; görsel yaşam döngüsü ayrı intent değil | FE ../hezarfen_frontend/src/routes/router.tsx:165-169; ../hezarfen_frontend/src/pages/bank-question-detail-page.tsx:27-31,48-61,95-116. BE ../hezarfen_backend/src/web/bank_questions.rs:357-376. CB src/catalog.py:1699-1714 |
| 14 | **/courses** | V/Ö/T/Y/A route; backend kayıt/yönetim kapsamı uygular | Ders/etüt/kulüp sekmeleri, filtre, detay, T+ oluştur, Y+ öğretmen ata. “Derslerim”, “Etütler nerede?”, “Ders oluştur” | “Ders bulunamadı”, filtre sonucu boş, yönetim kapsamı 403 | **Kısmi:** course_view, course_create ve study_club_info var; öğretmen atama ve tür bazlı yönetim eksik | FE ../hezarfen_frontend/src/routes/router.tsx:171-179; ../hezarfen_frontend/src/pages/courses-page.tsx:34-51,75-80,127-223. BE ../hezarfen_backend/src/web/courses.rs:199-225. CB src/catalog.py:586-629,1539-1561 |
| 15 | **/studies** | Kimlik doğrulandıktan sonra /courses?kind=study yönlendirmesi; ayrı sayfa değil | “Etüt sayfası nerede?”, “Etüde kendim kaydolabilir miyim?” | Ders listesinin boş/hata durumu devralınır | **Tam:** study_club_info bunun ayrı menü olmadığını ve filtreye yönlendiğini doğru anlatıyor | FE ../hezarfen_frontend/src/routes/router.tsx:181-187; ../hezarfen_frontend/src/pages/courses-page.tsx:161-223. CB src/catalog.py:1539-1550,2192 |
| 16 | **/clubs** | Kimlik doğrulandıktan sonra /courses?kind=club yönlendirmesi; ayrı sayfa değil | “Kulüpler nerede?”, “Kulübe nasıl katılırım?” | Ders listesinin boş/hata durumu devralınır | **Tam:** study_club_info filtre ve roster modelini doğru anlatıyor | FE ../hezarfen_frontend/src/routes/router.tsx:189-195; ../hezarfen_frontend/src/pages/courses-page.tsx:161-223. CB src/catalog.py:1539-1550 |
| 17 | **/courses/$id** | V/Ö/T/Y/A route; backend üyelik/yönetim kapsamı | Konular, materyaller, sınavlar, ödevler, oturumlar, ders notları, öğretmenler, roster; öğrenci ekle/çıkar; yoklama | Üye/yönetici değil 403/404; boş materyal/roster; kapasite ve tarih hataları | **Tam:** kayıt/çıkarma, oturum, yoklama ve materyal yanında course_subject_manage, course_note_manage ve course_teacher_manage ayrıntılı yönetim akışlarını kapsıyor | FE ../hezarfen_frontend/src/routes/router.tsx:197-201; ../hezarfen_frontend/src/pages/course-detail-page.tsx:57,82-144,302-328,604-683. BE ../hezarfen_backend/src/web/courses.rs:708-709,725,766-767; ../hezarfen_backend/src/web/course_notes.rs:129-130,173-174. CB src/catalog.py:632-729,1806-1821 |
| 18 | **/marks** | Tam Ö | Karnem ve devam durumu sekmeleri, ağırlıklı ortalama. “Notlarım”, “Devamsızlığım”, “Ortalama nasıl hesaplanır?” | “Henüz not yok”, dönem/ders verisi yok, yükleme hatası | **Tam:** report_card_view, weighted_average_info, attendance_view ve attendance_rate_info sayfanın ana sorularını kapsıyor | FE ../hezarfen_frontend/src/routes/router.tsx:203-210; ../hezarfen_frontend/src/pages/marks-page.tsx:16-20,35-71. CB src/catalog.py:1040-1165 |
| 19 | **/messages** | V/Ö/T/Y/A; kişisel posta kutusu | Yeni mesaj, gelen/gönderilen, yanıtla, arşivle, çöp, geri yükle, kalıcı sil, çöpü boşalt | “Mesaj yok”, alıcı/konu/metin doğrulaması, gönderim ve yenileme hatası | **Kısmi:** messages_use gönderme/okuma/arşiv/çöpü anlatıyor; yanıt, geri yükleme, kalıcı silme ve boşaltma ayrı sorgu olarak zayıf | FE ../hezarfen_frontend/src/routes/router.tsx:212-216; ../hezarfen_frontend/src/pages/messages-page.tsx:164-444. CB src/catalog.py:1515-1536 |
| 20 | **/pomodoro** | Tam Ö; T/Y/A kullanamaz | Odağı başlat/bitir, özel süre, toplam odak ve geçmiş. “Pomodoro başlat”, “Açık oturumu nasıl kapatırım?” | Aynı anda tek açık kayıt; açık değilken bitirme; “Henüz oturum yok” | **Tam:** pomodoro_use exact-role ve sunucu zamanı davranışını doğru açıklar | FE ../hezarfen_frontend/src/routes/router.tsx:218-222; ../hezarfen_frontend/src/pages/pomodoro-page.tsx:36-40,153-298. BE ../hezarfen_backend/src/web/pomodoro.rs:29-31,138,225. CB src/catalog.py:1467-1491; src/role_spaces.py:81-84 |
| 21 | **/management/student-marks** | T/Y/A | Öğrenci ara, not raporunu görüntüle. “Öğrencinin notlarına bak” | En az arama karakteri, öğrenci seçilmedi, sonuç yok, 403 | **Tam:** student_marks_lookup doğru yönetim route’unu ve rolü verir | FE ../hezarfen_frontend/src/routes/router.tsx:224-228; ../hezarfen_frontend/src/pages/student-marks-page.tsx:25-29,38-91,157-205. CB src/catalog.py:1100-1119 |
| 22 | **/management/pomodoros** | T/Y/A | Öğrenci ara, odak geçmişi ve toplam süre. “Öğrenci pomodoroları nerede?” | Arama/öğrenci seçimi, sonuç yok, yükleme hatası | **Tam:** student_pomodoro_lookup doğru ayrımı yapıyor | FE ../hezarfen_frontend/src/routes/router.tsx:230-234; ../hezarfen_frontend/src/pages/student-pomodoro-page.tsx:20-24,34-62,119-170. CB src/catalog.py:1494-1512 |
| 23 | **/attendance** | Tam Ö; /marks?tab=attendance yönlendirmesi | “Devamsızlığıma nereden bakarım?”, “Devam oranı nasıl?” | /marks boş/hata durumları devralınır | **Tam:** attendance_view ve attendance_rate_info mevcut | FE ../hezarfen_frontend/src/routes/router.tsx:236-242; ../hezarfen_frontend/src/pages/marks-page.tsx:18,40-71. CB src/catalog.py:1122-1165 |
| 24 | **/management/student-attendance** | T/Y/A | Öğrenci ara, devam/yoklama raporu. “Öğrencinin devamsızlığına bak” | Arama/öğrenci seçimi, sonuç yok, 403 | **Tam:** student_attendance_lookup doğru route ve rolü verir | FE ../hezarfen_frontend/src/routes/router.tsx:244-248; ../hezarfen_frontend/src/pages/student-attendance-page.tsx:20-24,33-61,101-149. CB src/catalog.py:1192-1210 |

### Route 25-48

| # | Route | Rol ve gerçek erişim | Görünür özellikler ve olası soru aileleri | Hata / boş / doğrulama yüzeyi | Chatbot kapsamı | Kanıt |
|---:|---|---|---|---|---|---|
| 25 | **/work** | Yalnız T/Y; A özellikle hariç | Kendi mesai giriş/çıkışı ve son kayıtlar. “Mesaiye giriş yap”, “Çıkışı unuttum” | Zaten açık mesai 409; açık kayıt yokken çıkış; “Kayıt yok” | **Tam:** work_checkin_out exact kapsamı ve iki temel hatayı anlatıyor | FE ../hezarfen_frontend/src/routes/router.tsx:250-254; ../hezarfen_frontend/src/pages/work-log-page.tsx:23-27,79-140. BE ../hezarfen_backend/src/web/work.rs:79-126. CB src/catalog.py:1311-1335 |
| 26 | **/management/staff-work** | Y/A | Personel ara, kapalı kaydı düzelt, sil, süreleri görüntüle. “Mesaiyi düzelt/sil” | Açık mesai düzenlenemez; giriş/çıkış zorunlu; çıkış girişten önce olamaz; sonuç yok | **Kısmi:** staff_work_manage görüntüleme/düzeltmeyi ve validasyonu kapsıyor; silme akışı zayıf | FE ../hezarfen_frontend/src/routes/router.tsx:256-260; ../hezarfen_frontend/src/pages/staff-work-page.tsx:59-63,201-224,251-350. BE ../hezarfen_backend/src/web/work.rs:154-232. CB src/catalog.py:1338-1361 |
| 27 | **/management/settings** | Y/A | Değerlendirme, not bantları, yoklama durumları; Yemekhane slot/etiket; Sistem dosya limiti ve Çelebi limitleri. “Not aralıklarını değiştir”, “Öğün saati ekle” | Kaydedilmemiş değişiklik, geçersiz dosya limiti; öğün adında / \ ? # % yasak; save error | **Tam:** school_settings artık üç sekmeyi ve kişisel ayarlardan farkını kapsıyor | FE ../hezarfen_frontend/src/routes/router.tsx:262-266; ../hezarfen_frontend/src/pages/settings-page.tsx:41-45,106-175,189-587. BE ../hezarfen_backend/src/web/settings.rs:268-352. CB src/catalog.py:1389-1411 |
| 28 | **/management/classes** | FE route V/Ö/T/Y/A; menü T+; backend liste/işlem yetkileri T+/Y+ | Şube listele, oluştur, filtrele. “Şubeler nerede?”, “Sınıf oluştur” | Liste boş, 403, form doğrulama | **Tam:** branches_info görüntülemeyi; class_section_manage oluşturma/düzenleme/silmeyi ayırıyor. FE route guard’ın genişliği backend yetkisi sanılmamalı | FE ../hezarfen_frontend/src/routes/router.tsx:268-272; ../hezarfen_frontend/src/pages/classes-page.tsx:27-35,133-163; ../hezarfen_frontend/src/components/layout/nav-items.ts:145. BE ../hezarfen_backend/src/web/classes.rs:474,546,697. CB src/catalog.py:1637-1659; src/role_spaces.py:64 |
| 29 | **/management/classes/$id** | FE route V/Ö/T/Y/A; yönetim Y+; bazı okumalar T+ | Düzenle/sil, blueprint, üye ekle/çıkar, ders bağla/ayır. “Şubeye öğrenci ekle”, “Dersi şubeye bağla” | Üye/ders listesi boş, duplicate/404/403, onay diyaloğu | **Tam:** class_section_manage detay CRUD, üye ekle/çıkar ve ders bağla/ayır akışlarını kapsıyor | FE ../hezarfen_frontend/src/routes/router.tsx:274-278; ../hezarfen_frontend/src/pages/class-detail-page.tsx:42-53,196-331. BE ../hezarfen_backend/src/web/classes.rs:697,735,827,1193-1426. CB src/catalog.py:1637-1659 |
| 30 | **/management/terms** | Y/A | Dönem oluştur/düzenle/sil, ders bağlama. “Akademik dönem ekle” | Başlangıç/bitiş tarih sırası, dönem listesi boş, silme onayı | **Tam:** term_manage route ve ana CRUD akışını kapsıyor | FE ../hezarfen_frontend/src/routes/router.tsx:280-284; ../hezarfen_frontend/src/pages/terms-page.tsx:47-51,69-254. CB src/catalog.py:1364-1386 |
| 31 | **/exams/$id/live** | T/Y/A | Canlı katılımcı rosterı, durum/ilerleme takibi. “Sınavı canlı izle” | Katılımcı yok, bağlantı/yükleme hatası, sınav bulunamadı | **Tam:** exam_live_monitor doğru route ve amacı kapsıyor | FE ../hezarfen_frontend/src/routes/router.tsx:286-290; ../hezarfen_frontend/src/pages/live-monitor-page.tsx:30-34,255-325. CB src/catalog.py:921-944 |
| 32 | **/admin/users** | Yalnız A | Kullanıcı ara/listele, rol değiştir, kullanıcı detayına git. “Öğrenciyi öğretmen yap” | Sonuç yok, geçersiz rol, kendi rolünü değiştirme 403 | **Kısmi:** user_role_change var; kullanıcı arama, profil açma ve veli bağlantısı işlemleri eksik | FE ../hezarfen_frontend/src/routes/router.tsx:292-296; ../hezarfen_frontend/src/pages/admin-users-page.tsx:19-24,34-74. BE ../hezarfen_backend/src/web/users.rs:456-459. CB src/catalog.py:1414-1439 |
| 33 | **/admin/users/$id** | Yalnız A | Kullanıcı profili, rol, veli-öğrenci bağlantısı ekle/çıkar. “Veliyi öğrenciye bağla” | Kullanıcı bulunamadı; yanlış rol çifti; duplicate bağlantı; onay | **Kısmi:** rol değişimi var; kullanıcı profili ve parent-link yönetimi için intent yok | FE ../hezarfen_frontend/src/routes/router.tsx:298-302; ../hezarfen_frontend/src/pages/admin-user-detail-page.tsx:22-26,66-157. BE ../hezarfen_backend/src/web/users.rs:579,591,690-691. CB src/catalog.py:1414-1439 |
| 34 | **/guide** | V/Ö/T/Y/A | Çelebi, Defter, Soru havuzu, Dersler, Sınavlar, Karnem; rol ve ipuçları. “Rehber nerede?” | Statik içerik; yalnız route guard loading/denied | **Tam:** guide_info güncel adım listesini anlatıyor | FE ../hezarfen_frontend/src/routes/router.tsx:304-308; ../hezarfen_frontend/src/pages/guide-page.tsx:42-49,58-70,74-216. CB src/catalog.py:228-247 |
| 35 | **/profile/me** | V/Ö/T/Y/A; kendi profili | Profil/rozet/üyelik/istatistik görüntüle; ad-soyad, görünen ad, bio, e-posta, telefon, doğum tarihi ve avatar düzenle. “Profilimi aç”, “Fotoğrafımı kaldır” | E-posta/telefon/tarih doğrulaması; PNG/JPEG/WebP/GIF ve varsayılan 5 MiB; yükleme/kaldırma hatası | **Tam:** profile_view, profile_edit ve personal_settings ayrımı doğru; route /profile/me | FE ../hezarfen_frontend/src/routes/router.tsx:312-316; ../hezarfen_frontend/src/pages/profile-page.tsx:24-31,47-53,100-202; ../hezarfen_frontend/src/components/users/profile-form.tsx:68-117,124-177; ../hezarfen_frontend/src/components/users/avatar-upload.tsx:31-41,79-125. CB src/catalog.py:366-447,2143 |
| 36 | **/profile/$userId** | V/Ö/T/Y/A frontend; backend hedef kapsamı; yalnız kendi profilinde düzenleme | Başka kullanıcı profili/üyeliklerini görüntüleme. “Çocuğumun profilini aç”, “Başkasının profilini düzenleyebilir miyim?” | Veli yalnız kendisi/bağlı çocuk; gizli veya kapsam dışı 403/404; loading/error | **Tam:** profile_view hedef kapsamını ve self-only düzenlemeyi açıklar; privacy_security destekler | FE ../hezarfen_frontend/src/routes/router.tsx:318-322; ../hezarfen_frontend/src/pages/profile-page.tsx:24-31,47-70,90-95,129-163. BE ../hezarfen_backend/src/web/users.rs:1036-1042. CB src/catalog.py:366-421,1444-1464 |
| 37 | **/students** | Tam V | Bağlı çocuk seç, not/devam/pomodoro/özet raporlarını görüntüle. “Çocuğumun notları/devamsızlığı” | Bağlı çocuk yok, veri boş, erişim hatası | **Kısmi:** parent_info temel rolü anlatıyor; çocuk seçimi, profil, randevu, yemek ve ödeme alt akışları ayrı değil | FE ../hezarfen_frontend/src/routes/router.tsx:324-328; ../hezarfen_frontend/src/pages/my-students-page.tsx:40-84,157-258. BE ../hezarfen_backend/src/web/users.rs:690-691. CB src/catalog.py:1564-1589 |
| 38 | **/questions** | Ö/T/Y/A; yalnız Ö yeni soru sorar | Soru listele/filtrele, Ö soru sorar, sahibi/T+ siler, T+ moderasyon | “Soru bulunamadı”, konu/detay/görsel doğrulaması, bekliyor/ret durumları | **Kısmi:** question_ask tam Öğrenci yetkisini, question_approve T+ moderasyonu doğru uygular; bağımsız edit/delete intentleri yok | FE ../hezarfen_frontend/src/routes/router.tsx:330-334; ../hezarfen_frontend/src/pages/questions-page.tsx:30-34,45-114. BE ../hezarfen_backend/src/web/questions.rs:263-264,431-433. CB src/catalog.py:1983-2003; src/role_spaces.py:105-109 |
| 39 | **/questions/$id** | Ö/T/Y/A; Ö+ çözüm; T+ onay/ret; sahibi/T+ silme | Detay, çözüm gönder, çözüm/soru sil, moderasyon. “Soruyu onayla”, “Çözümümü sil” | Bulunamadı/gizli, boş çözüm, sahiplik 403, bekleyen/ret | **Kısmi:** question_solve ve question_approve var; soru/çözüm düzenleme-silme ve görsel yaşam döngüsü eksik | FE ../hezarfen_frontend/src/routes/router.tsx:336-340; ../hezarfen_frontend/src/pages/question-detail-page.tsx:29-60,119-206. BE ../hezarfen_backend/src/web/questions.rs:611,723-724. CB src/catalog.py:2006-2045 |
| 40 | **/calendar** | V/Ö/T/Y/A | Aylık takvim; etkinlik, sınav, ödev, randevu, ders oturumu; gün seç/Bugün. “Takvimde neler var?” | Seçili günde kayıt yok, veri yükleme hatası | **Tam:** calendar_info aylık görünümü ve birleşik kaynakları doğru anlatıyor | FE ../hezarfen_frontend/src/routes/router.tsx:342-346; ../hezarfen_frontend/src/pages/calendar-page.tsx:121-293,381. CB src/catalog.py:1662-1678 |
| 41 | **/appointments** | V/Ö randevu al/iptal; T+ saat yayınla, onay/ret, yeniden planla | Uygun saat, rezervasyon, talepler, haftalık tekrar, iptal/ret/yeniden planlama. “Randevu al/iptal et”, “Saati değiştir” | Neden zorunluluğu; tarih sırası; en çok 52 haftalık slot; dört ayrı boş liste ve çakışma | **Kısmi:** book, slot_open, requests var; cancel, reschedule, slot/seri silme ve validasyon soruları eksik | FE ../hezarfen_frontend/src/routes/router.tsx:348-352; ../hezarfen_frontend/src/pages/appointments-page.tsx:50-78,269-359,438-625; ../hezarfen_frontend/src/components/appointments/reschedule-form.tsx:31-36. BE ../hezarfen_backend/src/web/appointments.rs:264-266,536-537,861-868. CB src/catalog.py:1825-1889 |
| 42 | **/meals** | V/Ö/T/Y/A; herkes görür, Y+ yayınlar | Menü listesi, öğün/rezervasyon durumu, menü yayınlama. “Bugün yemek ne?”, “Menü yayınla” | “Menü yok”, yükleme; slot/cutoff ve öğün doğrulaması | **Kısmi:** meal_view ve meal_menu_manage var; filtre/tarih ve yayın yaşam döngüsü ayrıntıları eksik | FE ../hezarfen_frontend/src/routes/router.tsx:354-358; ../hezarfen_frontend/src/pages/meals-page.tsx:28-95. BE ../hezarfen_backend/src/web/meals.rs:262,355,388,421-482. CB src/catalog.py:1893-1912,1937-1956 |
| 43 | **/meals/$id** | V/Ö rezervasyon; T+ servis kaydı; Y+ menü/diyet; yalnız A kredi | Yer ayır/iptal, personelin served/missed kaydı, beslenme profili, yemek düzenleme, kredi. “Çocuğuma yer ayır”, “Servis edildi işaretle”, “Alerji etiketi”, “Kredi ekle” | Cutoff/kapasite, rezervasyon yok, bilinmeyen diyet etiketi, yalnız öğrenciye kredi, para doğrulaması | **Tam:** meal_book, meal_menu_manage, meal_credit_manage, meal_service_mark ve meal_dietary_profile_manage rol ve işlemleri ayırıyor | FE ../hezarfen_frontend/src/routes/router.tsx:360-364; ../hezarfen_frontend/src/pages/meal-detail-page.tsx:54-74,184-291. BE ../hezarfen_backend/src/web/meals.rs:606-686,783-807,1100-1172,1479-1511. CB src/catalog.py:1915-1978 |
| 44 | **/management/payments** | Y/A | Öğrenci ara, borç/tahsilat, iade/ters kayıt, plan oluştur/ata. “Tahsilat gir”, “İade et”, “Plan ata” | Öğrenci seçilmedi, liste boş, tutar/para birimi, idempotency/çakışma, onay | **Kısmi:** fees_manage yalnız genel yönetimi anlatıyor; collect/refund/reverse/plan eylemleri ayrı değil | FE ../hezarfen_frontend/src/routes/router.tsx:366-370; ../hezarfen_frontend/src/pages/payments-page.tsx:78-82,536-945. BE ../hezarfen_backend/src/web/payments.rs:776-798,828. CB src/catalog.py:1613-1634 |
| 45 | **/management/payments/$userId** | Y/A | Seçili öğrencinin ekstre ve yönetim işlemleri. “Bu öğrencinin borcunu aç”, “Ödemeyi geri al” | Kullanıcı bulunamadı/öğrenci değil, kayıt yok, tutar ve sahiplik hataları | **Kısmi:** fees_manage hedef öğrenci URL’sini ve işlem ayrımlarını anlatmıyor | FE ../hezarfen_frontend/src/routes/router.tsx:372-376; ../hezarfen_frontend/src/pages/payments-page.tsx:80,601-700. BE ../hezarfen_backend/src/web/payments.rs:776-798,828. CB src/catalog.py:1613-1634 |
| 46 | **/payments** | FE route V/Ö/T/Y/A; menü V/Ö; backend fiilen kendi/bağlı çocuk ekstresi, T erişemez | Salt okunur borç, ödeme ve dönem ekstresi. “Ücretlerim nerede?”, “Çocuğumun ödemesi” | “Ekstre kaydı yok”, bağlı çocuk seçimi, 403/404 | **Tam:** fees_info Ücretlerim adını, Ö self ve V linked-child kapsamını doğru anlatıyor; personel rol uzayında reddediliyor | FE ../hezarfen_frontend/src/routes/router.tsx:378-382; ../hezarfen_frontend/src/pages/payment-statement-page.tsx:33-170; ../hezarfen_frontend/src/components/layout/nav-items.ts:157. BE ../hezarfen_backend/src/web/payments.rs:776-798,828. CB src/catalog.py:1593-1610; src/role_spaces.py:92-94 |
| 47 | **/whiteboards** | Ö/T/Y/A; V hariç | Listele, yeni tahta oluştur, katılımcı seç, aç. “Tahta oluştur”, “Ortak tahtayı aç” | “Tahta yok”, başlık/katılımcı doğrulaması, create/load error | **Kısmi:** board_view ve board_create var; arama, katılımcı yönetimi ve silme ayrı değil | FE ../hezarfen_frontend/src/routes/router.tsx:384-388; ../hezarfen_frontend/src/pages/whiteboards-page.tsx:25-177. BE ../hezarfen_backend/src/web/boards.rs:74,83-85. CB src/catalog.py:2049-2088 |
| 48 | **/whiteboards/$id** | Ö/T/Y/A; katılımcı; oluşturucu yönetir; T+ toplu davet | Eşzamanlı çizim, bağlantı durumu, geçmiş, kilit/aç, temizle, kapat, katılımcı ekle/çıkar, sil | Bağlanıyor/bağlı/koptu; boş geçmiş; yetkisiz katılımcı; onay ve API hataları | **Kısmi:** board_create bazı yönetim kontrollerini söyler; geçmiş, reconnect, tekil katılımcı, silme ve sahiplik soruları eksik | FE ../hezarfen_frontend/src/routes/router.tsx:390-394; ../hezarfen_frontend/src/pages/whiteboard-page.tsx:35-39,106-421. BE ../hezarfen_backend/src/web/boards.rs:74,83-85,717-744. CB src/catalog.py:2049-2088 |

## Route olmayan fakat benchmarkta mutlaka bulunması gereken özellikler

### Kişisel Ayarlar

Kişisel Ayarlar ayrı bir route değildir; hesap/avatar menüsünden açılan bir diyalogdur. Hesap bölümünde Ad, Soyad, E-posta, Telefon ve Doğum tarihi; Görünüm bölümünde tema, dil ve vurgu paleti vardır. Görünen ad, Hakkında ve avatar yalnız tam profil akışında /profile/me üzerinden yönetilir. Kanıt: ../hezarfen_frontend/src/components/users/account-profile-dialog.tsx:11-18,53-136; ../hezarfen_frontend/src/components/layout/sidebar-account.tsx:67-104; ../hezarfen_frontend/src/components/layout/user-menu.tsx:116-179.

Sunucuya kalıcı tercih olarak yalnız theme, language ve palette gönderilir. Bildirim tercihi alanı yoktur. Kanıt: ../hezarfen_frontend/src/api/users/patchMyPreferences.ts:4-12 ve ../hezarfen_frontend/src/contexts/preferences-context.tsx:32-52,173-203,219-247. Chatbotun personal_settings ve language_theme cevapları bu ayrımı güncel olarak doğru kuruyor: src/catalog.py:424-473.

### Bildirim Merkezi

Bildirim ayarları sayfası yoktur. Üst bardaki zil; okunmamış mesaj, etkinlik, sınav ve ödev bildirimlerini tek merkezde birleştirir. Bildirime basınca ilgili sayfa açılır; mesaj ayrıca okundu işaretlenir. Tek bildirim kapatılabilir veya Tümünü sil yapılabilir. Kapatılan kimlikler yalnız tarayıcı localStorage alanında saklanır. Kanıt: ../hezarfen_frontend/src/components/layout/notification-center.tsx:50-145,169-197,200-310 ve ../hezarfen_frontend/src/lib/notifications.ts:1-53.

Mevcut notification_settings_info cevabı artık hayalî ses/e-posta toggle’ı önermiyor; ayrı tercih ekranı olmadığını ve zil merkezini doğru anlatıyor. Kanıt: src/catalog.py:1717-1740. Benchmark, “bildirimleri kapatmak istiyorum” ile “bildirimi listeden silmek istiyorum” arasındaki farkı özellikle sınamalıdır.

## Ortak görünür durumlar ve hata dili

| Durum ailesi | Kullanıcının görebileceği durum | Benchmark soru örnekleri | Kanıt |
|---|---|---|---|
| Genel yükleme | Sayfa spinnerı ve “Yükleniyor…” | “Sayfa neden sürekli yükleniyor?”, “Yükleme bitmiyor” | ../hezarfen_frontend/src/components/ui/page-spinner.tsx:3-9; ../hezarfen_frontend/src/i18n/messages.ts:3335 |
| Genel API hatası | Hata kutusu ve “Tekrar dene” | “Tekrar dene ne yapıyor?”, “Sayfa hata verdi” | ../hezarfen_frontend/src/components/ui/error-alert.tsx:6-22; ../hezarfen_frontend/src/i18n/messages.ts:3359 |
| Yetki | “Bu içeriğe erişimin yok.”; oturumsuzsa /login | “Giriş yaptım ama 403”, “Bu içeriğe erişimin yok diyor” | ../hezarfen_frontend/src/components/layout/route-guard.tsx:31-49; ../hezarfen_frontend/src/i18n/messages.ts:3361 |
| Genel boş tablo | “Sonuç yok” | “Aramada neden kimse çıkmıyor?”, “Liste boş” | ../hezarfen_frontend/src/components/ui/data-table.tsx:328; ../hezarfen_frontend/src/i18n/messages.ts:3387 |
| Başarı | Oluşturuldu / Kaydedildi / Silindi | “Kaydedildi mi?”, “Silme başarılı mı?” | ../hezarfen_frontend/src/i18n/messages.ts:3393-3395 |
| Onay | Geri döndürülemez veya kapsamlı işlemlerde ConfirmDialog | “Silme onayı neden geliyor?”, “İptal edebilir miyim?” | ../hezarfen_frontend/src/components/ui/confirm-dialog.tsx:37-129 |
| WebSocket | Bağlanıyor / Bağlı / bağlantı kesildi | “Tahta bağlanmıyor”, “Canlı bağlantı koptu” | ../hezarfen_frontend/src/i18n/messages.ts:4281-4282; ../hezarfen_frontend/src/pages/whiteboard-page.tsx:106-421 |

## Modül bazlı boş durum envanteri

| Modül | Görünür boş durum | Kanıt |
|---|---|---|
| Defter | Henüz not yok / arama sonucu yok | ../hezarfen_frontend/src/pages/notes-page.tsx:159-160; ../hezarfen_frontend/src/i18n/messages.ts:3519,3613 |
| Etkinlik | Etkinlik yok; roster veya yoklama satırı yok | ../hezarfen_frontend/src/pages/events-page.tsx:210; ../hezarfen_frontend/src/pages/event-detail-page.tsx:309,352; ../hezarfen_frontend/src/i18n/messages.ts:3654,3667,3672 |
| Sınav | Sınav yok; sonuç yok | ../hezarfen_frontend/src/pages/exams-page.tsx:291; ../hezarfen_frontend/src/pages/exam-detail-page.tsx:732; ../hezarfen_frontend/src/i18n/messages.ts:3781,3794 |
| Ödev | Ödev yok | ../hezarfen_frontend/src/pages/homework-page.tsx:247; ../hezarfen_frontend/src/i18n/messages.ts:4180 |
| Karnem | Henüz not/devam kaydı yok | ../hezarfen_frontend/src/pages/marks-page.tsx:62; ../hezarfen_frontend/src/i18n/messages.ts:4214 |
| Ders/şube | Ders yok; şube, üye veya bağlı ders yok | ../hezarfen_frontend/src/pages/courses-page.tsx:204; ../hezarfen_frontend/src/pages/classes-page.tsx:153; ../hezarfen_frontend/src/pages/class-detail-page.tsx:254,265; ../hezarfen_frontend/src/i18n/messages.ts:4142,3102,3121-3122 |
| Randevu | Açık saat, talep, yaklaşan veya geçmiş randevu yok | ../hezarfen_frontend/src/pages/appointments-page.tsx:492,510,532,556; ../hezarfen_frontend/src/i18n/messages.ts:3743,3752-3753 |
| Yemek | Menü veya rezervasyon yok | ../hezarfen_frontend/src/pages/meals-page.tsx:90; ../hezarfen_frontend/src/pages/meal-detail-page.tsx:228; ../hezarfen_frontend/src/i18n/messages.ts:4342,4357 |
| Ödeme | Ekstre/işlem/öğrenci sonucu yok | ../hezarfen_frontend/src/pages/payment-statement-page.tsx:142; ../hezarfen_frontend/src/pages/payments-page.tsx:627,700; ../hezarfen_frontend/src/i18n/messages.ts:4470,4490,4436 |
| Tahta | Tahta veya geçmiş kaydı yok | ../hezarfen_frontend/src/pages/whiteboards-page.tsx:69; ../hezarfen_frontend/src/pages/whiteboard-page.tsx:399,421; ../hezarfen_frontend/src/i18n/messages.ts:4401,4427 |
| Mesai | Kendi/personel kaydı yok | ../hezarfen_frontend/src/pages/work-log-page.tsx:131; ../hezarfen_frontend/src/pages/staff-work-page.tsx:258,291; ../hezarfen_frontend/src/i18n/messages.ts:4552,4560 |
| Mesaj | Seçili klasörde mesaj yok | ../hezarfen_frontend/src/pages/messages-page.tsx:364; ../hezarfen_frontend/src/i18n/messages.ts:4578 |
| Takvim | Seçili gün için plan yok | ../hezarfen_frontend/src/pages/calendar-page.tsx:381; ../hezarfen_frontend/src/i18n/messages.ts:3694 |
| Bildirim | Yeni bildirim yok | ../hezarfen_frontend/src/components/layout/notification-center.tsx:255-264; ../hezarfen_frontend/src/i18n/messages.ts:3302 |
| Soru bankası/havuzu | Soru şablonu veya havuz sorusu yok | ../hezarfen_frontend/src/pages/question-bank-page.tsx:228; ../hezarfen_frontend/src/pages/questions-page.tsx:114; ../hezarfen_frontend/src/i18n/messages.ts:3872,3410 |
| Pomodoro/dönem | Oturum veya dönem yok | ../hezarfen_frontend/src/pages/pomodoro-page.tsx:298; ../hezarfen_frontend/src/pages/terms-page.tsx:196; ../hezarfen_frontend/src/i18n/messages.ts:3935,4516 |

## Doğrulama ve sınır durumları

| Alan | Gerçek kural / hata | Benchmarkta sınanacak soru | Kanıt |
|---|---|---|---|
| Giriş/kayıt | Kullanıcı adı ve şifre zorunlu; kayıt şifreleri eşleşmeli | “Şifreler uyuşmuyor”, “Boş kullanıcı adıyla kayıt olur mu?” | ../hezarfen_frontend/src/pages/login-page.tsx:39-43; ../hezarfen_frontend/src/pages/register-page.tsx:39-47; ../hezarfen_frontend/src/i18n/messages.ts:3424,3429-3430 |
| Profil e-posta | Biçim geçerli olmalı | “Profil e-postamı niye kabul etmiyor?” | ../hezarfen_frontend/src/components/users/profile-form.tsx:68-75; ../hezarfen_frontend/src/i18n/messages.ts:4277 |
| Profil telefon | İsteğe bağlı + ve 7-15 hane | “Telefon numaram geçersiz diyor” | ../hezarfen_frontend/src/components/users/profile-form.tsx:68-75; ../hezarfen_frontend/src/i18n/messages.ts:4278 |
| Profil doğum tarihi | Gerçek ve gelecekte olmayan tarih; giriş yer tutucusu GG/AA/YYYY, hata metni YYYY-AA-GG der | “Doğum tarihi formatı ne?”, “Neden iki format yazıyor?” | ../hezarfen_frontend/src/components/users/profile-form.tsx:14-24,68-75,172-173; ../hezarfen_frontend/src/i18n/messages.ts:4100,4279 |
| Avatar | PNG/JPEG/WebP/GIF; varsayılan en çok 5 MiB | “Fotoğraf dosyam neden yüklenmiyor?”, “Avatarı kaldır” | ../hezarfen_frontend/src/components/users/avatar-upload.tsx:31-41,79-125; ../hezarfen_frontend/src/i18n/messages.ts:3223-3232 |
| Defter | Başlık zorunlu ve en çok 200; içerik en çok 10.000; dosya sayısı en çok 10 | “Not başlığı zorunlu mu?”, “Kaç ek yükleyebilirim?” | ../hezarfen_frontend/src/components/notes/note-form.tsx:59-73; ../hezarfen_frontend/src/i18n/messages.ts:4107-4109 |
| Defter içe aktarma | Desteklenmeyen format/OCR hatası ve kısmi dosya yükleme olabilir | “PDF okunamadı”, “Bazı ekler neden yüklenmedi?” | ../hezarfen_frontend/src/components/notes/note-import-panel.tsx:37,63; ../hezarfen_frontend/src/pages/notes-page.tsx:135; ../hezarfen_frontend/src/i18n/messages.ts:3643-3646 |
| Tarih/saat | Bitiş başlangıçtan önce olamaz; işaret/not aralıkları geçerli olmalı | “Bitiş saati niye reddediliyor?”, “Not değeri aralık dışında” | ../hezarfen_frontend/src/i18n/messages.ts:4111-4114; ../hezarfen_frontend/src/components/courses/course-sessions-panel.tsx:121-151; ../hezarfen_frontend/src/components/exams/grade-form.tsx:44-48 |
| Randevu | Sebep/form alanı, yeniden planlama sırası; haftalık seri en çok 52 | “52’den fazla saat açabilir miyim?”, “Randevu saati çakışıyor” | ../hezarfen_frontend/src/components/appointments/book-appointment-form.tsx:25-29; ../hezarfen_frontend/src/components/appointments/reschedule-form.tsx:31-36; ../hezarfen_frontend/src/i18n/messages.ts:3754-3756,3771 |
| Personel mesaisi | Açık kayıt düzenlenemez; giriş/çıkış zorunlu ve sıralı | “Açık mesaiyi neden düzeltemiyorum?” | ../hezarfen_frontend/src/pages/staff-work-page.tsx:201,220-224; ../hezarfen_frontend/src/i18n/messages.ts:4567-4568 |
| Okul ayarları | Dosya limiti aralığı; öğün/slot adında / \ ? # % yasak | “Öğün adını niye kabul etmiyor?”, “Dosya limiti geçersiz” | ../hezarfen_frontend/src/pages/settings-page.tsx:111-124; ../hezarfen_frontend/src/i18n/messages.ts:4310-4311 |
| Etkinlik yoklaması | Önce öğrenci seçilmeli; hedef etkinlik kitlesinde olmalı | “Öğrenci seçmeden yoklama yapamıyorum” | ../hezarfen_frontend/src/pages/event-detail-page.tsx:291-303,327-340; ../hezarfen_backend/src/web/events.rs:481-535 |
| Ödev | Teslim tarihi ve başlangıç sırası geçerli olmalı; notlandırılmış teslim geri çekilemez | “Not verildikten sonra ödevi geri alabilir miyim?” | ../hezarfen_frontend/src/pages/homework-page.tsx:118-121; ../hezarfen_frontend/src/i18n/messages.ts:4187,4223,2653-2659 |
| Dönem | Dönem başlangıç/bitiş tarihleri geçerli sırada olmalı | “Dönem tarihleri geçersiz diyor” | ../hezarfen_frontend/src/pages/terms-page.tsx:138-142; ../hezarfen_frontend/src/i18n/messages.ts:4519 |

## Mevcut chatbotla çelişen veya açık kalan noktalar

| Öncelik | Bulgu | Etki | Kanıt / yapılacak benchmark |
|---:|---|---|---|
| 2 | /management/classes ve /payments frontend route guard’ları menü/backend kapsamından daha geniştir. | Yalnız route’a bakarak benchmark yazılırsa V/Ö için şube yönetimi veya T için ödeme okuma yanlışlıkla ALLOW beklenebilir. | FE ../hezarfen_frontend/src/routes/router.tsx:268-278,378-382; ../hezarfen_frontend/src/components/layout/nav-items.ts:145,157. BE ../hezarfen_backend/src/web/classes.rs:474,546,697; ../hezarfen_backend/src/web/payments.rs:776-798. |
| 3 | Profil tarih alanı kullanıcıya GG/AA/YYYY yer tutucusu gösterirken hata mesajı YYYY-AA-GG biçimini söyler. | Chatbot hangi formatı söyleyeceği konusunda kararsız kalabilir; test gerçek UI çelişkisini kayıt altına almalı. | FE ../hezarfen_frontend/src/i18n/messages.ts:4100,4279; ../hezarfen_frontend/src/components/users/profile-form.tsx:14-24. |
| 5 | fees_manage ve board_create gibi geniş intentler çok sayıda farklı eylemi tek cevapta toplar. | Retrieval doğru route'u bulsa bile kullanıcının “iade” veya “geçmişi aç” gibi asıl fiiline cevap ayrıntısı sınırlı kalabilir. | FE ../hezarfen_frontend/src/pages/payments-page.tsx:536-945; ../hezarfen_frontend/src/pages/whiteboard-page.tsx:106-421. |

Önceki yanlışlıklardan profil route'u, bildirim ayarı, etkinlikte öğrencinin kendi yoklamasını işaretlemesi, Pomodoro rolü, yemek kredisi rolü, etüt/kulüp yönlendirmesi, aylık takvim, mobil rol sekmeleri, `question_ask` exact Öğrenci yetkisi ve eski `messages_use` belirsizlik notu mevcut katalogda düzeltilmiştir. Bunlar regresyon benchmarkında tutulmalı, fakat artık “mevcut hata” olarak raporlanmamalıdır. Kanıt: src/catalog.py ve src/role_spaces.py içindeki ilgili intent/rol kayıtları.

## Öncelikli benchmark soru aileleri

Her ailede en az şu varyantlar bulunmalıdır: düzgün Türkçe, kısa/eksik Türkçe, yazım hatası, ekli fiil, olumsuzluk, rol beyanı, yetkisiz rol, iki niyetli cümle ve yakın kavram çakışması.

1. **Defter notu ile sınav/ödev puanı ayrımı**
   - “not al”, “ben not silmek”, “notu değiştir”, “Ayşe’nin sınav notunu sil”, “ödev puanını kaldır”, “not silme ama puanı değiştirme”
   - Beklenti: note_create/edit/delete ile exam_grade_student/homework_grade karışmamalı.

2. **Profil, kişisel ayar ve rol ayrımı**
   - “profilimi aç”, “görünen adımı değiştir”, “avatarı kaldır”, “paleti değiştir”, “bildirim sesini kapat”, “beni öğretmen yap”
   - Beklenti: profile_view/edit, personal_settings, notification_settings_info ve user_role_change ayrılmalı.

3. **Ders, etüt, kulüp ve şube**
   - “kulübe kendim yazılayım”, “şubeye öğrenci ekle”, “ders pdfi nerde”, “derse öğretmen ata”, “etüt ayrı sayfa mı”
   - Beklenti: filtre yönlendirmesi, yönetici roster modeli ve sınıf yönetimi yetkisi karışmamalı.

4. **Etkinlik ve yoklama**
   - “etkinlikler nerde”, “öğrenciyi etkinliğe ekle”, “kendi katılımımı var yap”, “etkinliği sil”, “roster boş”
   - Beklenti: yalnız T+ yoklama; student self-mark DENY; edit/registration boşluğu görünür olmalı.

5. **Sınav ve ödev yaşam döngüsü**
   - “sınava geri döncem”, “cevabım kaydoldu mu”, “sınavı yayınla”, “cevap kağıdını aç”, “ödev teslimini geri al”, “notlandıktan sonra dosyayı sil”
   - Beklenti: exact Ö giriş/teslim; T+ yönetim; eksik publish/withdraw intentleri fallbacke kaymamalı.

6. **Mesaj yaşam döngüsü**
   - “mesaj at”, “yanıtla”, “arşivden çıkar”, “çöpten geri getir”, “kalıcı sil”, “çöpü boşalt”
   - Beklenti: geniş messages_use yerine eylem bazlı cevap yeterliliği ölçülmeli.

7. **Randevu**
   - “randevu al”, “iptal et”, “saati değiştir”, “öğretmen müsaitlik açsın”, “talebi onayla”, “haftalık 60 saat aç”
   - Beklenti: V/Ö book; T+ manage; cancel/reschedule/validation açıkları ölçülmeli.

8. **Yemek ve ödeme**
   - “yemek ayır”, “çocuğuma ayır”, “servis edildi işaretle”, “alerji etiketi ekle”, “kredi yükle”, “tahsilat gir”, “iade et”, “plan ata”
   - Beklenti: T servis, Y menü/diyet, yalnız A kredi; payment management ile meal credit karışmamalı.

9. **Soru bankası ve soru havuzu**
   - “şablon soru oluştur”, “soruya görsel ekle”, “havuzda soru sor”, “çözüm gönder”, “soruyu onayla”, “çözümü sil”
   - Beklenti: question-bank ile questions ayrılmalı; ask yalnız exact Ö olmalı.

10. **Beyaz tahta**
    - “tahta aç/oluştur”, “katılımcı çıkar”, “kilitle”, “geçmişi göster”, “bağlantı koptu”, “tahtayı sil”
    - Beklenti: owner/participant/T+ bulk yetkileri ve WebSocket hata yüzeyi ayrı ölçülmeli.

11. **Olumsuzluk ve çok niyet**
    - “notu silme sadece değiştir”, “randevuyu onaylama reddet”, “ödevi silmeden puanla”, “tahtayı kapatma kilitle”, “etkinlik oluşturma sadece bak”
    - Beklenti: olumsuzlanan eylem seçilmemeli; sistem mümkünse tek baskın eylemi seçmeli, riskli çift eylemde açıklama istemeli.

12. **Yetki ve kapsam**
    - Her eylemi V/Ö/T/Y/A ile tekrar et: “Ben öğretmenim sınava gireyim”, “Adminim pomodoro başlat”, “Veliyim çocuğumun ödemesini aç”, “Yöneticiyim yemek kredisi ekle”
    - Beklenti backend sözleşmesi olmalı; yalnız rol sırası kullanılmamalı.

## Benchmark kayıt şeması önerisi

Mevcut uygulama iki katmanlıdır:

- Gold `data/benchmark.jsonl` insan denetimini kolaylaştırmak için minimal
  `question`, `expected_intent`, `role` alanlarını taşır.
- `stress-v3.5.0` kayıtları kalıcı `id`, tam `expected` yanıt sözleşmesi,
  `policy`, `family`, `mutation`, `scope`, `source`, `generator_version` ve
  gizlilik taraması alanlarını taşır. Sonuç JSONL'si tam Engine payload'ını;
  25 Markdown parçası kullanıcıya görünen soru/cevabı taşır.

Her soru için aşağıdaki alanlar tutulursa hem yanlış intent hem yanlış yetki hem de yanlış metin ayrı ayrı ölçülebilir:

| Alan | Açıklama |
|---|---|
| id | Kalıcı ve benzersiz vaka kimliği |
| query | Kullanıcı cümlesi |
| locale | tr veya en |
| role | V/Ö/T/Y/A/Z |
| authenticated | true/false |
| expected_intent | Beklenen intent |
| expected_auth_action | ALLOW, DENY, LOGIN veya CLARIFY |
| expected_route | Gerçek frontend route’u; route olmayan diyalog/özellikte null |
| expected_scope | self, enrolled, managed, linked-child, school veya global |
| expected_response_id | Beklenen cevap kimliği |
| must_include | Cevapta bulunması gereken route, rol, düğme veya uyarı |
| must_not_include | Yanlış yakın intent, yanlış rol veya olmayan UI kontrolü |
| surface | route, dialog, notification-center, validation, empty, error veya websocket |
| source | Bu belgedeki frontend/backend dosya:satır kanıtı |

Önerilen rapor ayrımları: intent doğruluğu, auth-action doğruluğu, route doğruluğu, role/scope doğruluğu, zorunlu ifade doğruluğu ve fallback oranı. Böylece doğru intent bulup yanlış yetki anlatan bir cevap “başarılı” sayılmaz.

## Kaynak özeti

- Route tanımları: ../hezarfen_frontend/src/routes/router.tsx:93-445
- Menü ve role göre görünürlük: ../hezarfen_frontend/src/components/layout/nav-items.ts:95-188,236-244
- Route guard: ../hezarfen_frontend/src/components/layout/route-guard.tsx:12-49
- Türkçe görünür metinler: ../hezarfen_frontend/src/i18n/messages.ts:3102-4578
- Chatbot intent kataloğu: src/catalog.py:85-2088
- Chatbot route eşlemesi: src/catalog.py:2122-2266
- Chatbot rol uzayları: src/role_spaces.py:48-201
- Backend rol extractorları: ../hezarfen_backend/src/web/extractor.rs:81-142
- Backend gözlem/kapsam yaklaşımı: ../hezarfen_backend/src/web/mod.rs:78-99
