# Çelebi Sentetik Stres Benchmarkı Sonuçları

> [!IMPORTANT]
> Bu küme bağımsız bir **gold benchmark değildir**. Yalnız insan etiketli sorulardan türetilen tanısal/metamorfik stres testidir; katalog örnekleri değerlendirme seed'i değildir.

- Generator: `stress-v3.5.0`
- Toplam vaka: **10000**
- Uygulama-içi: **9000**
- OOS: **1000**
- PASS: **9984**
- FAIL: **16**
- Soft FAIL: **4**
- Hard FAIL: **12**
- Tam sözleşme başarı oranı: **99.8%**

Tam Engine payload'ı `python stress_benchmark.py` çalıştırıldığında yerelde `data/stress_benchmark_results.jsonl` olarak üretilir (büyük ve yeniden üretilebilir olduğu için Git'e alınmaz). Markdown parçaları inceleme metadata'sı ile kullanıcıya görünen soru/cevabı gösterir; iç içe makine payload'ını göstermez.

## Kaynak bazında

| Değer | Toplam | PASS | FAIL | Başarı |
|---|---:|---:|---:|---:|
| benchmark | 9553 | 9539 | 14 | 99.9% |
| near_oos | 447 | 445 | 2 | 99.6% |

## Beklenen outcome bazında

| Değer | Toplam | PASS | FAIL | Başarı |
|---|---:|---:|---:|---:|
| allow | 5628 | 5620 | 8 | 99.9% |
| deny | 3628 | 3624 | 4 | 99.9% |
| fallback | 744 | 740 | 4 | 99.5% |

## Gerçek outcome bazında

| Değer | Toplam | PASS | FAIL | Başarı |
|---|---:|---:|---:|---:|
| allow | 5621 | 5620 | 1 | 100.0% |
| clarify | 7 | 0 | 7 | 0.0% |
| deny | 3624 | 3624 | 0 | 100.0% |
| fallback | 748 | 740 | 8 | 98.9% |

## Varyasyon ailesi bazında

| Değer | Toplam | PASS | FAIL | Başarı |
|---|---:|---:|---:|---:|
| semantic_paraphrase | 1240 | 1240 | 0 | 100.0% |
| sentence_form | 1383 | 1383 | 0 | 100.0% |
| ui_label_tr_en | 823 | 823 | 0 | 100.0% |
| role_context | 1413 | 1413 | 0 | 100.0% |
| turkish_ascii | 1290 | 1290 | 0 | 100.0% |
| conversational_filler | 1202 | 1202 | 0 | 100.0% |
| punctuation_case | 732 | 732 | 0 | 100.0% |
| single_typo | 955 | 941 | 14 | 98.5% |
| state_error | 332 | 332 | 0 | 100.0% |
| compound | 630 | 628 | 2 | 99.7% |

## Beklenen intent bazında

| Değer | Toplam | PASS | FAIL | Başarı |
|---|---:|---:|---:|---:|
| access_denied_help | 92 | 92 | 0 | 100.0% |
| account_access_problem | 92 | 92 | 0 | 100.0% |
| appointment_book | 91 | 91 | 0 | 100.0% |
| appointment_requests | 91 | 91 | 0 | 100.0% |
| appointment_slot_open | 91 | 91 | 0 | 100.0% |
| attendance_rate_info | 92 | 92 | 0 | 100.0% |
| attendance_view | 92 | 92 | 0 | 100.0% |
| board_create | 91 | 91 | 0 | 100.0% |
| board_view | 91 | 91 | 0 | 100.0% |
| bot_identity | 92 | 91 | 1 | 98.9% |
| branches_info | 92 | 92 | 0 | 100.0% |
| calendar_info | 92 | 92 | 0 | 100.0% |
| chatbot_service_problem | 92 | 92 | 0 | 100.0% |
| class_section_manage | 92 | 92 | 0 | 100.0% |
| course_create | 92 | 89 | 3 | 96.7% |
| course_enroll_student | 92 | 92 | 0 | 100.0% |
| course_materials_info | 91 | 91 | 0 | 100.0% |
| course_note_manage | 92 | 92 | 0 | 100.0% |
| course_remove_student | 92 | 92 | 0 | 100.0% |
| course_subject_manage | 92 | 92 | 0 | 100.0% |
| course_teacher_manage | 92 | 92 | 0 | 100.0% |
| course_view | 92 | 92 | 0 | 100.0% |
| event_attendance_mark | 92 | 92 | 0 | 100.0% |
| event_create | 92 | 92 | 0 | 100.0% |
| event_view | 92 | 92 | 0 | 100.0% |
| exam_add_question | 92 | 92 | 0 | 100.0% |
| exam_create | 92 | 92 | 0 | 100.0% |
| exam_enter_room | 92 | 92 | 0 | 100.0% |
| exam_finish_result | 92 | 92 | 0 | 100.0% |
| exam_grade_student | 92 | 92 | 0 | 100.0% |
| exam_live_monitor | 92 | 92 | 0 | 100.0% |
| exam_modes_info | 92 | 91 | 1 | 98.9% |
| exam_rejoin_retake | 92 | 92 | 0 | 100.0% |
| exam_save_answer | 92 | 92 | 0 | 100.0% |
| exam_schedule_info | 91 | 91 | 0 | 100.0% |
| farewell | 92 | 92 | 0 | 100.0% |
| fees_info | 92 | 92 | 0 | 100.0% |
| fees_manage | 92 | 92 | 0 | 100.0% |
| greeting | 92 | 92 | 0 | 100.0% |
| guide_info | 92 | 92 | 0 | 100.0% |
| help_capabilities | 92 | 92 | 0 | 100.0% |
| homework_assign | 92 | 92 | 0 | 100.0% |
| homework_grade | 92 | 92 | 0 | 100.0% |
| homework_manage | 92 | 92 | 0 | 100.0% |
| homework_submit | 92 | 92 | 0 | 100.0% |
| homework_view | 92 | 92 | 0 | 100.0% |
| homework_withdraw_submission | 92 | 92 | 0 | 100.0% |
| language_theme | 92 | 92 | 0 | 100.0% |
| lesson_session_add | 92 | 92 | 0 | 100.0% |
| login_how | 92 | 92 | 0 | 100.0% |
| logout_how | 92 | 92 | 0 | 100.0% |
| meal_book | 91 | 91 | 0 | 100.0% |
| meal_credit_manage | 91 | 91 | 0 | 100.0% |
| meal_dietary_profile_manage | 91 | 91 | 0 | 100.0% |
| meal_menu_manage | 91 | 91 | 0 | 100.0% |
| meal_service_mark | 91 | 91 | 0 | 100.0% |
| meal_view | 91 | 91 | 0 | 100.0% |
| messages_use | 92 | 92 | 0 | 100.0% |
| nav_overview | 92 | 92 | 0 | 100.0% |
| navigation_help | 92 | 92 | 0 | 100.0% |
| note_create | 92 | 92 | 0 | 100.0% |
| note_delete | 92 | 92 | 0 | 100.0% |
| note_edit | 92 | 92 | 0 | 100.0% |
| note_file_manage | 92 | 92 | 0 | 100.0% |
| note_import_ocr | 92 | 91 | 1 | 98.9% |
| notification_settings_info | 92 | 92 | 0 | 100.0% |
| oos | 1000 | 996 | 4 | 99.6% |
| parent_info | 92 | 92 | 0 | 100.0% |
| personal_settings | 92 | 92 | 0 | 100.0% |
| platform_info | 92 | 90 | 2 | 97.8% |
| pomodoro_use | 92 | 92 | 0 | 100.0% |
| privacy_security | 92 | 92 | 0 | 100.0% |
| profile_edit | 92 | 92 | 0 | 100.0% |
| profile_view | 92 | 92 | 0 | 100.0% |
| question_approve | 91 | 91 | 0 | 100.0% |
| question_ask | 91 | 91 | 0 | 100.0% |
| question_bank_info | 92 | 92 | 0 | 100.0% |
| question_bank_manage | 92 | 92 | 0 | 100.0% |
| question_solve | 91 | 91 | 0 | 100.0% |
| register_how | 92 | 92 | 0 | 100.0% |
| report_card_view | 92 | 92 | 0 | 100.0% |
| roles_permissions | 92 | 92 | 0 | 100.0% |
| roll_call | 92 | 90 | 2 | 97.8% |
| school_settings | 92 | 92 | 0 | 100.0% |
| session_info | 92 | 92 | 0 | 100.0% |
| smalltalk | 92 | 92 | 0 | 100.0% |
| staff_work_manage | 92 | 92 | 0 | 100.0% |
| student_attendance_lookup | 92 | 92 | 0 | 100.0% |
| student_marks_lookup | 92 | 92 | 0 | 100.0% |
| student_pomodoro_lookup | 92 | 92 | 0 | 100.0% |
| study_club_info | 92 | 92 | 0 | 100.0% |
| technical_error_help | 92 | 92 | 0 | 100.0% |
| term_manage | 92 | 92 | 0 | 100.0% |
| thanks | 92 | 92 | 0 | 100.0% |
| today_info | 92 | 92 | 0 | 100.0% |
| upload_problem | 92 | 90 | 2 | 97.8% |
| user_role_change | 92 | 92 | 0 | 100.0% |
| weighted_average_info | 92 | 92 | 0 | 100.0% |
| work_checkin_out | 92 | 92 | 0 | 100.0% |

## Rol bazında

| Değer | Toplam | PASS | FAIL | Başarı |
|---|---:|---:|---:|---:|
| Ziyaretçi | 2243 | 2240 | 3 | 99.9% |
| Veli | 1523 | 1522 | 1 | 99.9% |
| Öğrenci | 1697 | 1694 | 3 | 99.8% |
| Öğretmen | 1421 | 1418 | 3 | 99.8% |
| Yönetici | 1523 | 1523 | 0 | 100.0% |
| ADMIN | 1593 | 1587 | 6 | 99.6% |

## OOS türü ve FAIL şiddeti

`soft`, yalnız katı fallback sözleşmesi yerine intent/action/route üretmeden netleştirme isteyen semantik olarak güvenli yanıttır; sözleşme sonucu yine FAIL kalır. Diğer bütün sözleşme ihlalleri `hard` sayılır.

| OOS türü | Toplam | PASS | Soft FAIL | Hard FAIL | Sözleşme başarısı |
|---|---:|---:|---:|---:|---:|
| `fallback` | 744 | 740 | 4 | 0 | 99.5% |
| `action-boundary` | 112 | 112 | 0 | 0 | 100.0% |
| `data-boundary` | 144 | 144 | 0 | 0 | 100.0% |

## Hata kümeleri

| Failure reason | Vaka |
|---|---:|
| `response_id_mismatch` | 16 |
| `outcome_mismatch` | 15 |
| `meta_outcome_mismatch` | 15 |
| `reason_code_mismatch` | 15 |
| `intent_mismatch` | 12 |
| `meta_action_id_mismatch` | 12 |
| `fallback_mismatch` | 12 |
| `meta_route_key_mismatch` | 6 |
| `navigation_route_mismatch` | 4 |
| `auth_action_mismatch` | 4 |

## Okunabilir rapor parçaları

- [part-0001.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0001.md)
- [part-0002.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0002.md)
- [part-0003.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0003.md)
- [part-0004.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0004.md)
- [part-0005.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0005.md)
- [part-0006.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0006.md)
- [part-0007.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0007.md)
- [part-0008.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0008.md)
- [part-0009.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0009.md)
- [part-0010.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0010.md)
- [part-0011.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0011.md)
- [part-0012.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0012.md)
- [part-0013.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0013.md)
- [part-0014.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0014.md)
- [part-0015.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0015.md)
- [part-0016.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0016.md)
- [part-0017.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0017.md)
- [part-0018.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0018.md)
- [part-0019.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0019.md)
- [part-0020.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0020.md)
- [part-0021.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0021.md)
- [part-0022.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0022.md)
- [part-0023.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0023.md)
- [part-0024.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0024.md)
- [part-0025.md](STRES_BENCHMARK_SONUCLARI_parcalar/part-0025.md)

## İlk uygulama-içi FAIL örnekleri

| ID | Rol | Soru | Nedenler |
|---|---|---|---|
| `stress-4469cb2a075085c27604` | ADMIN | senin adım ne | intent_mismatch, outcome_mismatch, meta_outcome_mismatch, meta_action_id_mismatch, response_id_mismatch, meta_route_key_mismatch, reason_code_mismatch |
| `stress-ac5272f2d251aed7dffe` | ADMIN | acaba, Hazerfen tam olarak nr hakkında bilgi verir misin?? | intent_mismatch, outcome_mismatch, meta_outcome_mismatch, meta_action_id_mismatch, response_id_mismatch, fallback_mismatch, navigation_route_mismatch, meta_route_key_mismatch, reason_code_mismatch |
| `stress-1e768ff4664a9a4680dd` | ADMIN | Hazerfen tam olarak n | intent_mismatch, outcome_mismatch, meta_outcome_mismatch, meta_action_id_mismatch, response_id_mismatch, fallback_mismatch, navigation_route_mismatch, meta_route_key_mismatch, reason_code_mismatch |
| `stress-12eedc750344fae3a033` | Veli | bo dosyayı ek olarak kabul etmiyor | intent_mismatch, outcome_mismatch, meta_outcome_mismatch, meta_action_id_mismatch, response_id_mismatch, fallback_mismatch, reason_code_mismatch |
| `stress-b7ecb09283b63f03eadb` | Öğrenci | on birinci eli ekleyemiyorum | intent_mismatch, outcome_mismatch, meta_outcome_mismatch, meta_action_id_mismatch, response_id_mismatch, fallback_mismatch, reason_code_mismatch |
| `stress-b40acaff820a86744b97` | Öğretmen | ds açcam | intent_mismatch, outcome_mismatch, meta_outcome_mismatch, meta_action_id_mismatch, response_id_mismatch, fallback_mismatch, navigation_route_mismatch, meta_route_key_mismatch, reason_code_mismatch |
| `stress-707575efc479a5bf68d9` | Öğrenci | dsr açcam | intent_mismatch, outcome_mismatch, meta_outcome_mismatch, meta_action_id_mismatch, response_id_mismatch, auth_action_mismatch, fallback_mismatch, reason_code_mismatch |
| `stress-12969ae5abe42d4fbc11` | Öğrenci | müsaitsen, Amacım şu: ds açcam. Bana işlem yolunu anlatır mısın?? | intent_mismatch, outcome_mismatch, meta_outcome_mismatch, meta_action_id_mismatch, response_id_mismatch, auth_action_mismatch, fallback_mismatch, reason_code_mismatch |
| `stress-e5cfb7afcd14a76ea3a1` | Öğretmen | yoklma ak | intent_mismatch, outcome_mismatch, meta_outcome_mismatch, meta_action_id_mismatch, response_id_mismatch, navigation_route_mismatch, meta_route_key_mismatch, reason_code_mismatch |
| `stress-46c6aeaa5a52511a04b4` | Ziyaretçi | yolma al | intent_mismatch, outcome_mismatch, meta_outcome_mismatch, meta_action_id_mismatch, response_id_mismatch, auth_action_mismatch, fallback_mismatch, reason_code_mismatch |
| `stress-79bb2eb737bf653a1475` | ADMIN | Açık md sürekli mi açık kalıyor | intent_mismatch, meta_action_id_mismatch, response_id_mismatch, meta_route_key_mismatch |
| `stress-9aeaa66c02ebe62da731` | Ziyaretçi | taranmış PSF dosyasında OCR yapılıyor mu | intent_mismatch, outcome_mismatch, meta_outcome_mismatch, meta_action_id_mismatch, response_id_mismatch, auth_action_mismatch, reason_code_mismatch |

## İlk OOS FAIL örnekleri

| ID | Tür | Şiddet | Rol | Soru | Nedenler |
|---|---|---|---|---|---|
| `stress-2176c8b0638619da0da8` | `fallback` | `soft` | Öğretmen | Bana bir şiri yazar mısın | outcome_mismatch, meta_outcome_mismatch, response_id_mismatch, fallback_mismatch, reason_code_mismatch |
| `stress-aaff54087ca7c3dbd65d` | `fallback` | `soft` | Ziyaretçi | 2 atı 2 kaç eder | outcome_mismatch, meta_outcome_mismatch, response_id_mismatch, fallback_mismatch, reason_code_mismatch |
| `stress-a74ac2dc68281ae3015f` | `fallback` | `soft` | ADMIN | Beedn dersinde ne yapacağız | outcome_mismatch, meta_outcome_mismatch, response_id_mismatch, fallback_mismatch, reason_code_mismatch |
| `stress-c5f16a1bfd77cf6bc306` | `fallback` | `soft` | ADMIN | Sınav stesiyle nasıl başa çıkarım | outcome_mismatch, meta_outcome_mismatch, response_id_mismatch, fallback_mismatch, reason_code_mismatch |
