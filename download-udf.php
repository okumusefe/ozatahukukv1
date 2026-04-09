<?php
/**
 * UYAP Döküman Editörü (UDF) Dosya İndirme Endpointi
 * 
 * Bu dosya, dilekçeleri UYAP Döküman Editörü formatında (.udf) indirmek için kullanılır.
 * ob_clean() ile çıktı öncesi tüm boşluklar temizlenir ve exit ile dosya sonlandırılır.
 */

// Hata raporlamasını kapat (temiz çıktı için)
error_reporting(0);
ini_set('display_errors', 0);

// CORS başlıkları
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');

// POST verilerini al
$title = isset($_POST['title']) ? $_POST['title'] : 'Dilekce';
$content = isset($_POST['content']) ? $_POST['content'] : '';
$filename = isset($_POST['filename']) ? $_POST['filename'] : 'dilekce';

// Türkçe karakterleri koru
$content = mb_convert_encoding($content, 'UTF-8', 'UTF-8');

// UDF formatı için XML yapısı
// UYAP Döküman Editörü'nün tanıyacağı basit ama geçerli bir XML formatı
$udfContent = '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
$udfContent .= '<!DOCTYPE dokuman SYSTEM "dokuman.dtd">' . "\n";
$udfContent .= '<dokuman>' . "\n";
$udfContent .= '  <baslik>' . htmlspecialchars($title, ENT_XML1, 'UTF-8') . '</baslik>' . "\n";
$udfContent .= '  <tarih>' . date('d.m.Y') . '</tarih>' . "\n";
$udfContent .= '  <icerik><![CDATA[' . $content . ']]></icerik>' . "\n";
$udfContent .= '</dokuman>';

// Çıktı öncesi tüm buffer temizle
if (ob_get_length()) {
    ob_clean();
}

// İndirme başlıkları
header('Content-Type: application/octet-stream');
header('Content-Disposition: attachment; filename="' . $filename . '.udf"');
header('Content-Length: ' . strlen($udfContent));
header('Pragma: no-cache');
header('Expires: 0');

// Dosya içeriğini yaz
echo $udfContent;

// Sayfanın geri kalanının çalışmasını engelle
exit();
?>
