# Temel Python HTTP Sunucusu

Bu proje, Python soket programlaması kullanılarak sıfırdan geliştirilen basit bir HTTP sunucusudur. Statik dosya sunabilir, JSON API yanıtları verebilir ve Docker ile container olarak çalıştırılabilir.

---

## 🚀 Özellikler

- `GET` desteği (`/`, `/static/...`, `/api/hello`)
- `POST` desteği (`/api/test-post`)
- MIME tipi yönetimi
- Çoklu bağlantı (threading)
- Statik dosya sunumu
- Docker ile çalıştırma
