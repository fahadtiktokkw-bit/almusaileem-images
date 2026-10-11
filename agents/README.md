# Almusaileem Prompt Agent V1

وكيل محلي لتجهيز برومبتات التصميم والفيديو والتسويق وSEO، وتسجيل تقييم يدوي للمخرجات.

## تشغيل
```bash
python agents/prompt_agent.py --task video --subject "clouds and camel" --constraints "Keep all Arabic typography static"
```

التقييم اليدوي بعد فحص الناتج:
```bash
python agents/prompt_agent.py --task video --subject "clouds and camel" --scores 20,20,18,18,20 --output report.json
```

المعايير بالترتيب: الهندسة، النص والشعار، التغييرات المسموحة، الواقعية، الصيغة. النجاح 90/100 دون مخالفة حرجة. لا يدّعي السكربت مشاهدة الصورة أو الفيديو أو تشغيل Grok؛ إدخال الدرجات يدوي. لا توجد مفاتيح API مطلوبة.

المكتبة المرجعية على Google Drive:
https://docs.google.com/document/d/1sFnUN-CkZaUIguuV9Jua-Fh5k06WkZehlfY7qDWNXdU/edit

**الحالة:** إصدار أولي يعمل محلياً، وليس خدمة سحابية تلقائية أو تكاملاً مباشراً مع Grok/Google Drive.
