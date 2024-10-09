import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def raspar_noticias(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        titulos = soup.find_all('h2', class_='titulo-noticia')  # Ajuste o seletor conforme necessário
        
        noticias = []
        for titulo in titulos:
            noticia = {
                'Titulo': titulo.get_text(),
                'Link': titulo.find('a')['href']  # Supondo que o link esteja dentro de uma tag <a>
            }
            noticias.append(noticia)
        return noticias
    else:
        print(f'Erro ao acessar o site: {response.status_code}')
        return []

def gerar_relatorio(noticias):
    df = pd.DataFrame(noticias)
    df.to_csv('relatorio_noticias.csv', index=False)
    print('Relatório gerado e salvo como relatorio_noticias.csv')

def enviar_email(remetente, senha, destinatario, assunto, corpo, anexo):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = assunto

    mensagem.attach(MIMEText(corpo, 'plain'))

    with open(anexo, 'rb') as file:
        mensagem.attach(MIMEText(file.read(), 'csv'))

    try:
        servidor = smtplib.SMTP(smtp_server, smtp_port)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.send_message(mensagem)
        print(f'Email enviado para {destinatario}')
    except Exception as e:
        print(f'Erro ao enviar email: {e}')
    finally:
        servidor.quit()

def main():
    url = 'https://www.exemplo.com/noticias'  # Altere para a URL desejada
    noticias = raspar_noticias(url)

    if noticias:
        gerar_relatorio(noticias)

        remetente = 'seu_email@gmail.com'
        senha = 'sua_senha'  # Use variáveis de ambiente em produção
        destinatario = 'destinatario@example.com'
        assunto = 'Relatório de Notícias'
        corpo = 'Anexo está o relatório das últimas notícias.'

        enviar_email(remetente, senha, destinatario, assunto, corpo, 'relatorio_noticias.csv')

if __name__ == '__main__':
    main()
