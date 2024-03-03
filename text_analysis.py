import pandas as pd
from textblob import TextBlob
import os

def analyze_text(article_text):
    try:
        blob = TextBlob(article_text)
        
        positive_score = len([sentence for sentence in blob.sentences if sentence.sentiment.polarity > 0])
        negative_score = len([sentence for sentence in blob.sentences if sentence.sentiment.polarity < 0])
        polarity_score = blob.sentiment.polarity
        subjectivity_score = blob.sentiment.subjectivity
        avg_sentence_length = sum(len(sentence.split()) for sentence in blob.sentences) / len(blob.sentences)
        percentage_of_complex_words = len([word for word in blob.words if len(word) > 2]) / len(blob.words)
        fog_index = 0.4 * (avg_sentence_length + percentage_of_complex_words)
        avg_words_per_sentence = len(blob.words) / len(blob.sentences)
        complex_word_count = len([word for word in blob.words if len(word) > 2])
        word_count = len(blob.words)
        syllable_per_word = sum([syllables(word) for word in blob.words]) / len(blob.words)
        personal_pronouns = len([word for word in blob.words if word.lower() in ['i', 'me', 'my', 'mine', 'myself']])
        avg_word_length = sum([len(word) for word in blob.words]) / len(blob.words)
        
        return [positive_score, negative_score, polarity_score, subjectivity_score, avg_sentence_length,
                percentage_of_complex_words, fog_index, avg_words_per_sentence, complex_word_count,
                word_count, syllable_per_word, personal_pronouns, avg_word_length]
    except Exception as e:
        print(f"Error analyzing text: {e}")
        return None

def syllables(word):
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for i in range(1, len(word)):
        if word[i] in vowels and word[i - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count

article_texts_dir = 'article_rishap_texts'
article_files = os.listdir(article_texts_dir)

output_columns = ['URL_ID', 'ARTICLE_TITLE', 'ARTICLE_TEXT', 'POSITIVE SCORE', 'NEGATIVE SCORE',
                  'POLARITY SCORE', 'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS',
                  'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT',
                  'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']

output_df = pd.DataFrame(columns=output_columns)

for file in article_files:
    url_id = file.split('.')[0]
    filename = os.path.join(article_texts_dir, file)
    
    with open(filename, 'r', encoding='utf-8') as file:
        article_title = file.readline().strip()
        article_text = file.read().strip()
    
    analysis_result = analyze_text(article_text)
    
    if analysis_result:
        result_df = pd.DataFrame([[url_id, article_title, article_text] + analysis_result], columns=output_columns)
        output_df = pd.concat([output_df, result_df], ignore_index=True)

output_df.to_excel("Output.xlsx", index=False)
