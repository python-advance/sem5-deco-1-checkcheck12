# Шахов Кирилл
# ИВТ 3 курс  
#Инвариантная СР
#2.1 Разработать прототип программы «Калькулятор», позволяющую выполнять базовые арифметические действия и функцию обертку, 
#сохраняющую название выполняемой операции, аргументы и результат в файл
#2.2 Дополнение программы «Калькулятор» декоратором, сохраняющий действия, которые выполняются в файл-журнал.
#2.3 Рефакторинг (модификация) программы с декоратором модулем functools
#2.4 Формирование отчета по практическому заданию и публикация его в портфолио.

#Вариативная СР
#2.3 Разработка функции-декоратора, вычисляющей время выполнения декорируемой функции.

def get_valutes():
    import urllib.request #определяет функции и классы , которые помогают в открытии URL. Откройте URL-адрес, 
    #который может быть либо строкой, либо Request объектом.
    from xml.etree import ElementTree as ET #для работы с XML файлами
    
    resp = ET.parse(urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp"))
    #распарсиваем данные с сайта 
    valutes = {}
    #findall - находит только элементы с тегом, которые являются прямыми потомками текущего элемента
    for row in resp.findall('Valute'):
        valutes.update({row.find('CharCode').text: float(row.find('Value').text.replace(",", "."))})
    valutes.update({'RUB': 1})
    return valutes


"""Функций для постановки запятой в нужном месте"""
def print_valutes(valutes):
    result = ''
    i = 0
    for valute in valutes:
        if (i>0):
            result+= ','+valute
        else:
            result+= valute        
        i+= 1
    print (result)


def write_log(func):# в качестве аргумента передается функция calculate_valute
    import functools
    import datetime
    import time    
    #функция обертка
    @functools.wraps(func)
    def wrapper(*args): #  В *args сложены все аргументы функции calculate_valute
        timeStart = datetime.datetime.now()
        #time.sleep(2)
        result = func(*args)
        timeEnd = datetime.datetime.now()
        with open("logger.txt", "a") as f:
            f.write(("*" * 30) + "\n")
            f.write("Начало: " + str(timeStart) + "\n")
            f.write(args[3]+": " + str(args[2]) + "\n")
            f.write(args[4]+": " + str(result) + "\n")
            f.write("Конец: " + str(timeEnd) + "\n")
            f.write("Время выполнения: " + str(timeEnd - timeStart) + "\n")
            f.write(("*" * 30) + "\n")            
        return result
    return wrapper

"""Функция конвертирующая валюту, которая декорируется логгером """    
@write_log
def calculate_valute(fromValuteValue,toValuteValue,unit,fromValute,toValute):
    koff = fromValuteValue / toValuteValue
    result = unit * koff
    return result

if __name__ == "__main__":
    valutes = get_valutes()
    print_valutes(valutes.keys())
    
        
    while True:
        try:
            fromValute = input("Выберите конвертируемую валюту: ")  
            toValute = input("Выберите конечную валюту: ") 
            
            fromValuteValue = valutes[fromValute]
            toValuteValue = valutes[toValute]
        except (KeyError):
            print("Таких валют не существует, убедитесь что вы правильно ввели.")
            #созданы с целью того, чтобы программа не зацикливалась
            continue
        break
    
    while True:
        try:
            Money = float(input("введите количество единиц валюты: "))
        except (TypeError, ValueError):
            print("Вы ввели неправильное значение, нужно вводить число.")
            continue
        break
    
    resultMoney = calculate_valute(fromValuteValue,toValuteValue,Money,fromValute,toValute)
    
    print (fromValute+": "+str(Money)+" = "+toValute+": "+str(resultMoney))
