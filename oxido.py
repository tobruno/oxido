from openai import OpenAI
import os
import requests

file_path = 'openai_key.txt'

def read_api_key(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            api_key = file.read().strip()
            return api_key
    except FileNotFoundError:
        print(f"Plik {file_path} nie został znaleziony")
        return None

def read_article(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def generate_content(article_text, client):
    prompt = f"""
    Zamień format przedstawionego niżej Artykułu na typ HTML. Wytwarzając polecony tekst, zastosuj się do poniższych poleceń:
     1) Użyj odpowiednich tagów HTML do strukturyzacji treści. 
     2) Określ miejsca, gdzie warto wstawić grafiki (oznacz je z użyciem 
        tagu <img> z atrybutem src="image_placeholder.jpg"). Dodaj atrybut 'alt' do 
        każdego obrazka z dokładnym promptem, który możemy użyć do wygenerowania grafiki. 
     3) Umieść podpisy pod grafikami używając odpowiedniego tagu HTML. 
     4) Zwrócony kod powinien zawierać wyłącznie zawartość do wstawienia pomiędzy tagami <body> i </body>. Nie dołączaj znaczników <html>, <head> ani <body>.

    Artykuł:
    {article_text}
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-4o",
    )

    message = chat_completion.choices[0].message
    html_content = message.content.strip()
    return html_content


def save_html(html_content, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

def main():
    url = f'https://cdn.oxido.pl/hr/Zadanie%20dla%20JJunior%20AI%20Developera%20-%20tresc%20artykulu.txt'
    output_file = 'artykul.html'
    
    key = read_api_key(file_path)
    if key:
        print("Klucz API został odczytany")
    else:
        print("Nie udało się odczytać klucza API")
    client = OpenAI(api_key = key)

    article_text = read_article(url)
    html_content = generate_content(article_text, client)

    save_html(html_content, output_file)
    print("Program wykonał się prawidłowo - plik artykul.html został zapisany")





if __name__ == "__main__":
    main()