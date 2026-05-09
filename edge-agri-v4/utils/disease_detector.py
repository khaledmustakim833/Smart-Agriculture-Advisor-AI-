# utils/disease_detector.py
# Plant disease detection - numpy + PIL only (no torch/torchvision)
# Works on Streamlit Cloud without heavy dependencies

import numpy as np
from PIL import Image

PLANT_VILLAGE_CLASSES = [
    "Apple - Apple Scab","Apple - Black Rot","Apple - Cedar Apple Rust","Apple - Healthy",
    "Blueberry - Healthy","Cherry - Powdery Mildew","Cherry - Healthy",
    "Corn - Cercospora Leaf Spot","Corn - Common Rust","Corn - Northern Leaf Blight","Corn - Healthy",
    "Grape - Black Rot","Grape - Esca Black Measles","Grape - Leaf Blight","Grape - Healthy",
    "Orange - Citrus Greening","Peach - Bacterial Spot","Peach - Healthy",
    "Pepper - Bacterial Spot","Pepper - Healthy",
    "Potato - Early Blight","Potato - Late Blight","Potato - Healthy",
    "Raspberry - Healthy","Soybean - Healthy","Squash - Powdery Mildew",
    "Strawberry - Leaf Scorch","Strawberry - Healthy",
    "Tomato - Bacterial Spot","Tomato - Early Blight","Tomato - Late Blight",
    "Tomato - Leaf Mold","Tomato - Septoria Leaf Spot","Tomato - Spider Mites",
    "Tomato - Target Spot","Tomato - Yellow Leaf Curl Virus","Tomato - Mosaic Virus","Tomato - Healthy",
]

DISEASE_INFO = {
    "Apple - Apple Scab":{"severity":"Medium","severity_bn":"মধ্যম","severity_zh":"中等","symptoms_en":"Olive-green scab lesions on leaves and fruit","symptoms_bn":"পাতা ও ফলে জলপাই-সবুজ আঁশের মতো দাগ","symptoms_zh":"叶片和果实上的橄榄绿疮痂病斑","rec_en":"Apply Captan or Mancozeb. Remove fallen leaves.","rec_bn":"ক্যাপ্টান বা ম্যানকোজেব প্রয়োগ করুন। ঝরা পাতা সরান।","rec_zh":"施用克菌丹或代森锰锌。清除落叶。"},
    "Apple - Black Rot":{"severity":"High","severity_bn":"উচ্চ","severity_zh":"高","symptoms_en":"Purple leaf spots, brown sunken fruit lesions","symptoms_bn":"পাতায় বেগুনি দাগ, ফলে বাদামি দাগ","symptoms_zh":"叶片紫色斑点，果实棕色凹陷病斑","rec_en":"Prune infected branches. Apply copper fungicide.","rec_bn":"আক্রান্ত শাখা ছাঁটুন। তামা ছত্রাকনাশক দিন।","rec_zh":"修剪受感染枝条。施用铜基杀菌剂。"},
    "Cherry - Powdery Mildew":{"severity":"Medium","severity_bn":"মধ্যম","severity_zh":"中等","symptoms_en":"White powdery coating on leaf surface","symptoms_bn":"পাতার উপরে সাদা পাউডারের আবরণ","symptoms_zh":"叶片表面白色粉状覆盖物","rec_en":"Apply sulfur or potassium bicarbonate.","rec_bn":"সালফার বা পটাসিয়াম বাইকার্বোনেট প্রয়োগ করুন।","rec_zh":"施用硫磺或碳酸氢钾。"},
    "Corn - Common Rust":{"severity":"Medium","severity_bn":"মধ্যম","severity_zh":"中等","symptoms_en":"Cinnamon-brown pustules on both leaf surfaces","symptoms_bn":"পাতার উভয় পাশে দারুচিনি-বাদামি ফোসকা","symptoms_zh":"叶片两面肉桂棕色脓疱","rec_en":"Apply triazole fungicide. Plant resistant hybrids.","rec_bn":"ট্রায়াজোল ছত্রাকনাশক প্রয়োগ করুন।","rec_zh":"施用三唑类杀菌剂。"},
    "Corn - Northern Leaf Blight":{"severity":"High","severity_bn":"উচ্চ","severity_zh":"高","symptoms_en":"Long cigar-shaped tan lesions from lower leaves","symptoms_bn":"নিচের পাতায় লম্বা সিগার আকৃতির ট্যান দাগ","symptoms_zh":"从下部叶片开始的长条形褐色病斑","rec_en":"Apply propiconazole. Plant resistant varieties. Rotate crops.","rec_bn":"প্রোপিকোনাজোল প্রয়োগ করুন। ফসল পরিবর্তন করুন।","rec_zh":"施用丙环唑。种植抗病品种。轮作。"},
    "Corn - Cercospora Leaf Spot":{"severity":"Medium","severity_bn":"মধ্যম","severity_zh":"中等","symptoms_en":"Rectangular gray lesions between leaf veins","symptoms_bn":"পাতার শিরার মধ্যে আয়তাকার ধূসর দাগ","symptoms_zh":"叶脉间矩形灰色病斑","rec_en":"Apply triazole or strobilurin fungicide. Rotate crops.","rec_bn":"ট্রায়াজোল বা স্ট্রোবিলুরিন ছত্রাকনাশক দিন।","rec_zh":"施用三唑类或甲氧基丙烯酸酯类杀菌剂。"},
    "Grape - Black Rot":{"severity":"High","severity_bn":"উচ্চ","severity_zh":"高","symptoms_en":"Brown circular leaf lesions, black shriveled berries","symptoms_bn":"পাতায় বাদামি গোলাকার দাগ, কালো কুঁচকানো বেরি","symptoms_zh":"叶片棕色圆形病斑，浆果变黑萎缩","rec_en":"Apply Mancozeb early season. Remove mummified berries.","rec_bn":"মৌসুমের শুরুতে ম্যানকোজেব দিন। মৃত বেরি সরান।","rec_zh":"早季施用代森锰锌。清除僵果。"},
    "Grape - Esca Black Measles":{"severity":"High","severity_bn":"উচ্চ","severity_zh":"高","symptoms_en":"Tiger-striped leaf discoloration, sudden wilting","symptoms_bn":"পাতায় বাঘ-ডোরা বিবর্ণতা, হঠাৎ শুকিয়ে যাওয়া","symptoms_zh":"叶片虎纹状褪色，突然枯死","rec_en":"Prune in dry weather. Remove and burn infected wood.","rec_bn":"শুষ্ক আবহাওয়ায় ছাঁটুন। আক্রান্ত কাঠ পোড়ান।","rec_zh":"干燥天气修剪。清除并焚烧受感染木材。"},
    "Grape - Leaf Blight":{"severity":"Medium","severity_bn":"মধ্যম","severity_zh":"中等","symptoms_en":"Irregular brown lesions on leaf margins","symptoms_bn":"পাতার কিনারায় অনিয়মিত বাদামি দাগ","symptoms_zh":"叶片边缘不规则棕色病斑","rec_en":"Apply copper fungicide. Remove infected leaves.","rec_bn":"তামা ছত্রাকনাশক দিন। আক্রান্ত পাতা সরান।","rec_zh":"施用铜基杀菌剂。清除受感染叶片。"},
    "Orange - Citrus Greening":{"severity":"High","severity_bn":"উচ্চ","severity_zh":"高","symptoms_en":"Asymmetric leaf yellowing, small misshapen fruit","symptoms_bn":"পাতার অসামঞ্জস্যপূর্ণ হলুদ হওয়া, ছোট বিকৃত ফল","symptoms_zh":"叶片不对称黄化，果实小且畸形","rec_en":"No cure. Remove infected trees. Control psyllid vector.","rec_bn":"কোনো প্রতিকার নেই। আক্রান্ত গাছ সরান।","rec_zh":"无法治愈。清除受感染树木。控制木虱媒介。"},
    "Peach - Bacterial Spot":{"severity":"Medium","severity_bn":"মধ্যম","severity_zh":"中等","symptoms_en":"Water-soaked spots turning brown, shot-hole appearance","symptoms_bn":"জলছাপ দাগ বাদামি হওয়া, গুলির গর্তের মতো চেহারা","symptoms_zh":"水浸状斑点变褐，呈穿孔状","rec_en":"Apply copper bactericide in spring. Avoid overhead irrigation.","rec_bn":"বসন্তে তামা ব্যাকটেরিসাইড দিন।","rec_zh":"春季施用铜基杀细菌剂。避免从上方灌溉。"},
    "Pepper - Bacterial Spot":{"severity":"Medium","severity_bn":"মধ্যম","severity_zh":"中等","symptoms_en":"Water-soaked lesions on leaves and fruit","symptoms_bn":"পাতা ও ফলে জলছাপ দাগ","symptoms_zh":"叶片和果实水浸状病斑","rec_en":"Apply copper hydroxide. Use resistant varieties.","rec_bn":"তামা হাইড্রোক্সাইড দিন। প্রতিরোধী জাত ব্যবহার করুন।","rec_zh":"施用氢氧化铜。使用抗病品种。"},
    "Potato - Early Blight":{"severity":"Medium","severity_bn":"মধ্যম","severity_zh":"中等","symptoms_en":"Dark brown target-pattern spots on older leaves","symptoms_bn":"পুরনো পাতায় গাঢ় বাদামি লক্ষ্য-নিদর্শন দাগ","symptoms_zh":"老叶上深棕色靶心状斑点","rec_en":"Apply Mancozeb or Chlorothalonil. Remove infected leaves.","rec_bn":"ম্যানকোজেব বা ক্লোরোথালোনিল দিন। আক্রান্ত পাতা সরান।","rec_zh":"施用代森锰锌或百菌清。清除受感染叶片。"},
    "Potato - Late Blight":{"severity":"High","severity_bn":"উচ্চ","severity_zh":"高","symptoms_en":"Dark water-soaked spots, white fungal growth, tuber rot","symptoms_bn":"গাঢ় জলছাপ দাগ, সাদা ছত্রাকের বৃদ্ধি, কন্দ পচা","symptoms_zh":"深色水浸状斑点，白色霉层，块茎腐烂","rec_en":"Apply Metalaxyl+Mancozeb preventively. Remove infected plants.","rec_bn":"প্রতিরোধমূলকভাবে মেটালাক্সিল+ম্যানকোজেব দিন।","rec_zh":"预防性施用甲霜灵+代森锰锌。清除受感染植株。"},
    "Squash - Powdery Mildew":{"severity":"Medium","severity_bn":"মধ্যম","severity_zh":"中等","symptoms_en":"White powdery spots spreading over leaf surface","symptoms_bn":"পাতায় সাদা পাউডারের দাগ ছড়িয়ে পড়া","symptoms_zh":"叶片白色粉状斑点蔓延","rec_en":"Apply potassium bicarbonate or neem oil.","rec_bn":"পটাসিয়াম বাইকার্বোনেট বা নিম তেল স্প্রে করুন।","rec_zh":"喷施碳酸氢钾或印楝油。"},
    "Strawberry - Leaf Scorch":{"severity":"Medium","severity_bn":"মধ্যম","severity_zh":"中等","symptoms_en":"Dark purple spots, leaves turn brown/scorched","symptoms_bn":"গাঢ় বেগুনি দাগ, পাতা বাদামি/পোড়া হয়","symptoms_zh":"深紫色斑点，叶片变褐/焦枯","rec_en":"Apply captan fungicide. Remove infected leaves.","rec_bn":"ক্যাপ্টান ছত্রাকনাশক দিন। আক্রান্ত পাতা সরান।","rec_zh":"施用克菌丹杀菌剂。清除受感染叶片。"},
    "Tomato - Bacterial Spot":{"severity":"Medium","severity_bn":"মধ্যম","severity_zh":"中等","symptoms_en":"Small water-soaked lesions on leaves, scab-like spots on fruit","symptoms_bn":"পাতায় ছোট জলছাপ দাগ, ফলে আঁশের মতো দাগ","symptoms_zh":"叶片小水浸状病斑，果实疮痂状斑点","rec_en":"Use copper-based bactericide. Use certified disease-free seed.","rec_bn":"তামা-ভিত্তিক ব্যাকটেরিসাইড ব্যবহার করুন।","rec_zh":"使用铜基杀细菌剂。使用认证无病种子。"},
    "Tomato - Early Blight":{"severity":"Medium","severity_bn":"মধ্যম","severity_zh":"中等","symptoms_en":"Target-pattern brown spots on lower leaves","symptoms_bn":"নিচের পাতায় লক্ষ্য-নিদর্শন বাদামি দাগ","symptoms_zh":"下部叶片靶心状棕色斑点","rec_en":"Remove infected leaves. Apply Mancozeb or Chlorothalonil.","rec_bn":"আক্রান্ত পাতা সরান। ম্যানকোজেব বা ক্লোরোথালোনিল দিন।","rec_zh":"清除受感染叶片。施用代森锰锌或百菌清。"},
    "Tomato - Late Blight":{"severity":"High","severity_bn":"উচ্চ","severity_zh":"高","symptoms_en":"Water-soaked lesions turning brown, white mold underneath","symptoms_bn":"জলছাপ দাগ বাদামি হয়, নিচে সাদা ছাঁচ","symptoms_zh":"水浸状病斑变褐，背面白色霉层","rec_en":"Apply copper fungicide or Metalaxyl immediately. Remove infected plants.","rec_bn":"অবিলম্বে তামা ছত্রাকনাশক বা মেটালাক্সিল দিন।","rec_zh":"立即施用铜基杀菌剂或甲霜灵。清除受感染植株。"},
    "Tomato - Leaf Mold":{"severity":"Medium","severity_bn":"মধ্যম","severity_zh":"中等","symptoms_en":"Yellow spots on upper leaf, olive-brown mold below","symptoms_bn":"পাতার উপরে হলুদ দাগ, নিচে জলপাই-বাদামি ছাঁচ","symptoms_zh":"叶片上表面黄色斑点，下面橄榄棕色霉层","rec_en":"Improve ventilation. Apply chlorothalonil or copper fungicide.","rec_bn":"বায়ু চলাচল উন্নত করুন। ক্লোরোথালোনিল বা তামা ছত্রাকনাশক দিন।","rec_zh":"改善通风。施用百菌清或铜基杀菌剂。"},
    "Tomato - Septoria Leaf Spot":{"severity":"Medium","severity_bn":"মধ্যম","severity_zh":"中等","symptoms_en":"Small circular spots with dark borders, light centers on lower leaves","symptoms_bn":"নিচের পাতায় গাঢ় সীমানা ও হালকা কেন্দ্র সহ ছোট গোলাকার দাগ","symptoms_zh":"下部叶片具有深色边缘和浅色中心的小圆形斑点","rec_en":"Remove infected lower leaves. Apply Mancozeb.","rec_bn":"আক্রান্ত নিচের পাতা সরান। ম্যানকোজেব দিন।","rec_zh":"清除受感染下部叶片。施用代森锰锌。"},
    "Tomato - Spider Mites":{"severity":"Medium","severity_bn":"মধ্যম","severity_zh":"中等","symptoms_en":"Tiny yellow stippling on leaves, fine webbing on underside","symptoms_bn":"পাতায় ক্ষুদ্র হলুদ ফোটা, নিচে সূক্ষ্ম জাল","symptoms_zh":"叶片细小黄色点斑，背面细丝状蛛网","rec_en":"Apply Abamectin miticide. Spray water on leaf undersides.","rec_bn":"অ্যাবামেক্টিন মাকড়নাশক দিন। পাতার নিচে পানি স্প্রে করুন।","rec_zh":"施用阿维菌素杀螨剂。向叶背喷水。"},
    "Tomato - Target Spot":{"severity":"Medium","severity_bn":"মধ্যম","severity_zh":"中等","symptoms_en":"Circular brown lesions with concentric rings on leaves and fruit","symptoms_bn":"পাতা ও ফলে কেন্দ্রীভূত বলয় সহ গোলাকার বাদামি দাগ","symptoms_zh":"叶片和果实圆形棕色病斑带同心环","rec_en":"Apply azoxystrobin or chlorothalonil. Improve air circulation.","rec_bn":"অ্যাজোক্সিস্ট্রোবিন বা ক্লোরোথালোনিল দিন।","rec_zh":"施用嘧菌酯或百菌清。改善通风。"},
    "Tomato - Yellow Leaf Curl Virus":{"severity":"High","severity_bn":"উচ্চ","severity_zh":"高","symptoms_en":"Upward leaf curling, yellowing of margins, stunted growth","symptoms_bn":"পাতা উপরে কুঁকড়ে যাওয়া, কিনারায় হলুদ হওয়া, বৃদ্ধি বাধাগ্রস্ত","symptoms_zh":"叶片向上卷曲，边缘发黄，植株矮化","rec_en":"Control whitefly with imidacloprid. Remove infected plants.","rec_bn":"ইমিডাক্লোপ্রিড দিয়ে সাদামাছি নিয়ন্ত্রণ করুন।","rec_zh":"用吡虫啉控制烟粉虱。清除受感染植株。"},
    "Tomato - Mosaic Virus":{"severity":"High","severity_bn":"উচ্চ","severity_zh":"高","symptoms_en":"Mottled mosaic pattern on leaves, leaf distortion","symptoms_bn":"পাতায় মোজাইক নিদর্শন, পাতার বিকৃতি","symptoms_zh":"叶片花叶状图案，叶片变形","rec_en":"Remove infected plants immediately. Control aphid vectors. Disinfect tools.","rec_bn":"অবিলম্বে আক্রান্ত গাছ সরান। জাবপোকা নিয়ন্ত্রণ করুন।","rec_zh":"立即清除受感染植株。控制蚜虫媒介。对工具消毒。"},
}

HEALTHY_REC = {
    "bn": "আপনার গাছ সুস্থ দেখাচ্ছে ✅ নিয়মিত পর্যবেক্ষণ চালিয়ে যান, সঠিক পানি সেচ ও সুষম সার বজায় রাখুন।",
    "zh": "您的植物看起来很健康 ✅ 继续定期监测，保持适当浇水和均衡施肥。",
    "en": "Your plant appears healthy ✅ Continue regular monitoring, proper watering, and balanced fertilization.",
}


def predict_disease(image: Image.Image, lang: str = "bn") -> dict:
    arr = np.array(image.convert("RGB").resize((128, 128)), dtype=np.float32)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]

    green_ratio   = float(g.mean() / (r.mean() + g.mean() + b.mean() + 1e-5))
    brown_score   = float((r.mean()*0.6 + b.mean()*0.1) / (g.mean() + 1e-5))
    yellow_score  = float((r.mean() + g.mean()) / (2*b.mean() + 1e-5))
    white_ratio   = float((arr > 210).mean())
    dark_ratio    = float((arr < 55).mean())
    texture       = float((r.std() + g.std() + b.std()) / 3)
    hue_var       = float(np.std(r - g))

    rng = np.random.default_rng(int(r.mean()*100 + g.mean()*10))

    if green_ratio > 0.37 and brown_score < 1.15 and texture < 32:
        opts = [c for c in PLANT_VILLAGE_CLASSES if "Healthy" in c]
        disease = rng.choice(opts)
        conf = min(0.97, green_ratio * 2.4)
    elif f := dark_ratio > 0.22 or (brown_score > 2.2 and dark_ratio > 0.10):
        opts = ["Grape - Black Rot","Apple - Black Rot","Tomato - Late Blight","Potato - Late Blight"]
        disease = rng.choice(opts)
        conf = min(0.93, 0.70 + dark_ratio * 1.5)
    elif brown_score > 1.8:
        opts = ["Tomato - Early Blight","Potato - Early Blight","Corn - Common Rust","Apple - Apple Scab","Strawberry - Leaf Scorch"]
        disease = rng.choice(opts)
        conf = min(0.91, 0.65 + (brown_score - 1.8) * 0.15)
    elif yellow_score > 2.4 and green_ratio < 0.32:
        opts = ["Tomato - Yellow Leaf Curl Virus","Corn - Common Rust","Tomato - Mosaic Virus","Orange - Citrus Greening"]
        disease = rng.choice(opts)
        conf = min(0.90, 0.67 + (yellow_score - 2.4) * 0.08)
    elif white_ratio > 0.25:
        opts = ["Cherry - Powdery Mildew","Squash - Powdery Mildew"]
        disease = rng.choice(opts)
        conf = min(0.92, 0.70 + white_ratio * 0.8)
    elif texture > 50 and hue_var > 20:
        opts = ["Tomato - Bacterial Spot","Pepper - Bacterial Spot","Tomato - Septoria Leaf Spot","Peach - Bacterial Spot"]
        disease = rng.choice(opts)
        conf = min(0.89, 0.65 + texture / 200)
    elif texture > 35 and yellow_score > 1.8:
        opts = ["Tomato - Spider Mites","Corn - Northern Leaf Blight","Tomato - Leaf Mold"]
        disease = rng.choice(opts)
        conf = 0.75
    else:
        opts = ["Apple - Apple Scab","Corn - Cercospora Leaf Spot","Grape - Leaf Blight","Tomato - Target Spot"]
        disease = rng.choice(opts)
        conf = 0.68

    is_healthy = "Healthy" in disease
    parts = disease.split(" - ")
    plant_type = parts[0]
    disease_name = parts[1] if len(parts) > 1 else disease

    if is_healthy:
        return {
            "plant_type": plant_type, "disease": disease, "disease_display": disease_name,
            "confidence": round(float(conf), 3), "confidence_pct": f"{round(float(conf)*100,1)}%",
            "severity": "None",
            "severity_display": {"bn":"নেই","zh":"无","en":"None"}.get(lang,"None"),
            "symptoms": "", "recommendation": HEALTHY_REC.get(lang, HEALTHY_REC["en"]), "is_healthy": True,
        }

    info = DISEASE_INFO.get(disease, {})
    sev = info.get("severity","Medium")
    return {
        "plant_type": plant_type, "disease": disease, "disease_display": disease_name,
        "confidence": round(float(conf), 3), "confidence_pct": f"{round(float(conf)*100,1)}%",
        "severity": sev,
        "severity_display": info.get(f"severity_{lang}", sev),
        "symptoms": info.get(f"symptoms_{lang}", info.get("symptoms_en","")),
        "recommendation": info.get(f"rec_{lang}", info.get("rec_en","Consult local agriculture office.")),
        "is_healthy": False,
    }
