# Qdrant Vektör Veritabanı Kurulum Kılavuzu

Bu kılavuz, Qdrant vektör veritabanını kurmak, yapılandırmak ve kullanmak için gerekli adımları içermektedir. Aşağıda, Docker kullanarak Qdrant kurulumundan başlayarak, koleksiyon yönetimi, vektör yükleme, arama ve geri alma işlemleri, filtreleme, test yöntemleri, sorun giderme ve detaylı kod örnekleri sunulmaktadır.

## 1. Qdrant Kurulumu
### 1.1. Docker ile Kurulum
Qdrant, Docker ile kolayca kurulabilir. Öncelikle, Docker'ı sisteminize kurmanız gerekmektedir. Docker kurulumunu tamamladıktan sonra, aşağıdaki komutu terminalde çalıştırarak Qdrant'ı başlatın:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Bu komut, Qdrant sunucusunu 6333 portu üzerinden başlatır.

## 2. Qdrant Yapılandırması
Qdrant, yapılandırma dosyaları ile özelleştirilebilir. Örnek bir yapılandırma dosyası aşağıdaki gibidir:

```json
{
  "host": "0.0.0.0",
  "port": 6333,
  "storage": {
    "path": "./data/qdrant",
    "type": "local"
  }
}
```

## 3. Koleksiyon Yönetimi
### 3.1. Koleksiyon Oluşturma
Koleksiyon oluşturmak için aşağıdaki API çağrısını kullanabilirsiniz:

```bash
curl -X POST "http://localhost:6333/collections" -H "Content-Type: application/json" -d '{ "name": "my_collection", "vector_size": 300, "distance": "Cosine" }'
```

### 3.2. Koleksiyondan Silme
Bir koleksiyonu silmek için:

```bash
curl -X DELETE "http://localhost:6333/collections/my_collection"
```

## 4. Vektör Yükleme
### 4.1. Vektörleri Yükleme
Vektörlerinizi Qdrant'a yüklemek için aşağıdaki örneği kullanabilirsiniz:

```bash
curl -X POST "http://localhost:6333/collections/my_collection/points" -H "Content-Type: application/json" -d '{ "points": [{ "id": 1, "vector": [0.1, 0.2, 0.3], "payload": { "text": "Örnek vektör" } }] }'
```

## 5. Arama ve Geri Alma İşlemleri
Vektörler üzerinde arama yapmak için:

```bash
curl -X POST "http://localhost:6333/collections/my_collection/points/search" -H "Content-Type: application/json" -d '{ "vector": [0.1, 0.2, 0.3], "top": 5 }'
```

## 6. Filtreleme
Filtreleme yapmak için:

```bash
curl -X POST "http://localhost:6333/collections/my_collection/points/search" -H "Content-Type: application/json" -d '{ "vector": [0.1, 0.2, 0.3], "filter": { "must": [{ "key": "text", "match": "Örnek" }] }, "top": 5 }'
```

## 7. Test Yöntemleri
Qdrant ile entegrasyonunuzu test etmek için birim testleri yazabilirsiniz. Örnek bir test:

```python
import requests

def test_collection_creation():
    response = requests.post("http://localhost:6333/collections", json={"name": "test_collection", "vector_size": 300})
    assert response.status_code == 201
```

## 8. Sorun Giderme
Eğer sorun yaşıyorsanız, Qdrant'ın log dosyalarını kontrol edebilirsiniz. Log dosyaları genellikle `./data/qdrant/logs` dizininde bulunur.

## 9. Detaylı Kod Örnekleri
Aşağıda, Python ile Qdrant kullanarak bir örnek verilmiştir:

```python
import requests

# Koleksiyon oluşturma
response = requests.post("http://localhost:6333/collections", json={"name": "my_collection", "vector_size": 300})

# Vektör yükleme
requests.post("http://localhost:6333/collections/my_collection/points", json={"points": [{"id": 1, "vector": [0.1, 0.2, 0.3]}]})

# Arama yapma
search_response = requests.post("http://localhost:6333/collections/my_collection/points/search", json={"vector": [0.1, 0.2, 0.3]})
print(search_response.json())
```

Bu kılavuz, Qdrant vektör veritabanının temel kurulum ve kullanım adımlarını kapsamaktadır. Daha fazla bilgi ve gelişmiş özellikler için [Qdrant Belgeleri](https://qdrant.tech/documentation/) sayfasını ziyaret edebilirsiniz.