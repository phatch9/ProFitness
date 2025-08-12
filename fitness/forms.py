from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, PasswordField, SubmitField, Form, validators, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from fitness.database import User, Post

min_name = 2
max_name = 20
min_pw = 10
max_pw = 100


# SignUp class validation form for input fields
class SignUpForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(min=min_name, max=max_name)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=min_name, max=max_name)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=min_pw, max=max_pw)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # Searching email on database and validate email of user input in
    # if the email has already registered, it will prompt a validation error
    # otherwise, it will put the user info to database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already used, please choose another email')


# Signin class validation for user log in
class SignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


# Item class validation for user input nutrition for calories output
class itemForm(FlaskForm):
    item = StringField("Food Item", validators=[DataRequired()])
    submit = SubmitField('Search')


# Item class validation for user input calories for output calories info
class calorieForm(FlaskForm):
    consumed = DecimalField("Calories consumed", validators=[])
    burned = DecimalField("Calories burned", validators=[])
    submit = SubmitField("Submit")


# Calories form
class CalorieWorkoutForm(FlaskForm):
    cardio_wo = DecimalField("Calories burned during above cardio workout", validators=[])
    strength_wo = DecimalField("sCalories burned during above anaerobic workout", validators=[])
    rest = DecimalField("Rest(Calories)", validators=[])
    submit = SubmitField("Submit")


# User Profile Form for editing user information
class UserProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=min_name, max=max_name)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=min_name, max=max_name)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password', validators=[Optional()])
    new_password = PasswordField('New Password', validators=[Optional()])
    confirm_new_password = PasswordField('Confirm New Password', validators=[Optional(), EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Update Profile')

    def __init__(self, original_email, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already used, please choose another email')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        # Only require password fields if any are filled
        if self.current_password.data or self.new_password.data or self.confirm_new_password.data:
            if not self.current_password.data:
                self.current_password.errors.append('Current password is required to change password.')
                return False
            if not self.new_password.data:
                self.new_password.errors.append('New password is required.')
                return False
            if not self.confirm_new_password.data:
                self.confirm_new_password.errors.append('Please confirm your new password.')
                return False
        return True


# Profile form class
class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password', validators=[Optional()])
    new_password = PasswordField('New Password', validators=[Optional()])
    confirm_new_password = PasswordField('Confirm New Password', validators=[Optional(), EqualTo('new_password', message='Passwords must match')])

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        # Only require password fields if any are filled
        if self.current_password.data or self.new_password.data or self.confirm_new_password.data:
            if not self.current_password.data:
                self.current_password.errors.append('Current password is required to change password.')
                return False
            if not self.new_password.data:
                self.new_password.errors.append('New password is required.')
                return False
            if not self.confirm_new_password.data:
                self.confirm_new_password.errors.append('Please confirm your new password.')
                return False
        return True


