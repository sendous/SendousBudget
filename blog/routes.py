import datetime

from dateutil.relativedelta import relativedelta
from flask import render_template
from flask import session, redirect, url_for, flash, request, abort
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_user, current_user, logout_user, login_required

from blog import app, db, bcrypt
from blog.forms import RegistrationFrom, LoginForm, UpdateProfileForm, BuyForm, FilterBox
from blog.models import User, Buy

month = int(datetime.datetime.today().strftime('%m'))


@app.route('/', methods=['GET', 'POST'])
@register_breadcrumb(app, '.', 'Home')
def home():
    global month
    form = BuyForm()

    if 'startdate' not in session:
        startdate = datetime.datetime.today().strftime('%Y-%m-%d')
        enddate = datetime.datetime.today().strftime('%Y-%m-%d')
        buys = Buy.query.filter(Buy.date >= startdate). \
            filter(Buy.date <= enddate).all()
    else:
        startdate = session['startdate']
        enddate = session['enddate']
        buys = Buy.query.filter(Buy.date >= startdate). \
            filter(Buy.date <= enddate).all()

    if request.method == 'POST':
        if request.form['submit_button'] == 'Next':
            month += 1

        elif request.form['submit_button'] == 'Previous':
            startdate = datetime.datetime.today() + relativedelta(months=-1)
            enddate = datetime.datetime.today() + relativedelta(months=-2)
            buys = Buy.query.filter(Buy.date >= startdate). \
                filter(Buy.date <= enddate).all()
            flash(startdate.strftime('%Y-%m'))

    return render_template('home.html', form=form, buys=buys, title=startdate)


@app.route('/filter', methods=['GET', 'POST'])
def date():
    form = FilterBox()
    if form.validate_on_submit():
        session['startdate'] = form.startdate.data.strftime('%Y-%m-%d')
        session['enddate'] = form.enddate.data.strftime('%Y-%m-%d')
        return redirect(url_for('home'))
    return render_template('inc/filter.html', form=form, title='فیلتر')


@app.route('/buy/<int:buy_id>')
def detail(buy_id):
    buy = Buy.query.get_or_404(buy_id)
    return render_template('detail.html', buy=buy, title=buy.desc)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationFrom()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash('ثبت نام با موفقیت و بطور کامل انجام شد', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form, title='ثبت نام')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'), title="Login")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('شما با موفقیت وارد حساب کاربری خود شدید', 'success')
            return redirect(next_page if next_page else url_for('home'))
        else:
            flash('ایمیل یا نام کاربری اشتباه است', 'danger')
    return render_template('login.html', form=form, title='ورود')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('شما بطور کامل از حساب خود خارج شدید', 'success')
    return redirect(url_for('home'), title='خروج')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('اطلاعات شما با موفقیت ثبت شد', 'info')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('profile.html', form=form, title='پروفایل ')


@app.route('/buy/new', methods=['GET', 'POST'])
@login_required
def new_buy():
    form = BuyForm()
    if form.validate_on_submit():
        # s = re.match('^(?P<string>[A-Za-z-W]+)(?P<integer>[0-9]+)$', form.desc.data)
        # if s:
        #     buy = Buy(desc=s.group('string'), price=int(s.group('integer')), author=current_user, category=form.category.data)
        #     db.session.add(buy)
        #     db.session.commit()
        #     flash('عملیات با موفقیت انجام شد', 'info')
        #     return redirect(url_for('home'))
        # else:
        #     flash("!!!")
        buy = Buy(desc=form.desc.data, price=form.price.data, author=current_user,
                  category=form.category.data)
        db.session.add(buy)
        db.session.commit()
        flash('عملیات با موفقیت انجام شد', 'info')
        return redirect(url_for('home'))
    return render_template('create_buy.html', form=form, title='خرید جدید')


@app.route('/buy/<int:buy_id>/delete')
@login_required
def delete(buy_id):
    buy = Buy.query.get_or_404(buy_id)
    if buy.author != current_user:
        abort(403)
    db.session.delete(buy)
    db.session.commit()
    flash('خرید مورد نظر حذف گردید', 'info')
    return redirect(url_for('home'))


@app.route('/buy/<int:buy_id>/update', methods=['GET', 'POST'])
@login_required
def update(buy_id):
    buy = Buy.query.get_or_404(buy_id)
    if buy.author != current_user:
        abort(403)
    form = BuyForm()
    if form.validate_on_submit():
        buy.desc = form.desc.data
        buy.price = form.price.data
        buy.category = form.category.data
        db.session.commit()
        flash('ویرایش با موفقیت انجام شد', 'info')
        return redirect(url_for('detail', buy_id=buy.id))
    elif request.method == 'GET':
        form.desc.data = buy.desc
        form.price.data = buy.price
        form.category.data = buy.category
    return render_template('update.html', form=form, title='ویرایش ' + buy.desc)
