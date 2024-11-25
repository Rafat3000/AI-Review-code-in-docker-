# استيراد المكتبات اللازمة
from datetime import datetime  # للتعامل مع الوقت والتاريخ
from peewee import SqliteDatabase, TextField, DateTimeField, CharField, Model, FloatField , IntegrityError # مكتبة Peewee لإنشاء قواعد بيانات SQLite
import re  # استيراد مكتبة التعبيرات النمطية
# إنشاء قاعدة بيانات SQLite create sqlite db
db = SqliteDatabase('code_reviews.db')  # يتم إنشاء ملف قاعدة بيانات باسم code_reviews.db

# تعريف نموذج (جدول) CodeReview / define models tables
class CodeReview(Model):  
    # حقل لتخزين السؤال بصيغة نصية
    question = TextField()
    # حقل لتحديد لغة البرمجة المرتبطة بالمراجعة
    language = CharField()
    # حقل لتخزين الإجابة بصيغة نصية
    answer = TextField()
    # حقل لتخزين التقييم كعدد عشري
    score = FloatField()
    # حقل لتخزين تاريخ ووقت إنشاء السجل تلقائياً
    created_at = DateTimeField(default=datetime.now) 

    # تحديد قاعدة البيانات المرتبطة بالنموذج
    class Meta:
        database = db

    # تعريف وظيفة لإرجاع بيانات المراجعة كقائمة
    def get_review_data(self):
        return {
            'id': self.id,  # معرف المراجعة
            'question': self.question,  # السؤال
            'language': self.language,  # لغة البرمجة
            'answer': self.answer,  # الإجابة
            'score': self.score,  # التقييم
            'time': self.created_at  # وقت إنشاء السجل
        }

# تهيئة قاعدة البيانات intialize db
def init_database():
    db.connect()  # الاتصال بقاعدة البيانات
    db.create_tables([CodeReview], safe=True)  # إنشاء الجداول إذا لم تكن موجودة (التأكد من عدم التكرار)

# تعريف دالة لجلب جميع المراجعات difine functions 
def get_all_reviews():
    data = CodeReview.select().order_by(CodeReview.created_at.desc())  
    # جلب جميع المراجعات مرتبة تنازلياً حسب تاريخ الإنشاء
    return [r.get_review_data() for r in data]  
    # تحويل كل سجل إلى صيغة قائمة باستخدام الدالة المخصصة

def extract_code_quality_score(result):
    """استخراج درجة جودة الكود من النص باستخدام التعبيرات النمطية"""
    if not result:
        return 0
    
    # البحث عن رقم يتبع كلمة score أو درجة
    match = re.search(r'(?:score|درجة):\s*(\d+(?:\.\d+)?)', result, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return 0

# تعريف دالة لإنشاء مراجعة جديدة
def create_code_review(question, language, answer, result=None, score=None):
    """Creates a new code review entry in the database."""
    try:
        # إذا لم يتم تمرير score، استخرج القيمة من result
        if score is None:
            score = extract_code_quality_score(result)
        review = CodeReview.create(
            question=question,
            language=language,
            answer=answer,
            score=score
        )
        return review.get_review_data()
    
    except ValueError as e:
        print(f"Error extracting score: {e}")
        # التعامل مع الخطأ باستخدام قيمة افتراضية
        default_score = 0
        review = CodeReview.create(
            question=question,
            language=language,
            answer=answer,
            score=default_score
        )
        return review.get_review_data()
    
    except IntegrityError as e:
        print(f"Database integrity error: {e}")
        return None
