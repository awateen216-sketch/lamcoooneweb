import os
from urllib.parse import urlsplit

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "lamco1-dev-key-change-before-deployment",
)

LANGUAGES = {
    "ar": "العربية",
    "en": "English",
    "zh": "中文",
    "hi": "हिन्दी",
}

TRANSLATIONS = {
    "ar": {
        "home": "الرئيسية",
        "about": "من نحن",
        "about_description": "تقدم لامكو منتجات وحلولًا من الحديد لقطاعي البناء والصناعة، بما في ذلك قطاعات الجدران الجافة ومكونات الأسقف المعلقة وحوامل الكابلات والزوايا الإنشائية.",
        "about_location": "يقع مصنعنا في المدينة الصناعية الثالثة، جدة، المملكة العربية السعودية.",
        "quality_title": "جودة يمكنك الاعتماد عليها",
        "quality_description": "نركز على مواصفات المنتجات ودقة التصنيع وتقديم حلول تلبي متطلبات البناء والصناعة.",
        "quality_standards": "تتوافق بعض منتجات قطاعات الجدران الجافة مع معايير فنية مثل ASTM C645. وقد تتوفر خيارات الطلاء بالزنك عند الطلب، وفقًا لمواصفات المنتج.",
        "products": "المنتجات",
        "contact": "تواصل معنا",
        "contact_number": "رقم التواصل",
        "email": "البريد الإلكتروني",
        "technical_support": "الدعم الفني",
        "location_label": "الموقع",
        "hero_title": "حديد أقوى، مستقبل أكثر إشراقًا",
        "hero_text": "حلول الحديد والتصنيع لقطاع البناء والصناعة.",
        "explore": "استعرض المنتجات",
        "our_products": "منتجاتنا",
        "view_details": "عرض التفاصيل",
        "specifications": "المواصفات",
        "location": "جدة، المدينة الصناعية الثالثة، المملكة العربية السعودية",
        "quote": "اطلب عرض سعر",
        "specs_unavailable": "المواصفات غير متوفرة في الكتالوج المرفق. يرجى التواصل معنا للتفاصيل.",
        "no_image": "لا تتوفر صورة لهذا المنتج في الكتالوج المرفق",
        "illustration_note": "رسم توضيحي عام، وليس صورة لمنتج مصنع LAMCO1",
        "quote_options_title": "خيارات طلب عرض السعر",
        "quote_size": "المقاس أو العرض",
        "quote_thickness": "السماكة",
        "quote_length": "الطول",
        "quote_quantity": "الكمية",
        "quote_configuration": "التكوين أو التفاصيل المطلوبة",
        "quote_notes": "ملاحظات العميل",
        "quote_diameter": "القطر",
        "quote_section": "مقطع المنتج",
        "quote_package": "حجم العبوة",
        "quote_select": "اختر",
        "quote_enter": "أدخل القيمة المطلوبة",
        "quote_range": "النطاق المذكور في الكتالوج:",
        "quote_request_intro": "مرحبًا LAMCO1، أود طلب عرض سعر.",
        "quote_product": "المنتج",
        "quote_specs": "المواصفات المنشورة",
        "quote_unavailable_value": "غير محدد في الكتالوج؛ يرجى تأكيده",
        "quote_validation": "يرجى مراجعة الحقول المطلوبة والقيم المدخلة.",
    },
    "en": {
        "home": "Home",
        "about": "About Us",
        "about_description": "LAMCO provides steel products and solutions for the construction and industrial sectors, including drywall profiles, suspended ceiling components, cable trays, and structural angles.",
        "about_location": "Our factory is located in the Third Industrial City, Jeddah, Saudi Arabia.",
        "quality_title": "Quality You Can Rely On",
        "quality_description": "We focus on product specifications, manufacturing accuracy, and solutions suited to construction and industrial requirements.",
        "quality_standards": "Selected drywall profile products follow technical standards such as ASTM C645. Zinc coating options may be available upon request, subject to product specifications.",
        "products": "Products",
        "contact": "Contact Us",
        "contact_number": "Contact Number",
        "email": "Email",
        "technical_support": "Technical Support",
        "location_label": "Location",
        "hero_title": "Stronger Steel, Brighter Future",
        "hero_text": "Steel solutions and fabrication for construction and industry.",
        "explore": "Explore Products",
        "our_products": "Our Products",
        "view_details": "View Details",
        "specifications": "Specifications",
        "location": "Jeddah, Third Industrial City, Saudi Arabia",
        "quote": "Request a Quote",
        "specs_unavailable": "Specifications are not available in the supplied catalog. Contact us for details.",
        "no_image": "Product image not available in the attached catalog",
        "illustration_note": "Generic illustration, not a photograph of a LAMCO1 factory product",
        "quote_options_title": "Quote Request Options",
        "quote_size": "Size or width",
        "quote_thickness": "Thickness",
        "quote_length": "Length",
        "quote_quantity": "Quantity",
        "quote_configuration": "Required configuration or details",
        "quote_notes": "Customer notes",
        "quote_diameter": "Diameter",
        "quote_section": "Product section",
        "quote_package": "Package size",
        "quote_select": "Select",
        "quote_enter": "Enter requested value",
        "quote_range": "Catalog range:",
        "quote_request_intro": "Hello LAMCO1, I would like to request a quote.",
        "quote_product": "Product",
        "quote_specs": "Published specifications",
        "quote_unavailable_value": "Not specified in the catalog; please confirm",
        "quote_validation": "Please check the required fields and entered values.",
    },
    "zh": {
        "home": "首页",
        "about": "关于我们",
        "about_description": "LAMCO 为建筑和工业领域提供钢材产品与解决方案，包括石膏板龙骨、吊顶组件、电缆桥架和结构角钢。",
        "about_location": "我们的工厂位于沙特阿拉伯吉达第三工业城。",
        "quality_title": "值得信赖的品质",
        "quality_description": "我们注重产品规格、制造精度，以及满足建筑和工业需求的解决方案。",
        "quality_standards": "部分石膏板龙骨产品符合 ASTM C645 等技术标准。可根据产品规格按需提供锌涂层选项。",
        "products": "产品",
        "contact": "联系我们",
        "contact_number": "联系电话",
        "email": "电子邮箱",
        "technical_support": "技术支持",
        "location_label": "地址",
        "hero_title": "更强钢材，更光明的未来",
        "hero_text": "为建筑和工业提供钢材解决方案与加工服务。",
        "explore": "浏览产品",
        "our_products": "我们的产品",
        "view_details": "查看详情",
        "specifications": "产品规格",
        "location": "沙特阿拉伯吉达第三工业城",
        "quote": "申请报价",
        "specs_unavailable": "所提供的产品目录未列出此产品的规格。请联系我们了解详情。",
        "no_image": "所提供的产品目录中没有此产品的图片",
        "illustration_note": "通用示意图，并非 LAMCO1 工厂产品照片",
        "quote_options_title": "报价请求选项",
        "quote_size": "尺寸或宽度",
        "quote_thickness": "厚度",
        "quote_length": "长度",
        "quote_quantity": "数量",
        "quote_configuration": "所需配置或详细信息",
        "quote_notes": "客户备注",
        "quote_diameter": "直径",
        "quote_section": "产品截面",
        "quote_package": "包装规格",
        "quote_select": "请选择",
        "quote_enter": "请输入所需数值",
        "quote_range": "目录所列范围：",
        "quote_request_intro": "您好 LAMCO1，我想申请报价。",
        "quote_product": "产品",
        "quote_specs": "已公布规格",
        "quote_unavailable_value": "目录未注明，请确认",
        "quote_validation": "请检查必填项和输入值。",
    },
    "hi": {
        "home": "मुखपृष्ठ",
        "about": "हमारे बारे में",
        "about_description": "LAMCO निर्माण और औद्योगिक क्षेत्रों के लिए स्टील उत्पाद और समाधान प्रदान करता है, जिनमें ड्राईवॉल प्रोफाइल, सस्पेंडेड सीलिंग कंपोनेंट, केबल ट्रे और स्ट्रक्चरल एंगल शामिल हैं।",
        "about_location": "हमारा कारखाना जेद्दा, सऊदी अरब के तीसरे औद्योगिक शहर में स्थित है।",
        "quality_title": "विश्वसनीय गुणवत्ता",
        "quality_description": "हम उत्पाद विनिर्देशों, निर्माण की सटीकता और निर्माण तथा औद्योगिक आवश्यकताओं के अनुकूल समाधानों पर ध्यान देते हैं।",
        "quality_standards": "चयनित ड्राईवॉल प्रोफाइल उत्पाद ASTM C645 जैसे तकनीकी मानकों का पालन करते हैं। उत्पाद विनिर्देशों के अधीन, अनुरोध पर जिंक कोटिंग विकल्प उपलब्ध हो सकते हैं।",
        "products": "उत्पाद",
        "contact": "संपर्क करें",
        "contact_number": "संपर्क नंबर",
        "email": "ईमेल",
        "technical_support": "तकनीकी सहायता",
        "location_label": "स्थान",
        "hero_title": "मज़बूत स्टील, उज्ज्वल भविष्य",
        "hero_text": "निर्माण और उद्योग के लिए स्टील समाधान और निर्माण सेवाएँ।",
        "explore": "उत्पाद देखें",
        "our_products": "हमारे उत्पाद",
        "view_details": "विवरण देखें",
        "specifications": "विशेष विवरण",
        "location": "जेद्दा, तीसरा औद्योगिक शहर, सऊदी अरब",
        "quote": "मूल्य प्रस्ताव माँगें",
        "specs_unavailable": "दिए गए कैटलॉग में इस उत्पाद के विनिर्देश उपलब्ध नहीं हैं। विवरण के लिए संपर्क करें।",
        "no_image": "दिए गए कैटलॉग में इस उत्पाद की तस्वीर शामिल नहीं है",
        "illustration_note": "सामान्य चित्रण, LAMCO1 कारखाने के उत्पाद की तस्वीर नहीं",
        "quote_options_title": "कोटेशन अनुरोध विकल्प",
        "quote_size": "आकार या चौड़ाई",
        "quote_thickness": "मोटाई",
        "quote_length": "लंबाई",
        "quote_quantity": "मात्रा",
        "quote_configuration": "आवश्यक कॉन्फ़िगरेशन या विवरण",
        "quote_notes": "ग्राहक की टिप्पणियाँ",
        "quote_diameter": "व्यास",
        "quote_section": "उत्पाद अनुभाग",
        "quote_package": "पैकेज का आकार",
        "quote_select": "चुनें",
        "quote_enter": "वांछित मान दर्ज करें",
        "quote_range": "कैटलॉग में दी गई सीमा:",
        "quote_request_intro": "नमस्ते LAMCO1, मैं कोटेशन का अनुरोध करना चाहता/चाहती हूँ।",
        "quote_product": "उत्पाद",
        "quote_specs": "प्रकाशित विनिर्देश",
        "quote_unavailable_value": "कैटलॉग में निर्दिष्ट नहीं; कृपया पुष्टि करें",
        "quote_validation": "कृपया आवश्यक फ़ील्ड और दर्ज मान जाँचें।",
    },
}

def choice_field(key, options):
    return {"key": key, "type": "select", "options": options, "required": False}


def range_field(key, minimum, maximum, hint):
    unit = "m" if key == "quote_length" else "mm"
    return {
        "key": key,
        "type": "number",
        "min": minimum,
        "max": maximum,
        "step": "any",
        "hint": hint,
        "unit": unit,
        "required": False,
    }


def text_field(key, hint=None, required=False):
    return {"key": key, "type": "text", "hint": hint, "required": required}


PRODUCTS = [
    {"id": "drywall-steel-profiles", "name": "Drywall Steel Profiles", "name_ar": "قطاعات الصلب للجدران الجافة", "specs": None, "image": None, "quote_fields": [text_field("quote_configuration")]},
    {"id": "drywall-partition-system", "name": "Drywall Partition System", "name_ar": "نظام قواطع الجدران الجافة", "specs": None, "image": None, "quote_fields": [text_field("quote_configuration")]},
    {"id": "suspended-ceiling-systems", "name": "Suspended Ceiling Systems", "name_ar": "أنظمة الأسقف المعلقة", "specs": None, "image": None, "quote_fields": [text_field("quote_configuration")]},
    {"id": "cable-trays", "name": "Cable Trays", "name_ar": "حوامل الكابلات", "specs": None, "image": None, "illustration": "cable-tray.svg", "quote_fields": [text_field("quote_configuration")]},
    {"id": "structural-angles", "name": "Structural Angles", "name_ar": "زوايا إنشائية", "specs": None, "image": None, "illustration": "structural-angle.svg", "quote_fields": [text_field("quote_configuration")]},
    {"id": "metal-elbows", "name": "Metal Elbows", "name_ar": "أكواع معدنية", "specs": None, "image": None, "illustration": "metal-elbow.svg", "quote_fields": [text_field("quote_configuration")]},
    {
        "id": "plasterboard", "name": "Plasterboard", "name_ar": "ألواح الجبس",
        "specs": "1200×2400 or 1200×3000 mm; thicknesses 9.5, 12.5, 15, 16, 18 mm",
        "image": "plasterboard.jpg",
        "quote_fields": [choice_field("quote_size", ["1200×2400 mm", "1200×3000 mm"]), choice_field("quote_thickness", ["9.5 mm", "12.5 mm", "15 mm", "16 mm", "18 mm"])],
    },
    {
        "id": "galvanized-runner", "name": "Galvanized Runner", "name_ar": "مسار معدني مجلفن",
        "specs": "Width 42–200 mm; length 3–12 m; thickness 0.35–1.5 mm",
        "image": "galvanized-runner.jpg",
        "quote_fields": [range_field("quote_size", 42, 200, "42–200 mm"), range_field("quote_length", 3, 12, "3–12 m"), range_field("quote_thickness", 0.35, 1.5, "0.35–1.5 mm")],
    },
    {
        "id": "galvanized-stud", "name": "Galvanized Stud", "name_ar": "قائم معدني مجلفن",
        "specs": "Width 42–200 mm; length 3–12 m; thickness 0.35–1.5 mm",
        "image": "galvanized-stud.jpg",
        "quote_fields": [range_field("quote_size", 42, 200, "42–200 mm"), range_field("quote_length", 3, 12, "3–12 m"), range_field("quote_thickness", 0.35, 1.5, "0.35–1.5 mm")],
    },
    {"id": "drywall-screws", "name": "Drywall Screws", "name_ar": "براغي ألواح الجبس", "specs": "Multiple sizes depending on the system", "image": "drywall-screws.jpg", "quote_fields": [text_field("quote_configuration", "Multiple sizes depending on the system")]},
    {"id": "framing-screws", "name": "Framing Screws", "name_ar": "براغي تثبيت الإطار", "specs": "Listed length 11 mm", "image": "framing-screws.jpg", "quote_fields": [choice_field("quote_length", ["11 mm"])]},
    {"id": "drywall-joint-tape", "name": "Drywall Joint Tape", "name_ar": "شريط فواصل الجبس", "specs": "50 mm × 90 m", "image": "drywall-joint-tape.jpg", "quote_fields": [choice_field("quote_size", ["50 mm × 90 m"])]},
    {"id": "corner-tape", "name": "Corner Tape", "name_ar": "شريط الزوايا", "specs": "50 mm × 30 m", "image": "corner-tape.jpg", "quote_fields": [choice_field("quote_size", ["50 mm × 30 m"])]},
    {"id": "drywall-l-bead", "name": "Drywall L-Bead", "name_ar": "حافة جبس L-Bead", "specs": "25×25×3000 mm or 25×16×3000 mm; thickness 0.4 or 0.45 mm", "image": "drywall-l-bead.jpg", "quote_fields": [choice_field("quote_size", ["25×25×3000 mm", "25×16×3000 mm"]), choice_field("quote_thickness", ["0.4 mm", "0.45 mm"])]},
    {"id": "ready-mixed-joint-compound", "name": "Ready Mixed Joint Compound", "name_ar": "معجون فواصل جاهز", "specs": "28 kg, 15 kg, and 5 kg containers", "image": "ready-mixed-joint-compound.jpg", "quote_fields": [choice_field("quote_package", ["28 kg", "15 kg", "5 kg"])]},
    {"id": "furring-channel", "name": "Furring Channel", "name_ar": "قناة تثبيت ألواح الجبس", "specs": "Section 12×22×35×22×12 mm; length 3–12 m; thickness 0.35–1 mm", "image": "furring-channel.jpg", "quote_fields": [choice_field("quote_section", ["12×22×35×22×12 mm"]), range_field("quote_length", 3, 12, "3–12 m"), range_field("quote_thickness", 0.35, 1, "0.35–1 mm")]},
    {"id": "primary-channel", "name": "Primary Channel (C-channel)", "name_ar": "القناة الرئيسية C", "specs": "Section 11×38×11 mm; length 3–12 m; thickness 0.35–1 mm", "image": "primary-channel.jpg", "quote_fields": [choice_field("quote_section", ["11×38×11 mm"]), range_field("quote_length", 3, 12, "3–12 m"), range_field("quote_thickness", 0.35, 1, "0.35–1 mm")]},
    {"id": "perimeter-angle", "name": "Perimeter Angle", "name_ar": "زاوية محيط السقف", "specs": "25×25 mm; length 3–12 m; thickness 0.4–0.6 mm", "image": "perimeter-angle.jpg", "quote_fields": [choice_field("quote_size", ["25×25 mm"]), range_field("quote_length", 3, 12, "3–12 m"), range_field("quote_thickness", 0.4, 0.6, "0.4–0.6 mm")]},
    {"id": "shadow-line-wall-angle", "name": "Shadow Line Wall Angles", "name_ar": "زوايا السقف بخط الظل", "specs": "Multiple sizes; length 3–12 m; thickness 0.4–0.6 mm", "image": "shadow-line-wall-angle.jpg", "quote_fields": [text_field("quote_size"), range_field("quote_length", 3, 12, "3–12 m"), range_field("quote_thickness", 0.4, 0.6, "0.4–0.6 mm")]},
    {"id": "adjustable-rod-hanger", "name": "Adjustable Rod Hanger", "name_ar": "علاقة قضيب قابلة للتعديل", "specs": "Diameter 3.7 mm; quantity depends on design and load", "image": "adjustable-rod-hanger.jpg", "quote_fields": [choice_field("quote_diameter", ["3.7 mm"]), text_field("quote_configuration", "Design and load requirements")]},
    {"id": "threaded-rod-system", "name": "Threaded Rod System", "name_ar": "نظام القضيب الملولب", "specs": "Diameter 6 mm; quantity depends on design and load", "image": "threaded-rod-system.jpg", "quote_fields": [choice_field("quote_diameter", ["6 mm"]), text_field("quote_configuration", "Design and load requirements")]},
    {"id": "wire-connecting-clips", "name": "Wire Connecting Clips", "name_ar": "مشابك ربط القنوات", "specs": "38×2.5 mm", "image": "wire-connecting-clips.jpg", "quote_fields": [choice_field("quote_size", ["38×2.5 mm"])]},
]

for product in PRODUCTS:
    fields_by_key = {field["key"]: field for field in product["quote_fields"]}
    product["quote_fields"] = [
        fields_by_key.get(key) or text_field(key)
        for key in ("quote_size", "quote_thickness", "quote_length")
    ] + [
        field
        for field in product["quote_fields"]
        if field["key"] not in {"quote_size", "quote_thickness", "quote_length"}
    ]
    for field in product["quote_fields"]:
        field["required"] = False


@app.context_processor
def inject_language_data():
    lang = session.get("lang", "en")
    return {
        "lang": lang,
        "languages": LANGUAGES,
        "t": TRANSLATIONS.get(lang, TRANSLATIONS["en"]),
    }


@app.route("/language/<lang>")
def change_language(lang):
    if lang in LANGUAGES:
        session["lang"] = lang

    referrer = request.referrer
    if referrer and urlsplit(referrer).netloc == request.host:
        return redirect(referrer)
    return redirect(url_for("home"))


@app.route("/")
def home():
    featured_products = [product for product in PRODUCTS if product["image"]][:3]
    return render_template("index.html", products=featured_products)


@app.route("/products")
def products():
    return render_template("products.html", products=PRODUCTS)


@app.route("/products/<product_id>")
def product_details(product_id):
    product = next(
        (item for item in PRODUCTS if item["id"] == product_id),
        None,
    )

    if product is None:
        return "Product not found", 404

    return render_template("product_details.html", product=product)

if __name__ == "__main__":
    app.run(debug=True)
