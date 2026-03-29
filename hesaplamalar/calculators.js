/**
 * Özata Hukuk - Hesaplama Araçları JavaScript
 * Tüm hesaplama fonksiyonları burada toplanmıştır
 */

// Para formatı yardımcı fonksiyonu
function formatPara(tutar) {
    return tutar.toLocaleString('tr-TR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' TL';
}

// Kıdem Tazminatı Hesaplama
function hesaplaKidem() {
    const brut = parseFloat(document.getElementById('kidem-brut')?.value) || 0;
    const yil = parseInt(document.getElementById('kidem-yil')?.value) || 0;
    const ay = parseInt(document.getElementById('kidem-ay')?.value) || 0;
    const gun = parseInt(document.getElementById('kidem-gun')?.value) || 0;
    const izin = parseInt(document.getElementById('kidem-izin')?.value) || 0;
    const indirim = parseInt(document.getElementById('kidem-indirim')?.value) || 0;
    
    if (brut === 0) {
        alert('Lütfen aylık brüt ücret giriniz.');
        return;
    }
    
    // 2025 tavan ücret
    const tavan = 41868.77;
    const kullanilanBrut = Math.min(brut, tavan);
    
    // Toplam çalışılan gün
    const toplamGun = (yil * 365) + (ay * 30) + gun;
    const toplamYil = toplamGun / 365;
    
    // Günlük ücret
    const gunlukUcret = kullanilanBrut / 30;
    
    // Kıdem tazminatı
    const kidemTazminati = gunlukUcret * 30 * toplamYil;
    
    // İzin ücreti
    const izinUcreti = gunlukUcret * izin;
    
    // Toplam brüt
    const toplamBrut = kidemTazminati + izinUcreti;
    
    // Damga vergisi (binde 7.59)
    const damgaVergisi = toplamBrut * 0.00759;
    
    // Peşin ödeme indirimi
    let indirimTutari = 0;
    const indirimRow = document.getElementById('kidem-indirim-row');
    if (indirim > 0 && indirimRow) {
        indirimTutari = toplamBrut * (indirim / 100);
        indirimRow.style.display = 'flex';
        document.getElementById('kidem-indirim-tutar').textContent = '-' + formatPara(indirimTutari);
    } else if (indirimRow) {
        indirimRow.style.display = 'none';
    }
    
    // Net tutar
    const netTutar = toplamBrut - damgaVergisi - indirimTutari;
    
    // Sonuçları göster
    document.getElementById('kidem-sure').textContent = yil + ' yıl ' + ay + ' ay ' + gun + ' gün';
    document.getElementById('kidem-gunluk').textContent = formatPara(gunlukUcret);
    document.getElementById('kidem-30gun').textContent = formatPara(gunlukUcret * 30);
    document.getElementById('kidem-tutar').textContent = formatPara(kidemTazminati);
    document.getElementById('kidem-izin-ucreti').textContent = formatPara(izinUcreti);
    document.getElementById('kidem-toplam').textContent = formatPara(toplamBrut);
    document.getElementById('kidem-damga').textContent = formatPara(damgaVergisi);
    document.getElementById('kidem-net').textContent = formatPara(netTutar);
    
    // Sonuç kutusunu göster
    document.getElementById('kidem-sonuc').classList.add('active');
}

// İhbar Tazminatı Hesaplama
function hesaplaIhbar() {
    const brut = parseFloat(document.getElementById('ihbar-brut')?.value) || 0;
    const yil = parseInt(document.getElementById('ihbar-yil')?.value) || 0;
    const ay = parseInt(document.getElementById('ihbar-ay')?.value) || 0;
    const gun = parseInt(document.getElementById('ihbar-gun')?.value) || 0;
    
    if (brut === 0) {
        alert('Lütfen aylık brüt ücret giriniz.');
        return;
    }
    
    const gunlukUcret = brut / 30;
    
    // İhbar süresi hesaplama
    let ihbarSuresi = 0;
    const toplamAy = (yil * 12) + ay;
    
    if (toplamAy >= 180) ihbarSuresi = 56; // 15+ yıl
    else if (toplamAy >= 72) ihbarSuresi = 42; // 6-15 yıl
    else if (toplamAy >= 18) ihbarSuresi = 28; // 1.5-6 yıl
    else if (toplamAy >= 6) ihbarSuresi = 14; // 0.5-1.5 yıl
    else ihbarSuresi = 14;
    
    const ihbarTazminati = gunlukUcret * ihbarSuresi;
    
    document.getElementById('ihbar-sure').textContent = ihbarSuresi + ' gün';
    document.getElementById('ihbar-tutar').textContent = formatPara(ihbarTazminati);
    document.getElementById('ihbar-sonuc').classList.add('active');
}

// Fazla Mesai Hesaplama
function hesaplaMesai() {
    const saatUcret = parseFloat(document.getElementById('mesai-saat')?.value) || 0;
    const saat = parseFloat(document.getElementById('mesai-saat-sayisi')?.value) || 0;
    const gun = parseFloat(document.getElementById('mesai-gun-sayisi')?.value) || 1;
    const oran = parseFloat(document.getElementById('mesai-oran')?.value) || 50;
    
    if (saatUcret === 0 || saat === 0) {
        alert('Lütfen saat ücreti ve çalışma saati giriniz.');
        return;
    }
    
    const mesaiUcreti = saatUcret * saat * (1 + oran / 100) * gun;
    
    document.getElementById('mesai-tutar').textContent = formatPara(mesaiUcreti);
    document.getElementById('mesai-sonuc').classList.add('active');
}

// Gece Çalışması Hesaplama
function hesaplaGece() {
    const saatUcret = parseFloat(document.getElementById('gece-saat')?.value) || 0;
    const saat = parseFloat(document.getElementById('gece-saat-sayisi')?.value) || 0;
    const gun = parseFloat(document.getElementById('gece-gun-sayisi')?.value) || 1;
    
    if (saatUcret === 0 || saat === 0) {
        alert('Lütfen saat ücreti ve çalışma saati giriniz.');
        return;
    }
    
    // Gece çalışması %50 zamlı
    const geceUcreti = saatUcret * saat * 1.5 * gun;
    
    document.getElementById('gece-tutar').textContent = formatPara(geceUcreti);
    document.getElementById('gece-sonuc').classList.add('active');
}

// Bayram Tatil Ücreti Hesaplama
function hesaplaBayram() {
    const saatUcret = parseFloat(document.getElementById('bayram-saat')?.value) || 0;
    const saat = parseFloat(document.getElementById('bayram-saat-sayisi')?.value) || 0;
    const oran = parseFloat(document.getElementById('bayram-oran')?.value) || 200;
    
    if (saatUcret === 0 || saat === 0) {
        alert('Lütfen saat ücreti ve çalışma saati giriniz.');
        return;
    }
    
    const bayramUcreti = saatUcret * saat * (oran / 100);
    
    document.getElementById('bayram-tutar').textContent = formatPara(bayramUcreti);
    document.getElementById('bayram-sonuc').classList.add('active');
}

// İşsizlik Maaşı Hesaplama
function hesaplaIssizlik() {
    const brut = parseFloat(document.getElementById('issizlik-brut')?.value) || 0;
    const prim = parseInt(document.getElementById('issizlik-prim')?.value) || 0;
    const yas = parseInt(document.getElementById('issizlik-yas')?.value) || 0;
    
    if (brut === 0 || prim === 0) {
        alert('Lütfen brüt ücret ve prim günü giriniz.');
        return;
    }
    
    // Son 4 ay ortalama daily gross
    const gunlukBrut = brut / 30;
    const issizlikMaasi = gunlukBrut * 0.4; // %40 oranında
    
    // Süre hesaplama
    let sure = 0;
    if (prim >= 900 && yas >= 50) sure = 300; // 50+ yaş ve 900+ gün
    else if (prim >= 900) sure = 240; // 900+ gün
    else if (prim >= 540) sure = 180; // 540+ gün
    else if (prim >= 360) sure = 120; // 360+ gün
    else sure = 0;
    
    document.getElementById('issizlik-tutar').textContent = formatPara(issizlikMaasi);
    document.getElementById('issizlik-sure').textContent = sure + ' gün (' + (sure/30).toFixed(1) + ' ay)';
    document.getElementById('issizlik-sonuc').classList.add('active');
}

// Yıllık İzin Hesaplama
function hesaplaIzin() {
    const yil = parseInt(document.getElementById('izin-yil')?.value) || 0;
    const ay = parseInt(document.getElementById('izin-ay')?.value) || 0;
    const kullanilan = parseInt(document.getElementById('izin-kullanilan')?.value) || 0;
    
    const toplamAy = (yil * 12) + ay;
    
    let izinHakki = 0;
    if (toplamAy >= 180) izinHakki = 26; // 15+ yıl
    else if (toplamAy >= 60) izinHakki = 20; // 5-15 yıl
    else if (toplamAy >= 18) izinHakki = 14; // 1.5-5 yıl
    else izinHakki = 0;
    
    const kalanIzin = Math.max(0, izinHakki - kullanilan);
    
    document.getElementById('izin-hakki').textContent = izinHakki + ' gün';
    document.getElementById('izin-kalan').textContent = kalanIzin + ' gün';
    document.getElementById('izin-sonuc').classList.add('active');
}

// Doğum İzni Hesaplama
function hesaplaDogum() {
    const tur = document.getElementById('dogum-tur')?.value || 'isci';
    const once = parseInt(document.getElementById('dogum-once')?.value) || 0;
    const sonra = parseInt(document.getElementById('dogum-sonra')?.value) || 0;
    
    let toplamIzın = 0;
    let emzirme = 0;
    let ucretli = 0;
    
    if (tur === 'isci') {
        toplamIzın = once + sonra;
        emzirme = 180; // 6 ay emzirme izni
        ucretli = Math.min(once + sonra, 112); // Ücretli izin
    } else if (tur === 'memur') {
        toplamIzın = once + sonra;
        emzirme = 120; // 4 ay emzirme izni
        ucretli = Math.min(once + sonra, 112);
    }
    
    document.getElementById('dogum-toplam').textContent = toplamIzın + ' gün';
    document.getElementById('dogum-emzirme').textContent = emzirme + ' gün';
    document.getElementById('dogum-ucretli').textContent = ucretli + ' gün';
    document.getElementById('dogum-sonuc').classList.add('active');
}

// Netten Brüte Maaş Hesaplama
function hesaplaNetBrut() {
    const net = parseFloat(document.getElementById('net-net')?.value) || 0;
    
    if (net === 0) {
        alert('Lütfen net maaş tutarı giriniz.');
        return;
    }
    
    // Yaklaşık hesaplama (tersine mühendislik)
    let brut = net * 1.5; // Yaklaşık bir başlangıç değeri
    
    // SGK primi %14, işsizlik %1, gelir vergisi ortalama %15
    const tahminiKesintiOrani = 0.30;
    brut = net / (1 - tahminiKesintiOrani);
    
    const sgk = brut * 0.14;
    const issizlik = brut * 0.01;
    const gelirVergisi = brut * 0.15;
    const damgaVergisi = brut * 0.00759;
    
    document.getElementById('net-brut').textContent = formatPara(brut);
    document.getElementById('net-sgk').textContent = formatPara(sgk);
    document.getElementById('net-issizlik').textContent = formatPara(issizlik);
    document.getElementById('net-gelir').textContent = formatPara(gelirVergisi);
    document.getElementById('net-damga').textContent = formatPara(damgaVergisi);
    document.getElementById('net-sonuc').classList.add('active');
}

// İş Kazası Tazminatı Hesaplama
function hesaplaIsKazasi() {
    const brut = parseFloat(document.getElementById('iskazasi-brut')?.value) || 0;
    const engel = parseFloat(document.getElementById('iskazasi-engel')?.value) || 0;
    
    if (brut === 0 || engel === 0) {
        alert('Lütfen günlük ücret ve engel oranı giriniz.');
        return;
    }
    
    const tazminat = brut * 30 * (engel / 100) * 12; // Yıllık
    
    document.getElementById('iskazasi-tutar').textContent = formatPara(tazminat);
    document.getElementById('iskazasi-sonuc').classList.add('active');
}

// Emekli Maaşı Hesaplama
function hesaplaEmekli() {
    const prim = parseInt(document.getElementById('emekli-prim')?.value) || 0;
    const tur = document.getElementById('emekli-tur')?.value || '4a';
    const aylik = parseFloat(document.getElementById('emekli-aylik')?.value) || 0;
    
    if (prim === 0 || aylik === 0) {
        alert('Lütfen prim günü ve ortalama aylık kazancı giriniz.');
        return;
    }
    
    // Basit hesaplama (yaklaşık)
    const yillikKazanc = aylik * 12;
    const primYili = prim / 360;
    
    let maas = 0;
    if (tur === '4a') maas = (yillikKazanc * 0.02) * (primYili / 30); // SSK
    else if (tur === '4b') maas = (yillikKazanc * 0.025) * (primYili / 30); // Bağkur
    else if (tur === '4c') maas = (yillikKazanc * 0.03) * (primYili / 30); // Emekli Sandığı
    
    document.getElementById('emekli-maas').textContent = formatPara(maas);
    document.getElementById('emekli-sonuc').classList.add('active');
}

// Askerlik Borçlanması Hesaplama
function hesaplaAskerlik() {
    const gun = parseInt(document.getElementById('askerlik-gun')?.value) || 0;
    const ucret = parseFloat(document.getElementById('askerlik-ucret')?.value) || 0;
    
    if (gun === 0) {
        alert('Lütfen askerlik süresi giriniz.');
        return;
    }
    
    const maliyet = gun * (ucret || 100) * 0.32; // Günlük maliyet yaklaşık
    
    document.getElementById('askerlik-prim').textContent = gun + ' gün';
    document.getElementById('askerlik-maliyet').textContent = formatPara(maliyet);
    document.getElementById('askerlik-sonuc').classList.add('active');
}

// Yurtdışı Borçlanması Hesaplama
function hesaplaYurtdisi() {
    const gun = parseInt(document.getElementById('yurtdisi-gun')?.value) || 0;
    const ucret = parseFloat(document.getElementById('yurtdisi-ucret')?.value) || 0;
    const odeme = document.getElementById('yurtdisi-odeme')?.value || 'pesin';
    
    if (gun === 0) {
        alert('Lütfen yurtdışı çalışma süresi giriniz.');
        return;
    }
    
    let maliyet = gun * (ucret || 150) * 0.32;
    if (odeme === 'taksitli') maliyet = maliyet * 1.12; // Taksitli faiz
    
    document.getElementById('yurtdisi-prim').textContent = gun + ' gün';
    document.getElementById('yurtdisi-maliyet').textContent = formatPara(maliyet);
    document.getElementById('yurtdisi-sonuc').classList.add('active');
}

// Kira Stopajı Hesaplama
function hesaplaStopaj() {
    const kira = parseFloat(document.getElementById('stopaj-kira')?.value) || 0;
    const tur = document.getElementById('stopaj-tur')?.value || 'konut';
    
    if (kira === 0) {
        alert('Lütfen kira tutarı giriniz.');
        return;
    }
    
    let stopaj = 0;
    if (tur === 'konut') stopaj = kira * 0.20; // %20
    else if (tur === 'isyeri') stopaj = kira * 0.20; // %20
    
    const net = kira - stopaj;
    
    document.getElementById('stopaj-oran').textContent = '%20';
    document.getElementById('stopaj-kesinti').textContent = formatPara(stopaj);
    document.getElementById('stopaj-net').textContent = formatPara(net);
    document.getElementById('stopaj-sonuc').classList.add('active');
}

// SMM Hesaplama
function hesaplaSMM() {
    const tutar = parseFloat(document.getElementById('smm-tutar')?.value) || 0;
    
    if (tutar === 0) {
        alert('Lütfen makbuz tutarı giriniz.');
        return;
    }
    
    const gelirVergisi = tutar * 0.20;
    const damgaVergisi = tutar * 0.00948;
    const sgk = tutar * 0.075; // Yüzde 7.5
    const net = tutar - gelirVergisi - damgaVergisi - sgk;
    
    document.getElementById('smm-gelir').textContent = formatPara(gelirVergisi);
    document.getElementById('smm-damga').textContent = formatPara(damgaVergisi);
    document.getElementById('smm-sgk').textContent = formatPara(sgk);
    document.getElementById('smm-net').textContent = formatPara(net);
    document.getElementById('smm-sonuc').classList.add('active');
}

// Ceza Zamanaşımı Hesaplama
function hesaplaZamanasimi() {
    const tur = document.getElementById('zamanasimi-tur')?.value || 'diger';
    const yil = parseInt(document.getElementById('zamanasimi-yil')?.value) || 0;
    
    let sure = 0;
    if (tur === 'hapis') sure = 20; // 20 yıl
    else if (tur === 'hapis8') sure = 8; // 8 yıl
    else if (tur === 'diger') sure = 5; // 5 yıl
    else if (tur === 'ihbar') sure = 2; // 2 yıl
    else if (tur === 'kisaltma') sure = 1; // 1 yıl
    
    const kalan = Math.max(0, sure - yil);
    
    document.getElementById('zamanasimi-sure').textContent = sure + ' yıl';
    document.getElementById('zamanasimi-kalan').textContent = kalan + ' yıl';
    document.getElementById('zamanasimi-sonuc').classList.add('active');
}

// Hükümlü İnfaz Hesaplama
function hesaplaInfaz() {
    const ceza = parseInt(document.getElementById('infaz-ceza')?.value) || 0;
    const tur = document.getElementById('infaz-tur')?.value || 'agir';
    const yargi = document.getElementById('infaz-yargi')?.value || 'normal';
    
    if (ceza === 0) {
        alert('Lütfen ceza süresi giriniz.');
        return;
    }
    
    let oran = 0.66; // 2/3
    if (tur === 'agir') oran = 0.66;
    else if (tur === 'normal') oran = 0.50;
    else if (tur === 'kisa') oran = 0.50;
    
    if (yargi === 'denetimli') oran = 0.50;
    
    const infazSuresi = ceza * oran;
    const serbestlik = ceza - infazSuresi;
    
    document.getElementById('infaz-sure').textContent = infazSuresi.toFixed(1) + ' yıl';
    document.getElementById('infaz-serbestlik').textContent = serbestlik.toFixed(1) + ' yıl';
    document.getElementById('infaz-sonuc').classList.add('active');
}

// Mahkeme Harcı Hesaplama
function hesaplaMahkemeHarci() {
    const tutar = parseFloat(document.getElementById('mahkeme-tutar')?.value) || 0;
    const tur = document.getElementById('mahkeme-tur')?.value || 'basit';
    
    if (tutar === 0) {
        alert('Lütfen dava değeri giriniz.');
        return;
    }
    
    let harc = 0;
    if (tur === 'basit') harc = 68.60; // 2025 basit harç
    else if (tur === 'nispi') harc = Math.min(tutar * 0.0068, 13619.20); // %0.68, tavan uygulanır
    else if (tur === 'istinaf') harc = 136.90; // İstinaf harcı
    else if (tur === 'temyiz') harc = 205.40; // Temyiz harcı
    
    document.getElementById('mahkeme-harc').textContent = formatPara(harc);
    document.getElementById('mahkeme-sonuc').classList.add('active');
}

// İcra Harcı Hesaplama
function hesaplaIcraHarci() {
    const alacak = parseFloat(document.getElementById('icra-alacak')?.value) || 0;
    const tur = document.getElementById('icra-tur')?.value || 'takip';
    
    if (alacak === 0) {
        alert('Lütfen alacak tutarı giriniz.');
        return;
    }
    
    let harc = 0;
    if (tur === 'takip') harc = Math.min(alacak * 0.0068, 13619.20);
    else if (tur === 'harcsiz') harc = 0;
    else if (tur === 'itiraz') harc = 68.60;
    
    document.getElementById('icra-harc').textContent = formatPara(harc);
    document.getElementById('icra-sonuc').classList.add('active');
}

// Vekalet Ücreti Hesaplama
function hesaplaVekalet() {
    const deger = parseFloat(document.getElementById('vekalet-deger')?.value) || 0;
    const kdv = document.getElementById('vekalet-kdv')?.checked || false;
    
    if (deger === 0) {
        alert('Lütfen dava değeri giriniz.');
        return;
    }
    
    // Baro tarifesi (yaklaşık)
    let ucret = 0;
    if (deger <= 10000) ucret = 2000;
    else if (deger <= 50000) ucret = 3500;
    else if (deger <= 100000) ucret = 5000;
    else if (deger <= 250000) ucret = 7500;
    else ucret = deger * 0.03; // %3
    
    ucret = Math.min(ucret, 50000); // Tavan
    
    let kdvTutari = 0;
    if (kdv) kdvTutari = ucret * 0.20;
    
    const toplam = ucret + kdvTutari;
    
    document.getElementById('vekalet-ucret').textContent = formatPara(ucret);
    document.getElementById('vekalet-kdv-tutar').textContent = formatPara(kdvTutari);
    document.getElementById('vekalet-toplam').textContent = formatPara(toplam);
    document.getElementById('vekalet-sonuc').classList.add('active');
}

// Kira Artışı Hesaplama - Güncel (2026 Mart - %25 sınırı kaldırıldı)
function hesaplaKiraArtis() {
    const kira = parseFloat(document.getElementById('kira-mevcut')?.value) || 0;
    const yontem = document.getElementById('kira-yontem')?.value || 'tufe_gercek';
    const manuelOran = parseFloat(document.getElementById('kira-oran')?.value) || 0;
    
    if (kira === 0) {
        alert('Lütfen mevcut kira tutarı giriniz.');
        return;
    }
    
    let oran = 0;
    
    if (yontem === 'tufe_gercek') {
        // Mart 2026 TÜFE oranı (12 aylık ortalama)
        oran = 47.09;
    } else if (yontem === 'belirli' || yontem === 'serbest') {
        if (manuelOran === 0) {
            alert('Lütfen artış oranını giriniz.');
            return;
        }
        oran = manuelOran;
    }
    
    const artis = kira * (oran / 100);
    const yeniKira = kira + artis;
    const yillik = yeniKira * 12;
    
    // Sonuçları göster
    document.getElementById('kira-oran-text').textContent = '%' + oran.toFixed(2).replace('.', ',');
    document.getElementById('kira-mevcut-text').textContent = formatPara(kira);
    document.getElementById('kira-artis-tutar').textContent = formatPara(artis);
    document.getElementById('kira-yeni').textContent = formatPara(yeniKira);
    document.getElementById('kira-yeni-detay').textContent = formatPara(yeniKira);
    document.getElementById('kira-yillik').textContent = formatPara(yillik);
    document.getElementById('kira-sonuc').classList.add('active');
}

// Islah Harcı Hesaplama
function hesaplaIslahHarci() {
    const eski = parseFloat(document.getElementById('islah-eski')?.value) || 0;
    const yeni = parseFloat(document.getElementById('islah-yeni')?.value) || 0;
    
    if (eski === 0 || yeni === 0) {
        alert('Lütfen eski ve yeni dava değerlerini giriniz.');
        return;
    }
    
    const fark = yeni - eski;
    const harc = fark * 0.0068; // %0.68
    
    document.getElementById('islah-fark').textContent = formatPara(fark);
    document.getElementById('islah-harc').textContent = formatPara(harc);
    document.getElementById('islah-sonuc').classList.add('active');
}

// Tapu Harcı Hesaplama
function hesaplaTapuHarci() {
    const bedel = parseFloat(document.getElementById('tapu-bedel')?.value) || 0;
    const tur = document.getElementById('tapu-tur')?.value || 'satis';
    
    if (bedel === 0) {
        alert('Lütfen gayrimenkul değeri giriniz.');
        return;
    }
    
    let harc = 0;
    if (tur === 'satis') harc = bedel * 0.04; // Alıcı + satıcı %2 + %2 = %4
    else if (tur === 'ipotek') harc = bedel * 0.003; // %0.3
    
    document.getElementById('tapu-harc').textContent = formatPara(harc);
    document.getElementById('tapu-sonuc').classList.add('active');
}

// Nafaka Hesaplama
function hesaplaNafaka() {
    const gelir = parseFloat(document.getElementById('nafaka-gelir')?.value) || 0;
    const tur = document.getElementById('nafaka-tur')?.value || 'tedbir';
    const sure = parseInt(document.getElementById('nafaka-sure')?.value) || 0;
    
    if (gelir === 0) {
        alert('Lütfen gelir tutarı giriniz.');
        return;
    }
    
    let oran = 0;
    if (tur === 'tedbir') oran = 0.20; // %20
    else if (tur === 'yoksulluk') oran = 0.25; // %25
    else if (tur === 'istirak') oran = 0.30; // %30
    
    const nafaka = gelir * oran;
    const toplam = nafaka * sure;
    
    document.getElementById('nafaka-aylik').textContent = formatPara(nafaka);
    document.getElementById('nafaka-toplam').textContent = formatPara(toplam);
    document.getElementById('nafaka-sonuc').classList.add('active');
}

// Trafik Kazası Tazminatı Hesaplama
function hesaplaTrafikKazasi() {
    const arac = parseFloat(document.getElementById('trafik-arac')?.value) || 0;
    const kusur = parseFloat(document.getElementById('trafik-kusur')?.value) || 0;
    const manevi = parseFloat(document.getElementById('trafik-manevi')?.value) || 0;
    
    if (arac === 0) {
        alert('Lütfen araç değeri giriniz.');
        return;
    }
    
    const maddi = arac * (kusur / 100);
    const toplam = maddi + manevi;
    
    document.getElementById('trafik-maddi').textContent = formatPara(maddi);
    document.getElementById('trafik-toplam').textContent = formatPara(toplam);
    document.getElementById('trafik-sonuc').classList.add('active');
}

// Araç Değer Kaybı Hesaplama
function hesaplaAracDegerKaybi() {
    const arac = parseFloat(document.getElementById('deger-arac')?.value) || 0;
    const hasar = parseFloat(document.getElementById('deger-hasar')?.value) || 0;
    const yil = parseInt(document.getElementById('deger-yil')?.value) || 0;
    
    if (arac === 0 || hasar === 0) {
        alert('Lütfen araç değeri ve hasar oranı giriniz.');
        return;
    }
    
    // Yargıtay formülü (yaklaşık)
    const yasIndirimi = Math.min(yil * 0.10, 0.30); // Her yıl %10, max %30
    const degerKaybi = (arac * (hasar / 100)) * (1 - yasIndirimi) * 0.15;
    
    document.getElementById('deger-kayip').textContent = formatPara(degerKaybi);
    document.getElementById('deger-sonuc').classList.add('active');
}

// Günlük Yevmiye Hesaplama
function hesaplaYevmiye() {
    const brut = parseFloat(document.getElementById('yevmiye-brut')?.value) || 0;
    
    if (brut === 0) {
        alert('Lütfen brüt ücret giriniz.');
        return;
    }
    
    const yevmiye = brut / 30;
    
    document.getElementById('yevmiye-tutar').textContent = formatPara(yevmiye);
    document.getElementById('yevmiye-sonuc').classList.add('active');
}

// Belirsiz çağrıları yakalama - hata önleme
window.addEventListener('error', function(e) {
    if (e.message.includes('hesapla')) {
        console.log('Hesaplama fonksiyonu bulunamadı:', e.message);
    }
});
