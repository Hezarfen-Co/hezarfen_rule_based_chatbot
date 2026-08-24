"""Aşama 5 birim testleri: kural katmanı eşleşme davranışı."""

import unittest

from src.rules import RuleMatch, match


class RuleMatchTests(unittest.TestCase):
    def test_greeting_fires(self) -> None:
        result = match("Merhaba")
        self.assertIsInstance(result, RuleMatch)
        self.assertEqual(result.intent, "greeting")

    def test_privacy_fires_on_other_students_data(self) -> None:
        # Güvenlik açısından kritik: başkasının verisi -> her zaman privacy.
        for q in [
            "Arkadaşımın notlarını göster",
            "Başka bir öğrencinin devamsızlığı kaç?",
            "Bir öğretmenin telefon numarasını verir misin?",
        ]:
            with self.subTest(q=q):
                result = match(q)
                self.assertIsNotNone(result)
                self.assertEqual(result.intent, "privacy_security")

    def test_account_problem_fires(self) -> None:
        result = match("Şifremi unuttum")
        self.assertEqual(result.intent, "account_access_problem")

    def test_login_not_confused_with_account(self) -> None:
        # 'giriş yapamıyorum' login DEĞİL, hesap sorunudur.
        result = match("Giriş yapamıyorum")
        self.assertIsNotNone(result)
        self.assertEqual(result.intent, "account_access_problem")

    def test_login_fires_on_clear_login(self) -> None:
        result = match("Nasıl giriş yaparım?")
        self.assertEqual(result.intent, "login_how")

    def test_exam_add_question_not_confused_with_exam_create(self) -> None:
        result = match("Sınava soru eklemek istiyorum")
        self.assertEqual(result.intent, "exam_add_question")

    def test_report_card_fires(self) -> None:
        result = match("Karnemi göster")
        self.assertEqual(result.intent, "report_card_view")

    def test_bare_note_crud_means_personal_notebook(self) -> None:
        cases = {
            "not silmek": "note_delete",
            "ben not silmek": "note_delete",
            "not değiştirmek": "note_edit",
            "notumu düzenlemek": "note_edit",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                result = match(query)
                self.assertIsNotNone(result)
                self.assertEqual(result.intent, expected)

    def test_qualified_grades_keep_their_own_flows(self) -> None:
        cases = {
            "sınav notunu silmek": "exam_grade_student",
            "sınav notunu güncelle": "exam_grade_student",
            "öğrenci notunu değiştirmek": "exam_grade_student",
            "ödev notunu kaldırmak": "homework_grade",
            "öğrencinin ödev puanını kaldırmak": "homework_grade",
            "not bantlarını değiştirmek": "school_settings",
            "not aralıklarını güncellemek": "school_settings",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                result = match(query)
                self.assertIsNotNone(result)
                self.assertEqual(result.intent, expected)

    def test_adversarial_colloquial_variants(self) -> None:
        cases = {
            "eski defter notunu temizlemek istiyorum": "note_delete",
            "kişisel notta değişiklik yapacağım": "note_edit",
            "not almak istiyorum": "note_create",
            "sınava geri döncem": "exam_rejoin_retake",
            "öğrenciyi puanlıcam": "exam_grade_student",
            "öğrenciyi öğretmen yapcam": "user_role_change",
            "randevuyu onaylıcam": "appointment_requests",
            "menü yayınlıcam": "meal_menu_manage",
            "soruyu onaylıcam": "question_approve",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                result = match(query)
                self.assertIsNotNone(result)
                self.assertEqual(result.intent, expected)

    def test_named_grade_and_negated_roster_are_high_precision_rules(self) -> None:
        cases = {
            "Ali'nin notunu düzelt": "exam_grade_student",
            "öğrenci silmek istiyorum": "course_remove_student",
            "bu öğrenciyi dersten çıkaracağım": "course_remove_student",
            "sınıf listesinden nasıl kaldırırım": "course_remove_student",
            "öğrencinin ders kaydını sonlandırmam lazım": "course_remove_student",
            "rosterdaki remove düğmesini bulamadım": "course_remove_student",
            "öğrencinin notunu değil kaydını sil": "course_remove_student",
            "öğrencinin notunu değil kaydını kaldır": "course_remove_student",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                result = match(query)
                self.assertIsNotNone(result)
                self.assertEqual(result.intent, expected)

    def test_system_troubleshooting_and_class_rules(self) -> None:
        cases = {
            "dosya yüklerken 413 alıyorum": "upload_problem",
            "dosya yükleyemiyorum": "upload_problem",
            "dosya yükleme isteği bozuk multipart dönüyor": "upload_problem",
            "chatbot bridge bağlı değil": "chatbot_service_problem",
            "Çelebi çalışmıyor": "chatbot_service_problem",
            "Çelebi bad_reply durumuna düştü": "chatbot_service_problem",
            "chatbot mesajı interrupted görünüyor": "chatbot_service_problem",
            "yeni bir şube oluşturmak istiyorum": "class_section_manage",
            "şubeye öğrenci eklemek istiyorum": "class_section_manage",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                result = match(query)
                self.assertIsNotNone(result)
                self.assertEqual(result.intent, expected)

    def test_full_system_gap_intents_have_high_precision_rules(self) -> None:
        cases = {
            "PDF'yi defter notuna içe aktar": "note_import_ocr",
            "not içe aktarırken metin çıkarılamadı": "note_import_ocr",
            "Deftere dosya ekli not eklemek istiyorum": "note_create",
            "kişisel notuma dosya eklemek istiyorum": "note_file_manage",
            "defter ekini indirmek istiyorum": "note_file_manage",
            "dersime müfredat konusu eklemek istiyorum": "course_subject_manage",
            "konu silerken 409 alıyorum": "course_subject_manage",
            "ders notuna onuncudan sonra dosya eklenir mi": "course_note_manage",
            "sınıfla paylaşılacak ders notu eklemek istiyorum": "course_note_manage",
            "ders notundaki pdf dosyasını değiştirmek istiyorum": "course_note_manage",
            "derse başka öğretmen atamak istiyorum": "course_teacher_manage",
            "atanmamış öğretmeni çıkarınca 404 aldım": "course_teacher_manage",
            "ödev teslimimi geri çekmek istiyorum": "homework_withdraw_submission",
            "notlandırılmış ödevimi geri çekemiyorum": "homework_withdraw_submission",
            "ödevin son teslim tarihini değiştirmek istiyorum": "homework_manage",
            "ödev kaydını tamamen silmek istiyorum": "homework_manage",
            "yemekte öğrenciyi servis edildi işaretle": "meal_service_mark",
            "gelmedi işareti ücreti geri alır mı": "meal_service_mark",
            "öğrencinin beslenme profilini güncelle": "meal_dietary_profile_manage",
            "mutfak notunu temizlemek istiyorum": "meal_dietary_profile_manage",
            "soru bankasına yeni şablon eklemek istiyorum": "question_bank_manage",
            "soru bankasındaki şablonu okul görünürlüğüne açmak istiyorum": "question_bank_manage",
            "bankadaki soruyu silince sınav kopyası ne olur": "question_bank_manage",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                result = match(query)
                self.assertIsNotNone(result)
                self.assertEqual(result.intent, expected)

    def test_stress_discovered_paraphrases_keep_specific_intents(self) -> None:
        cases = {
            "öğrenci notunu yeniden ayarlamak": "exam_grade_student",
            "sınav puanını yeniden ayarlamak istiyorum": "exam_grade_student",
            "öğrencinin notunu listeden çıkarmak istiyorum": "exam_grade_student",
            "ödev puanını yeniden ayarlamak": "homework_grade",
            "ödev notunu listeden çıkarmak": "homework_grade",
            "notumu yeniden ayarlamak istiyorum": "note_edit",
            "Defter notuma dosya ilave etmek istiyorum": "note_file_manage",
            "mesai kaydını listeden çıkarmak": "staff_work_manage",
            "randevu serisini listeden çıkarmak": "appointment_slot_open",
            "Oturum tanımlamak nasıl yapılır": "lesson_session_add",
            "ders notundaki PDF dosyasını güncellemek": "course_note_manage",
            "Dersime yeni bir müfredat konusu yeni kayıt girmek istiyorum": "course_subject_manage",
            "Ödev teslimini hangi sayfadan yaparım": "homework_submit",
            "İngilizce arayüze geçmek yapmam gerekiyor": "language_theme",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                result = match(query)
                self.assertIsNotNone(result)
                self.assertEqual(result.intent, expected)

    def test_stress_discovered_natural_variants_keep_specific_intent(self) -> None:
        cases = {
            "Sınav ağırlıkları nota nasıl yansıyor": "weighted_average_info",
            "Dersime sınav eklemek istiyorum": "exam_create",
            "açık mod sınava başlangıç tarihi yazabilir miyim": "exam_create",
            "kapalı mesaiyi kaldırmak": "staff_work_manage",
            "bir öğretmenin mesaisini düzeltmek istiyorum": "staff_work_manage",
            "Derse kayıt yapma işlemi nasıl": "course_enroll_student",
            "Dersleri döneme göre süzebilir miyim": "course_view",
            "Beyaz tahta tanımlamak istiyorum": "board_create",
            "öğretmen olarak öğrencinin devamsızlığını sorgulamak istiyorum": "student_attendance_lookup",
            "not silmek. Bu işlem hangi ekrandan yapılıyor?": "note_delete",
            "Ana paneldeki özet nedir": "today_info",
            "Ama panel neyi gösterir": "today_info",
            "Hangi işlerde bana destek olursun": "help_capabilities",
            "üst rol her öğrenci işlemini yapabilir mi": "roles_permissions",
            "tahtayı kaldırmak çizim geçmişini de yok eder mi": "board_create",
            "Bı platform ne için var": "platform_info",
            "Sen nr yapabiliyorsun tam olarak": "help_capabilities",
            "el limitim dolu olduğu için yeni dosya yüklenmiyor": "upload_problem",
            "om birinci eki ekleyemiyorum": "upload_problem",
            "Notumu sınavdan sona nereden görürüm": "exam_finish_result",
            "Bir etkinlikte vat demek istiyorum": "event_attendance_mark",
            "PDF'yi Deftere ie aktarabilir miyim": "note_import_ocr",
            "şablonun komusu silinirse ne olur": "question_bank_manage",
            "randevu serisini sikmek neden reddediliyor": "appointment_slot_open",
            "Ders detay sayfasına nasıl giderim": "course_view",
            "Derse yeni bir ders saati eklemek istiyorum": "lesson_session_add",
            "Kaldığım sorudan devam edebilir miyim": "exam_rejoin_retake",
            "yeni şube oluştururken kapasiteyi hangi sayfada giriyorum": "class_section_manage",
            "zil menüsündeki tüm uyarıları temizlemek istiyorum": "notification_settings_info",
            "Hesap settings ayrı bir sayfa mı": "personal_settings",
            "Öde listemi görmek istiyorum": "homework_view",
            "Nabet dostum": "smalltalk",
            "odak ve ödev istatistiklerim profilimde hangi sayfada": "profile_view",
            "ders kaydını listeden çıkarmak": "course_remove_student",
            "ders notundaki PDF dosyasını düzenlemek": "course_note_manage",
            "Dersime sınav ilave etmek": "exam_create",
            "sınav notunu listeden çıkarmak": "exam_grade_student",
            "sınav puanını düzenlemek": "exam_grade_student",
            "öğrenci puanını listeden çıkar": "exam_grade_student",
            "var olan ödevi güncellemek": "homework_manage",
            "Kapalı mesai kaydını güncellemek": "staff_work_manage",
            "Şub listesi hangi sayfada": "branches_info",
            "soru bankasına şablon dahil etmek": "question_bank_manage",
            "soru bankasına yeni bir şablon ilave etmek": "question_bank_manage",
            "Drrs notu dosyalarını indir": "course_materials_info",
            "yemek rezervasyonumu listeden çıkarmak": "meal_book",
            "Öğüne yeemek ilave etmek": "meal_menu_manage",
            "Zor soruya çöüm göndermek": "question_solve",
            "tahtayı listeden çıkarmak": "board_create",
            "Yeni çizim tahtası oluştur": "board_create",
            "Deftere dosya ekli not ilave etmek": "note_create",
            "403 rol mü ders yetkisi mi demek": "access_denied_help",
            "yardim Sinav sırasında öğrencileri anlık takip etmek istiyorum": "exam_live_monitor",
            "kisa bir soru Ogretmen olarak ogrencinin devamsizligini sorgulamak istiyorum": "student_attendance_lookup",
            "dersime yeni bir müfredat konusu ellemek istiyorum": "course_subject_manage",
            "Devan yüzdemi nereden görürüm": "attendance_view",
            "öğrenciyi etkinlikte vsr olarak işaretlemek istiyorum": "event_attendance_mark",
            "soru bankasındaki şalonu okul görünürlüğüne açmak istiyorum": "question_bank_manage",
            "şablonun konusu silinirse nr olur": "question_bank_manage",
            "banla sorusunu silince sınavdaki kopyası da silinir mi": "question_bank_manage",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                result = match(query)
                self.assertIsNotNone(result)
                self.assertEqual(result.intent, expected)

    def test_full_system_gap_rules_do_not_steal_neighbour_intents(self) -> None:
        cases = {
            "not almak istiyorum": "note_create",
            "dosya yükleyemiyorum": "upload_problem",
            "öğretmenin yüklediği ders pdf nerede": "course_materials_info",
            "ödevimi teslim etmek istiyorum": "homework_submit",
            "ödevi notlandırmak istiyorum": "homework_grade",
            "yemek menüsü nerede": "meal_view",
            "yemek rezervasyonu yapmak istiyorum": "meal_book",
            "ödeme listemi görmek istiyorum": "fees_info",
            "soru bankası ne işe yarar": "question_bank_info",
            "sınava soru eklemek istiyorum": "exam_add_question",
            "soru havuzuna soru sormak istiyorum": "question_ask",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                result = match(query)
                self.assertIsNotNone(result)
                self.assertEqual(result.intent, expected)

    def test_curated_collision_regressions_choose_the_semantic_intent(self) -> None:
        cases = {
            "Etkinliğe katıldığımı nasıl bildiririm?": "event_attendance_mark",
            "Okulun şubeleri hangi sayfada?": "branches_info",
            "mesaj bildirimine basınca ne oluyor": "notification_settings_info",
            "isteğim başarısız oldu hata metnini nereye yazayım": "technical_error_help",
            "oturum süresi dolduğu için 401 alıyorum": "session_info",
            "oturumum bitince gelen 401 için yeniden mi giriş yapmalıyım": "session_info",
            "sınav sorusu değiştirirken attempts started hatası aldım": "exam_add_question",
            "ders oturumu oluştururken hata veriyor": "lesson_session_add",
            "şubeden öğrenciyi çıkarınca ders kayıtları ne olur": "class_section_manage",
            "sınıf grubu açmak ders açmakla aynı mı": "class_section_manage",
            "veliyim çocuğumun ödeme ekstresini nereden açarım": "fees_info",
            "notlandırılmış ödev dosyasını neden silemiyorum": "homework_submit",
            "kendime mesaj gönderemiyorum neden": "messages_use",
            "öğrenci kendi etkinlik yoklamasını neden işaretleyemiyor": "event_attendance_mark",
            "tahtayı kapatırsam yeniden açabilir miyim": "board_create",
            "not verilmemiş sınav neden karnede hiç görünmüyor": "report_card_view",
            "soru havuzunda pending soruyu kim görebilir": "question_approve",
            "ayarlar görünüm kısmında vurgu rengini değiştireceğim": "personal_settings",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                result = match(query)
                self.assertIsNotNone(result)
                self.assertEqual(result.intent, expected)

    def test_returns_none_for_out_of_scope(self) -> None:
        for q in ["Bugün hava nasıl olacak?", "Bana bir fıkra anlat", "2 artı 2 kaç eder?"]:
            with self.subTest(q=q):
                self.assertIsNone(match(q))

    def test_ambiguous_defers_to_none(self) -> None:
        # Eşit güçte iki intent (course_create: yeni+ders ; roll_call: yoklama+al)
        # -> belirsizlik -> karar verme.
        self.assertIsNone(match("yeni ders oluştur ve yoklama al"))

    def test_empty_query_returns_none(self) -> None:
        self.assertIsNone(match("   "))

    def test_match_has_reason(self) -> None:
        result = match("Karnemi göster")
        self.assertIn("karne", result.reason)


if __name__ == "__main__":
    unittest.main()
