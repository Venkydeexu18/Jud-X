import fitz
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def extract_text_from_pdf(pdf_path):
    text = ""
    pdf_document = fitz.open(pdf_path)
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

def extract_date_from_text(text):
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    dates = re.findall(date_pattern, text)
    if dates:
        return dates[0]  
    else:
        return None 

pdf_files = [
    'affidavit2.pdf',
    'affidavit3.pdf',
    'affidavit3.pdf',
]

data = {'Text': [], 'Date': []}

# Extract text and dates from PDFs
for pdf_file in pdf_files:
    text = extract_text_from_pdf(pdf_file)
    date = extract_date_from_text(text)
    
    data['Text'].append(text)
    data['Date'].append(date)

df = pd.DataFrame(data)

labels = ['priority', 'sentimental', 'normal']

df['Type'] = ['priority', 'sentimental', 'normal']

tfidf_vectorizer = TfidfVectorizer(max_features=1000)
X_tfidf = tfidf_vectorizer.fit_transform(df['Text'])

model = LogisticRegression()
model.fit(X_tfidf, df['Type'])

df['Predicted_Type'] = model.predict(X_tfidf)

df['Date'] = pd.to_datetime(df['Date'])
df.sort_values(by=['Predicted_Type', 'Date'], inplace=True)

df.reset_index(drop=True, inplace=True)

print(df[['Predicted_Type']])
