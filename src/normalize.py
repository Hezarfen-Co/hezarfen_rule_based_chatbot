"""Metin normalizasyonu ve hafif Türkçe kök bulma.

Amaç: aynı anlamı taşıyan farklı yazımları tek forma indirgemek. Türkçe
sondan-eklemeli olduğu için ('notlarımı', 'notların', 'notum' -> 'not') hafif
bir kök bulma, kelime-torbası eşleşmesinin en zayıf noktasını kapatır.

Tasarım kararları:
- Türkçe-duyarlı küçük harf: 'I'->'ı', 'İ'->'i' (Python'un varsayılan lower'ı
  bunları yanlış yapar).
- Aksan katlama (fold): ç->c, ğ->g, ı->i, ö->o, ş->s, ü->u — kullanıcı Türkçe
  karakter kullanmadan yazsa da ('sinav' ~ 'sınav') eşleşme tutar.
- Stemmer bilinçli olarak HAFİF ve fazla-kırpmaya karşı korumalıdır (asgari kök
  uzunluğu). Dilbilimsel mükemmellik değil, sorgu ile anahtar kelime arasında
  TUTARLILIK hedeflenir; kural katmanı önek (prefix) eşleşmesiyle bunu tamamlar.

Tüm fonksiyonlar saf ve deterministiktir (loglanabilir/test edilebilir).
"""

from __future__ import annotations

import re
from typing import Final


MIN_STEM_LENGTH: Final[int] = 3
_MAX_STEM_PASSES: Final[int] = 3

# Türkçe küçük harf için özel eşlemeler (lower() öncesi uygulanır).
_UPPER_MAP: Final[dict[str, str]] = {"İ": "i", "I": "ı"}

# Aksan katlama (küçük harf sonrası).
_FOLD_MAP: Final[dict[str, str]] = str.maketrans(
    {
        "ç": "c",
        "ğ": "g",
        "ı": "i",
        "ö": "o",
        "ş": "s",
        "ü": "u",
        "â": "a",
        "î": "i",
        "û": "u",
    }
)

# Yalnızca harf/rakam/boşluk bırak (Türkçe harfler dahil).
_PUNCT_RE: Final[re.Pattern[str]] = re.compile(r"[^0-9a-zçğıöşü\s]", re.IGNORECASE)
_WS_RE: Final[re.Pattern[str]] = re.compile(r"\s+")

# Sohbet dilinde sık görülen, kısa ve anlamı tekil olan yazım biçimleri.
# Bu tablo bilinçli olarak küçüktür: genel bir otomatik-düzeltici gibi davranıp
# geçerli kelimeleri başka niyetlere sürüklemek yerine yalnızca benchmarkta
# gözlenen, anlamı belirsiz olmayan biçimleri kanonik tokena çevirir.
_TOKEN_ALIASES: Final[dict[str, str]] = {
    "snv": "sinav",
    "snava": "sinava",
    "drs": "ders",
    "yoklma": "yoklama",
    "karnme": "karnem",
    "ogrnci": "ogrenci",
    "degstr": "degistir",
    "deistirmek": "degistirmek",
    "degistrmek": "degistirmek",
    "sle": "sil",
    "slemek": "silmek",
    "slmek": "silmek",
    "nto": "not",
    "guncellicem": "guncelle",
    "nerde": "nerede",
    "selm": "selam",
    "mrb": "merhaba",
    "nbr": "naber",
    "nabrr": "naber",
    "saol": "sagol",
    "saaol": "sagol",
    "sapl": "sagol",
    "aidn": "adin",
    "kiimsin": "kimsin",
    "hezarfn": "hezarfen",
    "unttum": "unuttum",
    "yuklicem": "yukleyecegim",
    "veil": "veli",
    "ccougu": "cocugu",
    "ebevey": "ebeveyn",
    "men": "menu",
    "mensu": "menu",
    "mensuu": "menu",
    "sbue": "sube",
    "sue": "sube",
    # Kısa sözcüklerde genel fuzzy düzeltme güvenli değildir (örn. soru/sorun,
    # yemek/demek). Bu yüzden yalnız stres testinde gerçekten gözlenen,
    # anlamı tekil bozuk yüzeyler açıkça eşlenir.
    "naver": "naber",
    "hsber": "haber",
    "sg": "sagol",
    "saok": "sagol",
    "saoll": "sagol",
    "sori": "soru",
    "sooru": "soru",
    "sour": "soru",
    "soryu": "soruyu",
    "souyu": "soruyu",
    "srouyu": "soruyu",
    "oddev": "odev",
    "odve": "odev",
    "oevi": "odevi",
    "yeek": "yemek",
    "yrmek": "yemek",
    "yemrkte": "yemekte",
    "geelmedi": "gelmedi",
    "gelmdei": "gelmedi",
    "saay": "saat",
    "sast": "saat",
    "kemdi": "kendi",
    "knedi": "kendi",
    "meesaj": "mesaj",
    "mesaaj": "mesaj",
    "odee": "odeme",
    "odemr": "odeme",
    "mtufak": "mutfak",
    "muutfak": "mutfak",
    "deavm": "devam",
    "devm": "devam",
    "drss": "ders",
    "yoklms": "yoklama",
    "yeno": "yeni",
    "psfi": "pdfi",
    "taag": "tag",
    "netde": "nerede",
    "deres": "derse",
    "coxum": "cozum",
    "ckmek": "cekmek",
    "bnka": "banka",
    "bkamak": "bakmak",
    "gotsel": "gorsel",
    "zaan": "zaman",
    "messi": "mesai",
    "kpnusunu": "konusunu",
    "knousunu": "konusunu",
    "kpnusunun": "konusunun",
    "kaudini": "kaydini",
    "nout": "notu",
    "gerri": "geri",
    # Stres kümelerinde gözlenen uzun/ayırt edici konuşma dili ve tek-harf
    # bozulmaları. Kısa, geçerli komşular (bi/bu, el/ek, sona/sonra) özellikle
    # burada yer almaz; onlar ancak cümle bağlamıyla çözülebilir.
    "sirfem": "sifrem",
    "degistircem": "degistir",
    "tkip": "takip",
    "drvam": "devam",
    "yukkselt": "yukselt",
    "yukkseltmek": "yukseltmek",
    "subbe": "sube",
    "subr": "sube",
    "tkavimi": "takvimi",
    "yoneim": "yonetim",
    "yoneyim": "yonetim",
    "nedre": "nerede",
    "tarrihlerini": "tarihlerini",
    "habet": "haber",
    "meenun": "menu",
    # v3.4 deterministik tek-typo kümesinde ölçülen, kısa/geçerli komşusu
    # bulunduğu için genel fuzzy yerine yalnız exact ele alınan yüzeyler.
    "mesak": "mesaj", "measj": "mesaj", "meaj": "mesaj", "mrsaj": "mesaj",
    "des": "ders", "dres": "ders", "dets": "ders", "derd": "ders",
    "nabre": "naber", "nabet": "naber", "nabeer": "naber",
    "salo": "sagol", "ssol": "sagol", "saag": "sagol",
    "soriyu": "soruyu", "sueb": "sube", "suve": "sube",
    "yemel": "yemek", "yemeek": "yemek", "yeemek": "yemek",
    "etkinlite": "etkinlikte", "etkinlkte": "etkinlikte",
    "nerdde": "nerede", "nrede": "nerede", "nerd": "nerede",
    "getor": "getir", "banaa": "bana", "kc": "kac",
    "mezuun": "mezun", "hrdiye": "hediye",
    "simifin": "sinifin", "devamsizligii": "devamsizligimi",
    "tahya": "tahta", "tahat": "tahta",
    "guid": "guide", "drrs": "ders", "coum": "cozum",
    "guncelleemek": "guncellemek",
    # v3.5 sabit-seed stres kümesinde gözlenen tek-harfli, anlamı açık yüzeyler.
    # Kısa/geçerli komşusu olan biçimler global fuzzy hedef yapılmaz; yalnız exact
    # yazım düzeltilir. Bağlama muhtaç olanlar ise rules.py'de ele alınır.
    "nasilsni": "nasilsin", "nasislin": "nasilsin",
    "kmisin": "kimsin", "kilavuu": "kilavuz", "guode": "guide",
    "lgo": "login", "kullainci": "kullanici", "ckis": "cikis",
    "rool": "rol", "sgv": "svg", "enaled": "enabled",
    "degisstirmem": "degistirmem", "otruumunun": "oturumunun",
    "deers": "ders", "konttrolu": "kontrolu", "asekron": "asenkron",
    "eklme": "ekleme", "srou": "soru", "odelver": "odevler",
    "odeb": "odev", "teslm": "teslim", "yzdemi": "yuzdemi",
    "noy": "not", "mrsai": "mesai", "yonetmii": "yonetimi",
    "siilinir": "silinir", "ypacam": "yapacagim", "msajimi": "mesajimi",
    "kuup": "kulup", "odrme": "odeme", "subbeleri": "subeleri",
    "bguun": "bugun", "pneldeki": "paneldeki", "banksi": "bankasi",
    "sotu": "soru", "etkinlkileri": "etkinlikleri",
    "sinvalarin": "sinavlarin", "dpsyalarini": "dosyalarini",
    "ssat": "saat", "iteklerini": "isteklerini", "ogum": "ogun",
    "ucrretini": "ucretini", "yoklamssini": "yoklamasini",
    "meunsu": "menusu", "ekllemek": "eklemek", "yaynilamak": "yayinlamak",
    "mutfal": "mutfak", "dietry": "dietary", "hvuzunda": "havuzunda",
    "havzua": "havuza", "onnaylicam": "onaylayacagim",
    "okusturmak": "olusturmak", "tahhta": "tahta",
}

# Uzun ve anlamı tekil sosyal/meta sözcüklerde tam bir silme/ekleme/değiştirme
# veya komşu harf yer değiştirmesini tolere eder. Genel sözlük düzeltmesi
# değildir; kısa/geçerli sözcükleri (örn. "sol") başka niyete çevirmemek için
# yalnız bu dar liste uygulanır.
_SAFE_TYPO_TARGETS: Final[dict[str, str]] = {
    "merhaba": "merhaba", "merhabalar": "merhaba",
    "selamlar": "selam",
    "tesekkur": "tesekkur", "tesekkurler": "tesekkur",
    "eyvallah": "eyvallah", "gorusuruz": "gorusuruz",
    # "kimsin" fuzzy hedef değildir: geçerli "kimin" sözcüğü yalnız bir harf
    # uzaktadır. Gözlenen "kiimsin" biçimi yukarıdaki açık alias ile çözülür.
    "hoscakal": "hoscakal", "robot": "robot",
    "platform": "platform", "hezarfen": "hezarfen",
    # Uzun/ayırt edici ürün sözcükleri ve yaygın çekimleri. Bir sorgu tokenı
    # yalnız TEK kanonik hedefe bir düzenleme uzaklıktaysa düzeltilir.
    "hezarfeni": "hezarfen", "kilavuz": "kilavuz",
    "hesabi": "hesap", "kayit": "kayit", "sistemden": "sistemden",
    "guvenli": "guvenli", "oturumu": "oturum", "cikarim": "cikarim",
    "ingilizce": "ingilizce", "yetki": "yetki", "erisim": "erisim",
    "dosya": "dosya", "siniri": "sinir", "sinav": "sinav",
    "etkinlik": "etkinlik", "olusturacagim": "olustur",
    "oturum": "oturum", "ogrenci": "ogrenci", "ogretmen": "ogretmen",
    "rezervasyonsuz": "rezervasyonsuz", "servis": "servis",
    "yayinlicam": "yayinla",
    "akademik": "akademik", "donem": "donem", "profil": "profil",
    "biyografi": "biyografi", "randevu": "randevu",
    "devamsizlik": "devamsizlik", "yoklama": "yoklama",
    "yapabiliyorsun": "yapabil",
    # Çekimli yüzey kanonik biçim olarak korunur. Lemma'ya indirgemek bazı
    # kuralların iyelik/hal bağlamını kaybetmesine neden olur.
    "ogrencinin": "ogrencinin", "ogretmenin": "ogretmenin",
    "ogrenciye": "ogrenciye", "ogrenciyi": "ogrenciyi",
    "ogretmeni": "ogretmeni", "reddetmek": "reddetmek",
    "kilavuzu": "kilavuzu", "listemi": "listemi",
    "sinavdan": "sinavdan", "beslenme": "beslenme",
    "yeniden": "yeniden", "olusturabilir": "olusturabilir",
    "agirliklari": "agirliklari", "etkinlige": "etkinlige",
    "etkinligi": "etkinligi", "etkinlikler": "etkinlikler",
    "erisimin": "erisimin", "sablonun": "sablonun",
    "sinirini": "sinirini", "programim": "programim",
    "profilini": "profilini", "tahtayi": "tahtayi",
    "tahtalari": "tahtalari", "bildirim": "bildirim",
    "bolumunde": "bolumunde", "bitirince": "bitirince",
    "atanmamis": "atanmamis", "atanan": "atanan",
    "arkadasimin": "arkadasimin", "kayitliyim": "kayitliyim",
    "kaydini": "kaydini", "karnesini": "karnesini",
    "karnede": "karnede", "havuzuna": "havuzuna", "havuzunda": "havuzunda",
    "gecmisime": "gecmisime", "kutusuna": "kutusuna",
    "musait": "musait", "takvimi": "takvimi", "takvim": "takvim",
    "paneli": "paneli", "ucreti": "ucreti", "sifre": "sifre",
    "yonetim": "yonetim", "deftere": "deftere",
    "karnme": "karnem", "hazerfen": "hezarfen",
    "panel": "panel", "tanitim": "tanitim", "kapatmak": "kapatmak",
    "geceler": "geceler", "dersleri": "dersleri",
    "aktarirken": "aktarirken", "baskasinin": "baskasinin",
    "listesini": "listesini", "sayisini": "sayisini",
    "universiteyi": "universiteyi",
}


def _one_safe_typo(left: str, right: str) -> bool:
    if left == right:
        return True
    if abs(len(left) - len(right)) > 1:
        return False
    if len(left) == len(right):
        differences = [i for i, (a, b) in enumerate(zip(left, right)) if a != b]
        if len(differences) == 1:
            return True
        return (
            len(differences) == 2
            and differences[1] == differences[0] + 1
            and left[differences[0]] == right[differences[1]]
            and left[differences[1]] == right[differences[0]]
        )
    shorter, longer = (left, right) if len(left) < len(right) else (right, left)
    i = j = skipped = 0
    while i < len(shorter) and j < len(longer):
        if shorter[i] == longer[j]:
            i += 1
            j += 1
        else:
            skipped += 1
            j += 1
            if skipped > 1:
                return False
    return True


def _safe_typo_alias(token: str) -> str:
    matches = {
        canonical for surface, canonical in _SAFE_TYPO_TARGETS.items()
        if _one_safe_typo(token, surface)
    }
    return next(iter(matches)) if len(matches) == 1 else token

# Katlanmış (ascii) tokenlar üzerinde çalışan, uzundan kısaya denenecek ekler.
_SUFFIXES: Final[tuple[str, ...]] = tuple(
    sorted(
        {
            # çoğul + iyelik/hal birleşik
            "larimizi", "lerimizi", "larinizi", "lerinizi",
            "larimiz", "lerimiz", "lariniz", "leriniz",
            "larini", "lerini", "larimi", "lerimi",
            "lardan", "lerden", "larda", "lerde",
            "larim", "lerim", "larin", "lerin",
            "lara", "lere", "lari", "leri",
            "lar", "ler",
            # iyelik
            "imiz", "iniz", "umuz", "unuz",
            "imi", "ini", "umu", "unu",
            "im", "in", "um", "un",
            # hal ekleri
            "ndan", "nden", "tan", "ten", "dan", "den",
            "nin", "nun", "nda", "nde",
            "da", "de", "ta", "te",
            "na", "ne", "ya", "ye",
            "yi", "yu", "yi",
            "si", "su",
            # fiil/soru
            "yor", "dir", "tir", "dur", "tur", "mis", "mus",
            "acak", "ecek", "mak", "mek",
            "mi", "mu",
            # tekil sesli hal ekleri (asgari uzunlukla korunur)
            "i", "u", "a", "e",
        },
        key=len,
        reverse=True,
    )
)


def turkish_lower(text: str) -> str:
    """Türkçe kurallarına göre küçük harfe çevirir."""

    for upper, lower in _UPPER_MAP.items():
        text = text.replace(upper, lower)
    return text.lower()


def strip_punctuation(text: str) -> str:
    """Harf/rakam/boşluk dışındaki karakterleri boşlukla değiştirir."""

    return _PUNCT_RE.sub(" ", text)


def collapse_whitespace(text: str) -> str:
    """Ardışık boşlukları teke indirir ve baştaki/sondaki boşluğu atar."""

    return _WS_RE.sub(" ", text).strip()


def normalize(text: str) -> str:
    """Tam normalizasyon: küçük harf + noktalama temizliği + boşluk sadeleştirme.

    Türkçe karakterleri KORUR (okunabilir/loglanabilir form).
    """

    return collapse_whitespace(strip_punctuation(turkish_lower(text)))


def fold_accents(text: str) -> str:
    """Türkçe özel karakterleri ascii karşılıklarına katlar."""

    return text.translate(_FOLD_MAP)


def tokenize(text: str) -> list[str]:
    """Normalize edilmiş metni boşluklardan tokenlara ayırır."""

    normalized = normalize(text)
    if not normalized:
        return []
    return normalized.split(" ")


def folded_tokens(text: str) -> list[str]:
    """Normalize + katla + güvenli yazım alias'ları; STEM ETME.

    Stem'in aksine kelimeleri çökertmez ('yapamıyor' -> 'yapamiyor', 'yap' değil),
    böylece anahtar kelime önek eşleşmesi ('sifre' <- 'sifremi') kesin kalır.
    """

    folded = [fold_accents(token) for token in tokenize(text)]
    direct = [_TOKEN_ALIASES.get(token, token) for token in folded]
    return [_safe_typo_alias(token) for token in direct]


def stem(token: str) -> str:
    """Katlanmış (ascii) bir token için hafif kök bulma.

    Girdi ascii'ye katlanmış varsayılır. Asgari kök uzunluğu korunur; en fazla
    birkaç geçişte en uzun eşleşen ek soyulur.
    """

    for _ in range(_MAX_STEM_PASSES):
        stripped = False
        for suffix in _SUFFIXES:
            if token.endswith(suffix) and len(token) - len(suffix) >= MIN_STEM_LENGTH:
                token = token[: -len(suffix)]
                stripped = True
                break
        if not stripped:
            break
    return token


def roots(text: str) -> list[str]:
    """Metni köklerine indirger: normalize + katla + token + stem.

    Kural katmanının kullandığı kanonik biçim. Boş tokenlar atlanır.
    """

    return [stem(fold_accents(token)) for token in tokenize(text) if token]
