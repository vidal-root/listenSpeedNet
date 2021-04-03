import time
import speedtest
from datetime import datetime
import os
import csv

class listenSpeedNet:
    def __init__(self):
        self.speed_download = None
        self.speed_upload = None
        self.error = True
        self.seconds = None
        self.speed_net()

    def speed_net(self):
        # result[0] -> minutos | result[1] -> extensão
        result = self.validate_input()
        self.seconds = result[0] * 60

        while True:
            try:
                speedtester = speedtest.Speedtest()
                self.speed_download = round(speedtester.download(threads=None)*(10**-6), 2)
                self.speed_upload = round(speedtester.upload(threads=None)*(10**-6), 2)
                self.create_file(result[1])
                time.sleep(self.seconds)
            except:
                print('Erro na requisição, aguardando conexão...')
                time.sleep(5)

    def validate_input(self):
        arr_out = []

        print('Iniciando programa, os dados coletados serão em Megabit (Mb).')

        while self.error:
            try:
                minute = int(input('Deseja verificar a velocidade de internet de quantos em quantos minutos?: '))
                self.error = False
                if minute < 1:
                    minute = 1
            except:
                print('É preciso informar um numero inteiro! Tente novamente.')

        self.error = True

        while self.error:
            type_file = input('Deseja obter qual tipo de arquivo? \n 1 - CSV \n 2 - TXT \n')

            if 'csv' in type_file:
                type_file = '1'
            if 'txt' in type_file:
                type_file = '2'

            if type_file.isnumeric():
                if int(type_file) == 1 or int(type_file) == 2:
                    self.error = False
                else:
                    print('Não entendi a opção desejada, tente novamente!')
            else:
                print('Não entendi a opção desejada, tente novamente!')

        arr_out.append([minute, int(type_file)])

        if int(type_file) == 1:
            print('Você escolheu "CSV". Iniciando Verificação, não feche o programa...')
        else:
            print('Você escolheu "TXT". Iniciando Verificação, não feche o programa...')

        return arr_out[0]

    def create_file(self, type_file):
        file_exists = None
        dt_now = datetime.now().strftime('%d/%m/%Y %H:%M')

        if (type_file == 1):
            type = 'csv'
            file_exists = os.path.isfile(os.getcwd() + os.sep + 'Tesde de Velocidade.' + type)
        else:
            type = 'txt'

        print('Inserindo novo registro...')

        with open(os.getcwd() + os.sep + 'Tesde de Velocidade.' + type, 'a', newline='', encoding='utf-8') as csv_file:
            if(type == 'csv'):
                fieldnames = ["Data", "Download", "Upload"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow({"Data": dt_now, "Download": self.speed_download, "Upload": self.speed_upload})
            else:
                ds_text = dt_now + ', Donwload: ' + str(self.speed_download) + ' Mb, Upload: ' + str(self.speed_upload) + ' Mb'
                csv_file.write(ds_text + os.linesep)

listen = listenSpeedNet()