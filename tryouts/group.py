# import openpyxl
#
# wb = openpyxl.Workbook()
# ws = wb.active
# for i in range(1, 25+1):
#     ws.append([i])
#
# # Expand handle at bottom
# # ws.sheet_properties.outlinePr.summaryBelow = True
# # ws.row_dimensions.group(2, 25-1, outline_level=1)
# # ws.row_dimensions.group(4, 9-1, outline_level=2)
# # ws.row_dimensions.group(6, 7-1, outline_level=3)
#
# # Expand handle at top
# # NOTE: Order counts!
# ws.sheet_properties.outlinePr.summaryBelow = False
# ws.row_dimensions.group(2+1, 25, outline_level=1)
# ws.row_dimensions.group(4+1, 9, outline_level=2)
# ws.row_dimensions.group(6+1, 7, outline_level=3)
#
# wb.save('testrows.xlsx')

classifier = ['chapter', 'collection', 'section', 'subsection', 'table', 'quote']
groups_level = {item: i for i, item in enumerate(classifier)}
print(groups_level)