# handle AI functions (langchain + ollama) : llama3.2:3b 
# استيراد المكتبات اللازمة
import mlflow  # مكتبة لتتبع العمليات التجريبية مثل التدريبات وتحليل النماذج
from langchain.chains import LLMChain  # لإنشاء سلاسل المحادثة مع النماذج اللغوية
from langchain_core.prompts import PromptTemplate  # لتوليد قوالب للأسئلة والمطالبات
from langchain_ollama.llms import OllamaLLM  # استخدام نموذج Ollama LLM
import json  # للتعامل مع البيانات بصيغة JSON

# إعداد mlflow لتتبع التجارب
# تحديد عنوان الخادم المحلي لـ mlflow
mlflow.set_tracking_uri("http://mlflow:5000")

# تعيين اسم المشروع التجريبي
mlflow.set_experiment('code_reviewer_llm')

# تفعيل التسجيل التلقائي للتفاصيل الخاصة بسلاسل LangChain
mlflow.langchain.autolog(
    log_models=True,  # تسجيل النماذج المستخدمة
    log_input_examples=True  # تسجيل الأمثلة المدخلة
)

# وظيفة لإنشاء قالب لمراجعة الكود
def generate_prompt_template():
    # تحديد المتغيرات التي سيأخذها القالب
    input_variables = ["question", "programming_language"]
    
    # نص القالب الذي يحتوي على التعليمات للنموذج اللغوي
    template = """
        You are an expert software engineer reviewing {programming_language} code. Analyze the following code and provide:
        - Code quality score from 1 to 10.
        - Code pros.
        - Code cons.
        - Code security check.
        - A better version of the code.
        - Explain the better version and why it is better.

        Code:
        ```
        {question}
        ```

        Return the data as markdown , like 
        ## Code quality score  : score
        - explanation of this score 

        <br>

        ## Code pros
        - explanation 

        <br>

        ## Code Cons
        - explanation 
        
        <br>

        ## Code security check
        - explanation 

        <br>

        ## A better version of the code 
        - explanation 

        <br>

        ## Explain the better version and why it is better
        - explanation 
        
    """
    # إرجاع قالب المطالبة (PromptTemplate)
    return PromptTemplate(input_variables=input_variables, template=template)


from langchain_groq import ChatGroq
# وظيفة لتنفيذ مراجعة الكود باستخدام نموذج Ollama LLM
def perform_code_review_with_qroq(question, programming_language):
    api_key="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"
    # تهيئة النموذج اللغوي Ollama
    llm = ChatGroq(
        model="mixtral-8x7b-32768",
        groq_api_key = api_key
      
    )
    
    # إنشاء قالب المطالبة
    prompt_template = generate_prompt_template()

    # إنشاء سلسلة LangChain creat pipline
    # الخطوة 1: إنشاء السلسلة باستخدام القالب والنموذج
    chain = LLMChain(prompt=prompt_template, llm=llm)

    # تشغيل السلسلة باستخدام المتغيرات المدخلة (السؤال ولغة البرمجة)
    result = chain.run({
        "question": question,  # الكود المطلوب مراجعته
        "programming_language": programming_language  # لغة البرمجة المستخدمة
    })

    # طباعة النتيجة (يمكن تفعيل هذا في حال الحاجة لفحص النتيجة)
    # print(f"result : {result}")

    # تحويل النتيجة إلى JSON (تعليق مؤقت لفهم النتائج)
    # review_data = json.loads(result)
    # print(f'review_data : {review_data}')
    
    # إرجاع النتيجة النهائية
    return result
