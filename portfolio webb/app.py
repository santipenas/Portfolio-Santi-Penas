from flask import Flask, render_template, redirect, url_for, flash
from forms import ContactForm

app = Flask(__name__)
app.config.from_object('config.Config')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects/web')
def projects_web():
    return render_template('projects_web.html')

@app.route('/projects/data')
def projects_data():
    return render_template('projects_data.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Aquí manejarías el envío del formulario, por ejemplo, enviando un correo
        flash('Mensaje enviado correctamente.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
