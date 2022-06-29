ALU / Nokia 7210 scanning host group for inventory
========================

## English:

#### Requirements:
* Paramiko library installed.
* Central router model Nokia SR 7750, scannable router model Nokia SAS 7210
* Tested with Python 3.7.4, Windows 7
* In the AGG_Scan.py executable file you need to specify the necessary subnets instead of 10.10.10.0/24 and 172.28.0.0/24 (line 20) or remove the check altogether.

#### Description:
A little script that I use when my boss asks me to re-inventorize equipment. It scans a group of routers of **Alcatel Lucent model 7210 SAS (now Nokia)**, then creates a text document which can be imported into excel.

#### Example:

We have a **service router model Nokia SR 7750** where all other **Nokia SAS 7210** routers are stacked on ospf.
On this router I execute the command:

	show router route-table | match 10.10.10. 
And I get entries like:

	10.30.10.16/32                               Remote  OSPF      54d03h14m  10
	10.10.10.6/32                                Remote  OSPF      01h18m34s  10
	10.10.10.7/32                                Remote  OSPF      97d19h52m  10
	10.10.10.8/32                                Remote  OSPF      97d19h51m  10
	10.10.10.9/32                                Remote  OSPF      97d19h51m  10
	10.10.10.10/32                               Remote  OSPF      97d19h51m  10
	10.10.10.11/32                               Remote  OSPF      97d19h51m  10
	10.10.10.12/32                               Remote  OSPF      97d19h52m  10
	10.10.10.13/32                               Remote  OSPF      97d19h52m  10
	10.10.10.14/32                               Remote  OSPF      23d22h05m  10

Then, I copy and paste these entries into the document **agg-ip.txt**. Then you can run the script, it will ask username and password to hosts (assuming that they are the same on the entire group of hosts scanned), then at the end of the scan it will also ask username and password to the service router to additionally get the **ip address match sdp label**.
At the end it creates a file agg-result.txt with the following content:

	10.10.10.6;router1;7210 SAS-M-1;NS123456789;00:01:02:07:ab:04;1001
	10.10.10.7;router2;7210 SAS-M-1;NS987654321;00:01:03:05:ab:04;1002
	10.10.10.8;router3;7210 SAS-M-1;NS010203045;00:01:04:06:ab:04;1003

Where from left to right ip address, hostname, host model, serial number, mac address, and sdp tag from the service router. All that remains is to import it into excel and put ";" as a separator.


<sub>PS: I have lived all my life in Donetsk (Ukraine) and my native language is Russian, I apologize for possible grammatical errors and comments in the code in Russian. Since recently, my dream is to speak English, I will be glad if you point out the errors, I will try to understand and correct them. <sub>

### Russian:

Требования:
* Установленная библиотека paramiko
* Центральный роутер модели Nokia SR 7750, сканируемые роутеры модели Nokia SAS 7210
* Протестировано на Python 3.7.4, ОС Windows 7
* В исполняемом файле AGG_Scan.py вам нужно указать необходимые вам подсети вместо 10.10.10.0/24 и 172.28.0.0/24 (line 20) либо вообще убрать проверку.

Небольшой скрипт которым я пользуюсь когда начальник просит произвести реинвентаризацию оборудования. Сканирует группу маршрутизаторов модели Alcatel Lucent (сейчас Nokia) 7210 SAS, затем создает текстовый документ который можно импортировать в excel.

У нас есть сервисный роутер модели Nokia SR 7750 куда стекаются по ospf все остальные маршрутизаторы Nokia SAS 7210.
На этом роутере исполняю команду:

	show router route-table | match 10.10.10. 
	
И получаю записи вида:

	10.30.10.16/32                               Remote  OSPF      54d03h14m  10
	10.10.10.6/32                                Remote  OSPF      01h18m34s  10
	10.10.10.7/32                                Remote  OSPF      97d19h52m  10
	10.10.10.8/32                                Remote  OSPF      97d19h51m  10
	10.10.10.9/32                                Remote  OSPF      97d19h51m  10
	10.10.10.10/32                               Remote  OSPF      97d19h51m  10
	10.10.10.11/32                               Remote  OSPF      97d19h51m  10
	10.10.10.12/32                               Remote  OSPF      97d19h52m  10
	10.10.10.13/32                               Remote  OSPF      97d19h52m  10
	10.10.10.14/32                               Remote  OSPF      23d22h05m  10

Затем, эти записи я копирую и вставляю в документ agg-ip.txt. После чего можно запускать скрипт, он спросит логин и пароль к хостам (подразумевается что они одинаковые на всей сканируемой группе хостов), затем по окончании сканирования он также спросит логин и пароль к сервис роутеру, чтобы дополнительно получить соответствие ip адреса sdp метке.
В конце создается файл agg-result.txt следующего содержания:

	10.10.10.6;router1;7210 SAS-M-1;NS123456789;00:01:02:07:ab:04;1001
	10.10.10.7;router2;7210 SAS-M-1;NS987654321;00:01:03:05:ab:04;1002
	10.10.10.8;router3;7210 SAS-M-1;NS010203045;00:01:04:06:ab:04;1003

Где слева направо ip адрес, имя хоста, модель хоста, серийный номер, мак адрес, и sdp метка с сервис роутера. Осталось только импортировать его в excel и указать в качестве разделителя ";".
