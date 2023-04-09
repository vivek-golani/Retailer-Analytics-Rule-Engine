
# =============================================================================
#     pathname, filename & macroname FOR TRIGGERING MACRO
# =============================================================================

pathname = path + '/Output/RARE ' + area + ' - ' + month + '.xlsb'
filename = 'RARE ' + area + ' - ' + month + '.xlsb'
macroname = 'CreateFromSelection'

# =============================================================================
#               MACRO TRIGGER CODE USING win32com client   
# =============================================================================

xl = win32com.client.Dispatch("Excel.Application")
wb = xl.Workbooks.Open(os.path.abspath(pathname))
xl.Application.Run("'" + filename + "'!" + macroname)
wb.Save()
xl.Application.Quit()
del xl
