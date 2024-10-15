import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner
import requests
from datetime import datetime
import boto3


# Classe para gerenciar o aplicativo
class AppRegistro:
    def __init__(self):
        self.region_name = "us-east-1"


    def cache_aws_credentials(self):
        with st.popover("Credencial"):
            self.aws_access_key_id = st.text_input("AWS ACCESS KEY", type="password")
            self.aws_secret_access_key = st.text_input("AWS SECRET ACCESS KEY", type="password")
        
        self.interface()
        
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

    def interface(self):
        st.title("Registro de Entrada/Saída")

        Registro = st.selectbox("Selecione o tipo de entrada/saída", ["Entrada", "Saída", "Banheiro", "Volta do Banheiro"])

        if st.checkbox("Ativar scanner de QR Code"):
            qr_code = qrcode_scanner(key='qrcode_scanner')

            data, hora = self.obter_hora_sao_paulo()

            if qr_code:
                st.write(f"QR Code: {qr_code}")
                st.write(f"Tipo de Entrada/Saída: {Registro}")

                if data and hora:
                    st.write(f"Data: {data}, Hora: {hora}")
                    Data = f"{data} {hora}"

                    # Adicionando o botão de enviar
                    if st.button("Enviar Registro"):
                        self.Enviar_registro(Registro, qr_code, Data)
                else:
                    st.write("Não foi possível obter a data e hora de São Paulo.")
                    agora = datetime.now()
                    print(agora)




    def Enviar_registro(self, registro, matricula, data_hora):
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )
        try:
            table = dynamodb.Table('Tabela_Alunos_Sepex')
            response = table.put_item(
                Item={"Data": data_hora,
                      "Matricula": matricula,
                      "Registro": registro}
            )
            st.success(f"Registro: {registro}, Aluno com a matricula {matricula}, cadastrado com sucesso as {data_hora}")
        except Exception as e:
            st.warning(f"Erro ao cadastrar Aluno: {e}")

app = AppRegistro()

if __name__ == "__main__":
    app.cache_aws_credentials()
