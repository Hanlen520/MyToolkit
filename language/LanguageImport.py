# -*- coding: cp936 -*-
import xlrd
import os
import sys
from xml.dom.minidom import parse


# reload(sys)
# sys.setdefaultencoding( "utf-8" )
"""
��������֤�ű�,������APK
���ȼ��Ĭ������(��Ĭ��������Ӣ�������,�ȶԵ���values-en, ʵ���� values
"""
class TranslateXml(object):
    #������Ҫ���Ե��ֶ�

    def __init__(self, xml_based_foder, excel_file):
        self.lang_tables = {

            'CHINE_NEW': 'zh-rCN', # ��������
             'CHINE_HK': 'zh-rHK', # ��������
            'ENGLISH': 'en',        # Ӣ��
            # 'FRENCH': 'fr',      # ����
            # 'DUTCH': 'nl',       # ����
            # 'GERMAN': 'de',      # �¹�
            # 'GREEK': 'el',       # ϣ��
            # 'HUNGARIAN': 'hu',   # ������
            # 'ITALIAN': 'it',     # �����
            # 'PORTUGUESE': 'pt',  # ������
            # 'SPANISH': 'es',     # ������
            # 'TURKISH': 'tr',     # ������
            # 'POLISH': 'pl',      # ����
            # 'CZECH': 'cs',       # �ݿ�
            # # 'MALAY': 'ms',       # ������
            # # 'INDONESIAN': 'in',  # ӡ��
            # # 'SLOVAK': 'sk',      # ˹�工��
            # 'ROMANIAN': 'ro',    # ��������
            # 'SLOVENIAN': 'sl',   # ˹��������
            # # 'THAI': 'th',        # ̩��
            # 'SERBIAN': 'sr',     # ����ά��
            # 'GALICIAN': 'gl',    # ��������
            # # 'VIETNAMESE': 'vi',  # Խ��
             'BRAZILIAN': 'pt-rBR', # ����
            # # 'JAPANESE': 'ja',    # ����
            # # 'LATINESP': 'es-rLA',  # ������������
            # # 'FARSI': 'fa',        # ��˹
            # 'CROATIAN': 'hr',	    # ���޵���
            # 'RUSSIAN': 'ru',	    # ����
            # # IDOL3 �� MIE ����
             'ARABIC': 'ar',            # ��������
            # 'CATALAN': 'ca',           # ��̩������
            # 'DANISH': 'da',            # ����
            # 'FINNISH': 'fi',           # ����
            # 'FRENCH_CA': 'fr-rCA',     # ����-���ô�
            # 'NORWEGIAN': 'no',         # Ų��
            # 'SWEDISH': 'sv',           # ���
            # # 'EUSKERA': 'eu',           # ��˹��
            # # IDOL3 ��������
            'ALBANIAN': 'sq'         # ������������
            # # 'BENGALI': 'bn-rBD',       # �ϼ���
            # 'BULGARIAN': 'bg',         # ����������
            # # 'CAMBODIAN': 'km-rKH',     # ����կ
            # 'ESTONIAN': 'et',          # ��ɳ������
            # 'HEBREW': 'he',            # ϣ������
            # # 'KOREAN': 'ko',            # ������
            # # 'LAOTIAN': 'lo-rLA',       # ������
            # 'LATVIAN': 'lv',           # ����ά����
            # 'LITHUANIAN': 'lt',        # ������
            # 'MACEDONIAN': 'mk',        # �����CATALAN
            # # 'MYANMAR': 'my-rMM',       # ���
            # 'UKRAINIAN': 'uk',         # �ڿ�����
            # # 'URDU': 'ur',              # ������
            # # 'HINDI': 'hi-rIN',          # ӡ����
            # 'SLOVAKIAN': 'sk',           #˹�工��
            # # 'BASQUE': 'eu'
        }
        # self.ignore = ["", ""]
        self.base_folder = xml_based_foder
        wb = xlrd.open_workbook(excel_file)
        self.sheet = wb.sheet_by_index(0)
        #�˴����Ե���,��Щ�������ļ���һ�и�ʽ��ͬ
        self.refNames = list(map(lambda x: x.split(":")[-1], self.sheet.col_values(0)[1:]))


    #��ȡ�������Ʋ���д
    def languages_from_excel(self):

        return list(map(lambda x: str(x.value.upper()), self.sheet.row(0)[1:]))

    #��ȡlang_tables�ж�������Բ���д
    def languages_from_defined(self):
        return list(map(lambda x: x.upper(), self.lang_tables.keys()))

    def values_from_excel(self, language):
        values = {}
        translations = self.sheet.col_values(list(map(lambda x: x.upper(), self.sheet.row_values(0))).index(language))[1:]
        for refName in self.refNames:
            #print translation
            values[refName] = translations[self.refNames.index(refName)].strip()
        return values

    def values_from_xml(self, file_path):
        values = {}
        doc = parse(file_path)
        strings = doc.getElementsByTagName("string")
        for refName in self.refNames:
            for string in strings:
                if string.getAttribute("name") == refName:
                    for child_node in string.childNodes:
                        if child_node.nodeType == 3:
                            values[refName] = child_node.nodeValue
        return values


    def check_result(self, values_from_xml, values_from_excel, language, file_path = None):
        for key in values_from_xml.keys():

            flag = False
            if "&gt;" in values_from_xml[key]:
                values_from_xml[key] = values_from_xml[key].replace("&gt;", ">")
            if "&lt;" in values_from_xml[key]:
                values_from_xml[key] = values_from_xml[key].replace("&gt;", "<")
            if "\\" in values_from_xml[key]:
                values_from_xml[key] = values_from_xml[key].replace("&quot;", "")
                flag = True

            if values_from_excel[key][0] == '"' and values_from_excel[key][-1] == '"':
                if flag:
                    values_from_xml[key] = '"' + values_from_xml[key] + '"'
                else:
                    values_from_xml[key] = '"' + values_from_xml[key][1: -1] + '"'

        if values_from_xml == values_from_excel:
            print("check " + language + " is passed!")
        else:
            print("check " + language + " is failed, please check the details as below:")
            print ("================values_from_xml==========================")
            print ("path is " + file_path)
            # print values_from_xml.keys()
            # print values_from_excel.keys()
            for key in filter(lambda x:values_from_excel[x] != values_from_xml[x], values_from_xml):
                # print "%s : %s"%(key,values_from_xml[key])
                print (key + ":")
                print (values_from_xml[key].encode("utf-8"))
            print ("************values_from_excel****************************")
            for key in filter(lambda x:values_from_xml[x] != values_from_excel[x], values_from_excel):
                print (key + ":")
                print (values_from_excel[key].encode("utf-8"))

    def main(self):
        languages_from_excel = self.languages_from_excel()
        languages_from_defined = self.languages_from_defined()

        if len(list(filter(lambda x: x in languages_from_defined, languages_from_excel))) == len(languages_from_excel):
            print ("all languages are existed in excel, check is passed!")
        else:
            print (filter(lambda x: x not in languages_from_defined, languages_from_excel))
        if len(list(filter(lambda x: os.path.isdir(os.path.join(self.base_folder, "values-" + self.lang_tables[x])) and os.path.isfile(os.path.join(self.base_folder, "values-" + self.lang_tables[x]) + "\\" + "strings.xml"), languages_from_excel))) == len(languages_from_excel):
            print ("all strings.xml file and corresponding folder are existed!")
        else:
            print ("the below languages are missed from xml files:")
            print (list(filter(lambda x: not os.path.isdir(os.path.join(self.base_folder, "values-" + self.lang_tables[x])) or not os.path.isfile(os.path.join(self.base_folder, "values-" + self.lang_tables[x]) + "\\" + "strings.xml"), languages_from_excel)))
            for item in filter(lambda x: not os.path.isdir(os.path.join(self.base_folder, "values-" + self.lang_tables[x])) or not os.path.isfile(os.path.join(self.base_folder, "values-" + self.lang_tables[x]) + "\\" + "strings.xml"), languages_from_excel):
                del languages_from_excel[languages_from_excel.index(item)]

        for language in languages_from_excel:
            values_from_xml = self.values_from_xml(os.path.join(self.base_folder, "values-" + self.lang_tables[language]) + "\\" + "strings.xml")
            for key in values_from_xml.keys():
                if "'" in values_from_xml[key]:
                    if values_from_xml[key][0] != '"' or values_from_xml[key][-1] != '"':
                        print ('string is not start and end with "' + " and language is " + language + ", please check " + os.path.join(self.base_folder, "values-" + self.lang_tables[language]) + "\\" + "strings.xml ", " for key " + key)
                    else:
                        values_from_xml[key] = values_from_xml[key][1:-1]
                    values_from_xml[key] = values_from_xml[key]
            values_from_excel = self.values_from_excel(language)
            self.check_result(values_from_xml, values_from_excel, language, os.path.join(self.base_folder, "values-" + self.lang_tables[language]) + "\\" + "strings.xml")

if __name__ == "__main__":
    # xml_based_foder = r"G:\language\apps_language\res"
    # excel_file = r"G:\language\apps_language\test.xlsx"
    xml_based_foder = r"G:\language\calendar\res"
    excel_file = r"G:\language\calendar\Calendar.xls"
    TranslateXml = TranslateXml(xml_based_foder, excel_file)
    TranslateXml.main()
