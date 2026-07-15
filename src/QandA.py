"""Eğitim platformu chatbot'u için başlangıç soru/cevap kataloğu.

Bu modül yalnızca veri içerir. Intent bulma, metin normalizasyonu ve cevap
şablonlarını doldurma işlemleri chatbot motorunun sorumluluğundadır.

`example_questions` geliştirme/rule örnekleridir. Gerçek benchmark soruları
ayrı bir dosyada tutulmalı ve bu listeye kopyalanmamalıdır.
"""

from __future__ import annotations

from typing import Any, Final


# Gerçek uygulamada bu bilgiler oturum açmış kullanıcıya göre API'den gelir.
MOCK_STUDENT: Final[dict[str, Any]] = {
    "student_id": "STU-2026-001",
    "first_name": "Deniz",
    "last_name": "Yılmaz",
    "student_number": "1042",
    "school": "Örnek Anadolu Lisesi",
    "class_name": "10-A",
    "academic_year": "2025-2026",
    "term": "2. dönem",
    "advisor_teacher": "Ayşe Demir",
    "grades": {
        "Matematik": [85, 90],
        "Türk Dili ve Edebiyatı": [78, 82],
        "Fizik": [74, 80],
        "Kimya": [88, 84],
        "İngilizce": [92, 95],
    },
    "grade_average": 84.8,
    "attendance": {
        "excused_days": 2,
        "unexcused_days": 1,
        "late_count": 3,
    },
    "today_schedule": [
        "Matematik",
        "Matematik",
        "Türk Dili ve Edebiyatı",
        "Fizik",
        "İngilizce",
        "Beden Eğitimi",
    ],
    "tomorrow_schedule": [
        "Kimya",
        "Biyoloji",
        "Tarih",
        "Matematik",
        "İngilizce",
        "Görsel Sanatlar",
    ],
    "upcoming_exams": [
        {"course": "Matematik", "date": "20 Mayıs 2026", "time": "10:00"},
        {"course": "Fizik", "date": "23 Mayıs 2026", "time": "11:00"},
    ],
    "active_homework": [
        {
            "course": "Türk Dili ve Edebiyatı",
            "title": "Roman incelemesi",
            "due_date": "18 Mayıs 2026",
        },
        {
            "course": "Matematik",
            "title": "İkinci derece denklemler testi",
            "due_date": "19 Mayıs 2026",
        },
    ],
    "announcements": [
        "Bilim fuarı başvuruları 22 Mayıs'a kadar devam ediyor.",
        "Veli toplantısı 30 Mayıs Cumartesi günü yapılacaktır.",
    ],
}


# Alan açıklamaları:
# - intent: Motorun döndüreceği benzersiz sınıf adı.
# - response_id: Testlerde cevap metni yerine karşılaştırılacak kararlı kimlik.
# - response_template: MOCK_STUDENT alanlarıyla doldurulabilecek cevap.
# - auth_required: Kişisel veri göstermek için oturum gerekip gerekmediği.
# - example_questions: Kural geliştirme örnekleri; benchmark değildir.
# - must_not_match: Bu intent ile sık karışabilecek intentler.
INTENTS: Final[list[dict[str, Any]]] = [
    {
        "intent": "greeting",
        "category": "general",
        "description": "Kullanıcının sohbeti başlatması veya selam vermesi.",
        "response_id": "welcome_message",
        "response_template": (
            "Merhaba! Notlar, devamsızlık, ders programı, sınavlar, ödevler "
            "ve okul duyuruları hakkında yardımcı olabilirim."
        ),
        "auth_required": False,
        "example_questions": [
            "Merhaba",
            "Selam",
            "Günaydın",
            "İyi günler",
            "Hey",
            "Selam bot",
            "Merhabalar",
            "Nasılsın?",
        ],
        "must_not_match": [],
    },
    {
        "intent": "help",
        "category": "general",
        "description": "Chatbotun neler yapabildiğinin sorulması.",
        "response_id": "capabilities",
        "response_template": (
            "Notlarını ve ortalamanı gösterebilir; devamsızlık, ders programı, "
            "yaklaşan sınavlar, ödevler ve duyurular hakkında bilgi verebilirim."
        ),
        "auth_required": False,
        "example_questions": [
            "Neler yapabilirsin?",
            "Bana nasıl yardımcı olabilirsin?",
            "Yardım",
            "Hangi soruları sorabilirim?",
            "Ne işe yarıyorsun?",
            "Komutları göster",
            "Özelliklerin neler?",
            "Senden ne öğrenebilirim?",
        ],
        "must_not_match": [],
    },
    {
        "intent": "student_profile",
        "category": "student",
        "description": "Öğrencinin okul, sınıf veya numara bilgisini istemesi.",
        "response_id": "student_profile_summary",
        "response_template": (
            "{first_name} {last_name}, {school} {class_name} sınıfındasın. "
            "Öğrenci numaran {student_number}."
        ),
        "auth_required": True,
        "example_questions": [
            "Öğrenci bilgilerimi göster",
            "Hangi sınıftayım?",
            "Okul numaram ne?",
            "Numaramı unuttum",
            "Profilimi göster",
            "Hangi okulda kayıtlıyım?",
            "Sınıfım neydi?",
            "Kayıt bilgilerim neler?",
        ],
        "must_not_match": ["advisor_teacher"],
    },
    {
        "intent": "course_grades",
        "category": "grades",
        "description": "Bir dersin veya tüm derslerin notlarını istemesi.",
        "response_id": "course_grades_list",
        "response_template": "Güncel ders notların: {grades}.",
        "auth_required": True,
        "entities": ["course"],
        "example_questions": [
            "Notlarımı göster",
            "Sınav sonuçlarım açıklandı mı?",
            "Matematikten kaç aldım?",
            "Fizik notum ne?",
            "Yazılı notlarımı öğrenebilir miyim?",
            "İngilizce sınav sonucumu göster",
            "Bu dönemki notlarım nasıl?",
            "Ders notlarım kaç?",
            "Son sınavdan kaç almışım?",
            "Kimya yazılım kaç geldi?",
        ],
        "must_not_match": ["grade_average", "upcoming_exams"],
    },
    {
        "intent": "grade_average",
        "category": "grades",
        "description": "Dönem veya genel not ortalamasını istemesi.",
        "response_id": "grade_average_value",
        "response_template": "{term} not ortalaman {grade_average}.",
        "auth_required": True,
        "example_questions": [
            "Ortalamam kaç?",
            "Not ortalamamı göster",
            "Dönem ortalamam ne?",
            "Genel ortalamam kaç oldu?",
            "Ortalama kaç geliyor?",
            "Başarı puanım nedir?",
            "Bu dönemki ortalamamı merak ediyorum",
            "Derslerimin ortalaması kaç?",
        ],
        "must_not_match": ["course_grades"],
    },
    {
        "intent": "attendance_summary",
        "category": "attendance",
        "description": "Özürlü, özürsüz devamsızlık ve geç kalma bilgisini istemesi.",
        "response_id": "attendance_summary",
        "response_template": (
            "{attendance[excused_days]} gün özürlü, "
            "{attendance[unexcused_days]} gün özürsüz devamsızlığın ve "
            "{attendance[late_count]} geç kalma kaydın bulunuyor."
        ),
        "auth_required": True,
        "example_questions": [
            "Devamsızlığım kaç gün?",
            "Kaç gün okula gelmemişim?",
            "Özürsüz devamsızlığımı göster",
            "Devamsızlık bilgilerim neler?",
            "Kaç kere geç kaldım?",
            "Yok yazıldığım günleri göster",
            "Devamsızlık hakkım ne durumda?",
            "Bugün yok yazılmış mıyım?",
            "Raporlu günlerim sisteme girilmiş mi?",
            "Devamsızlığım var mı?",
        ],
        "must_not_match": ["leave_document_process"],
    },
    {
        "intent": "today_schedule",
        "category": "schedule",
        "description": "Bugünün ders programını istemesi.",
        "response_id": "today_schedule_list",
        "response_template": "Bugünkü derslerin sırasıyla: {today_schedule}.",
        "auth_required": True,
        "example_questions": [
            "Bugün hangi dersler var?",
            "Bugünkü programım ne?",
            "Bugün ilk ders ne?",
            "Ders programımı göster",
            "Bugünün derslerini sırala",
            "Bugün matematik var mı?",
            "Öğleden sonra hangi dersler var?",
            "Bugün son dersimiz ne?",
        ],
        "must_not_match": ["tomorrow_schedule", "weekly_schedule"],
    },
    {
        "intent": "tomorrow_schedule",
        "category": "schedule",
        "description": "Yarının ders programını istemesi.",
        "response_id": "tomorrow_schedule_list",
        "response_template": "Yarınki derslerin sırasıyla: {tomorrow_schedule}.",
        "auth_required": True,
        "example_questions": [
            "Yarın hangi dersler var?",
            "Yarının programını göster",
            "Yarın ilk ders ne?",
            "Yarın matematik var mı?",
            "Yarın hangi kitapları getireceğim?",
            "Yarınki derslerimi sırala",
            "Yarın son iki ders ne?",
            "Yarının ders programı nedir?",
        ],
        "must_not_match": ["today_schedule", "weekly_schedule"],
    },
    {
        "intent": "weekly_schedule",
        "category": "schedule",
        "description": "Haftalık veya belirli bir günün ders programını istemesi.",
        "response_id": "weekly_schedule_link",
        "response_template": (
            "Haftalık ders programına Dersler > Ders Programı bölümünden ulaşabilirsin."
        ),
        "auth_required": True,
        "entities": ["weekday"],
        "example_questions": [
            "Haftalık ders programımı göster",
            "Pazartesi hangi dersler var?",
            "Cuma günü programım ne?",
            "Bu haftanın dersleri neler?",
            "Haftalık program nerede?",
            "Salı günü kaç dersim var?",
            "Çarşamba son ders ne?",
            "Perşembe beden eğitimi var mı?",
        ],
        "must_not_match": ["today_schedule", "tomorrow_schedule"],
    },
    {
        "intent": "upcoming_exams",
        "category": "exams",
        "description": "Yaklaşan sınavların tarih ve saatlerini istemesi.",
        "response_id": "upcoming_exams_list",
        "response_template": "Yaklaşan sınavların: {upcoming_exams}.",
        "auth_required": True,
        "entities": ["course", "date_range"],
        "example_questions": [
            "Yaklaşan sınavlarım neler?",
            "Sınavlar ne zaman?",
            "Matematik sınavı hangi gün?",
            "Bu hafta sınav var mı?",
            "Bir sonraki sınavım hangisi?",
            "Sınav takvimimi göster",
            "Yarın sınavım var mı?",
            "Fizik yazılısı saat kaçta?",
            "Mayıs ayındaki sınavlarım neler?",
            "En yakın yazılı ne zaman?",
        ],
        "must_not_match": ["course_grades", "makeup_exam"],
    },
    {
        "intent": "makeup_exam",
        "category": "exams",
        "description": "Kaçırılan sınav veya mazeret sınavı sürecini sorması.",
        "response_id": "makeup_exam_process",
        "response_template": (
            "Mazeret sınavı için geçerli belgeni okul yönetimine teslim etmelisin. "
            "Kesin tarih, başvurun onaylandıktan sonra duyurulur."
        ),
        "auth_required": False,
        "example_questions": [
            "Sınavı kaçırdım ne yapmalıyım?",
            "Mazeret sınavı ne zaman?",
            "Telafi sınavına nasıl girerim?",
            "Hasta olduğum için yazılıya giremedim",
            "Kaçırdığım sınavın telafisi var mı?",
            "Raporla sınava tekrar girebilir miyim?",
            "Mazeret sınavına nereden başvurulur?",
            "Sınava katılamadım",
        ],
        "must_not_match": ["upcoming_exams", "leave_document_process"],
    },
    {
        "intent": "active_homework",
        "category": "homework",
        "description": "Aktif ödevleri ve teslim tarihlerini istemesi.",
        "response_id": "active_homework_list",
        "response_template": "Teslim edilmesi gereken ödevlerin: {active_homework}.",
        "auth_required": True,
        "entities": ["course"],
        "example_questions": [
            "Ödevlerim neler?",
            "Yapmam gereken ödev var mı?",
            "Matematik ödevi neydi?",
            "Ödev teslim tarihi ne zaman?",
            "Bu haftaki ödevleri göster",
            "Yarın teslim edilecek ödev var mı?",
            "Edebiyat ödevinin konusu ne?",
            "Eksik ödevim var mı?",
            "Aktif görevlerimi göster",
            "Hangi ödevleri yapmadım?",
        ],
        "must_not_match": ["homework_submission"],
    },
    {
        "intent": "homework_submission",
        "category": "homework",
        "description": "Ödev yükleme ve teslim etme yöntemini sorması.",
        "response_id": "homework_submission_instructions",
        "response_template": (
            "Ödevini Ödevler > Aktif Ödevler bölümünden seçip 'Dosya Yükle' "
            "adımıyla teslim edebilirsin. Dosya türü ve boyut sınırını kontrol et."
        ),
        "auth_required": True,
        "example_questions": [
            "Ödevimi nasıl yüklerim?",
            "Ödev nereden teslim ediliyor?",
            "Dosya yükleyemiyorum",
            "Ödevi sisteme nasıl atacağım?",
            "Teslim butonu nerede?",
            "Hangi dosya türlerini yükleyebilirim?",
            "Ödev yükleme sınırı kaç MB?",
            "Yanlış dosya yükledim, değiştirebilir miyim?",
        ],
        "must_not_match": ["active_homework", "technical_problem"],
    },
    {
        "intent": "school_announcements",
        "category": "announcements",
        "description": "Okul veya sınıf duyurularını istemesi.",
        "response_id": "school_announcements_list",
        "response_template": "Güncel duyurular: {announcements}.",
        "auth_required": True,
        "example_questions": [
            "Yeni duyuru var mı?",
            "Okul duyurularını göster",
            "Bugün bir açıklama yapıldı mı?",
            "Son duyuru ne?",
            "Sınıfımıza gelen duyurular neler?",
            "Veli toplantısı ne zaman?",
            "Bilim fuarı başvurusu ne zaman bitiyor?",
            "Önemli bir bildirim var mı?",
        ],
        "must_not_match": ["academic_calendar"],
    },
    {
        "intent": "academic_calendar",
        "category": "calendar",
        "description": "Tatil, dönem başlangıcı veya karne tarihi gibi takvim bilgileri.",
        "response_id": "academic_calendar_info",
        "response_template": (
            "Akademik takvime Takvim bölümünden ulaşabilirsin. Tarihler okul "
            "yönetiminin yayımladığı güncel takvime göre gösterilir."
        ),
        "auth_required": False,
        "entities": ["event_type"],
        "example_questions": [
            "Okullar ne zaman kapanıyor?",
            "Karne günü ne zaman?",
            "Ara tatil hangi gün?",
            "Yaz tatili ne zaman başlıyor?",
            "İkinci dönem ne zaman bitecek?",
            "Resmî tatiller hangileri?",
            "Akademik takvimi göster",
            "Okul ne zaman açılacak?",
        ],
        "must_not_match": ["school_announcements", "upcoming_exams"],
    },
    {
        "intent": "advisor_teacher",
        "category": "teachers",
        "description": "Sınıf rehber öğretmeni bilgisini istemesi.",
        "response_id": "advisor_teacher_name",
        "response_template": "Sınıf rehber öğretmenin {advisor_teacher}.",
        "auth_required": True,
        "example_questions": [
            "Rehber öğretmenim kim?",
            "Sınıf öğretmenimizin adı ne?",
            "Danışman öğretmenim kim?",
            "Rehber hocam kimdi?",
            "Sınıf danışmanımı göster",
            "Hangi öğretmen sınıfımızdan sorumlu?",
            "Rehber öğretmenimin adını söyle",
            "Danışman hocama nasıl ulaşırım?",
        ],
        "must_not_match": ["student_profile", "teacher_contact"],
    },
    {
        "intent": "teacher_contact",
        "category": "teachers",
        "description": "Öğretmene ulaşma veya mesaj gönderme yöntemini sorması.",
        "response_id": "teacher_contact_instructions",
        "response_template": (
            "Öğretmenine Mesajlar > Yeni Mesaj bölümünden ulaşabilirsin. "
            "Kişisel telefon ve e-posta bilgileri paylaşılmaz."
        ),
        "auth_required": True,
        "entities": ["teacher", "course"],
        "example_questions": [
            "Matematik öğretmenime nasıl ulaşırım?",
            "Öğretmenime mesaj göndermek istiyorum",
            "Hocanın telefon numarası ne?",
            "Ders öğretmenine nereden yazabilirim?",
            "Fizik hocasına soru soracağım",
            "Öğretmenimin e-postasını verir misin?",
            "Rehber öğretmenime mesaj atabilir miyim?",
            "Öğretmene ulaşma yolu nedir?",
        ],
        "must_not_match": ["advisor_teacher"],
    },
    {
        "intent": "report_card_document",
        "category": "documents",
        "description": "Karne, transkript veya öğrenci belgesini istemesi.",
        "response_id": "student_document_instructions",
        "response_template": (
            "Belgeler bölümünden karne ve not dökümünü görüntüleyebilirsin. "
            "Resmî öğrenci belgesi için okul yönetimine başvurmalısın."
        ),
        "auth_required": True,
        "entities": ["document_type"],
        "example_questions": [
            "Karnemi nereden görebilirim?",
            "Öğrenci belgesi almak istiyorum",
            "Transkriptimi indir",
            "Not dökümü nerede?",
            "Karne PDF'ini nasıl alırım?",
            "Belge talebi oluşturabilir miyim?",
            "Eski karnelerimi göster",
            "Öğrenci belgesi nasıl çıkarılır?",
        ],
        "must_not_match": ["course_grades", "leave_document_process"],
    },
    {
        "intent": "leave_document_process",
        "category": "attendance",
        "description": "Sağlık raporu veya devamsızlık mazeret belgesi süreci.",
        "response_id": "leave_document_instructions",
        "response_template": (
            "Sağlık raporu veya mazeret belgesini okul yönetimine, okulun "
            "belirlediği süre içinde teslim etmelisin. Onay durumunu Devamsızlık "
            "bölümünden takip edebilirsin."
        ),
        "auth_required": False,
        "example_questions": [
            "Raporumu nereye teslim edeceğim?",
            "Sağlık raporu sisteme nasıl girilir?",
            "Devamsızlık için mazeret belgesi vereceğim",
            "Raporlu günümü nasıl düzelttiririm?",
            "Hastane raporunu yükleyebilir miyim?",
            "Mazeret belgesi kaç gün içinde verilmeli?",
            "Yoklamama itiraz etmek istiyorum",
            "Devamsızlığım yanlış girilmiş",
        ],
        "must_not_match": ["attendance_summary", "makeup_exam"],
    },
    {
        "intent": "password_reset",
        "category": "account",
        "description": "Şifresini unutan veya hesabına giremeyen kullanıcı.",
        "response_id": "password_reset_instructions",
        "response_template": (
            "Giriş ekranındaki 'Şifremi Unuttum' bağlantısını kullan. Kayıtlı "
            "iletişim bilgilerine erişemiyorsan okul yönetimine başvur."
        ),
        "auth_required": False,
        "example_questions": [
            "Şifremi unuttum",
            "Hesabıma giremiyorum",
            "Şifremi nasıl yenilerim?",
            "Giriş yapamıyorum",
            "Parolamı sıfırlamak istiyorum",
            "Şifre yenileme kodu gelmedi",
            "Hesabım kilitlendi",
            "Kullanıcı bilgilerimi kabul etmiyor",
        ],
        "must_not_match": ["update_contact_info", "technical_problem"],
    },
    {
        "intent": "update_contact_info",
        "category": "account",
        "description": "Telefon, e-posta veya veli iletişim bilgisini güncelleme isteği.",
        "response_id": "contact_update_instructions",
        "response_template": (
            "İletişim bilgisi değişiklikleri doğrulama gerektirir. Profil > "
            "İletişim Bilgileri bölümünü kullanabilir veya okul yönetimine başvurabilirsin."
        ),
        "auth_required": True,
        "entities": ["contact_type"],
        "example_questions": [
            "Telefon numaramı değiştirmek istiyorum",
            "E-posta adresimi nasıl güncellerim?",
            "Veli telefon numarası yanlış",
            "İletişim bilgilerimi düzenle",
            "Eski numaram kayıtlı görünüyor",
            "Yeni e-posta adresimi ekleyebilir miyim?",
            "Velimin bilgilerini değiştireceğim",
            "Profil bilgilerim güncel değil",
        ],
        "must_not_match": ["student_profile", "password_reset"],
    },
    {
        "intent": "technical_problem",
        "category": "support",
        "description": "Platformda hata, açılmayan sayfa veya çalışmayan özellik bildirimi.",
        "response_id": "technical_support_steps",
        "response_template": (
            "Sayfayı yenileyip tekrar giriş yapmayı deneyebilirsin. Sorun sürerse "
            "hata mesajı ve ekran görüntüsüyle teknik destek kaydı oluştur. "
            "Şifreni veya kişisel bilgilerini ekran görüntüsüne ekleme."
        ),
        "auth_required": False,
        "example_questions": [
            "Sistem çalışmıyor",
            "Sayfa açılmıyor",
            "Bir hata mesajı alıyorum",
            "Notlar bölümü yüklenmiyor",
            "Uygulama sürekli kapanıyor",
            "Dosya yüklerken hata veriyor",
            "Ekran dondu",
            "Platforma erişemiyorum",
            "Butona basıyorum ama hiçbir şey olmuyor",
            "Teknik desteğe nasıl ulaşırım?",
        ],
        "must_not_match": ["password_reset", "homework_submission"],
    },
    {
        "intent": "privacy_and_security",
        "category": "security",
        "description": "Kişisel veriler, hesap güvenliği veya başkasının bilgilerini isteme.",
        "response_id": "privacy_policy_message",
        "response_template": (
            "Yalnızca oturum açmış kullanıcının yetkili olduğu bilgiler gösterilir. "
            "Başka öğrencilerin not, devamsızlık veya iletişim bilgilerini paylaşamam."
        ),
        "auth_required": False,
        "example_questions": [
            "Arkadaşımın notlarını göster",
            "Başka bir öğrencinin devamsızlığı kaç?",
            "Bilgilerimi kimler görebilir?",
            "Verilerim güvende mi?",
            "Sınıftaki herkesin notlarını göster",
            "Bir öğrencinin telefonunu verir misin?",
            "Hesabımı başkası kullanmış olabilir",
            "Kişisel bilgilerimi silmek istiyorum",
        ],
        "must_not_match": ["course_grades", "attendance_summary", "teacher_contact"],
    },
]


FALLBACK: Final[dict[str, str]] = {
    "response_id": "fallback_clarification",
    "response_template": (
        "Bu isteği anlayamadım. Notlar, devamsızlık, ders programı, sınavlar, "
        "ödevler veya duyurular hakkında daha açık bir soru sorabilir misin?"
    ),
}


def get_intent(intent_name: str) -> dict[str, Any] | None:
    """Intent adına göre katalog kaydını döndürür."""

    return next(
        (item for item in INTENTS if item["intent"] == intent_name),
        None,
    )
