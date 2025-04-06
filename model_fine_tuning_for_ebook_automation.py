# -*- coding: utf-8 -*-
"""model_fine_tuning_for_ebook_automation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/177Vt03a-pClk8ZiEgBUyDhDedITVyiD8
"""

pip install transformers datasets torch

#Make sure to run your colab free tire on T4 GPU

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import random

sentences = {
    0: [
        "মূল্য ১০০ টাকা", "দাম ২০০ টাকা", "মূল্য ৩০০ টাকা", "দাম মাত্র ৪০০ টাকা", "বিক্রয়মূল্য ৫০০ টাকা",
        "মূল্য নির্ধারণ করা হয়েছে ৬০০ টাকা", "পণ্যের দাম ৭০০ টাকা", "মূল্য ৮০০ টাকা", "দাম মাত্র ৯০০ টাকা",
        "বিক্রয়মূল্য ১০০০ টাকা", "হাদিয়া মাত্র ১১০০ টাকা", "দাম ১২০০ টাকা", "মূল্য নির্ধারণ করা হয়েছে ১৩০০ টাকা",
        "পণ্যের হাদিয়া মাত্র ১৪০০ টাকা", "মূল্য মাত্র ১৫০০ টাকা", "এই পণ্যের হাদিয়া মাত্র ১৬০০ টাকা",'প্রকাশনায়'
        "বিক্রয়মূল্য নির্ধারণ করা হয়েছে ১৭০০ টাকা", "হাদিয়া মাত্র ১৮০০ টাকা", "পণ্যের দাম ১৯০০ টাকা", "মূল্য মাত্র ২০০০ টাকা",
        "বিক্রয়মূল্য ২১০০ টাকা", "হাদিয়া মাত্র ২২০০ টাকা", "দাম নির্ধারণ করা হয়েছে ২৩৫০ টাকা", "এই পণ্যের মূল্য ২৪০০ টাকা",
        "বিক্রয়মূল্য মাত্র ২৫০০ টাকা", "মূল্য নির্ধারণ করা হয়েছে ২৬০০ টাকা", "পণ্যের হাদিয়া মাত্র ২৭৫০ টাকা", "মূল্য ২৮০০ টাকা",
        "হাদিয়া মাত্র ২৯০০ টাকা", "মূল্য মাত্র ৩০০০ টাকা","নুরানী বুক হাউজ", "মদিনা লাইব্রেরি", "ইসলামি বই ঘর", "মক্কা বুক সেন্টার", "হুমায়ুন বুক স্টোর",
        "আলোর পাঠশালা", "আল কোরআন বুক হাউজ", "রহমত বুক কর্নার", "তালিমি প্রকাশনী", "আনোয়ার বুক ডিপো",
        "ইমাম বুক সেন্টার", "ফরিদ বুক হাউজ", "শহীদ বই ঘর", "আল হামদ বুক কর্নার", "মাহফুজ লাইব্রেরি",
        "নূর বুক সেন্টার", "তাওহিদ বুক কর্নার", "আল ফাতাহ বুক স্টোর", "মাহদি বুক কর্নার", "কিতাবঘর",
        "আল ফরহাদ বুক কর্নার", "মুসলিম বুক ডিপো", "ইলমের খোঁজ", "সাদ বুক সেন্টার", "বইয়ের দুনিয়া", "হেরা বুক হাউজ",
        "জাহান বুক কর্নার", "শান্তি বুক স্টোর", "কোরআন কর্নার", "তাহফিজ বুক ডিপো", "শিরোনাম প্রকাশন","ইসলামী টাওয়ার ১১ বাংলাবাজার ঢাকা ১১০০", "মুসলিম টাওয়ার ১৫ কারওয়ান বাজার ঢাকা ১২০০", "মক্কা টাওয়ার ২৭ মিরপুর রোড ঢাকা ১২১৫",
        "নূর টাওয়ার ৪৫ সোহরাওয়ার্দী ঢাকা ১২৩৪", "হেরা টাওয়ার ১৮ টাউন হল ঢাকা ১৩৪৫", "আল হামদ টাওয়ার ৩০ মধুবাগ ঢাকা ১৪৫৬",
        "ফোর্বস টাওয়ার ২২ পান্থপথ ঢাকা ১৫৬৭", "হাজী টাওয়ার ৮৭ গুলশান ঢাকা ১৬৭৮", "ফরিদ টাওয়ার ৩২ সেন্ট্রাল রোড ঢাকা ১৭৮৯",
        "মাহফুজ টাওয়ার ১৪ কুর্মিটোলা ঢাকা ১৮৯০", "আল কোরআন টাওয়ার ১০০ পুরানা পল্টন ঢাকা ১৯০১", "শহীদ টাওয়ার ৬০ নতুন বাজার ঢাকা ২০১২",
        "আল কাসিম টাওয়ার ৫৫ মিরপুর ঢাকা ২১০৩", "তাওহিদ টাওয়ার ৪৭ পশ্চিম মোল্লারটেক ঢাকা ২২১৪", "শাহাদাত টাওয়ার ৭৮ নবীন বাজার ঢাকা ২৩২৫",
        "হাদীস টাওয়ার ৬৪ রমনা ঢাকা ২৪৩৬", "আরব টাওয়ার ৮১ শ্রীকৃষ্ণপুর ঢাকা ২৫৪৭", "আল হুসাইন টাওয়ার ৫৩ কলাবাগান ঢাকা ২৬৫৮",
        "তালিমি টাওয়ার ৩৪ তেজগাঁও ঢাকা ২৭৬৯", "নূরানী টাওয়ার ৪১ বনানী ঢাকা ২৮৭০", "শরীফ টাওয়ার ২৬ মুগদা ঢাকা ২৯৭১",
        "তাওহিদ টাওয়ার ৬৯ আগারগাঁও ঢাকা ৩০৮২", "মুসলিম টাওয়ার ৭৩ ফার্মগেট ঢাকা ৩১৯৩", "মক্কা টাওয়ার ৫৩ সাইফুল্লাহ রোড ঢাকা ৩২৯৪",
        "ফরিদ টাওয়ার ৯৭ বংশাল ঢাকা ৩৩৯৫", "আল কোরআন টাওয়ার ৬৫ মতিঝিল ঢাকা ৩৪৯৬", "আল হামদ টাওয়ার ৩৮ পান্থপথ ঢাকা ৩৫৯৭",
        "ফোর্বস টাওয়ার ১৭ শাহবাগ ঢাকা ৩৬৯৮","মোবাইল ০১৯১১০০৬৮০৬", "যোগাযোগ ০১৯১১০০৭১৭০", "ফোন নাম্বার ০১৯১১০০৭২৭২", "ফোন করুন ০১৯১১০০৮৩৮৩", "আমার মোবাইল নম্বর ০১৯১১০০৯৪৯৪",
        "যোগাযোগের নম্বর ০১৯১১০১০৫০৫", "ফোন নম্বর ০১৯১১০১১৬১৬", "ফোনে যোগাযোগ করুন ০১৯১১০১২৭২৭", "আমার ফোন নাম্বার ০১৯১১০১৩৮৩৮",
        "মোবাইল নম্বর ০১৯১১০১৪৯৪৯", "ফোন করতে পারবেন ০১৯১১০১৫০০১", "যোগাযোগ করতে ০১৯১১০১৬১১১", "ফোন নম্বরে যোগাযোগ ০১৯১১০১৭২২২",
        "ফোন কল করুন ০১৯১১০১৮৩৩৩", "মোবাইল ফোন নম্বর ০১৯১১০১৯৪৪৪", "ফোনের মাধ্যমে যোগাযোগ ০১৯১১০২০৫৫৫", "ফোন করুন ০১৯১১০২১৬৬৬",
        "যোগাযোগের জন্য ফোন করুন ০১৯১১০২২৭৭৭", "ফোনে কথা বলুন ০১৯১১০২৩৮৮৮", "ফোন কলের মাধ্যমে যোগাযোগ ০১৯১১০২৪৯৯৯",
        "আমার যোগাযোগের নাম্বার ০১৯১১০২৫০০০", "ফোনে আমাকে খুঁজুন ০১৯১১০২৬১১১", "যোগাযোগের জন্য আমার মোবাইল ০১৯১১০২৭২২২",
        "ফোন করার জন্য কল করুন ০১৯১১০২৮৩৩৩", "ফোন নম্বর জানালে ভালো ০১৯১১০২৯৪৪৪", "ফোনে যোগাযোগ করুন এই নাম্বারে ০১৯১১০৩০৫৫৫",
        "আমার মোবাইল ফোন নম্বর ০১৯১১০৩১৬৬৬"
    ],
    1:[
        "প্রথম প্রকাশ : জুলাই ২০১২ ইং", "১ম প্রকাশ : জুলাই ২০১২ ইং",
        "দ্বিতীয় প্রকাশ : আগস্ট ২০১৩ ইং", "২য় প্রকাশ : আগস্ট ২০১৩ ইং",
        "তৃতীয় প্রকাশ : সেপ্টেম্বর ২০১৪ ইং", "৩য় প্রকাশ : সেপ্টেম্বর ২০১৪ ইং",
        "চতুর্থ প্রকাশ : অক্টোবর ২০১৫ ইং", "৪র্থ প্রকাশ : অক্টোবর ২০১৫ ইং",
        "পঞ্চম প্রকাশ : নভেম্বর ২০১৬ ইং", "৫ম প্রকাশ : নভেম্বর ২০১৬ ইং",
        "ষষ্ঠ প্রকাশ : ডিসেম্বর ২০১৭ ইং", "৬ষ্ঠ প্রকাশ : ডিসেম্বর ২০১৭ ইং",
        "সপ্তম প্রকাশ : জানুয়ারি ২০১৮ ইং", "৭ম প্রকাশ : জানুয়ারি ২০১৮ ইং",
        "অষ্টম প্রকাশ : ফেব্রুয়ারি ২০১৯ ইং", "৮ম প্রকাশ : ফেব্রুয়ারি ২০১৯ ইং",
        "নবম প্রকাশ : মার্চ ২০২০ ইং", "৯ম প্রকাশ : মার্চ ২০২০ ইং",
        "দশম প্রকাশ : এপ্রিল ২০২১ ইং", "১০ম প্রকাশ : এপ্রিল ২০২১ ইং",
        "একাদশ প্রকাশ : মে ২০২২ ইং", "১১তম প্রকাশ : মে ২০২২ ইং",
        "দ্বাদশ প্রকাশ : জুন ২০২৩ ইং", "১২তম প্রকাশ : জুন ২০২৩ ইং",
        "তেরোতম প্রকাশ : জুলাই ২০২৪ ইং", "১৩তম প্রকাশ : জুলাই ২০২৪ ইং",
        "চোদ্দতম প্রকাশ : আগস্ট ২০২৫ ইং", "১৪তম প্রকাশ : আগস্ট ২০২৫ ইং",
        "পনেরোতম প্রকাশ : সেপ্টেম্বর ২০২৬ ইং", "১৫তম প্রকাশ : সেপ্টেম্বর ২০২৬ ইং",
        "ষোলতম প্রকাশ : অক্টোবর ২০২৭ ইং", "১৬তম প্রকাশ : অক্টোবর ২০২৭ ইং",
        "সতেরোতম প্রকাশ : নভেম্বর ২০২৮ ইং", "১৭তম প্রকাশ : নভেম্বর ২০২৮ ইং",
        "আটত্রিশতম প্রকাশ : ডিসেম্বর ২০২৯ ইং", "১৮তম প্রকাশ : ডিসেম্বর ২০২৯ ইং",
        "ঊনত্রিশতম প্রকাশ : জানুয়ারি ২০৩০ ইং", "১৯তম প্রকাশ : জানুয়ারি ২০৩০ ইং",
        "ত্রিশতম প্রকাশ : ফেব্রুয়ারি ২০৩১ ইং", "২০তম প্রকাশ : ফেব্রুয়ারি ২০৩১ ইং",
        "একত্রিশতম প্রকাশ : মার্চ ২০৩২ ইং", "২১তম প্রকাশ : মার্চ ২০৩২ ইং",
        "বত্রিশতম প্রকাশ : এপ্রিল ২০৩৩ ইং", "২২তম প্রকাশ : এপ্রিল ২০৩৩ ইং",
        "আবদুল হান্নান", "আল-আমিন", "মাহফুজ আলী", "সৈয়দ হাসান", "ফিরোজ আহমেদ",
        "মেহেদী হাসান", "জাহিদুল ইসলাম", "রহমান সিদ্দীকি", "আবুল কালাম", "মুহাম্মদ সেলিম",
        "সিরাজুল ইসলাম", "আলী আকবর", "ফজলুল হক", "ইব্রাহিম খালেদ", "এনামুল হক",
        "জালাল উদ্দিন", "তৌফিক রহমান", "রফিকুল ইসলাম", "মোহাম্মদ রফিক", "বশির আহমেদ",
        "মীর সাঈদ", "নাজমুল ইসলাম", "শাহীন আলী", "মুহাম্মদ সোহেল", "আশরাফুল আলম",
        "সাইফুল ইসলাম", "আবদুল জব্বার", "জাহিদ হাসান", "রহমত আলী", "মুহাম্মদ ইসহাক",
        "আবুল হোসেন", "ফয়েজ আহমেদ", "মুফতি মাহমুদ", "ইফতেখার রহমান", "মুস্তাফিজুর রহমান",
        "আবদুল্লাহ আল-ফারুক", "নূর মোহাম্মদ", "আলী রহমান", "শাহীন আহমেদ", "ফজলুল করিম",
        "আল-আমিন চৌধুরী", "জাফর আহমেদ", "মুজিবুর রহমান", "সায়েদ আব্দুল হক", "মাজহারুল ইসলাম",
        "শাহজাহান সিদ্দিকী", "মালেক মিয়া", "ওমর ফারুক", "মহিউদ্দিন মোল্লা", "আলী রেজা",
        "হোসেন আলী", "আব্বাস সিদ্দিকী", "মোজাম্মেল হক", "মামুনুর রশীদ", "আল আমিন মিয়া",
        "সামসুল হক", "নাছির উদ্দিন", "তানভীর হোসেন", "মোর্শেদ আলী", "এহসানুল হক",
        "কামাল হোসেন", "মুকুল আহমেদ", "গোলাম রব্বানী", "ফয়েজ সিদ্দিকী", "আবুল হাসান",
        "ইসহাক আলী", "শাহিন সিদ্দিকী", "মিজানুর রহমান", "কাজী সোলায়মান", "শামসুল ইসলাম",
        "আসাদুল্লাহ", "নাফিসুল ইসলাম", "মুকিত আলী", "বিকাশ রঞ্জন", "মো. তৌহিদুল ইসলাম",
        "কাদের আলী", "রফিক সিদ্দিকী", "আলী রেজা সিদ্দিকী", "রেজাউল করিম", "মোহাম্মদ সিদ্দিক",
        "রহমতুল্লাহ", "মুস্তাকিম আহমেদ", "তাজুল ইসলাম", "মেহেদী মিয়া", "আবুল বশর",
        "আলমগীর হোসেন", "ফখরুল ইসলাম", "মাহবুব আলী", "মাহফুজ সিদ্দিকী", "আব্দুল মজিদ",
        "নুরুল ইসলাম", "আলম মিয়া", "মহিদুল্লাহ", "ফজলুল ইসলাম", "আবুল কালাম আজাদ",
        "মোহাম্মদ আলী", "হানিফ আহমেদ", "আবু সাঈদ", "শহীদুল ইসলাম", "মাহমুদুল হাসান",
        "সাব্বির আহমেদ", "মুরাদ হোসেন", "রফিকুল ইসলাম সিদ্দিকী", "ইয়াসিন আলী",
        "সামির আহমেদ", "রাব্বি সিদ্দিকী", "ফাহিমুল ইসলাম", "মুবারক আলী", "তাহের আহমেদ",
        "নির্দেশনা", "নির্দেশ", "উপদেশ", "পথনির্দেশ", "গাইডলাইন", "নির্দেশিকা", "পরামর্শ",
        "পাঠদর্শন", "হিদায়ত", "আদেশ", "আদর্শ", "সুপারিশ", "বিবরণ", "অধিকার",
        "নীতিমালা", "নেতৃত্ব", "সংকেত", "দিশা", "পথপ্রদর্শক", "উপদেষ্টা",
        "পর্যবেক্ষণ", "চিন্তা", "ব্যাখ্যা", "নির্দেশনা পত্র", "প্রকল্প নির্দেশনা",
        "কার্যক্রম নির্দেশনা", "সুপারিশ পত্র", "নতুন দিক নির্দেশনা",
        "সংকলন", "সংগ্রহ", "জমা", "সম্ভার", "সংগ্রহণ", "সংকলিত", "এলাহী", "তৈরি",
        "আয়োজন", "প্রস্তুত", "প্রতিলিপি", "আলোকিত",
        "অনুবাদ", "অনুবাদনা", "ভাষান্তর", "অনুবাদপত্র", "অভিধান", "ভাষান্তরিত",
        "তর্জমা", "বর্ণনা", "বিবরণ", "অর্থ রূপান্তর", "বাক্য রূপান্তর",'দ্বিতীয় সংস্করণ : অক্টোবর ২০১২ ইং',"প্রথম সংস্করণ : জানুয়ারি ২০১০ ইং",
        "তৃতীয় সংস্করণ : মার্চ ২০১৫ ইং",
        "চতুর্থ সংস্করণ : জুলাই ২০১৮ ইং",
        "পঞ্চম সংস্করণ : ডিসেম্বর ২০২০ ইং",
        "ষষ্ঠ সংস্করণ : ফেব্রুয়ারি ২০২২ ইং",
        "সপ্তম সংস্করণ : মে ২০১৭ ইং",
        "অষ্টম সংস্করণ : আগস্ট ২০১৯ ইং",
        "নবম সংস্করণ : এপ্রিল ২০২১ ইং",
        "দশম সংস্করণ : নভেম্বর ২০২৩ ইং",
      ],
    2:["সূচি", "তালিকা", "সূচিপত্র", "লিস্ট", "তালিকা পত্র", "নথি", "তথ্যপঞ্জী",
    "তালিকা নির্ধারণ", "রেজিস্টার", "সূচনাবলী", "অবস্থান", "পর্যায়"]

}


def generate_dataset(num_samples=5000):
    texts = []
    labels = []
    for _ in range(num_samples):
        label = random.choice([0,1,2])
        texts.append(random.choice(sentences[label]))
        labels.append(label)

    return Dataset.from_dict({"text": texts, "label": labels})

model_name = "bert-base-multilingual-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)

def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True)

dataset = generate_dataset()

tokenized_datasets = dataset.map(tokenize_function, batched=True)

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    eval_dataset=tokenized_datasets,
)


trainer.train()


results = trainer.evaluate()
print("Evaluation results:", results)


model.save_pretrained("./fine_tuned_bengali_model")
tokenizer.save_pretrained("./fine_tuned_bengali_model")

model = AutoModelForSequenceClassification.from_pretrained("./fine_tuned_bengali_model")
tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_bengali_model")

input_text = "প্রকাশনায়"
inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
outputs = model(**inputs)
predictions = torch.argmax(outputs.logits, dim=1)
print(f"Prediction: {predictions.item()}")

