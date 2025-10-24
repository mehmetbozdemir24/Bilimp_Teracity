# HuggingFace Embeddings Kullanarak Türkçe Gömme Rehberi

## Giriş
Bu rehber, HuggingFace kullanarak Türkçe metin gömme işlemi yapmayı anlatmaktadır. `ytu-ce-cosmos/turkish-e5-large` modelini kullanarak gömme işlemlerinin nasıl gerçekleştirileceği hakkında bilgi vereceğiz.

## Donanım Seçimi
Gömme işlemlerini CPU veya GPU üzerinde gerçekleştirmek için aşağıdaki yöntemleri kullanabilirsiniz.

```python
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
```

## Kod Örnekleri

### Örnek 1: Basit Gömme
```python
from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained("ytu-ce-cosmos/turkish-e5-large")
model = AutoModel.from_pretrained("ytu-ce-cosmos/turkish-e5-large").to(device)

text = "Merhaba, dünya!"
inputs = tokenizer(text, return_tensors="pt").to(device)
with torch.no_grad():
    embeddings = model(**inputs).last_hidden_state
```

### Örnek 2: Birden Fazla Metin ile Gömme
```python
texts = ["Merhaba, dünya!", "Nasılsın?"]
inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt").to(device)
with torch.no_grad():
    embeddings = model(**inputs).last_hidden_state
```

### Örnek 3: Batch İşleme
```python
import numpy as np

texts = ["Merhaba, dünya!", "Nasılsın?", "Bugün hava güzel."]
inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt").to(device)
with torch.no_grad():
    embeddings = model(**inputs).last_hidden_state
    batch_embeddings = np.mean(embeddings.cpu().numpy(), axis=1)  # Ortalama alma
```

### Örnek 4: Performans İpuçları
- Küçük metin parçaları kullanın.
- Veri kümenizi önceden işleyin.
- GPU'dan yararlanın.

### Örnek 5: Testler
```python
# Test 1: Gömme boyutu
assert embeddings.size(1) == model.config.hidden_size

# Test 2: Çıktı tipi
assert isinstance(embeddings, torch.Tensor)

# Test 3: Boş metin girişi
empty_input = tokenizer("", return_tensors="pt").to(device)
empty_embedding = model(**empty_input).last_hidden_state
assert empty_embedding.size(1) == model.config.hidden_size

# Test 4: Bellek kullanımı
import gc
gc.collect()
torch.cuda.empty_cache()
```

## Hata Ayıklama
- Eğer model yüklenemiyorsa, internet bağlantınızı kontrol edin.
- Bellek hatası alıyorsanız, daha küçük bir batch boyutu deneyin.

## Kontrol Listesi
- Modelin doğru yüklendiğinden emin olun.
- Giriş verilerinin uygun formatta olduğundan emin olun.
- Bellek kullanımını izleyin.
