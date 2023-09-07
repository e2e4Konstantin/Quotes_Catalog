tables = ['3.4-0-1-0-3', '3.4-0-1-0-4', '3.4-0-1-0-5', '3.4-0-1-0-6', '3.4-0-1-0-20', '3.4-0-1-0-21', '3.4-0-1-0-22', '3.4-0-1-0-23', '3.4-0-1-0-24']
# Table(code='3.4-0-1-0-3', title='Таблица 3.4-3. Ударно-вращательное бурение скважин глубиной до 10 м, диаметром 105 мм', subsection=None, section=None, collection='3.4', chapter='3')

table = tables[0]
print(table)

chapter = table.split('.')[0]

collection = table.split('-')[0]
section = '-'.join(table.split('-')[:2])
subsection = '-'.join(table.split('-')[:3])

print(chapter, collection, section, subsection)