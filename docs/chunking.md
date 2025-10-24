# Doküman İşleme (Chunking)

## Genel Bakış

Bilimp sisteminde doküman işleme modülü, PDF dokümanlarını okuyarak bunları küçük, yönetilebilir parçalara (chunks) böler. Bu süreç, embedding ve arama işlemlerinin etkinliğini artırır.

## Görevliler

- **Engin**: Doküman okuma ve temizleme
- **Batuhan**: Chunk'lara bölme algoritması

## Özellikler

### 1. PDF Okuma

`DocumentProcessor.read_pdf()` metodu:
- PDF dosyalarını okur
- Her sayfadan metni çıkarır
- Tüm metni birleştirir

```python
from src.chunking import DocumentProcessor

processor = DocumentProcessor()
text = processor.read_pdf("dokuman.pdf")
```

### 2. Metin Temizleme

`DocumentProcessor.clean_text()` metodu:
- Gereksiz boşlukları kaldırır
- Özel karakterleri düzeltir
- Metni normalize eder

### 3. Chunk'lara Bölme

`DocumentProcessor.chunk_text()` metodu:
- Metni belirli boyutta parçalara böler
- Kelime ortasında kesmeden böler
- Chunk'lar arası örtüşme (overlap) sağlar

#### Parametreler

- **chunk_size** (varsayılan: 512): Her chunk'ın maksimum karakter sayısı
- **chunk_overlap** (varsayılan: 50): Chunk'lar arası örtüşme miktarı

## Kullanım Örneği

```python
from src.chunking import DocumentProcessor

# Processor oluştur
processor = DocumentProcessor(chunk_size=512, chunk_overlap=50)

# Dokümanı işle
chunks = processor.process_document("belgeler/dokuman.pdf")

print(f"{len(chunks)} chunk oluşturuldu")
for i, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {i+1}:")
    print(chunk[:100] + "...")
```

## Öneriler

1. **Chunk Boyutu**: Daha küçük chunk'lar daha kesin arama sağlar, ancak bağlam kaybına neden olabilir
2. **Overlap**: Chunk'lar arası örtüşme, bağlam devamlılığını korur
3. **Doküman Formatı**: Şu an sadece PDF desteklenmektedir

## İleriye Dönük Geliştirmeler

- [ ] Word (.docx) desteği
- [ ] Excel (.xlsx) desteği
- [ ] HTML/Markdown desteği
- [ ] Görsel/tablo çıkarma
