import streamlit as st
import qrcode
import io
import requests

# Classe para gerenciar o aplicativo
class APPFormsQR:
    def __init__(self):
        pass

    # Função para gerar QR Code
    def gerar_qrcode(self, dados):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(dados)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        return img
    
    def obter_hora_sao_paulo(self):
        url = "http://worldtimeapi.org/api/timezone/America/Sao_Paulo"
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json()
            data_hora = dados['datetime']
            data = data_hora.split('T')[0]
            hora = data_hora.split('T')[1].split('.')[0]
            return data, hora
        else:
            return None, None

    # Função principal da interface
    def interface(self):
        st.title("Gerador de QRCODE")

        # Campo de entrada para o usuário
        Matricula = st.text_area("Digite a sua Matricula:")
        Nome = st.text_area("Digite o seu Nome:")
        
        if st.button("Gerar QR Code"):
            data, hora = self.obter_hora_sao_paulo()
            Data = f"{data} {hora}"
            Qrcode_text = f"{Matricula}/{Nome}/{Data}"
            print(Qrcode_text)
            # Gera o QR Code
            qrcode_img = self.gerar_qrcode(Qrcode_text)
            buffer = io.BytesIO()
            qrcode_img.save(buffer, format="PNG")
            buffer.seek(0)
            
            # Exibe o QR Code
            st.image(buffer, caption="QR Code Gerado", use_column_width=True)


app = APPFormsQR()

if __name__ == "__main__":
    app.interface()
