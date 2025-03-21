from flask import render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_required, current_user
from . import monitor_bp
from .forms import ServerForm
from ..models import db, Server, test
from .testlogic import check_dhis2_instance
from sqlalchemy import select

@monitor_bp.route('/')
def index():
    tests = {}
    
    servers = Server.query.all()
    if servers:
        for server in servers:
            address = server.ip_address
            tests[server.id] = test.query.filter_by(ip_address = address ).first()
    return render_template('monitor/index.html', servers=servers, test=tests)

@monitor_bp.route('/server/<int:id>')
def server_details(id):
    print(id)
    stmt = select(Server).where(Server.id == id)
    server = db.session.execute(stmt).scalar_one_or_none()
    print(server)
    if server:
        tests = db.session.execute(select(test).where(test.ip_address == server.ip_address)).scalars().all()
    else:
        tests = []
    print(tests)
    return render_template('monitor/server_details.html', server=server, test=tests)

@monitor_bp.route('/server/<int:id>/logs')
def server_logs(id):
    server = Server.query.get_or_404(id)
    # Logic to retrieve logs
    logs = []
    return render_template('monitor/server_logs.html', server=server, logs=logs)

@monitor_bp.route('/reports')
def reports():
    # Logic to retrieve and generate reports
    reports = []
    return render_template('monitor/reports.html', reports=reports)

@monitor_bp.route('/run_test', methods=['POST'])
@login_required
def run_test():
    data = request.get_json()
    print(data)
    server_data = data.get('server')
    url = server_data.get('ip_address')
    username = server_data.get('user_name')
    password = server_data.get('password')
    print(url, username, password)
    if not url or not username or not password:
        return jsonify({"success": False, "message": "All parameters are required"}), 400
    
    # Assuming run_server_test is a function that runs the test and returns the result
    # e.g., {"result": "success", "metric1": 100, "metric2": 200, "metric3": 300}
    test_result = check_dhis2_instance(url, username, password)

    if test_result is None:
        return jsonify({"success": False, "message": "Failed to run test"}), 500

    # Insert the test result into the database
    
    
        
    
    new_test = test(
        ip_address = url,
        user_name = username,
        available = test_result[0],
        analytics = test_result[1],
        dashboards = test_result[2],
        testTime = test_result[3],
        owner_id = current_user.id,
        last_checked = test_result[3]
    )
    db.session.add(new_test)
    db.session.commit()
    
    
    return jsonify({"success": True, "message": "Test ran successfully"})