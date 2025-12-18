#!/bin/bash

# Sayfa Meta Bilgileri Ekleme Scripti
# Her sayfa için meta title ve meta description ekler

BASE_URL="http://127.0.0.1:8000/api/site-settings/1"

# Site Settings ID'sini al (varsayılan 1)
SITE_ID=1

echo "Sayfa Meta Bilgileri ekleniyor..."

# 1. Anasayfa (/)
echo "1. Anasayfa ekleniyor..."
curl -X PATCH "${BASE_URL}/?lang=tr" \
  -H "Content-Type: application/json" \
  -d '{
    "page_metas": [
      {
        "page": "home",
        "meta_title": "Kitti - Çocuk Aksesuarları | Anasayfa",
        "meta_description": "Kitti ile çocuklarınız için dört mevsim renkli aksesuarlar. Kışın sıcacık berelerden yazın serinleten şapkalara kadar yüzlerce ürün."
      }
    ]
  }' | python3 -m json.tool

sleep 1

curl -X PATCH "${BASE_URL}/?lang=en" \
  -H "Content-Type: application/json" \
  -d '{
    "page_metas": [
      {
        "page": "home",
        "meta_title": "Kitti - Children Accessories | Home",
        "meta_description": "Kitti offers colorful accessories for children all year round. From warm winter hats to cool summer caps, hundreds of products."
      }
    ]
  }' | python3 -m json.tool

sleep 1

# 2. Ürünler (/products)
echo "2. Ürünler sayfası ekleniyor..."
curl -X PATCH "${BASE_URL}/?lang=tr" \
  -H "Content-Type: application/json" \
  -d '{
    "page_metas": [
      {
        "page": "products",
        "meta_title": "Ürünler - Kitti Çocuk Aksesuarları",
        "meta_description": "Kitti ürün kataloğu. Çocuklar için bere, şapka, eldiven ve daha fazlası. Tüm ürünlerimizi keşfedin."
      }
    ]
  }' | python3 -m json.tool

sleep 1

curl -X PATCH "${BASE_URL}/?lang=en" \
  -H "Content-Type: application/json" \
  -d '{
    "page_metas": [
      {
        "page": "products",
        "meta_title": "Products - Kitti Children Accessories",
        "meta_description": "Kitti product catalog. Hats, caps, gloves and more for children. Discover all our products."
      }
    ]
  }' | python3 -m json.tool

sleep 1

# 3. Hikayemiz (/our-story)
echo "3. Hikayemiz sayfası ekleniyor..."
curl -X PATCH "${BASE_URL}/?lang=tr" \
  -H "Content-Type: application/json" \
  -d '{
    "page_metas": [
      {
        "page": "our-story",
        "meta_title": "Hikayemiz - Kitti",
        "meta_description": "Kitti nin hikayesi. Çocukların hayal dünyasını renklendirmek için yola çıktık. Her bir ürünümüzde sevgi, neşe ve kaliteyi bir araya getiriyoruz."
      }
    ]
  }' | python3 -m json.tool

sleep 1

curl -X PATCH "${BASE_URL}/?lang=en" \
  -H "Content-Type: application/json" \
  -d '{
    "page_metas": [
      {
        "page": "our-story",
        "meta_title": "Our Story - Kitti",
        "meta_description": "The story of Kitti. We set out to color childrens world of imagination. We bring together love, joy and quality in each of our products."
      }
    ]
  }' | python3 -m json.tool

sleep 1

# 4. İletişim (/contact)
echo "4. İletişim sayfası ekleniyor..."
curl -X PATCH "${BASE_URL}/?lang=tr" \
  -H "Content-Type: application/json" \
  -d '{
    "page_metas": [
      {
        "page": "contact",
        "meta_title": "İletişim - Kitti",
        "meta_description": "Kitti ile iletişime geçin. Sorularınız, önerileriniz ve destek talepleriniz için bizimle iletişime geçebilirsiniz."
      }
    ]
  }' | python3 -m json.tool

sleep 1

curl -X PATCH "${BASE_URL}/?lang=en" \
  -H "Content-Type: application/json" \
  -d '{
    "page_metas": [
      {
        "page": "contact",
        "meta_title": "Contact - Kitti",
        "meta_description": "Contact Kitti. You can contact us for your questions, suggestions and support requests."
      }
    ]
  }' | python3 -m json.tool

sleep 1

# 5. Toptan Portal (/toptan-portal)
echo "5. Toptan Portal sayfası ekleniyor..."
curl -X PATCH "${BASE_URL}/?lang=tr" \
  -H "Content-Type: application/json" \
  -d '{
    "page_metas": [
      {
        "page": "toptan-portal",
        "meta_title": "Toptan Portal - Kitti",
        "meta_description": "Kitti toptan satış portalı. Toplu alımlar için özel fiyatlar ve avantajlar. Toptan satış için bizimle iletişime geçin."
      }
    ]
  }' | python3 -m json.tool

sleep 1

curl -X PATCH "${BASE_URL}/?lang=en" \
  -H "Content-Type: application/json" \
  -d '{
    "page_metas": [
      {
        "page": "toptan-portal",
        "meta_title": "Wholesale Portal - Kitti",
        "meta_description": "Kitti wholesale portal. Special prices and advantages for bulk purchases. Contact us for wholesale sales."
      }
    ]
  }' | python3 -m json.tool

sleep 1

# 6. Aydınlatma Metni (/aydinlatma-metni)
echo "6. Aydınlatma Metni sayfası ekleniyor..."
curl -X PATCH "${BASE_URL}/?lang=tr" \
  -H "Content-Type: application/json" \
  -d '{
    "page_metas": [
      {
        "page": "aydinlatma-metni",
        "meta_title": "Aydınlatma Metni - Kitti",
        "meta_description": "Kitti aydınlatma metni. Kişisel verilerinizin işlenmesi hakkında bilgilendirme metni."
      }
    ]
  }' | python3 -m json.tool

sleep 1

curl -X PATCH "${BASE_URL}/?lang=en" \
  -H "Content-Type: application/json" \
  -d '{
    "page_metas": [
      {
        "page": "aydinlatma-metni",
        "meta_title": "Privacy Notice - Kitti",
        "meta_description": "Kitti privacy notice. Information text about the processing of your personal data."
      }
    ]
  }' | python3 -m json.tool

sleep 1

# 7. Çerez Politikası (/cerez-politikasi)
echo "7. Çerez Politikası sayfası ekleniyor..."
curl -X PATCH "${BASE_URL}/?lang=tr" \
  -H "Content-Type: application/json" \
  -d '{
    "page_metas": [
      {
        "page": "cerez-politikasi",
        "meta_title": "Çerez Politikası - Kitti",
        "meta_description": "Kitti çerez politikası. Web sitemizde kullanılan çerezler hakkında bilgilendirme."
      }
    ]
  }' | python3 -m json.tool

sleep 1

curl -X PATCH "${BASE_URL}/?lang=en" \
  -H "Content-Type: application/json" \
  -d '{
    "page_metas": [
      {
        "page": "cerez-politikasi",
        "meta_title": "Cookie Policy - Kitti",
        "meta_description": "Kitti cookie policy. Information about cookies used on our website."
      }
    ]
  }' | python3 -m json.tool

sleep 1

# 8. İleti Onay Metni (/ileti-onay-metni)
echo "8. İleti Onay Metni sayfası ekleniyor..."
curl -X PATCH "${BASE_URL}/?lang=tr" \
  -H "Content-Type: application/json" \
  -d '{
    "page_metas": [
      {
        "page": "ileti-onay-metni",
        "meta_title": "İleti Onay Metni - Kitti",
        "meta_description": "Kitti ileti onay metni. E-posta ve SMS gönderimi için onay metni."
      }
    ]
  }' | python3 -m json.tool

sleep 1

curl -X PATCH "${BASE_URL}/?lang=en" \
  -H "Content-Type: application/json" \
  -d '{
    "page_metas": [
      {
        "page": "ileti-onay-metni",
        "meta_title": "Communication Consent - Kitti",
        "meta_description": "Kitti communication consent text. Consent text for email and SMS sending."
      }
    ]
  }' | python3 -m json.tool

echo ""
echo "✅ Tüm sayfa meta bilgileri başarıyla eklendi!"
echo ""
echo "Eklenen sayfalar:"
echo "1. Anasayfa"
echo "2. Ürünler"
echo "3. Hikayemiz"
echo "4. İletişim"
echo "5. Toptan Portal"
echo "6. Aydınlatma Metni"
echo "7. Çerez Politikası"
echo "8. İleti Onay Metni"

