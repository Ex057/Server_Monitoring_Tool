from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


from datetime import datetime
from .testlogic import check_dhis2_instance


from . import monitor_bp



@monitor_bp.route('/', methods=['GET', 'POST'])

def check_dhis2():

    if request.method == 'POST':
        base_url = request.form['base_url']
        username = request.form['username']
        password = request.form['password']
        result = check_dhis2_instance(base_url, username, password)
        print(result)
        tests = [{'testTime':result[3], 'available':result[0],'analytics':result[1],'dashboards':result[2],'username':username,'instance':base_url}]
    
        return render_template('blog/index.html', results = tests)
    
    return render_template('blog/index.html')


