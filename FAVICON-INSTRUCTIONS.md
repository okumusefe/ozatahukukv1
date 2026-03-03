# Favicon (Logo) Ekleme Talimatları

## Gerekli Dosyalar

Sitenizin Google arama sonuçlarında ve tarayıcı sekmelerinde logo göstermesi için aşağıdaki dosyaları oluşturmanız gerekiyor:

### 1. favicon.ico (16x16 ve 32x32)
- Klasik favicon formatı
- Tarayıcı sekmeleri için

### 2. favicon-16x16.png
- 16x16 piksel PNG formatında logo

### 3. favicon-32x32.png
- 32x32 piksel PNG formatında logo

### 4. apple-touch-icon.png
- 180x180 piksel PNG formatında logo
- iOS cihazlar için

## Logo Dosyalarını Oluşturma

### Önerilen Yöntem 1: Online Favicon Generator
1. https://favicon.io/ veya https://realfavicongenerator.net/ sitesine gidin
2. Logonuzu (gönderdiğiniz görseli) yükleyin
3. Tüm gerekli boyutları otomatik oluşturun
4. İndirilen dosyaları proje klasörünüze kopyalayın

### Önerilen Yöntem 2: Manuel Oluşturma
1. Logo görselinizi bir görsel düzenleme programında açın (Photoshop, GIMP, vb.)
2. Her bir boyut için ayrı ayrı kaydedin:
   - 16x16 piksel → `favicon-16x16.png`
   - 32x32 piksel → `favicon-32x32.png`
   - 180x180 piksel → `apple-touch-icon.png`
3. .ico dosyası oluşturmak için online bir converter kullanın

## Dosyaları Nereye Koymalısınız

Tüm favicon dosyalarını proje kök dizinine koyun:
```
/Users/efeokumus/Desktop/ozatahukuk/
├── favicon.ico
├── favicon-16x16.png
├── favicon-32x32.png
├── apple-touch-icon.png
├── index.html
├── styles.css
└── ...
```

## HTML Kodları Eklendi ✅

Tüm HTML sayfalarına gerekli meta taglar zaten eklendi:
```html
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
<link rel="shortcut icon" href="favicon.ico">
```

## Test Etme

Dosyaları ekledikten sonra:
1. Tarayıcınızın cache'ini temizleyin
2. Siteyi yeniden yükleyin
3. Tarayıcı sekmesinde logoyu kontrol edin
4. Google Search Console'da "URL İnceleme" aracıyla test edin

## Google Arama Sonuçları İçin

Google'ın logoyu arama sonuçlarında göstermesi için:
1. Favicon dosyalarının doğru yüklendiğinden emin olun
2. Google Search Console'da sitenizi doğrulayın
3. Sitemap gönderin
4. Google'ın siteyi yeniden taramasını bekleyin (birkaç gün sürebilir)

## Hızlı Çözüm

En hızlı yol:
1. https://favicon.io/favicon-converter/ adresine gidin
2. Logonuzu yükleyin
3. "Download" butonuna tıklayın
4. İndirilen ZIP dosyasını açın
5. Tüm dosyaları `/Users/efeokumus/Desktop/ozatahukuk/` klasörüne kopyalayın
6. Siteyi yeniden deploy edin

✅ HTML kodları hazır, sadece logo dosyalarını eklemeniz yeterli!
