"""
Routes and views for the flask application.
"""
from ast import Pass
from sqlalchemy.inspection import inspect
from collections import defaultdict
import os
import logging
from venv import create
import pandas as pd
import datetime as dt
from functools import wraps
from flask import (
    Flask,
    render_template,
    request,
    session,
    flash,
    redirect,
    url_for,
    jsonify,
    abort,
)
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask_sqlalchemy import SQLAlchemy

from DoctorsSchedule import app, db
from DoctorsSchedule.database import *

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    return result

@app.route('/')
def index():
    """Renders the home page."""
    schedule = Schedule.query.order_by(Schedule.doctor_specialization).all()
    return render_template(
        'index.html',
        title='جدول برنامه',
        schedule=schedule
    )

@app.route('/player')
def player():
    """Renders the player."""
    
    return render_template(
        'player.html',
        title='player',
        schedule=schedule
    )

@app.route('/schedule')
def schedule():
    """Renders the schedule page."""
    now = dt.datetime.now()
    t = now.hour
    tshift = "عصر" if t >= 12 else "صبح"
    week_day = dt.datetime.today().weekday()
    if week_day == 5:
        week_day = "شنبه"
    elif week_day == 6:
        week_day = "یکشنبه"
    elif week_day == 0:
        week_day = "دوشنبه"
    elif week_day == 1:
        week_day = "سه‌شنبه"
    elif week_day == 2:
        week_day = "چهارشنبه"
    elif week_day == 3:
        week_day = "پنج‌شنبه"
    elif week_day == 4:
        week_day = "جمعه"

    schedule = Schedule.query.filter(Schedule.weekday == week_day). \
        filter(Schedule.shift == tshift)

    return render_template(
        'schedule.html',
        title=week_day,
        schedule=schedule,
        weekday=week_day,
        shift=tshift,
    )

@app.route('/broadcast')
def broadcast():
    """Renders the broadcast page."""
    now = dt.datetime.now()
    t = now.hour
    tshift1 = "عصر" if t >= 12 else "صبح"
    tshift2 = "عصر" if t <= 12 else "صبح"

    week_day = dt.datetime.today().weekday()
    if week_day == 5:
        week_day = "شنبه"
    elif week_day == 6:
        week_day = "یکشنبه"
    elif week_day == 0:
        week_day = "دوشنبه"
    elif week_day == 1:
        week_day = "سه‌شنبه"
    elif week_day == 2:
        week_day = "چهارشنبه"
    elif week_day == 3:
        week_day = "پنج‌شنبه"
    elif week_day == 4:
        week_day = "جمعه"

    schedule1 = Schedule.query.filter(Schedule.weekday == week_day). \
        filter(Schedule.shift == tshift1). \
        order_by(Schedule.doctor_specialization)
    schedule2 = Schedule.query.filter(Schedule.weekday == week_day). \
        filter(Schedule.shift == tshift2). \
        order_by(Schedule.doctor_specialization)

    phrases = Phrases.query.order_by(Phrases.logdate.desc()).all()
    ModernSlider = Version.query.order_by(Version.id.desc()).first()
 
    s1=''
    sss1 = {
        "doctor_specialization": [],
        "doctor_name": []
    }
    dn11=[]
    ds11=[] 
    dn12=[]
    ds12=[] 
    for i in schedule1:
        if i.doctor_specialization==s1:
           dn11 += [i.doctor_name]
           ds11 += [i.doctor_specialization]
           #doctor_specialization1["doctor_name"].append([i.doctor_name])
        else:
            dn12 += [i.doctor_name]
            ds12 += [i.doctor_specialization] 
        s1=i.doctor_specialization  

    #print(query_to_dict(schedule1))
    schedule1 = pd.DataFrame(query_to_dict(schedule1))
    #print(schedule1)

    for i in ds12:
        sss1["doctor_specialization"] += [i]
        select1 = schedule1.loc[schedule1['doctor_specialization'] == i]
        sss1["doctor_name"] += [select1["doctor_name"].tolist()]


    #################################################

    s2=''
    sss2 = {
        "doctor_specialization": [],
        "doctor_name": []
    }
    dn21=[]
    ds21=[] 
    dn22=[]
    ds22=[] 
    for i in schedule2:
        if i.doctor_specialization==s2:
           dn21 += [i.doctor_name]
           ds21 += [i.doctor_specialization]
           #doctor_specialization1["doctor_name"].append([i.doctor_name])
        else:
            dn22 += [i.doctor_name]
            ds22 += [i.doctor_specialization] 
        s2=i.doctor_specialization  
    schedule2 = pd.DataFrame(query_to_dict(schedule2))

    for i in ds22:
        sss2["doctor_specialization"] += [i]
        select2 = schedule2.loc[schedule2['doctor_specialization'] == i]
        sss2["doctor_name"] += [select2["doctor_name"].tolist()]

    return render_template(
        'broadcast.html',
        title=week_day,
        schedule1=pd.DataFrame(sss1),
        schedule2=pd.DataFrame(sss2),
        weekday=week_day,
        shift1=tshift1,
        shift2=tshift2,
        phrases=phrases,
        ModernSlider=ModernSlider
    )

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            flash("لطفا وارد شوید")
            # return jsonify({"status": 0, "message": "لطفا وارد شوید"}), 401
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    """User login/authentication/session management."""
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin":
            error = "نام کاربری نامعتبر"
        elif request.form["password"] != "admin":
            error = "رمز عبور نامعتبر"
        else:
            session["logged_in"] = True
            flash("شما وارد سیستم شدید")
            return redirect(url_for("dashboard"))

    return render_template("login.html", title='ورود', error=error)

@app.route("/logout")
def logout():
    """User logout/authentication/session management."""
    session.pop("logged_in", None)
    flash("شما از سیستم خارج شدید")
    return redirect(url_for("index"))

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    """dashboard"""
    if not session.get("logged_in"):
        abort(401)

    schedule = Schedule.query.order_by(Schedule.doctor_specialization).all()
    phrases = Phrases.query.order_by(Phrases.logdate.desc()).all()
    #dr_specialization = Specialization.query.order_by(Specialization.id.desc()).all()
    dr_specialization = Specialization.query.order_by(Specialization.name.asc()).all()
    doctors = Doctors.query.order_by(Doctors.name.asc()).all()

    return render_template("dashboard.html", title='پیشخوان', schedule=schedule, dr_specialization=dr_specialization, doctors=doctors, phrases=phrases)

@app.route("/add/specialization", methods=["POST"])
def add_specialization():
    """Adds new specialization to the database."""
    if not session.get("logged_in"):
        abort(401)

    # specialization_entry = Specialization(name=request.form["name"],description=request.form["description"])
    specialization_entry = Specialization(name=request.form["name"])
    db.session.add(specialization_entry)
    db.session.commit()

    error = "تخصص ایجاد شد"
    flash(error)
    return redirect(url_for("dashboard"))

@app.route("/delete/specialization/<sid>", methods=['POST', 'GET'])
def delete_specialization(sid):
    """delete specialization from the database."""
    if not session.get("logged_in"):
        abort(401)
    print(sid)
    try:
        Specialization.query.filter_by(id=sid).delete()
        db.session.commit()
        error = "حذف شد"
        flash(error)
    except Exception as e:
        result = {"status": 0, "message": repr(e)}
        flash(result)
    return redirect(url_for("dashboard"))

@app.route("/add/doctors", methods=["POST"])
def add_doctors():
    """Adds new doctors to the database."""
    if not session.get("logged_in"):
        abort(401)

    # doctors_entry = Doctors(name=request.form["dr_name"],description=request.form["dr_description"],specialization_id=request.form["specialization"])
    doctors_entry = Doctors(
        name=request.form["dr_name"], specialization_id=request.form["specialization"])
    db.session.add(doctors_entry)
    db.session.commit()

    error = "پزشک جدید افزوده شد"
    flash(error)
    return redirect(url_for("dashboard"))

@app.route("/delete/doctors/<sid>", methods=['POST', 'GET'])
def delete_doctors(sid):
    """delete doctors from the database."""
    if not session.get("logged_in"):
        abort(401)
    print(sid)
    try:
        Doctors.query.filter_by(id=sid).delete()
        db.session.commit()
        error = "حذف شد"
        flash(error)
    except Exception as e:
        result = {"status": 0, "message": repr(e)}
        flash(result)
    return redirect(url_for("dashboard"))

@app.route("/add/schedule", methods=["POST"])
def add_schedule():
    """Adds new schedule to the database."""
    if not session.get("logged_in"):
        abort(401)

    drs = Doctors.query.filter(
        Doctors.id == request.form["doctor_name"]).first()
    sdr = Specialization.query.filter(
        Specialization.id == drs.specialization_id).first()
    #schedule_entry = Schedule(weekday=request.form["weekday"],start_hour=request.form["start_hour"],end_hour=request.form["end_hour"],doctor_name=drs.name,doctor_specialization=sdr.name)
    schedule_entry = Schedule(
        weekday=request.form["weekday"], shift=request.form["shift"], doctor_name=drs.name, doctor_specialization=sdr.name)
    db.session.add(schedule_entry)
    db.session.commit()

    error = "برنامه هفتگی برای پزشک افزوده شد"
    flash(error)
    return redirect(url_for("dashboard"))

@app.route("/add/group-schedule", methods=["POST"])
def add_group_schedule():
    """Adds new group schedule to the database."""
    if not session.get("logged_in"):
        abort(401)

    weekday=request.form["weekday"]
    shift=request.form["shift"]
    doctor_list = request.form.getlist('check')  # getting client list
    for i in doctor_list:
        drs = Doctors.query.filter(Doctors.id == i).first()
        sdr = Specialization.query.filter(Specialization.id == drs.specialization_id).first()
        schedule_entry = Schedule(weekday=weekday, shift=shift, doctor_name=drs.name, doctor_specialization=sdr.name)
        db.session.add(schedule_entry)
        db.session.commit()
        error = "برنامه هفتگی برای " + drs.name + " افزوده شد"
        flash(error)

    return redirect(url_for("dashboard"))

@app.route("/delete/schedule/<sid>", methods=['POST', 'GET'])
def delete_schedule(sid):
    """delete schedule from the database."""
    if not session.get("logged_in"):
        abort(401)
    print(sid)
    try:
        Schedule.query.filter_by(id=sid).delete()
        db.session.commit()
        error = "برنامه از لیست برنامه هفته حذف شد"
        flash(error)
    except Exception as e:
        result = {"status": 0, "message": repr(e)}
        flash(result)
    return redirect(url_for("dashboard"))

@app.route("/delete/group-schedule", methods=["POST"])
def delete_group_schedule():
    """delete group schedule from the database."""
    if not session.get("logged_in"):
        abort(401)

    Schedule.query.delete()
    db.session.commit()
    error = "لیست برنامه هفته حذف شد"
    flash(error)

    return redirect(url_for("dashboard"))

@app.route("/update/ModernSlider", methods=["POST"])
def update_ModernSlider():
    """Update ModernSlider"""
    if not session.get("logged_in"):
        abort(401)
    
    ModernSlider = Version(major=0, minor=0, build=0, revision=0,identifiers=request.form["autoplaySpeed"],name=request.form["speed"],description="0")
    db.session.add(ModernSlider)
    db.session.commit()
    error = "زمان بندی اسلایدر بروز شده"
    flash(error)
    return redirect(url_for("dashboard"))

@app.route("/add/phrase", methods=["POST"])
def add_phrases():
    """Adds new phrase to the database."""
    if not session.get("logged_in"):
        abort(401)

    file = request.files['file']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    error1 = "فایل با موفقیت بارگذاری شد"
    flash(error1)
    phrase_entry = Phrases(
        phrase=request.form["phrases"], file_address=file.filename)
    db.session.add(phrase_entry)
    db.session.commit()
    error2 = "یادداشت افزوده شد"
    flash(error2)
    return redirect(url_for("dashboard"))

@app.route("/delete/phrase/<sid>", methods=['POST', 'GET'])
def delete_phrase(sid):
    """delete phrase from the database."""
    if not session.get("logged_in"):
        abort(401)
    print(sid)
    try:
        Phrases.query.filter_by(id=sid).delete()
        db.session.commit()
        error = "حذف شد"
        flash(error)
    except Exception as e:
        result = {"status": 0, "message": repr(e)}
        flash(result)
    return redirect(url_for("dashboard"))


''''''''''''''''''''''''''''''''''''


@app.route('/ChangeLog')
def ChangeLog():
    version = Version.query.order_by(Version.id.desc()).limit(10).all()
    return render_template('ChangeLog.html',
                           title='روند تغییرات',
                           version=version)
