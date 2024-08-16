from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from .models import User, EditUser, FilterForm, SortForm, Apply, FilterApply
from .auth import is_validemail
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from werkzeug.exceptions import HTTPException
from . import db, baristaEmail, notifyEmail

views = Blueprint("views", __name__)


# 404 PAGE NOT FOUND
@views.errorhandler(HTTPException)
def handle_exception(e):
    if e.code == 404:
        return render_template('404.html', user=current_user), 404
    return e.description, e.code


## WEBPAGES ##

# HOME ROUTE

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)


# MENU ROUTE

@views.route("/menu")
def menu():
    return render_template("menu.html", user=current_user)


# NEWS ROUTE

@views.route("/news")
def news():
    return render_template("news.html", user=current_user)


# SETTINGS ROUTE

@views.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    edit_form = EditUser(obj=current_user)

    if request.method == 'POST' and 'edit_submit' in request.form:
        if edit_userfn(edit_form, current_user):
            return redirect(url_for('views.settings'))

    return render_template("settings.html", user=current_user, edit_form=edit_form)

# DELETE ACCOUNT IN SETTINGS ROUTE


@views.route('/settings/delete_account', methods=['POST'])
@login_required
def delete_userNORM():
    user_id = current_user.id

    # Call the helper function
    if 'confirm_delete_submit' in request.form:
        if delete_userfn(user_id):
            return redirect(url_for('views.home'))

    return redirect(url_for('views.settings'))


## ACTIONS ##


# GENERAL EDIT USER FUNCTION

def edit_userfn(edit_form, user):
    if edit_form.validate_on_submit():
        # EXISTING USER EMAIL CHECK
        existing_user = User.query.filter_by(
            email=edit_form.email.data).first()
        if existing_user and existing_user.id != user.id:
            flash('Email is already in use.', category='error')
            return False
        # SANCTA EMAIL DOMAIN VERIFICATION
        elif not is_validemail(edit_form.email.data):
            flash('Please use a valid school email.', category='error')
            return False

        # UPDATE EMAIL
        user.email = edit_form.email.data

        # UPDATE VALID PASSWORD INPUTS
        if edit_form.password.data:
            if edit_form.password.data == edit_form.confirm_password.data:
                user.password = generate_password_hash(edit_form.password.data)
            else:
                flash('Passwords do not match!', category='error')
                return False

        # ADD CHANGES
        db.session.commit()
        flash('User updated successfully!', category='success')
        return True

    return False


# GENERAL DELETE USER FUNCTION

def delete_userfn(user_id):
    user = User.query.get_or_404(user_id)

    # Admin Config Lock
    if user.email == 'admin@sanctamaria.school.nz':
        flash('This user cannot be deleted.', category='error')
        return False

    # Delete Associated Applications
    apply_pending = Apply.query.filter_by(
        author=user.id, status='pending').all()
    apply_accept = Apply.query.filter_by(
        author=user.id, status='accepted').all()

    for application in apply_pending:
        db.session.delete(application)

    for application in apply_accept:
        db.session.delete(application)

    # Delete the user
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return True


## ADMIN ROUTES ##

# DASHBOARD ROUTE

@views.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    if not current_user.is_staff:
        flash('You do not have permission to access this page.', category='error')
        return redirect(url_for('views.home'))

    query = User.query

    sort_by = request.args.get('sort_by', 'email_asc')
    sort_form = SortForm(data={'sort_by': sort_by})

    email_filter = request.args.get('email', '')
    is_staff_true = request.args.get('is_staff_true') == '1'
    is_staff_false = request.args.get('is_staff_false') == '1'

    filter_form = FilterForm(data={
        'email': email_filter,
        'is_staff_true': is_staff_true,
        'is_staff_false': is_staff_false
    })

    # SORT USER

    if sort_by == 'email_asc':
        query = User.query.order_by(User.email.asc())
    elif sort_by == 'email_desc':
        query = User.query.order_by(User.email.desc())
        # STAFF - [ INVERTED ASC/DESC TO MAKE SENSE ]
    elif sort_by == 'is_staff_asc':
        query = User.query.order_by(User.is_staff.desc())
    elif sort_by == 'is_staff_desc':
        query = User.query.order_by(User.is_staff.asc())

    # FILTER USER
    if filter_form.validate_on_submit() and 'filter_submit' in request.form:
        email_filter = filter_form.email.data
        is_staff_true = filter_form.is_staff_true.data
        is_staff_false = filter_form.is_staff_false.data
        return redirect(url_for('views.dashboard', sort_by=sort_by, email=email_filter,
                                is_staff_true='1' if is_staff_true else '',
                                is_staff_false='1' if is_staff_false else ''))

    # APPLY FILTERS
    if email_filter:
        query = query.filter(User.email.contains(email_filter))
    if is_staff_true and not is_staff_false:
        query = query.filter_by(is_staff=True)
    elif is_staff_false and not is_staff_true:
        query = query.filter_by(is_staff=False)

    # USER PAGINATION
    page = request.args.get('page', 1, type=int)
    paginUsers = query.paginate(page=page, per_page=12)

    # RETAIN FILTER PARAMETERS ON PAGINATION
    filterprmtrs = {
        'sort_by': sort_by,
        'email': email_filter,
        'is_staff_true': '1' if is_staff_true else '',
        'is_staff_false': '1' if is_staff_false else ''
    }

    paginEntries = {'pages': [{'url': url_for('views.dashboard', page=page_num, **filterprmtrs),
                               'num': page_num, 'current': page_num == paginUsers.page}
                              for page_num in paginUsers.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2)]}

    # EDIT USER ROUTE

    edit_user_id = request.args.get('edit_user_id')
    edit_form = EditUser()
    if edit_user_id:
        user = User.query.get_or_404(edit_user_id)

        # Admin Config Lock
        if user.email == 'admin@sanctamaria.school.nz':
            flash('This user cannot be edited.', category='error')
            return redirect(url_for('views.dashboard', **filterprmtrs))

        # EDIT USER VALIDATION
        if request.method == 'POST' and 'edit_submit' in request.form:
            if edit_form.validate_on_submit():
                # HANDLES EMAIL AND PASSWORD VERIFICATION
                if edit_userfn(edit_form, user):
                    # ADMIN CHECKBOX - SEPARATE FROM DEFINITION
                    user.is_staff = 'is_staff' in request.form
                    db.session.commit()
                    return redirect(url_for('views.dashboard', **filterprmtrs))
            else:
                flash('Passwords do not match!', category='error')
        else:
            edit_form = EditUser(obj=user)

    return render_template("dashboard.html",
                           user=current_user, edit_form=edit_form, edit_user_id=edit_user_id,
                           filter_form=filter_form, sort_form=sort_form, paginUsers=paginUsers, paginEntries=paginEntries)


# DASHBOARD DELETE USER ROUTE

@views.route('/dashboard/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    # if not current_user.is_staff:
    #     flash('Access denied!', 'danger')
    #     return redirect(url_for('views.home'))

    # Call the helper function
    if 'confirm_delete_submit' in request.form:
        if delete_userfn(user_id):
            return redirect(url_for('views.dashboard'))

    return redirect(url_for('views.dashboard'))


# WEEK DATES

def get_week_dates(start_date, weeks_offset=0):
    dates = []
    # Beninging of the Week
    start_of_week = start_date - \
        timedelta(days=start_date.weekday()) + timedelta(weeks=weeks_offset)
    for tabledate in range(5):
        day_date = start_of_week + timedelta(days=tabledate)
        dates.append(day_date)
    return dates


# DETERMINE WEEK - A or B

def apply_whichweek(date):
    week_number = date.isocalendar()[1]
    return week_number % 2 == 0


# WEEK DEFITION DICTIONARY FOR EASY USE
def determine_week(today):
    current_week = today.isocalendar()[1]
    WeekANow = (current_week % 2 == 0)
    WeekBNow = not WeekANow

    if WeekANow:
        weekDateA = get_week_dates(today)
        weekDateB = get_week_dates(today, weeks_offset=1)
    else:
        weekDateA = get_week_dates(today, weeks_offset=1)
        weekDateB = get_week_dates(today)

    weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    datesWeekA = {weekday[tabledate]: weekDateA[tabledate]
                  for tabledate in range(5)}
    datesWeekB = {weekday[tabledate]: weekDateB[tabledate]
                  for tabledate in range(5)}

    return WeekANow, WeekBNow, weekDateA, weekDateB, datesWeekA, datesWeekB


# SEE ALL PAGINATION PAGES IF ADMIN

def pendingApply(user, page, pendform=None):
    query = Apply.query.filter_by(status='pending')

    # Filter Apply Form for Pending Applications
    if pendform:
        if pendform.schoolid.data and pendform.schoolid.data != 'None':
            query = query.filter(Apply.schoolid == pendform.schoolid.data)
        if pendform.date_duty.data and pendform.date_duty.data != 'None':
            query = query.filter(Apply.date_duty == pendform.date_duty.data)
        if pendform.date_day.data and pendform.date_day.data != 'None':
            query = query.filter(Apply.date_day == pendform.date_day.data)
        if pendform.yearlevel.data and pendform.yearlevel.data != 'None':
            query = query.filter(Apply.yearlevel == pendform.yearlevel.data)

    if user.is_staff:
        return query.paginate(page=page, per_page=6)
    else:
        return query.filter_by(author=user.id).paginate(page=page, per_page=6)


## APPLY ROUTES ##


# APPLY ROUTE

@views.route("/apply", methods=['GET', 'POST'])
@login_required
def apply():
    if request.method == 'POST':
        # Filter Apply Form
        applyform = FilterApply(request.form)
        if applyform.validate_on_submit():
            return redirect(url_for('views.apply',
                                    schoolid=applyform.schoolid.data,
                                    date_duty=applyform.date_duty.data,
                                    date_day=applyform.date_day.data,
                                    yearlevel=applyform.yearlevel.data))
    else:
        applyform = FilterApply(request.args)

    # Base query for accepted applications
    query_accept = Apply.query.filter_by(status='accepted')

    posts = Apply.query.all()
    post_accept = query_accept.all()

    # DISPLAY DATE UNDER WEEKDAY
    today = datetime.now().date()
    WeekANow, WeekBNow, weekDateA, weekDateB, datesWeekA, datesWeekB = determine_week(
        today)

    # PENDING APPLICATION PAGINATION
    page = request.args.get('page', 1, type=int)
    post_pending = pendingApply(current_user, page, pendform=applyform)

    # RETAIN FILTER PARAMETERS ON PAGINATION
    filterprmtrs = {key: value for key,
                    value in request.args.items() if key != 'page'}

    paginPages = {'pages': [{'url': url_for('views.apply', page=page_num, **filterprmtrs),
                             'num': page_num, 'current': page_num == post_pending.page}
                            for page_num in post_pending.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2)]}

    return render_template("apply.html", user=current_user, posts=posts,
                           post_accept=post_accept, post_pending=post_pending,
                           weekDateA=weekDateA, weekDateB=weekDateB,
                           datesWeekA=datesWeekA, datesWeekB=datesWeekB, today=today,
                           WeekANow=WeekANow, WeekBNow=WeekBNow, applyform=applyform,
                           paginPages=paginPages)


# CREATE APPLICATIONS ROUTE

@views.route("/apply/submit_duty", methods=['GET', 'POST'])
@login_required
def create_dutydate():
    if current_user.is_staff:
        flash('You cannot apply as admin.', category='error')
        return redirect(url_for('views.apply'))

    if request.method == "POST":
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        date_duty = request.form.get('date_duty')
        date_day = request.form.get('date_day')
        yearlevel = request.form.get('yearlevel')

        # Year Level Validation
        if not firstname or not lastname or not yearlevel:
            flash('Full name, date and year level required.', category='error')
        elif yearlevel in ['≤10']:
            flash('Year 10 students or below are unable to apply for duty.',
                  category='error')
        else:
            # Max Baristas on Given Date for Application Purposes
            barista_max = 4
            current_count = Apply.query.filter_by(
                status='accepted', date_duty=date_duty, date_day=date_day).count()
            if current_count >= barista_max:
                flash(f'{date_day}, {date_duty} is full: {
                      barista_max} baristas max.', category='error')

            # Max 4 Applications
            elif Apply.query.filter_by(author=current_user.id).count() >= 4:
                flash('You cannot submit more than 4 applications.',
                      category='error')

            else:
                # Formatting User Apply Input
                post = Apply(
                    firstname=firstname, lastname=lastname,
                    date_duty=date_duty, date_day=date_day,
                    yearlevel=yearlevel, email=current_user.email, author=current_user.id,
                    schoolid=current_user.schoolid
                )
                db.session.add(post)
                db.session.commit()
                flash('Successfully applied!', category='success')

                # Store Selected Duty Date
                session['selected_duty_day'] = date_day
                session['selected_duty_week'] = date_duty

                # Redirect to the 'apply' route
                return redirect(url_for('views.apply'))

    # DISPLAY DATE UNDER WEEKDAY
    today = datetime.now().date()
    WeekANow, WeekBNow, weekDateA, weekDateB, datesWeekA, datesWeekB = determine_week(
        today)
    post_accept = Apply.query.filter_by(status='accepted').all()

    return render_template('submitduty.html', user=current_user,
                           weekDateA=weekDateA, weekDateB=weekDateB,
                           datesWeekA=datesWeekA, datesWeekB=datesWeekB,
                           today=today, WeekANow=WeekANow, WeekBNow=WeekBNow,
                           post_accept=post_accept)


# DELETE PENDING APPLICATIONS

@views.route("/apply/delete-apply/<id>", methods=['POST'])
@login_required
def delete_duty(id):
    application = Apply.query.filter_by(id=id, status='pending').first()
    if not application:
        flash('Application does not exist.', category='error')
    elif current_user.id != application.author and not current_user.is_staff:
        flash('You do not have permission to delete this application.',
              category='error')
    else:
        # Temporarily store the application ID for confirmation
        session['pending_delete'] = id

        if 'confirm_delete_submit' in request.form:
            # Retrieve the application ID from the session
            application_id = session.pop('pending_delete', None)

            if application_id:
                application = Apply.query.get_or_404(application_id)
                db.session.delete(application)
                db.session.commit()
                flash('Application deleted.', 'success')
            else:
                flash('Applicant not found.', 'error')
        return redirect(url_for('views.apply'))

    return redirect(url_for('views.apply'))


# ACCEPT APPLICATIONS

@views.route("/apply/accept-apply/<int:post_id>", methods=['GET', 'POST'])
@login_required
def accept_application(post_id):
    post = Apply.query.get_or_404(post_id)

    # User is not Staff
    if not current_user.is_staff:
        flash('You do not have permission to do this.', category='error')
        return redirect(url_for('views.apply'))

    if request.method == 'POST' and 'confirm_accept_submit' in request.form:
        # Week Day Categories
        # Week A or Week B
        week = post.date_duty
        # Tuesday or Thursday
        day = post.date_day

        # Maximum of 4 Baristas on Given Date
        barista_max = 4
        accepted_count = Apply.query.filter_by(
            status='accepted', date_duty=week, date_day=day).count()
        if accepted_count >= barista_max:
            flash(f'{day}, {week} is full: {
                  barista_max} baristas max.', category='error')
        else:
            post.status = 'accepted'
            db.session.commit()

            # Access the user's email through the relationship
            user_email = post.user.email

            # Send the barista email
            acceptBarista = baristaEmail(user_email, week, day)
            if acceptBarista == "Sent":
                flash('Barista added and email sent!', category='success')
            else:
                flash('Barista added, but failed to send email.',
                      category='warning')

        return redirect(url_for('views.apply'))
    return redirect(url_for('views.apply'))


# DELETE ACCEPTED APPLICATIONS

@views.route("/apply/delete-duty/<id>", methods=['POST'])
@login_required
def delete_accept(id):
    application = Apply.query.filter_by(id=id, status='accepted').first()
    if not application:
        flash('Barista does not exist.', category='error')
    elif current_user.id != application.author and not current_user.is_staff:
        flash('You do not have permission to remove this person.', category='error')
    else:
        # Temporarily store the application ID for confirmation
        session['pending_delete'] = id

        if 'confirm_delete_submit' in request.form:
            # Retrieve the application ID from the session
            application_id = session.pop('pending_delete', None)

            if application_id:
                application = Apply.query.get_or_404(application_id)
                db.session.delete(application)
                db.session.commit()
                flash('Barista removed.', 'success')
            else:
                flash('Application ID not found.', 'error')

    return redirect(url_for('views.apply'))


# NOTIFY ACCEPTED USER BARISTAS

def notifyDuty():
    today = datetime.now().date()
    weekday_name = today.strftime('%A')  # Get Today

    # Week A or Week B
    is_week_a = apply_whichweek(today)

    # Get all Baristas for the Day
    duty_applications = Apply.query.filter_by(status='accepted', date_day=weekday_name).all()

    for baristaGroup in duty_applications:
        # Week A Tuesday
        if is_week_a and weekday_name == 'Tuesday' and baristaGroup.date_duty == 'Week A':
            user_email = baristaGroup.user.email
            notifyEmail(user_email, 'Week A', 'Tuesday')

        # Week A Thursday
        elif is_week_a and weekday_name == 'Thursday' and baristaGroup.date_duty == 'Week A':
            user_email = baristaGroup.user.email
            notifyEmail(user_email, 'Week A', 'Thursday')

        # Week B Tuesday
        elif not is_week_a and weekday_name == 'Tuesday' and baristaGroup.date_duty == 'Week B':
            user_email = baristaGroup.user.email
            notifyEmail(user_email, 'Week B', 'Tuesday')

        # Week B Thursday
        elif not is_week_a and weekday_name == 'Thursday' and baristaGroup.date_duty == 'Week B':
            user_email = baristaGroup.user.email
            notifyEmail(user_email, 'Week B', 'Thursday')