# Otomatik IPTV Kanal Listesi Güncelleme Aracı

Türkçe IPTV/M3U listelerini **sırasını ve kanal bilgilerini bozmadan** onaran,
çalışmayan yayın linklerini [iptv-org](https://github.com/iptv-org/iptv)
kaynağından gelen çalışan linklerle değiştiren küçük bir araç.

> Bu repo **yalnızca aracı** içerir. İçinde hazır bir yayın listesi / kanal
> linki yoktur. Kullanıcı kendi M3U dosyasını aracın yanına koyar.

## Ne yapıyor?

1. Yanındaki, adında `guncel` geçen playlist dosyasını bulur.
2. Dosyadaki her kanalın URL'sini test eder.
3. Çalışmayanlar için iptv-org API'sinden aday linkler çeker ve onları da test eder.
4. Sadece **URL satırını** değiştirir; `#EXTINF`, kanal adı, logo, grup,
   `tvg-id` ve kanal sırası aynen kalır.
5. `yedek/` klasörüne yedek, `raporlar/` klasörüne CSV rapor yazar.

Varsayılan olarak kanal **silmez**; alternatif bulamazsa kanalı olduğu gibi
bırakır ve raporda belirtir. `--remove-dead` ile alternatifsizleri çıkarabilirsiniz.

## Yanlış eşleşme koruması

- Önce **tam `tvg-id`** aranır: `ShowTV.tr@SD` → `ShowTV.tr`.
- Ülke kodlu ID'ler sayesinde başka ülkedeki benzer isimli kanallarla
  karışmaz (`ShowTV.tr` ≠ `ShowTV.pr`).
- Aynı kanalın farklı feed'i varsa **aynı `@feed`** (SD/HD) tercih edilir;
  yoksa diğer feed'ler denenir.
- Fuzzy / substring / benzer isim araması **yoktur**.
- İsim eşleşmesi varsayılan olarak **kapalıdır**. `--name-match` verilse bile
  yalnızca aynı ülkede, tam normalize isimle ve isim tek bir kanala aitse çalışır.
- Elle tanımlanmış `ALIASES` dışında otomatik alias kurulmaz.

## Hızlı başlangıç (Windows)

1. Bu repoyu indirin veya zip'ten çıkarın.
2. Kendi playlist'inizi aracın yanına koyun ve adında `guncel` geçsin:
   - `guncel-kanallar.m3u`
   - `benim-guncel-listem.m3u`
3. `IPTV-GUNCELLE.bat` dosyasına **çift tıklayın**.
4. İlk çalışmada `requests` paketi yoksa otomatik kurulur.
5. Sonraki güncellemeler için yine aynı `.bat` dosyasına çift tıklayın.

Playlist'e değil, **`IPTV-GUNCELLE.bat`** dosyasına çift tıklayın.

Adında `guncel` geçen birden fazla dosya varsa ilk çalışmada hangisinin
güncelleneceğini sorar ve seçimi `playlist.txt` dosyasına kaydeder. Hiç
`guncel` dosyası yoksa hiçbir şeye dokunmadan uyarı verip kapanır.

### Python ile

```bash
pip install requests
python kanal_guncelle.py
```

## Kaynak

- `https://iptv-org.github.io/api/streams.json`
- `https://iptv-org.github.io/api/channels.json`
- `https://iptv-org.github.io/iptv/countries/tr.m3u`

Kaynak verisi `%LOCALAPPDATA%\benimliste-guncelle\cache` altında önbelleğe alınır.

## Seçenekler

| Seçenek | Açıklama |
|---|---|
| `--dry-run` | Hiçbir dosyaya yazmaz, sadece raporlar |
| `--scan-only` | Sadece tarar, link değiştirmez |
| `--only METIN` | Adında/ID'sinde metin geçen kanallar |
| `--limit N` | İlk N kanal (test için) |
| `--workers N` | Paralel kanal sayısı (varsayılan 8) |
| `--timeout S` | Okuma zaman aşımı (varsayılan 12 sn) |
| `--retries N` | Başarısız istekte tekrar sayısı (varsayılan 2) |
| `--confirm N` | Orijinal link başarısızsa kaç kez daha deneneceği (varsayılan 3) |
| `--deep` | İlk video segmentini de doğrular |
| `--siblings` / `--no-siblings` | Kalite varyantlarını dene (varsayılan: açık) |
| `--max-candidates N` | Kanal başına en fazla aday link (varsayılan 10) |
| `--name-match` | Aynı ülkede tam isim eşleşmesi dene (varsayılan: kapalı) |
| `--refresh-different` | Çalışan ama kaynakta URL'si değişmiş kanalları da günceller |
| `--remove-dead` | Alternatifi bulunamayanları listeden çıkarır |
| `--offline` | Kaynağı indirmeden son önbelleği kullanır |
| `--no-header` | `#Güncelleme:` tarihini değiştirmez |
| `--no-backup` | Yedek oluşturmaz |
| `--report DOSYA` | Rapor yolunu değiştirir |

## Geliştirme

```bash
python -m py_compile kanal_guncelle.py
python tests/test_matching.py
```

## Yasal uyarı

Bu araç yayın barındırmaz, yayınları yeniden dağıtmaz ve hiçbir yayın
sağlayıcısıyla bağlantılı değildir. Yalnızca kullanıcının kendi playlist
dosyasındaki URL'leri test eder ve kaynak veritabanından alternatif arar.

Kullanıcı, kendi playlist'indeki linklerin kullanım haklarından ve yerel
mevzuata uygunluğundan sorumludur. Ücretli, geo-blocked veya yetkisiz
yayınların linklerini halka açık şekilde dağıtmayın. Hak sahibi talebi
durumunda ilgili içerik kaldırılmalıdır.

## Lisans

MIT — bkz. [LICENSE](LICENSE).
