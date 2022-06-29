import time # Таймер для остановки программы.
import paramiko # Бибоиотека SSH подключений.
import re # Библиотека регулярных выражений.
import ipaddress # Библиотека проверки корректности ip адресов

class AGG_SCAN():

	def __init__(self):

		self.ip_list = open('./agg-ip.txt', 'r') # Файл с ip адресами.
		self.agg_ip_list = {}
		self.service_router = '10.0.0.1'

	def all_ip_validation(self):

		for ip in self.ip_list: # Для каждого ip в файле
			ip = ipaddress.IPv4Network(ip.split()[0], strict=False)
			if ip.num_addresses == 1: # Если у нас маска /32 то будет только 1 адрес.
				for addr in ip: # Таким образом мы распаковываем адрес из подсети, чтоб был без /32
					if addr in ipaddress.IPv4Network('10.10.10.0/24') or addr in ipaddress.IPv4Network('172.28.0.0/24'):
						self.agg_ip_list.setdefault(addr.exploded, {'hostname' : None, 'model' : None, 'serial' : None, 'mac' : None, 'sdp' : None})
					else:
						print ('Ошибка. Адрес '+str(ip)+' не находится в подсети 10.10.10.0/24 или 172.28.0.0/24\n')
						continue
			else:
				print (str(ip) + ' НЕ является лупбэком!')
				continue

	def connect_to_host(self, ip, login, password, port):

		try:
			client = paramiko.SSHClient()  # Открываем сессию.
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Добавляем ключ сервера в список известных хостов.
			client.connect(hostname=ip, username=login, password=password, port=port)  # Организуем подключение.
			time.sleep(1)

			self.agg_channel = client.invoke_shell()
			print(self.agg_channel.recv(1024).decode())

		except TimeoutError:
			print('\nПревышено время ожидания, хост '+str(ip)+' не отвечает на запросы...'); return False
		except EOFError:
			print('\nError reading SSH protocol banner\nНа '+str(ip)+' скорее всего достигнуто максимальное количество сессий...\n'); return False
		else:
			return True

	def connect_to_agg(self):

		self.__agg_login = input('\nВведите логин для подключения к agg: ')
		self.__agg_password = input('\nВведите пароль для подключения к agg: ')
		port_ssh = 22

		for ip in self.agg_ip_list:

			trigger = agg.connect_to_host(ip, self.__agg_login, self.__agg_password, port_ssh)
			if trigger: 
				agg.send_commands_to_agg_and_recieve_parameters(ip)
			else:
				print ('Узел '+str(ip)+' не доступен, перехожу к следующему...')
				continue

		agg.connect_to_sr()

	def send_commands_to_agg_and_recieve_parameters(self, ip):

		self.agg_channel.send('show chassis | match expression "Name|Type|Base MAC address|Serial number"\n'); time.sleep(.5)
		output = self.agg_channel.recv(8192)
		print('Считывание данных: \n', output.decode()); time.sleep(.5)

		agg_name    = re.findall(r'Name\s+[:]\s?(.*)', output.decode())
		agg_type    = re.findall(r'Type\s+[:]\s?(.*)', output.decode())
		agg_mac     = re.findall(r'Base MAC address\s+[:]\s?(.*)', output.decode())
		agg_serial  = re.findall(r'Serial number\s+[:]\s?(.*)', output.decode())

		self.agg_ip_list[ip]['hostname'] = agg_name[0].replace('\r','')
		self.agg_ip_list[ip]['model'] = agg_type[0].replace('\r','')
		self.agg_ip_list[ip]['mac'] = agg_mac[0].replace('\r','')
		self.agg_ip_list[ip]['serial'] = agg_serial[0].replace('\r','')

		print (self.agg_ip_list[ip])

		self.agg_channel.close()

	def connect_to_sr(self):

		self.__sr1_login = input('\nВведите логин для подключения к service_router: ')
		self.__sr1_password = input('\nВведите пароль для подключения к service_router: ')
		port_ssh = 22

		trigger = agg.connect_to_host(self.service_router, self.__sr1_login, self.__sr1_password, port_ssh)
		if trigger:
			agg.show_services_sdp_all()
		else:
			print('\nЧто то пошло не так...\nНажмите enter чтобы выйти...')



	def show_services_sdp_all(self):

		for ip in self.agg_ip_list:
			#[ \t*] - регулярное выражение для sr которое ожидает пробельные символы после ip, чтобы например с 10.10.10.1 не находило 10.10.10.10.
			self.agg_channel.send('show service sdp | match expression "'+str(ip)+'[ \t*]"\n'); time.sleep(.3) 
			output = self.agg_channel.recv(1024).decode()
			print(output)
			sdp = re.search(r'\d{4}', output)
			self.agg_ip_list[ip]['sdp'] = sdp.group(0)

		self.agg_channel.close()

		agg.create_and_fill_txt_file()

	def create_and_fill_txt_file(self):

		result = open('agg-result.txt', 'a')

		for ip in self.agg_ip_list:

			result.write(ip+';'+self.agg_ip_list[ip]['hostname']+';'+self.agg_ip_list[ip]['model']+';'+self.agg_ip_list[ip]['serial']+';'+self.agg_ip_list[ip]['mac']+';'+self.agg_ip_list[ip]['sdp']+'\n')



agg = AGG_SCAN()
agg.all_ip_validation()
agg.connect_to_agg()
