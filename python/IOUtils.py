#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paths

# Dado um arquivo a ser lido ele  retorna uma lista com os dados do arquivo
def read_file_to_list(filename):
  list_answer = []
  file = open(filename, 'r')
  for line in file:
      list_answer.append(line.strip())
  return list_answer


# Dado um arquivo a ser lido ele  retorna uma lista com os dados do arquivo
def read_file_to_dictlist(filename):
  list_answer = []
  file = open(filename, 'r')
  first_line = []
  for line in file:
    if (len(first_line) == 0):
      first_line = str(line).split('\n')[0].split(",")
    else:
      dictionary = {}
      lines = str(line).split('\n')[0].split(",")
      for i in range(0,len(first_line)):
        dictionary[first_line[i]] = lines[i]
      list_answer.append(dictionary)
  return list_answer

# Dada uma lista, salva os dados dessa lista num arquivo cujo nome eh passado
# O nome do arquivo deve ser no seguinte formato: path/nomeDoArquivo.extensao
def save_file(list, filename):
	file = open(filename, 'w')
	for line in range(0, len(list)):
		file.write(str(list[line]) + "\n")
	file.close()

# Dada uma lista de listas, salva os dados dessa lista num arquivo cujo nome eh passado
# O nome do arquivo deve ser no seguinte formato: path/nomeDoArquivo.extensao
def save_file_lists(lists, filename):
  file_ = open(filename, 'w')
  for line in lists:
    to_write = ""
    for i in range(len(line)):
      to_write += line[i]
      if (i != len(line)-1):
        to_write +=","
      else:
        to_write +="\n"
    try:
      to_write = to_write.decode('utf8').encode('utf8')
    except:
      try:
        to_write = to_write.encode('utf8')
      except:
        print "Can't convert to utf-8"
    file_.write(to_write)
  file_.close()

#Dado uma lista de elementos com elementos repetidos é retornado uma lista de elementos que não se repetem
def unique_element(list_):
  answer = []
  for element in list_:
    if (not (element in answer)):
      answer.append(element)
  return answer

'''dada uma lista de listas, retorna uma lista de dicionários'''
def lists_to_dicts(list):
    header = list[0]
    final_list = []
    for i in range(1,len(list)):
        line = list[i]
        new_column = {}
        for j in range(len(line)):
            column = line[j]
            new_column[header[j]] = column
        final_list.append(new_column)
    return final_list
