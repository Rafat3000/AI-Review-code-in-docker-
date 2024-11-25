# استيراد المكتبات الضرورية والوظائف من الملفات الأخرى
import streamlit as st  # مكتبة Streamlit لإنشاء واجهات المستخدم
from database import init_database, get_all_reviews, create_code_review  # وظائف لإدارة قاعدة البيانات
from config import PROGRAMMING_LANGUAGES  # قائمة اللغات البرمجية المدعومة
from ai import perform_code_review_with_qroq  # وظيفة للقيام بمراجعة الكود باستخدام الذكاء الاصطناعي
import time  # مكتبة لإضافة فاصل زمني
from utils import extract_code_quality_score  # وظيفة لاستخراج درجة جودة الكود من المراجعة

# تعريف وظيفة الشريط الجانبي
def sidebar_menu():
    # إضافة عنوان إلى الشريط الجانبي
    st.sidebar.title("Review History")

    # جلب جميع المراجعات من قاعدة البيانات
    reviews = get_all_reviews()

    # حالة تستخدم لتحديد ما إذا كان هناك مراجعة قيد العرض
    st.session_state['is_active'] = False

    # عرض أول 5 مراجعات فقط في الشريط الجانبي
    for review in reviews[:5]:
        text = review['question'][:33]  # أخذ أول 33 حرفًا فقط من نص الكود للسؤال
        if st.sidebar.button(text, key=review['id']):  # إنشاء زر لكل مراجعة
            display_json_review(review['answer'])  # عرض المراجعة الكاملة عند الضغط على الزر

# تعريف وظيفة لعرض مراجعة الذكاء الاصطناعي
def display_json_review(review_data):
    # عرض نص المراجعة باستخدام Markdown
    st.markdown(review_data)

# الوظيفة الرئيسية للتطبيق
def main():
    # ضبط إعدادات صفحة التطبيق (العنوان والأيقونة)
    st.set_page_config(page_title="AI Code Review Assistant", page_icon="🤖")

    # تهيئة قاعدة البيانات عند بدء التطبيق
    init_database()

    # إضافة الشريط الجانبي للتطبيق
    sidebar_menu()

    # عرض عنوان رئيسي في الواجهة الرئيسية
    st.title("AI Code Review Assistant")

    # اختيار لغة البرمجة من قائمة منسدلة
    language = st.selectbox("Programming Language", options=PROGRAMMING_LANGUAGES)

    # إدخال الكود المطلوب مراجعته عبر مربع نص
    code_input = st.text_area("Code to Review", height=200)

    # زر للبدء في عملية مراجعة الكود
    if st.button("Review Code"):
        with st.spinner("Analyzing Code..."):  # عرض مؤشر تحميل أثناء العملية
            time.sleep(1)  # تأخير بسيط لتجربة المستخدم (غير ضروري في الإنتاج)

            # استدعاء وظيفة الذكاء الاصطناعي لتحليل الكود
            review_data = perform_code_review_with_qroq(code_input, language)

            # عرض نتيجة مراجعة الذكاء الاصطناعي
            display_json_review(review_data)

            # استخراج درجة جودة الكود من المراجعة
            score = extract_code_quality_score(review_data)

            # حفظ بيانات المراجعة في قاعدة البيانات
            create_code_review(
                question=code_input,  # الكود الذي أدخله المستخدم
                answer=review_data,  # مراجعة الذكاء الاصطناعي
                language=language,  # اللغة البرمجية المختارة
                score=score  # درجة جودة الكود
            )

            # تحديث واجهة التطبيق لتظهر المراجعات الجديدة في الشريط الجانبي
            # يمكن إعادة تمكين الأسطر أدناه عند الحاجة
            # close_connection()
            # st.rerun()

# نقطة البداية لتشغيل التطبيق
if __name__ == "__main__":
    main()  # استدعاء الوظيفة الرئيسية عند تشغيل الملف
