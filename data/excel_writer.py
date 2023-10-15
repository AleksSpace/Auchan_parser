from datetime import datetime

from openpyxl.workbook import Workbook


def create_n_write_xlsx(data: dict):
    """Функция создаёт .xlsx документ в который записывает все xpath"""
    try:
        datetime_now = datetime.now()
        str_datetime_now = datetime_now.strftime("%Y-%m-%d_%H-%M-%S")
        name = f'file_{str_datetime_now}.xlsx'
        # создаем книгу
        wb = Workbook()
        # делаем единственный лист активным

        # sheet = wb.active
        for sheet_name, list_data in data.items():
            sheet = wb.create_sheet(title=sheet_name)

            for row in list_data:
                sheet.append(row)

            for column_cells in sheet.columns:
                max_length = 0
                column = column_cells[0].column_letter  # Получите буквенное обозначение столбца
                for cell in column_cells:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except Exception as ex:
                        raise Exception(f'Произошла ошибка: {ex}')
                adjusted_width = (max_length + 2)
                sheet.column_dimensions[column].width = adjusted_width
        wb.remove(wb.active)
        wb.save(name)
        return name
    except Exception as ex:
        raise Exception(f'Произошла ошибка во время создания xlsx документа: {ex}')
