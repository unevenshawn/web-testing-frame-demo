from testkit.case import create_test, str_join, entry_dir

from api.logUtil import LoggerUtil

logger = LoggerUtil.get_logger(__name__)
error_log = logger.error
info_log = logger.info
debug_log = logger.debug

workbook_suites = entry_dir()
for sheet_suite in workbook_suites:
    if not sheet_suite:
        continue
    debug_log(f'suite in test_ddt{sheet_suite}')
    # 在这个for循环里面的都是同一个xl_name和sheet_name
    xl_name = sheet_suite[0]['xl_name']
    sheet_name=sheet_suite[0]['sheetname']
    modulename = str_join("-", xl_name,sheet_name)

    # debug_log(f'测试步骤关键字包括：{list(suite.keys())}')
    # 因为一个sheet对应一个若干个test_case,而一个sheet只对应一个test类
    globals()[f'{modulename}'] = create_test(sheet_suite)
    debug_log(f'modulename是{modulename}')
