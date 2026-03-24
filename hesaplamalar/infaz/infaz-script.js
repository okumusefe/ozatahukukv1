class InfazCalculator {
    constructor() {
        this.init();
    }

    init() {
        this.form = document.getElementById('calculator-form');
        this.resultsSection = document.getElementById('results');
        
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.calculate();
        });

        document.getElementById('reset-btn').addEventListener('click', () => {
            this.reset();
        });

        document.getElementById('export-btn').addEventListener('click', () => {
            this.exportResults();
        });
    }

    calculate() {
        // Form validasyonu
        const crimeDate = document.getElementById('crime-date').value;
        const years = parseInt(document.getElementById('sentence-years').value) || 0;
        const months = parseInt(document.getElementById('sentence-months').value) || 0;
        const crimeType = document.getElementById('crime-type').value;

        if (!crimeDate || !crimeType || years === 0) {
            alert('Lütfen suç tarihini, suç türünü ve ceza yılını girin!');
            return;
        }

        console.log('Hesaplama başlıyor:', { crimeDate, years, months, crimeType });

        const baseSentence = this.getBaseSentence();
        console.log('Temel ceza (gün):', baseSentence);

        const reducedSentence = this.calculateReductions(baseSentence);
        console.log('İndirimli ceza:', reducedSentence);

        const prisonBreakdown = this.calculatePrisonBreakdown(reducedSentence);
        console.log('Cezaevi ayrımı:', prisonBreakdown);

        const releaseDate = this.calculateReleaseDate(prisonBreakdown);
        console.log('Tahliye tarihi:', releaseDate);

        this.displayResults({
            base: baseSentence,
            reduced: reducedSentence,
            prison: prisonBreakdown,
            release: releaseDate
        });
    }

    getBaseSentence() {
        const years = parseInt(document.getElementById('sentence-years').value) || 0;
        const months = parseInt(document.getElementById('sentence-months').value) || 0;
        return this.convertToDays(years, months, 0);
    }

    calculateReductions(baseSentence) {
        const effectiveRemorse = document.getElementById('effective-remorse').value;
        const goodBehavior = document.getElementById('good-behavior').value;
        const trialDuration = document.getElementById('trial-duration').value;
        const isRecidivist = document.getElementById('recidivist').checked;

        let totalReduction = 0;
        const breakdown = [];

        // Etkin pişmanlık indirimi
        if (effectiveRemorse === 'yes') {
            totalReduction += baseSentence * 0.25;
            breakdown.push('Etkin pişmanlık: 1/4 indirim');
        }

        // İyi hal indirimi
        if (goodBehavior === 'yes') {
            totalReduction += baseSentence * 0.1667;
            breakdown.push('İyi hal: 1/6 indirim');
        }

        // Yargılama süresi indirimi
        if (trialDuration === 'long') {
            totalReduction += baseSentence * 0.25;
            breakdown.push('Uzun yargılama süresi: 1/4 indirim');
        }

        // Mükerrirlik durumu
        if (isRecidivist) {
            breakdown.push('Mükerrir: İndirim uygulanmaz');
        }

        const totalReducedDays = Math.max(baseSentence - totalReduction, 0);

        return {
            total: totalReducedDays,
            breakdown: breakdown
        };
    }

    calculatePrisonBreakdown(reducedSentence) {
        const crimeType = document.getElementById('crime-type').value;
        const crimeDate = new Date(document.getElementById('crime-date').value);
        const isBefore2020 = crimeDate < new Date('2020-03-30');
        let totalReducedDays = reducedSentence.total;
        const breakdown = reducedSentence.breakdown;

        // Koşullu salıverilme oranını belirle
        let conditionalReleaseRatio = this.getConditionalReleaseRatio(crimeType);
        
        // Mükerrir kontrolü
        if (document.getElementById('recidivist').checked) {
            conditionalReleaseRatio = 0.66; // 2/3
            breakdown.push('Mükerrir: Koşullu salıverilme oranı 2/3');
        }

        // Cezaevinde kalacak süre
        const prisonTime = Math.floor(totalReducedDays * conditionalReleaseRatio);
        
        // Denetimli serbestlik süresi
        const probationYears = this.getProbationYears(crimeType);
        const probationTime = this.convertToDays(probationYears, 0, 0);

        // Kapalı ve açık cezaevi hesapla
        const closedPrison = Math.floor(prisonTime * 0.8);
        const openPrison = prisonTime - closedPrison;

        return {
            prison: prisonTime,
            probation: probationTime,
            closed: closedPrison,
            open: openPrison,
            probationYears: this.convertToDays(probationYears, 0, 0),
            conditionalReleaseRatio,
            breakdown: this.getBreakdownDetails(totalReducedDays, prisonTime, probationTime, conditionalReleaseRatio)
        };
    }

    getConditionalReleaseRatio(crimeType) {
        const crimeDate = new Date(document.getElementById('crime-date').value);
        const isBefore2014 = crimeDate < new Date('2014-06-28');
        const isBefore2020 = crimeDate < new Date('2020-03-30');
        const isBefore2023 = crimeDate < new Date('2023-07-01');
        const isBefore2024_03 = crimeDate < new Date('2024-03-12');
        const isBefore2024_11 = crimeDate < new Date('2024-11-14');
        const isBefore2025_06 = crimeDate < new Date('2025-06-04');
        const isBefore2025_12 = crimeDate < new Date('2025-12-25');

        const ratios = {
            // Genel suçlar - 11. Yargı Paketi ile değişen oranlar
            genel: isBefore2020 ? 0.5 : (isBefore2023 ? 0.66 : (isBefore2024_03 ? 0.5 : (isBefore2024_11 ? 0.66 : (isBefore2025_06 ? 0.5 : (isBefore2025_12 ? 0.66 : 0.5)))),
            
            // Kasten öldürme - 11. Yargı Paketi değişikliği
            kastenOldurme: isBefore2023 ? 0.66 : (isBefore2024_03 ? 0.5 : (isBefore2024_11 ? 0.66 : (isBefore2025_06 ? 0.5 : (isBefore2025_12 ? 0.75 : 0.66))),
            
            // Nitelikli yaralama
            nitelikliYaralama: isBefore2023 ? 0.66 : (isBefore2024_03 ? 0.5 : (isBefore2024_11 ? 0.66 : (isBefore2025_06 ? 0.5 : (isBefore2025_12 ? 0.75 : 0.66))),
            
            // Cinsel dokunulmazlığa karşı suçlar
            cinselSaldiri: {
                basit: isBefore2014 ? 0.66 : (isBefore2023 ? 0.75 : (isBefore2024_03 ? 0.5 : (isBefore2024_11 ? 0.75 : (isBefore2025_06 ? 0.5 : (isBefore2025_12 ? 0.75 : 0.66))),
                nitelikli: isBefore2023 ? 0.75 : (isBefore2024_03 ? 0.5 : (isBefore2024_11 ? 0.75 : (isBefore2025_06 ? 0.5 : (isBefore2025_12 ? 0.75 : 0.66)))
            },
            
            // Uyuşturucu suçları - 11. Yargı Paketi ile değişen oranlar
            uyusturucu: {
                kullanmak: isBefore2023 ? 0.66 : (isBefore2024_03 ? 0.5 : (isBefore2024_11 ? 0.75 : (isBefore2025_06 ? 0.5 : (isBefore2025_12 ? 0.75 : 0.66))),
                ticaret: isBefore2023 ? 0.75 : (isBefore2024_03 ? 0.5 : (isBefore2024_11 ? 0.75 : (isBefore2025_06 ? 0.5 : (isBefore2025_12 ? 0.75 : 0.66)))
            },
            
            // Terör suçları - 11. Yargı Paketi ile değişen oranlar
            teror: isBefore2023 ? 0.66 : (isBefore2024_03 ? 0.5 : (isBefore2024_11 ? 0.75 : (isBefore2025_06 ? 0.5 : (isBefore2025_12 ? 0.75 : 0.66))),
            
            // İşkence ve eziyet
            iskence: isBefore2023 ? 0.66 : (isBefore2024_03 ? 0.5 : (isBefore2024_11 ? 0.75 : (isBefore2025_06 ? 0.5 : (isBefore2025_12 ? 0.75 : 0.66))),
            eziyet: isBefore2023 ? 0.66 : (isBefore2024_03 ? 0.5 : (isBefore2024_11 ? 0.75 : (isBefore2025_06 ? 0.5 : (isBefore2025_12 ? 0.75 : 0.66))),
            
            // Özel hayata karşı suçlar
            ozelHayat: isBefore2023 ? 0.66 : (isBefore2024_03 ? 0.5 : (isBefore2024_11 ? 0.75 : (isBefore2025_06 ? 0.5 : (isBefore2025_12 ? 0.75 : 0.66))),
            
            // Örgüt suçları
            orgut: isBefore2023 ? 0.66 : (isBefore2024_03 ? 0.5 : (isBefore2024_11 ? 0.75 : (isBefore2025_06 ? 0.5 : (isBefore2025_12 ? 0.75 : 0.66)))
        };

        if (typeof ratios[crimeType] === 'object') {
            return ratios[crimeType].basit || ratios[crimeType].ticaret || 0.66;
        }

        return ratios[crimeType] || 0.66;
    }

    getProbationYears(crimeType) {
        const crimeDate = new Date(document.getElementById('crime-date').value);
        const isBefore2020 = crimeDate < new Date('2020-03-30');
        const isBefore2023 = crimeDate < new Date('2023-07-01');
        const isBefore2024_03 = crimeDate < new Date('2024-03-12');
        const isBefore2024_11 = crimeDate < new Date('2024-11-14');
        const isBefore2025_06 = crimeDate < new Date('2025-06-04');
        const isBefore2025_12 = crimeDate < new Date('2025-12-25');
        
        // 11. Yargı Paketi ile değişen denetimli serbestlik süreleri
        const exceptionCrimes = [
            'kastenOldurme',
            'nitelikliYaralama',
            'cinselSaldiri',
            'uyusturucu',
            'teror',
            'iskence',
            'eziyet',
            'ozelHayat',
            'orgut'
        ];

        if (exceptionCrimes.includes(crimeType)) {
            // İstisna suçlar: 2024-11 öncesi 1 yıl, 2024-11 sonrası 6 ay
            if (isBefore2024_11) return 1;
            else return 0.5; // 6 ay
        } else {
            // Genel suçlar: 2020 öncesi 3 yıl, 2020-2024 arası 1 yıl, 2024-11 sonrası 6 ay
            if (isBefore2020) return 3;
            else if (isBefore2024_11) return 1;
            else return 0.5; // 6 ay
        }
    }

    getBreakdownDetails(totalDays, prisonTime, probationTime, ratio) {
        const crimeDate = new Date(document.getElementById('crime-date').value);
        const isBefore2014 = crimeDate < new Date('2014-06-28');
        const isBefore2020 = crimeDate < new Date('2020-03-30');
        const isBefore2023 = crimeDate < new Date('2023-07-01');
        const isBefore2024 = crimeDate < new Date('2024-02-20');
        const isBefore2025_06 = crimeDate < new Date('2025-06-04');
        const isBefore2025_12 = crimeDate < new Date('2025-12-25');
        
        const ratioText = ratio === 0.5 ? '1/2' : ratio === 0.66 ? '2/3' : ratio === 0.75 ? '3/4' : ratio === 0.8 ? '4/5' : `${ratio}`;
        
        let legalBasis = '';
        if (isBefore2025_12) {
            if (isBefore2025_06) {
                legalBasis = ' (10. Yargı Paketi sonrası)';
            } else {
                legalBasis = ' (11. Yargı Paketi sonrası)';
            }
        } else if (isBefore2024_11) {
            legalBasis = ' (9. Yargı Paketi sonrası)';
        } else if (isBefore2024_03) {
            legalBasis = ' (8. Yargı Paketi sonrası)';
        } else if (isBefore2023) {
            legalBasis = ' (7. Yargı Paketi sonrası)';
        } else if (isBefore2020) {
            legalBasis = ' (7242 Sayılı Kanun sonrası)';
        } else {
            legalBasis = ' (7242 Sayılı Kanun öncesi)';
        }
        
        return [
            `Temel Ceza: ${this.formatSentence(totalDays)}`,
            `Koşullu Salıverilme Oranı: ${ratioText}${legalBasis}`,
            `Cezaevinde Kalma Süresi: ${this.formatSentence(prisonTime)}`,
            `Denetimli Serbestlik: ${this.formatSentence(probationTime)}`
        ];
    }

    calculateReleaseDate(prisonBreakdown) {
        const crimeDate = new Date(document.getElementById('crime-date').value);
        const prisonDays = prisonBreakdown.prison;
        const probationDays = prisonBreakdown.probation;

        if (!crimeDate || isNaN(crimeDate.getTime())) {
            return 'Geçersiz suç tarih';
        }

        const releaseDate = new Date(crimeDate);
        releaseDate.setDate(releaseDate.getDate() + prisonDays);
        releaseDate.setFullYear(releaseDate.getFullYear() + Math.floor(probationDays / 365));
        releaseDate.setDate(releaseDate.getDate() + (probationDays % 365));

        return releaseDate.toLocaleDateString('tr-TR');
    }

    formatSentence(days) {
        const years = Math.floor(days / 365);
        const remainingDays = days % 365;
        const months = Math.floor(remainingDays / 30);
        const remainingDays2 = remainingDays % 30;

        if (years > 0 && months > 0) {
            return `${years} yıl, ${months} ay, ${remainingDays2} gün`;
        } else if (years > 0) {
            return `${years} yıl, ${remainingDays} gün`;
        } else if (months > 0) {
            return `${months} ay, ${remainingDays2} gün`;
        } else {
            return `${remainingDays2} gün`;
        }
    }

    convertToDays(years, months, days) {
        return (years * 365) + (months * 30) + days;
    }

    displayResults(results) {
        const baseText = this.formatSentence(results.base);
        const reducedText = this.formatSentence(results.reduced.total);
        const closedText = this.formatSentence(results.prison.closed);
        const openText = this.formatSentence(results.prison.open);
        const probationText = this.formatSentence(results.prison.probation);
        const releaseText = results.release;

        document.getElementById('base-sentence').textContent = baseText;
        document.getElementById('reduced-sentence').textContent = reducedText;
        document.getElementById('closed-prison').textContent = closedText;
        document.getElementById('open-prison').textContent = openText;
        document.getElementById('probation').textContent = probationText;
        document.getElementById('release-date').textContent = releaseText;

        // Detaylı breakdown göster
        const breakdownDiv = document.getElementById('calculation-breakdown');
        breakdownDiv.innerHTML = results.prison.breakdown.map(item => `<div class="breakdown-item">${item}</div>`).join('');

        this.resultsSection.classList.remove('hidden');
        this.resultsSection.classList.add('visible');
    }

    reset() {
        this.form.reset();
        this.resultsSection.classList.add('hidden');
        this.resultsSection.classList.remove('visible');
    }

    exportResults() {
        const baseText = document.getElementById('base-sentence').textContent;
        const reducedText = document.getElementById('reduced-sentence').textContent;
        const closedText = document.getElementById('closed-prison').textContent;
        const openText = document.getElementById('open-prison').textContent;
        const probationText = document.getElementById('probation').textContent;
        const releaseText = document.getElementById('release-date').textContent;

        const content = `İNFAZ SÜRESİ HESAPLAMA SONUÇLARI
========================================
Tarih: ${new Date().toLocaleDateString('tr-TR')}
Suç Tarihi: ${document.getElementById('crime-date').value}
Suç Türü: ${document.getElementById('crime-type').selectedOptions[0]?.text || 'Seçilmedi'}

HESAPLAMA SONUÇLARI:
==================
Temel Ceza: ${baseText}
İndirimli Ceza: ${reducedText}
Kapalı Cezaevi: ${closedText}
Açık Cezaevi: ${openText}
Denetimli Serbestlik: ${probationText}
Tahliye Tarihi: ${releaseText}

KİŞİSEL BİLGİLER:
=================
Yaş Grubu: ${document.getElementById('age').selectedOptions[0]?.text}
Cinsiyet: ${document.getElementById('gender').selectedOptions[0]?.text}
0-6 Yaş Çocuğu: ${document.getElementById('child-0-6').checked ? 'Var' : 'Yok'}
Ağır Hastalık: ${document.getElementById('health-issue').checked ? 'Var' : 'Yok'}
Mükerrir: ${document.getElementById('recidivist').checked ? 'Evet' : 'Hayır'}

İNDİRİMLER:
===========
Etkin Pişmanlık: ${document.getElementById('effective-remorse').selectedOptions[0]?.text}
İyi Hal: ${document.getElementById('good-behavior').selectedOptions[0]?.text}
Yargılama Süresi: ${document.getElementById('trial-duration').selectedOptions[0]?.text}

UYGULANAN YASAL MEVZUAT:
========================
Bu hesaplama 5275 sayılı Ceza ve Güvenlik Tedbirlerinin İnfazı 
Hakkında Kanun ve 7242 sayılı Kanun değişikliklerine göre yapılmıştır.

DAHİL EDİLEN YARGI PAKETLERİ:
- 7242 Sayılı Kanun (30.03.2020)
- 7. Yargı Paketi (07.04.2023)
- 8. Yargı Paketi (12.03.2024)
- 9. Yargı Paketi (14.11.2024)
- 10. Yargı Paketi (25.12.2025)
- 11. Yargı Paketi (04.06.2025)

Yasal sonuçlar için bir avukata danışınız.
© 2026 İnfaz Süresi Hesaplayıcı - Türk Ceza Hukuku`;

        const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `infaz-hesaplamasi-${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// Sayfa yüklendiğinde hesaplayıcıyı başlat
document.addEventListener('DOMContentLoaded', () => {
    new InfazCalculator();
});
