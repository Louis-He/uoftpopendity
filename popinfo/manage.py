#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import requests
import re
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone

from popinfo.popdensity.models import Connrecord

def get_conn_data():
    print("[Info] Get connection data.")
    locations = ['0036', '0078', '0075', '0049', '0131', '0047', '0073', '0003', 'X073', 'X033', '0032', '0033', '0064',
                 '0072', 'A068', '0068', '0146', '0067', '0930', '0143', '0079', '0028', '0080', '0038', '0104', '0042',
                 '0089', '0088', 'A006', '0077', 'B006', '0103', '0006', '0134', '0133', '0132', '0066', '0130', '0128',
                 '0127', '0110', '0106', '0052', '0016', '0065', '0194', '0061', 'A061', '0145', '0056', '0057', '0062',
                 '0154', '0083', '0161', '0192', '0155', '0160', 'A005', '0005', '0024', '0022', '0004', '0020', '0007',
                 '0011', '0008', '0010', '0009', '0026', '0027', '0172', '0021', '0153', '0043', 'A008', '0019', 'A010',
                 '0070', '0575', '0420', '0502', '0501', '0421', '0426', '0429', '0434', '0435', '0443', 'A098', '0453',
                 '0455', '0503', '0012', 'B012', '0603', '0602', 'A030', '0600', '0098', '0518', '0515', '0514', '0509',
                 '0508', '0608', '0507', '0506', '0504', '0675', '0002', '0111', '0101', '0001', '0034', '0053', '0051',
                 '0050', '0041', '0030', '0029', '0023', '0528', '0014', '0013', '0123', '0415', '0411', '0405', '0401',
                 '0407', '0417', '0418', '0419', 'XMUS', 'XMSB', 'XLAW', 'XINN', 'XESC', '0025', 'XNEW', 'XROB', 'B010',
                 '0423', '0416', 'XXSU', 'XXFC', 'XXBC', 'XWDW', 'XVIC', 'XVAR', 'XSMC', '097A', '0430', '0156', '0530',
                 '0115', '0120', '0152', '0125', '0129', '0138', '0142', '0105', '0158', '0091', '0054', '0087', '0040',
                 'A032', '0195', '0171', '0071', '0082', '0090', '0097']
    url = "https://maps.wireless.utoronto.ca/stg/popUp.php?name="
    for location in locations:
        tmp_url = url + location
        res = requests.get(tmp_url, timeout=5)
        if(res.status_code == 200):
            res = res.text
            loc = re.search("<CENTER>.*</CENTER>", res)
            connection_num = re.search("Number of connections : .*?<P>", res)

            rec = Connrecord(recordtime=timezone.now(), location=loc, conn=connection_num)
            rec.save()
            # print(loc.group()[len("<CENTER>"):-len("</CENTER>")], connection_num.group()[len("Number of connections : <BQ>"):-len("<P>")])
        else:
            print("[Warning] Connection Timeout.")

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popinfo.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_conn_data, 'interval', seconds=10 * 60)
    scheduler.start()
    main()
