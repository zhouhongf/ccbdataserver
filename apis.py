class APIs:
    api_mauhy_summary = {'name': 'mau_hy_summary_branch',
                  'urls': {
                      'getMauHyLatestYearMonth': '/mauhy/latestyearmonth',
                      'checkMauHySummary': '/mauhy/summarycheck',
                      'getMauHySummary': '/mauhy/summary',
                      'getMauHyMaxrate': '/mauhy/maxrate',
                  }
                         }

    api_mauhy_target = {'name': 'mau_hy_target', 'urls': {'getMauHyTarget': '/mauhy/target'}}

    api_mauhy_month = {'name': 'mau_hy_month',
                       'urls': {'getMauHyMonth': '/mauhy/month/mauaccum',
                                }
                       }
