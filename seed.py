from app import create_app, db
from app.models import Product, Store, User

app = create_app('dev')


def reset():
    with app.app_context():
        db.drop_all()
        setup()


def setup():
    with app.app_context():
        db.create_all()
        user = User.create("test@example.com", "test")
        db.session.add(user)
        store = Store(name="Test store", user=user)
        for i in range(2):
            prod = Product(name='Test Book v{}'.format((1 + i) * 2),
                           description='Book #{} in the series'.format(i + 1),
                           price_cents=100 * i + 1,
                           store=store)
            db.session.add(prod)
        db.session.commit()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Product': Product,
        'Store': Store,
        'setup': setup,
        'reset': reset
    }

# set FLASK_APP=seed.py
# flask run
# setup()

